"""Generate the Open Graph social card for the documentation.

Social platforms do not render SVG previews, so the card shipped as
``ogp_image`` has to be a raster image. This script regenerates it from the
brand colours used by the sidebar wordmark.

Run from the repository root::

    python scripts/make_social_card.py

The result is written to ``docs/_static/social-card.png`` and committed.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630

TEAL = "#0F766E"
INK = "#1F2937"
MUTED = "#4B5563"
BACKGROUND = "#FFFFFF"

OUTPUT = os.path.join("docs", "_static", "social-card.png")

# Segoe UI matches the sidebar wordmark's font stack closely enough that the
# card and the site read as the same brand.
FONT_CANDIDATES = {
    "bold": [
        r"C:\Windows\Fonts\segoeuib.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "regular": [
        r"C:\Windows\Fonts\segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
}


def load_font(weight, size):
    for path in FONT_CANDIDATES[weight]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise SystemExit("No {} font found; edit FONT_CANDIDATES".format(weight))


def main():
    card = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(card)

    # Teal spine on the left, echoing the favicon's solid block.
    draw.rectangle([0, 0, 16, HEIGHT], fill=TEAL)

    title_font = load_font("bold", 96)
    tagline_font = load_font("regular", 40)
    footer_font = load_font("regular", 30)

    left = 96
    baseline = 196

    # "Py" teal, "QuantLib" ink, drawn as two runs so the split matches the
    # wordmark exactly.
    draw.text((left, baseline), "Py", font=title_font, fill=TEAL)
    py_width = draw.textlength("Py", font=title_font)
    draw.text((left + py_width, baseline), "QuantLib", font=title_font, fill=INK)

    # Same two-part tagline as the landing page.
    draw.text(
        (left, baseline + 148),
        "Python bindings for QuantLib,",
        font=tagline_font,
        fill=INK,
    )
    draw.text(
        (left, baseline + 202),
        "the open-source library for quantitative finance.",
        font=tagline_font,
        fill=MUTED,
    )

    draw.text(
        (left, HEIGHT - 96),
        "pyquantlib.readthedocs.io",
        font=footer_font,
        fill=TEAL,
    )

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    card.save(OUTPUT, "PNG", optimize=True)
    print("wrote {} ({}x{})".format(OUTPUT, WIDTH, HEIGHT))


if __name__ == "__main__":
    sys.exit(main())
