"""Refined brand shapes (mm units). All return SVG path 'd' strings."""
import math
from lib import smooth_closed, smooth_open, mirror_points, fmt

def manta_pts(scale=1.0, cx=0, cy=0):
    """Right half of a manta ray (top view, head up). Returns full mirrored point list."""
    right = [
        (0, -16),                                   # mouth centre
        (3.2, -17.5), (4.6, -21), (5.2, -25.5), (6.6, -26.5), (7.6, -23.5), (7.4, -18.5), (8.6, -15.5),   # right cephalic lobe (short, forward)
        (14, -14.5), (24, -12.5), (36, -9), (47, -4.5), (56, 0.5), (62, 5.5), (64, 8.5),  # leading edge to wing tip
        (61, 8.8), (50, 6.5), (38, 7.5), (27, 11.5), (19, 17), (13, 23.5),  # trailing edge (concave) back towards body
        (9.5, 28.5), (6, 32.5), (3.2, 36.5),       # pelvic area / tail base
        (1.4, 40), (1.0, 52), (0.7, 66), (0.35, 80), (0, 84),   # tail
    ]
    pts = mirror_points(right)
    return [(cx + x * scale, cy + y * scale) for x, y in pts]

def manta_fill(scale=1.0, cx=0, cy=0):
    return smooth_closed(manta_pts(scale, cx, cy), tension=0.5)

def manta_line(scale=1.0, cx=0, cy=0):
    """Single continuous open line: starts at left wing tip, loops over the head, right wing, body, tail flick.
    Returns 'd' for stroking."""
    s = scale
    P = lambda x, y: (cx + x * s, cy + y * s)
    pts = [
        P(-66, 9), P(-58, 2), P(-46, -4.5), P(-34, -9.5), P(-22, -13), P(-12, -14.8),
        P(-8.4, -16), P(-7.2, -20), P(-6.4, -25.5), P(-5, -26.5), P(-4.2, -23), P(-3.6, -18), P(-1.5, -16.5),
        P(1.5, -16.5), P(3.6, -18), P(4.2, -23), P(5, -26.5), P(6.4, -25.5), P(7.2, -20), P(8.4, -16),
        P(12, -14.8), P(22, -13), P(34, -9.5), P(46, -4.5), P(58, 2), P(66, 9),
        P(60, 8.5), P(48, 6.5), P(36, 8), P(26, 12), P(18, 17.5), P(12, 24), P(8, 30), P(4.5, 35.5),
        P(2, 40), P(1.3, 52), P(0.9, 66), P(0.4, 80), P(-0.3, 86), P(-2.5, 89), P(-5.5, 88),
    ]
    main = smooth_open(pts, tension=0.5)
    # left wing trailing edge drawn as a second stroke that meets the body (keeps it 'one line' visually)
    pts2 = [P(-66, 9), P(-60, 8.5), P(-48, 6.5), P(-36, 8), P(-26, 12), P(-18, 17.5), P(-12, 24), P(-8, 30), P(-4.5, 35.5), P(-2.2, 40), P(-1.4, 50)]
    return main, smooth_open(pts2, tension=0.5)

def yacht(x, y, scale=1.0, bow='right'):
    """Sleek motor-yacht side profile (bow right). Origin at waterline under the stern. Returns closed path."""
    pts = [
        (0, 0), (1, -6), (4, -8.5),                                   # transom
        (12, -9), (13, -13), (17, -17.5), (26, -20.5), (40, -21.5), (52, -21), (58, -19.5), (63, -16.5), (66, -13.5),  # superstructure / hardtop
        (69, -12), (74, -10), (90, -8.5), (104, -6.5), (112, -4), (116, 0),   # foredeck to bow
    ]
    if bow == 'left':
        pts = [(-px, py) for px, py in pts]
    d = 'M ' + ' L '.join(f'{fmt(x + px * scale)} {fmt(y + py * scale)}' for px, py in pts) + ' Z'
    return d

def yacht_outline_pts(x, y, scale=1.0):
    return [(x + px * scale, y + py * scale) for px, py in [(0,0),(0,-7),(3,-9.5),(8,-10.5),(10,-10.5),(11,-14),(14,-18.5),(22,-21.5),(34,-22.5),(44,-22),(50,-20.5),(55,-17.5),(58,-14.5),(60,-13.5),(62,-11.5),(66,-10.5),(80,-9.5),(96,-8),(108,-5.5),(114,-3),(116,0)]]

def kelingking_aerial(x0, y0, w, h):
    """Kelingking headland in plan view: the famous 'T-rex head' - head at the LEFT-TOP, open mouth facing left,
    neck running down to the right (mainland). Returns closed smooth path inside box."""
    n = [
        # start at mainland bottom-right, go up the outer (western) edge of the neck to the head
        (1.00, 1.00), (0.90, 0.82), (0.78, 0.66), (0.66, 0.52), (0.56, 0.40), (0.50, 0.30),   # outer neck edge (left side of neck, going up)
        (0.44, 0.20), (0.36, 0.11), (0.26, 0.05), (0.16, 0.05), (0.08, 0.10), (0.03, 0.19), (0.02, 0.29),  # top of skull
        (0.06, 0.36), (0.12, 0.40),                                                     # upper jaw tip (snout)
        (0.09, 0.45), (0.05, 0.52), (0.08, 0.58), (0.16, 0.60), (0.24, 0.57),           # open mouth and lower jaw
        (0.30, 0.52), (0.34, 0.50), (0.42, 0.54), (0.50, 0.60), (0.58, 0.68), (0.66, 0.78), (0.74, 0.88), (0.80, 1.00),  # inner (beach) side of the neck back to mainland
    ]
    P = [(x0 + px * w, y0 + py * h) for px, py in n]
    return smooth_closed(P, tension=0.5)

def sun_rays(cx, cy, r_in, r_out, n=12, width=1.2):
    out = []
    for i in range(n):
        a = math.radians(i * 360 / n)
        x1, y1 = cx + r_in * math.cos(a), cy + r_in * math.sin(a)
        x2, y2 = cx + r_out * math.cos(a), cy + r_out * math.sin(a)
        out.append(f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}"/>')
    return '\n'.join(out)

def sparkle(cx, cy, r, ratio=0.28):
    """4-point sparkle star path."""
    pts = []
    for i in range(8):
        a = math.radians(i * 45 - 90)
        rr = r if i % 2 == 0 else r * ratio
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = 'M ' + ' '.join(f'{fmt(px)} {fmt(py)}' for px, py in pts) + ' Z'
    # soften with quadratic curves between points
    d = f'M {fmt(pts[0][0])} {fmt(pts[0][1])}'
    for i in range(8):
        p1 = pts[(i + 1) % 8]; p2 = pts[(i + 2) % 8]
        if i % 2 == 0:
            d += f' Q {fmt(p1[0])} {fmt(p1[1])} {fmt(p2[0])} {fmt(p2[1])}'
    return d + ' Z'

def star5(cx, cy, r, inner=0.42, rot=-90):
    pts = []
    for i in range(10):
        a = math.radians(rot + i * 36)
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return 'M ' + ' L '.join(f'{fmt(px)} {fmt(py)}' for px, py in pts) + ' Z'

def bodysuit_flat(x, y, scale=1.0, back=False):
    """Flat sketch of the tank bodysuit, centred at x, top of straps at y. Height ~ 620 units*scale. Returns (outline_d, details list)."""
    S = lambda px, py: (x + px * scale, y + py * scale)
    neck_drop = 70 if not back else 120
    right = [
        (62, 0), (70, 0), (74, 14), (88, 40), (112, 70), (128, 110), (132, 160), (128, 230), (118, 300), (112, 360), (116, 420), (128, 470), (136, 520), (134, 560), (112, 560), (70, 600), (28, 620), (0, 622),
    ]
    # outer outline (right side) then mirrored
    outline_pts = right + [(-px, py) for px, py in reversed(right[:-1])]
    # neckline between straps: inner edge of straps
    # Build full path: start at left strap outer top, go around outer edge clockwise to right strap outer top, then across inner neck
    outer = [S(px, py) for px, py in outline_pts]
    d = smooth_open(outer, tension=0.35)
    # neck inner curve from right strap inner top (62,0)... we started at (62,0) which is strap inner edge; outline list starts at right strap inner top -> goes right/down... Let me close with neckline curve
    if back:
        neck = [S(62, 0), S(58, 30), S(48, 70), S(34, 100), S(18, 116), S(0, 120), S(-18, 116), S(-34, 100), S(-48, 70), S(-58, 30), S(-62, 0)]
    else:
        neck = [S(62, 0), S(56, 24), S(40, 52), S(18, 66), S(0, neck_drop), S(-18, 66), S(-40, 52), S(-56, 24), S(-62, 0)]
    d += ' ' + smooth_open(neck, tension=0.5)[1:].replace('M', 'L', 1) if False else ''
    # simpler: build a single closed path from explicit sequence
    seq = [S(62, 0)] + [S(px, py) for px, py in right[1:]] + [S(-px, py) for px, py in reversed(right[1:-1])] + [S(-62, 0)]
    body = smooth_open(seq, tension=0.35)
    neck_d = smooth_open(list(reversed(neck)), tension=0.5)  # from (-62,0) to (62,0)
    full = body + ' ' + neck_d.replace('M', 'L', 1) + ' Z'
    # armhole inner curves (strap inner edge to side)
    arm_r = smooth_open([S(70, 0), S(78, 30), S(96, 62), S(118, 88), S(128, 110)], tension=0.5)
    arm_l = smooth_open([S(-70, 0), S(-78, 30), S(-96, 62), S(-118, 88), S(-128, 110)], tension=0.5)
    leg = smooth_open([S(-134, 560), S(-100, 572), S(-60, 596), S(-20, 616), S(0, 620), S(20, 616), S(60, 596), S(100, 572), S(134, 560)], tension=0.5)
    return full, [arm_r, arm_l]
