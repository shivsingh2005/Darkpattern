import { memo, useCallback, useEffect, useMemo, useState } from 'react';
import { LoaderCircle, ScanSearch } from 'lucide-react';
import { analyzeText, analyzeUrl } from '../services/api';

const tabs = [
  { id: 'url', label: 'Website Scan' },
  { id: 'text', label: 'Text Scan' },
];

const URL_STAGES = [
  { limit: 20, label: 'Launching browser...' },
  { limit: 50, label: 'Loading page...' },
  { limit: 70, label: 'Extracting content...' },
  { limit: 90, label: 'Running detection...' },
  { limit: 100, label: 'Generating insights...' },
];

const isValidHttpUrl = (value) => {
  try {
    const parsed = new URL(value);
    return ['http:', 'https:'].includes(parsed.protocol) && Boolean(parsed.hostname);
  } catch {
    return false;
  }
};

const Scanner = ({ onResults, onError, onSuccess, clearError }) => {
  const [activeTab, setActiveTab] = useState('url');
  const [url, setUrl] = useState('');
  const [text, setText] = useState('');
  const [explain, setExplain] = useState(true);
  const [loading, setLoading] = useState(false);
  const [urlProgress, setUrlProgress] = useState(0);

  const isButtonDisabled = useMemo(() => {
    if (loading) return true;
    if (activeTab === 'url') return !url.trim();
    return !text.trim();
  }, [activeTab, loading, text, url]);

  const urlStageLabel = useMemo(() => {
    const stage = URL_STAGES.find((item) => urlProgress <= item.limit);
    return stage ? stage.label : 'Generating insights...';
  }, [urlProgress]);

  useEffect(() => {
    if (!loading || activeTab !== 'url') return undefined;
    const timer = setInterval(() => {
      setUrlProgress((current) => {
        if (current >= 95) return current;
        const step = current < 20 ? 5 : current < 50 ? 4 : current < 70 ? 3 : 2;
        return Math.min(95, current + step);
      });
    }, 350);
    return () => clearInterval(timer);
  }, [activeTab, loading]);

  const handleTabSwitch = useCallback(
    (tabId) => {
      if (loading) return;
      clearError();
      setActiveTab(tabId);
      setUrlProgress(0);
    },
    [clearError, loading]
  );

  const runWebsiteScan = useCallback(async () => {
    const trimmedUrl = url.trim();
    if (!trimmedUrl) {
      onError('Please enter a URL to scan.');
      return;
    }
    if (!isValidHttpUrl(trimmedUrl)) {
      onError('Invalid URL format. Use http:// or https://');
      return;
    }

    clearError();
    setLoading(true);
    setUrlProgress(5);
    try {
      const data = await analyzeUrl(trimmedUrl, explain);
      setUrlProgress(100);
      onResults({ mode: 'url', data });
      onSuccess('Website scan completed.');
    } catch (error) {
      onError(error?.message || 'Failed to scan website.');
    } finally {
      setLoading(false);
      setTimeout(() => setUrlProgress(0), 600);
    }
  }, [clearError, explain, onError, onResults, onSuccess, url]);

  const runTextScan = useCallback(async () => {
    const trimmedText = text.trim();
    if (!trimmedText) {
      onError('Please enter text to analyze.');
      return;
    }

    clearError();
    setLoading(true);
    try {
      const data = await analyzeText(trimmedText, explain);
      onResults({ mode: 'text', data });
      onSuccess('Text scan completed.');
    } catch (error) {
      onError(error?.message || 'Failed to analyze text.');
    } finally {
      setLoading(false);
    }
  }, [clearError, explain, onError, onResults, onSuccess, text]);

  return (
    <section className="animate-fade-in-up rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-soft">
      <div className="mb-5 flex items-center justify-between">
        <h2 className="text-xl font-semibold text-slate-100">Detection Engine</h2>
        <span className="text-xs uppercase tracking-wider text-slate-400">3-Layer Pipeline</span>
      </div>

      <div className="mb-5 flex rounded-lg border border-slate-700 bg-slate-950/80 p-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            type="button"
            disabled={loading}
            onClick={() => handleTabSwitch(tab.id)}
            className={`flex-1 rounded-md px-4 py-2 text-sm font-medium transition ${
              activeTab === tab.id
                ? 'bg-indigo-500/20 text-indigo-200'
                : 'text-slate-300 hover:bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <label className="mb-4 flex items-center gap-2 text-sm text-slate-300">
        <input
          type="checkbox"
          checked={explain}
          disabled={loading}
          onChange={(event) => setExplain(event.target.checked)}
          className="h-4 w-4 accent-cyan-400"
        />
        Generate AI explanation (Layer 3)
      </label>

      {activeTab === 'url' ? (
        <div className="space-y-4">
          <input
            type="url"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            placeholder="https://example.com"
            disabled={loading}
            className="w-full rounded-lg border border-slate-700 bg-slate-950/70 px-4 py-3 text-sm text-slate-100 outline-none ring-indigo-400/40 transition focus:ring"
          />
          <button
            type="button"
            onClick={runWebsiteScan}
            disabled={isButtonDisabled}
            className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-65"
          >
            {loading ? (
              <>
                <LoaderCircle className="animate-spin" size={18} />
                Scanning website...
              </>
            ) : (
              <>
                <ScanSearch size={18} />
                Scan Website
              </>
            )}
          </button>

          {loading && (
            <div className="rounded-lg border border-slate-700 bg-slate-950/70 p-4">
              <div className="mb-2 flex items-center justify-between text-xs text-slate-300">
                <span>{urlStageLabel}</span>
                <span>{Math.min(100, urlProgress)}%</span>
              </div>
              <div className="h-2 rounded-full bg-slate-800">
                <div
                  className="h-2 rounded-full bg-gradient-to-r from-cyan-400 to-indigo-400"
                  style={{ width: `${Math.min(100, urlProgress)}%` }}
                />
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          <textarea
            rows={6}
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Only 2 left! Hurry!"
            disabled={loading}
            className="w-full resize-none rounded-lg border border-slate-700 bg-slate-950/70 px-4 py-3 text-sm text-slate-100 outline-none ring-indigo-400/40 transition focus:ring"
          />
          <button
            type="button"
            onClick={runTextScan}
            disabled={isButtonDisabled}
            className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-65"
          >
            {loading ? (
              <>
                <LoaderCircle className="animate-spin" size={18} />
                Analyzing text...
              </>
            ) : (
              <>
                <ScanSearch size={18} />
                Analyze Text
              </>
            )}
          </button>
        </div>
      )}
    </section>
  );
};

export default memo(Scanner);
