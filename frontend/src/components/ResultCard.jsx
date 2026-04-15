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
    border: 'border-red-300/70',
    badge: 'bg-red-100 text-red-800 border-red-300',
    bar: 'from-red-400 to-red-500',
    description: 'Pressures users into actions by tying choices to unrelated outcomes.',
  },
  Misdirection: {
    border: 'border-orange-300/70',
    badge: 'bg-orange-100 text-orange-800 border-orange-300',
    bar: 'from-orange-400 to-orange-500',
    description: 'Draws attention toward preferred actions while hiding meaningful alternatives.',
  },
  Obstruction: {
    border: 'border-slate-300/80',
    badge: 'bg-slate-100 text-slate-800 border-slate-300',
    bar: 'from-slate-400 to-slate-500',
    description: 'Makes opt-out or cancellation difficult through friction and extra steps.',
  },
  Scarcity: {
    border: 'border-yellow-300/80',
    badge: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    bar: 'from-yellow-400 to-yellow-500',
    description: 'Uses stock or availability pressure to force quick, emotional decisions.',
  },
  Sneaking: {
    border: 'border-fuchsia-300/80',
    badge: 'bg-fuchsia-100 text-fuchsia-800 border-fuchsia-300',
    bar: 'from-fuchsia-400 to-fuchsia-500',
    description: 'Introduces hidden terms, defaults, or charges that users may not notice.',
  },
  'Social Proof': {
    border: 'border-blue-300/80',
    badge: 'bg-blue-100 text-blue-800 border-blue-300',
    bar: 'from-blue-400 to-blue-500',
    description: 'Leverages crowd behavior to nudge users into conforming choices.',
  },
  Urgency: {
    border: 'border-pink-300/80',
    badge: 'bg-pink-100 text-pink-800 border-pink-300',
    bar: 'from-pink-400 to-pink-500',
    description: 'Creates artificial time pressure to bypass careful evaluation.',
  },
  Unknown: {
    border: 'border-slate-300/80',
    badge: 'bg-slate-100 text-slate-700 border-slate-300',
    bar: 'from-slate-400 to-slate-500',
    description: 'Pattern detected but category confidence is unavailable.',
  },
};

const pct = (value) => `${((value || 0) * 100).toFixed(1)}%`;

const ResultCard = ({ result }) => {
  if (!result?.is_dark_pattern) {
    return (
      <article className="rounded-2xl border border-emerald-300 bg-emerald-50 p-5">
        <div className="mb-2 flex items-center gap-2 text-emerald-800">
          <CheckCircle2 size={18} />
          <h3 className="text-base font-semibold">No Dark Pattern Detected</h3>
        </div>
        <p className="text-sm text-emerald-900/80">This text appears clean based on the current classifier.</p>
        <p className="mt-3 text-xs font-semibold uppercase tracking-wide text-emerald-700">
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
    <article className={`rounded-2xl border bg-[#fffaf2] p-5 ${theme.border}`}>
      <div className="mb-3 flex items-start justify-between gap-3">
        <div className="flex items-center gap-2 text-rose-700">
          <ShieldAlert size={18} />
          <h3 className="text-base font-semibold">Dark Pattern Detected</h3>
        </div>
        <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${theme.badge}`}>{category}</span>
      </div>

      <blockquote className="rounded-xl border border-[#d7c8ad] bg-[#f8efdf] px-4 py-3 text-sm italic text-[#384654]">
        "{result.text}"
      </blockquote>

      <p className="mt-3 text-sm text-[#506071]">{theme.description}</p>

      <div className="mt-4 rounded-xl border border-[#d7c8ad] bg-[#f8efdf] p-3">
        <div className="mb-2 flex items-center justify-between text-xs uppercase tracking-wide text-[#6c5b42]">
          <span>Type confidence</span>
          <span>{pct(typeConfidence)}</span>
        </div>
        <div className="h-2 rounded-full bg-[#e3d5bd]">
          <div
            className={`h-2 rounded-full bg-gradient-to-r ${theme.bar}`}
            style={{ width: `${Math.max(0, Math.min(100, typeConfidence * 100))}%` }}
          />
        </div>
      </div>

      <details className="mt-4 rounded-xl border border-[#d7c8ad] bg-[#f8efdf] p-3">
        <summary className="cursor-pointer text-sm font-semibold text-[#23313d]">Show all scores</summary>
        <div className="mt-3 grid gap-2">
          {ALL_CATEGORIES.map((label) => {
            const score = Number(allScores[label] || 0);
            return (
              <div key={label}>
                <div className="mb-1 flex items-center justify-between text-xs text-[#5a6673]">
                  <span>{label}</span>
                  <span>{pct(score)}</span>
                </div>
                <div className="h-2 rounded-full bg-[#e3d5bd]">
                  <div
                    className="h-2 rounded-full bg-gradient-to-r from-[#c18135] to-[#0f766e]"
                    style={{ width: `${Math.max(0, Math.min(100, score * 100))}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </details>

      {explanation && (
        <div className="mt-4 grid gap-2 rounded-xl border border-[#d7c8ad] bg-[#f8efdf] p-3 text-sm text-[#354453]">
          <p>
            <span className="font-semibold text-[#1f2830]">Why it's a dark pattern:</span> {explanation.why}
          </p>
          <p>
            <span className="font-semibold text-[#1f2830]">Psychological mechanism:</span>{' '}
            {explanation.psychological_mechanism}
          </p>
          <p>
            <span className="font-semibold text-[#1f2830]">Harm:</span> {explanation.harm}
          </p>
          <div className="rounded-lg border border-emerald-300 bg-emerald-50 p-3 text-emerald-900">
            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-emerald-700">Ethical alternative</p>
            <p>{explanation.ethical_alternative}</p>
          </div>
        </div>
      )}
    </article>
  );
};

export default ResultCard;
