import { BarChart3, Database, Microscope, Target } from 'lucide-react';

const statCards = [
  {
    title: 'Unified Taxonomy',
    value: '8 Core Classes',
    note: 'Behavioral + interface-level categorization',
    icon: Microscope,
  },
  {
    title: 'Empirical Dataset',
    value: '3,865 Entries',
    note: 'Annotated deceptive pattern corpus',
    icon: Database,
  },
  {
    title: 'Best ML Model',
    value: '~90% Accuracy',
    note: 'Logistic Regression with TF-IDF features',
    icon: Target,
  },
  {
    title: 'Dominant Patterns',
    value: '80%+ Coverage',
    note: 'Scarcity, Urgency, Social Proof',
    icon: BarChart3,
  },
];

const contributions = [
  { label: 'Scarcity', value: 34 },
  { label: 'Urgency', value: 27 },
  { label: 'Social Proof', value: 20 },
  { label: 'Others', value: 19 },
];

const ResearchOverview = () => {
  return (
    <section className="animate-fade-in-up rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-soft">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-white">Research Overview</h2>
        <p className="mt-2 text-sm text-slate-300">
          Interdisciplinary findings spanning behavioral economics, machine learning, and digital
          consumer protection policy.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {statCards.map(({ title, value, note, icon: Icon }) => (
          <article key={title} className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
            <div className="mb-3 inline-flex rounded-md bg-indigo-500/15 p-2 text-indigo-300">
              <Icon size={18} />
            </div>
            <p className="text-xs uppercase tracking-wide text-slate-400">{title}</p>
            <p className="mt-1 text-xl font-semibold text-slate-100">{value}</p>
            <p className="mt-1 text-xs text-slate-400">{note}</p>
          </article>
        ))}
      </div>

      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950/70 p-4">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-300">
          Pattern Distribution Snapshot
        </h3>
        <div className="mt-4 space-y-3">
          {contributions.map((item) => (
            <div key={item.label}>
              <div className="mb-1 flex items-center justify-between text-xs text-slate-300">
                <span>{item.label}</span>
                <span>{item.value}%</span>
              </div>
              <div className="h-2 rounded-full bg-slate-800">
                <div
                  className="h-2 rounded-full bg-gradient-to-r from-indigo-400 to-cyan-400"
                  style={{ width: `${item.value}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ResearchOverview;
