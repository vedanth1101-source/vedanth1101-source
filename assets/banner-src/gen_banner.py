"""Render the profile banner (dark + light) with PIL.

Concept: a real terminal window (Catppuccin Mocha / Latte), not mono-as-costume.
Title bar with traffic lights, a live zsh session with syntax-accurate coloring,
the name as the large output of `whoami --name`, and a last prompt line that
TYPES OUT rotating taglines with a blinking cursor.

Each theme is written twice:
  - banner-<theme>.png  : static fallback (first tagline fully typed)
  - banner-<theme>.gif  : animated typing loop
Deterministic — NOT a browser screenshot. Rendered at 2x, GIF downscaled to 1x.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # -> assets/
S = 2  # supersample / retina scale
W, H = 1200 * S, 320 * S

FONTS = "C:/Windows/Fonts/"
MONO_F = "CascadiaCode.ttf"

# Taglines typed on the last prompt line (rotating). Kept truthful.
MESSAGES = [
    "rule engines · developer tooling · agentic systems",
    "decisions in single-digit milliseconds",
    "final-year CS @ SSN College of Engineering",
]


def font(px):
    return ImageFont.truetype(FONTS + MONO_F, px * S)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# Catppuccin Mocha (dark) / Latte (light). One palette, two renditions.
THEMES = {
    "dark": {
        "desk_top": "#0c0c14", "desk_bot": "#08080e",
        "window": "#1e1e2e", "titlebar": "#181825", "hairline": "#313244",
        "dot_r": "#f38ba8", "dot_y": "#f9e2af", "dot_g": "#a6e3a1",
        "title": "#7f849c",
        "text": "#cdd6f4", "muted": "#a6adc8", "dim": "#6c7086",
        "green": "#a6e3a1", "blue": "#89b4fa", "peach": "#fab387",
        "mauve": "#cba6f7", "yellow": "#f9e2af",
        "name": "#cdd6f4",
        "shadow": (0, 0, 0, 150),
    },
    "light": {
        "desk_top": "#dce0e8", "desk_bot": "#c9cdda",
        "window": "#eff1f5", "titlebar": "#e6e9ef", "hairline": "#bcc0cc",
        "dot_r": "#d20f39", "dot_y": "#df8e1d", "dot_g": "#40a02b",
        "title": "#8c8fa1",
        "text": "#4c4f69", "muted": "#6c6f85", "dim": "#9ca0b0",
        "green": "#40a02b", "blue": "#1e66f5", "peach": "#fe640b",
        "mauve": "#8839ef", "yellow": "#df8e1d",
        "name": "#4c4f69",
        "shadow": (60, 66, 97, 70),
    },
}


def desktop(t):
    """Vertical gradient backdrop the terminal window floats on."""
    top = hex_rgb(t["desk_top"])
    bot = hex_rgb(t["desk_bot"])
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        f = y / (H - 1)
        row = tuple(round(top[i] * (1 - f) + bot[i] * f) for i in range(3))
        for x in range(W):
            px[x, y] = row
    return img.convert("RGBA")


def draw_segs(d, x, y, segs, fnt):
    """Draw a run of (text, hexcolor) segments in mono; return the end x."""
    for text, col in segs:
        d.text((x, y), text, font=fnt, fill=hex_rgb(col))
        x += d.textlength(text, font=fnt)
    return x


def compose(t, typed_text, cursor_on):
    """Full terminal frame. `typed_text` fills the last prompt line; the peach
    cursor block trails it when `cursor_on`."""
    img = desktop(t)

    mx, my = 18 * S, 15 * S
    win = (mx, my, W - mx, H - my)
    radius = 22 * S
    titlebar_h = 58 * S

    # drop shadow (offset + blur, never a flat halo)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    off = 10 * S
    sd.rounded_rectangle((win[0], win[1] + off, win[2], win[3] + off),
                         radius=radius, fill=t["shadow"])
    shadow = shadow.filter(ImageFilter.GaussianBlur(22 * S))
    img.alpha_composite(shadow)

    # window body + title bar
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(win, radius=radius, fill=hex_rgb(t["window"]))
    d.rounded_rectangle((win[0], win[1], win[2], win[1] + titlebar_h + radius),
                        radius=radius, fill=hex_rgb(t["titlebar"]))
    d.rectangle((win[0], win[1] + titlebar_h, win[2], win[1] + titlebar_h + radius),
                fill=hex_rgb(t["window"]))
    d.line((win[0], win[1] + titlebar_h, win[2], win[1] + titlebar_h),
           fill=hex_rgb(t["hairline"]), width=max(1, S))

    # traffic lights
    cy = win[1] + titlebar_h // 2
    dot_r = 8 * S
    dx = win[0] + 34 * S
    for col in (t["dot_r"], t["dot_y"], t["dot_g"]):
        d.ellipse((dx - dot_r, cy - dot_r, dx + dot_r, cy + dot_r), fill=hex_rgb(col))
        dx += 30 * S

    # centered title
    tf = font(14)
    title = "vedanth@github \u2014 zsh"
    tw = d.textlength(title, font=tf)
    tb = tf.getbbox(title)
    d.text(((W - tw) / 2, cy - (tb[3] - tb[1]) / 2 - tb[1]),
           title, font=tf, fill=hex_rgb(t["title"]))

    # terminal session
    pf = font(18)
    of = font(17)
    nf = font(46)
    cx0 = win[0] + 46 * S
    y = win[1] + titlebar_h + 34 * S

    def prompt(cmd_segs):
        base = [("vedanth@portfolio", t["green"]), (" ", t["muted"]),
                ("~", t["blue"]), (" ", t["muted"]), ("%", t["peach"]),
                ("  ", t["muted"])]
        return base + cmd_segs

    draw_segs(d, cx0, y, prompt([("whoami", t["mauve"]), (" --name", t["yellow"])]), pf)
    y += 26 * S

    d.text((cx0, y), "VEDANTH  M  S", font=nf, fill=hex_rgb(t["name"]),
           stroke_width=max(1, S // 2), stroke_fill=hex_rgb(t["name"]))
    y += 60 * S

    draw_segs(d, cx0, y, prompt([("cat", t["mauve"]), (" role.txt", t["blue"])]), pf)
    y += 22 * S
    draw_segs(d, cx0, y, [("Backend & ", t["muted"]),
                          ("AI-Integrated", t["peach"]),
                          (" Software Engineer", t["muted"])], of)
    y += 30 * S

    # last line: prompt prefix + typed tagline + blinking cursor
    endx = draw_segs(d, cx0, y, prompt([]), pf)
    if typed_text:
        d.text((endx, y), typed_text, font=pf, fill=hex_rgb(t["text"]))
        endx += d.textlength(typed_text, font=pf)
    if cursor_on:
        cb = pf.getbbox("M")
        d.rectangle((endx + 2 * S, y + cb[1], endx + 13 * S, y + cb[3]),
                    fill=hex_rgb(t["peach"]))
    return img


def build_static(theme_name):
    t = THEMES[theme_name]
    img = compose(t, MESSAGES[0], True)
    path = os.path.join(OUT, f"banner-{theme_name}.png")
    img.convert("RGB").save(path, "PNG")
    print("wrote", path, img.size)


def build_gif(theme_name):
    t = THEMES[theme_name]
    step = 3            # chars revealed per typing frame
    type_ms = 60        # per typing frame
    blink_ms = 430      # per blink frame while holding
    holds = 4           # blink cycles held after a line finishes
    small = (W // S, H // S)

    frames, durs = [], []
    for msg in MESSAGES:
        for k in range(0, len(msg) + 1, step):
            frames.append(compose(t, msg[:k], True))
            durs.append(type_ms)
        for b in range(holds * 2):
            frames.append(compose(t, msg, b % 2 == 0))
            durs.append(blink_ms)

    # downscale to 1x (crisp) and quantize to one shared palette. disposal=1
    # keeps prior pixels so Pillow's optimizer stores only the changed strip
    # (the typing line), which is what keeps the GIF small.
    rgb = [f.convert("RGB").resize(small, Image.LANCZOS) for f in frames]
    pal = rgb[0].convert("P", palette=Image.ADAPTIVE, colors=160)
    pframes = [f.quantize(palette=pal, dither=Image.NONE) for f in rgb]

    path = os.path.join(OUT, f"banner-{theme_name}.gif")
    pframes[0].save(path, save_all=True, append_images=pframes[1:],
                    duration=durs, loop=0, optimize=True, disposal=1)
    kb = os.path.getsize(path) // 1024
    print("wrote", path, small, f"{len(pframes)} frames", f"{kb} KB")


if __name__ == "__main__":
    for name in ("dark", "light"):
        build_static(name)
        build_gif(name)
