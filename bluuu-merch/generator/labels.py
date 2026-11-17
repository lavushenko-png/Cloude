"""Back-neck logo and inside tagless label artworks."""
import re, os
from lib import *
from designs import NAVY, AZURE, DEEP, L2, WHITE

LOGO = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brand', 'bluuu-logo-nav.svg')).read()
# extract the path 'd's (icon + wordmark), viewBox 0 0 140 30
LOGO_PATHS = re.findall(r'<path d="([^"]+)" fill="#2E53D9"', LOGO)

def logo_group(x, y, width_mm, fill=AZURE):
    s = width_mm / 140.0
    inner = ''.join(f'<path d="{d}"/>' for d in LOGO_PATHS)
    return f'<g transform="translate({fmt(x)} {fmt(y)}) scale({fmt(s)})" fill="{fill}">{inner}</g>'

def back_neck_logo():
    w, h = 40, 8.6
    return svg_doc(w, h, logo_group(0, 0, 40))

def inside_label(size='S'):
    w, h = 50, 30
    b = []
    b.append(logo_group(14, 3, 22, fill=NAVY))
    b.append(T_('bluuu.tours', 25, 11.5, 'middle', 2.6, DEEP, 'petrov'))
    # size box
    b.append(f'<rect x="20.5" y="13" width="9" height="6.5" rx="1" fill="none" stroke="{NAVY}" stroke-width="0.35"/>')
    b.append(T_(size, 25, 17.9, 'middle', 4.6, NAVY, 'petrov-sb'))
    b.append(T_('95% COTTON · 5% ELASTANE', 25, 22.3, 'middle', 2.4, NAVY, 'petrov'))
    b.append(T_('95% 棉 · 5% 氨纶', 25, 25.2, 'middle', 2.2, NAVY, 'cjk'))
    b.append(T_('WASH COLD 30° · INSIDE OUT · DO NOT BLEACH', 25, 27.4, 'middle', 1.7, DEEP, 'petrov'))
    b.append(T_('DO NOT TUMBLE DRY · IRON LOW ON REVERSE', 25, 29.4, 'middle', 1.7, DEEP, 'petrov'))
    b.append(T_('DESIGNED IN BALI · MADE IN CHINA', 25, 1.9, 'middle', 1.6, DEEP, 'petrov'))
    return svg_doc(w, h, '\n'.join(b))

def T_(text, x, y, anchor, size, fill, key):
    d, w = text_path(text, key, size, x, y, anchor)
    return f'<path d="{d}" fill="{fill}"/>'

if __name__ == '__main__':
    import cairosvg
    os.makedirs('out/labels', exist_ok=True)
    open('out/labels/back-neck-logo.svg', 'w').write(back_neck_logo())
    for sz in ['XS', 'S', 'M', 'L']:
        open(f'out/labels/inside-label-{sz}.svg', 'w').write(inside_label(sz))
    cairosvg.svg2png(url='out/labels/back-neck-logo.svg', write_to='out/labels/back-neck-logo.png', output_width=800, background_color='white')
    cairosvg.svg2png(url='out/labels/inside-label-S.svg', write_to='out/labels/inside-label-S.png', output_width=1000, background_color='white')
    print('labels ok')
