#!/usr/bin/env python3
"""Render a GitHub profile as an animated koi pond SVG.

- One koi per top code language in public repos; koi length follows its share.
- The past year of contributions lies on the pond floor as pebbles.
- One lily pad per month, sized by that month's contributions; a lotus marks the best month.
- Ripples rise from the pond for each active day in the last week.
- How fast the koi swim follows the last week compared with the yearly average.

Usage:
  GITHUB_TOKEN=... python3 koi_pond.py --login USER --out pond/pond.svg
  python3 koi_pond.py --login USER --calendar cal.json --languages langs.json --out pond.svg
"""

import argparse
import datetime as dt
import json
import math
import os
import random
import urllib.request

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel weekday } }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false) {
      nodes { name languages(first: 20) { edges { size node { name } } } }
    }
  }
}
"""

LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2,
          "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
NOT_CODE = {"HTML", "CSS", "SCSS", "Sass", "Less", "Batchfile", "Dockerfile", "Nix",
            "Makefile", "Procfile", "PowerShell", "Shell", "Jupyter Notebook"}
NOTEBOOK_AS = {"Jupyter Notebook": "Python"}


def fetch(login, token):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "koi-pond"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    user = payload["data"]["user"]
    cal = user["contributionsCollection"]["contributionCalendar"]
    langs = {}
    for repo in user["repositories"]["nodes"]:
        if repo["name"].lower() == login.lower():
            continue
        langs[repo["name"]] = {e["node"]["name"]: e["size"] for e in repo["languages"]["edges"]}
    return cal, langs


# ---------------------------------------------------------------- look

W, H = 900, 320
POND = (14, 14, 600, 292)          # x, y, w, h
PANEL_X = 630
FONT = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
FLOOR = ["#0e4429", "#006d32", "#26a641", "#39d353"]

VARIETIES = [
    # name, base, belly/gradient, patches [(color, cx, cy, rx, ry)], fin
    ("Kohaku", "#f8f4ec", "#ffffff",
     [("#e2391f", 14, -2, 11, 7), ("#e2391f", -4, 2, 8, 6.5), ("#e2391f", 25, 0, 4.5, 4)], "#fbefe6"),
    ("Yamabuki", "#f2b12c", "#ffe08a", [], "#f7d27a"),
    ("Showa", "#f3eee4", "#ffffff",
     [("#d73a22", 12, 2, 9, 6), ("#1c1c1e", 0, -4, 9, 5), ("#1c1c1e", 22, 4, 4, 3.2),
      ("#d73a22", -12, 0, 6, 4.5)], "#e9e2d6"),
    ("Asagi", "#7e9cb2", "#a9c2d3",
     [("#e8742c", 20, 7, 8, 3.5), ("#e8742c", 20, -7, 8, 3.5)], "#e99a62"),
]


def f(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def smooth_closed(points):
    """Catmull-Rom through points as a closed cubic Bezier path."""
    n = len(points)
    d = f"M{f(points[0][0])} {f(points[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = points[i - 1], points[i], points[(i + 1) % n], points[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d + " Z"


def loop_points(cx, cy, ax, ay, kind, phase, n=40):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        if kind == "eight":
            pts.append((cx + ax * math.sin(t + phase), cy + ay * math.sin(2 * (t + phase))))
        else:
            wob = 1 + 0.12 * math.sin(3 * t)
            pts.append((cx + ax * wob * math.cos(t + phase), cy + ay * wob * math.sin(t + phase)))
    return pts


def path_length(points):
    return sum(math.dist(points[i], points[(i + 1) % len(points)]) for i in range(len(points)))


def koi_shape(uid, variety, scale, tail_period):
    """A koi facing +x, centred on the origin, drawn at length 60 then scaled."""
    name, base, belly, patches, fin = variety
    body = ("M30 0 C30 -7 23 -11 13 -11 C1 -11 -13 -7 -21 -3 C-24 -1.5 -24 1.5 -21 3 "
            "C-13 7 1 11 13 11 C23 11 30 7 30 0 Z")
    tail = "M-21 0 C-28 -4 -34 -11 -41 -12 C-37 -6 -36 -2 -35 0 C-36 2 -37 6 -41 12 C-34 11 -28 4 -21 0 Z"
    pec = "M0 0 C3 -1 7 2 8 7 C4 7 1 4 0 0 Z"
    s = []
    s.append(f'<g transform="scale({f(scale)})">')
    s.append(f'<g><animateTransform attributeName="transform" type="rotate" values="-4 16 0;4 16 0;-4 16 0" '
             f'dur="{f(tail_period)}s" repeatCount="indefinite"/>')
    s.append(f'<path d="{tail}" fill="{fin}" opacity=".85"><animateTransform attributeName="transform" type="rotate" '
             f'values="-16 -21 0;16 -21 0;-16 -21 0" dur="{f(tail_period)}s" begin="-{f(tail_period / 4)}s" repeatCount="indefinite"/></path>')
    for side in (1, -1):
        s.append(f'<g transform="translate(11 {8 * side}) scale(1 {side})"><path d="{pec}" fill="{fin}" opacity=".8">'
                 f'<animateTransform attributeName="transform" type="rotate" values="-10;14;-10" dur="{f(tail_period * 1.3)}s" repeatCount="indefinite"/></path></g>')
    s.append(f'<radialGradient id="{uid}g" cx=".6" cy=".5" r=".6"><stop offset="0" stop-color="{belly}"/>'
             f'<stop offset="1" stop-color="{base}"/></radialGradient>')
    s.append(f'<clipPath id="{uid}c"><path d="{body}"/></clipPath>')
    s.append(f'<path d="{body}" fill="url(#{uid}g)"/>')
    s.append(f'<g clip-path="url(#{uid}c)">')
    for color, cx, cy, rx, ry in patches:
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}"/>')
    s.append('<path d="M28 0 C18 -1 0 -1 -20 0" stroke="#fff" stroke-opacity=".28" stroke-width="2.4" fill="none"/>')
    s.append("</g>")
    s.append('<circle cx="24" cy="-5" r="1.3" fill="#111"/><circle cx="24" cy="5" r="1.3" fill="#111"/>')
    s.append("</g></g>")
    return "".join(s)


# ---------------------------------------------------------------- build

def build(cal, langs, login, today=None):
    rnd = random.Random(login)
    days = []
    for c, wk in enumerate(cal["weeks"]):
        for d in wk["contributionDays"]:
            days.append((c, d["weekday"], dt.date.fromisoformat(d["date"]), d["contributionCount"],
                         LEVELS[d["contributionLevel"]]))
    days.sort(key=lambda x: x[2])
    last_day = today or days[-1][2]
    total = cal["totalContributions"]

    # Languages (code only), by bytes across public repos.
    lang_bytes = {}
    for repo in langs.values():
        for name, size in repo.items():
            name = NOTEBOOK_AS.get(name, name)
            if name in NOT_CODE:
                continue
            lang_bytes[name] = lang_bytes.get(name, 0) + size
    lang_total = sum(lang_bytes.values()) or 1
    top = sorted(lang_bytes.items(), key=lambda kv: -kv[1])[:4]
    shares = [(n, b / lang_total) for n, b in top]

    # Months, weekdays, recent activity.
    months = {}
    for _, _, date, n, _ in days:
        key = (date.year, date.month)
        months[key] = months.get(key, 0) + n
    month_keys = sorted(months)[-12:]
    best_month = max(month_keys, key=lambda k: months[k])
    weekday = [0] * 7
    for _, r, _, n, _ in days:
        weekday[r] += n
    last7 = [d for d in days if (last_day - d[2]).days < 7]
    recent7 = sum(d[3] for d in last7)
    active7 = sum(1 for d in last7 if d[3] > 0)
    quiet = 0
    for d in reversed(days):
        if d[3] > 0:
            break
        quiet += 1
    avg7 = total / 52 if total else 0
    if quiet >= 14:
        mood, speed = "RESTING", 0.45
    elif avg7 and recent7 > 1.5 * avg7:
        mood, speed = "DARTING", 1.6
    else:
        mood, speed = "CRUISING", 1.0

    px, py, pw, ph = POND
    out = []
    a = out.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
    a(f"<title>{login} koi pond: {', '.join(n for n, _ in shares)} koi; {total:,} contributions in the last year</title>")
    a("<defs>"
      '<radialGradient id="water" cx=".45" cy=".4" r=".8"><stop offset="0" stop-color="#14606d"/>'
      '<stop offset=".55" stop-color="#0b3f4a"/><stop offset="1" stop-color="#05232b"/></radialGradient>'
      '<radialGradient id="caustic"><stop offset="0" stop-color="#bff6ff" stop-opacity=".16"/>'
      '<stop offset="1" stop-color="#bff6ff" stop-opacity="0"/></radialGradient>'
      '<radialGradient id="pad" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#5fb36a"/>'
      '<stop offset="1" stop-color="#23663a"/></radialGradient>'
      '<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>'
      '<filter id="padshadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.2"/></filter>'
      f'<clipPath id="pondclip"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="26"/></clipPath>'
      "</defs>")

    # Frame.
    a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="#0a0f12" stroke="#1d2a30"/>')
    a(f'<g clip-path="url(#pondclip)">')
    a(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="url(#water)"/>')

    # Pond floor: the year as pebbles.
    ncols = len(cal["weeks"])
    pitch, cell = 10, 8
    fx = px + (pw - (ncols * pitch - (pitch - cell))) / 2
    fy = py + ph - 7 * pitch - 14
    a('<g opacity=".62">')
    for c, r, date, n, lv in days:
        x, y = fx + c * pitch, fy + r * pitch
        fill = FLOOR[lv - 1] if lv else "#ffffff"
        op = "1" if lv else ".05"
        a(f'<rect x="{f(x)}" y="{f(y)}" width="{cell}" height="{cell}" rx="2.4" fill="{fill}" opacity="{op}">'
          f'<title>{date}: {n} contribution{"" if n == 1 else "s"}</title></rect>')
    a("</g>")

    # Caustic light drifting over the floor.
    for k in range(4):
        cx, cy = rnd.uniform(px + 80, px + pw - 80), rnd.uniform(py + 40, py + ph - 40)
        dx, dy = rnd.uniform(-60, 60), rnd.uniform(-30, 30)
        dur = rnd.uniform(14, 22)
        a(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rnd.uniform(70, 120))}" ry="{f(rnd.uniform(40, 70))}" fill="url(#caustic)">'
          f'<animateTransform attributeName="transform" type="translate" values="0 0;{f(dx)} {f(dy)};0 0" dur="{f(dur)}s" repeatCount="indefinite"/></ellipse>')

    # Koi: shadows first, then bodies.
    lanes = [  # cx, cy, ax, ay, kind
        (px + pw * .5, py + ph * .40, pw * .36, ph * .26, "eight"),
        (px + pw * .46, py + ph * .52, pw * .30, ph * .30, "loop"),
        (px + pw * .58, py + ph * .38, pw * .24, ph * .22, "loop"),
        (px + pw * .38, py + ph * .45, pw * .22, ph * .28, "eight"),
    ]
    fish = []
    for i, (lang, share) in enumerate(shares):
        cx, cy, ax, ay, kind = lanes[i]
        pts = loop_points(cx, cy, ax, ay, kind, phase=i * 1.3)
        if i % 2:
            pts = pts[::-1]
        length = 34 + 52 * math.sqrt(share)
        scale = length / 60
        px_per_s = 26 * speed * (1.15 - 0.25 * scale)
        dur = path_length(pts) / px_per_s
        tail = max(0.45, 1.25 / speed * (0.8 + 0.25 * scale))
        fish.append((i, lang, share, pts, scale, dur, tail))

    for i, lang, share, pts, scale, dur, tail in fish:
        shadow = [(x + 7, y + 11) for x, y in pts]
        begin = -dur * (i * 0.27)
        a(f'<g opacity=".32" filter="url(#soft)"><g transform="scale({f(scale)})">'
          '<path d="M30 0 C30 -8 20 -11 10 -11 C-6 -11 -20 -6 -40 0 C-20 6 -6 11 10 11 C20 11 30 8 30 0 Z" fill="#000"/></g>'
          f'<animateMotion path="{smooth_closed(shadow)}" rotate="auto" dur="{f(dur)}s" begin="{f(begin)}s" repeatCount="indefinite"/></g>')
    for i, lang, share, pts, scale, dur, tail in fish:
        begin = -dur * (i * 0.27)
        a(f'<g><title>{lang} koi: {share * 100:.0f}% of code in public repos</title>'
          f'{koi_shape(f"k{i}", VARIETIES[i], scale, tail)}'
          f'<animateMotion path="{smooth_closed(pts)}" rotate="auto" dur="{f(dur)}s" begin="{f(begin)}s" repeatCount="indefinite"/></g>')

    # Lily pads: one per month along the upper banks.
    spots = [(px + 46, py + 40), (px + 120, py + 28), (px + 205, py + 46), (px + 300, py + 26),
             (px + 390, py + 44), (px + 470, py + 26), (px + 556, py + 50), (px + 560, py + 128),
             (px + 30, py + 118), (px + 92, py + 182), (px + 520, py + 186), (px + 248, py + 120)]
    peak = max(months[k] for k in month_keys) or 1
    for idx, key in enumerate(month_keys):
        x, y = spots[idx % len(spots)]
        n = months[key]
        r = 9 + 17 * math.sqrt(n / peak) if n else 6
        notch = rnd.uniform(0, 360)
        label = dt.date(key[0], key[1], 1).strftime("%b %Y")
        bob = rnd.uniform(5, 8)
        a(f'<g transform="translate({f(x)} {f(y)})"><title>{label}: {n:,} contributions</title>'
          f'<g><animateTransform attributeName="transform" type="rotate" values="-4;4;-4" dur="{f(bob)}s" repeatCount="indefinite"/>'
          f'<circle cx="3" cy="4" r="{f(r)}" fill="#021317" opacity=".55" filter="url(#padshadow)"/>'
          f'<path d="M0 0 L{f(r * math.cos(math.radians(notch - 16)))} {f(r * math.sin(math.radians(notch - 16)))} '
          f'A{f(r)} {f(r)} 0 1 0 {f(r * math.cos(math.radians(notch + 16)))} {f(r * math.sin(math.radians(notch + 16)))} Z" '
          f'fill="{"url(#pad)" if n else "#1d4a33"}" opacity="{1 if n else .7}"/>'
          f'<path d="M0 0 L{f(r * .8 * math.cos(math.radians(notch + 180)))} {f(r * .8 * math.sin(math.radians(notch + 180)))}" '
          'stroke="#8fd19a" stroke-opacity=".35" stroke-width=".8"/>')
        if key == best_month:
            for p in range(8):
                ang = p * 45
                a(f'<ellipse cx="0" cy="{f(-r * .32)}" rx="{f(r * .16)}" ry="{f(r * .36)}" fill="#f7a8c4" '
                  f'stroke="#fff" stroke-opacity=".5" stroke-width=".6" transform="rotate({ang})"/>')
            for p in range(6):
                a(f'<ellipse cx="0" cy="{f(-r * .2)}" rx="{f(r * .12)}" ry="{f(r * .24)}" fill="#ffd1e1" transform="rotate({p * 60 + 30})"/>')
            a(f'<circle r="{f(r * .12)}" fill="#ffd66b"/>')
        a("</g></g>")

    # Ripples: one source per active day in the last week.
    for k in range(active7):
        x = rnd.uniform(px + 90, px + pw - 90)
        y = rnd.uniform(py + 70, py + ph - 110)
        period = rnd.uniform(3.2, 4.6)
        start = -rnd.uniform(0, period)
        for ring in range(2):
            b = start - ring * 0.7
            a(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="2" ry="1.3" fill="none" stroke="#d8fbff" stroke-width="1.2" opacity="0">'
              f'<animate attributeName="rx" values="2;34" dur="{f(period)}s" begin="{f(b)}s" repeatCount="indefinite"/>'
              f'<animate attributeName="ry" values="1.3;20" dur="{f(period)}s" begin="{f(b)}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values=".7;0" dur="{f(period)}s" begin="{f(b)}s" repeatCount="indefinite"/></ellipse>')

    a("</g>")
    a(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="26" fill="none" stroke="#2b3a3f" stroke-width="3"/>')
    a(f'<rect x="{px + 4}" y="{py + 4}" width="{pw - 8}" height="{ph - 8}" rx="22" fill="none" stroke="#9fe7f0" stroke-opacity=".08"/>')

    # ------------------------------------------------ panel
    x0 = PANEL_X
    a(f'<text x="{x0}" y="40" fill="#f0dfbd" font-size="15" font-weight="700" letter-spacing="3">KOI POND</text>')
    a(f'<text x="{x0}" y="57" fill="#7d8b91" font-size="11">@{login} · {mood.lower()}</text>')
    mood_color = {"RESTING": "#7d8b91", "CRUISING": "#5fd3e6", "DARTING": "#ffb35c"}[mood]
    a(f'<circle cx="{W - 26}" cy="36" r="4" fill="{mood_color}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle>')

    y = 84
    a(f'<text x="{x0}" y="{y}" fill="#5b6a70" font-size="9.5" font-family="{MONO}" letter-spacing="1.5">KOI = TOP LANGUAGES</text>')
    y += 10
    for i, (lang, share) in enumerate(shares):
        yy = y + i * 22
        a(f'<g transform="translate({x0 + 14} {yy + 9}) scale(.36)">{static_koi(f"m{i}", VARIETIES[i])}</g>')
        a(f'<text x="{x0 + 34}" y="{yy + 12}" fill="#e6edf3" font-size="12">{lang}</text>')
        a(f'<text x="{W - 26}" y="{yy + 12}" fill="#9aa7ad" font-size="11" font-family="{MONO}" text-anchor="end">{share * 100:.0f}%</text>')
        bw = W - 26 - (x0 + 34)
        a(f'<rect x="{x0 + 34}" y="{yy + 16}" width="{f(bw)}" height="3" rx="1.5" fill="#1b252a"/>')
        a(f'<rect x="{x0 + 34}" y="{yy + 16}" width="{f(bw * share)}" height="3" rx="1.5" fill="{VARIETIES[i][4] if i != 0 else "#e2391f"}"/>')

    y = 94 + len(shares) * 22 + 18
    a(f'<text x="{x0}" y="{y}" fill="#5b6a70" font-size="9.5" font-family="{MONO}" letter-spacing="1.5">WEEKLY RHYTHM</text>')
    top_w = max(weekday) or 1
    bw, gap, bh = 26, 7, 28
    for k, label in enumerate("SMTWTFS"):
        h = max(2, bh * weekday[k] / top_w)
        bx = x0 + k * (bw + gap)
        best = weekday[k] == top_w
        a(f'<rect x="{bx}" y="{y + 8 + bh - h:.1f}" width="{bw}" height="{h:.1f}" rx="3" fill="{"#39d353" if best else "#1f6f43"}">'
          f'<title>{["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][k]}: {weekday[k]:,} contributions</title></rect>')
        a(f'<text x="{bx + bw / 2}" y="{y + bh + 21}" fill="{"#e6edf3" if best else "#5b6a70"}" font-size="9.5" font-family="{MONO}" text-anchor="middle">{label}</text>')

    y = y + bh + 46
    stats = [(f"{total:,}", "this year"), (f"{recent7:,}", "last 7 days"),
             (dt.date(*best_month, 1).strftime("%b"), "best month")]
    cw = (W - 26 - x0) / 3
    for k, (val, lab) in enumerate(stats):
        cx = x0 + k * cw
        a(f'<text x="{f(cx)}" y="{y}" fill="#f0dfbd" font-size="17" font-weight="700">{val}</text>')
        a(f'<text x="{f(cx)}" y="{y + 15}" fill="#7d8b91" font-size="10">{lab}</text>')

    a(f'<text x="{x0}" y="{H - 12}" fill="#45545a" font-size="8.5" font-family="{MONO}">'
      "pad=month · lotus=best · floor=year</text>")
    a("</svg>")
    return "\n".join(out), mood


def static_koi(uid, variety):
    name, base, belly, patches, fin = variety
    body = ("M30 0 C30 -7 23 -11 13 -11 C1 -11 -13 -7 -21 -3 C-24 -1.5 -24 1.5 -21 3 "
            "C-13 7 1 11 13 11 C23 11 30 7 30 0 Z")
    tail = "M-21 0 C-28 -4 -34 -11 -41 -12 C-37 -6 -36 -2 -35 0 C-36 2 -37 6 -41 12 C-34 11 -28 4 -21 0 Z"
    s = [f'<path d="{tail}" fill="{fin}" opacity=".9"/>',
         f'<clipPath id="{uid}c"><path d="{body}"/></clipPath>',
         f'<path d="{body}" fill="{base}"/>', f'<g clip-path="url(#{uid}c)">']
    s += [f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c}"/>' for c, cx, cy, rx, ry in patches]
    s.append("</g>")
    return "".join(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", required=True)
    ap.add_argument("--out", default="pond/pond.svg")
    ap.add_argument("--calendar", help="calendar JSON instead of the GitHub API")
    ap.add_argument("--languages", help="languages JSON {repo: {lang: bytes}} instead of the API")
    args = ap.parse_args()
    if args.calendar:
        cal = json.load(open(args.calendar))
        langs = json.load(open(args.languages)) if args.languages else {}
    else:
        cal, langs = fetch(args.login, os.environ["GITHUB_TOKEN"])
    svg, mood = build(cal, langs, args.login)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as fh:
        fh.write(svg)
    print(f"wrote {args.out} ({len(svg) // 1024} KB, mood {mood})")


if __name__ == "__main__":
    main()
