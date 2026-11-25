#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page (1024x1024 PNG).

Everything is drawn from code with PIL: no photos, no downloads, no network.
Deterministic: same input, same bytes every run.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJAVU_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
NAVY2 = (31, 58, 77)
INK = (26, 26, 26)
GREY = (90, 86, 76)
RED = (180, 35, 24)
GOLD = (201, 162, 39)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)
TEAL = (18, 74, 78)

def font(path, size):
    return ImageFont.truetype(path, size)

F_MAST = font(DEJAVU_B, 30)
F_DATE = font(DEJAVU_B, 78)
F_DATESUB = font(DEJAVU, 23)
F_TAG = font(DEJAVU_B, 18)
F_LEAD = font(DEJAVU_B, 41)
F_LEAD_SUB = font(DEJAVU, 22)
F_CARD_H = font(DEJAVU_B, 28)
F_CARD_B = font(DEJAVU, 21)
F_TICK_H = font(DEJAVU_B, 20)
F_TICK = font(DEJAVU, 20)
F_FOOT = font(DEJAVU, 17)

def wrap(d, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def center(d, y, text, fnt, fill, x0=0, x1=W):
    tw = d.textlength(text, font=fnt)
    d.text(((x0 + x1 - tw) / 2, y), text, font=fnt, fill=fill)

def tag_chip(d, x, y, text, color):
    tw = d.textlength(text, font=F_TAG)
    pad = 12
    d.rounded_rectangle([x, y, x + tw + 2 * pad, y + 30], radius=4, fill=color)
    d.text((x + pad, y + 4), text, font=F_TAG, fill=(255, 255, 255))

def draw_ship(d, x, y, s, hull=(70, 90, 120), deck=(180, 35, 24)):
    """Small cargo ship with smoke, scaled by s (width ~ 3.2*s)."""
    d.polygon([(x, y + 1.6 * s), (x + 3.2 * s, y + 1.6 * s),
               (x + 2.8 * s, y + 2.4 * s), (x + 0.4 * s, y + 2.4 * s)],
              fill=hull)
    d.rectangle([x + 1.1 * s, y + 0.7 * s, x + 1.9 * s, y + 1.6 * s], fill=deck)
    d.rectangle([x + 1.45 * s, y + 0.1 * s, x + 1.55 * s, y + 0.7 * s], fill=INK)
    d.ellipse([x + 1.35 * s, y - 0.3 * s, x + 1.7 * s, y + 0.05 * s], fill=(150, 150, 150))
    d.ellipse([x + 1.5 * s, y - 0.55 * s, x + 1.9 * s, y - 0.15 * s], fill=(170, 170, 170))
    for i, wx in enumerate([0.0, 1.1, 2.2]):
        d.arc([x + wx * s, y + 2.6 * s, x + (wx + 1.0) * s, y + 3.1 * s],
              180, 360, fill=(120, 140, 160), width=3)

def draw_globe(d, cx, cy, r, line=(31, 58, 77)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=line, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=line, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=line, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=line, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 180, 360, fill=line, width=3)

def draw_tower(d, x, y, s):
    """Tall tower with a drone and burst above it."""
    d.polygon([(x + 0.4 * s, y + 3.0 * s), (x + 0.7 * s, y), (x + 1.3 * s, y),
               (x + 1.6 * s, y + 3.0 * s)], fill=(70, 90, 120))
    d.polygon([(x + 0.85 * s, y - 0.7 * s), (x + 1.0 * s, y), (x + 1.15 * s, y)],
              fill=(180, 35, 24))
    for row in range(5):
        for col in range(2):
            d.rectangle([x + (0.75 + col * 0.35) * s, y + (0.6 + row * 0.45) * s,
                         x + (0.95 + col * 0.35) * s, y + (0.85 + row * 0.45) * s],
                        fill=(240, 220, 130))
    # drone
    dx, dy = x + 2.3 * s, y + 0.3 * s
    d.ellipse([dx, dy, dx + 0.5 * s, dy + 0.3 * s], fill=INK)
    d.line([dx - 0.25 * s, dy - 0.1 * s, dx + 0.75 * s, dy - 0.1 * s], fill=INK, width=3)
    d.ellipse([dx - 0.35 * s, dy - 0.25 * s, dx - 0.05 * s, dy + 0.05 * s], fill=(180, 35, 24))
    d.ellipse([dx + 0.55 * s, dy - 0.25 * s, dx + 0.85 * s, dy + 0.05 * s], fill=(180, 35, 24))
    # burst
    bx, by = x + 2.3 * s, y + 1.4 * s
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 0.15 * s, 0.5 * s
        a = math.radians(ang)
        d.line([bx + r1 * math.cos(a), by + r1 * math.sin(a),
                bx + r2 * math.cos(a), by + r2 * math.sin(a)],
               fill=(230, 120, 20), width=4)
    d.ellipse([bx - 0.18 * s, by - 0.18 * s, bx + 0.18 * s, by + 0.18 * s],
              fill=(230, 120, 20))

def draw_medal(d, cx, cy, r):
    d.polygon([(cx - r * 0.55, cy - r * 1.7), (cx - r * 0.1, cy - r * 0.6),
               (cx - r * 0.75, cy - r * 0.6)], fill=(180, 35, 24))
    d.polygon([(cx + r * 0.55, cy - r * 1.7), (cx + r * 0.1, cy - r * 0.6),
               (cx + r * 0.75, cy - r * 0.6)], fill=(31, 58, 77))
    d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 1.3], fill=GOLD,
              outline=(150, 115, 20), width=3)
    d.ellipse([cx - r * 0.62, cy - r * 0.32, cx + r * 0.62, cy + r * 0.92],
              outline=(150, 115, 20), width=2)
    d.text((cx - r * 0.28, cy + r * 0.02), "★", font=font(DEJAVU_B, int(r * 0.85)),
           fill=(150, 115, 20))

def draw_shield(d, cx, cy, r):
    pts = [(cx, cy - r), (cx + r * 0.85, cy - r * 0.55), (cx + r * 0.85, cy + r * 0.1),
           (cx, cy + r), (cx - r * 0.85, cy + r * 0.1), (cx - r * 0.85, cy - r * 0.55)]
    d.polygon(pts, outline=(31, 58, 77), width=4)
    d.ellipse([cx - r * 0.22, cy - r * 0.35, cx + r * 0.22, cy + r * 0.09],
              fill=(180, 35, 24))
    d.polygon([(cx - r * 0.12, cy + r * 0.05), (cx + r * 0.12, cy + r * 0.05),
               (cx + r * 0.28, cy + r * 0.55), (cx - r * 0.28, cy + r * 0.55)],
              fill=(180, 35, 24))

def draw_tanker(d, x, y, s):
    d.polygon([(x, y + 1.5 * s), (x + 3.4 * s, y + 1.5 * s),
               (x + 3.0 * s, y + 2.3 * s), (x + 0.4 * s, y + 2.3 * s)],
              fill=(120, 60, 40))
    for i in range(3):
        d.rectangle([x + (0.5 + i * 0.7) * s, y + 0.8 * s,
                     x + (1.05 + i * 0.7) * s, y + 1.5 * s],
                    fill=(201, 162, 39) if i % 2 == 0 else (70, 90, 120))
    d.rectangle([x + 2.7 * s, y + 0.5 * s, x + 3.1 * s, y + 1.5 * s], fill=(240, 240, 240))
    # sea mine: spiky circle
    import math
    mx, my, mr = x + 3.7 * s, y + 0.9 * s, 0.32 * s
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([mx + mr * 0.8 * math.cos(a), my + mr * 0.8 * math.sin(a),
                mx + mr * 1.5 * math.cos(a), my + mr * 1.5 * math.sin(a)],
               fill=INK, width=3)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=INK)
    for i, wx in enumerate([0.0, 1.2, 2.4]):
        d.arc([x + wx * s, y + 2.35 * s, x + (wx + 1.0) * s, y + 2.7 * s],
              180, 360, fill=(140, 170, 190), width=3)

def card(d, x, y, w, h, tag, tag_color, headline, body, art):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD, outline=BORDER, width=2)
    tag_chip(d, x + 18, y + 16, tag, tag_color)
    art_x = x + w - 132
    art_y = y + 44
    art(d, art_x, art_y)
    maxw = w - 132 - 36
    lines = wrap(d, headline, F_CARD_H, maxw)
    ly = y + 52
    for ln in lines[:2]:
        d.text((x + 18, ly), ln, font=F_CARD_H, fill=INK)
        ly += 32
    blines = wrap(d, body, F_CARD_B, maxw)
    ly = y + 120
    for ln in blines[:2]:
        d.text((x + 18, ly), ln, font=F_CARD_B, fill=GREY)
        ly += 24

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 152], fill=NAVY)
    d.rectangle([0, 152, W, 158], fill=GOLD)
    center(d, 16, "THE WORLD IN ONE DAY", F_MAST, (240, 220, 130))
    center(d, 50, "25 NOVEMBER 2026", F_DATE, (255, 255, 255))
    center(d, 128, "WEDNESDAY  ·  THE DAY'S WORLD NEWS IN ONE IMAGE",
           F_DATESUB, (200, 205, 220))

    # ---- Lead story: Ukraine drone strikes on Russian ships ----
    lx, ly, lw, lh = 32, 174, 960, 224
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=CARD,
                        outline=BORDER, width=2)
    d.rectangle([lx, ly + 10, lx + 8, ly + lh - 10], fill=RED)
    tag_chip(d, lx + 24, ly + 16, "WAR  ·  UKRAINE", RED)
    draw_ship(d, lx + lw - 200, ly + 46, 44)
    d.text((lx + 24, ly + 52), "UKRAINE DRONES HIT", font=F_LEAD, fill=INK)
    d.text((lx + 24, ly + 98), "RUSSIAN SHIPS IN TWO SEAS", font=F_LEAD, fill=INK)
    sub = ("Zelenskyy confirms strikes on a cargo ship in the Gulf of Finland "
           "and a warship sunk off Benghazi, Libya — Russia calls it “terrorism”.")
    sublines = wrap(d, sub, F_LEAD_SUB, lw - 48 - 230)
    sy = ly + 148
    for ln in sublines[:3]:
        d.text((lx + 24, sy), ln, font=F_LEAD_SUB, fill=GREY)
        sy += 25

    # ---- Grid of four stories ----
    gy = 412
    gh = 168
    gw = 472
    card(d, 32, gy, gw, gh, "CLIMATE  ·  ANTALYA", (31, 90, 60),
         "COP31 ENDS WITH NO DEAL",
         "Oil and gas producers block a fossil-fuel phase-out.",
         lambda dd, ax, ay: draw_globe(dd, ax + 55, ay + 55, 48))
    card(d, 520, gy, gw, gh, "MIDDLE EAST  ·  RIYADH", (120, 50, 30),
         "DRONE HITS RIYADH'S TALLEST TOWER",
         "Houthi strike on the Saudi capital injures 11 people.",
         lambda dd, ax, ay: draw_tower(dd, ax + 8, ay + 18, 30))
    card(d, 32, gy + gh + 12, gw, gh, "USA  ·  WASHINGTON", (31, 58, 77),
         "TRUMP HONOURS GIULIANI",
         "Medal of Freedom for the former New York mayor.",
         lambda dd, ax, ay: draw_medal(dd, ax + 60, ay + 62, 34))
    card(d, 520, gy + gh + 12, gw, gh, "CYBER  ·  USA", (90, 40, 90),
         "CYBER BREACH HITS CIA, ODNI",
         "Intrusion into unclassified systems, agencies say.",
         lambda dd, ax, ay: draw_shield(dd, ax + 60, ay + 60, 42))

    # ---- Iran strip ----
    iy = 774
    d.rounded_rectangle([32, iy, 992, iy + 108], radius=10, fill=NAVY2)
    tag_chip(d, 56, iy + 14, "ENERGY  ·  STRAIT OF HORMUZ", (180, 35, 24))
    draw_tanker(d, 992 - 215, iy + 20, 30)
    d.text((56, iy + 48), "MINES HIT THREE OIL TANKERS", font=F_CARD_H, fill=(255, 255, 255))
    d.text((56, iy + 80), "Iran reports sea-mine strikes; power rationing begins.",
           font=F_CARD_B, fill=(210, 220, 230))

    # ---- Also today ticker ----
    ty = 896
    d.rounded_rectangle([32, ty, 992, ty + 92], radius=10, fill=CARD,
                        outline=BORDER, width=2)
    d.text((56, ty + 10), "ALSO TODAY", font=F_TICK_H, fill=RED)
    d.text((56, ty + 38), "GAZA — Death toll reported at 74,746; WFP: 266 million face acute hunger.",
           font=F_TICK, fill=INK)
    d.text((56, ty + 64), "SPORT — England beat Australia by 8 wickets in the 2nd T20I (chasing 185).",
           font=F_TICK, fill=INK)

    # ---- Footer ----
    center(d, 1000, "News first reported Wednesday 25 November 2026  ·  Drawn entirely from code",
           F_FOOT, GREY)

    img.save(OUT, "PNG", optimize=True)

if __name__ == "__main__":
    main()
