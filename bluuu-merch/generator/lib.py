"""Vector text + shape helpers for the Bluuu merch designs.
All coordinates are in millimetres (SVG user units = mm)."""
import math, os, functools
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fonts', 'ttf')
FONTS = {
    'petrov': 'petrov-sans-regular.ttf', 'petrov-sb': 'petrov-sans-semibold.ttf',
    'bebas': 'bebas-neue-400.ttf', 'anton': 'anton-400.ttf', 'archivo': 'archivo-black-400.ttf',
    'space-mono': 'space-mono-400.ttf', 'space-mono-b': 'space-mono-700.ttf',
    'grotesk': 'space-grotesk-500.ttf', 'grotesk-b': 'space-grotesk-700.ttf',
    'syne-b': 'syne-800.ttf', 'unbounded': 'unbounded-700.ttf', 'unbounded-x': 'unbounded-900.ttf',
    'instrument': 'instrument-serif-400.ttf', 'playfair-i': 'playfair-display-700.ttf', 'dmserif': 'dm-serif-display-400.ttf',
    'caveat': 'caveat-600.ttf', 'caveat-b': 'caveat-700.ttf', 'marker': 'permanent-marker-400.ttf', 'kalam': 'kalam-700.ttf',
    'pacifico': 'pacifico-400.ttf', 'righteous': 'righteous-400.ttf', 'shrikhand': 'shrikhand-400.ttf', 'dela': 'dela-gothic-one-400.ttf',
    'bricolage': 'bricolage-grotesque-800.ttf', 'cormorant': 'cormorant-garamond-600.ttf', 'manrope': 'manrope-800.ttf',
    'cjk': ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 0),
}

@functools.lru_cache(None)
def _load(key):
    spec = FONTS[key]; idx = 0
    if isinstance(spec, tuple):
        path, idx = spec
    else:
        path = os.path.join(FONTDIR, spec)
    tt = TTFont(path, fontNumber=idx) if path.endswith('.ttc') else TTFont(path)
    blob = hb.Blob.from_file_path(path)
    face = hb.Face(blob, idx)
    font = hb.Font(face)
    upem = tt['head'].unitsPerEm
    font.scale = (upem, upem)
    return tt, font, upem

def shape(text, key, size, tracking=0.0, features=None):
    """Return list of (glyphname, x, y, advance) in mm plus total width."""
    tt, font, upem = _load(key)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, features or {"kern": True, "liga": True})
    s = size / upem
    names = tt.getGlyphOrder()
    out = []; x = 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gname = names[info.codepoint]
        out.append((gname, x + pos.x_offset * s, pos.y_offset * s, pos.x_advance * s))
        x += pos.x_advance * s + tracking
    width = x - tracking if out else 0
    return out, width

def glyph_path(key, gname, transform):
    tt, font, upem = _load(key)
    gs = tt.getGlyphSet()
    pen = SVGPathPen(gs, ntos=lambda v: ('%.3f' % v).rstrip('0').rstrip('.'))
    tp = TransformPen(pen, transform)
    gs[gname].draw(tp)
    return pen.getCommands()

def text_path(text, key, size, x=0, y=0, anchor='start', tracking=0.0, italic=0.0, scale_x=1.0):
    """Outline text as a single SVG path string. y is the baseline. Units mm.
    italic = shear in degrees (fake italic). scale_x = horizontal stretch."""
    tt, font, upem = _load(key)
    s = size / upem
    glyphs, width = shape(text, key, size, tracking)
    width *= scale_x
    if anchor == 'middle': x0 = x - width / 2
    elif anchor == 'end': x0 = x - width
    else: x0 = x
    shear = math.tan(math.radians(italic))
    d = []
    for gname, gx, gy, adv in glyphs:
        # font units -> mm, flip y, shear, place
        tx = x0 + gx * scale_x; ty = y - gy
        # transform matrix (xx, xy, yx, yy, dx, dy) applied as x' = xx*x + yx*y + dx ; y' = xy*x + yy*y + dy
        d.append(glyph_path(key, gname, (s * scale_x, 0, -s * shear, -s, tx, ty)))
    return ' '.join(p for p in d if p), width

def text_width(text, key, size, tracking=0.0, scale_x=1.0):
    return shape(text, key, size, tracking)[1] * scale_x

def text_bbox_height(key, size, text='H'):
    tt, font, upem = _load(key)
    gs = tt.getGlyphSet(); names = tt.getGlyphOrder()
    cmap = tt.getBestCmap()
    bp = BoundsPen(gs); gs[cmap[ord(text[0])]].draw(bp)
    return (bp.bounds[3] - bp.bounds[1]) * size / upem

def arc_text(text, key, size, cx, cy, r, start_deg=None, tracking=0.0, upward=True, spread=None):
    """Text along an arc. upward=True: text reads along the top of a circle (letters' tops point away from center).
    Returns path d. Centered on angle 'centre' (-90 top / +90 bottom)."""
    tt, font, upem = _load(key)
    s = size / upem
    glyphs, width = shape(text, key, size, tracking)
    total_angle = math.degrees(width / r)
    if upward:
        a0 = -90 - total_angle / 2
    else:
        a0 = 90 + total_angle / 2
    d = []
    for gname, gx, gy, adv in glyphs:
        mid = gx + adv / 2
        ang = math.degrees(mid / r)
        if upward:
            a = a0 + ang
            px = cx + r * math.cos(math.radians(a)); py = cy + r * math.sin(math.radians(a))
            rot = math.radians(a + 90)
        else:
            a = a0 - ang
            px = cx + r * math.cos(math.radians(a)); py = cy + r * math.sin(math.radians(a))
            rot = math.radians(a - 90)
        c, sn = math.cos(rot), math.sin(rot)
        # glyph local: x from -adv/2 .. , y up. Compose: scale(s,-s) then rotate then translate.
        # local point (X,Y) font units -> (s*X - s*adv/2/s? ) careful: shift by half advance in mm
        half = adv / 2
        # matrix for local mm coords: X' = X - half ; then rotate
        xx = s * c; xy = s * sn; yx = s * sn; yy = -s * c  # includes y flip: (x, -y) rotated
        # rotation of vector (x, -y): x'' = x*c - (-y)*sn = x*c + y*sn ; y'' = x*sn + (-y)*c = x*sn - y*c
        yx = s * sn; yy = -s * c
        dx = px - half * c; dy = py - half * sn
        d.append(glyph_path(key, gname, (xx, xy, yx, yy, dx, dy)))
    return ' '.join(p for p in d if p)

def fmt(v):
    return ('%.3f' % v).rstrip('0').rstrip('.')

def svg_doc(w, h, body, bg=None, defs=''):
    bgrect = f'<rect width="{fmt(w)}" height="{fmt(h)}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{fmt(w)}mm" height="{fmt(h)}mm" viewBox="0 0 {fmt(w)} {fmt(h)}">\n'
            f'<defs>{defs}</defs>\n{bgrect}\n{body}\n</svg>\n')

# ---------- shapes ----------
def circle_halftone(cx, cy, rmax, cols, rows, w, h, density, fill, rmin=0.15, step=None):
    """Generate halftone dots over box (cx,cy,w,h) with dot radius from density(x,y) in 0..1."""
    out = []
    sx = w / cols; sy = h / rows
    for j in range(rows):
        for i in range(cols):
            x = cx - w / 2 + (i + 0.5) * sx + (sx / 2 if j % 2 else 0)
            y = cy - h / 2 + (j + 0.5) * sy
            dnorm = max(0.0, min(1.0, density(x, y)))
            r = rmin + (rmax - rmin) * dnorm
            if dnorm > 0.02:
                out.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="{fill}"/>')
    return '\n'.join(out)

def wave_path(x0, x1, y, amp, wavelength, phase=0.0, steps=None):
    """Smooth sine wave as cubic-approx polyline path (open)."""
    n = steps or max(40, int((x1 - x0) / wavelength * 24))
    pts = []
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        pts.append((x, y + amp * math.sin(2 * math.pi * (x - x0) / wavelength + phase)))
    return 'M ' + ' L '.join(f'{fmt(px)} {fmt(py)}' for px, py in pts)

def smooth_closed(points, tension=0.5):
    """Catmull-Rom closed spline -> cubic bezier path."""
    n = len(points)
    d = f'M {fmt(points[0][0])} {fmt(points[0][1])}'
    for i in range(n):
        p0 = points[(i - 1) % n]; p1 = points[i]; p2 = points[(i + 1) % n]; p3 = points[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        d += f' C {fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}'
    return d + ' Z'

def smooth_open(points, tension=0.5):
    n = len(points)
    d = f'M {fmt(points[0][0])} {fmt(points[0][1])}'
    for i in range(n - 1):
        p0 = points[max(i - 1, 0)]; p1 = points[i]; p2 = points[i + 1]; p3 = points[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        d += f' C {fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}'
    return d

def mirror_points(right_half):
    """right_half: points from top-center going clockwise down the right side to bottom-center.
    Returns full closed outline (right side then mirrored left side)."""
    left = [(-x, y) for x, y in reversed(right_half[1:-1])]
    return right_half + left

def manta_outline(scale=1.0, cx=0, cy=0):
    """Stylised manta ray, top view, head up. Returns closed smooth path (units mm, approx 100 wide at scale 1)."""
    # right half, starting at top centre (between cephalic fins), clockwise
    pts = [
        (0, -14),      # top centre between horns (mouth)
        (4, -17), (6.5, -24), (8.5, -26.5), (10, -24), (9.5, -17),  # right cephalic fin (horn)
        (14, -14), (22, -11), (32, -6), (41, 0), (48, 7), (52, 12),  # leading edge of right wing
        (50, 13.5), (40, 10), (30, 11), (22, 15), (16, 20), (12, 24), # trailing edge back to body
        (9, 27), (6, 30), (3.5, 36),   # body tapering to tail base
        (1.6, 40), (1.2, 55), (0.9, 70), (0.5, 84), (0, 86),  # tail
    ]
    pts = [(cx + x * scale, cy + y * scale) for x, y in mirror_points(pts)]
    return smooth_closed(pts, tension=0.55)

def yacht_silhouette(x, y, scale=1.0):
    """Simple modern motor yacht side profile, bow to the right. Origin = waterline centre."""
    hull = [(-30, 0), (-30, -6), (-26, -8), (-2, -8.5), (18, -8), (28, -6), (34, -2), (34, 0)]
    cabin = [(-22, -8), (-20, -15), (-14, -17), (4, -17), (12, -13), (16, -8)]
    top = [(-16, -17), (-14, -21), (-2, -22), (4, -20), (6, -17)]
    def poly(pts):
        return 'M ' + ' L '.join(f'{fmt(x + px * scale)} {fmt(y + py * scale)}' for px, py in pts) + ' Z'
    return poly(hull) + ' ' + poly(cabin) + ' ' + poly(top)

def kelingking_profile(x0, y0, w, h):
    """Stylised Kelingking 'T-rex' headland silhouette inside box (x0,y0,w,h). Returns closed path.
    Profile faces left (nose/mouth at left)."""
    # normalised points (0..1) of the land mass, top edge left->right then down the right side and bottom back
    pts = [
        (0.00, 1.00), (0.00, 0.78), (0.04, 0.70), (0.06, 0.60), (0.10, 0.56), (0.16, 0.57), (0.20, 0.50),  # lower jaw/mouth
        (0.14, 0.44), (0.10, 0.36), (0.12, 0.26), (0.18, 0.18), (0.26, 0.12), (0.36, 0.09), (0.46, 0.10),   # head/snout top
        (0.52, 0.16), (0.56, 0.26), (0.60, 0.34), (0.66, 0.38), (0.74, 0.36), (0.82, 0.30), (0.90, 0.24), (1.00, 0.20),  # ridge to mainland
        (1.00, 1.00),
    ]
    P = [(x0 + px * w, y0 + py * h) for px, py in pts]
    return smooth_open(P[:-1], tension=0.45) + f' L {fmt(P[-1][0])} {fmt(P[-1][1])} Z'

# ---------- geometry utils ----------
def spline_polyline(points, closed=True, samples=12, tension=0.5):
    """Sample the Catmull-Rom spline used by smooth_closed/smooth_open into a dense polyline."""
    n = len(points); out = []
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        if closed:
            p0 = points[(i - 1) % n]; p1 = points[i]; p2 = points[(i + 1) % n]; p3 = points[(i + 2) % n]
        else:
            p0 = points[max(i - 1, 0)]; p1 = points[i]; p2 = points[i + 1]; p3 = points[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        for k in range(samples):
            t = k / samples; mt = 1 - t
            x = mt**3 * p1[0] + 3 * mt**2 * t * c1[0] + 3 * mt * t**2 * c2[0] + t**3 * p2[0]
            y = mt**3 * p1[1] + 3 * mt**2 * t * c1[1] + 3 * mt * t**2 * c2[1] + t**3 * p2[1]
            out.append((x, y))
    return out

def point_in_poly(x, y, poly):
    inside = False; n = len(poly); j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-9) + xi):
            inside = not inside
        j = i
    return inside

def rot(deg, cx=0, cy=0):
    return f'rotate({fmt(deg)} {fmt(cx)} {fmt(cy)})'
