#!/usr/bin/env python3
"""Regenerate the PNG icons and the Open Graph share image for qibcode.

    pip install pillow
    python3 tools/make-images.py                      # DejaVu / default font
    python3 tools/make-images.py --font Bricolage.ttf # use the brand typeface

Outputs (into assets/img/):
    apple-touch-icon.png  180 x 180
    icon-192.png          192 x 192
    icon-512.png          512 x 512
    og-image.png          1200 x 630
The geometry mirrors assets/img/favicon.svg, so the PNGs and the SVG match.
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")

NAVY = "#10204A"
BLUE = "#0047A0"
RED = "#CD2E3A"
RED_ON_NAVY = "#F26B74"
WHITE = "#FFFFFF"
MIST = "#EEF2F8"
MUTED = "#5A6478"
LINE = "#D9DFEA"


def mark(size, tile=NAVY, ring=WHITE, tail=RED_ON_NAVY, radius=0.22, scale=4):
    """The Q mark on a rounded tile, drawn oversized and downsampled for smooth edges."""
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if tile:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=s * radius, fill=tile)
    cx = cy = s * 29 / 64
    r = s * 14 / 64
    w = s * 7 / 64
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ring, width=int(round(w)))
    x1 = y1 = s * 37 / 64
    x2 = y2 = s * 45 / 64
    d.line([x1, y1, x2, y2], fill=tail, width=int(round(w)))
    for x, y in ((x1, y1), (x2, y2)):
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=tail)
    return img.resize((size, size), Image.LANCZOS)


def load_font(path, size, weight=700):
    """Load a TTF; supports the variable Bricolage Grotesque if a path is given."""
    candidates = [path, "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    for p in candidates:
        if p and os.path.exists(p):
            font = ImageFont.truetype(p, size)
            try:
                axes = font.get_variation_axes()
                values = []
                for axis in axes:
                    name = axis.get("name", b"")
                    name = name.decode() if isinstance(name, bytes) else str(name)
                    if "Weight" in name or name == "wght":
                        values.append(weight)
                    elif "Optical" in name or name == "opsz":
                        values.append(axis["maximum"])
                    else:
                        values.append(axis["default"])
                font.set_variation_by_axes(values)
            except Exception:
                pass
            return font
    return ImageFont.load_default()


def og_image(font_path):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # Right-hand mist block, like the hero.
    d.rectangle([760, 0, W, H], fill=MIST)

    # A simple phone silhouette with a question card, echoing the live sample on the site.
    px, py, pw, ph = 860, 95, 220, 470
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=34, fill=NAVY)
    d.rounded_rectangle([px + 8, py + 8, px + pw - 8, py + ph - 8], radius=27, fill=WHITE)
    d.rounded_rectangle([px + 70, py + 18, px + pw - 70, py + 34], radius=8, fill=NAVY)
    d.rounded_rectangle([px + 26, py + 60, px + pw - 26, py + 66], radius=3, fill=LINE)
    d.rounded_rectangle([px + 26, py + 60, px + 100, py + 66], radius=3, fill=BLUE)
    small = load_font(font_path, 17, 600)
    tiny = load_font(font_path, 13, 500)
    d.text((px + 26, py + 86), "What is the national", font=small, fill=NAVY)
    d.text((px + 26, py + 108), "flower of Korea?", font=small, fill=NAVY)
    opts = ["Cherry blossom", "Mugunghwa", "Lotus", "Rose"]
    oy = py + 150
    for i, o in enumerate(opts):
        fill = "#E2F3EA" if i == 1 else "#F6F8FB"
        outline = "#1E8E5A" if i == 1 else LINE
        d.rounded_rectangle([px + 26, oy, px + pw - 26, oy + 44], radius=10, fill=fill, outline=outline, width=2)
        d.text((px + 40, oy + 13), o, font=tiny, fill=NAVY)
        oy += 54

    # Mark and wordmark.
    m = mark(104, tile=None, ring=BLUE, tail=RED)
    img.paste(m, (96, 92), m)
    big = load_font(font_path, 118, 700)
    d.text((88, 196), "QibCode", font=big, fill=NAVY)
    lead = load_font(font_path, 40, 500)
    d.text((96, 350), "Apps for life's big steps.", font=lead, fill=NAVY)
    sub = load_font(font_path, 26, 500)
    d.text((96, 420), "An independent app studio in Seoul.", font=sub, fill=MUTED)
    d.text((96, 456), "First app: Korea Naturalization Practice.", font=sub, fill=MUTED)
    foot = load_font(font_path, 22, 500)
    d.text((96, 560), "qibcode.com", font=foot, fill=BLUE)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", default=None, help="path to a TTF/OTF to use for text (e.g. Bricolage Grotesque)")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    mark(180).save(os.path.join(OUT, "apple-touch-icon.png"))
    mark(192).save(os.path.join(OUT, "icon-192.png"))
    mark(512).save(os.path.join(OUT, "icon-512.png"))
    og_image(args.font).save(os.path.join(OUT, "og-image.png"), optimize=True)
    print("wrote icons and og-image.png to", OUT)


if __name__ == "__main__":
    main()
