# Генератор дизайнов (исходники)

- `lib.py` — текст → кривые (uharfbuzz + fontTools), арочный текст, сплайны, халфтон.
- `shapes.py` — фирменные формы: манта (заливка и одной линией), яхта, скала Келингкинг, плоский эскиз боди.
- `designs.py` — 10 дизайнов (функции d01…d10), палитра и Pantone-соответствия.
- `build.py` → `out/designs/*/artwork.svg|preview.png`, `manifest.json`.
- `mockup.js` (Playwright) — наложение артов на фото (1 мм = 2,85 px, multiply).
- `techdraw.py`, `labels.py`, `techpack.py`, `lookbook.py`, `export.py`, `topdf.js` — схемы, этикетки, тех-пак, лукбук, экспорт, PDF.

Шрифты не включены в репозиторий: Petrov Sans — с сайта bluuu.tours (woff2 → ttf через fontTools), остальные — пакеты `@fontsource/*` (OFL), сконвертированные в TTF в `fonts/ttf/`. Для китайских подписей используется системный WenQuanYi Zen Hei.
