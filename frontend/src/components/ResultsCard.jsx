import { AlertCircle, CheckCircle2, ShieldAlert } from 'lucide-react';

const riskStyles = {
  Low: 'border-emerald-400/40 bg-emerald-500/10 text-emerald-300',
  Medium: 'border-amber-400/40 bg-amber-500/10 text-amber-300',
  High: 'border-rose-400/40 bg-rose-500/10 text-rose-300',
};

const RiskIcon = ({ risk }) => {
  if (risk === 'High') return <ShieldAlert size={18} />;
  if (risk === 'Medium') return <AlertCircle size={18} />;
  return <CheckCircle2 size={18} />;
};

const ResultsCard = ({ results }) => {
  if (!results) {
    return (
      <section className="animate-fade-in-up rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-soft">
        <h2 className="text-xl font-semibold text-white">Scan Results</h2>
        <p className="mt-3 text-sm text-slate-300">
          Run a website scan or text analysis to see detection metrics and suspicious content.
        </p>
      </section>
    );
  }

  const riskLevel = results.risk_level || 'Low';
  const detectedTexts = results.detected_texts || [];

  return (
    <section className="animate-fade-in-up rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-soft">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h2 className="text-xl font-semibold text-white">Scan Results</h2>
        <span
          className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm font-medium ${riskStyles[riskLevel] || riskStyles.Low}`}
        >
          <RiskIcon risk={riskLevel} />
          Risk: {riskLevel}
        </span>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-400">Total Contents Scanned</p>
          <p className="mt-2 text-2xl font-bold text-cyan-300">{results.total_contents_scanned}</p>
        </div>
        <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-400">Dark Patterns Detected</p>
          <p className="mt-2 text-2xl font-bold text-rose-300">{results.total_dark_patterns_detected}</p>
        </div>
        <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-400">Dark Ratio</p>
          <p className="mt-2 text-2xl font-bold text-amber-300">{results.dark_ratio}%</p>
        </div>
      </div>

      <div className="mt-6">
        <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-slate-300">Suspicious Texts</h3>
        {detectedTexts.length === 0 ? (
          <div className="rounded-lg border border-emerald-400/30 bg-emerald-500/10 p-4 text-sm text-emerald-300">
            No suspicious chunks detected in this scan.
          </div>
        ) : (
          <div className="space-y-3">
            {detectedTexts.map((item, index) => (
              <div
                key={`${index}-${item.text?.slice(0, 16)}`}
                className="rounded-lg border border-rose-400/30 bg-rose-500/10 p-4"
              >
                <p className="text-sm text-rose-100">{item.text}</p>
                <p className="mt-2 text-xs font-medium text-rose-300">
                  Confidence: {((item.confidence || 0) * 100).toFixed(2)}%
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
};

export default ResultsCard;
