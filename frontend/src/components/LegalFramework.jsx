const frameworks = [
  {
    region: 'United States',
    flag: '🇺🇸',
    points: ['FTC enforcement actions', 'False urgency scrutiny', 'Hidden fee prohibition trends'],
  },
  {
    region: 'European Union',
    flag: '🇪🇺',
    points: [
      'Digital Services Act (Article 25)',
      'GDPR consent integrity requirements',
      'AI Act risk-based interface restrictions',
    ],
  },
  {
    region: 'India',
    flag: '🇮🇳',
    points: [
      'Consumer Protection Act, 2019',
      'CCPA Dark Pattern Guidelines, 2023',
      '2025 enforcement advisory posture',
    ],
  },
];

const LegalFramework = () => {
  return (
    <section className="animate-fade-in-up rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-soft">
      <h2 className="text-2xl font-semibold text-white">Global Regulatory Response</h2>
      <p className="mt-2 text-sm text-slate-300">
        Policy landscape for deceptive interface interventions and platform accountability.
      </p>

      <div className="mt-5 grid gap-4 lg:grid-cols-3">
        {frameworks.map((item) => (
          <article key={item.region} className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
            <h3 className="text-lg font-semibold text-slate-100">
              <span className="mr-2" role="img" aria-label={item.region}>
                {item.flag}
              </span>
              {item.region}
            </h3>
            <ul className="mt-3 space-y-2 text-sm text-slate-300">
              {item.points.map((point) => (
                <li key={point} className="flex gap-2">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-indigo-300" />
                  <span>{point}</span>
                </li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
};

export default LegalFramework;
