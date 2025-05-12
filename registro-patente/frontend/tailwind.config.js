/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false,
  theme: {
    extend: {
      colors: {
        'accent': '#B0DAD7',
        'light-gray': '#EAEAEA',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
} 