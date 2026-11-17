"""The 10 Bluuu bodysuit print designs. Each returns dict(w,h,defs,body,meta)."""
import math
from lib import *
from shapes import *

AZURE='#007FFF'; BLUE='#0073E0'; DEEP='#005CB3'; NAVY='#0D1B2E'; NAVY2='#002542'; INK='#003459'
L1='#CCE9FF'; L2='#99D3FF'; L3='#66BDFF'; L4='#339FFF'; PALE='#E6F4FF'
ORANGE='#FF8A00'; AMBER='#F59E0B'; SAND='#F3E7D3'; ROYAL='#2E53D9'; WHITE='#FFFFFF'; GREY='#E6EAEC'; LGREY='#F3F5F6'

PANTONE = {
    AZURE: ('Bluuu Azure', '2727 C'), BLUE: ('Bluuu Blue', '285 C'), DEEP: ('Deep Blue', '2935 C'),
    NAVY: ('Night Navy', '5395 C'), NAVY2: ('Abyss', '282 C'), INK: ('Ink Blue', '2767 C'),
    L1: ('Ice', '290 C'), L2: ('Lagoon', '291 C'), L3: ('Sky', '292 C'), L4: ('Bright Sky', '2191 C'), PALE: ('Mist', '9420 C'),
    ORANGE: ('Sunset Orange', '151 C'), AMBER: ('Amber', '1375 C'), SAND: ('Sand', '7506 C'), ROYAL: ('Logo Royal', '2726 C'),
    WHITE: ('White (puff)', 'White'), GREY: ('Fog Grey', 'Cool Gray 1 C'), LGREY: ('Cloud', 'Cool Gray 1 C'),
}

def P(d, fill, **kw):
    extra = ' '.join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
    return f'<path d="{d}" fill="{fill}" {extra}/>'

def T(text, key, size, x, y, fill, anchor='start', tracking=0, italic=0, scale_x=1.0, **kw):
    d, w = text_path(text, key, size, x, y, anchor, tracking, italic, scale_x)
    return P(d, fill, **kw)

# ------------------------------------------------------------------ 01
def d01():
    w, h = 190, 150
    body = []
    size = 96  # x-height ~ 49 mm
    d, tw = text_path('uuu', 'petrov-sb', size, x=w/2, y=92, anchor='middle', tracking=-1.5)
    body.append(P(d, AZURE))
    # tiny manta surfacing above the last u
    body.append(P(manta_fill(0.16, w/2 + tw/2 - 9, 30), NAVY))
    # lock-up
    body.append(T('bluuu', 'petrov-sb', 9, w/2 - 1, 118, NAVY, anchor='end', tracking=0.2))
    body.append(f'<rect x="{fmt(w/2+2)}" y="111" width="0.6" height="8" fill="{NAVY}"/>')
    body.append(T('nusa penida', 'petrov', 9, w/2 + 6, 118, NAVY, tracking=0.2))
    body.append(T('MANTA RAYS · SNORKELING · ONE UNFORGETTABLE DAY', 'petrov', 4.2, w/2, 131, DEEP, anchor='middle', tracking=0.9))
    return dict(w=w, h=h, defs='', body='\n'.join(body),
        meta=dict(id='01', slug='uuu-wave', name='uuu', style='Минимал / типографика', style_en='Minimal typographic',
                  colors=[AZURE, NAVY, DEEP], method='screen', placement='center', top=70, note='Три «u» из названия читаются как волна. 1 основной цвет + тёмный лок-ап.'))

# ------------------------------------------------------------------ 02
def d02():
    w, h = 170, 175
    body = []
    m1, m2 = manta_line(1.12, 85, 64)
    sw = 0.9
    g = f'fill="none" stroke="{NAVY}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
    body.append(f'<path d="{m1}" {g}/><path d="{m2}" {g}/>')
    # bubbles rising from the head
    for (bx, by, br) in [(96, 26, 1.6), (101, 18, 2.4), (94, 10, 1.2)]:
        body.append(f'<circle cx="{bx}" cy="{by}" r="{br}" {g}/>')
    # caption, left bottom
    body.append(T('swim with mantas', 'petrov-sb', 7, 8, 150, NAVY))
    body.append(T('manta point · nusa penida', 'petrov', 4.5, 8, 158, NAVY, tracking=0.3))
    body.append(T('bluuu', 'petrov-sb', 4.5, 8, 166, AZURE, tracking=0.2))
    return dict(w=w, h=h, defs='', body='\n'.join(body),
        meta=dict(id='02', slug='manta-line', name='Manta Line', style='Line-art / тату-графика', style_en='Single-line art',
                  colors=[NAVY, AZURE], method='screen-fine', placement='center', top=65, note='Манта одной непрерывной линией. Тонкая графика под татуировки владелицы; ширина линии 0,9 мм.'))

# ------------------------------------------------------------------ 03
def d03():
    w, h = 200, 165
    body = []
    # arched BLUUU with offset shadow (orange) and navy outline
    arc = arc_text('BLUUU', 'archivo', 40, 100, 182, 148, tracking=1.0)
    body.append(f'<path d="{arc}" fill="{ORANGE}" transform="translate(1.8 1.8)"/>')
    body.append(f'<path d="{arc}" fill="{AZURE}" stroke="{NAVY}" stroke-width="1.4" stroke-linejoin="round" paint-order="stroke"/>')
    # manta centre
    body.append(P(manta_fill(0.72, 100, 92), NAVY))
    # side stars
    body.append(P(star5(36, 92, 4.5), ORANGE)); body.append(P(star5(164, 92, 4.5), ORANGE))
    # NUSA PENIDA
    body.append(T('NUSA PENIDA', 'bebas', 20, 100, 142, NAVY, anchor='middle', tracking=2.2))
    # bottom band
    body.append(f'<rect x="38" y="147" width="124" height="0.8" fill="{NAVY}"/>')
    body.append(T("EST. 2016  ·  BALI  ·  08°45'S", 'bebas', 7.5, 100, 157, NAVY, anchor='middle', tracking=1.2))
    return dict(w=w, h=h, defs='', body='\n'.join(body),
        meta=dict(id='03', slug='varsity-2016', name='Varsity 2016', style='Колледж / varsity', style_en='Collegiate varsity',
                  colors=[AZURE, NAVY, ORANGE], method='screen-puff', placement='center', top=60, note='Арочная надпись, манта как эмблема, год основания. Рекомендуем объёмную (puff) краску на буквах.'))

# ------------------------------------------------------------------ 04
def d04():
    w, h = 200, 240
    body = []
    # top-left block (left chest zone, wearer's left = viewer's right? No: wearer's left chest = viewer's right on photo; we design in garment view => wearer's left is on the RIGHT side of artwork)
    x0 = 118
    body.append(f'<rect x="{x0}" y="10" width="9" height="9" fill="{AZURE}"/>')
    body.append(T('01', 'space-mono-b', 4.6, x0 + 4.5, 16.6, WHITE, anchor='middle'))
    body.append(T('BLUUU TOURS', 'petrov-sb', 7.2, x0 + 13, 17.6, NAVY, tracking=0.3))
    lines = ['SERANGAN HARBOUR → NUSA PENIDA', "08°45'22\"S  115°32'40\"E", 'DEP 08:00 — RET 18:00', 'MANTA POINT / CRYSTAL BAY', 'KELINGKING / BROKEN BEACH']
    y = 26
    for ln in lines:
        body.append(T(ln, 'space-mono', 3.9, x0, y, NAVY)); y += 6.0
    body.append(f'<rect x="{x0}" y="{fmt(y-3)}" width="76" height="0.5" fill="{NAVY}"/>')
    body.append(T('PREMIUM DAY TOUR · SINCE 2016', 'space-mono', 3.4, x0, y + 2.8, NAVY))
    # vertical ruler on the left edge (wearer's right side)
    rx = 14
    body.append(f'<rect x="{rx}" y="14" width="0.6" height="200" fill="{NAVY}"/>')
    for i in range(0, 201, 10):
        L = 5 if i % 50 == 0 else 2.5
        body.append(f'<rect x="{rx}" y="{14+i}" width="{L}" height="0.5" fill="{NAVY}"/>')
    for i in range(0, 201, 50):
        body.append(T(f'{i:03d}', 'space-mono', 3.0, rx + 6.5, 14 + i + 1.1, NAVY))
    body.append(f'<g transform="rotate(-90 {rx-3} 214)">{T("BLUUU EXPEDITION  —  NUSA PENIDA  —  BALI  —  INDONESIA", "space-mono", 3.8, rx-3, 214, NAVY, tracking=0.5)}</g>')
    # dashed route from Serangan (top-left of block) down to the crosshair, with waypoints
    route = [(x0 - 6, 66), (108, 78), (92, 96), (74, 120), (68, 146), (84, 172), (100, 184)]
    body.append(f'<path d="{smooth_open(route, 0.5)}" fill="none" stroke="{NAVY}" stroke-width="0.6" stroke-dasharray="2.2 1.8" stroke-linecap="round"/>')
    wps = [((x0 - 6, 66), 'SERANGAN', 'left'), ((92, 96), 'MANTA POINT', 'left'), ((68, 146), 'CRYSTAL BAY', 'left'), ((84, 172), 'KELINGKING', 'right')]
    for (px, py), label, side in wps:
        body.append(f'<circle cx="{fmt(px)}" cy="{fmt(py)}" r="1.9" fill="{WHITE}" stroke="{NAVY}" stroke-width="0.6"/>')
        body.append(f'<circle cx="{fmt(px)}" cy="{fmt(py)}" r="0.7" fill="{NAVY}"/>')
        if side == 'left':
            body.append(T(label, 'space-mono', 3.4, px - 4, py + 1.2, NAVY, anchor='end'))
        else:
            body.append(T(label, 'space-mono', 3.4, px + 4, py + 1.2, NAVY))
    # centre-bottom crosshair + depth note
    cx, cy = 100, 195
    body.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="none" stroke="{NAVY}" stroke-width="0.6"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="1.2" fill="{AZURE}"/>')
    for (dx, dy) in [(1,0),(-1,0),(0,1),(0,-1)]:
        body.append(f'<rect x="{fmt(cx + dx*11 - (3 if dx else 0.25))}" y="{fmt(cy + dy*11 - (3 if dy else 0.25))}" width="{6 if dx else 0.5}" height="{6 if dy else 0.5}" fill="{NAVY}"/>')
    body.append(T('MANTA POINT · DEPTH 12 M · VIS 25 M', 'space-mono', 3.5, cx, cy + 20, NAVY, anchor='middle'))
    body.append(T('SWIM · SNORKEL · DIVE', 'space-mono-b', 3.5, cx, cy + 26, AZURE, anchor='middle'))
    return dict(w=w, h=h, defs='', body='\n'.join(body),
        meta=dict(id='04', slug='expedition', name='Expedition 08°45′S', style='Utility / gorpcore', style_en='Technical utility',
                  colors=[NAVY, AZURE, WHITE], method='dtf', placement='center', top=45, note='Техническая раскладка: координаты, маршрут, линейка вдоль бока. Мелкий текст — DTF или тонкая шелкография.'))

# ------------------------------------------------------------------ 05
def d05():
    w, h = 190, 135
    defs = f'''
    <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{PALE}"/><stop offset="0.30" stop-color="{L3}"/><stop offset="0.49" stop-color="{AZURE}"/>
      <stop offset="0.51" stop-color="{INK}"/><stop offset="0.72" stop-color="{BLUE}"/><stop offset="1" stop-color="{L1}"/>
    </linearGradient>
    <radialGradient id="bub" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#ffffff"/><stop offset="0.45" stop-color="{L1}"/><stop offset="1" stop-color="{AZURE}"/></radialGradient>'''
    body = []
    d, tw = text_path('bluuu', 'unbounded-x', 44, x=w/2, y=92, anchor='middle', tracking=-1.0, italic=9)
    body.append(f'<path d="{d}" fill="{NAVY}" transform="translate(2.2 2.6)"/>')
    body.append(f'<path d="{d}" fill="url(#chrome)" stroke="{NAVY}" stroke-width="1.2" stroke-linejoin="round" paint-order="stroke"/>')
    # highlight strokes (thin white arcs on the letters) - simple: white thin copy offset
    body.append(f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="0.7" stroke-linejoin="round" transform="translate(-0.9 -1.1)" opacity="0.9"/>')
    body.append(T('deep', 'pacifico', 20, 36, 46, AZURE, italic=0))
    body.append(T('nusa penida · bali · since 2016', 'space-mono', 3.6, w/2 + 6, 110, NAVY, anchor='middle', tracking=0.5))
    # bubbles
    for (bx, by, br) in [(152, 30, 7), (165, 44, 4), (144, 46, 2.5), (28, 108, 3.5), (18, 97, 2.2)]:
        body.append(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="url(#bub)" stroke="{NAVY}" stroke-width="0.6"/>')
    for (sx, sy, sr) in [(22, 32, 6), (170, 100, 5), (98, 28, 3.2)]:
        body.append(P(sparkle(sx, sy, sr), AZURE)); body.append(P(sparkle(sx, sy, sr*0.45), WHITE))
    return dict(w=w, h=h, defs=defs, body='\n'.join(body),
        meta=dict(id='05', slug='deep-bluuu-y2k', name='deep bluuu', style='Y2K / хром', style_en='Y2K chrome',
                  colors=[AZURE, NAVY, L3, L1, WHITE], method='dtg', placement='center', top=70, note='Хромовый градиент, пузырьки, блики. Только цифровая печать (DTG/DTF) — градиенты.'))

# ------------------------------------------------------------------ 06
def d06():
    w, h = 170, 205
    cx, cy, R = 85, 80, 64
    defs = f'<clipPath id="circ"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>'
    body = []
    bands = [(0, 52, L1), (52, 66, L2), (66, 78, L3)]
    sea = [(78, 90, AZURE), (90, 102, BLUE), (102, 118, DEEP), (118, 146, INK)]
    g = ['<g clip-path="url(#circ)">']
    for y0, y1, c in bands + sea:
        g.append(f'<rect x="0" y="{y0}" width="{w}" height="{y1-y0}" fill="{c}"/>')
    # sun (sets into horizon at y=78)
    g.append(f'<circle cx="{cx}" cy="64" r="22" fill="{ORANGE}"/>')
    g.append(f'<rect x="0" y="78" width="{w}" height="80" fill="{AZURE}" opacity="0"/>')
    # retro cut lines through the sun
    for yy in (58, 64, 70, 75):
        g.append(f'<rect x="0" y="{yy}" width="{w}" height="1.6" fill="{L1}"/>')
    # reflection bars
    for i, (yy, ww) in enumerate([(84, 30), (92, 22), (100, 15), (109, 9)]):
        g.append(f'<rect x="{fmt(cx-ww/2)}" y="{yy}" width="{ww}" height="2" rx="1" fill="{ORANGE}"/>')
    # yacht on the horizon
    g.append(P(yacht(100, 78.5, 0.26, bow='left'), NAVY))
    g.append('</g>')
    body.extend(g)
    body.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{NAVY}" stroke-width="1.2"/>')
    # type
    body.append(T('Nusa Penida', 'shrikhand', 24, w/2, 174, ORANGE, anchor='middle', stroke=NAVY, stroke_width='1.1', stroke_linejoin='round', paint_order='stroke'))
    body.append(T('SUNSET CROSSING  ·  BLUUU TOURS  ·  BALI', 'bebas', 7, w/2, 188, NAVY, anchor='middle', tracking=1.4))
    body.append(T('SERANGAN HARBOUR — SINCE 2016', 'space-mono', 3.2, w/2, 196, DEEP, anchor='middle', tracking=0.4))
    return dict(w=w, h=h, defs=defs, body='\n'.join(body),
        meta=dict(id='06', slug='sunset-crossing', name='Sunset Crossing', style='Ретро-сёрф 70-х', style_en='70s surf retro',
                  colors=[L1, L2, L3, AZURE, BLUE, DEEP, INK, ORANGE, NAVY], method='dtg', placement='center', top=55, note='Полосатый закат в круге, яхта на горизонте, ретро-леттеринг. 9 цветов — DTG/DTF или 6-цветная шелкография с упрощением.'))

# ------------------------------------------------------------------ 07
def d07():
    w, h = 200, 235
    body = []
    body.append(T('BLUUU', 'anton', 78, w/2, 84, NAVY, anchor='middle', tracking=1.5))
    # halftone manta in azure overlapping the type
    pts = manta_pts(1.42, 100, 118)
    poly = spline_polyline(pts, closed=True, samples=10, tension=0.5)
    ys = [p[1] for p in poly]; ymin, ymax = min(ys), max(ys)
    xs = [p[0] for p in poly]; xmin, xmax = min(xs), max(xs)
    def dens(x, y):
        if not point_in_poly(x, y, poly): return 0
        t = (y - ymin) / (ymax - ymin)   # 0 at head, 1 at tail tip
        v = 1.0 - 0.9 * max(0, (t - 0.25) / 0.75) ** 1.1
        return v
    dots = circle_halftone(100, (ymin+ymax)/2, 0.95, cols=120, rows=int((ymax-ymin)/1.65), w=xmax-xmin+2, h=ymax-ymin+2, density=dens, fill=AZURE, rmin=0.22)
    body.append(dots)
    body.append(T('MANTA POINT', 'bebas', 15, w/2, 213, NAVY, anchor='middle', tracking=3))
    body.append(T("NUSA PENIDA  ·  08°45'S 115°32'E  ·  CAPTURED BY OUR GUESTS", 'space-mono', 3.3, w/2, 222, NAVY, anchor='middle', tracking=0.3))
    body.append(T('bluuu tours', 'petrov-sb', 4.5, w/2, 230, AZURE, anchor='middle', tracking=0.4))
    return dict(w=w, h=h, defs='', body='\n'.join(body),
        meta=dict(id='07', slug='manta-point-halftone', name='Manta Point', scale=0.9, style='Стритвир / халфтон', style_en='Streetwear halftone',
                  colors=[NAVY, AZURE], method='screen', placement='center', top=55, note='Крупный логотип-шрифт + манта из растровых точек (мин. точка 0,45 мм). 2 цвета шелкографии, точки печатаются поверх navy.'))

# ------------------------------------------------------------------ 08
def d08():
    w, h = 170, 180
    body = []
    g = f'fill="none" stroke="{NAVY}" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"'
    go = f'fill="none" stroke="{ORANGE}" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"'
    body.append(f'<g transform="rotate(-4 85 70)">{T("best day", "caveat-b", 34, 85, 72, NAVY, anchor="middle")}</g>')
    body.append(f'<g transform="rotate(-4 85 100)">{T("of my bali trip!", "caveat-b", 24, 88, 102, NAVY, anchor="middle")}</g>')
    # sun top-right
    body.append(f'<circle cx="142" cy="30" r="9" {go}/>')
    body.append(f'<g {go}>{sun_rays(142, 30, 12.5, 18, n=10)}</g>')
    # waves bottom-left with a little boat
    for i, yy in enumerate([128, 136, 144]):
        body.append(f'<path d="{wave_path(14, 70 - i*6, yy, 2.2, 14)}" {g}/>')
    body.append(f'<path d="{yacht(38, 125.5, 0.24)}" fill="#ffffff" stroke="{NAVY}" stroke-width="1.1" stroke-linejoin="round"/>')
    # manta doodle top-left (line version)
    m1, m2 = manta_line(0.26, 34, 28)
    body.append(f'<path d="{m1}" {g}/><path d="{m2}" {g}/>')
    # stars + 4.9
    for i in range(5):
        body.append(P(star5(96 + i*9, 134, 3.6), ORANGE))
    body.append(T('4.9 / 15 000 reviews', 'caveat', 9, 96, 147, NAVY))
    # hand arrow + bluuu signature
    body.append(f'<path d="M 118 158 Q 128 150 150 156" {g}/><path d="M 146 152 L 150 156 L 145 158.5" {g}/>')
    body.append(T('bluuu', 'caveat-b', 14, 152, 170, AZURE, anchor='middle'))
    body.append(T('nusa penida · bali', 'caveat', 8, 24, 168, NAVY))
    return dict(w=w, h=h, defs='', body='\n'.join(body),
        meta=dict(id='08', slug='best-day-doodle', name='Best Day', style='Рукописный / дудл', style_en='Hand-drawn doodle',
                  colors=[NAVY, ORANGE, AZURE], method='screen', placement='center', top=60, note='Цитата из реальных отзывов, дудлы: солнце, волны, яхта, манта, 5 звёзд. 3 цвета, живой характер.'))

# ------------------------------------------------------------------ 09
def d09():
    w, h = 140, 195
    cw, ch, r = 124, 150, 7
    ox, oy = 8, 8
    defs = f'<clipPath id="card"><rect x="{ox}" y="{oy}" width="{cw}" height="{ch}" rx="{r}"/></clipPath>'
    body = ['<g clip-path="url(#card)">']
    body.append(f'<rect x="{ox}" y="{oy}" width="{cw}" height="{ch}" fill="{PALE}"/>')
    # sun
    body.append(f'<circle cx="104" cy="36" r="11" fill="{SAND}"/>')
    # sea bands (horizon y=70)
    for y0, y1, c in [(58, 74, L2), (74, 90, L3), (90, 106, L4), (106, 124, AZURE), (124, 142, BLUE), (142, 160, DEEP)]:
        body.append(f'<rect x="{ox}" y="{y0}" width="{cw}" height="{y1-y0}" fill="{c}"/>')
    # white foam lines
    for yy, x0, x1 in [(86, 96, 118), (100, 104, 126), (114, 100, 120)]:
        body.append(f'<rect x="{x0}" y="{yy}" width="{x1-x0}" height="0.9" rx="0.45" fill="#ffffff" opacity="0.85"/>')
    # Kelingking headland seen from the viewpoint: foreground ridge bottom-right rising to the T-rex head at the far left.
    def poly(pts, fill, **kw):
        extra = ' '.join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
        return f'<path d="M ' + ' L '.join(f'{fmt(a)} {fmt(b)}' for a, b in pts) + f' Z" fill="{fill}" {extra}/>'
    land = [
        (134, 150), (126, 141), (116, 129), (106, 117), (97, 106), (89, 97), (82, 90),            # outer ridge of the neck up to the skull
        (76, 82), (70, 74), (62, 69), (52, 66), (42, 67), (33, 71), (26, 78), (21, 86),             # big rounded cranium
        (16, 93), (12, 100),                                                                         # snout tip pointing down-left
        (20, 103), (30, 103), (37, 106),                                                             # underside of the upper jaw
        (30, 112), (24, 121),                                                                        # lower jaw tip (wide open mouth)
        (36, 125), (48, 121), (56, 114),                                                             # jaw back to the throat
        (64, 120), (74, 131), (86, 143), (98, 155), (102, 160), (134, 160),                          # inner (cove) side of the neck
    ]
    body.append(poly(land, NAVY))
    body.append(poly([(82, 90), (89, 97), (97, 106), (106, 117), (116, 129), (126, 141), (134, 150), (134, 160), (118, 160), (108, 148), (98, 136), (90, 124), (83, 112), (80, 100)], INK))
    body.append(poly([(62, 69), (70, 74), (76, 82), (82, 90), (80, 100), (74, 92), (68, 82), (60, 74)], INK))
    for (x1, y1, x2, y2) in [(30, 76, 30, 100), (40, 69, 40, 104), (50, 67, 50, 112), (60, 70, 60, 112), (94, 118, 94, 140), (104, 130, 104, 152)]:
        body.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{DEEP}" stroke-width="0.6" opacity="0.7"/>')
    # beach: white-sand crescent in the cove at the foot of the cliff
    beach = [(20, 126), (36, 129), (50, 125), (60, 122), (70, 133), (82, 145), (94, 157), (98, 162), (88, 162), (78, 150), (66, 139), (56, 130), (46, 132), (34, 135), (18, 132)]
    body.append(poly(beach, SAND))
    body.append(f'<path d="M 18 134 L 34 137 L 46 134 L 56 132 L 66 141 L 78 152 L 88 162" fill="none" stroke="#ffffff" stroke-width="1.0" stroke-linejoin="round" stroke-linecap="round" opacity="0.95"/>')
    # tiny yacht
    body.append(P(yacht(108, 80, 0.09), WHITE))
    body.append('</g>')
    body.append(f'<rect x="{ox}" y="{oy}" width="{cw}" height="{ch}" rx="{r}" fill="none" stroke="{NAVY}" stroke-width="0.9"/>')
    body.append(T('KELINGKING', 'petrov-sb', 8.5, ox, 174, NAVY, tracking=2.6))
    body.append(T('Nusa Penida — Bali', 'petrov', 5, ox, 182, NAVY, tracking=0.3))
    body.append(T('bluuu', 'petrov-sb', 7, ox + cw, 174, AZURE, anchor='end', tracking=0.2))
    body.append(T("08°45'S", 'space-mono', 3.6, ox + cw, 182, DEEP, anchor='end'))
    return dict(w=w, h=h, defs=defs, body='\n'.join(body),
        meta=dict(id='09', slug='kelingking-flat', name='Kelingking', style='Flat-иллюстрация / постер', style_en='Flat landscape poster',
                  colors=[PALE, SAND, L2, L3, L4, AZURE, BLUE, DEEP, NAVY, INK, WHITE], method='dtg', placement='center', top=55, note='Открытка с видом на скалу-«тираннозавра» и пляж. 11 плашечных цветов — DTG/DTF.'))

# ------------------------------------------------------------------ 10
def d10():
    w, h = 200, 75
    body = []
    d, tw = text_path('BLUUU', 'petrov-sb', 50, x=w/2, y=46, anchor='middle', tracking=0.5)
    body.append(f'<path d="{d}" fill="{WHITE}" stroke="{GREY}" stroke-width="0.35"/>')
    # tiny azure manta accent at the end
    body.append(P(manta_fill(0.11, w/2 + tw/2 + 5, 14), AZURE))
    body.append(T('EST. 2016  ·  SERANGAN  ·  BALI', 'petrov', 4.6, w/2, 60, L2, anchor='middle', tracking=1.6))
    return dict(w=w, h=h, defs='', body='\n'.join(body),
        meta=dict(id='10', slug='tonal-bluuu', name='Tonal BLUUU', style='Премиум тон-в-тон', style_en='Tone-on-tone premium',
                  colors=[WHITE, AZURE, L2], method='puff', placement='center', top=80, note='Белая объёмная (puff/HD) печать на белом — видна фактурой и тенью. Акцент: маленькая лазурная манта.'))

ALL = [d01, d02, d03, d04, d05, d06, d07, d08, d09, d10]
