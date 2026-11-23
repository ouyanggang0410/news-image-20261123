# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ouyanggang0410/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ouyanggang0410/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

**THE HORIZON** — one image that sums up the world's news on Monday 23 November 2026: COP31 ends with no deal, a deadly drone strike near Kyiv, a factory fire in Indonesia, a minister's resignation in Seoul, a cartel boss captured in Mexico, and more, laid out as a one-page newspaper front page.

## Run it

```sh
python3 render.py
```

Writes `news-image.png` (1024x1024). Pure Python standard library: the PNG is written by hand (zlib + struct) and every letter is drawn from a stroke font defined in `render.py`, so it runs anywhere python3 runs, with no network and no third-party packages.

## The image

- `news-image.png` — the finished front page (1024x1024)
- `render.py` — PNG writer, canvas, stroke font, layout
- `news.py` — the day's stories, checked against live reporting dated 23 November 2026

## Sources

BBC World, Reuters wires, Indian morning papers, 23 November 2026.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qhmde06g&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
