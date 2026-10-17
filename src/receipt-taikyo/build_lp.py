"""Inline unDraw SVGs, calendar markup and the template form script into the LP sources."""
import re, sys, calendar
from pathlib import Path
ROOT = Path("/home/user/lp-site")
SRC = Path(__file__).parent / "src"

def undraw(m):
    name, cls = m.group(1), m.group(2)
    s = (ROOT / "assets/undraw" / f"{name}.svg").read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    s = re.sub(r"<title>.*?</title>", "", s, flags=re.S)
    s = re.sub(r'\s(id|data-name)="[^"]*"', "", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("<svg ", f'<svg class="undraw {cls}" aria-hidden="true" focusable="false" ', 1)
    return s

def cal_html():
    # 曜日の並びは2027年のもの（ページ上では年を表示しない・イメージ扱い）
    out = []
    names = ["日", "月", "火", "水", "木", "金", "土"]
    for mon in (1, 2, 3):
        first_wd, ndays = calendar.monthrange(2027, mon)  # Monday=0
        lead = (first_wd + 1) % 7  # Sunday start
        cells = ['<i class="c-h">%s</i>' % n for n in names]
        cells += ['<i class="c-e"></i>'] * lead
        for d in range(1, ndays + 1):
            cls = ["c-d"]
            if mon == 1 and 4 <= d <= 15:
                cls.append("is-open")
            if (mon == 2 and d >= 16) or (mon == 3 and d <= 15):
                cls.append("is-tax")
            idx = lead + d
            cells.append(f'<i class="{" ".join(cls)}" style="--i:{idx}">{d}</i>')
        out.append(f'<div class="cal-m rv" data-m="{mon}"><p class="cal-mt"><b>{mon}</b>月</p><div class="cal-g">{"".join(cells)}</div></div>')
    return "\n".join(out)

for slug in sys.argv[1:]:
    src = (SRC / f"{slug}.src.html").read_text(encoding="utf-8")
    tpl = (ROOT / "_template" / f"{slug}.html").read_text(encoding="utf-8")
    script = re.search(r"<script>\s*\(function \(\) \{\s*var FORM_ENDPOINT.*?</script>", tpl, flags=re.S).group(0)
    out = re.sub(r"<!--@undraw:([\w-]+):([\w -]*)-->", undraw, src)
    out = out.replace("<!--@cal-->", cal_html())
    out = out.replace("<!--@formscript-->", script)
    assert "<!--@" not in out, "unresolved placeholder"
    (ROOT / "lp" / f"{slug}.html").write_text(out, encoding="utf-8")
    print(slug, len(out))
