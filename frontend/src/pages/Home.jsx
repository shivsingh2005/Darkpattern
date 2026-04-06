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
    <main className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-4 py-8 md:px-8 md:py-12">
      <div className="fixed right-4 top-4 z-50 flex w-[min(92vw,360px)] flex-col gap-2">
        <Toast type="error" message={error} />
        <Toast type="success" message={success} />
      </div>

      <Hero />

      <section className="animate-fade-in-up rounded-2xl border border-slate-800 bg-slate-900/60 p-6 shadow-soft md:p-8">
        <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-300">Core Workspace</p>
            <h2 className="mt-2 text-2xl font-semibold text-white md:text-3xl">Detection Engine</h2>
            <p className="mt-2 max-w-2xl text-sm text-slate-300 md:text-base">
              Run URL or text analysis first, then review risk signals, categories, and explanations in one place.
            </p>
          </div>
          <div className="flex gap-2 text-xs text-slate-200">
            <span className="rounded-full border border-slate-600 bg-slate-800/80 px-3 py-1">Layer 1 Binary</span>
            <span className="rounded-full border border-slate-600 bg-slate-800/80 px-3 py-1">Layer 2 Category</span>
            <span className="rounded-full border border-slate-600 bg-slate-800/80 px-3 py-1">Layer 3 Explainability</span>
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
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-6 text-sm text-slate-300 shadow-soft md:p-8">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">Results Panel</p>
                <h3 className="mt-2 text-xl font-semibold text-slate-100">No Analysis Yet</h3>
                <p className="mt-3 max-w-xl leading-relaxed text-slate-300">
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
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 px-5 py-4">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-200">Research and Policy Context</p>
          <p className="mt-2 text-sm text-slate-300">
            Supporting evidence, taxonomy references, and legal mappings for interpreting model output.
          </p>
        </div>
        <ResearchOverview />
        <TaxonomyCards />
        <LegalFramework />
      </section>

      <footer className="rounded-xl border border-slate-800 bg-slate-900/70 px-5 py-4 text-center text-xs text-slate-400">
        “A Behavioral and Legal Analysis of Dark Patterns” · Academic Policy-Tech Monitoring Interface
      </footer>
    </main>
  );
};

export default Home;
