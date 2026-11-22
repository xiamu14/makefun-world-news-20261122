from __future__ import annotations

import functools
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1024, 1024
WHITE = '#FFFFFF'
INK = '#111111'
SUBTLE = '#2B2B2B'
MUTED = '#5A5A5A'
RED = '#AF242A'
RULE = '#D6D5D1'
PANEL_BG = '#F6F6F4'
SLATE = '#222831'

FONTS = Path('/System/Library/Fonts/Supplemental')
ASSETS = Path('/Users/ben/Workspace/Project/make-fun/world-news-2026-11-22')

# Restrained editorial pin palette (scarlet, charcoal, slate, deep sepia) following style.md
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
    pts = [
        (x - dx * 0.4, y1),
        (x, y1 + 4),
        (x, mid - 4),
        (x + dx, mid),
        (x, mid + 4),
        (x, y2 - 4),
        (x - dx * 0.4, y2),
    ]
    draw.line(pts, fill=color, width=1)


def draw_wavy_rule(draw: ImageDraw.ImageDraw, x1: int, x2: int, y: int, color: str = RULE) -> None:
    pts = []
    for x in range(x1, x2 + 1, 2):
        pts.append((x, y + math.sin((x - x1) * 0.45) * 1.4))
    if len(pts) > 1:
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
    elif name == 'wallstreet_bw':
        im = Image.open(ASSETS / 'expanded-english/illustrations/finance-climate.png').convert('RGB')
        iw, ih = im.size
        im = im.crop((0, int(ih * 0.04), iw, int(ih * 0.48)))
    else:
        sheet = Image.open(ASSETS / 'illustration-assets/editorial-contact-sheet.png').convert('RGB')
        sw, sh = sheet.size
        cw, ch = sw // 2, sh // 3
        coords = {'hormuz': (0, 2), 'tennis': (1, 2), 'nigeria': (1, 0), 'brazil': (0, 1), 'wolbachia': (1, 1)}
        gx, gy = coords[name]
        im = sheet.crop((gx * cw + 4, gy * ch + 4, (gx + 1) * cw - 4, (gy + 1) * ch - 4))
    return ImageOps.fit(im, (w, h), method=Image.Resampling.LANCZOS)


def build_card_art(kind: str, w: int, h: int) -> Image.Image:
    # Combine real editorial photography with monochrome/scarlet magazine overlays (style.md)
    if kind == 'hormuz_scene':
        im = load_photo('hormuz', w, h)
        d = ImageDraw.Draw(im)
        # Overlay subtle silhouette of two tankers + mine + IRAN coast tag
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
        # Editorial clock + NEW TEXT sheet overlay
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
        d.ellipse((w - 46, 18, w - 16, 48), fill=RED, outline='#FFFFFF', width=1)
        draw_centered(d, w - 31, 25, '2h', font('georgia_bold', 12), '#FFFFFF')
        return im

    # High-contrast editorial monochrome + scarlet illustrations (style.md palette: white, pale gray, deep black, scarlet)
    im = Image.new('RGB', (w, h), '#EAEAE6')
    d = ImageDraw.Draw(im)

    if kind == 'baltic_ship':
        # Monochrome seascape + black ship hull + scarlet flame accent + dark smoke plumes
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
        d.rectangle((22, 32, 54, int(h * 0.72)), fill='#FFFFFF', outline='#111111')
        d.rectangle((60, 26, 86, int(h * 0.72)), fill='#444444')
        d.polygon([(78, int(h * 0.72)), (100, 14), (120, int(h * 0.72))], fill=RED)
        for sx, sy, sr in [(110, 18, 11), (126, 12, 14), (144, 9, 11)]:
            d.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill='#333333')

    elif kind == 'nato_poland':
        d.rectangle((0, 0, w, h), fill='#F2F2EE')
        cx = w // 2
        d.polygon([(cx - 26, 14), (cx + 26, 14), (cx + 22, 48), (cx, 62), (cx - 22, 48)], fill='#111111')
        d.rectangle((cx - 18, 20, cx + 18, 33), fill='#FFFFFF')
        d.rectangle((cx - 18, 33, cx + 18, 46), fill=RED)
        d.polygon([(cx, 18), (cx + 4, 33), (cx, 48), (cx - 4, 33)], fill='#111111')
        d.polygon([(cx - 14, 33), (cx, 29), (cx + 14, 33), (cx, 37)], fill='#111111')

    elif kind == 'drone_wave':
        d.rectangle((0, 0, w, h), fill='#1A1D20')
        for r in (16, 30, 44):
            d.arc((w // 2 - r, 54 - r, w // 2 + r, 54 + r), 195, 345, fill='#777777', width=1)
        for dx, dy in [(32, 30), (80, 22), (128, 34)]:
            d.polygon([(dx, dy), (dx + 18, dy + 6), (dx + 4, dy + 13)], fill=RED)
            d.line((dx - 10, dy - 2, dx, dy + 3), fill='#FFFFFF', width=1)

    elif kind == 'gaza_van':
        d.rectangle((0, 0, w, h), fill='#EFEFE9')
        d.rectangle((0, 48, w, h), fill='#C8C7C0')
        d.rectangle((50, 28, 122, 50), fill='#FFFFFF', outline='#111111', width=1)
        d.rectangle((108, 32, 120, 41), fill='#DDDDDD', outline='#111111')
        d.line((68, 34, 68, 44), fill=RED, width=3)
        d.line((63, 39, 73, 39), fill=RED, width=3)
        d.ellipse((58, 46, 70, 58), fill='#111111')
        d.ellipse((102, 46, 114, 58), fill='#111111')
        d.polygon([(88, 28), (102, 10), (114, 28)], fill=RED)

    elif kind == 'mexico_cartel':
        d.rectangle((0, 0, w, h), fill='#F2F2EE')
        d.polygon([(115, 8), (175, 16), (182, 52), (128, 56)], fill='#DDDDD6', outline='#999999')
        d.text((130, 18), 'SINALOA', font=font('narrow_bold', 8), fill=RED, anchor='lt')
        d.ellipse((32, 24, 66, 58), outline='#111111', width=4)
        d.ellipse((86, 24, 120, 58), outline='#111111', width=4)
        d.rectangle((64, 37, 88, 45), fill=RED, outline='#111111')

    elif kind == 'fbi_cyber':
        d.rectangle((0, 0, w, h), fill='#181A1D')
        d.rectangle((14, 22, 78, 56), fill='#282C30', outline='#666666')
        for ry in (28, 37, 46):
            d.ellipse((20, ry, 25, ry + 5), fill='#FFFFFF')
            d.ellipse((30, ry, 35, ry + 5), fill=RED)
            d.line((42, ry + 2, 70, ry + 2), fill='#888888', width=2)
        d.text((82, 46), '010011', font=font('narrow_bold', 8), fill='#CCCCCC', anchor='lt')
        d.rectangle((114, 34, 142, 54), fill=RED, outline='#FFFFFF')
        d.arc((118, 18, 138, 42), 180, 330, fill='#FFFFFF', width=3)

    elif kind == 'sudan_mine':
        d.rectangle((0, 0, w, h), fill='#F0EFEA')
        d.rectangle((0, 48, w, h), fill='#CDCBC4')
        d.polygon([(46, 28), (92, 28), (100, 40), (90, 48), (46, 48)], fill='#222222')
        d.rectangle((54, 32, 74, 41), fill='#FFFFFF')
        d.ellipse((50, 44, 62, 56), fill='#111111')
        d.ellipse((82, 44, 94, 56), fill='#111111')
        d.polygon([(128, 18), (148, 50), (108, 50)], fill='#FFFFFF', outline=RED, width=2)
        d.text((126, 27), '!', font=font('bold', 16), fill=RED, anchor='lt')

    elif kind == 'belgium_strike':
        d.rectangle((0, 0, w, h), fill='#EFEFE9')
        d.rectangle((0, 48, w, h), fill='#333333')
        d.rectangle((40, 22, 50, 48), fill='#666666')
        d.polygon([(32, 14), (58, 14), (52, 22), (38, 22)], fill='#111111')
        d.polygon([(92, 44), (154, 44), (166, 34), (150, 34), (142, 40), (100, 40)], fill='#FFFFFF', outline='#111111')
        d.rectangle((110, 14, 166, 29), fill=RED)
        draw_centered(d, 138, 17, 'STRIKE', font('narrow_bold', 10), '#FFFFFF')

    elif kind == 'f1_vegas':
        d.rectangle((0, 0, w, h), fill='#141619')
        d.rectangle((0, 48, w, h), fill='#2A2D32')
        for bx, bh, bcol in [(126, 20, '#888888'), (142, 32, RED), (158, 26, '#BBBBBB')]:
            d.rectangle((bx, 48 - bh, bx + 11, 48), fill=bcol)
        d.text((90, 18), 'P1', font=font('didot', 18, index=2), fill='#FFFFFF', anchor='lt')
        d.polygon([(22, 46), (82, 46), (76, 39), (42, 39), (28, 34), (22, 40)], fill='#FFFFFF')
        d.ellipse((30, 42, 42, 54), fill='#111111', outline='#FFFFFF')
        d.ellipse((64, 42, 76, 54), fill='#111111', outline='#FFFFFF')

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
    d.rectangle((5, 5, round(tw + 15), 20), fill=bg)
    d.text((10, 7), text, font=f, fill='#FFFFFF', anchor='lt')


def draw_sub_pill(d: ImageDraw.ImageDraw, x: int, y: int, text: str) -> None:
    f = font('bold', 9)
    tw = round(d.textlength(text, font=f))
    d.rectangle((x, y, x + tw + 12, y + 15), fill='#FFFFFF', outline='#111111', width=1)
    d.text((x + 6, y + 2), text, font=f, fill='#111111', anchor='lt')


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
    mx = 20
    iw = W - 2 * mx  # 984

    # 1. Vanity Fair / style.md Masthead with Flanking Editorial Braces & Didone Serif
    d.text((mx, 6), 'THE WORLD DAILY · DIGITAL EDITION', font=font('narrow_bold', 9), fill=RED, anchor='lt')
    rt = '30 STORIES · 7 REGIONS · CONTEST DAY: SUNDAY 22 NOVEMBER 2026'
    d.text((W - mx - d.textlength(rt, font=font('narrow_bold', 9)), 6), rt, font=font('narrow_bold', 9), fill=MUTED, anchor='lt')

    draw_brace(d, mx + 4, 20, 74, 'left')
    draw_brace(d, mx + 148, 20, 74, 'right')
    draw_centered(d, mx + 76, 23, '30 STORIES · 7 REGIONS', font('narrow_bold', 9), RED)
    draw_centered(d, mx + 76, 36, 'THE WORLD DAILY', font('georgia_bold', 10), INK)
    draw_centered(d, mx + 76, 49, 'EARLY EDITION', font('narrow', 9), MUTED)
    draw_centered(d, mx + 76, 61, 'WORLD DIGEST →', font('narrow_bold', 8), RED)

    draw_centered(d, W // 2, 18, 'SUNDAY 22 NOVEMBER 2026', font('didot', 44, index=2), INK)
    draw_centered(d, W // 2, 68, data['deck'], font('italic', 11), SUBTLE)

    rx = W - mx - 152
    draw_brace(d, rx + 4, 20, 74, 'left')
    draw_brace(d, rx + 148, 20, 74, 'right')
    draw_centered(d, rx + 76, 23, 'CONTEST DATE LOCK', font('narrow_bold', 9), RED)
    draw_centered(d, rx + 76, 36, '22 NOV 2026 ONLY', font('georgia_bold', 10), INK)
    draw_centered(d, rx + 76, 49, 'NOT 13 NOV BASELINE', font('narrow', 9), MUTED)
    draw_centered(d, rx + 76, 61, 'DATE CHECK →', font('narrow_bold', 8), RED)

    # Double rule under masthead (style.md)
    d.line((mx, 86, W - mx, 86), fill=INK, width=2)
    d.line((mx, 89, W - mx, 89), fill=RULE, width=1)

    # 2. 6-Stat Breaking Numbers Strip (y = 93..133) with delicate vertical rules & scarlet markers
    sw = iw // 6
    for i, st in enumerate(data['stats']):
        sx = mx + i * sw
        if i > 0:
            d.line((sx, 95, sx, 131), fill=RULE, width=1)
        d.text((sx + 5, 94), st['num'], font=font('didot', 21, index=2), fill=RED if i in (0, 3, 5) else INK, anchor='lt')
        nw = d.textlength(st['num'], font=font('didot', 21, index=2)) + 10
        for li, line in enumerate(st['desc'].split('\n')[:2]):
            d.text((sx + nw, 96 + li * 11), line, font=font('sans', 8), fill=SUBTLE, anchor='lt')

    # 3. Editorial Region Navigation Bar (style.md pale gray + black/scarlet typography + arrows)
    d.rectangle((mx, 136, W - mx, 154), fill=PANEL_BG, outline=RULE, width=1)
    nav_str = 'MIDDLE EAST 7   ·   EUROPE 6   ·   ASIA 5   ·   AMERICAS 5   ·   AFRICA 3   ·   OCEANIA 2   ·   GLOBAL 2'
    draw_centered(d, W // 2, 140, nav_str, font('narrow_bold', 9), INK)

    # 4. Top 3 Lead Photo-Editorial Cards (y = 160..356)
    lw = (iw - 24) // 3  # 320
    for i, lead in enumerate(data['leads']):
        lx = mx + i * (lw + 12)
        if i > 0:
            d.line((lx - 6, 160, lx - 6, 352), fill=RULE, width=1)
        im = build_card_art(lead['art'], lw, 108)
        draw_badge(im, lead['badge'], RED if i != 1 else INK)
        idraw = ImageDraw.Draw(im)
        draw_sub_pill(idraw, 6, 24, lead['sub_pill'])
        draw_src_pill(idraw, lw, 108, lead['src_pill'])
        canvas.paste(im, (lx, 160))
        d.rectangle((lx, 160, lx + lw - 1, 267), outline=INK, width=1)
        d.text((lx, 272), lead['kicker'], font=font('narrow_bold', 9), fill=RED, anchor='lt')
        ty = 284
        for tl in wrap_lines(d, lead['title'], font('georgia_bold', 12), lw)[:2]:
            d.text((lx, ty), tl, font=font('georgia_bold', 12), fill=INK, anchor='lt')
            ty += 14
        for bl in wrap_lines(d, lead['body'], font('sans', 9), lw)[:3]:
            d.text((lx, ty + 2), bl, font=font('sans', 9), fill=SUBTLE, anchor='lt')
            ty += 11

    # 5. Vanity Fair « FEATURED » Pale-Gray Band with 5 Circular Medallions (Stories 4–8, y = 366..512)
    feat_top, feat_bot = 368, 512
    d.rectangle((mx, feat_top, W - mx, feat_bot), fill=PANEL_BG, outline=RULE, width=1)
    pill_w = 152
    d.rectangle((W // 2 - pill_w // 2, feat_top - 9, W // 2 + pill_w // 2, feat_top + 9), fill=WHITE, outline=RULE, width=1)
    draw_centered(d, W // 2, feat_top - 6, '«  FEATURED DISPATCHES  »', font('narrow_bold', 10), INK)

    cw = iw // 5
    for idx, c in enumerate(data['cards'][:5]):
        fcx = mx + idx * cw + cw // 2
        if idx > 0:
            d.line((mx + idx * cw, feat_top + 14, mx + idx * cw, feat_bot - 10), fill=RULE, width=1)
        cim = build_card_art(c['art'], 120, 120)
        paste_circle_medallion(canvas, cim, fcx, feat_top + 44, 62)
        # Scarlet badge pill overlapping bottom of medallion
        bw_badge = round(d.textlength(c['badge'], font=font('narrow_bold', 8))) + 10
        d.rectangle((fcx - bw_badge // 2, feat_top + 68, fcx + bw_badge // 2, feat_top + 80), fill=RED)
        draw_centered(d, fcx, feat_top + 70, c['badge'], font('narrow_bold', 8), WHITE)
        draw_centered(d, fcx, feat_top + 84, c['kicker'], font('narrow_bold', 8), MUTED)
        ty = feat_top + 95
        for tl in wrap_lines(d, c['title'], font('georgia_bold', 10), cw - 14)[:2]:
            draw_centered(d, fcx, ty, tl, font('georgia_bold', 10), INK)
            ty += 12
        for sl in wrap_lines(d, c['sub'], font('sans', 8), cw - 12)[:2]:
            draw_centered(d, fcx, ty + 1, sl, font('sans', 8), SUBTLE)
            ty += 10

    # 6. Row of 5 Framed Editorial Cards (Stories 9–13, y = 520..658)
    card_w = (iw - 4 * 10) // 5  # 188
    for idx, c in enumerate(data['cards'][5:]):
        cx = mx + idx * (card_w + 10)
        cy = 520
        im = build_card_art(c['art'], card_w, 60)
        draw_badge(im, c['badge'], INK if idx % 2 == 1 else RED)
        idraw = ImageDraw.Draw(im)
        draw_src_pill(idraw, card_w, 60, c['src_pill'])
        canvas.paste(im, (cx, cy))
        d.rectangle((cx, cy, cx + card_w - 1, cy + 59), outline=INK, width=1)
        d.text((cx, cy + 64), c['kicker'], font=font('narrow_bold', 8), fill=RED, anchor='lt')
        ty = cy + 75
        for tl in wrap_lines(d, c['title'], font('georgia_bold', 10), card_w)[:2]:
            d.text((cx, ty), tl, font=font('georgia_bold', 10), fill=INK, anchor='lt')
            ty += 12
        for sl in wrap_lines(d, c['sub'], font('sans', 8), card_w)[:2]:
            d.text((cx, ty + 1), sl, font=font('sans', 8), fill=SUBTLE, anchor='lt')
            ty += 10

    # 7. Bottom 3-Column Magazine Section with Red Top Rules & Downward Arrows ↓ (y = 666..982)
    bot_y = 666
    map_w = 338
    draw_section_header_arrow(d, mx, bot_y, map_w, 'WHERE IT HAPPENED · 01–30')
    draw_world_map(canvas, mx, bot_y + 24, map_w, 250, data['pins'])
    leg_y = bot_y + 280
    lx_cur = mx
    for rname, rcol in REGION_PIN_COLORS.items():
        d.ellipse((lx_cur, leg_y + 2, lx_cur + 8, leg_y + 10), fill=rcol)
        lbl = rname.title()
        d.text((lx_cur + 11, leg_y), lbl, font=font('bold', 8), fill=INK, anchor='lt')
        lx_cur += round(d.textlength(lbl, font=font('bold', 8)) + 16)

    # Vertical rule between Map and Briefs
    d.line((mx + map_w + 8, bot_y + 10, mx + map_w + 8, 978), fill=RULE, width=1)

    bx = mx + map_w + 16
    bw = W - mx - bx  # 630
    sub_w = (bw - 14) // 2
    draw_section_header_arrow(d, bx, bot_y, sub_w, 'WORLD & DIPLOMACY · 14–22')
    draw_section_header_arrow(d, bx + sub_w + 14, bot_y, sub_w, 'SOCIETY, SCIENCE & SPORT · 23–30')

    for idx, (bid, bloc, btxt) in enumerate(data['briefs']):
        col = 0 if idx < 9 else 1
        row = idx if idx < 9 else idx - 9
        sx = bx + col * (sub_w + 14)
        sy = bot_y + 26 + row * 22
        d.text((sx, sy), bid, font=font('narrow_bold', 9), fill=RED, anchor='lt')
        d.text((sx + 15, sy), bloc, font=font('georgia_bold', 9), fill=INK, anchor='lt')
        lw_loc = round(d.textlength(bloc, font=font('georgia_bold', 9))) + 19
        d.text((sx + lw_loc, sy), wrap_lines(d, btxt, font('sans', 8), sub_w - lw_loc)[0], font=font('sans', 8), fill=SUBTLE, anchor='lt')
        if row < 8:
            d.line((sx, sy + 16, sx + sub_w, sy + 16), fill=RULE, width=1)

    # DATE CHECK box in pale gray with scarlet top rule
    dc_y = 894
    d.rectangle((bx, dc_y, W - mx, 974), fill=PANEL_BG, outline=RULE, width=1)
    d.line((bx, dc_y, W - mx, dc_y), fill=RED, width=2)
    dy = dc_y + 6
    for dl in wrap_lines(d, data['date_check'], font('sans', 8), bw - 14)[:5]:
        d.text((bx + 7, dy), dl, font=font('sans', 8), fill=INK, anchor='lt')
        dy += 12

    # 8. Footer
    d.line((mx, 984, W - mx, 984), fill=INK, width=1)
    d.text((mx, 990), 'THE WORLD DAILY · Every story happened or was first reported on Sunday 22 November 2026. Officials\' counts and claims are attributed.', font=font('sans', 8), fill=MUTED, anchor='lt')
    rt_end = '01–30 · Editorial Edition'
    d.text((W - mx - d.textlength(rt_end, font=font('narrow_bold', 8)), 990), rt_end, font=font('narrow_bold', 8), fill=INK, anchor='lt')

    canvas.save(out_path, format='PNG', optimize=True)
    if out_path.stat().st_size > 1048576:
        canvas.save(out_path, format='JPEG', quality=92, subsampling=0, optimize=True)


if __name__ == '__main__':
    base = Path(__file__).resolve().parent
    render(base / 'edition-data.json', base / 'entry.png')
    p = base / 'entry.png'
    print(f'Wrote {p} ({p.stat().st_size} bytes)')
