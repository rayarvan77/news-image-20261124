#!/usr/bin/env python3
"""Draw entry.png: a broadsheet front page summing up the world news of
Tuesday 24 November 2026. Deterministic Pillow primitives only: no photos,
no network, no randomness, no timestamps. Running this script twice writes
byte-identical PNGs."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREEN = (27, 94, 32)
GREEN_LIGHT = (46, 125, 50)
GREY = (90, 86, 78)
RULE = (18, 18, 18)
TILE_BG = (255, 255, 255)
BLUE = (21, 58, 110)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    """Draw wrapped paragraph; return y just below the last line."""
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def tile(draw, x, y, w, h, kicker, headline, body, accent=RED,
         head_size=26, body_size=17, body_lines=2):
    """One bordered news tile with kicker, headline and body text."""
    draw.rectangle([x, y, x + w, y + h], fill=TILE_BG, outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 5], fill=accent)
    kx, ky = x + 14, y + 16
    draw.text((kx, ky), kicker, font=font(SANS_B, 16), fill=accent)
    hy = ky + 26
    lines = wrap(draw, headline, font(SERIF_B, head_size), w - 28)[:2]
    for line in lines:
        draw.text((kx, hy), line, font=font(SERIF_B, head_size), fill=INK)
        hy += head_size + 6
    blines = wrap(draw, body, font(SANS, body_size),
                  w - 28)[:body_lines]
    by = hy + 6
    for line in blines:
        draw.text((kx, by), line, font=font(SANS, body_size),
                  fill=(52, 52, 52))
        by += int(body_size * 1.28)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    R = W - M

    # ---- Masthead ----
    rule(d, M, 26, R, width=3)
    d.text((W // 2, 36), "THE WORLD TODAY", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    d.text((W // 2, 108), "TUESDAY, 24 NOVEMBER 2026",
           font=font(SANS_B, 22), fill=RED, anchor="ma")
    rule(d, M, 140, R, width=2)
    d.text((M, 150), "ONE IMAGE  ·  THE WORLD'S NEWS",
           font=font(SANS_B, 15), fill=GREY)
    d.text((R, 150), "TUESDAY EDITION", font=font(SANS_B, 15),
           fill=GREY, anchor="ra")
    rule(d, M, 172, R, width=1, fill=GREY)

    # ---- Lead story (left) ----
    lx, lw = M, 620
    d.text((lx, 190), "WASHINGTON  ·  TECHNOLOGY", font=font(SANS_B, 19),
           fill=RED)
    d.text((lx, 214), "THE COMEBACK", font=font(SERIF_B, 62), fill=INK)
    y = para(d, lx, 292,
             "Nvidia reinstates Jensen Huang as chief executive \u2014 "
             "just 11 days after he quit \u2014 after President Trump "
             "lobbied the board. Shares post the biggest one-day "
             "market-cap gain on record for a US company.",
             font(SANS, 21), lw, leading=28)

    # Chip + rising market graphic under the lead text
    gx, gy, gw, gh = lx, 420, 300, 96
    d.rectangle([gx + 34, gy + 22, gx + 130, gy + 74], fill=GREEN,
                outline=INK, width=2)
    d.rectangle([gx + 52, gy + 38, gx + 112, gy + 58], fill=(255, 255, 255),
                outline=INK, width=1)
    d.text((gx + 82, gy + 40), "AI", font=font(SANS_B, 15), fill=GREEN,
           anchor="ma")
    for i in range(5):  # chip pins, top and bottom
        px = gx + 44 + i * 18
        d.line([(px, gy + 14), (px, gy + 22)], fill=INK, width=3)
        d.line([(px, gy + 74), (px, gy + 82)], fill=INK, width=3)
    for i in range(3):
        py = gy + 32 + i * 18
        d.line([(gx + 26, py), (gx + 34, py)], fill=INK, width=3)
        d.line([(gx + 130, py), (gx + 138, py)], fill=INK, width=3)
    # rising arrow chart
    ax0, ay0 = gx + 190, gy + 84
    d.line([(ax0, ay0), (ax0 + 100, ay0 - 58)], fill=RED, width=5)
    d.line([(ax0 + 100, ay0 - 58), (ax0 + 78, ay0 - 58)], fill=RED, width=5)
    d.line([(ax0 + 100, ay0 - 58), (ax0 + 100, ay0 - 36)], fill=RED, width=5)
    d.text((ax0 + 8, ay0 - 96), "S&P 500  +4.7%",
           font=font(SANS_B, 19), fill=RED)
    d.text((lx, gy + 104), "The board had said he would not return.",
           font=font(SANS, 17), fill=GREY)
    d.text((lx, gy + 126), "Trump: \u201cWe have one of our great stars "
           "back in play.\u201d",
           font=font(SANS, 17), fill=GREY)

    # ---- Market reaction box (right of lead) ----
    bx, bw = 668, R - 668
    by, bh = 190, 372
    d.rectangle([bx, by, bx + bw, by + bh], fill=TILE_BG, outline=INK,
                width=2)
    d.rectangle([bx, by, bx + bw, by + 5], fill=GREEN)
    d.text((bx + 16, by + 18), "MARKET REACTION", font=font(SANS_B, 17),
           fill=GREEN)
    d.text((bx + 16, by + 48), "Wall Street roars", font=font(SERIF_B, 27),
           fill=INK)
    rows = [
        ("S&P 500", "+4.7%", "in a single session"),
        ("Nvidia", "record gain", "largest one-day rise in"),
        ("", "", "US market-cap history"),
        ("Nasdaq", "+6.5%", "in a single session"),
        ("Dow", "+1,450 pts", "points gained Monday"),
        ("", "", "both surge on Huang's return"),
    ]
    ry = by + 92
    for name, val, note in rows:
        if name:
            d.text((bx + 16, ry), name, font=font(SANS_B, 19), fill=INK)
            d.text((bx + bw - 16, ry), val, font=font(SANS_B, 19),
                   fill=GREEN, anchor="ra")
            ry += 27
        else:
            d.text((bx + 16, ry), note, font=font(SANS, 16), fill=GREY)
            ry += 23
    rule(d, bx + 16, ry + 4, bx + bw - 16, width=1, fill=GREY)
    para(d, bx + 16, ry + 14,
         "Huang quit on 12 November after reports of affairs, one "
         "with a suspected Chinese spy.", font(SANS, 16), bw - 32,
         fill=(52, 52, 52), leading=21)

    # ---- Row 2: three tiles ----
    ty, th, tw, gap = 586, 176, 304, 16
    tile(d, M, ty, tw, th, "WAR AT SEA",
         "Ukraine sinks Russian warship",
         "Sea drones sank the corvette Merkury off Libya, Kyiv says.",
         accent=BLUE)
    tile(d, M + tw + gap, ty, tw, th, "KYIV REGION",
         "Drone strike kills 11 in Dymer",
         "A boy is pulled alive from the rubble of a block of flats.",
         accent=RED)
    tile(d, M + 2 * (tw + gap), ty, tw, th, "THANKSGIVING SKIES",
         "Delta glitch strands flyers",
         "2,190 flights delayed, 274 cancelled on Sunday.",
         accent=GREEN)

    # ---- Row 3: three tiles ----
    ty2 = 778
    tile(d, M, ty2, tw, th, "CYBER MEGADEAL",
         "CrowdStrike to buy Zscaler for $43.9bn",
         "All-stock deal unites two security giants.",
         accent=BLUE)
    tile(d, M + tw + gap, ty2, tw, th, "PACIFIC",
         "Magnitude 6.5 quake strikes Vanuatu",
         "Tremor shakes the island nation; no tsunami warning.",
         accent=GREEN)
    tile(d, M + 2 * (tw + gap), ty2, tw, th, "THAI\u2013CAMBODIA",
         "Truce holds after border war",
         "Ceasefire ends weeks of clashes that killed 100+ and "
         "displaced hundreds of thousands.",
         accent=RED, body_size=16, body_lines=3)

    # ---- Also strip + footer ----
    rule(d, M, 966, R, width=2)
    d.text((M, 976),
           "ALSO:  EU seals Indonesia trade deal  \u00b7  Bitcoin and "
           "gold surge on Huang return  \u00b7  Spain votes Sunday",
           font=font(SANS_B, 14), fill=INK)
    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
