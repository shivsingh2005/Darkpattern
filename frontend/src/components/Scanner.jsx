import { memo, useCallback, useMemo, useState } from 'react';
import { LoaderCircle, ScanSearch } from 'lucide-react';
import { detectFromText, detectFromUrl, extractErrorMessage } from '../services/api';

const tabs = [
  { id: 'url', label: 'Website Scan' },
  { id: 'text', label: 'Text Scan' },
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
  const [loading, setLoading] = useState(false);

  const isButtonDisabled = useMemo(() => {
    if (loading) return true;
    if (activeTab === 'url') return !url.trim();
    return !text.trim();
  }, [activeTab, loading, text, url]);

  const handleTabSwitch = useCallback(
    (tabId) => {
      if (loading) return;
      clearError();
      setActiveTab(tabId);
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
    try {
      const data = await detectFromUrl(trimmedUrl);
      onResults(data);
      onSuccess('Website scan completed.');
    } catch (error) {
      onError(extractErrorMessage(error));
    } finally {
      setLoading(false);
    }
  }, [clearError, onError, onResults, onSuccess, url]);

  const runTextScan = useCallback(async () => {
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
      onSuccess('Text scan completed.');
    } catch (error) {
      onError(extractErrorMessage(error));
    } finally {
      setLoading(false);
    }
  }, [clearError, onError, onResults, onSuccess, text]);

  return (
    <section className="animate-fade-in-up rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-soft">
      <div className="mb-5 flex items-center justify-between">
        <h2 className="text-xl font-semibold text-slate-100">Detection Engine</h2>
        <span className="text-xs uppercase tracking-wider text-slate-400">ML Inference</span>
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
                Scanning text...
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
