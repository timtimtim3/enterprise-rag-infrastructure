/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: {
          base: "#0f0f12",
          sidebar: "#0a0a0d",
          surface: "#16161b",
          elevated: "#1e1e25",
          hover: "#1a1a22",
        },
        border: {
          subtle: "#23232e",
          DEFAULT: "#2d2d3a",
          strong: "#3d3d4e",
        },
        text: {
          primary: "#e4e4f0",
          secondary: "#7e7e9a",
          muted: "#4a4a60",
          inverse: "#0f0f12",
        },
        accent: {
          DEFAULT: "#f0a030",
          dim: "#2a1f08",
          hover: "#f5b350",
          muted: "#7a5018",
        },
      },
      fontFamily: {
        sans: ["DM Sans", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      fontSize: {
        "2xs": ["0.65rem", { lineHeight: "1rem" }],
      },
      animation: {
        "fade-in": "fadeIn 0.2s ease-out",
        "slide-up": "slideUp 0.2s ease-out",
        "pulse-dot": "pulseDot 1.4s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        slideUp: {
          from: { opacity: "0", transform: "translateY(8px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        pulseDot: {
          "0%, 80%, 100%": { opacity: "0.2", transform: "scale(0.8)" },
          "40%": { opacity: "1", transform: "scale(1)" },
        },
      },
    },
  },
  plugins: [],
};
