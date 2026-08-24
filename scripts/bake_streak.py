"""Bake the contribution-streak card into a committed SVG.

The public streak-stats.demolab.com instance shares one GitHub token across
everyone, so it frequently rate-limits and returns an error card ("Failed to
retrieve contributions") or fails the image request outright. Referencing it
live means the streak intermittently vanishes from the README.

Instead we fetch it here, KEEP IT ONLY IF IT'S A VALID CARD, and write it to
assets/streak.svg for the README to load by relative path. A committed file is
served by GitHub itself and always renders. On a bad/failed fetch we leave the
existing file untouched, so the last good card stays visible indefinitely.

    python scripts/bake_streak.py <github_user>
"""
import sys
import time
import urllib.request

OUT = "assets/streak.svg"

# Card styling — keep in sync with the theme. (Mirrors the params the README
# previously passed to streak-stats.demolab.com.)
PARAMS = (
    "card_width=850&hide_border=true&background=1e1e2e&stroke=313244"
    "&ring=fab387&fire=f38ba8&currStreakLabel=fab387&sideLabels=a6adc8"
    "&dates=6c7086&currStreakNum=cdd6f4&sideNums=cdd6f4"
)


def is_valid_card(svg):
    """A good card carries the streak labels; the error card says it failed."""
    if "Failed to retrieve" in svg or "Something went wrong" in svg:
        return False
    return "<svg" in svg and "Current Streak" in svg


def fetch(user, attempts=6):
    url = f"https://streak-stats.demolab.com?user={user}&{PARAMS}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for i in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                svg = r.read().decode("utf-8")
            if is_valid_card(svg):
                return svg
            print(f"attempt {i + 1}: error/degraded card, retrying")
        except Exception as e:
            print(f"attempt {i + 1}: {e}")
        time.sleep(5)  # let a transient rate-limit clear (python sleep, not shell)
    return None


def main(user):
    svg = fetch(user)
    if svg is None:
        print(f"no valid card this run; keeping existing {OUT}")
        return  # exit 0 — do NOT overwrite the last good card
    open(OUT, "w", encoding="utf-8").write(svg)
    print(f"wrote {OUT} ({len(svg)} bytes)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "vedanth1101-source")
