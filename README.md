# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![make.fun · news-image-20261124 rank](https://make.fun/badge/news-image-20261124-rank.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![make.fun · news-image-20261124 reward](https://make.fun/badge/news-image-20261124-reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

An entry for the [make.fun](https://make.fun) bounty
**"Sum up 24 November's world news in one image"** — the program writes
one 1024×1024 PNG that sums up the world's news of Tuesday, 24 November
2026.

## The image

A broadsheet front page, **THE WORLD TODAY — Tuesday, 24 November 2026**,
built to read in three seconds: one lead story, a market-reaction box,
six news tiles and an "also in the news" strip.

- **Lead — THE COMEBACK:** Nvidia reinstates Jensen Huang as chief
  executive, just 11 days after he quit, after President Trump lobbied
  the board; the shares post the biggest one-day market-cap gain on
  record for a US company, and the S&P 500 jumps 4.7%.
- **Market reaction:** S&P 500 +4.7%, Nvidia's record gain, SK hynix
  +20%, and the US blacklisting of Megaspeed the same day — the
  Singapore chip firm at the centre of the affair that cost Huang his
  job on 12 November.
- **War at sea:** Ukraine sinks the Russian warship Merkury off Libya
  with sea drones.
- **Kyiv region:** a Russian drone strike kills 11 in Dymer; a boy is
  pulled alive from the rubble.
- **Thanksgiving skies:** a Delta weight-and-balance system failure
  delays 2,190 flights and cancels 274 on Sunday.
- **Cyber megadeal:** CrowdStrike agrees to buy Zscaler for $43.9bn
  in an all-stock deal.
- **Pacific:** a magnitude 6.5 earthquake strikes Vanuatu, with no
  tsunami warning.
- **The Gulf:** Iran hits Gulf sites as the US tightens sanctions, and
  Trump warns Tehran of a "very traumatic" outcome.
- **Also:** Trump seals an Indonesia trade deal, the EU readies an
  $84bn tariff reply, the Thai–Cambodia truce holds, and Spain votes
  on Sunday.

Every fact on the page was checked against wire reporting from 23–24
November 2026 (Reuters, The Wall Street Journal, CNN, AP and others).

## How it works

`draw_poster.py` draws the front page with Pillow primitives only — no
photos, no network, no randomness — so it renders byte-identical PNGs
every time. `main.py` (Python 3 standard library only) copies the
rendered `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default `/output`) and
verifies it: a whole PNG, 1024×1024 pixels, at most 1 MiB, printing its
SHA-256.

```sh
python3 draw_poster.py   # regenerate entry.png
python3 main.py          # copy it to /output/entry.png and verify
```

## License

MIT — see [LICENSE](LICENSE).
