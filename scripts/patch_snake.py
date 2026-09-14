import re
import sys

path = sys.argv[1]

with open(path, "r", encoding="utf-8") as f:
    svg = f.read()

EMPTY_COLORS = ["#ebedf0", "#161b22", "#0d1117", "#000000"]

def replace_rect(match):
    full = match.group(0)
    for c in EMPTY_COLORS:
        if c.lower() in full.lower():
            x = re.search(r'x="([\d.]+)"', full)
            y = re.search(r'y="([\d.]+)"', full)
            if x and y:
                cx = float(x.group(1)) + 5
                cy = float(y.group(1)) + 7
                return f'<text x="{cx}" y="{cy}" font-size="10" text-anchor="middle">😴</text>'
    return full

svg = re.sub(r'<rect[^>]*/>', replace_rect, svg)

with open(path, "w", encoding="utf-8") as f:
    f.write(svg)
