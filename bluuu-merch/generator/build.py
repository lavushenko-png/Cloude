import os, json, io, cairosvg
from PIL import Image, ImageDraw
from lib import svg_doc
import designs
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'designs')
os.makedirs(OUT, exist_ok=True)
manifest = []
tiles = []
for fn in designs.ALL:
    d = fn(); m = d['meta']
    folder = os.path.join(OUT, f"{m['id']}-{m['slug']}"); os.makedirs(folder, exist_ok=True)
    sc = m.get('scale', 1.0)
    if sc != 1.0:
        d['w'], d['h'] = round(d['w'] * sc, 1), round(d['h'] * sc, 1)
        d['body'] = f'<g transform="scale({sc})">' + d['body'] + '</g>'
    svg = svg_doc(d['w'], d['h'], d['body'], bg=None, defs=d['defs'])
    open(os.path.join(folder, 'artwork.svg'), 'w').write(svg)
    # preview on white (tonal design on light grey so it is visible)
    bg = '#DCE3E8' if m['id'] == '10' else 'white'
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=int(d['w'] * 6), background_color=bg)
    open(os.path.join(folder, 'preview.png'), 'wb').write(png)
    im = Image.open(io.BytesIO(png)).convert('RGB')
    tiles.append((m['id'], im))
    m.update(w=d['w'], h=d['h']); manifest.append(m)
json.dump(manifest, open(os.path.join(OUT, 'manifest.json'), 'w'), ensure_ascii=False, indent=2)
# contact sheet
cell = 700
sheet = Image.new('RGB', (cell * 5, int(cell * 1.3) * 2), '#f3f5f6')
dr = ImageDraw.Draw(sheet)
for i, (mid, im) in enumerate(tiles):
    im = im.copy(); im.thumbnail((cell - 40, int(cell * 1.3) - 60))
    x = (i % 5) * cell + 20; y = (i // 5) * int(cell * 1.3) + 40
    sheet.paste(im, (x + (cell - 40 - im.width) // 2, y))
    dr.text((x, y - 30), mid, fill='#0D1B2E')
sheet.save(os.path.join(OUT, 'contact-sheet.jpg'), quality=85)
print('built', len(manifest))
