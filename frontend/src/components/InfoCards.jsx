import { AlertTriangle, Clock3, Layers, ShieldAlert } from 'lucide-react';

const patterns = [
  {
    title: 'Confirm Shaming',
    description: 'Uses guilt or shame language to push users into an action.',
    example: 'No thanks, I hate saving money.',
    icon: ShieldAlert,
  },
  {
    title: 'Scarcity',
    description: 'Creates artificial scarcity to force fast decisions.',
    example: 'Only 2 left in stock!',
    icon: Layers,
  },
  {
    title: 'Urgency',
    description: 'Applies countdown pressure to reduce user reflection time.',
    example: 'Offer expires in 5 minutes!',
    icon: Clock3,
  },
  {
    title: 'Forced Continuity',
    description: 'Starts free but silently shifts to recurring charges.',
    example: 'Free trial today, auto-charged later.',
    icon: AlertTriangle,
  },
];

const InfoCards = () => {
  return (
    <section className="animate-fade-in-up">
      <h2 className="mb-5 text-xl font-semibold text-slate-100 md:text-2xl">Common Dark Patterns</h2>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {patterns.map(({ title, description, example, icon: Icon }) => (
          <article
            key={title}
            className="group rounded-xl border border-slate-800 bg-slate-900/70 p-5 shadow-soft transition-all duration-300 hover:-translate-y-1 hover:border-cyan-400/40"
          >
            <div className="mb-4 inline-flex rounded-lg bg-cyan-400/10 p-2 text-cyan-300 transition group-hover:bg-cyan-400/20">
              <Icon size={20} />
            </div>
            <h3 className="text-lg font-semibold text-white">{title}</h3>
            <p className="mt-2 text-sm text-slate-300">{description}</p>
            <p className="mt-3 rounded-md border border-slate-700 bg-slate-800/80 p-2 text-xs italic text-slate-200">
              Example: {example}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
};

export default InfoCards;
