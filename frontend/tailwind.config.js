/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      boxShadow: {
        soft: '0 10px 30px rgba(2, 6, 23, 0.35)',
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { opacity: 0.8 },
          '50%': { opacity: 1 },
        },
      },
      animation: {
        pulseGlow: 'pulseGlow 2s ease-in-out infinite',
      },
    },
  },
  plugins: [],
};
