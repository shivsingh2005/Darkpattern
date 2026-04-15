import { ShieldCheck, Scale, BrainCircuit } from 'lucide-react';

const badges = [
  { label: 'Behavioral Science', icon: BrainCircuit },
  { label: 'Machine Learning', icon: ShieldCheck },
  { label: 'Regulatory Compliance', icon: Scale },
];

const Hero = () => {
  return (
    <section className="animate-fade-in-up surface relative overflow-hidden rounded-3xl px-6 py-8 md:px-8 md:py-9">
      <div className="absolute inset-0 bg-gradient-to-br from-emerald-100/60 via-transparent to-amber-100/70" />
      <div className="absolute -top-24 right-8 h-64 w-64 rounded-full border border-emerald-800/20 bg-emerald-500/10" />
      <div className="absolute -bottom-16 -left-20 h-56 w-56 rounded-full border border-amber-800/20 bg-amber-500/10" />

      <div className="relative z-10 grid gap-5 lg:grid-cols-12 lg:items-stretch">
        <div className="lg:col-span-8">
          <p className="mb-3 inline-flex rounded-full border border-emerald-300 bg-emerald-100/70 px-3 py-1 text-xs font-extrabold uppercase tracking-[0.22em] text-emerald-900">
            Academic AI Compliance Platform
          </p>
          <h1 className="text-3xl font-semibold leading-tight text-[#1f2830] md:text-5xl">
            Dark Pattern Detection &amp; Regulatory Analysis Platform
          </h1>
          <p className="mt-3 max-w-3xl text-base leading-relaxed text-[#435160] md:text-lg">
            AI-supported scanning for deceptive UX patterns, tied to behavioral triggers and legal exposure across global frameworks.
          </p>

          <div className="mt-5 flex flex-wrap gap-3">
            <a
              href="#workspace"
              className="inline-flex items-center rounded-full bg-[#0f766e] px-5 py-2.5 text-sm font-extrabold text-white transition hover:bg-[#0a4a45]"
            >
              Start Scanning
            </a>
            <a
              href="#research"
              className="inline-flex items-center rounded-full border border-[#ccb68f] bg-[#f8efdf] px-5 py-2.5 text-sm font-bold text-[#5e5139] transition hover:border-[#75ada8] hover:bg-[#dff3f0] hover:text-[#0a4a45]"
            >
              Explore Taxonomy
            </a>
            <a
              href="#policy"
              className="inline-flex items-center rounded-full border border-[#ccb68f] bg-[#f8efdf] px-5 py-2.5 text-sm font-bold text-[#5e5139] transition hover:border-[#75ada8] hover:bg-[#dff3f0] hover:text-[#0a4a45]"
            >
              View Legal Frameworks
            </a>
          </div>

          <div className="mt-5 flex flex-wrap gap-2">
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

        <div className="space-y-3 lg:col-span-4">
          <div className="surface-alt rounded-2xl p-4">
            <p className="kicker">Live Focus</p>
            <h3 className="mt-2 text-2xl font-semibold text-slate-900">Scan First</h3>
            <p className="ink-soft mt-1 text-sm">
              Start with website scan for broader surface coverage, then use text scan for targeted validation.
            </p>
          </div>

          <div className="surface-alt rounded-2xl p-4">
            <p className="kicker">Current Stack</p>
            <div className="mt-2 grid grid-cols-2 gap-2 text-sm font-semibold text-[#3f4c59]">
              <span className="rounded-lg border border-[#d8c7a9] bg-[#fff7e8] px-2 py-1">FastAPI API</span>
              <span className="rounded-lg border border-[#d8c7a9] bg-[#fff7e8] px-2 py-1">React + Vite</span>
              <span className="rounded-lg border border-[#d8c7a9] bg-[#fff7e8] px-2 py-1">3-Layer ML</span>
              <span className="rounded-lg border border-[#d8c7a9] bg-[#fff7e8] px-2 py-1">Policy Mapping</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
