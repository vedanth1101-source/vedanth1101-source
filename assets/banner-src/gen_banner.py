"""Render the profile banner (dark + light) as high-res PNGs with PIL.

Concept: a real terminal window (Catppuccin Mocha / Latte), not mono-as-costume.
Title bar with traffic lights, a live zsh session with syntax-accurate coloring,
the name as the large output of `whoami --name`, and a blinking cursor block.
Deterministic — NOT a browser screenshot. Output is 2400x600 (2x supersampled).
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # -> assets/
S = 2  # supersample / retina scale
W, H = 1200 * S, 300 * S

FONTS = "C:/Windows/Fonts/"
MONO_F = "CascadiaCode.ttf"


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
        px_row = tuple(round(top[i] * (1 - f) + bot[i] * f) for i in range(3))
        for x in range(W):
            px[x, y] = px_row
    return img.convert("RGBA")


def draw_segs(d, x, y, segs, fnt):
    """Draw a run of (text, hexcolor) segments in mono; return the end x."""
    for text, col in segs:
        d.text((x, y), text, font=fnt, fill=hex_rgb(col))
        x += d.textlength(text, font=fnt)
    return x


def build(theme_name):
    t = THEMES[theme_name]
    img = desktop(t)

    # ---- window geometry ----
    mx, my = 34 * S, 26 * S
    win = (mx, my, W - mx, H - my)
    radius = 24 * S
    titlebar_h = 66 * S

    # ---- drop shadow (offset + blur, never a flat halo) ----
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    off = 10 * S
    sd.rounded_rectangle((win[0], win[1] + off, win[2], win[3] + off),
                         radius=radius, fill=t["shadow"])
    shadow = shadow.filter(ImageFilter.GaussianBlur(22 * S))
    img.alpha_composite(shadow)

    # ---- window body + title bar ----
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(win, radius=radius, fill=hex_rgb(t["window"]))
    # title bar: rounded top, squared bottom (clip via a second fill)
    d.rounded_rectangle((win[0], win[1], win[2], win[1] + titlebar_h + radius),
                        radius=radius, fill=hex_rgb(t["titlebar"]))
    d.rectangle((win[0], win[1] + titlebar_h, win[2], win[1] + titlebar_h + radius),
                fill=hex_rgb(t["window"]))
    d.line((win[0], win[1] + titlebar_h, win[2], win[1] + titlebar_h),
           fill=hex_rgb(t["hairline"]), width=max(1, S))

    # ---- traffic lights ----
    cy = win[1] + titlebar_h // 2
    dot_r = 8 * S
    dx = win[0] + 34 * S
    for col in (t["dot_r"], t["dot_y"], t["dot_g"]):
        d.ellipse((dx - dot_r, cy - dot_r, dx + dot_r, cy + dot_r), fill=hex_rgb(col))
        dx += 30 * S

    # ---- title (centered) ----
    tf = font(14)
    title = "vedanth@github \u2014 zsh"
    tw = d.textlength(title, font=tf)
    tb = tf.getbbox(title)
    d.text(((W - tw) / 2, cy - (tb[3] - tb[1]) / 2 - tb[1]),
           title, font=tf, fill=hex_rgb(t["title"]))

    # ---- terminal session ----
    pf = font(17)          # prompt / command lines
    of = font(16)          # command output
    nf = font(40)          # the name (hero)
    cx0 = win[0] + 48 * S
    y = win[1] + titlebar_h + 30 * S

    def prompt(cmd_segs):
        base = [("vedanth@portfolio", t["green"]), (" ", t["muted"]),
                ("~", t["blue"]), (" ", t["muted"]), ("%", t["peach"]),
                ("  ", t["muted"])]
        return base + cmd_segs

    # line 1: whoami --name
    draw_segs(d, cx0, y, prompt([("whoami", t["mauve"]), (" --name", t["yellow"])]), pf)
    y += 21 * S

    # hero: the name as command output (faux-bold via stroke)
    d.text((cx0, y), "VEDANTH  M  S", font=nf, fill=hex_rgb(t["name"]),
           stroke_width=max(1, S // 2), stroke_fill=hex_rgb(t["name"]))
    y += 46 * S

    # line 2: cat role.txt
    draw_segs(d, cx0, y, prompt([("cat", t["mauve"]), (" role.txt", t["blue"])]), pf)
    y += 19 * S
    draw_segs(d, cx0, y, [("Backend & ", t["muted"]),
                          ("AI-Integrated", t["peach"]),
                          (" Software Engineer", t["muted"])], of)
    y += 22 * S

    # line 3: prompt + blinking cursor block
    endx = draw_segs(d, cx0, y, prompt([]), pf)
    cb = pf.getbbox("M")
    d.rectangle((endx, y + cb[1], endx + 11 * S, y + cb[3]), fill=hex_rgb(t["peach"]))

    path = os.path.join(OUT, f"banner-{theme_name}.png")
    img.convert("RGB").save(path, "PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    build("dark")
    build("light")
