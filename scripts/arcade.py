#!/usr/bin/env python3
"""Render a GitHub contribution calendar as a Pac-Man arcade SVG.

Pac-Man walks the calendar column by column and eats a pellet on every day
with contributions. Each eaten day lights up in GitHub's own color for that
day, so the final frame is the real contribution graph.

Usage:
  GITHUB_TOKEN=... python3 arcade.py --login USER --out arcade/arcade.svg
  python3 arcade.py --login USER --data sample.json --out arcade.svg
"""

import argparse
import datetime as dt
import json
import os
import urllib.request

# ---------------------------------------------------------------- data

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel weekday } }
      }
    }
  }
}
"""

LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2,
          "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def fetch_calendar(login, token):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {token}",
                 "Content-Type": "application/json",
                 "User-Agent": "contribution-arcade"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


# ---------------------------------------------------------------- style

W = 900
CELL, GAP = 13, 3
PITCH = CELL + GAP
GRID_Y = 82
EMPTY = "#161b22"
GREENS = ["#0e4429", "#006d32", "#26a641", "#39d353"]
WALL = "#2a3cff"
PELLET = "#ffcfa0"
PAC = "#ffd60a"
GHOSTS = [("#ff2a2a", 1.0), ("#ffb8ff", 1.6), ("#26e6ff", 2.2), ("#ffb852", 2.8)]
FONT = "'Courier New',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

STEP_EMPTY = 0.045   # seconds per empty cell
STEP_PELLET = 0.11   # seconds per pellet cell
INTRO = 2.2          # READY!
HOLD = 6.5           # STAGE CLEAR, full graph on screen
FRIGHT = 3.0         # seconds ghosts stay blue after a power pellet


def f(x):
    return f"{x:.4f}".rstrip("0").rstrip(".")


def kt(times, total):
    return ";".join(f(min(max(t / total, 0.0), 1.0)) for t in times)


# ---------------------------------------------------------------- build

def build(cal, login):
    weeks = cal["weeks"]
    ncols = len(weeks)
    grid_w = ncols * PITCH - GAP
    gx = (W - grid_w) / 2

    days = []  # (col, row, date, count, level)
    for c, wk in enumerate(weeks):
        for d in wk["contributionDays"]:
            days.append((c, d["weekday"], d["date"], d["contributionCount"],
                         LEVELS[d["contributionLevel"]]))
    by_cell = {(c, r): (date, n, lv) for c, r, date, n, lv in days}

    def center(c, r):
        return gx + c * PITCH + CELL / 2, GRID_Y + r * PITCH + CELL / 2

    # Serpentine path through every existing day, then off the right edge.
    nodes = []
    for c in range(ncols):
        rows = range(7) if c % 2 == 0 else range(6, -1, -1)
        nodes += [(c, r) for r in rows if (c, r) in by_cell]
    last_c, last_r = nodes[-1]
    exit_pts = [(last_c + k, last_r) for k in (1, 2, 3, 4)]

    # Pac-Man arrival time at each node.
    arrive, t = [], INTRO
    for i, node in enumerate(nodes):
        if i:
            t += STEP_PELLET if by_cell[node][1] > 0 else STEP_EMPTY
        arrive.append(t)
    for _ in exit_pts:
        t += STEP_EMPTY * 1.5
        arrive.append(t)
    pac_end = arrive[-1]
    ghost_end = pac_end + max(lag for _, lag in GHOSTS)
    clear_at = ghost_end + 0.2
    T = clear_at + HOLD

    path_pts = [center(c, r) for c, r in nodes + exit_pts]
    path_d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in path_pts)
    npts = len(path_pts)
    key_points = [i / (npts - 1) for i in range(npts)]

    # Eat events and stats.
    eat = {}  # node -> time
    for i, node in enumerate(nodes):
        if by_cell[node][1] > 0:
            eat[node] = arrive[i]
    events = sorted((tm, by_cell[node][1]) for node, tm in eat.items())
    total = cal["totalContributions"]

    fright = []
    for node, tm in sorted(eat.items(), key=lambda kv: kv[1]):
        if by_cell[node][2] == 4:
            if fright and tm <= fright[-1][1]:
                fright[-1][1] = tm + FRIGHT
            else:
                fright.append([tm, tm + FRIGHT])

    ordered = sorted(days, key=lambda d: d[2])
    longest = run = 0
    for d in ordered:
        run = run + 1 if d[3] > 0 else 0
        longest = max(longest, run)
    best = max(d[3] for d in ordered)
    active = sum(1 for d in ordered if d[3] > 0)

    out = []
    a = out.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="268" '
      f'viewBox="0 0 {W} 268" font-family="{FONT}" font-weight="700">')
    a(f"<title>{login} contribution arcade: {total:,} contributions in the last year</title>")
    a("<defs>"
      '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">'
      '<feGaussianBlur stdDeviation="1.6" result="b"/>'
      '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
      '<linearGradient id="sweep" x1="0" x2="1">'
      '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
      '<stop offset=".5" stop-color="#fff" stop-opacity=".35"/>'
      '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
      '<radialGradient id="vignette" cx=".5" cy=".5" r=".75">'
      '<stop offset=".6" stop-color="#000" stop-opacity="0"/>'
      '<stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>'
      '<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse">'
      '<rect width="4" height="1" fill="#fff" opacity=".035"/></pattern>'
      "</defs>")

    # Cabinet: dark screen inside a classic blue double-line maze wall.
    a('<rect x="1" y="1" width="898" height="266" rx="16" fill="#05070c"/>')
    a(f'<rect x="5" y="5" width="890" height="258" rx="13" fill="none" stroke="{WALL}" stroke-width="2.5" filter="url(#glow)"/>')
    a(f'<rect x="11" y="11" width="878" height="246" rx="9" fill="none" stroke="{WALL}" stroke-width="1.2" opacity=".85"/>')

    # Header.
    a(f'<text x="44" y="32" fill="#ff3b3b" font-size="12" letter-spacing="2">1UP'
      '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="0.9s" repeatCount="indefinite"/></text>')
    digits = max(4, len(str(total)))
    dh = 20
    a('<clipPath id="score-clip"><rect x="40" y="38" width="120" height="22"/></clipPath>')
    a('<g clip-path="url(#score-clip)">')
    times = [0.0] + [tm for tm, _ in events]
    scores, acc = [0], 0
    for _, n in events:
        acc += n
        scores.append(acc)
    for p in range(digits):
        x = 46 + p * 13
        place = 10 ** (digits - 1 - p)
        vals = [f"0,{-((s // place) % 10) * dh}" for s in scores]
        strip = "".join(f'<text x="{x}" y="{55 + k * dh}" fill="#fff" font-size="19" text-anchor="middle">{k}</text>' for k in range(10))
        a(f'<g>{strip}<animateTransform attributeName="transform" type="translate" calcMode="discrete" '
          f'values="{";".join(vals)}" keyTimes="{kt(times, T)}" dur="{f(T)}s" repeatCount="indefinite"/></g>')
    a("</g>")

    a(f'<text x="{W/2}" y="32" fill="#fff" font-size="12" letter-spacing="2" text-anchor="middle">HIGH SCORE</text>')
    a(f'<text x="{W/2}" y="55" fill="#fff" font-size="19" text-anchor="middle">{total}</text>')
    a(f'<text x="{W-44}" y="32" fill="{PAC}" font-size="12" letter-spacing="2" text-anchor="end">{login.upper()}</text>')
    a(f'<text x="{W-44}" y="53" fill="#9aa4b2" font-size="11" letter-spacing="1" text-anchor="end">'
      f'BEST DAY <tspan fill="#fff">{best}</tspan>  STREAK <tspan fill="#fff">{longest}D</tspan></text>')

    # Month labels.
    prev_month, last_label = None, -9
    for c, wk in enumerate(weeks):
        first = dt.date.fromisoformat(wk["contributionDays"][0]["date"])
        if first.month != prev_month:
            if c - last_label >= 3 and c < ncols - 1:
                a(f'<text x="{f(gx + c * PITCH)}" y="{GRID_Y - 7}" fill="#6e7681" font-size="10" letter-spacing="1">'
                  f'{first.strftime("%b").upper()}</text>')
                last_label = c
            prev_month = first.month

    # Calendar cells.
    a("<g>")
    for c, r, date, n, lv in days:
        x, y = gx + c * PITCH, GRID_Y + r * PITCH
        a(f'<rect x="{f(x)}" y="{f(y)}" width="{CELL}" height="{CELL}" rx="2.5" fill="{EMPTY}"/>')
    a("</g>")

    lit, pellets, flashes, pops = [], [], [], []
    for (c, r), tm in eat.items():
        date, n, lv = by_cell[(c, r)]
        x, y = gx + c * PITCH, GRID_Y + r * PITCH
        cx, cy = center(c, r)
        on = f'calcMode="discrete" values="0;1" keyTimes="0;{f(tm / T)}" dur="{f(T)}s" repeatCount="indefinite"'
        off = f'calcMode="discrete" values="1;0" keyTimes="0;{f(tm / T)}" dur="{f(T)}s" repeatCount="indefinite"'
        lit.append(f'<rect x="{f(x)}" y="{f(y)}" width="{CELL}" height="{CELL}" rx="2.5" fill="{GREENS[lv-1]}" opacity="0">'
                   f'<title>{date}: {n} contributions</title><animate attributeName="opacity" {on}/></rect>')
        flashes.append(f'<rect x="{f(x-1)}" y="{f(y-1)}" width="{CELL+2}" height="{CELL+2}" rx="3" fill="#fff" opacity="0">'
                       f'<animate attributeName="opacity" values="0;0;.9;0;0" keyTimes="{kt([0, tm, tm + .03, tm + .4, T], T)}" '
                       f'dur="{f(T)}s" repeatCount="indefinite"/></rect>')
        if lv == 4:
            dot = (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="4.2" fill="{PELLET}">'
                   '<animate attributeName="opacity" values="1;.2;1" dur=".6s" repeatCount="indefinite"/></circle>')
        else:
            dot = f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{[0, 1.6, 2.1, 2.7][lv]}" fill="{PELLET}"/>'
        pellets.append(f'<g>{dot}<animate attributeName="opacity" {off}/></g>')
        if lv >= 3:
            pops.append(f'<text x="{f(cx)}" y="{f(cy - 9)}" fill="#26e6ff" font-size="10" text-anchor="middle" opacity="0" stroke="#05070c" stroke-width="3" paint-order="stroke">+{n}'
                        f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt([0, tm, tm + .02, tm + .6, tm + 1.1, T], T)}" '
                        f'dur="{f(T)}s" repeatCount="indefinite"/>'
                        f'<animateTransform attributeName="transform" type="translate" values="0,0;0,0;0,-12;0,-12" '
                        f'keyTimes="{kt([0, tm, tm + 1.1, T], T)}" dur="{f(T)}s" repeatCount="indefinite"/></text>')
    a("<g>" + "".join(lit) + "</g>")
    a("<g>" + "".join(pellets) + "</g>")
    a("<g>" + "".join(flashes) + "</g>")

    # STAGE CLEAR sweep across the finished graph.
    a(f'<rect x="{f(gx - 80)}" y="{GRID_Y - 4}" width="80" height="{7 * PITCH + 5}" fill="url(#sweep)" opacity="0">'
      f'<animate attributeName="opacity" calcMode="discrete" values="0;1;0" keyTimes="{kt([0, clear_at, clear_at + 1.6], T)}" dur="{f(T)}s" repeatCount="indefinite"/>'
      f'<animateTransform attributeName="transform" type="translate" values="0,0;0,0;{f(grid_w + 80)},0;{f(grid_w + 80)},0" '
      f'keyTimes="{kt([0, clear_at, clear_at + 1.6, T], T)}" dur="{f(T)}s" repeatCount="indefinite"/></rect>')

    # Ghosts.
    def ghost_body(color):
        zig = "".join(f" l-{f(13/6)} {2 if k % 2 == 0 else -2}" for k in range(6))
        return f'<path d="M-6.5 6.5 V0 A6.5 6.5 0 0 1 6.5 0 V6.5{zig} Z" fill="{color}">'

    for gi, (color, lag) in enumerate(GHOSTS):
        g_times = [tm + lag for tm in arrive]
        start, end = g_times[0], g_times[-1]
        # Body color over time: normal, blue while frightened, flashing white at the end.
        cols, ts = [color], [0.0]
        for s, e in fright:
            if e <= start or s >= end:
                continue
            cols += ["#2121de", "#f5f5f5", "#2121de", "#f5f5f5", color]
            ts += [s, e - .6, e - .45, e - .3, e]
        fill_anim = (f'<animate attributeName="fill" calcMode="discrete" values="{";".join(cols)}" '
                     f'keyTimes="{kt(ts, T)}" dur="{f(T)}s" repeatCount="indefinite"/>')
        face_vals, scared_vals = ["1"], ["0"]
        for k in range(1, len(cols)):
            normal = cols[k] == color
            face_vals.append("1" if normal else "0")
            scared_vals.append("0" if normal else "1")
        face_kt = kt(ts, T)
        a(f'<g opacity="0"><animate attributeName="opacity" calcMode="discrete" values="0;1;0" '
          f'keyTimes="{kt([0, start, end], T)}" dur="{f(T)}s" repeatCount="indefinite"/>'
          f'<g filter="url(#glow)">'
          f'{ghost_body(color)}{fill_anim}</path>'
          f'<g><animate attributeName="opacity" calcMode="discrete" values="{";".join(face_vals)}" keyTimes="{face_kt}" dur="{f(T)}s" repeatCount="indefinite"/>'
          '<ellipse cx="-2.4" cy="-1" rx="2" ry="2.4" fill="#fff"/><ellipse cx="2.4" cy="-1" rx="2" ry="2.4" fill="#fff"/>'
          '<circle cx="-1.7" cy="-.6" r="1.1" fill="#1d3cff"/><circle cx="3.1" cy="-.6" r="1.1" fill="#1d3cff"/></g>'
          f'<g opacity="0"><animate attributeName="opacity" calcMode="discrete" values="{";".join(scared_vals)}" keyTimes="{face_kt}" dur="{f(T)}s" repeatCount="indefinite"/>'
          '<rect x="-3" y="-2" width="1.6" height="1.6" fill="#ffcfa0"/><rect x="1.4" y="-2" width="1.6" height="1.6" fill="#ffcfa0"/>'
          '<path d="M-4 3 l1.3-1 1.3 1 1.3-1 1.3 1 1.3-1 1.3 1" fill="none" stroke="#ffcfa0" stroke-width=".9"/></g>'
          "</g>"
          f'<animateMotion path="{path_d}" calcMode="linear" keyPoints="0;{";".join(f(k) for k in key_points)};1" '
          f'keyTimes="0;{kt(g_times, T)};1" dur="{f(T)}s" repeatCount="indefinite"/></g>')

    # Pac-Man.
    r = 6.8
    a(f'<g><animate attributeName="opacity" calcMode="discrete" values="1;0" keyTimes="0;{f(pac_end / T)}" dur="{f(T)}s" repeatCount="indefinite"/>'
      f'<g filter="url(#glow)">'
      f'<path d="M0 0 L{r} 0 A{r} {r} 0 0 0 -{r} 0 Z" fill="{PAC}">'
      '<animateTransform attributeName="transform" type="rotate" values="-42;0;-42" dur=".28s" repeatCount="indefinite"/></path>'
      f'<path d="M0 0 L{r} 0 A{r} {r} 0 0 1 -{r} 0 Z" fill="{PAC}">'
      '<animateTransform attributeName="transform" type="rotate" values="42;0;42" dur=".28s" repeatCount="indefinite"/></path>'
      "</g>"
      f'<animateMotion path="{path_d}" rotate="auto" calcMode="linear" keyPoints="0;{";".join(f(k) for k in key_points)};1" '
      f'keyTimes="0;{kt(arrive, T)};1" dur="{f(T)}s" repeatCount="indefinite"/></g>')

    a("<g>" + "".join(pops) + "</g>")

    # READY!
    a(f'<g><animate attributeName="opacity" calcMode="discrete" values="1;0" keyTimes="0;{f(INTRO / T)}" dur="{f(T)}s" repeatCount="indefinite"/>'
      f'<rect x="{W/2 - 70}" y="{GRID_Y + 40}" width="140" height="30" rx="6" fill="#05070c" opacity=".85"/>'
      f'<text x="{W/2}" y="{GRID_Y + 61}" fill="{PAC}" font-size="20" letter-spacing="3" text-anchor="middle">READY!</text></g>')

    # Footer: lives, progress bar, legend.
    fy = 228
    for k in range(3):
        lx = 48 + k * 20
        a(f'<path d="M{lx} {fy} L{lx + 6.5} {fy - 4} A7 7 0 1 0 {lx + 6.5} {fy + 4} Z" fill="{PAC}"/>')
    a(f'<text x="112" y="{fy + 4}" fill="#9aa4b2" font-size="11" letter-spacing="1">ACTIVE <tspan fill="#fff">{active}D</tspan></text>')

    bar_x, bar_w = W / 2 - 150, 300
    a(f'<rect x="{bar_x}" y="{fy - 6}" width="{bar_w}" height="12" rx="6" fill="none" stroke="{WALL}" stroke-width="1.5"/>')
    widths = [f(bar_w * s / total) for s in scores]
    a(f'<rect x="{bar_x}" y="{fy - 6}" width="0" height="12" rx="6" fill="{PAC}">'
      f'<animate attributeName="width" values="{";".join(widths)};{f(bar_w)};{f(bar_w)}" '
      f'keyTimes="{kt(times + [clear_at, T], T)}" dur="{f(T)}s" repeatCount="indefinite"/></rect>')
    a(f'<text x="{W/2}" y="{fy + 26}" fill="#6e7681" font-size="10" letter-spacing="2" text-anchor="middle">'
      f'{total:,} CONTRIBUTIONS IN THE LAST YEAR</text>')
    a(f'<g opacity="0"><animate attributeName="opacity" calcMode="discrete" values="0;1;0;1;0;1" '
      f'keyTimes="{kt([0, clear_at, clear_at + .4, clear_at + .8, clear_at + 1.2, clear_at + 1.6], T)}" dur="{f(T)}s" repeatCount="indefinite"/>'
      f'<rect x="{bar_x - 6}" y="{fy - 11}" width="{bar_w + 12}" height="22" rx="11" fill="#05070c"/>'
      f'<text x="{W/2}" y="{fy + 5}" fill="{PAC}" font-size="14" letter-spacing="3" text-anchor="middle">STAGE CLEAR!</text></g>')

    lx = W - 44 - 5 * 15 - 34
    a(f'<text x="{lx - 6}" y="{fy + 4}" fill="#6e7681" font-size="10" letter-spacing="1" text-anchor="end">LESS</text>')
    for k, colr in enumerate([EMPTY] + GREENS):
        a(f'<rect x="{lx + k * 15}" y="{fy - 6}" width="11" height="11" rx="2" fill="{colr}"/>')
    a(f'<text x="{lx + 5 * 15 + 2}" y="{fy + 4}" fill="#6e7681" font-size="10" letter-spacing="1">MORE</text>')

    # CRT finish.
    a('<rect x="12" y="12" width="876" height="244" rx="8" fill="url(#scan)" pointer-events="none"/>')
    a('<rect x="12" y="12" width="876" height="244" rx="8" fill="url(#vignette)" pointer-events="none"/>')
    a("</svg>")
    return "\n".join(out), T


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", required=True)
    ap.add_argument("--out", default="arcade/arcade.svg")
    ap.add_argument("--data", help="calendar JSON instead of the GitHub API")
    args = ap.parse_args()
    if args.data:
        with open(args.data) as fh:
            cal = json.load(fh)
    else:
        cal = fetch_calendar(args.login, os.environ["GITHUB_TOKEN"])
    svg, loop = build(cal, args.login)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as fh:
        fh.write(svg)
    print(f"wrote {args.out} ({len(svg) // 1024} KB, {loop:.1f}s loop, "
          f"{cal['totalContributions']} contributions)")


if __name__ == "__main__":
    main()
