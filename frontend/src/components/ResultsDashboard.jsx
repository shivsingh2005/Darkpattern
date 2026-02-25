import { AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

const riskStyleMap = {
  Low: 'border-emerald-400/40 bg-emerald-500/10 text-emerald-300',
  Medium: 'border-amber-400/40 bg-amber-500/10 text-amber-300',
  High: 'border-rose-400/40 bg-rose-500/10 text-rose-300',
};

const progressBarMap = {
  Low: 'from-emerald-400 to-emerald-500',
  Medium: 'from-amber-300 to-amber-500',
  High: 'from-rose-400 to-rose-600',
};

const RiskIcon = ({ level }) => {
  if (level === 'High') return <ShieldAlert size={16} />;
  if (level === 'Medium') return <AlertTriangle size={16} />;
  return <CheckCircle2 size={16} />;
};

const ResultsDashboard = ({ results }) => {
  if (!results) {
    return (
      <section className="animate-fade-in-up rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-soft">
        <h2 className="text-xl font-semibold text-slate-100">Results Dashboard</h2>
        <p className="mt-3 text-sm text-slate-300">
          Awaiting scan output. Run the Detection Engine to view risk metrics and suspicious
          snippets.
        </p>
      </section>
    );
  }

  const riskLevel = results.risk_level || 'Low';
  const ratio = Number(results.dark_ratio || 0);

  return (
    <section className="animate-fade-in-up rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-soft">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h2 className="text-xl font-semibold text-slate-100">Results Dashboard</h2>
        <span
          className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wider ${riskStyleMap[riskLevel] || riskStyleMap.Low}`}
        >
          <RiskIcon level={riskLevel} />
          {riskLevel} Risk
        </span>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-400">Total Contents Scanned</p>
          <p className="mt-2 text-2xl font-semibold text-indigo-300">{results.total_contents_scanned}</p>
        </div>
        <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-400">Dark Patterns Detected</p>
          <p className="mt-2 text-2xl font-semibold text-rose-300">{results.total_dark_patterns_detected}</p>
        </div>
        <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-400">Dark Ratio</p>
          <p className="mt-2 text-2xl font-semibold text-amber-300">{ratio}%</p>
        </div>
      </div>

      <div className="mt-5 rounded-lg border border-slate-800 bg-slate-950/70 p-4">
        <div className="mb-2 flex items-center justify-between text-xs text-slate-300">
          <span>Dark Pattern Exposure Index</span>
          <span>{ratio}%</span>
        </div>
        <div className="h-2 rounded-full bg-slate-800">
          <div
            className={`h-2 rounded-full bg-gradient-to-r ${progressBarMap[riskLevel] || progressBarMap.Low}`}
            style={{ width: `${Math.max(0, Math.min(100, ratio))}%` }}
          />
        </div>
      </div>

      <div className="mt-6">
        <h3 className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-slate-300">
          Detected Text Snippets
        </h3>
        {!results.detected_texts?.length ? (
          <div className="rounded-lg border border-emerald-400/30 bg-emerald-500/10 p-4 text-sm text-emerald-300">
            No dark pattern snippets detected in the current scan.
          </div>
        ) : (
          <div className="space-y-3">
            {results.detected_texts.map((item, index) => (
              <article
                key={`${index}-${item.text?.slice(0, 18)}`}
                className="rounded-lg border border-rose-400/30 bg-rose-500/10 p-4"
              >
                <p className="text-sm text-rose-100">{item.text}</p>
                <p className="mt-2 text-xs font-semibold text-rose-300">
                  Confidence: {((item.confidence || 0) * 100).toFixed(2)}%
                </p>
              </article>
            ))}
          </div>
        )}
      </div>
    </section>
  );
};

export default ResultsDashboard;
