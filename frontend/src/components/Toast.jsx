import { AlertTriangle, CheckCircle2 } from 'lucide-react';

const styles = {
  success: 'border-emerald-300 bg-emerald-50 text-emerald-800',
  error: 'border-rose-300 bg-rose-50 text-rose-800',
};

const Toast = ({ type = 'success', message }) => {
  if (!message) return null;

  const Icon = type === 'error' ? AlertTriangle : CheckCircle2;
  return (
    <div
      className={`pointer-events-auto flex items-start gap-2 rounded-lg border px-4 py-3 shadow-lg backdrop-blur-sm ${styles[type] || styles.success}`}
      role="status"
      aria-live="polite"
    >
      <Icon size={18} className="mt-0.5" />
      <p className="text-sm font-medium">{message}</p>
    </div>
  );
};

export default Toast;
