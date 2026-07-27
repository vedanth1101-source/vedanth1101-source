"""Bake snk's CSS-variable colors into inline SVG presentation attributes.

snk renders the contribution snake with all colors/animation in a <style> block
using CSS custom properties (fill:var(--c1) ...). GitHub does NOT apply that CSS
when the SVG is loaded via <img> from a private repo, so every cell falls back to
no fill and the grid renders black/colorless.

This rewrites each <rect> to carry an inline `fill="#hex"` (and stroke) resolved
from the class -> var -> hex chain. Inline presentation attributes survive GitHub's
CSS stripping, so the heatmap shows its colors statically; if the CSS is ever
honored (e.g. opened directly) it still wins and animates. Run in place:

    python scripts/bake_snake.py dist/github-snake.svg dist/github-snake-dark.svg
"""
import re
import sys


def bake(path):
    svg = open(path, encoding="utf-8").read()
    style = re.search(r"<style>(.*?)</style>", svg, re.S)
    if not style:
        raise SystemExit(f"{path}: no <style> block found")
    sty = style.group(1)

    # --var: value  ->  #hex
    def as_hex(v):
        v = v.strip()
        return v if v.startswith("#") else "#" + v

    varhex = {name: as_hex(val)
              for name, val in re.findall(r"--([a-z0-9]+)\s*:\s*([^;}]+)", sty)}

    # .class { ... fill:var(--x) ... stroke:var(--y) ... }
    class_fill, class_stroke = {}, {}
    for cls, body in re.findall(r"\.([a-z][a-z0-9_-]*)\s*\{([^}]*)\}", sty):
        fm = re.search(r"fill:\s*var\(--([a-z0-9]+)\)", body)
        sm = re.search(r"stroke:\s*var\(--([a-z0-9]+)\)", body)
        if fm and fm.group(1) in varhex:
            class_fill[cls] = varhex[fm.group(1)]
        if sm and sm.group(1) in varhex:
            class_stroke[cls] = varhex[sm.group(1)]

    def resolve(classes):
        # base class 'c' first, then let any more-specific class override fill
        fill = class_fill.get("c")
        stroke = class_stroke.get("c")
        for c in classes:
            if c != "c" and c in class_fill:
                fill = class_fill[c]
            if c != "c" and c in class_stroke:
                stroke = class_stroke[c]
        return fill, stroke

    def repl(m):
        tag, classes = m.group(0), m.group(1).split()
        fill, stroke = resolve(classes)
        add = ""
        if fill and " fill=" not in tag:
            add += f' fill="{fill}"'
        if stroke and " stroke=" not in tag:
            add += f' stroke="{stroke}"'
        return tag[:-2] + add + "/>" if tag.endswith("/>") else tag

    baked = re.sub(r'<rect class="([^"]*)"[^>]*/>', repl, svg)
    open(path, "w", encoding="utf-8").write(baked)
    n = len(re.findall(r"<rect[^>]* fill=", baked))
    print(f"baked {path}: {n} rects given inline fill")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: bake_snake.py <svg> [<svg> ...]")
    for p in sys.argv[1:]:
        bake(p)
