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
    <section className="animate-fade-in-up surface rounded-2xl p-6">
      <div className="mb-6">
        <p className="kicker">Evidence Layer</p>
        <h2 className="text-3xl font-semibold text-slate-900">Research Overview</h2>
        <p className="ink-soft mt-2 text-sm">
          Interdisciplinary findings spanning behavioral economics, machine learning, and digital
          consumer protection policy.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {statCards.map(({ title, value, note, icon: Icon }) => (
          <article key={title} className="surface-alt rounded-xl p-4">
            <div className="mb-3 inline-flex rounded-md bg-[#dff3f0] p-2 text-[#0f766e]">
              <Icon size={18} />
            </div>
            <p className="text-xs uppercase tracking-wide text-[#7a6442]">{title}</p>
            <p className="mt-1 text-xl font-semibold text-slate-900">{value}</p>
            <p className="mt-1 text-xs text-[#5f6a78]">{note}</p>
          </article>
        ))}
      </div>

      <div className="surface-alt mt-6 rounded-xl p-4">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-[#7a6442]">
          Pattern Distribution Snapshot
        </h3>
        <div className="mt-4 space-y-3">
          {contributions.map((item) => (
            <div key={item.label}>
              <div className="mb-1 flex items-center justify-between text-xs text-[#5b6673]">
                <span>{item.label}</span>
                <span>{item.value}%</span>
              </div>
              <div className="h-2 rounded-full bg-[#e3d5bd]">
                <div
                  className="h-2 rounded-full bg-gradient-to-r from-[#c18135] to-[#0f766e]"
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
