#!/usr/bin/env python3
"""Draw the news-image entry for 19 November 2026.

One 1024x1024 poster: a masthead naming the day, a lead panel on the
day's biggest story (GTA VI launches), six story panels across regions
and fields, and a footer ticker with three more stories. All shapes and
text are drawn with Pillow; the output is deterministic (fixed seed,
no timestamps, no network), so running it twice writes identical bytes.

Run:  python3 draw_poster.py        # writes entry.png next to this file
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

NAVY = (11, 31, 58)
NAVY_LIGHT = (18, 48, 86)
CREAM = (247, 243, 234)
CARD = (255, 255, 255)
INK = (20, 24, 34)
MUTED = (90, 96, 110)
RED = (192, 57, 43)
TEAL = (14, 124, 123)
GOLD = (212, 160, 23)
PINK = (231, 84, 128)
PURPLE = (123, 47, 190)
ORANGE = (255, 158, 87)
SKY_DUSK = (64, 32, 96)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
REG = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731


def vgrad(draw, box, stops):
    """Vertical gradient across box; stops = [(pos0-1, (r,g,b)), ...]."""
    x0, y0, x1, y1 = box
    n = y1 - y0
    for i in range(n):
        t = i / max(n - 1, 1)
        for j in range(len(stops) - 1):
            p0, c0 = stops[j]
            p1, c1 = stops[j + 1]
            if p0 <= t <= p1:
                f = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                col = tuple(round(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))
                break
        else:
            col = stops[-1][1]
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, fnt, fill, spacing=2):
    """Draw text with manual letter spacing."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x


def panel(draw, x, y, w, h, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD,
                           outline=(210, 208, 198), width=2)
    draw.rounded_rectangle([x, y, x + w, y + 8], radius=4, fill=accent)
    draw.rectangle([x, y + 4, x + w, y + 8], fill=accent)


def story_card(draw, x, y, w, h, accent, kicker, title, body, icon):
    panel(draw, x, y, w, h, accent)
    icon(draw, x + 18, y + 16, w - 36, 100)
    ty = y + 128
    draw.text((x + 18, ty), kicker, font=BOLD(17), fill=accent)
    ty += 26
    for line in wrap(draw, title, BOLD(26), w - 36):
        draw.text((x + 18, ty), line, font=BOLD(26), fill=INK)
        ty += 31
    ty += 6
    for line in wrap(draw, body, REG(19), w - 36)[:2]:
        draw.text((x + 18, ty), line, font=REG(19), fill=MUTED)
        ty += 24


# ---- icons (each draws inside x, y, w, h) -------------------------------

def icon_flags(draw, x, y, w, h):
    # US, China, Russia flag chips, left to right.
    fw, fh = 84, 56
    gap = 14
    total = fw * 3 + gap * 2
    sx = x + (w - total) // 2
    sy = y + (h - fh) // 2
    # USA: stripes + canton
    for i in range(7):
        draw.rectangle([sx, sy + i * 8, sx + fw, sy + i * 8 + 8],
                       fill=RED if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([sx, sy, sx + 34, sy + 32], fill=(60, 59, 110))
    for r in range(3):
        for c in range(4):
            draw.ellipse([sx + 5 + c * 8, sy + 5 + r * 9,
                          sx + 9 + c * 8, sy + 9 + r * 9], fill=(255, 255, 255))
    # China: red + yellow stars
    cx = sx + fw + gap
    draw.rectangle([cx, sy, cx + fw, sy + fh], fill=(222, 41, 16))
    draw.regular_polygon((cx + 18, sy + 16, 10), 5, fill=(255, 222, 0))
    for px, py in [(cx + 44, sy + 10), (cx + 56, sy + 20),
                   (cx + 56, sy + 34), (cx + 44, sy + 44)]:
        draw.regular_polygon((px, py, 5), 5, fill=(255, 222, 0))
    # Russia: white / blue / red bands
    rx = cx + fw + gap
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([rx, sy + i * (fh // 3), rx + fw, sy + (i + 1) * (fh // 3)],
                       fill=col)
    for fx in (sx, cx, rx):
        draw.rounded_rectangle([fx, sy, fx + fw, sy + fh], radius=4,
                               outline=(200, 200, 200), width=2)


def icon_capitol(draw, x, y, w, h):
    cx = x + w // 2
    base = y + h - 6
    draw.rectangle([cx - 78, base - 10, cx + 78, base], fill=INK)
    draw.rectangle([cx - 68, base - 18, cx + 68, base - 10], fill=INK)
    for i in range(-3, 4):
        draw.rectangle([cx + i * 20 - 4, base - 42, cx + i * 20 + 4, base - 18],
                       fill=INK)
    draw.rectangle([cx - 70, base - 42, cx + 70, base - 37], fill=INK)
    draw.pieslice([cx - 32, base - 78, cx + 32, base - 30], 180, 360, fill=INK)
    draw.rectangle([cx - 3, base - 86, cx + 3, base - 74], fill=INK)
    draw.ellipse([cx - 4, base - 92, cx + 4, base - 84], fill=INK)
    draw.ellipse([cx - 92, base - 8, cx - 80, base + 4], fill=GOLD)
    draw.ellipse([cx + 80, base - 8, cx + 92, base + 4], fill=GOLD)


def icon_chart(draw, x, y, w, h):
    ox, oy = x + 14, y + h - 16
    draw.line([(ox, oy - h + 24), (ox, oy), (ox + w - 28, oy)],
              fill=MUTED, width=3)
    pts = [(ox + 6, oy - 18), (ox + 52, oy - 34), (ox + 92, oy - 26),
           (ox + 138, oy - 52), (ox + 184, oy - 44), (ox + 232, oy - 84),
           (ox + 268, oy - 96)]
    draw.line(pts, fill=TEAL, width=6, joint="curve")
    hx, hy = pts[-1]
    draw.polygon([(hx, hy), (hx - 18, hy + 2), (hx - 2, hy + 16)], fill=TEAL)
    draw.ellipse([pts[3][0] - 7, pts[3][1] - 7, pts[3][0] + 7, pts[3][1] + 7],
                 fill=RED)


def icon_voyager(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(10, 16, 38))
    rng = random.Random(19)
    for _ in range(46):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, h - 4)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    cx, cy = x + w // 2 + 30, y + h // 2 + 6
    draw.polygon([(cx - 52, cy - 26), (cx - 8, cy - 6), (cx - 52, cy + 14)],
                 fill=(200, 205, 220))
    draw.line([(cx - 8, cy - 6), (cx + 34, cy - 26)], fill=(200, 205, 220), width=3)
    draw.polygon([(cx - 30, cy - 4), (cx + 40, cy - 4), (cx + 22, cy + 18),
                  (cx - 12, cy + 18)], fill=(230, 232, 240))
    draw.line([(cx + 40, cy - 4), (cx + 62, cy - 16)], fill=GOLD, width=3)
    draw.ellipse([cx + 58, cy - 20, cx + 66, cy - 12], fill=GOLD)
    draw.ellipse([cx - 120, cy - 34, cx - 112, cy - 26], fill=(255, 240, 180))
    draw.ellipse([cx - 88, cy + 26, cx - 80, cy + 34], fill=(255, 240, 180))


def icon_bridge(draw, x, y, w, h):
    base = y + h - 18
    draw.rectangle([x, base, x + w, base + 8], fill=INK)
    for tx in (x + 62, x + w - 78):
        draw.rectangle([tx, y + 34, tx + 16, base], fill=INK)
        draw.rectangle([tx - 6, y + 26, tx + 22, y + 34], fill=INK)
    for i in range(6):
        fx = x + 78 + i * 26
        draw.line([(x + 70, y + 30), (fx, base)], fill=MUTED, width=2)
        fx2 = x + w - 78 - i * 26
        draw.line([(x + w - 70, y + 30), (fx2, base)], fill=MUTED, width=2)
    for cx, cy, r in [(x + w // 2 - 40, y + 26, 12), (x + w // 2 - 14, y + 14, 16),
                      (x + w // 2 + 16, y + 28, 11)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 150))
    draw.polygon([(x + w // 2 - 8, y + 44), (x + w // 2 + 8, y + 44),
                  (x + w // 2, y + 62)], fill=RED)


def icon_cyclone(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2 + 4
    for k in range(5):
        r = 12 + k * 13
        a0 = -40 + k * 38
        draw.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 250,
                 fill=TEAL if k % 2 == 0 else NAVY_LIGHT, width=6)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
    for dx, dy in [(-86, 34), (-64, 52), (70, 40), (88, 22)]:
        draw.line([(cx + dx, cy + dy - 12), (cx + dx, cy + dy + 12)],
                  fill=(90, 140, 200), width=4)


def lead_panel(draw, x, y, w, h):
    # Vice City sunset: orange -> pink -> purple sky, sun, skyline, sea.
    vgrad(draw, (x, y, x + w, y + h),
          [(0.0, ORANGE), (0.45, PINK), (0.78, PURPLE), (1.0, (48, 20, 80))])
    sun_cx, sun_cy, sun_r = x + w - 190, y + 150, 74
    draw.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
                 fill=(255, 214, 120))
    draw.ellipse([sun_cx - sun_r - 12, sun_cy - sun_r - 12,
                  sun_cx + sun_r + 12, sun_cy + sun_r + 12],
                 outline=(255, 214, 120, 120), width=3)
    rng = random.Random(7)
    horizon = y + h - 96
    bx = x
    while bx < x + w - 30:
        bw = rng.randint(46, 96)
        bh = rng.randint(52, 118)
        draw.rectangle([bx, horizon - bh, bx + bw, horizon], fill=(38, 16, 66))
        for wy in range(horizon - bh + 10, horizon - 8, 18):
            for wx in range(bx + 8, bx + bw - 8, 16):
                if rng.random() < 0.45:
                    draw.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 214, 120))
        bx += bw + rng.randint(2, 10)
    # two small birds in the sky, right of the headline
    for bx, by, s in [(x + 560, y + 52, 12), (x + 640, y + 84, 9)]:
        draw.arc([bx - s, by - s, bx, by + s], 300, 360, fill=(40, 12, 60), width=4)
        draw.arc([bx, by - s, bx + s, by + s], 180, 240, fill=(40, 12, 60), width=4)
    # sea strip with light glints under the sun
    draw.rectangle([x, horizon, x + w, y + h], fill=(24, 10, 52))
    for i in range(4):
        sy = horizon + 16 + i * 16
        sw = 90 + i * 46
        draw.line([(sun_cx - sw // 2, sy), (sun_cx + sw // 2, sy)],
                  fill=(255, 190, 110), width=3)
    # text
    tx, ty = x + 26, y + 22
    draw.text((tx, ty), "GAMES  •  THE LAUNCH OF THE YEAR", font=BOLD(20),
              fill=(255, 230, 190))
    draw.text((tx, ty + 34), "GTA VI IS OUT", font=BOLD(72), fill=(255, 255, 255),
              stroke_width=2, stroke_fill=(40, 10, 60))
    # dark band so the sub-lines stay readable over the skyline
    draw.rounded_rectangle([tx - 8, ty + 116, x + w - 26, ty + 196], radius=10,
                           fill=(20, 8, 40, 165))
    draw.text((tx, ty + 126),
              "Grand Theft Auto VI rolls out worldwide —",
              font=BOLD(26), fill=(255, 255, 255))
    draw.text((tx, ty + 158),
              "Vice City returns after a 13-year wait.",
              font=BOLD(26), fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img, "RGBA")

    # masthead
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    draw.rectangle([0, 118, W, 124], fill=GOLD)
    gx, gy, gr = 62, 59, 34
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(255, 255, 255), width=3)
    draw.ellipse([gx - 16, gy - gr, gx + 16, gy + gr], outline=(255, 255, 255), width=2)
    draw.line([(gx - gr, gy), (gx + gr, gy)], fill=(255, 255, 255), width=2)
    draw.arc([gx - gr, gy - 12, gx + gr, gy + 12], 200, 340, fill=(255, 255, 255), width=2)
    tracked(draw, (116, 18), "THE WORLD IN ONE PICTURE", BOLD(24),
            (180, 200, 225), spacing=4)
    draw.text((116, 50), "THURSDAY 19 NOVEMBER 2026", font=BOLD(44),
              fill=(255, 255, 255))

    # lead story
    lead_panel(draw, 24, 138, 976, 272)

    # story rows
    row_y = [422, 706]
    row_h = 272
    cards = [
        (icon_flags, RED, "SUMMIT IN SHENZHEN",
         "TRUMP, XI & PUTIN MEET",
         "Three leaders open trilateral talks in Shenzhen."),
        (icon_capitol, NAVY_LIGHT, "UNITED STATES",
         "FIRST BLACK SPEAKER",
         "Democrats pick Jeffries to lead the House."),
        (icon_chart, TEAL, "MARKETS",
         "$81.3BN IPO",
         "Biggest listing ever; valued up to $1.5tn."),
        (icon_voyager, (10, 16, 38), "SPACE",
         "VOYAGER 1: ONE LIGHT-DAY",
         "Record distance for NASA's probe, 50 years on."),
        (icon_bridge, RED, "UKRAINE WAR",
         "CRIMEA BRIDGE HIT AGAIN",
         "Another attack reported; traffic halted."),
        (icon_cyclone, TEAL, "WEATHER",
         "CYCLONE AKVAN NEARS INDIA",
         "Landfall expected on India's east coast."),
    ]
    for i, (icon, accent, kicker, title, body) in enumerate(cards):
        r, c = divmod(i, 3)
        x = 24 + c * (312 + 20)
        story_card(draw, x, row_y[r], 312, row_h, accent, kicker, title, body, icon)

    # footer ticker (shrink the font until the line fits the width)
    draw.rectangle([0, 984, W, H], fill=NAVY)
    ticker = ("ALSO TODAY:  EU proposes €45bn Ukraine loan  •  Eisenkot tapped to form "
              "Israel's government  •  Four nations urge Gaza aid access as floods hit")
    size = 19
    while size > 12 and draw.textlength(ticker, font=REG(size)) > W - 48:
        size -= 1
    draw.text((24, 984 + (40 - size) // 2 - 2), ticker, font=REG(size),
              fill=(220, 228, 240))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
