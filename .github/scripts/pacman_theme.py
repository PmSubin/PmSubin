"""Re-skin the pac-man contribution graph so it matches the 8-bit profile panels."""
import re, sys

src, dst = sys.argv[1], sys.argv[2]
svg = open(src, encoding="utf-8").read()

m = re.search(r'<svg width="(\d+)" height="(\d+)"', svg)
w, h = int(m.group(1)), int(m.group(2))
pad = 18
W, H = w + pad * 2, h + pad * 2

colors = {
    "#0d1117": "#0d1226",  # background -> panel navy
    "#161b22": "#151c3a",  # empty day
    "#0e4429": "#3b2a66",  # contribution levels -> purple scale
    "#006d32": "#6b3fe0",
    "#26a641": "#9b6dff",
    "#39d353": "#c9b6ff",
    "#ffffff": "#5ec8ff",  # maze walls -> arcade blue
    "#8b949e": "#8b93b8",  # month labels
}
for a, b in colors.items():
    svg = re.sub(re.escape(a), b, svg, flags=re.I)

svg = svg.replace(' rx="5"', ' rx="2"')
svg = svg.replace("<text ", '<text font-family="ui-monospace,Menlo,Consolas,monospace" ')

svg = svg.replace(
    m.group(0),
    f'<svg width="{W}" height="{H}" viewBox="{-pad} {-pad} {W} {H}"',
    1,
)
frame = (
    f'<rect x="{-pad}" y="{-pad}" width="{W}" height="{H}" fill="#0b0f1f"/>'
    f'<rect x="{-pad + 4}" y="{-pad + 4}" width="{W - 8}" height="{H - 8}" fill="#0d1226" '
    f'stroke="#2b3566" stroke-width="4" shape-rendering="crispEdges"/>'
    f'<rect x="{-pad + 4}" y="{-pad + 4}" width="4" height="{H - 8}" fill="#9b6dff" shape-rendering="crispEdges"/>'
)
svg = re.sub(r'<rect width="100%" height="100%" fill="#0d1226"/>', frame, svg, count=1)
open(dst, "w", encoding="utf-8").write(svg)
print(f"themed {src} -> {dst} ({W}x{H})")
