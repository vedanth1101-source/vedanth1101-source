"""Generate a Catppuccin contribution-activity area chart as a committed SVG.

The public github-readme-activity-graph service runs out of Vercel quota and
returns HTTP 402, so the README's activity graph intermittently breaks. This
renders the chart ourselves from GitHub's contribution data (fetched via `gh`),
writing assets/activity.svg for the README to load by relative path. A committed
SVG is served by GitHub and always renders; the 12h workflow keeps it current.

    python scripts/gen_activity.py <github_user>

Requires the GitHub CLI (`gh`) authenticated. In CI, set GH_TOKEN.
"""
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone

WINDOW_DAYS = 30

# Catppuccin Mocha
BG = "#1e1e2e"
GRID = "#313244"
PEACH = "#fab387"
MAUVE = "#cba6f7"
TEXT = "#cdd6f4"
DIM = "#6c7086"

W, H = 850, 260
PADL, PADR, PADT, PADB = 48, 20, 52, 34
PLOTW = W - PADL - PADR
PLOTH = H - PADT - PADB
MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fetch(user):
    to = datetime.now(timezone.utc)
    frm = to - timedelta(days=WINDOW_DAYS + 4)
    q = ("{user(login:\"%s\"){contributionsCollection("
         "from:\"%sT00:00:00Z\",to:\"%sT23:59:59Z\"){contributionCalendar"
         "{weeks{contributionDays{date contributionCount}}}}}}"
         % (user, frm.strftime("%Y-%m-%d"), to.strftime("%Y-%m-%d")))
    out = subprocess.run(["gh", "api", "graphql", "-f", f"query={q}"],
                         capture_output=True, text=True, check=True).stdout
    weeks = (json.loads(out)["data"]["user"]["contributionsCollection"]
             ["contributionCalendar"]["weeks"])
    days = [d for w in weeks for d in w["contributionDays"]]
    days = days[-WINDOW_DAYS:]
    while len(days) > 2 and days[-1]["contributionCount"] == 0:
        days.pop()  # drop today/incomplete trailing zeros so the line doesn't dip
    return days


def smooth(pts):
    """Catmull-Rom spline through pts as a cubic-bezier path string."""
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1x, c1y = p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6
        c2x, c2y = p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6
        d += f" C {c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def fmt_date(s):
    y, m, dd = s.split("-")
    return f"{MONTHS[int(m)]} {int(dd)}"


def render(days):
    counts = [d["contributionCount"] for d in days]
    n = len(counts)
    maxc = max(counts) or 1
    baseline = PADT + PLOTH

    def px(i):
        return PADL + (i / (n - 1) * PLOTW if n > 1 else PLOTW / 2)

    def py(c):
        return PADT + PLOTH - (c / maxc) * (PLOTH - 6)

    pts = [(px(i), py(c)) for i, c in enumerate(counts)]
    line = smooth(pts)
    area = f"{line} L {pts[-1][0]:.1f},{baseline} L {pts[0][0]:.1f},{baseline} Z"

    svg = [
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' "
        f"width='{W}' height='{H}' font-family=\"'Segoe UI',Ubuntu,Helvetica,sans-serif\">",
        f"<rect width='{W}' height='{H}' rx='6' fill='{BG}'/>",
        f"<defs><linearGradient id='a' x1='0' y1='0' x2='0' y2='1'>"
        f"<stop offset='0' stop-color='{PEACH}' stop-opacity='0.35'/>"
        f"<stop offset='1' stop-color='{PEACH}' stop-opacity='0'/></linearGradient></defs>",
        f"<text x='{PADL - 20}' y='32' fill='{PEACH}' font-size='18' "
        f"font-weight='600'>Contribution Activity</text>",
    ]
    # horizontal gridlines + y labels
    for freq in (0, 0.5, 1.0):
        val = round(maxc * freq)
        y = PADT + PLOTH - freq * (PLOTH - 6)
        svg.append(f"<line x1='{PADL}' y1='{y:.1f}' x2='{W - PADR}' y2='{y:.1f}' "
                   f"stroke='{GRID}' stroke-width='1'/>")
        svg.append(f"<text x='{PADL - 8}' y='{y + 4:.1f}' fill='{DIM}' font-size='11' "
                   f"text-anchor='end'>{val}</text>")
    # area + line
    svg.append(f"<path d='{area}' fill='url(#a)'/>")
    svg.append(f"<path d='{line}' fill='none' stroke='{PEACH}' stroke-width='2.5' "
               f"stroke-linecap='round' stroke-linejoin='round'/>")
    # points
    for x, y in pts:
        svg.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='2.4' fill='{MAUVE}'/>")
    # x labels (~6 evenly spaced)
    step = max(1, (n - 1) // 5)
    for i in range(0, n, step):
        svg.append(f"<text x='{px(i):.1f}' y='{baseline + 20:.1f}' fill='{DIM}' "
                   f"font-size='11' text-anchor='middle'>{fmt_date(days[i]['date'])}</text>")
    svg.append("</svg>")
    return "".join(svg)


def main(user):
    days = fetch(user)
    if len(days) < 2:
        print("not enough data; keeping existing assets/activity.svg")
        return
    open("assets/activity.svg", "w", encoding="utf-8").write(render(days))
    print(f"wrote assets/activity.svg ({len(days)} days, peak {max(d['contributionCount'] for d in days)})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "vedanth1101-source")
