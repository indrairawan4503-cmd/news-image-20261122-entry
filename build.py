#!/usr/bin/env python3
"""Build the news-image-20261122 variant A front page (photo-montage newspaper).

All text is drawn in code with PIL; all photos were generated for this entry.
Output: entry.png, 1024x1024, deterministic (no timestamps, fixed inputs).
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1024, 1024
PAPER = (245, 241, 230)
INK = (20, 20, 20)
RED = (178, 34, 34)
GREY = (90, 86, 78)
RULE = (60, 58, 52)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PHOTOS = "photos"
LEAD = f"{PHOTOS}/media-generation-gulf-tanker-0-3984b888-4265-491f-b53e-a54b0e4d64b6.webp"
PERU = f"{PHOTOS}/media-generation-peru-quake-0-05d4b196-af79-43c5-84fd-fe7f3640bc61.webp"
COP = f"{PHOTOS}/media-generation-cop31-0-4084e19d-11c3-4a06-9093-4fee3a32a3ad.webp"
EST = f"{PHOTOS}/media-generation-estonia-border-0-58388ed0-3549-4fda-aedf-6fd3736e41ac.webp"
MEX = f"{PHOTOS}/media-generation-mexico-sinaloa-0-d7cdc2e1-b571-4bc5-a190-6eee76f51e98.webp"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(path, w, h):
    return ImageOps.fit(Image.open(path).convert("RGB"), (w, h),
                        Image.LANCZOS, centering=(0.5, 0.45))


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 4


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # margin
    x0, x1 = M, W - M

    # ---- Masthead ----
    y = 12
    y = draw_centered(d, y, "THE WORLD IN ONE DAY", font(SERIF_B, 58), INK)
    y = draw_centered(d, y + 2, "SUNDAY 22 NOVEMBER 2026",
                      font(SANS_B, 32), RED)
    d.line([(x0, y + 8), (x1, y + 8)], fill=RULE, width=3)
    d.line([(x0, y + 14), (x1, y + 14)], fill=RULE, width=1)
    y += 22

    # ---- Lead story: Gulf escalation ----
    lead_h = 232
    img.paste(fit(LEAD, x1 - x0, lead_h), (x0, y))
    d.rectangle([x0, y, x1, y + lead_h], outline=RULE, width=2)
    y += lead_h + 8
    y = draw_centered(d, y, "IRAN STRIKES US BASE", font(SERIF_B, 36), INK)
    y = draw_centered(d, y - 2, "AS TANKER IS HIT IN HORMUZ",
                      font(SERIF_B, 36), INK)
    y = draw_centered(
        d, y + 2,
        "Tehran targets Bahrain too; ADNOC vessel attacked, one crew missing.",
        font(SANS, 20), GREY)
    d.line([(x0, y + 8), (x1, y + 8)], fill=RULE, width=1)
    y += 16

    # ---- Four panels, 2 x 2 ----
    panels = [
        (PERU, "6.9 QUAKE SHAKES PERU'S ANDES",
         "No casualties reported at first."),
        (COP, "COP31 DEADLOCKED OVER FOSSIL FUELS",
         "Talks run into overtime, no deal yet."),
        (EST, "ESTONIA TO CLOSE RUSSIAN BORDER",
         "Moscow decries a \u201cnew Iron Curtain\u201d."),
        (MEX, "11 KILLED IN MEXICO AFTER CARTEL BOSS HELD",
         "Violence erupts in Sinaloa after the capture."),
    ]
    gap = 16
    pw = (x1 - x0 - gap) // 2
    ph = 150
    py = y
    for i, (photo, head, cap) in enumerate(panels):
        col, row = i % 2, i // 2
        px = x0 + col * (pw + gap)
        pyy = py + row * (ph + 78 + 10)
        img.paste(fit(photo, pw, ph), (px, pyy))
        d.rectangle([px, pyy, px + pw, pyy + ph], outline=RULE, width=1)
        ty = pyy + ph + 5
        for line in wrap(d, head, font(SERIF_B, 22), pw):
            d.text((px, ty), line, font=font(SERIF_B, 22), fill=INK)
            ty += 25
        d.text((px, ty), cap, font=font(SANS, 16), fill=GREY)
    y = py + 2 * (ph + 78 + 10) - 10

    # ---- Ticker ----
    d.line([(x0, y + 4), (x1, y + 4)], fill=RULE, width=1)
    ty = y + 12
    label = "ALSO TODAY: "
    d.text((x0, ty), label, font=font(SANS_B, 16), fill=RED)
    lx = x0 + d.textlength(label, font=font(SANS_B, 16))
    ticker = ("Russia hits Zelenskyy's hometown  \u2022  FBI probes crime-database "
              "hack  \u2022  Australia ends England T20 run")
    d.text((lx, ty), ticker, font=font(SANS, 16), fill=INK)

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
