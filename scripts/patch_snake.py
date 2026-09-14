# -*- coding: utf-8 -*-
import re
import sys
import os
import base64
import urllib.request

# Twemoji 72x72 sleeping face (U+1F634)
EMOJI_URL = "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f634.png"

def fetch_emoji_b64():
    try:
        with urllib.request.urlopen(EMOJI_URL, timeout=30) as r:
            data = r.read()
        return base64.b64encode(data).decode("ascii")
    except Exception as e:
        print(f"warn: cannot fetch emoji: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("usage: patch_snake.py <svg>")
        sys.exit(0)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"skip: {path} not found")
        return

    emoji_b64 = fetch_emoji_b64()
    if not emoji_b64:
        print("skip: emoji not fetched")
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
                    pad = 1.0
                    img_w = max(6.0, ww - pad * 2)
                    img_h = max(6.0, hh - pad * 2)
                    return (
                        f'<image x="{float(x.group(1))+pad:.1f}" '
                        f'y="{float(y.group(1))+pad:.1f}" '
                        f'width="{img_w:.1f}" height="{img_h:.1f}" '
                        f'href="data:image/png;base64,{emoji_b64}" '
                        f'preserveAspectRatio="xMidYMid meet"/>'
                    )
        return full

    new_svg, count = pattern.subn(replace_rect, svg)
    print(f"{path}: replaced {count} rect(s)")

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_svg)

if __name__ == "__main__":
    main()
