"""Inline unDraw SVGs into page sources.

Usage: python3 inline.py <src.html> <out.html>
Marker syntax in source: <!--UNDRAW:name:class-name-->
"""
import re
import sys
from pathlib import Path

ASSETS = Path("/home/user/lp-site/assets/undraw")


def load(name, cls):
    s = (ASSETS / f"{name}.svg").read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    s = re.sub(r"<title>.*?</title>", "", s, flags=re.S)
    s = re.sub(r'\s(id|data-name)="[^"]*"', "", s)
    s = re.sub(r">\s+<", "><", s).strip()
    s = s.replace("<svg ", f'<svg class="{cls}" aria-hidden="true" focusable="false" data-undraw="{name}" ', 1)
    return s


def main():
    src, out = sys.argv[1], sys.argv[2]
    html = Path(src).read_text(encoding="utf-8")
    used = []

    def rep(m):
        used.append(m.group(1))
        return load(m.group(1), m.group(2))

    html = re.sub(r"<!--UNDRAW:([a-z0-9-]+):([a-z0-9 -]+)-->", rep, html)
    Path(out).write_text(html, encoding="utf-8")
    print("inlined:", ", ".join(used))


main()
