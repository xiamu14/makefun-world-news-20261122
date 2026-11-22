from __future__ import annotations

import functools
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1024, 1024
INK = '#111111'
SUBTLE = '#333333'
MUTED = '#5F5F5F'
RED = '#AF242A'
RULE = '#D4D3CE'
PANEL_BG = '#F5F5F2'

FONTS = Path('/System/Library/Fonts/Supplemental')
ASSETS = Path('/Users/ben/Workspace/Project/make-fun/world-news-2026-11-22')

REGION_COLORS = {
    'EUROPE': '#2B5B84',
    'ASIA': '#C88A2B',
    'MIDDLE EAST': '#AF242A',
    'AFRICA': '#2E6F40',
    'AMERICAS': '#6B4C9A',
    'OCEANIA': '#2E8B8B',
    'GLOBAL': '#555555',
}


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
    lines, cur = [], ''
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


def draw_centered(draw: ImageDraw.ImageDraw, cx: int, y: int, text: str, f: ImageFont.FreeTypeFont, fill: str) -> None:
    tw = draw.textlength(text, font=f)
    draw.text((round(cx - tw / 2), y), text, font=f, fill=fill, anchor='lt')


def draw_brace(draw: ImageDraw.ImageDraw, x: int, y1: int, y2: int, side: str = 'left', color: str = '#999999') -> None:
    mid = (y1 + y2) / 2
    dx = -6 if side == 'left' else 6
    pts = [(x - dx * 0.4, y1), (x, y1 + 4), (x, mid - 4), (x + dx, mid), (x, mid + 4), (x, y2 - 4), (x - dx * 0.4, y2)]
    draw.line(pts, fill=color, width=1)


def draw_art(kind: str, w: int, h: int) -> Image.Image:
    if kind == 'hormuz_photo':
        sheet = Image.open(ASSETS / 'illustration-assets/editorial-contact-sheet.png').convert('RGB')
        sw, sh = sheet.size
        im = sheet.crop((4, 2 * (sh // 3) + 4, sw // 2 - 4, sh - 4))
        return ImageOps.fit(im, (w, h), method=Image.Resampling.LANCZOS)
    if kind == 'cop31_photo':
        im = Image.open(ASSETS / 'expanded-english/illustrations/finance-climate.png').convert('RGB')
        iw, ih = im.size
        return ImageOps.fit(im.crop((0, int(ih * 0.52), iw, int(ih * 0.96))), (w, h), method=Image.Resampling.LANCZOS)
    if kind == 'tehran_photo':
        im = Image.open(ASSETS / 'lead-illustration/tehran-dusk.png').convert('RGB')
        iw, ih = im.size
        return ImageOps.fit(im.crop((0, int(ih * 0.14), iw, int(ih * 0.86))), (w, h), method=Image.Resampling.LANCZOS)

    # Crisp vector-style editorial illustrations in Pillow
    im = Image.new('RGB', (w, h), '#DCE6EE')
    d = ImageDraw.Draw(im)
    if kind == 'baltic_ship':
        d.rectangle((0, 0, w, int(h * 0.55)), fill='#CEDAE3')
        d.rectangle((0, int(h * 0.55), w, h), fill='#3B6E8C')
        # Ship hull + smoke
        d.polygon([(70, int(h * 0.65)), (240, int(h * 0.65)), (225, int(h * 0.80)), (85, int(h * 0.80))], fill='#232A31')
        d.rectangle((100, int(h * 0.50), 145, int(h * 0.65)), fill='#E9E7E2')
        for cx, cy, r, col in [(165, 36, 18, '#555A60'), (185, 24, 22, '#6E747B'), (205, 16, 16, '#898F96')]:
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        d.ellipse((158, int(h * 0.55), 178, int(h * 0.72)), fill='#D9532F')
    elif kind == 'bahrain_fire':
        d.rectangle((0, 0, w, h), fill='#EFEBE4')
        d.rectangle((0, int(h * 0.72), w, h), fill='#C8B89E')
        d.rectangle((36, int(h * 0.42), 92, int(h * 0.72)), fill='#5D6268')
        d.rectangle((104, int(h * 0.50), 152, int(h * 0.72)), fill='#7A7F85')
        d.polygon([(72, int(h * 0.45)), (98, int(h * 0.18)), (118, int(h * 0.48))], fill='#D94E28')
        d.ellipse((84, 8, 128, 36), fill='#666666')
    elif kind == 'nato_poland':
        d.rectangle((0, 0, w, h), fill='#E8EEF4')
        d.polygon([(w // 2 - 28, 18), (w // 2 + 28, 18), (w // 2 + 24, 58), (w // 2, 76), (w // 2 - 24, 58)], fill='#1F4E8C')
        d.rectangle((w // 2 - 14, 34, w // 2 + 14, 46), fill='#FFFFFF')
        d.rectangle((w // 2 - 14, 46, w // 2 + 14, 58), fill='#AF242A')
    elif kind == 'drone_wave':
        d.rectangle((0, 0, w, h), fill='#1D2A38')
        for r in (16, 30, 44):
            d.arc((w // 2 - r, h // 2 - r + 10, w // 2 + r, h // 2 + r + 10), 190, 350, fill='#5B86A8', width=1)
        for dx, dy in [(42, 34), (96, 26), (144, 44)]:
            d.polygon([(dx, dy), (dx + 14, dy + 6), (dx, dy + 12)], fill='#E2583E')
    elif kind == 'gaza_van':
        d.rectangle((0, 0, w, h), fill='#EAE6DF')
        d.rectangle((0, int(h * 0.70), w, h), fill='#B9B2A6')
        d.rectangle((48, int(h * 0.42), 134, int(h * 0.70)), fill='#FFFFFF', outline='#444444')
        d.ellipse((58, int(h * 0.65), 76, int(h * 0.80)), fill='#222222')
        d.ellipse((110, int(h * 0.65), 128, int(h * 0.80)), fill='#222222')
        d.polygon([(82, int(h * 0.30)), (96, int(h * 0.14)), (110, int(h * 0.42))], fill='#D94E28')
    elif kind == 'mexico_cartel':
        d.rectangle((0, 0, w, h), fill='#E8E1D5')
        d.ellipse((46, 30, 82, 66), outline='#222222', width=4)
        d.ellipse((104, 30, 140, 66), outline='#222222', width=4)
        d.line((82, 48, 104, 48), fill='#222222', width=3)
    elif kind == 'fbi_cyber':
        d.rectangle((0, 0, w, h), fill='#18222D')
        d.rectangle((32, 26, 156, 72), fill='#253545', outline='#4A6A88')
        d.rectangle((80, 38, 108, 60), fill='#D9A136')
        d.arc((84, 24, 104, 46), 180, 360, fill='#D9A136', width=3)
    elif kind == 'sudan_mine':
        d.rectangle((0, 0, w, h), fill='#EDE1CA')
        d.rectangle((0, int(h * 0.68), w, h), fill='#C2A67D')
        d.polygon([(94, 24), (124, 68), (64, 68)], fill='#F2C94C', outline='#111111')
        d.text((91, 38), '!', font=font('bold', 22), fill='#111111')
    elif kind == 'belgium_strike':
        d.rectangle((0, 0, w, h), fill='#E4E9EE')
        d.rectangle((0, int(h * 0.72), w, h), fill='#555A60')
        d.polygon([(40, 56), (132, 56), (144, 46), (120, 48), (48, 48)], fill='#FFFFFF', outline='#333333')
        d.rectangle((106, 22, 166, 38), fill=RED)
        draw_centered(d, 136, 25, 'STRIKE', font('narrow_bold', 10), '#FFFFFF')
    elif kind == 'f1_vegas':
        d.rectangle((0, 0, w, h), fill='#171722')
        for rx, col in [(36, '#AF242A'), (66, '#E2B63B'), (96, '#2E8B8B'), (126, '#6B4C9A')]:
            d.rectangle((rx, 30, rx + 18, h - 10), fill=col)
        draw_centered(d, w // 2, 16, 'P1', font('didot', 22, index=2), '#FFFFFF')
    return im


def draw_badge(im: Image.Image, text: str, bg: str = RED) -> None:
    d = ImageDraw.Draw(im)
    f = font('narrow_bold', 10)
    tw = d.textlength(text, font=f)
    d.rectangle((6, 6, round(tw + 16), 22), fill=bg)
    d.text((11, 8), text, font=f, fill='#FFFFFF', anchor='lt')


def draw_world_map(canvas: Image.Image, x0: int, y0: int, mw: int, mh: int, pins: list[dict]) -> None:
    d = ImageDraw.Draw(canvas)
    d.rectangle((x0, y0, x0 + mw, y0 + mh), fill='#F2F4F5', outline=RULE, width=1)

    def proj(lon: float, lat: float) -> tuple[int, int]:
        px = x0 + round(((lon + 180.0) / 360.0) * mw)
        py = y0 + round(((85.0 - lat) / 145.0) * mh)
        return px, py

    # Simplified crisp landmass polygons
    continents = [
        [(-165, 65), (-130, 70), (-80, 62), (-55, 50), (-75, 28), (-105, 18), (-125, 38)],  # N America
        [(-80, 12), (-50, 5), (-35, -8), (-55, -35), (-70, -52), (-80, -15)],  # S America
        [(-10, 36), (0, 50), (15, 58), (35, 68), (55, 65), (50, 45), (30, 38), (5, 36)],  # Europe
        [(-16, 35), (10, 37), (34, 31), (50, 12), (40, -10), (28, -34), (15, -30), (10, 5), (-16, 15)],  # Africa
        [(35, 38), (60, 38), (75, 20), (105, 10), (122, 24), (142, 44), (165, 64), (100, 72), (55, 68)],  # Asia
        [(114, -22), (145, -12), (153, -28), (138, -38), (115, -34)],  # Australia
    ]
    for poly in continents:
        d.polygon([proj(lo, la) for lo, la in poly], fill='#DFDDD4', outline='#C5C2B7')

    f_pin = font('narrow_bold', 8)
    for p in pins:
        px, py = proj(p['lon'], p['lat'])
        px = max(x0 + 8, min(x0 + mw - 8, px))
        py = max(y0 + 8, min(y0 + mh - 8, py))
        col = REGION_COLORS.get(p['r'], '#555555')
        d.ellipse((px - 6, py - 6, px + 6, py + 6), fill=col, outline='#FFFFFF')
        draw_centered(d, px, py - 5, str(p['id']), f_pin, '#FFFFFF')


def render(data_path: Path, out_path: Path) -> None:
    data = json.loads(data_path.read_text(encoding='utf-8'))
    canvas = Image.new('RGB', (W, H), '#FFFFFF')
    d = ImageDraw.Draw(canvas)
    mx = 22
    iw = W - 2 * mx  # 980

    # 1. Masthead with Vanity Fair-style flanking braces
    d.text((mx, 8), 'THE WORLD IN ONE DAY', font=font('narrow_bold', 9), fill=RED, anchor='lt')
    rt = '30 STORIES · 7 REGIONS · ALL DATED SUNDAY 22 NOV 2026'
    d.text((W - mx - d.textlength(rt, font=font('narrow_bold', 9)), 8), rt, font=font('narrow_bold', 9), fill=MUTED, anchor='lt')

    draw_brace(d, mx + 4, 24, 72, 'left')
    draw_brace(d, mx + 134, 24, 72, 'right')
    draw_centered(d, mx + 69, 27, 'THE WORLD DAILY', font('narrow_bold', 10), INK)
    draw_centered(d, mx + 69, 41, 'EARLY EDITION', font('sans', 8), MUTED)
    draw_centered(d, mx + 69, 54, '30 STORIES →', font('narrow_bold', 9), RED)

    draw_centered(d, W // 2, 22, data['masthead'], font('didot', 48, index=2), INK)

    rx = W - mx - 138
    draw_brace(d, rx + 4, 24, 72, 'left')
    draw_brace(d, rx + 134, 24, 72, 'right')
    draw_centered(d, rx + 69, 27, '7 REGIONS', font('narrow_bold', 10), INK)
    draw_centered(d, rx + 69, 41, 'VERIFIED 22 NOV', font('sans', 8), MUTED)
    draw_centered(d, rx + 69, 54, 'DATE CHECK →', font('narrow_bold', 9), RED)

    draw_centered(d, W // 2, 74, data['deck'], font('italic', 11), SUBTLE)
    d.line((mx, 92, W - mx, 92), fill=INK, width=2)

    # 2. 6-Stat Breaking Numbers Strip (y = 97..137)
    sw = iw // 6
    for i, st in enumerate(data['stats']):
        sx = mx + i * sw
        if i > 0:
            d.line((sx, 99, sx, 134), fill=RULE, width=1)
        d.text((sx + 6, 98), st['num'], font=font('georgia_bold', 19), fill=INK, anchor='lt')
        nw = d.textlength(st['num'], font=font('georgia_bold', 19)) + 12
        for li, line in enumerate(st['desc'].split('\n')[:2]):
            d.text((sx + nw, 100 + li * 11), line, font=font('sans', 8), fill=MUTED, anchor='lt')
    d.line((mx, 138, W - mx, 138), fill=RULE, width=1)

    # 3. 7-Region Color Bar (y = 143..163)
    tot = sum(r['count'] for r in data['regions'])
    rx_cur = mx
    for r in data['regions']:
        rw = round((r['count'] / tot) * iw)
        d.rectangle((rx_cur, 143, rx_cur + rw - 2, 161), fill=r['color'])
        draw_centered(d, rx_cur + rw // 2, 146, r['name'], font('narrow_bold', 9), '#FFFFFF')
        rx_cur += rw

    # 4. Top 3 Lead Illustrated Cards (y = 170..356)
    lw = (iw - 24) // 3  # 318
    for i, lead in enumerate(data['leads']):
        lx = mx + i * (lw + 12)
        im = draw_art(lead['art'], lw, 102)
        draw_badge(im, lead['badge'], RED if i != 1 else '#2B5B84')
        canvas.paste(im, (lx, 170))
        d.rectangle((lx, 170, lx + lw - 1, 271), outline=RULE, width=1)
        d.text((lx, 276), lead['kicker'], font=font('narrow_bold', 9), fill=RED, anchor='lt')
        ty = 289
        for tl in wrap_lines(d, lead['title'], font('georgia_bold', 12), lw)[:2]:
            d.text((lx, ty), tl, font=font('georgia_bold', 12), fill=INK, anchor='lt')
            ty += 14
        for bl in wrap_lines(d, lead['body'], font('sans', 9), lw)[:2]:
            d.text((lx, ty + 2), bl, font=font('sans', 9), fill=SUBTLE, anchor='lt')
            ty += 11
    d.line((mx, 355, W - mx, 355), fill=RULE, width=1)

    # 5. Middle 10 Illustrated Cards (2 rows x 5 cols, y = 362..646)
    cw = (iw - 4 * 10) // 5  # 188
    for idx, c in enumerate(data['cards']):
        row, col = divmod(idx, 5)
        cx = mx + col * (cw + 10)
        cy = 362 + row * 144
        im = draw_art(c['art'], cw, 64)
        draw_badge(im, c['badge'], '#1D2A38' if row == 1 else RED)
        canvas.paste(im, (cx, cy))
        d.rectangle((cx, cy, cx + cw - 1, cy + 63), outline=RULE, width=1)
        d.text((cx, cy + 68), c['kicker'], font=font('narrow_bold', 8), fill=RED, anchor='lt')
        ty = cy + 80
        for tl in wrap_lines(d, c['title'], font('georgia_bold', 10), cw)[:2]:
            d.text((cx, ty), tl, font=font('georgia_bold', 10), fill=INK, anchor='lt')
            ty += 12
        for sl in wrap_lines(d, c['sub'], font('sans', 8), cw)[:2]:
            d.text((cx, ty + 2), sl, font=font('sans', 8), fill=MUTED, anchor='lt')
            ty += 10
    d.line((mx, 650, W - mx, 650), fill=INK, width=2)

    # 6. Bottom 2-Zone: Left World Map + Right 17 Briefs + DATE CHECK (y = 658..994)
    map_w = 340
    d.text((mx, 658), 'WHERE IT HAPPENED · NUMBERED AS THE STORIES', font=font('narrow_bold', 10), fill=INK, anchor='lt')
    draw_world_map(canvas, mx, 675, map_w, 250, data['pins'])
    # Legend under map
    leg_y = 934
    lx_cur = mx
    for rname, rcol in REGION_COLORS.items():
        d.ellipse((lx_cur, leg_y + 2, lx_cur + 7, leg_y + 9), fill=rcol)
        d.text((lx_cur + 10, leg_y), rname.title(), font=font('sans', 8), fill=MUTED, anchor='lt')
        lx_cur += round(d.textlength(rname.title(), font=font('sans', 8)) + 18)
        if lx_cur > mx + map_w - 40:
            lx_cur = mx
            leg_y += 14

    # Right side: 17 briefs in 2 sub-columns + DATE CHECK box
    bx = mx + map_w + 18
    bw = W - mx - bx  # 622
    d.text((bx, 658), 'ALSO ON SUNDAY 22 NOVEMBER · 17 MORE STORIES', font=font('narrow_bold', 10), fill=RED, anchor='lt')
    d.line((bx, 672, W - mx, 672), fill=RULE, width=1)

    sub_w = (bw - 16) // 2
    for idx, (bid, bloc, btxt) in enumerate(data['briefs']):
        col = 0 if idx < 9 else 1
        row = idx if idx < 9 else idx - 9
        sx = bx + col * (sub_w + 16)
        sy = 678 + row * 28
        d.text((sx, sy), bid, font=font('narrow_bold', 9), fill=RED, anchor='lt')
        d.text((sx + 16, sy), bloc, font=font('bold', 9), fill=INK, anchor='lt')
        lw_loc = round(d.textlength(bloc, font=font('bold', 9))) + 20
        lines = wrap_lines(d, btxt, font('sans', 8), sub_w - lw_loc)
        if lines:
            d.text((sx + lw_loc, sy + 1), lines[0], font=font('sans', 8), fill=SUBTLE, anchor='lt')
            if len(lines) > 1:
                d.text((sx + 16, sy + 12), lines[1], font=font('sans', 8), fill=SUBTLE, anchor='lt')

    # DATE CHECK box at bottom right
    dc_y = 934
    d.rectangle((bx, dc_y, W - mx, 990), fill=PANEL_BG, outline=RED, width=1)
    dy = dc_y + 6
    for dl in wrap_lines(d, data['date_check'], font('sans', 8), bw - 14)[:4]:
        d.text((bx + 7, dy), dl, font=font('sans', 8), fill=INK, anchor='lt')
        dy += 12

    # 7. Footer
    d.line((mx, 998, W - mx, 998), fill=RULE, width=1)
    d.text((mx, 1004), 'Every story happened or was first reported on Sunday 22 November 2026 in at least one time zone.', font=font('sans', 8), fill=MUTED, anchor='lt')
    rt_end = 'Sources named beside each story · 01–30'
    d.text((W - mx - d.textlength(rt_end, font=font('sans', 8)), 1004), rt_end, font=font('sans', 8), fill=MUTED, anchor='lt')

    canvas.save(out_path, format='PNG', optimize=True)
    if out_path.stat().st_size > 1048576:
        canvas.save(out_path, format='JPEG', quality=92, subsampling=0, optimize=True)


if __name__ == '__main__':
    base = Path(__file__).resolve().parent
    render(base / 'edition-data.json', base / 'entry.png')
    p = base / 'entry.png'
    print(f'Wrote {p} ({p.stat().st_size} bytes)')
