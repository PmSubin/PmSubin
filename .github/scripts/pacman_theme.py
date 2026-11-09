"""Re-skin the pac-man contribution graph so it matches the 8-bit profile panels.

usage: pacman_theme.py <src.svg> <dst.svg> [dark|light]
  dark  -> re-skins pacman-contribution-graph-dark.svg (GitHub dark theme)
  light -> re-skins pacman-contribution-graph.svg      (GitHub light theme)
"""
import re, sys

src, dst = sys.argv[1], sys.argv[2]
theme = sys.argv[3] if len(sys.argv) > 3 else "dark"
svg = open(src, encoding="utf-8").read()

m = re.search(r'<svg width="(\d+)" height="(\d+)"', svg)
w, h = int(m.group(1)), int(m.group(2))
pad = 18
W, H = w + pad * 2, h + pad * 2

THEMES = {
    "dark": {
        "colors": {
            "#0d1117": "#0d1226",  # background -> panel navy
            "#161b22": "#151c3a",  # empty day
            "#0e4429": "#3b2a66",  # contribution levels -> purple scale
            "#006d32": "#6b3fe0",
            "#26a641": "#9b6dff",
            "#39d353": "#c9b6ff",
            "#ffffff": "#5ec8ff",  # maze walls -> arcade blue
            "#8b949e": "#8b93b8",  # month labels
        },
        "panel": "#0d1226",
        "accent": "#9b6dff",
    },
    "light": {
        "colors": {
            "#ffffff": "#fffaf0",  # background -> warm card white
            "#ebedf0": "#ece7f8",  # empty day
            "#9be9a8": "#d4c6ff",  # contribution levels -> purple scale, darker = more
            "#40c463": "#ad93ff",
            "#30a14e": "#8257ff",
            "#216e39": "#5b2fd6",
            "#000000": "#1a9be0",  # maze walls -> arcade blue
            "#57606a": "#5f6789",  # month labels
        },
        "panel": "#fffaf0",
        "accent": "#8257ff",
    },
}
t = THEMES[theme]

# one pass, so a colour that is both a source and a target is not swapped twice
rx = re.compile("|".join(re.escape(k) for k in t["colors"]), re.I)
svg = rx.sub(lambda c: t["colors"][c.group(0).lower()], svg)

svg = svg.replace(' rx="5"', ' rx="2"')
svg = svg.replace("<text ", '<text font-family="ui-monospace,Menlo,Consolas,monospace" ')

svg = svg.replace(
    m.group(0),
    f'<svg width="{W}" height="{H}" viewBox="{-pad} {-pad} {W} {H}"',
    1,
)
# the margin around the frame stays transparent so the panel sits on either GitHub theme
frame = (
    f'<rect x="{-pad + 4}" y="{-pad + 4}" width="{W - 8}" height="{H - 8}" fill="{t["panel"]}" '
    f'stroke="#2b3566" stroke-width="4" shape-rendering="crispEdges"/>'
    f'<rect x="{-pad + 4}" y="{-pad + 4}" width="4" height="{H - 8}" fill="{t["accent"]}" shape-rendering="crispEdges"/>'
)
bg = f'<rect width="100%" height="100%" fill="{t["panel"]}"/>'
assert svg.count(bg) >= 1, "background rect not found"
svg = svg.replace(bg, frame, 1)
open(dst, "w", encoding="utf-8").write(svg)
print(f"themed {src} -> {dst} ({theme}, {W}x{H})")
