import { ShieldCheck, Scale, BrainCircuit } from 'lucide-react';

const badges = [
  { label: 'Behavioral Science', icon: BrainCircuit },
  { label: 'Machine Learning', icon: ShieldCheck },
  { label: 'Regulatory Compliance', icon: Scale },
];

const Hero = () => {
  return (
    <section className="animate-fade-in-up relative overflow-hidden rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 via-indigo-950/70 to-slate-900 px-6 py-14 shadow-soft md:px-12">
      <div className="absolute -top-20 -right-20 h-64 w-64 rounded-full bg-indigo-500/20 blur-3xl" />
      <div className="absolute -bottom-24 -left-10 h-64 w-64 rounded-full bg-blue-500/20 blur-3xl" />
      <div className="relative z-10 max-w-4xl">
        <p className="mb-3 inline-flex rounded-full border border-indigo-300/30 bg-indigo-400/10 px-3 py-1 text-xs font-medium uppercase tracking-[0.22em] text-indigo-200">
          Academic AI Compliance Platform
        </p>
        <h1 className="text-3xl font-semibold leading-tight text-white md:text-5xl">
          Dark Pattern Detection &amp; Regulatory Analysis Platform
        </h1>
        <p className="mt-4 max-w-3xl text-base leading-relaxed text-slate-200 md:text-lg">
          An AI-powered system grounded in behavioral science, empirical research, and global
          regulatory frameworks.
        </p>

        <div className="mt-7 flex flex-wrap gap-2">
          {badges.map(({ label, icon: Icon }) => (
            <span
              key={label}
              className="inline-flex items-center gap-2 rounded-full border border-slate-600 bg-slate-900/60 px-3 py-1 text-xs font-medium text-slate-200"
            >
              <Icon size={14} className="text-indigo-300" />
              {label}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Hero;
