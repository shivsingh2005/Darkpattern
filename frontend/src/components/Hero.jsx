import { ShieldCheck, Scale, BrainCircuit } from 'lucide-react';

const badges = [
  { label: 'Behavioral Science', icon: BrainCircuit },
  { label: 'Machine Learning', icon: ShieldCheck },
  { label: 'Regulatory Compliance', icon: Scale },
];

const Hero = () => {
  return (
    <section className="animate-fade-in-up surface relative overflow-hidden rounded-3xl px-6 py-14 md:px-12">
      <div className="absolute inset-0 bg-gradient-to-br from-emerald-100/60 via-transparent to-amber-100/70" />
      <div className="absolute -top-24 right-8 h-64 w-64 rounded-full border border-emerald-800/20 bg-emerald-500/10" />
      <div className="absolute -bottom-16 -left-20 h-56 w-56 rounded-full border border-amber-800/20 bg-amber-500/10" />

      <div className="relative z-10 max-w-4xl">
        <p className="mb-3 inline-flex rounded-full border border-emerald-300 bg-emerald-100/70 px-3 py-1 text-xs font-extrabold uppercase tracking-[0.22em] text-emerald-900">
          Academic AI Compliance Platform
        </p>
        <h1 className="text-4xl font-semibold leading-tight text-[#1f2830] md:text-6xl">
          Dark Pattern Detection &amp; Regulatory Analysis Platform
        </h1>
        <p className="mt-4 max-w-3xl text-base leading-relaxed text-[#435160] md:text-lg">
          An AI-powered system grounded in behavioral science, empirical research, and global
          regulatory frameworks.
        </p>

        <div className="mt-7 flex flex-wrap gap-2">
          {badges.map(({ label, icon: Icon }) => (
            <span
              key={label}
              className="inline-flex items-center gap-2 rounded-full border border-[#6e9f98] bg-[#e3f3f1] px-3 py-1 text-xs font-bold text-[#0a4a45]"
            >
              <Icon size={14} className="text-[#0f766e]" />
              {label}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Hero;
