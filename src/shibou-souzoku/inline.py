"""Replace <!--@undraw NAME CLASS--> markers with the inline SVG (root id stripped),
and <!--@genko COLS ROWS|TITLE|TEXT--> with manuscript-grid cells."""
import re, sys, pathlib
SRC, OUT = sys.argv[1], sys.argv[2]
html = pathlib.Path(SRC).read_text(encoding="utf-8")
AS = pathlib.Path("/home/user/lp-site/assets/undraw")
used = []
def rep(m):
    name, cls = m.group(1), (m.group(2) or "").strip()
    svg = (AS / f"{name}.svg").read_text(encoding="utf-8").strip()
    svg = re.sub(r'^<\?xml[^>]*>\s*', '', svg)
    def root(mm):
        tag = mm.group(0)
        tag = re.sub(r'\s(id|data-name)="[^"]*"', '', tag)
        return tag[:-1] + f' class="ud {cls}" aria-hidden="true" focusable="false" data-src="assets/undraw/{name}.svg">'
    svg = re.sub(r'<svg\b[^>]*>', root, svg, count=1)
    used.append(name)
    return svg
html = re.sub(r'<!--@undraw\s+([\w-]+)\s*([^>]*?)-->', rep, html)

# ---- genko (manuscript grid) generator: <!--@genko COLS ROWS|col1|text-->
PUNCT = set("、。，．」』）")
def genko(m):
    cols, rows = int(m.group(1)), int(m.group(2))
    title, text = m.group(3), m.group(4)
    cells = []
    # title column: two blank cells then title, pad to rows
    tcol = ["", ""] + [(ch, "t") for ch in title]
    tcol = [c if c else ("", "") for c in tcol]
    tcol += [("", "")] * (rows - len(tcol))
    cells += tcol
    # body: parse {c}..{/} and {u}..{/}
    body = []
    cls = ""
    i = 0
    while i < len(text):
        if text.startswith("{c}", i): cls = "c"; i += 3; continue
        if text.startswith("{u}", i): cls = "u"; i += 3; continue
        if text.startswith("{/}", i): cls = ""; i += 3; continue
        body.append((text[i], cls)); i += 1
    col = []
    out = []
    for ch, c in body:
        if ch in PUNCT and len(col) == 0 and out:
            # burasage: hang punctuation in the last cell of previous column
            pch, pc = out[-1][-1]
            out[-1][-1] = (pch + ch, pc)
            continue
        col.append((ch, c))
        if len(col) == rows:
            out.append(col); col = []
    if col: out.append(col)
    for c in out:
        cells += c + [("", "")] * (rows - len(c))
    while len(cells) < cols * rows:
        cells.append(("", ""))
    html = []
    for ch, c in cells[: cols * rows]:
        ch_html = ch if len(ch) < 2 else f'{ch[0]}<s>{ch[1]}</s>'
        cl = f' class="{c}"' if c else ""
        html.append(f"<i{cl}>{ch_html}</i>" if ch else "<i></i>")
    return "".join(html)
html = re.sub(r'<!--@genko\s+(\d+)\s+(\d+)\|([^|]*)\|(.*?)-->', genko, html)
pathlib.Path(OUT).write_text(html, encoding="utf-8")
print("inlined:", used)
