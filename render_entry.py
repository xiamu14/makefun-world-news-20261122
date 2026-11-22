from __future__ import annotations

import functools
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1024, 1024
WHITE = '#FFFFFF'
INK = '#111111'
SUBTLE = '#222222'
MUTED = '#525252'
RED = '#AF242A'
RULE = '#D6D5D1'
PANEL_BG = '#F6F6F4'

FONTS = Path('/System/Library/Fonts/Supplemental')
ASSETS = Path('/Users/ben/Workspace/Project/make-fun/world-news-2026-11-22')

REGION_PIN_COLORS = {
    'MIDDLE EAST': '#AF242A',
    'EUROPE': '#1F2933',
    'ASIA': '#7C2D12',
    'AFRICA': '#3E4C59',
    'AMERICAS': '#8B1E24',
    'OCEANIA': '#334E68',
    'GLOBAL': '#111111',
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


def draw_brace(draw: ImageDraw.ImageDraw, x: int, y1: int, y2: int, side: str = 'left', color: str = '#888888') -> None:
    mid = (y1 + y2) / 2
    dx = -6 if side == 'left' else 6
    pts = [(x - dx * 0.4, y1), (x, y1 + 4), (x, mid - 4), (x + dx, mid), (x, mid + 4), (x, y2 - 4), (x - dx * 0.4, y2)]
    draw.line(pts, fill=color, width=1)


def draw_section_header_arrow(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, label: str) -> None:
    cx = x + w // 2
    f = font('narrow_bold', 11)
    lw = draw.textlength(label, font=f) + 14
    draw.line((x, y + 6, round(cx - lw / 2), y + 6), fill=RED, width=1)
    draw.line((round(cx + lw / 2), y + 6, x + w, y + 6), fill=RED, width=1)
    draw_centered(draw, cx, y, label, f, RED)
    draw_centered(draw, cx, y + 11, '↓', font('bold', 10), RED)


def load_photo(name: str, w: int, h: int) -> Image.Image:
    if name == 'tehran':
        im = Image.open(ASSETS / 'lead-illustration/tehran-dusk.png').convert('RGB')
        iw, ih = im.size
        im = im.crop((0, int(ih * 0.12), iw, int(ih * 0.88)))
    elif name == 'cop31':
        im = Image.open(ASSETS / 'expanded-english/illustrations/finance-climate.png').convert('RGB')
        iw, ih = im.size
        im = im.crop((0, int(ih * 0.52), iw, int(ih * 0.96)))
    else:
        sheet = Image.open(ASSETS / 'illustration-assets/editorial-contact-sheet.png').convert('RGB')
        sw, sh = sheet.size
        cw, ch = sw // 2, sh // 3
        im = sheet.crop((4, 2 * ch + 4, cw - 4, sh - 4))
    return ImageOps.fit(im, (w, h), method=Image.Resampling.LANCZOS)


def build_card_art(kind: str, w: int, h: int) -> Image.Image:
    if kind == 'hormuz_scene':
        im = load_photo('hormuz', w, h)
        d = ImageDraw.Draw(im)
        d.text((w - 38, 8), 'IRAN', font=font('narrow_bold', 9), fill='#111111', anchor='lt')
        d.polygon([(36, h - 30), (114, h - 30), (108, h - 20), (42, h - 20)], fill='#111111')
        d.rectangle((90, h - 40, 102, h - 30), fill='#FFFFFF')
        d.ellipse((34, h - 36, 46, h - 24), fill=RED)
        d.polygon([(176, h - 24), (258, h - 24), (252, h - 14), (182, h - 14)], fill='#111111')
        d.rectangle((234, h - 34, 246, h - 24), fill='#FFFFFF')
        d.ellipse((228, h - 30, 240, h - 18), fill=RED)
        return im

    if kind == 'cop31_scene':
        im = load_photo('cop31', w, h)
        d = ImageDraw.Draw(im)
        cx, cy = w - 74, 52
        d.ellipse((cx - 13, cy - 13, cx + 13, cy + 13), fill='#FFFFFF', outline='#111111', width=2)
        d.line((cx, cy, cx, cy - 8), fill='#111111', width=2)
        d.line((cx, cy, cx, cy + 7), fill=RED, width=2)
        d.rectangle((w - 46, 36, w - 10, 74), fill='#FFFFFF', outline='#111111', width=1)
        d.text((w - 41, 43), 'NEW', font=font('narrow_bold', 9), fill=RED, anchor='lt')
        d.text((w - 42, 54), 'TEXT', font=font('narrow_bold', 9), fill=INK, anchor='lt')
        return im

    if kind == 'iran_power':
        im = load_photo('tehran', w, h)
        d = ImageDraw.Draw(im)
        d.ellipse((w - 50, 22, w - 16, 56), fill=RED, outline='#FFFFFF', width=2)
        draw_centered(d, w - 33, 30, '2h', font('georgia_bold', 14), '#FFFFFF')
        return im

    im = Image.new('RGB', (w, h), '#EAEAE6')
    d = ImageDraw.Draw(im)

    if kind == 'baltic_ship':
        d.rectangle((0, 0, w, int(h * 0.54)), fill='#EAEAE6')
        d.rectangle((0, int(h * 0.54), w, h), fill='#2B3036')
        d.polygon([(240, int(h * 0.44)), (w, int(h * 0.40)), (w, int(h * 0.54)), (230, int(h * 0.54))], fill='#C8C7C2')
        d.text((250, int(h * 0.42)), 'GOGLAND', font=font('narrow_bold', 8), fill='#333333', anchor='lt')
        d.polygon([(62, 68), (234, 68), (220, 84), (76, 84)], fill='#111111')
        d.rectangle((86, 52, 124, 68), fill='#FFFFFF', outline='#111111')
        d.rectangle((130, 58, 172, 68), fill='#555555')
        for sx, sy, sr, scol in [(176, 46, 13, '#444444'), (192, 34, 17, '#585858'), (212, 22, 19, '#707070')]:
            d.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=scol)
        d.polygon([(154, 68), (167, 42), (180, 68)], fill=RED)

    elif kind == 'bahrain_fire':
        d.rectangle((0, 0, w, h), fill='#EFEFE9')
        d.rectangle((0, int(h * 0.72), w, h), fill='#D0CFC9')
        d.rectangle((26, 40, 64, int(h * 0.72)), fill='#FFFFFF', outline='#111111')
        d.rectangle((70, 32, 98, int(h * 0.72)), fill='#444444')
        d.polygon([(88, int(h * 0.72)), (112, 18), (134, int(h * 0.72))], fill=RED)
        for sx, sy, sr in [(122, 24, 12), (138, 18, 14)]:
            d.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill='#333333')

    elif kind == 'nato_poland':
        d.rectangle((0, 0, w, h), fill='#F2F2EE')
        cx = w // 2
        d.polygon([(cx - 32, 18), (cx + 32, 18), (cx + 28, 62), (cx, 80), (cx - 28, 62)], fill='#111111')
        d.rectangle((cx - 22, 26, cx + 22, 42), fill='#FFFFFF')
        d.rectangle((cx - 22, 42, cx + 22, 58), fill=RED)
        d.polygon([(cx, 24), (cx + 5, 42), (cx, 60), (cx - 5, 42)], fill='#111111')

    elif kind == 'drone_wave':
        d.rectangle((0, 0, w, h), fill='#1A1D20')
        for r in (20, 38, 56):
            d.arc((w // 2 - r, 72 - r, w // 2 + r, 72 + r), 195, 345, fill='#777777', width=1)
        for dx, dy in [(36, 40), (88, 30), (120, 46)]:
            d.polygon([(dx, dy), (dx + 20, dy + 7), (dx + 5, dy + 15)], fill=RED)

    elif kind == 'gaza_van':
        d.rectangle((0, 0, w, h), fill='#EFEFE9')
        d.rectangle((0, 52, w, h), fill='#C8C7C0')
        d.rectangle((66, 30, 152, 54), fill='#FFFFFF', outline='#111111', width=1)
        d.rectangle((136, 34, 150, 44), fill='#DDDDDD', outline='#111111')
        d.line((88, 36, 88, 48), fill=RED, width=3)
        d.line((82, 42, 94, 42), fill=RED, width=3)
        d.ellipse((74, 50, 88, 64), fill='#111111')
        d.ellipse((128, 50, 142, 64), fill='#111111')
        d.polygon([(112, 30), (128, 10), (142, 30)], fill=RED)

    elif kind == 'mexico_cartel':
        d.rectangle((0, 0, w, h), fill='#F2F2EE')
        d.polygon([(145, 10), (220, 18), (226, 58), (160, 62)], fill='#DDDDD6', outline='#999999')
        d.text((164, 22), 'SINALOA', font=font('narrow_bold', 9), fill=RED, anchor='lt')
        d.ellipse((42, 26, 80, 64), outline='#111111', width=4)
        d.ellipse((104, 26, 142, 64), outline='#111111', width=4)
        d.rectangle((78, 40, 106, 50), fill=RED, outline='#111111')

    elif kind == 'fbi_cyber':
        d.rectangle((0, 0, w, h), fill='#181A1D')
        d.rectangle((22, 24, 96, 62), fill='#282C30', outline='#666666')
        for ry in (30, 40, 50):
            d.ellipse((28, ry, 34, ry + 6), fill='#FFFFFF')
            d.ellipse((40, ry, 46, ry + 6), fill=RED)
            d.line((54, ry + 3, 86, ry + 3), fill='#888888', width=2)
        d.rectangle((146, 36, 180, 60), fill=RED, outline='#FFFFFF')
        d.arc((152, 18, 174, 44), 180, 330, fill='#FFFFFF', width=3)

    elif kind == 'sudan_mine':
        d.rectangle((0, 0, w, h), fill='#F0EFEA')
        d.rectangle((0, 52, w, h), fill='#CDCBC4')
        d.polygon([(54, 30), (108, 30), (118, 44), (104, 54), (54, 54)], fill='#222222')
        d.rectangle((64, 34, 88, 44), fill='#FFFFFF')
        d.ellipse((60, 48, 74, 62), fill='#111111')
        d.ellipse((98, 48, 112, 62), fill='#111111')
        d.polygon([(164, 18), (188, 56), (140, 56)], fill='#FFFFFF', outline=RED, width=2)
        d.text((161, 29), '!', font=font('bold', 18), fill=RED, anchor='lt')

    return im


def paste_circle_medallion(canvas: Image.Image, im: Image.Image, cx: int, cy: int, diameter: int) -> None:
    sq = ImageOps.fit(im, (diameter, diameter), method=Image.Resampling.LANCZOS)
    mask = Image.new('L', (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter - 1, diameter - 1), fill=255)
    canvas.paste(sq, (cx - diameter // 2, cy - diameter // 2), mask)
    d = ImageDraw.Draw(canvas)
    d.ellipse((cx - diameter // 2, cy - diameter // 2, cx + diameter // 2 - 1, cy + diameter // 2 - 1), outline=INK, width=1)


def draw_badge(im: Image.Image, text: str, bg: str = RED) -> None:
    d = ImageDraw.Draw(im)
    f = font('narrow_bold', 10)
    tw = d.textlength(text, font=f)
    d.rectangle((5, 5, round(tw + 15), 21), fill=bg)
    d.text((10, 7), text, font=f, fill='#FFFFFF', anchor='lt')


def draw_sub_pill(d: ImageDraw.ImageDraw, x: int, y: int, text: str) -> None:
    f = font('bold', 9)
    tw = round(d.textlength(text, font=f))
    d.rectangle((x, y, x + tw + 12, y + 16), fill='#FFFFFF', outline='#111111', width=1)
    d.text((x + 6, y + 3), text, font=f, fill='#111111', anchor='lt')


def draw_src_pill(d: ImageDraw.ImageDraw, w: int, h: int, text: str) -> None:
    f = font('narrow_bold', 8)
    tw = round(d.textlength(text, font=f))
    x1 = w - tw - 12
    y1 = h - 15
    d.rectangle((x1, y1, w - 3, h - 3), fill='#111111')
    d.text((x1 + 5, y1 + 2), text, font=f, fill='#FFFFFF', anchor='lt')


def draw_world_map(canvas: Image.Image, x0: int, y0: int, mw: int, mh: int, pins: list[dict]) -> None:
    d = ImageDraw.Draw(canvas)
    d.rectangle((x0, y0, x0 + mw, y0 + mh), fill=PANEL_BG, outline=RULE, width=1)

    def proj(lon: float, lat: float) -> tuple[int, int]:
        px = x0 + round(((lon + 180.0) / 360.0) * mw)
        py = y0 + round(((82.0 - lat) / 142.0) * mh)
        return px, py

    continents = [
        [(-165, 65), (-130, 70), (-80, 62), (-55, 50), (-75, 28), (-100, 16), (-122, 36)],
        [(-80, 11), (-50, 5), (-35, -8), (-54, -36), (-70, -52), (-80, -15)],
        [(-10, 36), (0, 50), (15, 58), (35, 68), (55, 65), (50, 45), (30, 38), (5, 36)],
        [(-16, 35), (10, 37), (34, 31), (50, 12), (40, -10), (28, -34), (15, -30), (10, 5), (-16, 15)],
        [(35, 38), (60, 38), (75, 20), (105, 10), (122, 24), (142, 44), (165, 64), (100, 72), (55, 68)],
        [(114, -22), (145, -12), (153, -28), (138, -38), (115, -34)],
    ]
    for poly in continents:
        d.polygon([proj(lo, la) for lo, la in poly], fill='#DEDCD6', outline='#BDBAB2')

    f_pin = font('narrow_bold', 8)
    for p in pins:
        px, py = proj(p['lon'], p['lat'])
        px = max(x0 + 8, min(x0 + mw - 8, px))
        py = max(y0 + 8, min(y0 + mh - 8, py))
        col = REGION_PIN_COLORS.get(p['r'], INK)
        d.ellipse((px - 6, py - 6, px + 6, py + 6), fill=col, outline='#FFFFFF')
        draw_centered(d, px, py - 5, str(p['id']), f_pin, '#FFFFFF')


def render(data_path: Path, out_path: Path) -> None:
    data = json.loads(data_path.read_text(encoding='utf-8'))
    canvas = Image.new('RGB', (W, H), WHITE)
    d = ImageDraw.Draw(canvas)
    mx = 22
    iw = W - 2 * mx  # 980

    # 1. Masthead with Flanking Braces
    d.text((mx, 6), 'THE WORLD DAILY · DIGITAL EDITION', font=font('narrow_bold', 9), fill=RED, anchor='lt')
    rt = '23 STORIES · 7 REGIONS · SUNDAY 22 NOVEMBER 2026'
    d.text((W - mx - d.textlength(rt, font=font('narrow_bold', 9)), 6), rt, font=font('narrow_bold', 9), fill=MUTED, anchor='lt')

    draw_brace(d, mx + 4, 20, 74, 'left')
    draw_brace(d, mx + 148, 20, 74, 'right')
    draw_centered(d, mx + 76, 23, '23 STORIES · 7 REGIONS', font('narrow_bold', 9), RED)
    draw_centered(d, mx + 76, 36, 'THE WORLD DAILY', font('georgia_bold', 10), INK)
    draw_centered(d, mx + 76, 49, 'EARLY EDITION', font('narrow', 9), MUTED)
    draw_centered(d, mx + 76, 61, 'WORLD DIGEST →', font('narrow_bold', 8), RED)

    draw_centered(d, W // 2, 18, data['masthead'], font('didot', 44, index=2), INK)
    draw_centered(d, W // 2, 68, data['deck'], font('italic', 11), SUBTLE)

    rx = W - mx - 152
    draw_brace(d, rx + 4, 20, 74, 'left')
    draw_brace(d, rx + 148, 20, 74, 'right')
    draw_centered(d, rx + 76, 23, 'EDITION DATE', font('narrow_bold', 9), RED)
    draw_centered(d, rx + 76, 36, '22 NOV 2026', font('georgia_bold', 11), INK)
    draw_centered(d, rx + 76, 50, 'SUNDAY WORLD', font('narrow', 9), MUTED)
    draw_centered(d, rx + 76, 61, 'DATE CHECK →', font('narrow_bold', 8), RED)

    d.line((mx, 86, W - mx, 86), fill=INK, width=2)
    d.line((mx, 89, W - mx, 89), fill=RULE, width=1)

    # 2. 6-Stat Breaking Numbers Strip (y = 93..133)
    sw = iw // 6
    for i, st in enumerate(data['stats']):
        sx = mx + i * sw
        if i > 0:
            d.line((sx, 95, sx, 131), fill=RULE, width=1)
        d.text((sx + 5, 94), st['num'], font=font('didot', 22, index=2), fill=RED if i in (0, 3, 5) else INK, anchor='lt')
        nw = d.textlength(st['num'], font=font('didot', 22, index=2)) + 10
        for li, line in enumerate(st['desc'].split('\n')[:2]):
            d.text((sx + nw, 96 + li * 12), line, font=font('sans', 9), fill=SUBTLE, anchor='lt')

    # 3. Region Bar
    d.rectangle((mx, 136, W - mx, 154), fill=PANEL_BG, outline=RULE, width=1)
    nav_str = 'MIDDLE EAST 6   ·   EUROPE 6   ·   AMERICAS 5   ·   ASIA 3   ·   OCEANIA 1   ·   AFRICA 1   ·   GLOBAL 1'
    draw_centered(d, W // 2, 140, nav_str, font('narrow_bold', 9), INK)

    # 4. Top 3 Lead Cards (y = 160..356)
    lw = (iw - 24) // 3  # 318
    for i, lead in enumerate(data['leads']):
        lx = mx + i * (lw + 12)
        if i > 0:
            d.line((lx - 6, 160, lx - 6, 352), fill=RULE, width=1)
        im = build_card_art(lead['art'], lw, 108)
        draw_badge(im, lead['badge'], RED if i != 1 else INK)
        idraw = ImageDraw.Draw(im)
        draw_sub_pill(idraw, 6, 25, lead['sub_pill'])
        draw_src_pill(idraw, lw, 108, lead['src_pill'])
        canvas.paste(im, (lx, 160))
        d.rectangle((lx, 160, lx + lw - 1, 267), outline=INK, width=1)
        d.text((lx, 272), lead['kicker'], font=font('narrow_bold', 9), fill=RED, anchor='lt')
        ty = 285
        for tl in wrap_lines(d, lead['title'], font('georgia_bold', 13), lw)[:2]:
            d.text((lx, ty), tl, font=font('georgia_bold', 13), fill=INK, anchor='lt')
            ty += 15
        for bl in wrap_lines(d, lead['body'], font('sans', 9), lw)[:3]:
            d.text((lx, ty + 2), bl, font=font('sans', 9), fill=SUBTLE, anchor='lt')
            ty += 11

    # 5. « FEATURED DISPATCHES » Pale-Gray Band with 4 Larger Circular Medallions (y = 368..524)
    feat_top, feat_bot = 368, 524
    d.rectangle((mx, feat_top, W - mx, feat_bot), fill=PANEL_BG, outline=RULE, width=1)
    pill_w = 156
    d.rectangle((W // 2 - pill_w // 2, feat_top - 9, W // 2 + pill_w // 2, feat_top + 9), fill=WHITE, outline=RULE, width=1)
    draw_centered(d, W // 2, feat_top - 6, '«  FEATURED DISPATCHES  »', font('narrow_bold', 10), INK)

    fw = iw // 4
    for idx, c in enumerate(data['featured']):
        fcx = mx + idx * fw + fw // 2
        if idx > 0:
            d.line((mx + idx * fw, feat_top + 14, mx + idx * fw, feat_bot - 10), fill=RULE, width=1)
        cim = build_card_art(c['art'], 160, 160)
        paste_circle_medallion(canvas, cim, fcx, feat_top + 48, 76)
        bw_badge = round(d.textlength(c['badge'], font=font('narrow_bold', 9))) + 12
        d.rectangle((fcx - bw_badge // 2, feat_top + 76, fcx + bw_badge // 2, feat_top + 90), fill=RED)
        draw_centered(d, fcx, feat_top + 78, c['badge'], font('narrow_bold', 9), WHITE)
        draw_centered(d, fcx, feat_top + 94, c['kicker'], font('narrow_bold', 9), MUTED)
        ty = feat_top + 106
        for tl in wrap_lines(d, c['title'], font('georgia_bold', 11), fw - 18)[:2]:
            draw_centered(d, fcx, ty, tl, font('georgia_bold', 11), INK)
            ty += 13
        draw_centered(d, fcx, ty + 2, f"{c['sub']} ({c['src_pill']})", font('sans', 9), SUBTLE)

    # 6. Row of 4 Larger Framed Cards (y = 534..674)
    card_w = (iw - 3 * 12) // 4  # 236
    for idx, c in enumerate(data['cards']):
        cx = mx + idx * (card_w + 12)
        cy = 534
        im = build_card_art(c['art'], card_w, 68)
        draw_badge(im, c['badge'], INK if idx % 2 == 1 else RED)
        idraw = ImageDraw.Draw(im)
        draw_src_pill(idraw, card_w, 68, c['src_pill'])
        canvas.paste(im, (cx, cy))
        d.rectangle((cx, cy, cx + card_w - 1, cy + 67), outline=INK, width=1)
        d.text((cx, cy + 72), c['kicker'], font=font('narrow_bold', 9), fill=RED, anchor='lt')
        ty = cy + 84
        for tl in wrap_lines(d, c['title'], font('georgia_bold', 11), card_w)[:2]:
            d.text((cx, ty), tl, font=font('georgia_bold', 11), fill=INK, anchor='lt')
            ty += 13
        for sl in wrap_lines(d, c['sub'], font('sans', 9), card_w)[:2]:
            d.text((cx, ty + 2), sl, font=font('sans', 9), fill=SUBTLE, anchor='lt')
            ty += 11

    # 7. Bottom 2-Zone Section with Red Top Rules & Downward Arrows ↓ (y = 682..978)
    bot_y = 682
    map_w = 340
    draw_section_header_arrow(d, mx, bot_y, map_w, 'WHERE IT HAPPENED')
    draw_world_map(canvas, mx, bot_y + 24, map_w, 236, data['pins'])
    leg_y = bot_y + 266
    lx_cur = mx
    for rname, rcol in REGION_PIN_COLORS.items():
        d.ellipse((lx_cur, leg_y + 2, lx_cur + 8, leg_y + 10), fill=rcol)
        lbl = rname.title()
        d.text((lx_cur + 11, leg_y), lbl, font=font('bold', 8), fill=INK, anchor='lt')
        lx_cur += round(d.textlength(lbl, font=font('bold', 8)) + 16)

    d.line((mx + map_w + 8, bot_y + 10, mx + map_w + 8, 976), fill=RULE, width=1)

    bx = mx + map_w + 16
    bw = W - mx - bx  # 624
    sub_w = (bw - 16) // 2
    draw_section_header_arrow(d, bx, bot_y, sub_w, 'WORLD & DIPLOMACY')
    draw_section_header_arrow(d, bx + sub_w + 16, bot_y, sub_w, 'GLOBAL DISPATCHES')

    for idx, (bid, bloc, btxt) in enumerate(data['briefs']):
        col = 0 if idx < 6 else 1
        row = idx if idx < 6 else idx - 6
        sx = bx + col * (sub_w + 16)
        sy = bot_y + 26 + row * 33
        d.text((sx, sy), bid, font=font('narrow_bold', 10), fill=RED, anchor='lt')
        d.text((sx + 16, sy), bloc, font=font('georgia_bold', 10), fill=INK, anchor='lt')
        lw_loc = round(d.textlength(bloc, font=font('georgia_bold', 10))) + 21
        lines = wrap_lines(d, btxt, font('sans', 9), sub_w - lw_loc)
        if lines:
            d.text((sx + lw_loc, sy + 1), lines[0], font=font('sans', 9), fill=SUBTLE, anchor='lt')
            if len(lines) > 1:
                d.text((sx + 16, sy + 13), lines[1], font=font('sans', 9), fill=SUBTLE, anchor='lt')
        if row < 5:
            d.line((sx, sy + 28, sx + sub_w, sy + 28), fill=RULE, width=1)

    # Clean, legible 10px DATE CHECK box
    dc_y = 918
    d.rectangle((bx, dc_y, W - mx, 974), fill=PANEL_BG, outline=RULE, width=1)
    d.line((bx, dc_y, W - mx, dc_y), fill=RED, width=2)
    dy = dc_y + 8
    for dl in wrap_lines(d, data['date_check'], font('sans', 10), bw - 16)[:3]:
        d.text((bx + 8, dy), dl, font=font('sans', 10), fill=INK, anchor='lt')
        dy += 14

    # 8. Footer
    d.line((mx, 984, W - mx, 984), fill=INK, width=1)
    d.text((mx, 990), 'THE WORLD DAILY · Sunday 22 November 2026 · Officials\' counts and claims are attributed.', font=font('sans', 9), fill=MUTED, anchor='lt')
    rt_end = '23 Stories · Editorial Edition'
    d.text((W - mx - d.textlength(rt_end, font=font('narrow_bold', 9)), 990), rt_end, font=font('narrow_bold', 9), fill=INK, anchor='lt')

    canvas.save(out_path, format='PNG', optimize=True)
    if out_path.stat().st_size > 1048576:
        canvas.save(out_path, format='JPEG', quality=92, subsampling=0, optimize=True)


if __name__ == '__main__':
    base = Path(__file__).resolve().parent
    render(base / 'edition-data.json', base / 'entry.png')
    p = base / 'entry.png'
    print(f'Wrote {p} ({p.stat().st_size} bytes)')
