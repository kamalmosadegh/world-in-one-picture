# The World in One Picture — 19 November 2026

A make.fun news-image entry: one program that writes one image summing
up the world's news of Thursday 19 November 2026.

## The image

`entry.png` (1024×1024, PNG) is a front-page-style poster drawn by
`draw_poster.py` with Pillow:

- **Masthead** — "THURSDAY 19 NOVEMBER 2026".
- **Lead story** — Grand Theft Auto VI launches worldwide; Vice City
  returns after a 13-year wait.
- **Six more stories** — the Trump–Xi–Putin trilateral talks in
  Shenzhen; Hakeem Jeffries nominated as the first Black Speaker of
  the US House; Anthropic's $81.3bn IPO, the biggest ever; NASA's
  Voyager 1 passing one light-day from Earth, 50 years after launch;
  another attack on the Crimea Bridge; Cyclone Akvan nearing India's
  east coast.
- **Footer ticker** — the EU's proposed €45bn Ukraine loan, Eisenkot
  tapped to form Israel's next government, and four nations urging
  Gaza aid access as floods hit.

Every story was reported on 19 November 2026 (BBC, The New York
Times, Al Jazeera, NDTV, The Hindu and wire reports carried that
morning). The drawing is original work: flat vector-style shapes and
DejaVu text, no photographs, no copied artwork.

## The program

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. The output is byte-identical on every run: no
network, no clock, no randomness at run time.

Regenerate the poster (development only, needs Pillow + DejaVu fonts):

```sh
python3 draw_poster.py
```

Check the entry locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
