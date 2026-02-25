import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000,
});

const normalizeRiskLevel = (ratio) => {
  if (ratio >= 60) return 'High';
  if (ratio >= 25) return 'Medium';
  return 'Low';
};

const clampRatio = (ratio) => {
  if (typeof ratio !== 'number' || Number.isNaN(ratio)) return 0;
  return Math.max(0, Math.min(100, Number(ratio.toFixed(2))));
};

const normalizeResponse = (data) => {
  if (
    typeof data.total_contents_scanned === 'number' &&
    typeof data.total_dark_patterns_detected === 'number' &&
    typeof data.dark_ratio === 'number'
  ) {
    return {
      total_contents_scanned: data.total_contents_scanned,
      total_dark_patterns_detected: data.total_dark_patterns_detected,
      dark_ratio: clampRatio(data.dark_ratio),
      risk_level: data.risk_level || normalizeRiskLevel(data.dark_ratio),
      detected_texts: Array.isArray(data.detected_texts) ? data.detected_texts : [],
    };
  }

  if (typeof data.prediction === 'number') {
    const detected = data.prediction === 1;
    return {
      total_contents_scanned: 1,
      total_dark_patterns_detected: detected ? 1 : 0,
      dark_ratio: detected ? 100 : 0,
      risk_level: detected ? 'High' : 'Low',
      detected_texts: detected
        ? [{ text: 'Input text flagged as suspicious', confidence: data.confidence ?? 0 }]
        : [],
    };
  }

  throw new Error('Unexpected API response format');
};

export const detectFromUrl = async (url) => {
  const { data } = await api.post('/detect-from-url', { url });
  return normalizeResponse(data);
};

export const detectFromText = async (text) => {
  try {
    const { data } = await api.post('/detect-from-text', { text });
    return normalizeResponse(data);
  } catch (error) {
    if (error?.response?.status === 404) {
      const { data } = await api.post('/analyze', { text });
      return normalizeResponse(data);
    }
    throw error;
  }
};

export const extractErrorMessage = (error) => {
  const message = error?.response?.data?.message;
  if (typeof message === 'string' && message.trim()) return message;
  const detail = error?.response?.data?.detail;
  if (typeof detail === 'string' && detail.trim()) return detail;
  return 'Something went wrong. Please try again.';
};
