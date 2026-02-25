import {
  AlarmClock,
  ArrowBigRightDash,
  BellRing,
  DoorClosed,
  Eye,
  Hourglass,
  Layers,
  Users,
} from 'lucide-react';

const taxonomy = [
  {
    name: 'Scarcity',
    definition: 'Artificially constrained availability to trigger impulsive choice.',
    bias: 'Loss Aversion',
    example: 'Only 2 seats remaining at this price.',
    icon: Layers,
  },
  {
    name: 'Urgency',
    definition: 'Time pressure framing to reduce deliberation and comparison.',
    bias: 'Temporal Discounting',
    example: 'Offer expires in 05:00 minutes.',
    icon: AlarmClock,
  },
  {
    name: 'Social Proof',
    definition: 'Peer activity signals used as persuasive decision shortcuts.',
    bias: 'Bandwagon Effect',
    example: '1,200 users bought this in the last hour.',
    icon: Users,
  },
  {
    name: 'Misdirection',
    definition: 'Visual hierarchy manipulates attention toward a preferred option.',
    bias: 'Salience Bias',
    example: 'Bright “Accept” button, muted “Manage choices”.',
    icon: Eye,
  },
  {
    name: 'Sneaking',
    definition: 'Critical costs/consents hidden until later interaction steps.',
    bias: 'Default Effect',
    example: 'Pre-ticked add-on appears only at checkout.',
    icon: ArrowBigRightDash,
  },
  {
    name: 'Obstruction',
    definition: 'Intentional friction imposed on opt-out or cancellation tasks.',
    bias: 'Status Quo Bias',
    example: 'Cancellation requires multiple hidden pages.',
    icon: DoorClosed,
  },
  {
    name: 'Forced Action',
    definition: 'Users must perform unrelated action to access core service.',
    bias: 'Compliance Pressure',
    example: 'Create account to continue one-time purchase.',
    icon: Hourglass,
  },
  {
    name: 'Nagging',
    definition: 'Repeated prompts interrupt flow until user accepts option.',
    bias: 'Decision Fatigue',
    example: 'Popup reappears each page refresh until accepted.',
    icon: BellRing,
  },
];

const TaxonomyCards = () => {
  return (
    <section className="animate-fade-in-up">
      <h2 className="text-2xl font-semibold text-white">Behavioral Taxonomy (Table I)</h2>
      <p className="mt-2 text-sm text-slate-300">
        Classification of deceptive design strategies and their underlying cognitive exploitation.
      </p>

      <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {taxonomy.map(({ name, definition, bias, example, icon: Icon }) => (
          <article
            key={name}
            className="group rounded-xl border border-slate-800 bg-slate-900/70 p-4 shadow-soft transition-all duration-300 hover:-translate-y-1 hover:border-indigo-400/50"
          >
            <div className="mb-3 inline-flex rounded-md bg-indigo-500/15 p-2 text-indigo-300">
              <Icon size={18} />
            </div>
            <h3 className="text-lg font-semibold text-slate-100">{name}</h3>
            <p className="mt-2 text-sm leading-relaxed text-slate-300">{definition}</p>
            <p className="mt-3 text-xs font-medium uppercase tracking-wide text-cyan-300">Bias: {bias}</p>
            <p className="mt-2 rounded-md border border-slate-700 bg-slate-950/70 p-2 text-xs italic text-slate-300">
              {example}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
};

export default TaxonomyCards;
