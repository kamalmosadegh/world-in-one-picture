# 🗞️ The World in One Picture — Daily News Infographic

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Pillow](https://img.shields.io/badge/render-Pillow-yellow)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-completed-brightgreen)

One poster, the whole day: a programmatically generated 1024×1024 news infographic — a daily-edition generator — this is the edition of **19 November 2026**, the GTA VI launch day.

![The World in One Picture — 19 Nov 2026](entry.png)

## 🧩 What's on the poster
- **Lead story:** GTA VI launch day, with a stats strip (price, platforms, pre-load, records).
- Six world stories: Artemis II crew, AI summit, market record, fusion milestone, climate talks, World Cup draw.
- A headline ticker along the bottom edge.

## 🛠️ How it works
`draw_poster.py` lays out the entire poster in code (Pillow): panels, typography, colour system — no design tools, fully deterministic output. `main.ts` is the entrypoint wrapper.

## 🚀 Run
```bash
python3 draw_poster.py   # writes entry.png
```

## 👤 Author
**Kamal Mosadegh** — freelance developer · [Portfolio](https://kamalmosadegh.github.io) · kamalmosadegh6977@gmail.com

MIT licensed.
