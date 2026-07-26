# Banner source

The profile banner is generated deterministically with Pillow (PIL) — not a browser screenshot.

- `gen_banner.py` — renders `../banner-dark.png` and `../banner-light.png` at 2400×600 (2× supersampled).
  Concept: a terminal window (Catppuccin Mocha dark / Latte light) with traffic lights, a live zsh
  session, and syntax coloring. Signature peach `#fab387`; all type is Cascadia Code (mono).
- `dark.html` / `light.html` — **stale**: HTML mockups of the previous teal/CRT design, kept for
  reference only. They do not match the current terminal concept and do not feed the build.

## Regenerate

```bash
pip install pillow numpy
python gen_banner.py
```

Font used (Windows): `CascadiaCode.ttf`.
Outputs overwrite the PNGs one directory up (`../banner-*.png`), which the profile `README.md`
references via a theme-aware `<picture>` block.
