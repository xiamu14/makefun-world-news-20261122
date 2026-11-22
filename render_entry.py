from __future__ import annotations

import functools
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1024, 1024
INK = '#111111'
SUBTLE = '#333333'
MUTED = '#666666'
RED = '#AF242A'
RULE = '#D6D5D1'
PANEL_BG = '#F5F5F3'

FONTS = Path('/System/Library/Fonts/Supplemental')
ASSETS = Path('/Users/ben/Workspace/Project/make-fun/world-news-2026-11-22')


@functools.lru_cache(maxsize=64)
def font(kind: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    names = {
        'didot': 'Didot.ttc',
        'sans': 'Arial.ttf',
        'bold': 'Arial Bold.ttf',
        'narrow': 'Arial Narrow.ttf',
        'narrow_bold': 'Arial Narrow Bold.ttf',
        'italic': 'Georgia Italic.ttf',
        'georgia': 'Georgia.ttf',
        'georgia_bold': 'Georgia Bold.ttf',
    }
    return ImageFont.truetype(str(FONTS / names[kind]), size, index=index)


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ''
    for w in words:
        cand = f'{cur} {w}'.strip()
        if draw.textlength(cand, font=f) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered_text(draw: ImageDraw.ImageDraw, cx: int, y: int, text: str, f: ImageFont.FreeTypeFont, fill: str) -> None:
    tw = draw.textlength(text, font=f)
    draw.text((round(cx - tw / 2), y), text, font=f, fill=fill, anchor='lt')


def draw_wavy_rule(draw: ImageDraw.ImageDraw, x1: int, x2: int, y: int, color: str = RULE) -> None:
    pts = []
    for x in range(x1, x2 + 1, 2):
        dy = math.sin((x - x1) * 0.45) * 1.5
        pts.append((x, y + dy))
    if len(pts) > 1:
        draw.line(pts, fill=color, width=1)


def draw_brace(draw: ImageDraw.ImageDraw, x: int, y1: int, y2: int, side: str = 'left', color: str = '#999999') -> None:
    mid = (y1 + y2) / 2
    dx = -7 if side == 'left' else 7
    pts = [
        (x - dx * 0.5, y1),
        (x, y1 + 5),
        (x, mid - 5),
        (x + dx, mid),
        (x, mid + 5),
        (x, y2 - 5),
        (x - dx * 0.5, y2),
    ]
    draw.line(pts, fill=color, width=1)


def load_crop(kind: str, target_w: int, target_h: int) -> Image.Image:
    if kind == 'tehran':
        im = Image.open(ASSETS / 'lead-illustration/tehran-dusk.png').convert('RGB')
        w, h = im.size
        im = im.crop((0, int(h * 0.10), w, int(h * 0.88)))
    elif kind == 'finance':
        im = Image.open(ASSETS / 'expanded-english/illustrations/finance-climate.png').convert('RGB')
        w, h = im.size
        im = im.crop((0, int(h * 0.04), w, int(h * 0.48)))
    elif kind == 'climate':
        im = Image.open(ASSETS / 'expanded-english/illustrations/finance-climate.png').convert('RGB')
        w, h = im.size
        im = im.crop((0, int(h * 0.52), w, int(h * 0.96)))
    else:
        sheet = Image.open(ASSETS / 'illustration-assets/editorial-contact-sheet.png').convert('RGB')
        sw, sh = sheet.size
        cw, ch = sw // 2, sh // 3
        grid = {
            'nigeria': (1, 0),
            'brazil': (0, 1),
            'wolbachia': (1, 1),
            'hormuz': (0, 2),
            'tennis': (1, 2),
        }
        gx, gy = grid[kind]
        im = sheet.crop((gx * cw + 4, gy * ch + 4, (gx + 1) * cw - 4, (gy + 1) * ch - 4))
    return ImageOps.fit(im, (target_w, target_h), method=Image.Resampling.LANCZOS)


def paste_circle(canvas: Image.Image, im: Image.Image, cx: int, cy: int, diameter: int) -> None:
    sq = ImageOps.fit(im, (diameter, diameter), method=Image.Resampling.LANCZOS)
    mask = Image.new('L', (diameter, diameter), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse((0, 0, diameter - 1, diameter - 1), fill=255)
    canvas.paste(sq, (cx - diameter // 2, cy - diameter // 2), mask)
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((cx - diameter // 2, cy - diameter // 2, cx + diameter // 2 - 1, cy + diameter // 2 - 1), outline=RULE, width=1)


def render(data_path: Path, out_path: Path) -> None:
    data = json.loads(data_path.read_text(encoding='utf-8'))
    canvas = Image.new('RGB', (W, H), '#FFFFFF')
    draw = ImageDraw.Draw(canvas)

    mx = 24
    inner_w = W - 2 * mx  # 976

    # 1. Masthead with flanking editorial braces (Vanity Fair style)
    draw_brace(draw, mx + 8, 18, 80, side='left')
    draw_brace(draw, mx + 188, 18, 80, side='right')
    draw_centered_text(draw, mx + 98, 20, '24 STORIES · 3 DESKS', font('narrow_bold', 9), RED)
    draw_centered_text(draw, mx + 98, 34, 'EARLY EDITION', font('georgia_bold', 11), INK)
    draw_centered_text(draw, mx + 98, 50, 'SUNDAY · 22 NOV 2026', font('narrow', 10), SUBTLE)
    draw_centered_text(draw, mx + 98, 65, 'WORLD DIGEST →', font('narrow_bold', 9), RED)

    f_mast = font('didot', 54, index=2)
    draw_centered_text(draw, W // 2, 18, data['masthead'], f_mast, INK)

    rx = W - mx - 196
    draw_brace(draw, rx + 8, 18, 80, side='left')
    draw_brace(draw, rx + 188, 18, 80, side='right')
    draw_centered_text(draw, rx + 98, 20, 'KEY TRENDS', font('narrow_bold', 9), RED)
    draw_centered_text(draw, rx + 98, 34, 'S&P −8.6% · BRENT $92.57', font('narrow_bold', 11), INK)
    draw_centered_text(draw, rx + 98, 50, 'TAIWAN >80% → 3.8%', font('narrow', 10), SUBTLE)
    draw_centered_text(draw, rx + 98, 65, 'COP31 IN OVERTIME →', font('narrow_bold', 9), RED)

    # Sub-masthead navigation bar
    draw.line((mx, 90, W - mx, 90), fill=RULE, width=1)
    draw.text((mx, 95), '22 NOVEMBER 2026', font=font('italic', 11), fill=RED, anchor='lt')
    draw_centered_text(draw, W // 2, 95, 'WORLD AFFAIRS ▸    ECONOMY & SOCIETY ▸    PLANET & PEOPLE ▸    KEY NUMBERS', font('narrow_bold', 10), INK)
    rw_num = draw.textlength('01–24', font=font('narrow_bold', 10))
    draw.text((W - mx - rw_num, 95), '01–24', font=font('narrow_bold', 10), fill=MUTED, anchor='lt')
    draw.line((mx, 113, W - mx, 113), fill=INK, width=2)

    # 2. Asymmetric 3-Zone Hero Band (y = 124..446)
    hero_top = 124
    left_x, left_w = mx, 196
    ctr_x, ctr_w = mx + left_w + 18, 492
    side_x, side_w = ctr_x + ctr_w + 18, W - mx - (ctr_x + ctr_w + 18)  # 252

    # Left Column: 2 stacked photo-led cards ([09] Wall Street, [08] Lewis Pugh)
    left_cards = [
        ('finance', 'MARKETS · −8.6% WK', 'Wall Street reels as AI trade unwinds', 'S&P −8.6% · Nasdaq ≈−10%', 'CNBC / NPR · wk to 20 Nov'),
        ('hormuz', 'HORMUZ · 15KM SWIM', 'Pugh swims to spotlight the strait', 'Urges ceasefire & pollution cleanup', 'AFP / ST · 22 Nov'),
    ]
    ly = hero_top
    for idx, (crop_k, cat, hline, sub, src) in enumerate(left_cards):
        im = load_crop(crop_k, left_w, 72)
        canvas.paste(im, (left_x, ly))
        draw.rectangle((left_x, ly, left_x + left_w - 1, ly + 71), outline=RULE, width=1)
        ly += 77
        draw_centered_text(draw, left_x + left_w // 2, ly, cat, font('narrow_bold', 9), RED)
        ly += 13
        for hl in wrap_lines(draw, hline, font('georgia_bold', 11), left_w)[:2]:
            draw_centered_text(draw, left_x + left_w // 2, ly, hl, font('georgia_bold', 11), INK)
            ly += 13
        draw_centered_text(draw, left_x + left_w // 2, ly + 1, sub, font('sans', 9), SUBTLE)
        ly += 13
        draw_centered_text(draw, left_x + left_w // 2, ly, src, font('sans', 8), MUTED)
        ly += 16
        if idx == 0:
            draw.line((left_x + 20, ly - 3, left_x + left_w - 20, ly - 3), fill=RULE, width=1)
            ly += 5

    # Center Hero: Tehran Power Rationing ([01])
    hero_im = load_crop('tehran', ctr_w, 186)
    canvas.paste(hero_im, (ctr_x, hero_top))
    draw.rectangle((ctr_x, hero_top, ctr_x + ctr_w - 1, hero_top + 185), outline=RULE, width=1)
    hy = hero_top + 194
    draw_centered_text(draw, ctr_x + ctr_w // 2, hy, 'W O R L D   /   I R A N   ·   2 2   N O V   2 0 2 6', font('narrow_bold', 10), RED)
    hy += 16
    draw_centered_text(draw, ctr_x + ctr_w // 2, hy, 'Iran Announces Power Rationing', font('didot', 25, index=2), INK)
    hy += 28
    draw_centered_text(draw, ctr_x + ctr_w // 2, hy, 'as Gulf Tensions Persist', font('didot', 22, index=1), INK)
    hy += 28
    hero_sum = 'Utility plans up to 2-hr daily outages from 22 Nov; Bahrain reports industrial-facility strike.'
    for sl in wrap_lines(draw, hero_sum, font('sans', 10), ctr_w - 30)[:2]:
        draw_centered_text(draw, ctr_x + ctr_w // 2, hy, sl, font('sans', 10), SUBTLE)
        hy += 13
    draw_centered_text(draw, ctr_x + ctr_w // 2, hy + 3, '→   [01] RFE/RL · Reuters / ST · 22 Nov', font('sans', 8), RED)

    # Right Sidebar: KEY NUMBERS & TRENDS
    side_bot = 442
    draw.rectangle((side_x, hero_top, side_x + side_w, side_bot), fill=PANEL_BG)
    draw.rectangle((side_x, hero_top, side_x + side_w, side_bot), outline=RULE, width=1)
    sx_c = side_x + side_w // 2
    sy = hero_top + 10
    draw.line((side_x + 28, sy + 6, side_x + 62, sy + 6), fill=INK, width=1)
    draw.line((side_x + side_w - 62, sy + 6, side_x + side_w - 28, sy + 6), fill=INK, width=1)
    draw_centered_text(draw, sx_c, sy, 'KEY NUMBERS', font('narrow_bold', 12), INK)
    sy += 22

    # Bar chart: US Stocks weekly
    draw_centered_text(draw, sx_c, sy, 'US STOCKS · WK TO 20 NOV', font('narrow_bold', 9), RED)
    sy += 14
    bars = [('S&P 500', 8.6, '−8.6%'), ('Dow', 8.0, '−8.0%'), ('Nasdaq', 10.0, '≈−10%')]
    bx0 = side_x + 56
    bmax = 124
    for lbl, val, val_s in bars:
        draw.text((side_x + 12, sy), lbl, font=font('sans', 9), fill=INK, anchor='lt')
        bw = round((val / 11.0) * bmax)
        draw.rectangle((bx0, sy + 2, bx0 + bw, sy + 11), fill=RED)
        draw.text((bx0 + bw + 5, sy), val_s, font=font('bold', 9), fill=RED, anchor='lt')
        sy += 16
    sy += 6
    draw_wavy_rule(draw, side_x + 18, side_x + side_w - 18, sy)
    sy += 10

    # Numeric trend blocks
    trend_blocks = [
        ('US GASOLINE & BRENT · 20 NOV', '$3.69/gal  ·  Brent $92.57', '−3¢/day (+59¢/yr) · Brent +0.64% · WTI $83.98'),
        ('TAIWAN CHINA EXPOSURE', '>80% to 3.8%', 'Outbound inv. 2010–25 · CN+HK exports ≈44% to ≈27%'),
        ('HEALTH, LEGAL & DIGITAL', '≈69% fewer  ·  $7.25bn', 'Wolbachia dengue · Bayer deal · 19,372 YT purged'),
    ]
    for t_idx, (t_cat, t_big, t_sub) in enumerate(trend_blocks):
        draw_centered_text(draw, sx_c, sy, t_cat, font('narrow_bold', 9), RED)
        sy += 12
        draw_centered_text(draw, sx_c, sy, t_big, font('georgia_bold', 13), INK)
        sy += 17
        for tl in wrap_lines(draw, t_sub, font('sans', 8), side_w - 18)[:2]:
            draw_centered_text(draw, sx_c, sy, tl, font('sans', 8), MUTED)
            sy += 11
        sy += 4
        if t_idx < len(trend_blocks) - 1:
            draw_wavy_rule(draw, side_x + 28, side_x + side_w - 28, sy)
            sy += 8

    # 3. Middle "FEATURED" Band with 4 Circular Medallions (y = 456..626)
    feat_top, feat_bot = 460, 622
    draw.rectangle((mx, feat_top, W - mx, feat_bot), fill=PANEL_BG)
    draw.rectangle((mx, feat_top, W - mx, feat_bot), outline=RULE, width=1)
    # Floating "// FEATURED //" header pill
    pill_w = 126
    draw.rectangle((W // 2 - pill_w // 2, feat_top - 10, W // 2 + pill_w // 2, feat_top + 10), fill='#FFFFFF', outline=RULE, width=1)
    draw_centered_text(draw, W // 2, feat_top - 7, '«  FEATURED  »', font('narrow_bold', 11), INK)

    featured = [
        ('climate', 'CLIMATE · ANTALYA', 'COP31 talks enter overtime', '~200 delegations weigh deal'),
        ('brazil', 'WEATHER · 114 KM/H', 'Brazil supercell hits thousands', 'Tupanciretã · at least 3 dead'),
        ('wolbachia', 'HEALTH · ≈69% FEWER', 'Wolbachia cuts dengue in trial', '4-yr Brazil study, 5,700+ kids'),
        ('nigeria', 'NIGERIA · 24+ DEAD', 'Funeral boat capsizes in Bayelsa', '24 rescued · search continues'),
    ]
    fw = inner_w // 4
    for f_idx, (fk, fcat, ftitle, fsub) in enumerate(featured):
        fcx = mx + f_idx * fw + fw // 2
        f_im = load_crop(fk, 160, 160)
        paste_circle(canvas, f_im, fcx, feat_top + 56, 76)
        draw_centered_text(draw, fcx, feat_top + 101, fcat, font('narrow_bold', 9), RED)
        t_lines = wrap_lines(draw, ftitle, font('georgia_bold', 11), fw - 22)[:2]
        ty = feat_top + 115
        for fl in t_lines:
            draw_centered_text(draw, fcx, ty, fl, font('georgia_bold', 11), INK)
            ty += 13
        draw_centered_text(draw, fcx, ty + 3, fsub, font('sans', 8), MUTED)

    # 4. Bottom 3-Column Section with Red Top Rules + Downward Arrows (y = 638..994)
    bot_top = 640
    col_gap = 26
    col_w = (inner_w - 2 * col_gap) // 3  # 308

    # Vertical column dividers
    for c_i in (1, 2):
        gx = mx + c_i * col_w + (c_i - 1) * col_gap + col_gap // 2
        draw.line((gx, bot_top + 16, gx, 994), fill=RULE, width=1)

    bottom_cols = [
        ('WORLD AFFAIRS', None, [
            ('02', 'Bahrain reports industrial-facility strike', 'Fire reported 21 Nov, no injuries; Iran cites US targets · Reuters / ST'),
            ('03', 'Baltic drone strike forces ship evacuation', 'Sparta II’s 16 crew rescued by Finland; cargo unconfirmed · Reuters'),
            ('04', 'NATO reassures Poland after incursion', 'Rutte pledges defence after 3 Russian objects enter airspace · Reuters'),
            ('05', 'Taiwan warns Canada on China trade', 'Urges weighing coercion risks; investment share fell >80%→3.8% · AP'),
            ('06', 'Bangladesh adds 90 guard platoons', 'Security reinforced after political arson ahead of Hasina vow · AFP'),
            ('07', 'Japan ad faces vetting backlash', 'Incomplete check on YouTuber in ¥300m security campaign · Kyodo'),
        ]),
        ('ECONOMY & SOCIETY', None, [
            ('10', 'White House touts $17bn+ Asia deals', 'Commercial & defence packages; announced, not disbursed · Reuters'),
            ('11', 'Trump orders contractor Congress alerts', 'Federal firms must notify White House before disclosures · Reuters'),
            ('12', 'Indonesia queries 19,372 YT removals', 'Asks Google to explain Q3 coordinated-influence purge · ST'),
            ('13', 'Judge clears $7.25bn Bayer settlement', 'Roundup cancer claims deal; Bayer denies causation · NPR'),
            ('14', 'Jury convicts in Palisades Fire retrial', 'Rinderknecht guilty on 2025 arson counts; sentencing Mar 2027 · AP'),
            ('15', 'Meiji’s Alaska repatriation, revisited', '22 Nov feature details Aug return of 11 bone fragments & 1 object · Asahi'),
            ('16', 'Zagreb rallies over patient’s death', 'Thousands protest after footage; 4 technicians investigated · Reuters'),
        ]),
        ('PLANET & PEOPLE', ('tennis', 'SPORT · TURIN PREVIEW', 'Zverev meets Alcaraz in ATP final', '22 Nov title match set after Saturday semifinals · AP / ST'), [
            ('20', 'Hillsborough dengue hits 12-week low', '19 local cases (8–14 Nov); Florida emergency runs to 26 Nov · WUSF'),
            ('22', 'Magnitude 4.1 quake hits Myanmar', '95 km depth early 22 Nov; no casualty report yet · ANI / NCS'),
            ('23', 'US gas eases to $3.69; Brent $92.57', 'Pump price −3¢/day (+59¢/yr); Brent +0.64%, WTI $83.98/bbl · CNBC'),
        ]),
    ]

    for c_idx, (sec_name, photo_lead, items) in enumerate(bottom_cols):
        cx = mx + c_idx * (col_w + col_gap)
        ccx = cx + col_w // 2

        # Red top rule with centered label + downward arrow (Vanity Fair style)
        lbl_w = draw.textlength(sec_name, font=font('narrow_bold', 12)) + 16
        draw.line((cx, bot_top + 6, ccx - lbl_w / 2, bot_top + 6), fill=RED, width=1)
        draw.line((ccx + lbl_w / 2, bot_top + 6, cx + col_w, bot_top + 6), fill=RED, width=1)
        draw_centered_text(draw, ccx, bot_top, sec_name, font('narrow_bold', 12), RED)
        draw_centered_text(draw, ccx, bot_top + 13, '↓', font('bold', 11), RED)

        cy = bot_top + 30
        if photo_lead is not None:
            pk, pcat, phead, psub = photo_lead
            pim = load_crop(pk, col_w, 92)
            canvas.paste(pim, (cx, cy))
            draw.rectangle((cx, cy, cx + col_w - 1, cy + 91), outline=RULE, width=1)
            cy += 97
            draw_centered_text(draw, ccx, cy, pcat, font('narrow_bold', 9), RED)
            cy += 12
            draw_centered_text(draw, ccx, cy, phead, font('georgia_bold', 12), INK)
            cy += 15
            draw_centered_text(draw, ccx, cy, psub, font('sans', 9), SUBTLE)
            cy += 16
            draw.line((cx, cy, cx + col_w, cy), fill=RULE, width=1)
            cy += 7

        rem_h = 994 - cy
        slot_h = rem_h / len(items)
        for i_idx, (iid, ihead, isum) in enumerate(items):
            iy = round(cy + i_idx * slot_h)
            draw.text((cx, iy + 1), iid, font=font('narrow_bold', 10), fill=RED, anchor='lt')
            draw.text((cx + 17, iy), ihead, font=font('georgia_bold', 10), fill=INK, anchor='lt')
            by = iy + 14
            for bl in wrap_lines(draw, isum, font('sans', 9), col_w)[:2]:
                draw.text((cx, by), bl, font=font('sans', 9), fill=SUBTLE, anchor='lt')
                by += 11
            if i_idx < len(items) - 1:
                ry = round(cy + (i_idx + 1) * slot_h) - 4
                draw.line((cx, ry, cx + col_w, ry), fill=RULE, width=1)

    # 5. Footer
    draw.line((mx, 998, W - mx, 998), fill=RULE, width=1)
    draw.text((mx, 1003), data['footer'], font=font('sans', 8), fill=MUTED, anchor='lt')
    rw_end = draw.textlength('01–24', font=font('narrow_bold', 8))
    draw.text((W - mx - rw_end, 1003), '01–24', font=font('narrow_bold', 8), fill=INK, anchor='lt')

    canvas.save(out_path, format='PNG', optimize=True)
    if out_path.stat().st_size > 1048576:
        canvas.save(out_path, format='JPEG', quality=92, subsampling=0, optimize=True)


if __name__ == '__main__':
    base = Path(__file__).resolve().parent
    render(base / 'edition-data.json', base / 'entry.png')
    p = base / 'entry.png'
    print(f'Wrote {p} ({p.stat().st_size} bytes)')
