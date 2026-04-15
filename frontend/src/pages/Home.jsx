import { useCallback, useEffect, useState } from 'react';
import Hero from '../components/Hero';
import ResearchOverview from '../components/ResearchOverview';
import TaxonomyCards from '../components/TaxonomyCards';
import LegalFramework from '../components/LegalFramework';
import Scanner from '../components/Scanner';
import ResultCard from '../components/ResultCard';
import UrlScanResults from '../components/UrlScanResults';
import Toast from '../components/Toast';

const Home = () => {
  const [results, setResults] = useState(null);
  const [resultMode, setResultMode] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const clearError = useCallback(() => setError(''), []);
  const showError = useCallback((message) => {
    setSuccess('');
    setError(message);
  }, []);
  const showSuccess = useCallback((message) => {
    setError('');
    setSuccess(message);
  }, []);

  useEffect(() => {
    if (!error && !success) return undefined;
    const timeout = setTimeout(() => {
      setError('');
      setSuccess('');
    }, 2800);
    return () => clearTimeout(timeout);
  }, [error, success]);

  return (
    <main className="paper-grid relative mx-auto flex w-full max-w-[1200px] flex-col gap-8 px-4 py-8 md:px-8 md:py-12">
      <div className="pointer-events-none absolute -left-20 top-24 h-56 w-56 rounded-full bg-emerald-700/15 blur-3xl" />
      <div className="pointer-events-none absolute -right-12 top-[36rem] h-64 w-64 rounded-full bg-amber-600/20 blur-3xl" />

      <div className="fixed right-4 top-4 z-50 flex w-[min(92vw,360px)] flex-col gap-2">
        <Toast type="error" message={error} />
        <Toast type="success" message={success} />
      </div>

      <Hero />

      <section className="animate-fade-in-up surface relative rounded-3xl p-6 md:p-8">
        <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="kicker">Core Workspace</p>
            <h2 className="mt-2 text-3xl font-semibold text-slate-900 md:text-4xl">Detection Engine</h2>
            <p className="ink-soft mt-2 max-w-2xl text-sm md:text-base">
              Run URL or text analysis first, then review risk signals, categories, and explanations in one place.
            </p>
          </div>
          <div className="flex flex-wrap gap-2 text-xs font-semibold">
            <span className="accent-chip rounded-full px-3 py-1">Layer 1 Binary</span>
            <span className="accent-chip rounded-full px-3 py-1">Layer 2 Category</span>
            <span className="accent-chip rounded-full px-3 py-1">Layer 3 Explainability</span>
          </div>
        </div>

        <section className="grid gap-6 xl:grid-cols-12">
          <div className="xl:col-span-5">
            <Scanner
              onResults={(payload) => {
                setResultMode(payload.mode);
                setResults(payload.data);
              }}
              onError={showError}
              onSuccess={showSuccess}
              clearError={clearError}
            />
          </div>

          <section className="xl:col-span-7">
            {!results && (
              <div className="surface-alt rounded-2xl p-6 text-sm md:p-8">
                <p className="kicker">Results Panel</p>
                <h3 className="mt-2 text-2xl font-semibold text-slate-900">No Analysis Yet</h3>
                <p className="ink-soft mt-3 max-w-xl leading-relaxed">
                  Start with a website URL or text snippet in the Detection Engine to generate a structured dark-pattern analysis report.
                </p>
              </div>
            )}
            {results && resultMode === 'text' && <ResultCard result={results} />}
            {results && resultMode === 'url' && <UrlScanResults data={results} />}
          </section>
        </section>
      </section>

      <section className="space-y-6">
        <div className="surface rounded-2xl px-5 py-4">
          <p className="kicker">Research and Policy Context</p>
          <p className="ink-soft mt-2 text-sm">
            Supporting evidence, taxonomy references, and legal mappings for interpreting model output.
          </p>
        </div>
        <ResearchOverview />
        <TaxonomyCards />
        <LegalFramework />
      </section>

      <footer className="surface rounded-2xl px-5 py-4 text-center text-xs font-medium text-[#6c5b42]">
        “A Behavioral and Legal Analysis of Dark Patterns” · Academic Policy-Tech Monitoring Interface
      </footer>
    </main>
  );
};

export default Home;
