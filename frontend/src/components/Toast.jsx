import { AlertTriangle, CheckCircle2 } from 'lucide-react';

const styles = {
  success: 'border-emerald-400/40 bg-emerald-500/15 text-emerald-200',
  error: 'border-rose-400/40 bg-rose-500/15 text-rose-100',
};

const Toast = ({ type = 'success', message }) => {
  if (!message) return null;

  const Icon = type === 'error' ? AlertTriangle : CheckCircle2;
  return (
    <div
      className={`pointer-events-auto flex items-start gap-2 rounded-lg border px-4 py-3 shadow-soft backdrop-blur-sm ${styles[type] || styles.success}`}
      role="status"
      aria-live="polite"
    >
      <Icon size={18} className="mt-0.5" />
      <p className="text-sm font-medium">{message}</p>
    </div>
  );
};

export default Toast;
