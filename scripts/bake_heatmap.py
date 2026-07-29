"""Bake a theme-matched contribution heatmap from ghchart.rshah.org.

ghchart renders the GitHub contribution grid but hardcodes empty cells to
light gray (#EEEEEE) and labels to #767676 — bright squares that clash on a
dark README. We fetch it once (base color = peach) and recolor its five fixed
levels + labels into the repo's Catppuccin palette, writing a dark and a light
SVG that the README loads by relative path (like the snake it replaces).

The five source hexes are deterministic for base=fab387 (ghchart derives a fixed
ramp from the base color, independent of the contribution data), so the literal
mapping below is stable as cells fill in.

    python scripts/bake_heatmap.py <github_user>
"""
import re
import sys
import urllib.request

BASE = "fab387"  # ghchart base color -> fixed 5-level ramp recolored below

# source hex (from ghchart, base=fab387) -> theme hex.  L0 = empty cell.
DARK = {
    "#eeeeee": "#45475a",  # L0 empty  (matches snake dots)
    "#ffffd4": "#8a5e46",  # L1
    "#ffe6ba": "#b87f4d",  # L2
    "#c88f6c": "#e09a58",  # L3
    "#fab387": "#fab387",  # L4 peak (signature peach, unchanged)
    "#767676": "#6c7086",  # month/day labels
}
LIGHT = {
    "#eeeeee": "#e6e9ef",
    "#ffffd4": "#f6d9bf",
    "#ffe6ba": "#f2b98a",
    "#c88f6c": "#ec8f4e",
    "#fab387": "#fe640b",
    "#767676": "#8c8fa1",
}


def fetch(user):
    url = f"https://ghchart.rshah.org/{BASE}/{user}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last = None
    for _ in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                svg = r.read().decode("utf-8")
            if "<svg" in svg and "rect" in svg:
                return svg
        except Exception as e:  # transient TLS/network on ghchart is common
            last = e
    raise SystemExit(f"ghchart fetch failed for {user}: {last}")


def recolor(svg, mapping):
    def sub(m):
        return "#" + mapping[("#" + m.group(1).lower())][1:]
    keys = "|".join(k[1:] for k in mapping)
    return re.sub(f"#({keys})", sub, svg, flags=re.IGNORECASE)


def main(user):
    svg = fetch(user)
    for name, mapping in (("dark", DARK), ("light", LIGHT)):
        out = f"assets/heatmap-{name}.svg"
        open(out, "w", encoding="utf-8").write(recolor(svg, mapping))
        print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "vedanth1101-source")
