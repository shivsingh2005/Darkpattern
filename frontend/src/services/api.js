const DEFAULT_REMOTE_API_URL = 'https://darkpattern-1.onrender.com';

const normalizeBaseUrl = (value) => {
  if (!value) return '';
  const trimmed = String(value).trim();
  if (!trimmed) return '';
  // Avoid accidental double-prefixing when users set VITE_API_URL like ".../api".
  return trimmed.replace(/\/+$/, '').replace(/\/api$/, '');
};

const envBaseUrl = normalizeBaseUrl(import.meta.env.VITE_API_URL);
const isLocalHost =
  typeof window !== 'undefined' && ['localhost', '127.0.0.1'].includes(window.location.hostname);

const BASE_URLS = (() => {
  // If env URL is explicitly set, respect it as the single source of truth.
  if (envBaseUrl) {
    return [envBaseUrl];
  }

  // In local development, try proxy first and fall back to the deployed API.
  if (isLocalHost) {
    return ['/api', DEFAULT_REMOTE_API_URL];
  }

  return [DEFAULT_REMOTE_API_URL];
})();

/**
 * @typedef {{
 *   category: string,
 *   confidence: number,
 *   all_scores: Record<string, number>
 * }} TypeClassification
 */

/**
 * @typedef {{
 *   why: string,
 *   psychological_mechanism: string,
 *   harm: string,
 *   ethical_alternative: string
 * }} LlmExplanation
 */

/**
 * @typedef {{
 *   text: string,
 *   is_dark_pattern: boolean,
 *   binary_confidence: number,
 *   type: TypeClassification | null,
 *   explanation: LlmExplanation | null
 * }} AnalyzeResponse
 */

/**
 * @typedef {{
 *   text: string,
 *   source?: 'urgency_scarcity' | 'popups_overlays' | 'cta_buttons' | 'checkout_price_text' | 'social_proof',
 *   is_dark_pattern: boolean,
 *   binary_confidence: number,
 *   type: TypeClassification | null,
 *   explanation: LlmExplanation | null
 * }} UrlFinding
 */

/**
 * @typedef {{
 *   url: string,
 *   page_title: string,
 *   total_texts_scanned: number,
 *   dark_patterns_found: number,
 *   high_priority_findings: UrlFinding[],
 *   results: UrlFinding[],
 *   summary: Record<string, number>
 * }} UrlAnalyzeResponse
 */

async function requestJson(path, body) {
  let lastError = null;

  for (let index = 0; index < BASE_URLS.length; index += 1) {
    const baseUrl = BASE_URLS[index];
    const hasFallback = index < BASE_URLS.length - 1;

    try {
      const response = await fetch(`${baseUrl}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const text = await response.text();
      let payload = null;

      if (text) {
        try {
          payload = JSON.parse(text);
        } catch {
          payload = null;
        }
      }

      if (!response.ok) {
        const detail =
          payload?.detail ||
          payload?.error?.detail ||
          payload?.message ||
          payload?.error ||
          `Request failed with status ${response.status}`;

        const serverError = new Error(String(detail));

        // If a local proxy/backend is missing or unhealthy, try the next base URL.
        if (hasFallback && (response.status === 404 || response.status >= 500)) {
          lastError = serverError;
          continue;
        }

        throw serverError;
      }

      return payload;
    } catch (error) {
      if (hasFallback && error instanceof TypeError) {
        // Network failure (for example, local backend not running).
        lastError = error;
        continue;
      }
      throw error;
    }
  }

  if (lastError) {
    throw lastError;
  }

  throw new Error('Request failed');
}

/**
 * @param {string} text
 * @param {boolean} [explain=true]
 * @returns {Promise<AnalyzeResponse>}
 */
export async function analyzeText(text, explain = true) {
  return requestJson('/analyze', { text, explain });
}

/**
 * @param {string} url
 * @param {boolean} [explain=true]
 * @returns {Promise<UrlAnalyzeResponse>}
 */
export async function analyzeUrl(url, explain = true) {
  return requestJson('/detect-from-url', { url, explain });
}
