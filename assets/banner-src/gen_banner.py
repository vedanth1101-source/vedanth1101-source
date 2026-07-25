"""Render the profile banner (dark + light) as high-res PNGs with PIL."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
S = 2  # supersample / retina scale
W, H = 1200 * S, 300 * S

FONTS = "C:/Windows/Fonts/"
def font(name, px):
    return ImageFont.truetype(FONTS + name, px * S)

NAME_F = "seguisb.ttf"      # Segoe UI Semibold
TAG_F  = "segoeui.ttf"      # Segoe UI
TAGB_F = "seguisb.ttf"
MONO_F = "CascadiaCode.ttf"


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


THEMES = {
    "dark": {
        "top": "#0d1117", "bot": "#010409",
        "glows": [("#22d3ee", 0.16, 0.88, -0.20, 1.15),
                  ("#0d9488", 0.14, 1.02, 1.15, 0.95)],
        "scan": (255, 255, 255, 6),
        "name": "#f0f6fc", "eyebrow": "#2dd4bf", "dot": "#2dd4bf",
        "tag_strong": "#cdd9e5", "tag_mid": "#9aa5b1", "tag_accent": "#2dd4bf",
        "term": "#6e7d8f", "prompt": "#2dd4bf", "cursor": "#2dd4bf",
        "rule": ("#0d9488", "#22d3ee"), "accent_bar": ("#0d9488", "#22d3ee"),
    },
    "light": {
        "top": "#ffffff", "bot": "#f2f5f9",
        "glows": [("#0d9488", 0.10, 0.88, -0.20, 1.15),
                  ("#0891b2", 0.10, 1.02, 1.15, 0.95)],
        "scan": (0, 0, 0, 4),
        "name": "#0b1220", "eyebrow": "#0f766e", "dot": "#0d9488",
        "tag_strong": "#1f2937", "tag_mid": "#55627a", "tag_accent": "#0f766e",
        "term": "#6b7688", "prompt": "#0f766e", "cursor": "#0d9488",
        "rule": ("#0d9488", "#0891b2"), "accent_bar": ("#0d9488", "#0891b2"),
    },
}


def background(t):
    top = np.array(hex_rgb(t["top"]), float)
    bot = np.array(hex_rgb(t["bot"]), float)
    ramp = np.linspace(0, 1, H)[:, None]
    base = (top[None, :] * (1 - ramp) + bot[None, :] * ramp)
    img = np.repeat(base[:, None, :], W, axis=1)

    yy, xx = np.mgrid[0:H, 0:W]
    for hexc, alpha, cx, cy, radius in t["glows"]:
        c = np.array(hex_rgb(hexc), float)
        d = np.sqrt(((xx - cx * W) / (radius * W)) ** 2 +
                    ((yy - cy * H) / (radius * W)) ** 2)
        g = np.clip(1 - d, 0, 1) ** 2 * alpha
        img = img * (1 - g[:, :, None]) + c[None, None, :] * g[:, :, None]

    return Image.fromarray(np.clip(img, 0, 255).astype("uint8"), "RGB").convert("RGBA")


def hgrad_bar(w, h, c0, c1):
    a = np.array(hex_rgb(c0), float)
    b = np.array(hex_rgb(c1), float)
    ramp = np.linspace(0, 1, w)[:, None]
    row = (a[None, :] * (1 - ramp) + b[None, :] * ramp)
    arr = np.repeat(row[None, :, :], h, axis=0)
    return Image.fromarray(arr.astype("uint8"), "RGB")


def draw_tracked(draw, xy, text, fnt, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking * S
    return x


def build(theme_name):
    t = THEMES[theme_name]
    img = background(t)
    d = ImageDraw.Draw(img)

    # top hairline accent, faded at the ends
    bar = hgrad_bar(W, 4 * S, *t["accent_bar"]).convert("RGBA")
    mask = np.zeros((4 * S, W), "uint8")
    xr = np.linspace(0, 1, W)
    edge = np.clip(np.minimum(xr / 0.30, (1 - xr) / 0.55), 0, 1)
    mask[:] = (edge * 235).astype("uint8")[None, :]
    bar.putalpha(Image.fromarray(mask, "L"))
    img.alpha_composite(bar, (0, 0))

    # scanlines
    scan = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scan)
    for y in range(0, H, 3 * S):
        sd.line([(0, y), (W, y)], fill=t["scan"], width=S)
    img.alpha_composite(scan)

    d = ImageDraw.Draw(img)
    left = 72 * S
    top = 60 * S

    # eyebrow: dot + tracked mono label
    dot = 7 * S
    ey_y = top
    d.ellipse([left, ey_y + 3 * S, left + dot, ey_y + 3 * S + dot], fill=hex_rgb(t["dot"]))
    eb_font = font(MONO_F, 14)
    draw_tracked(d, (left + dot + 16 * S, ey_y), "SOFTWARE  ENGINEER", eb_font,
                 hex_rgb(t["eyebrow"]), 3)

    # name
    name_font = font(NAME_F, 60)
    name_y = ey_y + 40 * S
    end_x = draw_tracked(d, (left, name_y), "VEDANTH   M   S", name_font,
                         hex_rgb(t["name"]), 7)
    nb = name_font.getbbox("VEDANTH")
    name_h = nb[3] - nb[1]

    # accent rule
    rule_y = name_y + name_h + 26 * S
    rule = hgrad_bar(108 * S, 3 * S, *t["rule"])
    img.paste(rule, (left, rule_y))

    # tagline (mixed colours)
    d = ImageDraw.Draw(img)
    tag_y = rule_y + 22 * S
    tf = font(TAG_F, 23)
    tfb = font(TAGB_F, 23)
    segs = [("Backend systems", tfb, t["tag_strong"]),
            ("  &  ", tf, t["tag_mid"]),
            ("AI-integrated", tfb, t["tag_accent"]),
            (" applications", tf, t["tag_mid"])]
    x = left
    for text, fnt, col in segs:
        d.text((x, tag_y), text, font=fnt, fill=hex_rgb(col))
        x += d.textlength(text, font=fnt)

    # terminal line + cursor
    term_font = font(MONO_F, 15)
    term_y = H - 62 * S
    d.text((left, term_y), ">", font=term_font, fill=hex_rgb(t["prompt"]))
    tx = left + d.textlength("> ", font=term_font) + 6 * S
    msg = "building systems that make decisions in milliseconds"
    d.text((tx, term_y), msg, font=term_font, fill=hex_rgb(t["term"]))
    cx = tx + d.textlength(msg, font=term_font) + 8 * S
    tb = term_font.getbbox("Ag")
    d.rectangle([cx, term_y + tb[1], cx + 8 * S, term_y + tb[3]], fill=hex_rgb(t["cursor"]))

    path = os.path.join(OUT, f"banner-{theme_name}.png")
    img.convert("RGB").save(path, "PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    build("dark")
    build("light")
