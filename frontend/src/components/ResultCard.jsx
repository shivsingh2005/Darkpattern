import { CheckCircle2, ShieldAlert } from 'lucide-react';

const ALL_CATEGORIES = [
  'Forced Action',
  'Misdirection',
  'Obstruction',
  'Scarcity',
  'Sneaking',
  'Social Proof',
  'Urgency',
];

const CATEGORY_THEME = {
  'Forced Action': {
    border: 'border-red-400/40',
    badge: 'bg-red-500/20 text-red-200 border-red-400/50',
    bar: 'from-red-400 to-red-600',
    description: 'Pressures users into actions by tying choices to unrelated outcomes.',
  },
  Misdirection: {
    border: 'border-orange-400/40',
    badge: 'bg-orange-500/20 text-orange-200 border-orange-400/50',
    bar: 'from-orange-300 to-orange-500',
    description: 'Draws attention toward preferred actions while hiding meaningful alternatives.',
  },
  Obstruction: {
    border: 'border-slate-400/40',
    badge: 'bg-slate-500/20 text-slate-200 border-slate-400/50',
    bar: 'from-slate-300 to-slate-500',
    description: 'Makes opt-out or cancellation difficult through friction and extra steps.',
  },
  Scarcity: {
    border: 'border-yellow-400/40',
    badge: 'bg-yellow-500/20 text-yellow-200 border-yellow-400/50',
    bar: 'from-yellow-300 to-yellow-500',
    description: 'Uses stock or availability pressure to force quick, emotional decisions.',
  },
  Sneaking: {
    border: 'border-purple-400/40',
    badge: 'bg-purple-500/20 text-purple-200 border-purple-400/50',
    bar: 'from-purple-300 to-purple-500',
    description: 'Introduces hidden terms, defaults, or charges that users may not notice.',
  },
  'Social Proof': {
    border: 'border-blue-400/40',
    badge: 'bg-blue-500/20 text-blue-200 border-blue-400/50',
    bar: 'from-blue-300 to-blue-500',
    description: 'Leverages crowd behavior to nudge users into conforming choices.',
  },
  Urgency: {
    border: 'border-pink-400/40',
    badge: 'bg-pink-500/20 text-pink-200 border-pink-400/50',
    bar: 'from-pink-300 to-pink-500',
    description: 'Creates artificial time pressure to bypass careful evaluation.',
  },
  Unknown: {
    border: 'border-slate-500/40',
    badge: 'bg-slate-700/40 text-slate-200 border-slate-500/50',
    bar: 'from-slate-300 to-slate-500',
    description: 'Pattern detected but category confidence is unavailable.',
  },
};

const pct = (value) => `${((value || 0) * 100).toFixed(1)}%`;

const ResultCard = ({ result }) => {
  if (!result?.is_dark_pattern) {
    return (
      <article className="rounded-xl border border-emerald-400/40 bg-emerald-500/10 p-5">
        <div className="mb-2 flex items-center gap-2 text-emerald-200">
          <CheckCircle2 size={18} />
          <h3 className="text-base font-semibold">No Dark Pattern Detected</h3>
        </div>
        <p className="text-sm text-emerald-100/90">This text appears clean based on the current classifier.</p>
        <p className="mt-3 text-xs font-semibold uppercase tracking-wide text-emerald-200">
          Binary confidence: {pct(result?.binary_confidence)}
        </p>
      </article>
    );
  }

  const category = result?.type?.category || 'Unknown';
  const theme = CATEGORY_THEME[category] || CATEGORY_THEME.Unknown;
  const typeConfidence = result?.type?.confidence || 0;
  const allScores = result?.type?.all_scores || {};
  const explanation = result?.explanation;

  return (
    <article className={`rounded-xl border bg-slate-950/70 p-5 ${theme.border}`}>
      <div className="mb-3 flex items-start justify-between gap-3">
        <div className="flex items-center gap-2 text-rose-200">
          <ShieldAlert size={18} />
          <h3 className="text-base font-semibold">Dark Pattern Detected</h3>
        </div>
        <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${theme.badge}`}>{category}</span>
      </div>

      <blockquote className="rounded-lg border border-slate-700 bg-slate-900/70 px-4 py-3 text-sm italic text-slate-200">
        "{result.text}"
      </blockquote>

      <p className="mt-3 text-sm text-slate-300">{theme.description}</p>

      <div className="mt-4 rounded-lg border border-slate-700 bg-slate-900/80 p-3">
        <div className="mb-2 flex items-center justify-between text-xs uppercase tracking-wide text-slate-300">
          <span>Type confidence</span>
          <span>{pct(typeConfidence)}</span>
        </div>
        <div className="h-2 rounded-full bg-slate-700">
          <div
            className={`h-2 rounded-full bg-gradient-to-r ${theme.bar}`}
            style={{ width: `${Math.max(0, Math.min(100, typeConfidence * 100))}%` }}
          />
        </div>
      </div>

      <details className="mt-4 rounded-lg border border-slate-700 bg-slate-900/80 p-3">
        <summary className="cursor-pointer text-sm font-semibold text-slate-200">Show all scores</summary>
        <div className="mt-3 grid gap-2">
          {ALL_CATEGORIES.map((label) => {
            const score = Number(allScores[label] || 0);
            return (
              <div key={label}>
                <div className="mb-1 flex items-center justify-between text-xs text-slate-300">
                  <span>{label}</span>
                  <span>{pct(score)}</span>
                </div>
                <div className="h-2 rounded-full bg-slate-700">
                  <div
                    className="h-2 rounded-full bg-gradient-to-r from-cyan-400 to-indigo-400"
                    style={{ width: `${Math.max(0, Math.min(100, score * 100))}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </details>

      {explanation && (
        <div className="mt-4 grid gap-2 rounded-lg border border-slate-700 bg-slate-900/80 p-3 text-sm text-slate-200">
          <p>
            <span className="font-semibold text-slate-100">Why it's a dark pattern:</span> {explanation.why}
          </p>
          <p>
            <span className="font-semibold text-slate-100">Psychological mechanism:</span>{' '}
            {explanation.psychological_mechanism}
          </p>
          <p>
            <span className="font-semibold text-slate-100">Harm:</span> {explanation.harm}
          </p>
          <div className="rounded-md border border-emerald-400/40 bg-emerald-500/10 p-3 text-emerald-100">
            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-emerald-300">Ethical alternative</p>
            <p>{explanation.ethical_alternative}</p>
          </div>
        </div>
      )}
    </article>
  );
};

export default ResultCard;
