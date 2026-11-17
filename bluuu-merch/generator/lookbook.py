import json, base64, os
from designs import PANTONE, AZURE, NAVY
from copy_ru import COPY, METHOD_RU
man = json.load(open('out/designs/manifest.json'))
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
f400 = b64('../site/PetrovSans-Regular.woff2'); f600 = b64('../site/PetrovSans-SemiBold.woff2')
PAL = [('#007FFF', 'Bluuu Azure', 'основной'), ('#0073E0', 'Bluuu Blue', 'кнопки сайта'), ('#005CB3', 'Deep Blue', 'тени'), ('#0D1B2E', 'Night Navy', 'текст, тёмные секции'), ('#66BDFF', 'Sky', 'градиенты'), ('#CCE9FF', 'Ice', 'фон'), ('#FF8A00', 'Sunset Orange', 'акцент'), ('#F3E7D3', 'Sand', 'пляж')]

def chips(cols):
    return ''.join(f'<span class="chip" title="{PANTONE.get(c,("",""))[0]} {c}"><i style="background:{c}"></i>{PANTONE.get(c,("?",))[0]}</span>' for c in cols)

cards = []
for m in man:
    c = COPY[m['id']]
    cards.append(f'''
<article class="design" id="d{m['id']}">
  <figure class="mock"><img src="img/mock-{m['id']}.jpg" alt="Дизайн {m['id']} {c['name']} на боди" loading="lazy" width="915" height="998"></figure>
  <div class="info">
    <div class="eyebrow"><span class="num">{m['id']}</span><span class="tag">{c['tag']}</span></div>
    <h3>{c['name']}</h3>
    <p class="concept">{c['concept']}</p>
    <p class="why"><b>Почему купят.</b> {c['why']}</p>
    <dl class="spec">
      <div><dt>Печать</dt><dd>{c['print']}</dd></div>
      <div><dt>Размер арта</dt><dd>{m['w']:g} × {m['h']:g} мм</dd></div>
      <div><dt>Положение</dt><dd>центр груди, {m['top']} мм от горловины</dd></div>
      <div><dt>Цвета</dt><dd class="chips">{chips(m['colors'])}</dd></div>
    </dl>
    <figure class="art"><img src="img/art-{m['id']}.png" alt="Плоский арт {c['name']}" loading="lazy"><figcaption>Арт 1:1 · файл BLU-BS-{m['id']}-{m['slug']}.svg / .pdf</figcaption></figure>
  </div>
</article>''')

rows = ''.join(f"<tr><td>{m['id']}</td><td>{COPY[m['id']]['name']}</td><td>{COPY[m['id']]['tag']}</td><td>{m['w']:g}×{m['h']:g}</td><td>{len(m['colors'])}</td><td>{METHOD_RU[m['method']]}</td></tr>" for m in man)
pal = ''.join(f'<div class="sw"><i style="background:{h}"></i><b>{n}</b><span>{h}</span><small>{u}</small></div>' for h, n, u in PAL)

html = f'''<title>Bluuu Merch Capsule</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: brand-blue editorial lookbook; one column of design cards, each card = photo mockup + spec sheet */
@font-face{{font-family:'Petrov Sans';font-weight:400;font-display:swap;src:url(data:font/woff2;base64,{f400}) format('woff2')}}
@font-face{{font-family:'Petrov Sans';font-weight:600;font-display:swap;src:url(data:font/woff2;base64,{f600}) format('woff2')}}
:root{{
  --bg:#F3F7FB; --card:#FFFFFF; --fg:#0D1B2E; --muted:#4F6174; --line:#D5E2EE;
  --accent:#007FFF; --accent-deep:#0073E0; --accent-soft:#E6F4FF; --sun:#FF8A00;
  --display:'Petrov Sans', Inter, system-ui, sans-serif; --body:'Petrov Sans', Inter, system-ui, sans-serif; --mono:'Space Mono', ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0A1628;--card:#111D35;--fg:#E6F4FF;--muted:#9FB3C8;--line:#22314B;--accent:#339FFF;--accent-deep:#66BDFF;--accent-soft:#0F2A4A;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0A1628;--card:#111D35;--fg:#E6F4FF;--muted:#9FB3C8;--line:#22314B;--accent:#339FFF;--accent-deep:#66BDFF;--accent-soft:#0F2A4A;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--body);font-size:16px;line-height:1.5;padding-block:0 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.wrap{{max-width:1120px;margin:0 auto}}
h1,h2,h3{{font-family:var(--display);font-weight:600;letter-spacing:-0.01em;text-wrap:balance;margin:0}}
h1{{font-size:clamp(40px,7vw,84px);line-height:.98}}
h1 em{{font-style:italic;color:var(--accent)}}
h2{{font-size:clamp(26px,3.4vw,38px);margin-bottom:12px}}
h3{{font-size:30px;line-height:1.1}}
p{{margin:0}}
.lead{{font-size:19px;color:var(--muted);max-width:60ch}}
.label{{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-deep)}}
section{{padding-block:56px 8px}}
hr{{border:0;border-top:1px solid var(--line);margin:40px 0 0}}
/* hero */
.hero{{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:end;padding-block:48px 24px}}
.hero .copy{{display:grid;gap:22px}}
.hero figure{{margin:0;border-radius:18px;overflow:hidden;background:var(--card);aspect-ratio:3/4;max-width:100%}}
.hero img{{width:100%;height:100%;object-fit:cover;display:block}}
.facts{{display:flex;flex-wrap:wrap;gap:10px 28px;font-family:var(--mono);font-size:12px;color:var(--muted)}}
.facts b{{color:var(--fg);font-weight:400}}
/* brand */
.brandgrid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:22px}}
.sw{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;display:grid;gap:3px;font-size:13px}}
.sw i{{display:block;height:54px;border-radius:8px;margin-bottom:8px}}
.sw b{{font-weight:600}} .sw span{{font-family:var(--mono);font-size:11px;color:var(--muted)}} .sw small{{color:var(--muted)}}
.dna{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px}}
.dna div{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;display:grid;gap:6px}}
.dna b{{font-weight:600}} .dna p{{color:var(--muted);font-size:14px}}
.type-demo{{font-family:var(--display);font-size:44px;font-weight:600;line-height:1;color:var(--accent)}}
/* garment */
.garment{{display:grid;grid-template-columns:.8fr 1.2fr;gap:28px;align-items:start;margin-top:22px}}
.garment figure{{margin:0;border-radius:14px;overflow:hidden;aspect-ratio:3/4;max-width:100%}} .garment img{{width:100%;height:100%;object-fit:cover;display:block}}
.zones{{display:grid;gap:10px}}
.zones div{{display:grid;grid-template-columns:34px 1fr;gap:12px;align-items:start;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}}
.zones i{{font-style:normal;font-family:var(--mono);font-size:12px;background:var(--accent-soft);color:var(--accent-deep);border-radius:8px;height:34px;display:grid;place-items:center}}
.zones p{{font-size:14px;color:var(--muted)}} .zones b{{font-weight:600}}
/* designs */
.design{{display:grid;grid-template-columns:minmax(0,.92fr) minmax(0,1.08fr);gap:28px;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:22px;margin-top:22px;break-inside:avoid}}
.mock{{margin:0;border-radius:14px;overflow:hidden;aspect-ratio:915/998;max-width:100%;background:var(--accent-soft)}}
.mock img{{width:100%;height:100%;object-fit:cover;display:block}}
.info{{display:grid;gap:14px;align-content:start;min-width:0}}
.eyebrow{{display:flex;gap:12px;align-items:center}}
.num{{font-family:var(--mono);font-size:13px;color:#fff;background:var(--accent);border-radius:8px;padding:4px 9px}}
.tag{{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}}
.concept{{font-size:17px}} .why{{font-size:15px;color:var(--muted)}} .why b{{color:var(--fg);font-weight:600}}
.spec{{margin:4px 0 0;display:grid;gap:8px;border-top:1px solid var(--line);padding-top:12px}}
.spec div{{display:grid;grid-template-columns:120px 1fr;gap:10px;font-size:14px}}
.spec dt{{color:var(--muted)}} .spec dd{{margin:0}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}}
.chip{{display:inline-flex;align-items:center;gap:6px;font-size:12px;border:1px solid var(--line);border-radius:999px;padding:2px 9px 2px 4px}}
.chip i{{width:16px;height:16px;border-radius:50%;display:inline-block;border:1px solid rgba(0,0,0,.08)}}
.art{{margin:6px 0 0;display:grid;gap:6px}}
.art img{{width:100%;max-width:360px;border:1px solid var(--line);border-radius:10px;background:#fff}}
.art figcaption{{font-family:var(--mono);font-size:11px;color:var(--muted)}}
/* table */
table{{width:100%;border-collapse:collapse;font-size:14px;margin-top:18px;font-variant-numeric:tabular-nums}}
th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line)}} th{{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:400}}
.tablewrap{{overflow-x:auto}}
.cols{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px}}
.cols div{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px}} .cols b{{display:block;font-weight:600;margin-bottom:6px}} .cols p,.cols li{{font-size:14px;color:var(--muted)}} .cols ul{{margin:0;padding-left:18px}}
.pick{{border-color:var(--accent)}}
ol.steps{{margin:18px 0 0;padding:0;list-style:none;display:grid;gap:10px;counter-reset:s}}
ol.steps li{{display:grid;grid-template-columns:34px 1fr;gap:12px;align-items:start;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:15px}}
ol.steps li::before{{counter-increment:s;content:counter(s,decimal-leading-zero);font-family:var(--mono);font-size:12px;background:var(--accent-soft);color:var(--accent-deep);border-radius:8px;height:34px;display:grid;place-items:center}}
footer{{margin-top:56px;font-size:13px;color:var(--muted);display:flex;flex-wrap:wrap;gap:8px 24px}}
@media (max-width:820px){{.hero,.garment,.design{{grid-template-columns:1fr}} .brandgrid{{grid-template-columns:repeat(2,1fr)}} .dna,.cols{{grid-template-columns:1fr}} h3{{font-size:26px}} .design{{padding:14px}} .spec div{{grid-template-columns:100px 1fr}}}}
@media print{{body{{background:#fff;color:#0D1B2E}} .design{{break-inside:avoid;page-break-inside:avoid}} section{{padding-block:28px 4px}} .hero figure{{max-height:600px}}}}
</style>
<div class="wrap">
<header class="hero">
  <div class="copy">
    <span class="label">Bluuu Tours · Bali → Nusa Penida · мерч-капсула 2026</span>
    <h1>Боди <em>Bluuu</em>.<br>10 принтов, которые хочется носить</h1>
    <p class="lead">Коллекция для магазина Bluuu в Серангане: вещи покупают до или после тура на Нуса Пениду. Ни один дизайн не кричит логотипом — каждый рассказывает про день на воде: манты, скала Келингкинг, закат на обратном пути, координаты и цитаты из отзывов.</p>
    <div class="facts"><span>Изделие <b>белое боди-майка, fine rib</b></span><span>База <b>образец с фото</b></span><span>Размеры <b>XS–L</b></span><span>Файлы <b>SVG · PDF · PNG 300 dpi</b></span></div>
  </div>
  <figure><img src="img/hero.jpg" alt="Дизайн Manta Point на белом боди" width="1134" height="1512"></figure>
</header>

<section id="brand">
  <span class="label">01 · ДНК бренда с сайта bluuu.tours</span>
  <h2>Лазурь, ночной navy и одна тёплая нота</h2>
  <p class="lead">Палитра и шрифт взяты напрямую из кода сайта: CSS-переменные primary-50…950, тёмные фоны секций, янтарные звёзды рейтинга и фирменный шрифт Petrov Sans (Regular и SemiBold). Все арты набраны этим же шрифтом и переведены в кривые.</p>
  <div class="brandgrid">{pal}</div>
  <div class="dna">
    <div><span class="type-demo">Bluuu</span><b>Petrov Sans</b><p>Геометрический гротеск сайта. Заголовок «Discover <i>Nusa Penida</i>» задаёт приём: прямой + курсив, белый + лазурь.</p></div>
    <div><b>Мотивы</b><p>Манта (главный момент тура), яхта, скала Келингкинг, гавань Серанган, широта 08°45′S, год основания 2016, рейтинг 4.9 и 15 000+ отзывов, фразы «captured by our guests», «best day of our Bali trip».</p></div>
    <div><b>Тон</b><p>Premium, seamless, спокойный: много воздуха, мало элементов. Поэтому в коллекции нет «кричащих» сувенирных композиций — только вещи, которые носятся как дизайнерская одежда.</p></div>
  </div>
</section>

<section id="garment">
  <span class="label">02 · Изделие и зоны печати</span>
  <h2>Белое боди-майка с тонкими бретелями</h2>
  <div class="garment">
    <figure><img src="img/sample-photo-sm.jpg" alt="Образец боди на модели" width="756" height="1008"></figure>
    <div class="zones">
      <div><i>A</i><div><b>Центр груди — основная зона</b><p>До 200 × 240 мм. Верх арта на 45–80 мм ниже горловины, по линии центра переда. Все 10 дизайнов рассчитаны на эту зону и на размеры XS–L без перемасштабирования.</p></div></div>
      <div><i>B</i><div><b>Спинка, под горловиной</b><p>Логотип Bluuu 40 × 8,6 мм в лазури, 25 мм ниже горловины спинки. Единый для всей капсулы — тихая «подпись» бренда.</p></div></div>
      <div><i>C</i><div><b>Внутренняя печатная этикетка</b><p>Вместо вшивного ярлыка — печать 50 × 30 мм внутри спинки: логотип, размер, состав, уход, «Designed in Bali · Made in China».</p></div></div>
      <div><i>·</i><div><b>Ткань и посадка</b><p>Fine rib 92–95 % хлопок + 5–8 % эластан, 240–260 г/м², optic white; глубокий вырез спинки, высокий вырез ноги, застёжка на кнопках в ластовице. Все краски — с эластичной добавкой под стрейч.</p></div></div>
    </div>
  </div>
</section>

<section id="designs">
  <span class="label">03 · Коллекция</span>
  <h2>Десять принтов, десять характеров</h2>
  <p class="lead">Мокапы наложены на присланное фото с реальным масштабом (1 мм = 2,85 px), поэтому размер принта на теле соответствует тех-паку.</p>
  {''.join(cards)}
</section>

<section id="summary">
  <span class="label">04 · Сводка</span>
  <h2>Что, где и как печатать</h2>
  <div class="tablewrap"><table>
    <thead><tr><th>№</th><th>Дизайн</th><th>Стиль</th><th>Арт, мм</th><th>Цветов</th><th>Метод</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <div class="cols">
    <div class="pick"><b>Первые сэмплы — 4 дизайна</b><p>01 uuu, 02 Manta Line, 07 Manta Point, 05 deep bluuu: закрывают четыре вкуса (минимал, арт, стрит, Y2K) и три технологии печати, так что по сэмплам сразу видно качество фабрики.</p></div>
    <div><b>Вторая волна</b><p>03 Varsity, 09 Kelingking, 08 Best Day — после первых продаж. 04, 06, 10 держим как лимитированные дропы (например, к высокому сезону).</p></div>
    <div><b>Цена и варианты</b><p>Розница 35–45 USD в магазине и на борту. Второй колорвей: navy-база с инверсией цветов для 01, 07 и 10. Тот же арт 09 идёт на открытку и магнит.</p></div>
  </div>
</section>

<section id="next">
  <span class="label">05 · Следующие шаги</span>
  <h2>От файла до полки</h2>
  <ol class="steps">
    <li>Отправить фабрике тех-пак (PDF) и ZIP с артами. Запросить strike-off (пробные оттиски) на реальной ткани по каждому цвету.</li>
    <li>Утвердить цвет по Pantone/HEX на оттисках: лазурь 007FFF — самый капризный, проверить при дневном свете.</li>
    <li>Получить по одному пред-продакшн образцу (размер S) четырёх первых дизайнов, тест: 5 стирок при 30°, растяжение 30 % без трещин.</li>
    <li>Съёмка образцов на борту и в магазине; запуск предзаказа в WhatsApp-рассылке после тура.</li>
    <li>Тираж: по размерной сетке XS–L, старт 50–100 шт. на дизайн.</li>
  </ol>
</section>
<footer><span>Bluuu Merch Capsule · v1.0 · ноябрь 2026</span><span>Цвета и шрифт — с bluuu.tours</span><span>Файлы для фабрики: bluuu-merch/factory/</span></footer>
</div>
'''
os.makedirs('out/lookbook', exist_ok=True)
open('out/lookbook/index.html', 'w').write(html)
# standalone copy with doctype for local PDF rendering
open('out/lookbook/lookbook-standalone.html', 'w').write('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + html.replace('<meta name="claude:viewport-fit-sides" content="cover">', '') + '</head></html>' if False else '<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + html + '</body></html>')
print('lookbook html', len(html) // 1024, 'KB')
