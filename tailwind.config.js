// Tailwind 3.4.17 — ta pati versija, kurią davė cdn.tailwindcss.com.
// Klasės renkamos iš šablonų, JS ir Python (dalis HTML sudedama views/
// templatetags eilutėse). Pridėjus klasę — `npm run build:css`
// (./idiek.sh tai daro pats).
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
    './apps/**/*.py',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        // Rodo į tuos pačius CSS kintamuosius kaip base.html :root —
        // vienas akcento šaltinis (anksčiau tailwind.config base.html'e).
        primary: 'rgb(var(--accent-rgb) / <alpha-value>)',
        'primary-dark': 'rgb(var(--accent-hover-rgb) / <alpha-value>)',
        'primary-soft': 'rgb(var(--accent-soft-rgb) / <alpha-value>)',
      },
    },
  },
  plugins: [],
};
