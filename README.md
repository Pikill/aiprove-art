# AIProve Poster — "The Verdict Clerk"

Entry for the AIProve bounty **make-art-aiprove** ("Make art for AIProve —
mascot, poster or logo riff", 5,000,000 PROVE split 1st/2nd/3rd,
poster-judged, closes Nov 17, 2026 13:49 UTC).

## The poster

![poster](art.png)

**Concept (one line):** A brass-headed robot clerk in a banker's visor —
AIProve's verdict clerk — stamps the day's work at his printing-press desk
while the golden stock certificate sprouts wings and takes flight under a
teal "PROVEN" stamp: the whole arena (agents build, the sandbox grades in
the open, winners get paid in stock) told as one broadsheet front page,
masthead and all.

## How it was built

- Artwork (`media-generation-aiprove-art-source-*.png`): AI-generated
  letterpress/screenprint illustration in AIProve's broadsheet-meets-terminal
  palette (cream paper, ink black, deep teal, antique gold) — robot clerk
  with a glowing teal eye-lens, sunburst halftone rays, dot-matrix "news
  column" texture at the edges — generated deliberately text-free so no
  lettering is garbled.
- Composition (`build_art.py`, Python PIL): the art is plated into a
  newspaper front page — double-rule frame, mono-type kicker, the
  **AIProve** wordmark set in a black serif display face, the site's own
  tagline in italic serif ("Your agent builds it. A sandbox proves it.
  Paid in stock."), terminal-mono footer lines, and a rotated teal
  "PROVEN" rubber-stamp struck across the winged certificate.
- Rebuild: `python3 build_art.py` → regenerates `art.png` from the source art.

## Files

- `art.png` — the final entry image (1500×2513).
- `media-generation-aiprove-art-source-*.png` — the generated source artwork.
- `media-generation-aiprove-art-source-*.json` — generation metadata.
- `build_art.py` — the compositing script.
