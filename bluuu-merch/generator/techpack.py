"""Factory tech pack (EN + 中文) as HTML pages -> PDF via Chromium."""
import json, os, re, base64, datetime
from designs import PANTONE, AZURE, NAVY, DEEP
from copy_ru import COPY
man = json.load(open('out/designs/manifest.json'))
TODAY = datetime.date.today().isoformat()
def hex2cmyk(h):
    r, g, b = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    k = 1 - max(r, g, b)
    if k >= 0.999: return (0, 0, 0, 100)
    c = (1 - r - k) / (1 - k); m = (1 - g - k) / (1 - k); y = (1 - b - k) / (1 - k)
    return tuple(round(v * 100) for v in (c, m, y, k))
METHOD = {
 'screen': ('Screen print, plastisol or water-based ink with stretch additive', '丝网印刷（胶浆/水浆 + 弹性助剂）'),
 'screen-fine': ('Fine-line screen print (180–200 T mesh) or DTF transfer', '细线丝网印刷（180–200目）或 DTF 热转印'),
 'screen-puff': ('Screen print; lettering in puff ink (0.5–1 mm rise), other colours flat', '丝网印刷；字母发泡印花（高度0.5–1mm），其余平面印'),
 'dtf': ('DTF transfer (300 dpi, soft-hand hot-melt) or fine screen print', 'DTF 热转印（300dpi，软手感热熔胶）或细线丝印'),
 'dtg': ('DTG direct-to-garment (pretreat, 1200 dpi) or DTF transfer', '数码直喷 DTG（预处理，1200dpi）或 DTF 热转印'),
 'puff': ('White puff / high-density ink tone-on-tone (2 strokes, 0.5–1 mm rise) + 1 flat colour; alt: tonal embroidery', '白色发泡/厚板印花（同色调，两刀，高度0.5–1mm）+ 1 平面色；备选：同色刺绣'),
}
NOTES = {
 '01': 'Solid shapes. Keep Azure opaque on white; 2 strokes if needed.',
 '02': 'Line weight 0.9 mm; must stay crisp – no spread > 0.15 mm. Bubbles are 0.9 mm strokes.',
 '03': 'Azure letters with 1.4 mm navy keyline + orange offset shadow; puff on letters only (azure). Registration ±0.5 mm.',
 '04': 'Smallest text cap-height 2.4 mm; dashed route 0.6 mm; ruler ticks 0.5 mm. No ink spread. Print on relaxed garment.',
 '05': 'Gradient (chrome) artwork – digital only. White highlights are part of the artwork (print white). Navy keyline 1.2 mm.',
 '06': 'Flat bands of 7 blues + orange + navy outline. Digital preferred; for screen print simplify to 6 spot colours (merge Ice/Lagoon and Blue/Deep).',
 '07': 'Halftone: smallest dot 0.45 mm, largest 1.9 mm, 1.65 mm grid. Print NAVY first, AZURE dots over it (wet-on-wet or flash). Mesh 120 T for navy, 156 T for dots.',
 '08': 'Hand-drawn strokes 1.1 mm, round caps. Stars/sun in Sunset Orange, signature in Azure.',
 '09': 'Flat illustration, 11 spot colours – digital print. Keep card corner radius 7 mm crisp. No white under-base needed on white fabric.',
 '10': 'Letters: white puff/HD ink on optic-white fabric (tone-on-tone), 0.35 mm Fog-grey keyline optional. Manta accent in Azure flat ink. Alt: white tonal embroidery, 40 mm letter height.',
}
NOTES_ZH = {
 '01': '实色图形，白底上天蓝需遮盖力足，必要时印两刀。',
 '02': '线宽0.9mm，必须清晰，扩张不超过0.15mm。',
 '03': '天蓝字 + 1.4mm 藏青描边 + 橙色错位阴影；仅字母发泡。套位 ±0.5mm。',
 '04': '最小字高2.4mm；虚线0.6mm；刻度0.5mm。不可扩张，松弛状态下印花。',
 '05': '渐变（镀铬效果）仅数码印。白色高光为图案一部分（需印白）。',
 '06': '7种蓝色+橙色+藏青描边平面色块。优先数码；丝印可简化为6色。',
 '07': '网点：最小0.45mm，最大1.9mm，网格1.65mm。先印藏青，再叠印天蓝网点。',
 '08': '手绘线条1.1mm圆头。星星/太阳为日落橙，签名为天蓝。',
 '09': '平面插画11个专色，数码印。圆角7mm需清晰。',
 '10': '字母：白色发泡/厚板印在漂白面料上（同色调）。小魔鬼鱼为天蓝平面色。备选：白色同色刺绣。',
}
def colour_rows(cols):
    r = []
    for c in cols:
        name, pms = PANTONE.get(c, ('—', '—')); cmyk = hex2cmyk(c)
        r.append(f'<tr><td><i class="sw" style="background:{c}"></i></td><td>{name}</td><td class="mono">{c}</td><td class="mono">{cmyk[0]}/{cmyk[1]}/{cmyk[2]}/{cmyk[3]}</td><td class="mono">{pms}</td></tr>')
    return ''.join(r)
def inline_svg(path, cls=''):
    s = open(path).read()
    s = re.sub(r'width="[^"]+mm" height="[^"]+mm"', f'class="{cls}"', s, count=1)
    return s
def b64img(p):
    ext = p.rsplit('.', 1)[1]; mime = 'image/png' if ext == 'png' else 'image/jpeg'
    return f'data:{mime};base64,' + base64.b64encode(open(p, 'rb').read()).decode()

pages = []
head = f'<div class="hd"><span>BLUUU TOURS — TECH PACK 技术包</span><span>Style BLU-BS · Women\'s tank bodysuit 女式吊带连体衣</span><span>v1.0 · {TODAY}</span></div>'
def foot(n): return f'<div class="ft"><span>Confidential – for production use only · 仅供生产使用</span><span>Page {n}</span></div>'

# ---- cover
pages.append(f'''<section class="page cover">
<div class="cov-l"><span class="eyebrow">TECH PACK · 技术包 / 工艺单</span>
<h1>Bluuu Tours<br>Printed Tank Bodysuit</h1>
<p class="big">女式印花吊带连体衣 · 10 prints · White colourway</p>
<table class="meta"><tr><td>Style code 款号</td><td>BLU-BS-01 … BLU-BS-10</td></tr><tr><td>Season 季节</td><td>2026 · Bluuu shop, Serangan (Bali)</td></tr><tr><td>Version 版本</td><td>1.0 — {TODAY}</td></tr><tr><td>Sizes 尺码</td><td>XS · S · M · L</td></tr><tr><td>Base colour 底色</td><td>Optic white 漂白</td></tr><tr><td>Contact 联系人</td><td>Bluuu Tours · info@bluuu.tours</td></tr></table>
<p class="small">Units: millimetres unless stated. Pantone references are nearest Solid Coated approximations – match to HEX/CMYK on strike-offs and send for approval before bulk.<br>单位：毫米。潘通色号为最接近的 Solid Coated 近似值，请以 HEX/CMYK 为准制作印花样并在大货前确认。</p></div>
<div class="cov-r"><img src="{b64img('out/lookbook/img/hero.jpg')}" alt=""></div>
</section>''')

# ---- garment spec
pages.append(f'''<section class="page">{head}
<h2>1 · Garment specification 款式规格</h2>
<div class="two">
<div><img class="photo" src="{b64img('out/lookbook/img/sample-photo-sm.jpg')}" alt="sample"><p class="cap">Reference sample (customer photo) 参考样衣（客户照片）</p></div>
<div>
<table class="spec">
<tr><th>Item 品名</th><td>Women's fitted tank bodysuit, scoop neck, thin straps 女式修身吊带连体衣，圆领，细肩带</td></tr>
<tr><th>Fabric 面料</th><td>Fine 1×1 rib knit, 92–95 % cotton / 5–8 % elastane, 240–260 g/m², optic white, pre-shrunk, 4-way stretch 细罗纹针织，92–95% 棉 / 5–8% 氨纶，240–260 g/m²，漂白，预缩，四面弹</td></tr>
<tr><th>Alternative 备选</th><td>95 % modal / 5 % spandex jersey, 220 g/m² (softer hand) 95% 莫代尔/5% 氨纶汗布</td></tr>
<tr><th>Construction 工艺</th><td>Self-fabric bound neckline and armholes (10 mm); straps 20 mm; low scoop back (neck drop 120 mm); high-cut leg; cotton-lined gusset with 3 nickel-free snaps; coverstitch leg hems 自布包边领口及袖窿（10mm）；肩带20mm；后深圆领（领深120mm）；高叉；棉布里裆，3粒无镍按扣；腿口绷缝</td></tr>
<tr><th>Trims 辅料</th><td>Snaps 10 mm nickel-free, white; no woven neck label (tagless print, see §3); optional woven side label 12 × 40 mm "bluuu" at left side seam 按扣10mm无镍白色；无织唛领标（印标，见第3节）；可选侧缝织唛12×40mm</td></tr>
<tr><th>Colourway 配色</th><td>Optic white body 漂白；prints per design pages 印花见各页</td></tr>
<tr><th>Packing 包装</th><td>Fold 250 × 200 mm, 1 pc per recycled polybag with size sticker; hangtag TBD 折叠250×200mm，每件一个可回收胶袋带尺码贴；吊牌待定</td></tr>
</table>
<table class="sizes"><caption>Reference measurements (cm, half, relaxed) 参考尺寸表（厘米，半围，松弛） · Grade from approved physical sample 以确认的实物样衣为准 · Tolerance ±1 cm 公差</caption>
<tr><th>POM 部位</th><th>XS</th><th>S</th><th>M</th><th>L</th></tr>
<tr><td>Chest 1/2 胸围</td><td>30</td><td>32</td><td>34</td><td>36</td></tr>
<tr><td>Waist 1/2 腰围</td><td>26</td><td>28</td><td>30</td><td>32</td></tr>
<tr><td>Hip 1/2 臀围</td><td>31</td><td>33</td><td>35</td><td>37</td></tr>
<tr><td>Front length HPS–crotch 前长（肩点至裆）</td><td>60</td><td>62</td><td>64</td><td>66</td></tr>
<tr><td>Front neck drop from HPS 前领深</td><td>7</td><td>7</td><td>7.5</td><td>7.5</td></tr>
<tr><td>Back neck drop 后领深</td><td>12</td><td>12</td><td>12.5</td><td>12.5</td></tr>
<tr><td>Strap width 肩带宽</td><td>2</td><td>2</td><td>2</td><td>2</td></tr>
<tr><td>Leg opening 腿口</td><td>24</td><td>25</td><td>26</td><td>27</td></tr>
<tr><td>Gusset width 裆宽</td><td>6</td><td>6</td><td>6.5</td><td>6.5</td></tr>
</table></div></div>{foot(2)}</section>''')

# ---- print requirements
pages.append(f'''<section class="page">{head}
<h2>2 · Print zones & general print requirements 印花位置与通用要求</h2>
<div class="two">
<div>{inline_svg('out/tech/placement-01.svg', 'draw')}<p class="cap">Zone A centre front (shown with design 01) · Zone B back-neck logo · Zone C inside tagless label<br>A 前中印花区（以01款为例）· B 后领标志 · C 内领印标</p></div>
<div class="req">
<h3>Placement 位置</h3>
<ul><li>All artwork centred on centre-front line; top edge measured from CF neck point (lowest point of front neckline). Tolerance ±3 mm, rotation ±1°. 所有图案以前中线居中；顶边自前领中点量起。公差±3mm，旋转±1°。</li>
<li>Print on relaxed (unstretched) garment on a flat platen. 松弛平铺状态下印花。</li>
<li>Same artwork size for XS–L (no grading). XS–L 使用同一尺寸图案，不放码。</li></ul>
<h3>Inks & durability 油墨与牢度</h3>
<ul><li>Fabric is 4-way stretch: use stretch additive / elastic binder. Test: stretch 30 % – no cracking. 面料四面弹：须加弹性助剂。拉伸30%不龟裂。</li>
<li>Soft hand feel; avoid thick plastisol deposits except where puff is specified. 手感柔软；除指定发泡外避免厚胶浆。</li>
<li>Wash test: 5 cycles at 30 °C inside out – no cracking, fading or peeling (DTF). 水洗测试：30°C反面洗5次，无龟裂、褪色、脱落。</li>
<li>Cure per ink datasheet (plastisol 160 °C full cure; water-based 150 °C 2–3 min). 按油墨规格固化。</li></ul>
<h3>Minimums 最小值</h3>
<ul><li>Positive line 0.5 mm; text cap height 2.0 mm; halftone dot 0.45 mm; keylines as drawn. 正线0.5mm；字高2.0mm；网点0.45mm。</li>
<li>Mesh: 120–156 T solids, 180–200 T fine lines/halftone. 网目：实色120–156目，细线/网点180–200目。</li></ul>
<h3>Colour 颜色</h3>
<ul><li>Match to HEX / CMYK given on each page; Pantone Solid Coated is a nearest reference only. 以各页 HEX/CMYK 为准，潘通仅作参考。</li>
<li>Strike-offs of every colour on the actual white rib fabric for approval before bulk. 大货前须在实际面料上做印花样确认。</li></ul>
</div></div>{foot(3)}</section>''')

# ---- labels
pages.append(f'''<section class="page">{head}
<h2>3 · Labels & branding trims 标签与辅料</h2>
<div class="three">
<div><h3>B · Back-neck logo 后领标志</h3>{inline_svg('out/labels/back-neck-logo.svg', 'lab')}<table class="spec small"><tr><th>Size</th><td>40 × 8.6 mm</td></tr><tr><th>Position</th><td>Outside back, centred, 25 mm below CB neck 后背外侧居中，后领中点下25mm</td></tr><tr><th>Method</th><td>Screen print or DTF, 1 colour 丝印或DTF，1色</td></tr><tr><th>Colour</th><td>Bluuu Azure #007FFF · CMYK 100/50/0/0 · PMS 2727 C</td></tr><tr><th>File</th><td class="mono">labels/back-neck-logo.svg / .pdf</td></tr></table></div>
<div><h3>C · Inside tagless label 内领印标</h3>{inline_svg('out/labels/inside-label-S.svg', 'lab')}<table class="spec small"><tr><th>Size</th><td>50 × 30 mm</td></tr><tr><th>Position</th><td>Inside back, centred, 15 mm below CB neck 后背内侧居中，后领中点下15mm</td></tr><tr><th>Method</th><td>Heat-transfer tagless label or water-based screen print, 2 colours (Navy #0D1B2E, Deep Blue #005CB3), soft hand 无感烫标或水浆丝印，2色，软手感</td></tr><tr><th>Sizes</th><td>4 versions: XS / S / M / L (files provided) 四个尺码版本</td></tr><tr><th>File</th><td class="mono">labels/inside-label-XS…L.svg / .pdf</td></tr></table></div>
<div><h3>Care wording 洗涤说明</h3><p>WASH COLD 30° · INSIDE OUT · DO NOT BLEACH · DO NOT TUMBLE DRY · IRON LOW ON REVERSE · 95 % COTTON 5 % ELASTANE · DESIGNED IN BALI · MADE IN CHINA</p><p>30°冷水洗 · 反面洗 · 不可漂白 · 不可转笼烘干 · 反面低温熨烫 · 95%棉 5%氨纶</p>
<h3>Hangtag 吊牌 (TBD)</h3><p>Suggested: 60 × 90 mm, 350 g uncoated card, Azure print, cotton string. Artwork to follow. 建议：60×90mm，350g 无涂布卡纸，天蓝色印刷，棉绳。图稿后续提供。</p>
<h3>Optional woven label 可选织唛</h3><p>12 × 40 mm, white ground, azure "bluuu", folded loop at left side seam, 60 mm above leg opening. 白底天蓝字，对折车缝于左侧缝，腿口上60mm。</p></div>
</div>{foot(4)}</section>''')

# ---- design pages
n = 5
for m in man:
    c = COPY[m['id']]; meth = METHOD[m['method']]
    base = f"BLU-BS-{m['id']}-{m['slug']}"
    pages.append(f'''<section class="page">{head}
<h2>4.{int(m['id'])} · Design {m['id']} — {c['name']} <span class="sub">{m['style_en']}</span></h2>
<div class="two dz">
<div>{inline_svg(f"out/tech/placement-{m['id']}.svg", 'draw')}<p class="cap">Placement drawing, scale 1:4 · 印花位置图（比例1:4）· Zone A</p></div>
<div>
<div class="artbox"><img src="{b64img(f"out/lookbook/img/art-{m['id']}.png")}" alt="artwork"></div>
<table class="spec small">
<tr><th>Artwork code 图稿编号</th><td class="mono">{base}</td></tr>
<tr><th>Artwork size 图案尺寸</th><td><b>{m['w']:g} × {m['h']:g} mm</b> (W × H), scale 1:1 in files 文件为1:1</td></tr>
<tr><th>Placement 位置</th><td>Centre front, top edge <b>{m['top']} mm</b> below CF neck point 前中，顶边距前领中点 {m['top']} mm</td></tr>
<tr><th>Method 工艺</th><td>{meth[0]}<br>{meth[1]}</td></tr>
<tr><th>Colours 颜色</th><td>{len(m['colors'])} · <table class="cols"><tr><th></th><th>Name</th><th>HEX</th><th>CMYK</th><th>PMS (ref)</th></tr>{colour_rows(m['colors'])}</table></td></tr>
<tr><th>Notes 备注</th><td>{NOTES[m['id']]}<br>{NOTES_ZH[m['id']]}</td></tr>
<tr><th>Files 文件</th><td class="mono">artwork/{base}.svg · .pdf (vector, text outlined 文字已转曲) · -300dpi.png (transparent)</td></tr>
</table></div></div>{foot(n)}</section>''')
    n += 1

# ---- approval / QC / order
order_rows = ''.join(f"<tr><td>{m['id']}</td><td>{COPY[m['id']]['name']}</td><td></td><td></td><td></td><td></td><td></td></tr>" for m in man)
pages.append(f'''<section class="page">{head}
<h2>5 · Approval process, QC & order form 确认流程、质检与订单表</h2>
<div class="two">
<div><h3>Approval steps 确认步骤</h3>
<ol><li>Fabric swatch + strike-offs of all colours on actual fabric (photo in daylight + physical) 面料小样 + 全色印花样（日光下照片 + 实物）</li>
<li>Pre-production sample, size S, designs 01 / 02 / 05 / 07 first, then the rest 产前样，S码，先做 01/02/05/07，其余随后</li>
<li>Customer PP approval in writing 客户书面确认产前样</li>
<li>Bulk production; keep 1 sealed sample per design 大货生产；每款封样1件</li>
<li>Final inspection AQL 2.5 (major) / 4.0 (minor), photos before shipping 终检 AQL 2.5/4.0，出货前拍照</li></ol>
<h3>QC checklist 质检要点</h3>
<ul><li>Print position ±3 mm; no ghosting, pinholes, fibrillation 印花位置±3mm；无重影、针孔、起毛</li>
<li>Colour within ΔE 2 of approved strike-off 颜色与确认样 ΔE≤2</li>
<li>Stretch 30 % no cracking; 5 washes no change 拉伸30%不裂；5次水洗无变化</li>
<li>Puff rise 0.5–1 mm even; DTF edges fully bonded 发泡高度均匀；DTF边缘粘合牢固</li>
<li>Snaps aligned, nickel-free certificate; no loose threads 按扣对位，无镍证明；无线头</li></ul></div>
<div><h3>Order form 订单表 (to be completed 待填写)</h3>
<table class="order"><tr><th>#</th><th>Design</th><th>XS</th><th>S</th><th>M</th><th>L</th><th>Total</th></tr>{order_rows}<tr><td colspan="6"><b>Total 合计</b></td><td></td></tr></table>
<p class="small">Delivery terms, packing list and shipping marks to be confirmed separately. Please quote: sample cost, unit price per design at 100 / 300 / 500 pcs, lead time. 交期、装箱单及唛头另行确认。请报价：样品费、每款100/300/500件单价、生产周期。</p>
<h3>Files delivered 交付文件</h3>
<ul class="mono"><li>bluuu-bodysuit-techpack.pdf (this document)</li><li>artwork/BLU-BS-01 … 10 .svg / .pdf / -300dpi.png</li><li>labels/back-neck-logo, inside-label-XS…L</li></ul></div></div>{foot(n)}</section>''')

css = '''
@page{size:A4 landscape;margin:0}
*{box-sizing:border-box} body{margin:0;font-family:Inter,"WenQuanYi Zen Hei",system-ui,sans-serif;color:#0D1B2E;font-size:10.5px;line-height:1.35;background:#fff}
.page{width:297mm;height:210mm;padding:10mm 12mm 9mm;page-break-after:always;position:relative;overflow:hidden;background:#fff}
.hd,.ft{display:flex;justify-content:space-between;font-family:"Space Mono",ui-monospace,monospace;font-size:8px;letter-spacing:.06em;color:#4F6174;text-transform:uppercase}
.hd{border-bottom:1px solid #0D1B2E;padding-bottom:3mm;margin-bottom:4mm} .ft{position:absolute;left:12mm;right:12mm;bottom:6mm;border-top:1px solid #D5E2EE;padding-top:2mm;text-transform:none}
h1{font-size:34px;line-height:1.02;margin:6px 0 10px;font-weight:700;letter-spacing:-.01em} h2{font-size:17px;margin:0 0 4mm;font-weight:700} h3{font-size:11px;margin:4mm 0 1.5mm;text-transform:uppercase;letter-spacing:.06em;color:#0073E0} .sub{font-weight:400;color:#4F6174;font-size:12px;margin-left:8px}
.eyebrow{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:.14em;color:#0073E0} .big{font-size:14px;color:#4F6174;margin:0 0 8mm} .small{font-size:8.5px;color:#4F6174;margin-top:4mm} p{margin:0 0 2mm}
.cover{display:grid;grid-template-columns:1.15fr .85fr;gap:10mm;padding:16mm 14mm} .cov-r img{width:100%;height:178mm;object-fit:cover;border-radius:4mm} .cov-l{display:flex;flex-direction:column;justify-content:center}
table{border-collapse:collapse;width:100%} td,th{padding:1.4mm 2mm;border-bottom:1px solid #D5E2EE;vertical-align:top;text-align:left} th{font-weight:600;background:#F3F7FB;width:28%}
.meta{max-width:150mm;margin:4mm 0;font-size:10px} .meta td:first-child{color:#4F6174;width:40%}
.two{display:grid;grid-template-columns:1fr 1fr;gap:8mm;align-items:start} .three{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8mm;align-items:start}
.photo{width:100%;max-height:120mm;object-fit:cover;border-radius:3mm} .cap{font-size:8px;color:#4F6174;margin-top:1.5mm}
.spec th{width:24%} .spec.small{font-size:9px} .spec.small th,.spec.small td{padding:1.1mm 1.6mm}
.sizes{margin-top:4mm;font-size:9px;font-variant-numeric:tabular-nums} .sizes caption{text-align:left;font-size:8px;color:#4F6174;margin-bottom:1mm} .sizes th{width:auto;text-align:center} .sizes td{text-align:center} .sizes td:first-child{text-align:left}
.req ul,.req ol,ol,ul{margin:0 0 2mm;padding-left:4.5mm} li{margin-bottom:1mm}
.draw{width:100%;height:auto;border:1px solid #D5E2EE;border-radius:2mm} .lab{width:100%;height:auto;border:1px dashed #99D3FF;padding:3mm;border-radius:2mm;background:#fff;max-height:50mm}
.dz{grid-template-columns:1.05fr .95fr} .artbox{border:1px solid #D5E2EE;border-radius:2mm;padding:3mm;display:flex;justify-content:center;background:#fff;margin-bottom:3mm} .artbox img{max-height:62mm;max-width:100%}
.cols{font-size:8.5px;margin-top:1mm} .cols th{background:none;font-weight:600;width:auto;padding:.6mm 1.2mm} .cols td{padding:.6mm 1.2mm;border-bottom:1px solid #EEF3F8} .sw{display:inline-block;width:9px;height:9px;border-radius:50%;border:1px solid rgba(0,0,0,.15);vertical-align:middle}
.mono{font-family:"Space Mono",ui-monospace,monospace;font-size:8.5px} .order td,.order th{text-align:center;height:6.5mm;border:1px solid #D5E2EE;background:none;width:auto} .order td:nth-child(2){text-align:left}
'''
html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Bluuu Tours — Tech Pack — Printed Tank Bodysuit</title><style>{css}</style></head><body>{"".join(pages)}</body></html>'
os.makedirs('out/techpack', exist_ok=True)
open('out/techpack/techpack.html', 'w').write(html)
print('techpack html', len(html)//1024, 'KB, pages', len(pages))
