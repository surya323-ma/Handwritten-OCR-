/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        panel: "#0f1524",
        panelLight: "#161d31",
        border: "#232b40",
        accent: "#22d3ee",
      },
    },
  },
  plugins: [],
};
