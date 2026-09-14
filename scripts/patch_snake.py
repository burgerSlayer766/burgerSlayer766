# -*- coding: utf-8 -*-
import re
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("usage: patch_snake.py <svg>")
        sys.exit(0)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"skip: {path} not found")
        return

    with open(path, "r", encoding="utf-8") as f:
        svg = f.read()

    EMPTY_COLORS = ["#ebedf0", "#161b22", "#0d1117", "#000000"]

    pattern = re.compile(r'<rect\b[^>]*?(?:/>|></rect>)', re.IGNORECASE)

    def replace_rect(match):
        full = match.group(0)
        for c in EMPTY_COLORS:
            if c.lower() in full.lower():
                x = re.search(r'x="([\d.]+)"', full)
                y = re.search(r'y="([\d.]+)"', full)
                w = re.search(r'width="([\d.]+)"', full)
                h = re.search(r'height="([\d.]+)"', full)
                if x and y:
                    ww = float(w.group(1)) if w else 10.0
                    hh = float(h.group(1)) if h else 10.0
                    cx = float(x.group(1)) + ww / 2
                    cy = float(y.group(1)) + hh * 0.8
                    size = max(8.0, hh * 1.1)
                    return (
                        f'<text x="{cx:.1f}" y="{cy:.1f}" '
                        f'font-size="{size:.1f}" text-anchor="middle" '
                        f'dominant-baseline="middle">😴</text>'
                    )
        return full

    new_svg, count = pattern.subn(replace_rect, svg)
    print(f"{path}: replaced {count} rect(s)")

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_svg)

if __name__ == "__main__":
    main()
