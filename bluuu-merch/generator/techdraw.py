"""Technical drawings for the tech pack: flat sketch with print placement + dimension callouts (mm)."""
import re, json, os
from lib import *
from shapes import bodysuit_flat
from designs import NAVY, AZURE, DEEP, L2
from labels import logo_group

DIM = '#E11D48'   # dimension line colour (red, standard for tech packs)
GARMENT_XSCALE = 1.22   # widen the sketch so chest flat width ~ 320 mm (size S/M relaxed)

def inner_svg(svg_text):
    """Strip outer <svg> wrapper -> (defs, body, w, h)."""
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text)
    w, h = float(m.group(1)), float(m.group(2))
    defs = re.search(r'<defs>(.*?)</defs>', svg_text, re.S).group(1)
    body = svg_text.split('</defs>', 1)[1].rsplit('</svg>', 1)[0]
    return defs, body, w, h

def dim_h(x1, x2, y, label, above=True):
    """Horizontal dimension line with arrows and label."""
    o = -3 if above else 5.5
    return (f'<g stroke="{DIM}" stroke-width="0.35" fill="none">'
            f'<line x1="{fmt(x1)}" y1="{fmt(y)}" x2="{fmt(x2)}" y2="{fmt(y)}"/>'
            f'<line x1="{fmt(x1)}" y1="{fmt(y-2)}" x2="{fmt(x1)}" y2="{fmt(y+2)}"/><line x1="{fmt(x2)}" y1="{fmt(y-2)}" x2="{fmt(x2)}" y2="{fmt(y+2)}"/></g>'
            + T_(label, (x1 + x2) / 2, y + o, 'middle'))

def dim_v(x, y1, y2, label, left=True):
    o = -2 if left else 2
    anchor = 'end' if left else 'start'
    return (f'<g stroke="{DIM}" stroke-width="0.35" fill="none">'
            f'<line x1="{fmt(x)}" y1="{fmt(y1)}" x2="{fmt(x)}" y2="{fmt(y2)}"/>'
            f'<line x1="{fmt(x-2)}" y1="{fmt(y1)}" x2="{fmt(x+2)}" y2="{fmt(y1)}"/><line x1="{fmt(x-2)}" y1="{fmt(y2)}" x2="{fmt(x+2)}" y2="{fmt(y2)}"/></g>'
            + T_(label, x + o, (y1 + y2) / 2 + 1.5, anchor))

def T_(text, x, y, anchor='start', size=4.2, fill=DIM, key='space-mono-b'):
    d, w = text_path(text, key, size, x, y, anchor)
    return f'<path d="{d}" fill="{fill}"/>'

def Tn(text, x, y, anchor='start', size=4.2, fill=NAVY, key='petrov'):
    d, w = text_path(text, key, size, x, y, anchor)
    return f'<path d="{d}" fill="{fill}"/>'

def garment(cx, top, back=False):
    full, arms = bodysuit_flat(0, 0, 1.0, back=back)
    g = f'<g transform="translate({fmt(cx)} {fmt(top)}) scale({GARMENT_XSCALE} 1)">'
    g += f'<path d="{full}" fill="#ffffff" stroke="{NAVY}" stroke-width="0.6" vector-effect="non-scaling-stroke"/>'
    for a in arms:
        g += f'<path d="{a}" fill="none" stroke="{NAVY}" stroke-width="0.45" vector-effect="non-scaling-stroke"/>'
    # waist/hip stitch hints
    g += f'<path d="M -112 560 Q 0 600 112 560" fill="none" stroke="{NAVY}" stroke-width="0.3" stroke-dasharray="2 1.5"/>'
    g += '</g>'
    return g

def placement_page_svg(meta, artwork_svg, extras=True):
    """A4-landscape-ish drawing (297 x 200 mm): front flat with artwork placed, dims, plus back flat with neck hits."""
    W, H = 297, 200
    defs, body, aw, ah = inner_svg(artwork_svg)
    s = 0.25  # sketch scale: 1 mm garment = 0.25 mm page
    fx, fy = 75, 12   # front sketch origin (top of straps)
    bx = 203
    out = [f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    # FRONT
    out.append(f'<g transform="translate(0 0) scale({s})">{garment(fx / s, fy / s)}</g>')
    out.append(f'<g transform="scale({s})">{garment(bx / s, fy / s, back=True)}</g>')
    # artwork placed on the front: top edge = CF neck (y=70 in sketch) + meta.top
    top_mm = meta['top']; w_mm = meta['w']; h_mm = meta['h']
    ax = fx - (w_mm / 2) * s; ay = fy + (70 + top_mm) * s
    out.append(f'<rect x="{fmt(ax)}" y="{fmt(ay)}" width="{fmt(w_mm*s)}" height="{fmt(h_mm*s)}" fill="none" stroke="{DIM}" stroke-width="0.3" stroke-dasharray="1.2 0.8"/>')
    out.append(f'<svg x="{fmt(ax)}" y="{fmt(ay)}" width="{fmt(w_mm*s)}" height="{fmt(h_mm*s)}" viewBox="0 0 {fmt(aw)} {fmt(ah)}"><defs>{defs}</defs>{body}</svg>')
    # CF neck marker
    nx, ny = fx, fy + 70 * s
    out.append(f'<circle cx="{fmt(nx)}" cy="{fmt(ny)}" r="0.9" fill="{DIM}"/>')
    out.append(T_('CF NECK', nx + 2.5, ny - 1.5, 'start', 3.2)); out.append(T_('前中领点', nx + 19, ny - 1.5, 'start', 3.2, key='cjk'))
    # dims
    out.append(dim_v(fx + (w_mm / 2) * s + 14, ny, ay, f'{top_mm} mm', left=False))
    out.append(dim_v(fx - (w_mm / 2) * s - 10, ay, ay + h_mm * s, f'{h_mm:g} mm', left=True))
    out.append(dim_h(ax, ax + w_mm * s, ay + h_mm * s + 8, f'{w_mm:g} mm', above=False))
    out.append(f'<line x1="{fmt(fx)}" y1="{fmt(fy-4)}" x2="{fmt(fx)}" y2="{fmt(fy + 640*s)}" stroke="{DIM}" stroke-width="0.25" stroke-dasharray="3 1.5"/>')
    out.append(T_('CENTRE FRONT', fx - 2, fy + 640 * s + 5, 'end', 3.2)); out.append(T_('前中线', fx + 2, fy + 640 * s + 5, 'start', 3.2, key='cjk'))
    out.append(Tn('FRONT', fx - 2, H - 6, 'end', 5, key='petrov-sb')); out.append(Tn('正面', fx + 3, H - 6, 'start', 5, key='cjk'))
    out.append(Tn('BACK', bx - 2, H - 6, 'end', 5, key='petrov-sb')); out.append(Tn('背面', bx + 3, H - 6, 'start', 5, key='cjk'))
    # BACK neck hits
    bny = fy + 120 * s
    out.append(f'<circle cx="{fmt(bx)}" cy="{fmt(bny)}" r="0.9" fill="{DIM}"/>')
    # outside back-neck logo 40 x 8.6 mm, 25 mm below CB neck
    lw, lh = 40, 8.6
    lx, ly = bx - lw / 2 * s, bny + 25 * s
    out.append(logo_group(lx, ly, lw * s))
    out.append(dim_v(bx + 22, bny, ly, '25 mm', left=False))
    out.append(f'<line x1="{fmt(lx + lw*s)}" y1="{fmt(ly + lh*s/2)}" x2="{fmt(bx + 40)}" y2="{fmt(ly - 4)}" stroke="{DIM}" stroke-width="0.25"/>')
    out.append(T_('A  BACK NECK LOGO 40×8.6 mm', bx + 41, ly - 5, 'start', 2.5))
    out.append(T_('1C AZURE · 后领标志 · 领口下 25 mm', bx + 41, ly - 1.2, 'start', 2.5, key='cjk'))
    # inside printed label 50 x 30 mm, 15 mm below CB neck (shown dashed)
    ix, iy = bx - 25 * s, bny + 15 * s
    out.append(f'<rect x="{fmt(ix)}" y="{fmt(iy)}" width="{fmt(50*s)}" height="{fmt(30*s)}" fill="none" stroke="{DEEP}" stroke-width="0.3" stroke-dasharray="1 0.8"/>')
    out.append(f'<line x1="{fmt(ix + 50*s)}" y1="{fmt(iy + 30*s)}" x2="{fmt(bx + 40)}" y2="{fmt(iy + 30*s + 10)}" stroke="{DEEP}" stroke-width="0.25"/>')
    out.append(T_('B  INSIDE LABEL 50×30 mm (inside)', bx + 41, iy + 30 * s + 11, 'start', 2.5, fill=DEEP))
    out.append(T_('内领印标（内侧）· 领口下 15 mm', bx + 41, iy + 30 * s + 14.8, 'start', 2.5, fill=DEEP, key='cjk'))
    return svg_doc(W, H, '\n'.join(out), bg='white')

if __name__ == '__main__':
    man = json.load(open('out/designs/manifest.json'))
    os.makedirs('out/tech', exist_ok=True)
    import cairosvg
    for m in man:
        svg = open(f"out/designs/{m['id']}-{m['slug']}/artwork.svg").read()
        page = placement_page_svg(m, svg)
        open(f"out/tech/placement-{m['id']}.svg", 'w').write(page)
    cairosvg.svg2png(url='out/tech/placement-01.svg', write_to='out/tech/placement-01.png', output_width=1600)
    cairosvg.svg2png(url='out/tech/placement-04.svg', write_to='out/tech/placement-04.png', output_width=1600)
    print('tech drawings ok')
