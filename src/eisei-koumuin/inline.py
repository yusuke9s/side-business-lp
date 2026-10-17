import re, sys, pathlib
src, out = sys.argv[1], sys.argv[2]
html = pathlib.Path(src).read_text(encoding="utf-8")
def rep(m):
    name, cls = m.group(1), m.group(2) or ""
    svg = pathlib.Path(f"/home/user/lp-site/assets/undraw/{name}.svg").read_text(encoding="utf-8").strip()
    svg = re.sub(r'<\?xml[^>]*>', '', svg)
    svg = svg.replace("<svg ", f'<svg class="ud {cls}" aria-hidden="true" focusable="false" data-src="assets/undraw/{name}.svg" ', 1)
    return svg
html = re.sub(r'<!--UNDRAW:([\w-]+):?([\w -]*)-->', rep, html)
pathlib.Path(out).write_text(html, encoding="utf-8")
print(out, len(html))
