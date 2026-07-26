# Banner source

The profile banner is generated deterministically with Pillow (PIL) — not a browser screenshot.

- `gen_banner.py` — per theme, renders a static `../banner-<theme>.png` (2400×600, 2× supersampled)
  and an animated `../banner-<theme>.gif` (1200×300) whose last prompt line types out rotating
  taglines (`MESSAGES` in the script) with a blinking cursor. Concept: a terminal window (Catppuccin
  Mocha dark / Latte light) with traffic lights, a live zsh session, and syntax coloring. Signature
  peach `#fab387`; all type is Cascadia Code (mono). The GIF stays ~100 KB via `disposal=1`.
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
