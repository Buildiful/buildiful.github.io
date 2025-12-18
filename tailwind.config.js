/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html"],
  theme: {
    extend: {
      colors: {
        terminal: '#1c1c1c',
        terminalBorder: '#2a2a2a',
        accentBlue: '#e5e7eb',
        accentRed: '#d4d4d4',
      },
      boxShadow: {
        soft: '0 20px 60px rgba(0,0,0,0.4)',
      }
    },
  },
  plugins: [],
}
