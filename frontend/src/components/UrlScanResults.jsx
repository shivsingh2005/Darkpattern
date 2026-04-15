import { useState } from 'react';
import { Download } from 'lucide-react';
import ResultCard from './ResultCard';

const SOURCE_LABELS = {
  urgency_scarcity: 'Urgency/Scarcity Detector',
  timer_countdown: 'Timer/Countdown',
  popups_overlays: 'Popup/Overlay',
  cta_buttons: 'CTA Button',
  checkout_price_text: 'Checkout Text',
  social_proof: 'Social Proof',
};

const formatPercent = (value) => `${(Number(value || 0) * 100).toFixed(2)}%`;

const formatDateUtc = (date = new Date()) =>
  date.toISOString().replace('T', ' ').replace('Z', ' UTC');

const toTitle = (value = '') => {
  if (!value) return 'Unknown';
  return value
    .replace(/_/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/\b\w/g, (match) => match.toUpperCase());
};

const truncateText = (value, max = 260) => {
  const text = String(value || '').replace(/\s+/g, ' ').trim();
  if (!text) return 'N/A';
  if (text.length <= max) return text;
  return `${text.slice(0, max - 3)}...`;
};

const getRiskBand = (riskScore) => {
  if (riskScore >= 75) return 'High';
  if (riskScore >= 45) return 'Moderate';
  return 'Low';
};

const getSeverityLabel = (binaryConfidence, typeConfidence) => {
  const combined = Number(binaryConfidence || 0) * 0.6 + Number(typeConfidence || 0) * 0.4;
  if (combined >= 0.85) return 'Critical';
  if (combined >= 0.7) return 'High';
  if (combined >= 0.55) return 'Medium';
  return 'Low';
};

const buildReportContent = (data, allResults, darkFindings) => {
  const generatedAt = formatDateUtc();
  const totalScanned = Number(data.total_texts_scanned || allResults.length || 0);
  const darkCount = Number(data.dark_patterns_found || darkFindings.length || 0);
  const detectionRate = totalScanned > 0 ? darkCount / totalScanned : 0;

  const avgBinaryDark =
    darkFindings.length > 0
      ? darkFindings.reduce((sum, item) => sum + Number(item.binary_confidence || 0), 0) / darkFindings.length
      : 0;

  const avgTypeDark =
    darkFindings.length > 0
      ? darkFindings.reduce((sum, item) => sum + Number(item.type?.confidence || 0), 0) / darkFindings.length
      : 0;

  const riskScore = Math.min(
    100,
    Math.round(detectionRate * 55 * 100 + avgBinaryDark * 25 + avgTypeDark * 20)
  );
  const riskBand = getRiskBand(riskScore);

  const summaryLines = Object.entries(data.summary || {})
    .sort((a, b) => Number(b[1] || 0) - Number(a[1] || 0))
    .map(([category, count]) => `- ${category}: ${count}`);

  const sourceCountMap = darkFindings.reduce((acc, item) => {
    const key = item.source ? SOURCE_LABELS[item.source] || toTitle(item.source) : 'Unspecified Source';
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});

  const sourceLines = Object.entries(sourceCountMap)
    .sort((a, b) => b[1] - a[1])
    .map(([source, count]) => `- ${source}: ${count}`);

  const rankedFindings = [...darkFindings]
    .sort((a, b) => {
      const scoreA = Number(a.binary_confidence || 0) * 0.6 + Number(a.type?.confidence || 0) * 0.4;
      const scoreB = Number(b.binary_confidence || 0) * 0.6 + Number(b.type?.confidence || 0) * 0.4;
      return scoreB - scoreA;
    })
    .slice(0, 25);

  const findingLines = rankedFindings.flatMap((item, index) => {
    const allScores = Object.entries(item.type?.all_scores || {})
      .sort((a, b) => Number(b[1] || 0) - Number(a[1] || 0))
      .slice(0, 3)
      .map(([label, score]) => `${label} (${formatPercent(score)})`)
      .join(', ');

    const source = item.source ? SOURCE_LABELS[item.source] || toTitle(item.source) : 'Unspecified Source';
    const severity = getSeverityLabel(item.binary_confidence, item.type?.confidence);

    const lines = [
      `${index + 1}. Finding Snapshot`,
      `   Severity: ${severity}`,
      `   Source: ${source}`,
      `   Category: ${item.type?.category || 'Unknown'}`,
      `   Binary confidence: ${formatPercent(item.binary_confidence)}`,
      `   Category confidence: ${formatPercent(item.type?.confidence)}`,
      `   Text evidence: ${truncateText(item.text)}`,
      `   Alternative top categories: ${allScores || 'N/A'}`,
    ];

    if (item.explanation?.why) {
      lines.push(`   Why this is deceptive: ${item.explanation.why}`);
    }
    if (item.explanation?.psychological_mechanism) {
      lines.push(`   Psychological mechanism: ${item.explanation.psychological_mechanism}`);
    }
    if (item.explanation?.harm) {
      lines.push(`   Potential harm: ${item.explanation.harm}`);
    }
    if (item.explanation?.ethical_alternative) {
      lines.push(`   Ethical alternative: ${item.explanation.ethical_alternative}`);
    }

    return lines;
  });

  const nonDarkSamples = allResults
    .filter((item) => !item.is_dark_pattern)
    .slice(0, 5)
    .map(
      (item, index) =>
        `${index + 1}. ${truncateText(item.text, 180)} (binary confidence: ${formatPercent(item.binary_confidence)})`
    );

  const recommendations = [
    riskBand === 'High'
      ? '- Prioritize immediate UX remediation for high-confidence findings and add legal review before next release.'
      : '- Triage findings by severity and schedule iterative UI corrections in the next sprint.',
    '- Add pre-release checks for urgency, scarcity, and social-proof copy in marketing and checkout flows.',
    '- Validate user-facing consent and pricing disclosures against regional compliance requirements.',
    '- Re-scan after remediation and compare risk score trends over time.',
  ];

  return [
    'Dark Pattern Detection Detailed Website Report',
    '==============================================',
    `Generated at: ${generatedAt}`,
    `URL: ${data.url || ''}`,
    `Page title: ${data.page_title || ''}`,
    '',
    'Executive Summary',
    '-----------------',
    `Texts scanned: ${totalScanned}`,
    `Dark patterns found: ${darkCount}`,
    `Detection rate: ${(detectionRate * 100).toFixed(2)}%`,
    `Risk score: ${riskScore}/100 (${riskBand})`,
    `Average binary confidence (dark findings): ${formatPercent(avgBinaryDark)}`,
    `Average category confidence (dark findings): ${formatPercent(avgTypeDark)}`,
    '',
    'Category Summary',
    '----------------',
    ...summaryLines,
    '',
    'Source Distribution',
    '-------------------',
    ...(sourceLines.length ? sourceLines : ['No source-tagged dark findings available.']),
    '',
    'Prioritized Findings',
    '--------------------',
    ...(findingLines.length ? findingLines : ['No dark patterns detected.']),
    '',
    'Non-Dark Sample Observations',
    '----------------------------',
    ...(nonDarkSamples.length ? nonDarkSamples : ['No non-dark sample observations available.']),
    '',
    'Actionable Recommendations',
    '--------------------------',
    ...recommendations,
    '',
    'Raw payload (JSON)',
    '------------------',
    JSON.stringify(data, null, 2),
    '',
  ].join('\n');
};

const UrlScanResults = ({ data }) => {
  const [activeCategory, setActiveCategory] = useState('All');

  if (!data) {
    return (
      <section className="surface-alt rounded-2xl p-6">
        <p className="ink-soft text-sm">Run a URL scan to view detailed findings.</p>
      </section>
    );
  }

  const darkResults = (data.results || []).filter((item) => item.is_dark_pattern);
  const categoriesInResults = [...new Set(darkResults.map((item) => item.type?.category).filter(Boolean))];
  const filteredResults =
    activeCategory === 'All'
      ? darkResults
      : darkResults.filter((item) => item.type?.category === activeCategory);

  const summaryEntries = Object.entries(data.summary || {});

  const handleDownloadReport = () => {
    const fileSafeHost = (data.url || 'website-report').replace(/https?:\/\//, '').replace(/[^a-zA-Z0-9.-]/g, '_');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const fileName = `dark-pattern-report-${fileSafeHost}-${timestamp}.txt`;
    const reportContent = buildReportContent(data, data.results || [], darkResults);

    const blob = new Blob([reportContent], { type: 'text/plain;charset=utf-8' });
    const downloadUrl = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(downloadUrl);
  };

  return (
    <section className="surface space-y-6 rounded-2xl p-6">
      <div className="surface-alt rounded-xl p-4">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="text-2xl font-semibold text-slate-900">{data.page_title || data.url}</h2>
            <p className="ink-soft mt-1 text-sm">
              {data.dark_patterns_found} dark patterns found across {data.total_texts_scanned} texts scanned
            </p>
          </div>
          <button
            type="button"
            onClick={handleDownloadReport}
            className="inline-flex items-center gap-2 rounded-lg border border-[#75ada8] bg-[#dff3f0] px-3 py-2 text-xs font-extrabold uppercase tracking-wide text-[#0a4a45] transition hover:bg-[#cdeae6]"
          >
            <Download size={15} />
            Download Report
          </button>
        </div>
        <div className="mt-4 grid gap-2 sm:grid-cols-2">
          {summaryEntries.map(([category, count]) => (
            <div key={category}>
              <div className="mb-1 flex items-center justify-between text-xs text-[#5b6673]">
                <span>{category}</span>
                <span>{count}</span>
              </div>
              <div className="h-2 rounded-full bg-[#e3d5bd]">
                <div
                  className="h-2 rounded-full bg-gradient-to-r from-[#c18135] to-[#0f766e]"
                  style={{ width: `${Math.max(0, Math.min(100, Number(count) * 10))}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {(data.high_priority_findings || []).length > 0 && (
        <section className="space-y-3 rounded-xl border border-orange-300 bg-orange-50 p-4">
          <h3 className="text-sm font-semibold uppercase tracking-wide text-orange-800">High Priority Findings</h3>
          {(data.high_priority_findings || []).map((finding, index) => (
            <div key={`priority-${index}-${finding.text?.slice(0, 14)}`} className="space-y-2">
              <span className="inline-flex rounded-full border border-orange-300 bg-orange-100 px-2 py-1 text-xs font-semibold text-orange-800">
                {SOURCE_LABELS[finding.source] || finding.source}
              </span>
              <ResultCard result={finding} />
            </div>
          ))}
        </section>
      )}

      <section className="space-y-3">
        <h3 className="kicker">All Findings</h3>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setActiveCategory('All')}
            className={`rounded-full border px-3 py-1 text-xs font-semibold ${
              activeCategory === 'All'
                ? 'border-[#75ada8] bg-[#dff3f0] text-[#0a4a45]'
                : 'border-[#ccb68f] bg-[#f8efdf] text-[#6b5d45]'
            }`}
          >
            All
          </button>
          {categoriesInResults.map((category) => (
            <button
              key={category}
              type="button"
              onClick={() => setActiveCategory(category)}
              className={`rounded-full border px-3 py-1 text-xs font-semibold ${
                activeCategory === category
                  ? 'border-[#75ada8] bg-[#dff3f0] text-[#0a4a45]'
                  : 'border-[#ccb68f] bg-[#f8efdf] text-[#6b5d45]'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {filteredResults.length === 0 ? (
          <div className="rounded-lg border border-emerald-300 bg-emerald-50 p-4 text-sm text-emerald-800">
            No dark patterns found.
          </div>
        ) : (
          <div className="space-y-3">
            {filteredResults.map((finding, index) => (
              <ResultCard key={`result-${index}-${finding.text?.slice(0, 16)}`} result={finding} />
            ))}
          </div>
        )}
      </section>
    </section>
  );
};

export default UrlScanResults;
