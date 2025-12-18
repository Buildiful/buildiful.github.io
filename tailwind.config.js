/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.html"],
  theme: {
    extend: {
      colors: {
        terminal: '#1f2933',
        terminalBorder: '#374151',
        accentBlue: '#67e8f9',
        accentRed: '#fca5a5',
      },
      boxShadow: {
        soft: '0 20px 60px rgba(0,0,0,0.4)',
      }
    },
  },
  plugins: [],
}
