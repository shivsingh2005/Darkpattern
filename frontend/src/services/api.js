const BASE_URL = import.meta.env.VITE_API_URL || '/api';

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
  const response = await fetch(`${BASE_URL}${path}`, {
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
      payload?.message ||
      payload?.error ||
      `Request failed with status ${response.status}`;
    throw new Error(String(detail));
  }

  return payload;
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
