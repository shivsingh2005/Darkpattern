import { useCallback, useEffect, useState } from 'react';
import Hero from '../components/Hero';
import ResearchOverview from '../components/ResearchOverview';
import TaxonomyCards from '../components/TaxonomyCards';
import LegalFramework from '../components/LegalFramework';
import Scanner from '../components/Scanner';
import ResultsDashboard from '../components/ResultsDashboard';
import Toast from '../components/Toast';

const Home = () => {
  const [results, setResults] = useState(null);
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
      <ResearchOverview />
      <TaxonomyCards />
      <LegalFramework />

      <section className="grid gap-6 lg:grid-cols-2">
        <Scanner
          onResults={setResults}
          onError={showError}
          onSuccess={showSuccess}
          clearError={clearError}
        />
        <ResultsDashboard results={results} />
      </section>

      <footer className="rounded-xl border border-slate-800 bg-slate-900/70 px-5 py-4 text-center text-xs text-slate-400">
        “A Behavioral and Legal Analysis of Dark Patterns” · Academic Policy-Tech Monitoring Interface
      </footer>
    </main>
  );
};

export default Home;
