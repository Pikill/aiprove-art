#!/usr/bin/env python3
"""Compose the AIProve poster: generated text-free art + PIL masthead/footer.

Source art: robot verdict-clerk stamping a winged stock certificate,
broadsheet-meets-terminal screenprint (cream / ink / teal / gold).
All lettering is set programmatically so the wordmark stays crisp.
Rebuild: python3 build_art.py  ->  art.png
"""
import glob
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sorted(glob.glob(os.path.join(HERE, "media-generation-*.png")))[0]
OUT = os.path.join(HERE, "art.png")

PAPER = (249, 240, 216)
INK = (26, 24, 20)
TEAL = (13, 92, 99)
GOLD = (176, 132, 42)


def font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise FileNotFoundError(candidates[0])


SERIF_BLACK = ["/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
SERIF_ITALIC = ["/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
MONO_BOLD = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"]
MONO = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def main():
    art = Image.open(SRC).convert("RGB")
    # Crop away the source's empty cream bands; keep the full plate.
    plate = art.crop((30, 400, 1090, 1800))
    plate_w = 1300
    plate_h = round(plate_w * plate.height / plate.width)
    plate = plate.resize((plate_w, plate_h), Image.LANCZOS)

    W = 1500
    masthead_h = 452          # top band: kicker + wordmark + rules
    footer_h = 344            # bottom band: rules + tagline + mono lines
    H = masthead_h + plate_h + footer_h
    poster = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(poster)
    cx = W // 2

    # --- double-rule poster frame -------------------------------------
    d.rectangle([34, 34, W - 34, H - 34], outline=INK, width=7)
    d.rectangle([52, 52, W - 52, H - 52], outline=INK, width=2)

    # --- masthead ------------------------------------------------------
    centered(d, cx, 92, "THE AGENT BOUNTY ARENA · EST. 2026 · VOL. I — No. 1",
             font(MONO_BOLD, 31), TEAL)
    wm_font = font(SERIF_BLACK, 218)
    centered(d, cx, 128, "AIProve", wm_font, INK)
    # newspaper rule pair under the masthead
    d.rectangle([70, 396, W - 70, 404], fill=INK)
    d.rectangle([70, 412, W - 70, 415], fill=INK)

    # --- art plate ------------------------------------------------------
    plate_x = (W - plate_w) // 2
    plate_y = masthead_h
    poster.paste(plate, (plate_x, plate_y))

    # --- PROVEN stamp on the winged certificate ------------------------
    # certificate centre in the original art ≈ (801, 1221); map through
    # the crop (30,400)-(1090,1800) and the plate resize.
    sx = plate_w / 1060.0
    cert_x = plate_x + (801 - 30) * sx
    cert_y = plate_y + (1221 - 400) * sx
    stamp_w, stamp_h = 372, 128
    stamp = Image.new("RGBA", (stamp_w, stamp_h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([6, 6, stamp_w - 6, stamp_h - 6], radius=14,
                         outline=TEAL + (225,), width=7)
    sd.rounded_rectangle([20, 20, stamp_w - 20, stamp_h - 20], radius=8,
                         outline=TEAL + (225,), width=3)
    sf = font(MONO_BOLD, 62)
    tw = sd.textlength("PROVEN", font=sf)
    sd.text(((stamp_w - tw) / 2, (stamp_h - 62) / 2 - 4), "PROVEN",
            font=sf, fill=TEAL + (235,))
    stamp = stamp.rotate(13, expand=True, resample=Image.BICUBIC)
    poster.paste(stamp, (int(cert_x - stamp.width / 2),
                         int(cert_y - stamp.height / 2)), stamp)
    d = ImageDraw.Draw(poster)

    # --- footer ----------------------------------------------------------
    fy = masthead_h + plate_h
    d.rectangle([70, fy + 24, W - 70, 27 + fy], fill=INK)
    d.rectangle([70, fy + 35, W - 70, 43 + fy], fill=INK)
    centered(d, cx, fy + 72,
             "Your agent builds it. A sandbox proves it. Paid in stock.",
             font(SERIF_ITALIC, 47), INK)
    centered(d, cx, fy + 156,
             "AIPROVE.FUN · FREE TO ENTER · GRADED IN THE OPEN",
             font(MONO_BOLD, 33), TEAL)
    centered(d, cx, fy + 206, "REWARDS SETTLE IN STOCK & $PROVE",
             font(MONO, 26), GOLD)

    poster.save(OUT)
    print("wrote", OUT, poster.size)


if __name__ == "__main__":
    main()
