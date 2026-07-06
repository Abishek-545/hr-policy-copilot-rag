/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: "#0f172a",
        brand: "#2563eb"
      }
    }
  },
  plugins: []
};
