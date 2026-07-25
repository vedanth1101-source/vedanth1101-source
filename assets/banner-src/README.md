# Banner source

The profile banner is generated deterministically with Pillow (PIL) — not a browser screenshot.

- `gen_banner.py` — renders `../banner-dark.png` and `../banner-light.png` at 2400×600 (2× supersampled).
  Palette: teal `#0d9488` / cyan `#22d3ee` / `#2dd4bf`; name in Segoe UI Semibold; terminal line in Cascadia Code.
- `dark.html` / `light.html` — the original HTML mockups the PIL script was derived from (reference only).

## Regenerate

```bash
pip install pillow numpy
python gen_banner.py
```

Fonts used (Windows): `seguisb.ttf` (Segoe UI Semibold), `segoeui.ttf`, `CascadiaCode.ttf`.
Outputs overwrite the PNGs one directory up, which the profile `README.md` references via a
theme-aware `<picture>` block.
