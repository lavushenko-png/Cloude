"""Export factory artwork files: SVG (1:1 mm), PDF (vector), PNG 300 dpi transparent. Also crops for the lookbook."""
import os, json, shutil, cairosvg
from PIL import Image
man = json.load(open('out/designs/manifest.json'))
os.makedirs('out/factory/artwork', exist_ok=True); os.makedirs('out/factory/labels', exist_ok=True)
os.makedirs('out/lookbook/img', exist_ok=True)
for m in man:
    src = f"out/designs/{m['id']}-{m['slug']}"
    base = f"out/factory/artwork/BLU-BS-{m['id']}-{m['slug']}"
    svg = open(f'{src}/artwork.svg').read()
    open(base + '.svg', 'w').write(svg)
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=base + '.pdf')
    dpi = 300; wpx = int(round(m['w'] / 25.4 * dpi)); hpx = int(round(m['h'] / 25.4 * dpi))
    cairosvg.svg2png(bytestring=svg.encode(), write_to=base + '-300dpi.png', output_width=wpx, output_height=hpx)
    # lookbook images
    im = Image.open(f'{src}/mockup.jpg'); im.crop((150, 170, 1370, 1500)).resize((915, 998), Image.LANCZOS).save(f"out/lookbook/img/mock-{m['id']}.jpg", quality=84)
    pv = Image.open(f'{src}/preview.png').convert('RGB'); pv.thumbnail((900, 900)); pv.save(f"out/lookbook/img/art-{m['id']}.png", optimize=True)
for f in os.listdir('out/labels'):
    if f.endswith('.svg'):
        svg = open(f'out/labels/{f}').read(); shutil.copy(f'out/labels/{f}', f'out/factory/labels/{f}')
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=f"out/factory/labels/{f[:-4]}.pdf")
shutil.copy('photo.jpg', 'out/lookbook/img/sample-photo.jpg')
Image.open('photo.jpg').resize((756, 1008)).save('out/lookbook/img/sample-photo-sm.jpg', quality=84)
Image.open('out/designs/07-manta-point-halftone/mockup.jpg').resize((1134, 1512)).save('out/lookbook/img/hero.jpg', quality=86)
print('export ok'); os.system('ls -la out/factory/artwork | head -40; du -sh out/factory out/lookbook/img')
