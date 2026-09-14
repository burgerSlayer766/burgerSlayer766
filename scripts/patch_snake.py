# -*- coding: utf-8 -*-
import re
import sys
import os

def make_sleeping_face(x, y, w, h):
    """Рисует спящий смайлик векторными фигурами по центру клетки."""
    cx = x + w / 2.0
    cy = y + h / 2.0
    r = min(w, h) * 0.42

    # Голова (жёлтый круг)
    face = (
        f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" '
        f'fill="#FFD93B" stroke="#E0B000" stroke-width="0.35"/>'
    )

    # Закрытые глаза — две дуги (смотрят "вниз", как у спящего)
    eye_dy = -r * 0.15
    eye_dx = r * 0.38
    eye_w = r * 0.28
    eye_y = cy + eye_dy
    l_eye = (
        f'<path d="M {cx-eye_dx-eye_w:.2f} {eye_y:.2f} '
        f'Q {cx-eye_dx:.2f} {eye_y + eye_w*1.1:.2f} '
        f'{cx-eye_dx+eye_w:.2f} {eye_y:.2f}" '
        f'fill="none" stroke="#222" stroke-width="0.5" stroke-linecap="round"/>'
    )
    r_eye = (
        f'<path d="M {cx+eye_dx-eye_w:.2f} {eye_y:.2f} '
        f'Q {cx+eye_dx:.2f} {eye_y + eye_w*1.1:.2f} '
        f'{cx+eye_dx+eye_w:.2f} {eye_y:.2f}" '
        f'fill="none" stroke="#222" stroke-width="0.5" stroke-linecap="round"/>'
    )

    # Ротик — маленькая горизонтальная линия
    mouth_y = cy + r * 0.4
    mouth = (
        f'<line x1="{cx-r*0.13:.2f}" y1="{mouth_y:.2f}" '
        f'x2="{cx+r*0.13:.2f}" y2="{mouth_y:.2f}" '
        f'stroke="#222" stroke-width="0.4" stroke-linecap="round"/>'
    )

    # Рука/щёчка — маленький штрих рядом (намёк на сон)
    return f'<g>{face}{l_eye}{r_eye}{mouth}</g>'


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
                    xx = float(x.group(1))
                    yy = float(y.group(1))
                    ww = float(w.group(1)) if w else 10.0
                    hh = float(h.group(1)) if h else 10.0
                    return make_sleeping_face(xx, yy, ww, hh)
        return full

    new_svg, count = pattern.subn(replace_rect, svg)
    print(f"{path}: replaced {count} rect(s)")

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_svg)


if __name__ == "__main__":
    main()
