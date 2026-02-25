import { memo, useCallback, useMemo, useState } from 'react';
import { LoaderCircle, SearchCheck } from 'lucide-react';
import { detectFromText, detectFromUrl, extractErrorMessage } from '../services/api';

const tabs = [
  { id: 'url', label: 'Scan Website' },
  { id: 'text', label: 'Scan Text' },
];

const isValidHttpUrl = (value) => {
  try {
    const parsed = new URL(value);
    return ['http:', 'https:'].includes(parsed.protocol) && Boolean(parsed.hostname);
  } catch {
    return false;
  }
};

const ScannerTabs = ({ onResults, onError, clearError, onSuccess }) => {
  const [activeTab, setActiveTab] = useState('url');
  const [url, setUrl] = useState('');
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);

  const isUrlTab = activeTab === 'url';
  const isButtonDisabled = useMemo(() => {
    if (loading) return true;
    if (isUrlTab) return !url.trim();
    return !text.trim();
  }, [loading, isUrlTab, text, url]);

  const handleTabChange = useCallback((tabId) => {
    setActiveTab(tabId);
    clearError();
  }, [clearError]);

  const scanWebsite = useCallback(async () => {
    const trimmedUrl = url.trim();
    if (!trimmedUrl) {
      onError('Please enter a valid URL.');
      return;
    }
    if (!isValidHttpUrl(trimmedUrl)) {
      onError('Invalid URL. Please include http:// or https://');
      return;
    }

    clearError();
    setLoading(true);
    try {
      const data = await detectFromUrl(trimmedUrl);
      onResults(data);
      onSuccess('Website scan completed successfully.');
    } catch (error) {
      onError(extractErrorMessage(error));
    } finally {
      setLoading(false);
    }
  }, [clearError, onError, onResults, onSuccess, url]);

  const scanText = useCallback(async () => {
    const trimmedText = text.trim();
    if (!trimmedText) {
      onError('Please enter text to analyze.');
      return;
    }

    clearError();
    setLoading(true);
    try {
      const data = await detectFromText(trimmedText);
      onResults(data);
      onSuccess('Text analysis completed successfully.');
    } catch (error) {
      onError(extractErrorMessage(error));
    } finally {
      setLoading(false);
    }
  }, [clearError, onError, onResults, onSuccess, text]);

  return (
    <section className="animate-fade-in-up rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-soft">
      <h2 className="mb-4 text-xl font-semibold text-white">Scanner</h2>

      <div className="mb-5 flex rounded-lg border border-slate-700 bg-slate-950/70 p-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => handleTabChange(tab.id)}
            disabled={loading}
            className={`flex-1 rounded-md px-4 py-2 text-sm font-medium transition ${
              activeTab === tab.id
                ? 'bg-cyan-500/20 text-cyan-200'
                : 'text-slate-300 hover:bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'url' ? (
        <div className="space-y-4">
          <input
            type="url"
            placeholder="https://example.com"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            disabled={loading}
            className="w-full rounded-lg border border-slate-700 bg-slate-950/70 px-4 py-3 text-sm text-slate-100 outline-none ring-cyan-400/40 transition focus:ring"
          />
          <button
            type="button"
            onClick={scanWebsite}
            disabled={isButtonDisabled}
            className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {loading ? (
              <>
                <LoaderCircle className="animate-spin" size={18} />
                Scanning website...
              </>
            ) : (
              <>
                <SearchCheck size={18} />
                Scan Website
              </>
            )}
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <textarea
            rows={6}
            placeholder="Only 2 left! Hurry!"
            value={text}
            onChange={(event) => setText(event.target.value)}
            disabled={loading}
            className="w-full resize-none rounded-lg border border-slate-700 bg-slate-950/70 px-4 py-3 text-sm text-slate-100 outline-none ring-cyan-400/40 transition focus:ring"
          />
          <button
            type="button"
            onClick={scanText}
            disabled={isButtonDisabled}
            className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {loading ? (
              <>
                <LoaderCircle className="animate-spin" size={18} />
                Scanning text...
              </>
            ) : (
              <>
                <SearchCheck size={18} />
                Analyze Text
              </>
            )}
          </button>
        </div>
      )}
    </section>
  );
};

export default memo(ScannerTabs);
