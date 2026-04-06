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

const buildReportContent = (data, findings) => {
  const generatedAt = new Date().toISOString();
  const summaryLines = Object.entries(data.summary || {}).map(([category, count]) => `- ${category}: ${count}`);

  const findingLines = findings.flatMap((item, index) => {
    const lines = [
      `${index + 1}. Text: ${item.text || ''}`,
      `   Category: ${item.type?.category || 'Unknown'}`,
      `   Binary confidence: ${formatPercent(item.binary_confidence)}`,
      `   Category confidence: ${formatPercent(item.type?.confidence)}`,
    ];

    if (item.explanation?.why) {
      lines.push(`   Why: ${item.explanation.why}`);
    }

    return lines;
  });

  return [
    'Dark Pattern Detection Website Report',
    '=====================================',
    `Generated at: ${generatedAt}`,
    `URL: ${data.url || ''}`,
    `Page title: ${data.page_title || ''}`,
    `Texts scanned: ${data.total_texts_scanned || 0}`,
    `Dark patterns found: ${data.dark_patterns_found || 0}`,
    '',
    'Category Summary',
    '----------------',
    ...summaryLines,
    '',
    'Detected Findings',
    '-----------------',
    ...(findingLines.length ? findingLines : ['No dark patterns detected.']),
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
      <section className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
        <p className="text-sm text-slate-300">Run a URL scan to view detailed findings.</p>
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
    const reportContent = buildReportContent(data, darkResults);

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
    <section className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-soft">
      <div className="rounded-xl border border-slate-700 bg-slate-950/70 p-4">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="text-lg font-semibold text-slate-100">{data.page_title || data.url}</h2>
            <p className="mt-1 text-sm text-slate-300">
              {data.dark_patterns_found} dark patterns found across {data.total_texts_scanned} texts scanned
            </p>
          </div>
          <button
            type="button"
            onClick={handleDownloadReport}
            className="inline-flex items-center gap-2 rounded-lg border border-cyan-400/40 bg-cyan-500/10 px-3 py-2 text-xs font-semibold uppercase tracking-wide text-cyan-200 transition hover:bg-cyan-500/20"
          >
            <Download size={15} />
            Download Report
          </button>
        </div>
        <div className="mt-4 grid gap-2 sm:grid-cols-2">
          {summaryEntries.map(([category, count]) => (
            <div key={category}>
              <div className="mb-1 flex items-center justify-between text-xs text-slate-300">
                <span>{category}</span>
                <span>{count}</span>
              </div>
              <div className="h-2 rounded-full bg-slate-700">
                <div
                  className="h-2 rounded-full bg-gradient-to-r from-cyan-400 to-indigo-400"
                  style={{ width: `${Math.max(0, Math.min(100, Number(count) * 10))}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {(data.high_priority_findings || []).length > 0 && (
        <section className="space-y-3 rounded-xl border border-orange-400/30 bg-orange-500/10 p-4">
          <h3 className="text-sm font-semibold uppercase tracking-wide text-orange-200">High Priority Findings</h3>
          {(data.high_priority_findings || []).map((finding, index) => (
            <div key={`priority-${index}-${finding.text?.slice(0, 14)}`} className="space-y-2">
              <span className="inline-flex rounded-full border border-orange-300/50 bg-orange-400/20 px-2 py-1 text-xs font-semibold text-orange-100">
                {SOURCE_LABELS[finding.source] || finding.source}
              </span>
              <ResultCard result={finding} />
            </div>
          ))}
        </section>
      )}

      <section className="space-y-3">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-200">All Findings</h3>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setActiveCategory('All')}
            className={`rounded-full border px-3 py-1 text-xs font-semibold ${
              activeCategory === 'All'
                ? 'border-cyan-400 bg-cyan-500/20 text-cyan-200'
                : 'border-slate-600 bg-slate-800 text-slate-300'
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
                  ? 'border-cyan-400 bg-cyan-500/20 text-cyan-200'
                  : 'border-slate-600 bg-slate-800 text-slate-300'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {filteredResults.length === 0 ? (
          <div className="rounded-lg border border-emerald-400/30 bg-emerald-500/10 p-4 text-sm text-emerald-200">
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
