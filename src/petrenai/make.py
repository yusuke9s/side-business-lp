"""Builds lp/pet.html and lp/renai.html from *.src.html.

Placeholders:
  {{UNDRAW name extra-class}}  -> inline unDraw SVG (ids stripped, recolored ink)
  {{SKYLINE}} {{STARS}}        -> renai night city SVG pieces
  {{CAL_GRID}}                 -> pet calendar date grid (Jan 2027)
  {{SNOW}}                     -> nothing (snow is CSS/JS)
"""
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SITE = Path("/home/user/lp-site")
UD = SITE / "assets" / "undraw"

INK = {"pet": {"#3f3d56": "#1e3d34", "#2f2e41": "#1b2f29"},
       "renai": {"#3f3d56": "#2b2257", "#2f2e41": "#221a45", "#090814": "#120c2b"}}


def undraw(name, cls, page):
    s = (UD / f"{name}.svg").read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>", "", s).strip()
    s = re.sub(r'\s(id|data-name)="[^"]*"', "", s)
    s = re.sub(r"<svg\b([^>]*)>", lambda m: "<svg" + re.sub(r'\s(width|height)="[^"]*"', "", m.group(1))
               + f' class="ud {cls}" aria-hidden="true" focusable="false">', s, count=1)
    for a, b in INK[page].items():
        s = s.replace(f'"{a}"', f'"{b}"')
    return s


def skyline():
    rnd = random.Random(7)
    out = []
    # back layer
    x = 0
    back = []
    while x < 1440:
        w = rnd.randint(40, 90)
        h = rnd.randint(110, 220)
        back.append(f'<rect x="{x}" y="{320 - h}" width="{w}" height="{h}"/>')
        x += w + rnd.randint(-6, 4)
    out.append('<g fill="#2a1f5c" opacity=".85">' + "".join(back) + "</g>")
    # tower with antenna
    out.append('<g fill="#231a50"><rect x="1080" y="70" width="46" height="250"/><rect x="1098" y="30" width="10" height="44"/>'
               '<circle cx="1103" cy="28" r="4" fill="#ff6b6b" class="beacon"/></g>')
    # front layer with windows
    x = -10
    front = []
    wins = []
    while x < 1450:
        w = rnd.randint(56, 120)
        h = rnd.randint(60, 150)
        top = 320 - h
        front.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" rx="2"/>')
        if rnd.random() < .3:
            front.append(f'<rect x="{x + w * .2:.0f}" y="{top - 12}" width="{w * .6:.0f}" height="14"/>')
        for wy in range(top + 12, 312, 16):
            for wx in range(x + 8, x + w - 10, 14):
                r = rnd.random()
                if r < .34:
                    cls = ""
                    if rnd.random() < .22:
                        cls = f' class="tw tw{rnd.randint(1, 4)}"'
                    op = rnd.choice([".95", ".8", ".6"])
                    col = rnd.choice(["#ffd27a", "#ffd27a", "#ffe6b0", "#c7b8ff"])
                    wins.append(f'<rect x="{wx}" y="{wy}" width="6" height="8" fill="{col}" opacity="{op}"{cls}/>')
        x += w + rnd.randint(2, 10)
    out.append('<g fill="#150f33">' + "".join(front) + "</g>")
    out.append("<g>" + "".join(wins) + "</g>")
    return "".join(out)


def stars():
    rnd = random.Random(11)
    s = []
    for i in range(70):
        x = rnd.uniform(0, 1440)
        y = rnd.uniform(0, 520)
        r = rnd.choice([0.8, 1, 1.2, 1.6])
        cls = f' class="st st{rnd.randint(1, 3)}"' if rnd.random() < .5 else ""
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}"{cls}/>')
    return "".join(s)


def cal_grid():
    # Jan 1 2027 = Friday. Columns: 日月火水木金土
    out = []
    heads = "日月火水木金土"
    x0, y0, cw, ch = 42, 190, 26, 13
    for i, d in enumerate(heads):
        col = "#d64545" if i == 0 else ("#2a6fb0" if i == 6 else "#5b6b66")
        out.append(f'<text x="{x0 + i * cw}" y="{y0}" fill="{col}" font-size="8.5" font-weight="700" text-anchor="middle">{d}</text>')
    for day in range(1, 32):
        idx = day + 4  # offset: Friday index 5 for day1
        col_i, row = idx % 7, idx // 7
        red = col_i == 0 or day in (1, 11)
        fill = "#d64545" if red else ("#2a6fb0" if col_i == 6 else "#2b3a35")
        out.append(f'<text x="{x0 + col_i * cw}" y="{y0 + 13 + row * ch}" fill="{fill}" font-size="9" text-anchor="middle">{day}</text>')
    return "".join(out)


def build(slug):
    src = (HERE / f"{slug}.src.html").read_text(encoding="utf-8")
    src = re.sub(r"\{\{UNDRAW ([\w-]+) ?([\w -]*)\}\}", lambda m: undraw(m.group(1), m.group(2).strip(), slug), src)
    src = src.replace("{{SKYLINE}}", skyline()).replace("{{STARS}}", stars()).replace("{{CAL_GRID}}", cal_grid())
    left = re.findall(r"\{\{[^}]*\}\}", src)
    if left:
        sys.exit(f"unreplaced placeholders in {slug}: {left}")
    (SITE / "lp" / f"{slug}.html").write_text(src, encoding="utf-8")
    print(slug, len(src))


if __name__ == "__main__":
    for s in sys.argv[1:] or ["pet", "renai"]:
        build(s)
