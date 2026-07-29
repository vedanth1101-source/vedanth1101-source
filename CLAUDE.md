# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is a **GitHub profile README** repository, not an application. For it to render on the
GitHub profile page, the repo must be named exactly `vedanth1101-source` (the account username)
**and be public**. It is currently **private**, so the README does not display on the profile
until visibility is changed:

```bash
gh repo edit vedanth1101-source/vedanth1101-source --visibility public --accept-visibility-change-consequences
```

There is no conventional build/lint/test. The only executable code is the banner generator.

## The one real build step: the banner

`assets/banner-src/gen_banner.py` renders the banner **deterministically with Pillow**
(NOT browser screenshots). Per theme it writes two files: `banner-<theme>.png` (static, 2400×986 ~2.43:1
2× supersampled) and `banner-<theme>.gif` (1200×493 animated — the last prompt line types out
rotating taglines, `MESSAGES` in the script). The `README.md` `<picture>` block uses the **GIFs**
as the theme-aware sources (`banner-dark.gif` / `banner-light.gif`) with the dark PNG as `<img>` fallback.
The GIF stays small (~100 KB) via `disposal=1` so only the changed typing strip is stored per frame.

Regenerate (run from `assets/banner-src/`, overwrites the four files one directory up):

```bash
pip install pillow numpy
python gen_banner.py
```

The script hardcodes Windows font paths (`C:/Windows/Fonts/`): `seguisb.ttf` (Segoe UI Semibold),
`segoeui.ttf`, `CascadiaCode.ttf`. On another OS these paths must change. `dark.html` / `light.html`
in the same folder are reference mockups the PIL script was derived from — they do not feed the build.

## Single theme, enforced by hand across many surfaces

Everything is unified under one Catppuccin-based terminal palette (Mocha dark / Latte light). The
same colors are duplicated as literals in several independent places, so a theme change means editing
all of them in lockstep — there is no shared config:

- `THEMES` dict in `gen_banner.py` (terminal window body, title bar, traffic lights, syntax coloring)
- `github-readme-stats` / `top-langs` / `streak-stats` / `activity-graph` query params in `README.md`
  (`title_color=fab387`, `icon_color=89b4fa`, `text_color=cdd6f4`, `bg_color=1e1e2e`, etc.)
- snake colors in `.github/workflows/snake.yml` (`color_snake`, `color_dots`)

Core palette (Mocha): signature peach `#fab387`; mauve `#cba6f7`, blue `#89b4fa`, green `#a6e3a1`;
text `#cdd6f4` / muted `#a6adc8` / dim `#6c7086`; surfaces crust `#11111b` / base `#1e1e2e`.
Light renders as Catppuccin Latte (bg `#eff1f5`, peach `#fe640b`).

## External-service dependencies baked into README URLs

The README pulls live images from third-party render services with the username embedded in each URL:
`readme-typing-svg.demolab.com`, `skillicons.dev`, `github-readme-stats.vercel.app`,
`streak-stats.demolab.com`, `github-readme-activity-graph.vercel.app`, `komarev.com` (view counter),
`capsule-render.vercel.app`. Renaming the account or changing the theme requires updating these URLs.

## Contribution snake

`.github/workflows/snake.yml` (Platane/snk) runs every 12h, on push to `main`, and on manual
dispatch. Because the repo is **private**, `raw.githubusercontent.com/.../output/...` is not
publicly fetchable and GitHub's image proxy 404s it — so the workflow commits the snake SVGs to
**`assets/github-snake-dark.svg` / `assets/github-snake.svg` on `main`** (not the old `output`
branch), and the README's snake `<picture>` loads them by **relative path** (like the banner).
The auto-commit uses `[skip ci]` so it does not retrigger the workflow. If the repo is ever made
public, either relative paths or the original `output`-branch raw URLs would work.

## Verifying a change actually renders

GitHub's README rendering differs from raw Markdown preview. After editing `README.md`, confirm the
rendered HTML:

```bash
gh api repos/vedanth1101-source/vedanth1101-source/readme -H "Accept: application/vnd.github.html+json"
```

## Project links caveat

The "Selected Work" repos (sentinelx, BugBuddy, farm-manager-ai-poc) may be private; their links 404
for logged-out visitors when private.
