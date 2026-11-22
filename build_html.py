from __future__ import annotations

import html
import json
from pathlib import Path

REGION_OKLCH = {
    'EUROPE': 'oklch(0.46 0.13 245)',
    'ASIA': 'oklch(0.48 0.12 195)',
    'MIDDLE EAST': 'oklch(0.46 0.15 310)',
    'AFRICA': 'oklch(0.46 0.13 150)',
    'N. AMERICA': 'oklch(0.48 0.18 24)',
    'S. AMERICA': 'oklch(0.50 0.14 70)',
    'OCEANIA': 'oklch(0.46 0.12 170)',
    'GLOBAL': 'oklch(0.24 0.01 260)',
}

SVGS: dict[str, str] = {
    'cop31_scene': """
    <svg viewBox="0 0 318 106" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="318" height="106" fill="oklch(0.96 0.01 85)"/>
      <circle cx="159" cy="48" r="40" fill="none" stroke="oklch(0.88 0.02 220)" stroke-width="1" stroke-dasharray="3 3"/>
      <g transform="translate(14,22)">
        <rect width="74" height="46" rx="2" fill="oklch(0.48 0.21 25)"/>
        <circle cx="28" cy="23" r="11" fill="white"/>
        <circle cx="32" cy="23" r="8.8" fill="oklch(0.48 0.21 25)"/>
        <polygon points="45,23 51,21 47,26 47,20 51,25" fill="white"/>
        <text x="37" y="56" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="8" fill="oklch(0.35 0.02 260)">TÜRKİYE</text>
      </g>
      <g transform="translate(230,22)">
        <rect width="74" height="46" rx="2" fill="oklch(0.34 0.16 258)"/>
        <rect width="32" height="22" fill="oklch(0.30 0.14 258)"/>
        <path d="M0,0 L32,22 M32,0 L0,22" stroke="white" stroke-width="2.8"/>
        <path d="M0,0 L32,22 M32,0 L0,22" stroke="oklch(0.50 0.20 25)" stroke-width="1.1"/>
        <path d="M16,0 V22 M0,11 H32" stroke="white" stroke-width="4.2"/>
        <path d="M16,0 V22 M0,11 H32" stroke="oklch(0.50 0.20 25)" stroke-width="2"/>
        <circle cx="16" cy="34" r="3.8" fill="white"/>
        <circle cx="54" cy="13" r="1.8" fill="white"/><circle cx="62" cy="22" r="1.8" fill="white"/>
        <circle cx="50" cy="29" r="1.8" fill="white"/><circle cx="56" cy="37" r="1.8" fill="white"/>
        <text x="37" y="56" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="8" fill="oklch(0.35 0.02 260)">AUSTRALIA</text>
      </g>
      <g transform="translate(124,18)">
        <rect width="70" height="52" rx="3" fill="white" stroke="oklch(0.46 0.13 245)" stroke-width="1.5"/>
        <polygon points="55,0 70,15 55,15" fill="oklch(0.90 0.03 240)"/>
        <rect x="9" y="9" width="36" height="4" rx="1" fill="oklch(0.46 0.13 245)"/>
        <line x1="9" y1="20" x2="61" y2="20" stroke="oklch(0.65 0.04 250)" stroke-width="2"/>
        <line x1="9" y1="27" x2="61" y2="27" stroke="oklch(0.65 0.04 250)" stroke-width="2"/>
        <line x1="9" y1="34" x2="46" y2="34" stroke="oklch(0.65 0.04 250)" stroke-width="2"/>
        <line x1="9" y1="41" x2="38" y2="41" stroke="oklch(0.65 0.04 250)" stroke-width="2"/>
        <circle cx="55" cy="41" r="6.5" fill="oklch(0.42 0.12 152)"/>
        <polyline points="51.5,41 54,43.5 58.5,38.5" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
      </g>
      <text x="159" y="13" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="10.5" fill="oklch(0.22 0.01 260)">ANTALYA · OVERTIME DRAFT</text>
      <rect x="14" y="80" width="290" height="21" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="159" y="94.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="12.5" fill="white">COP31: FINAL DRAFT TABLED</text>
    </svg>""",
    'ukraine_barrage': """
    <svg viewBox="0 0 318 106" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="318" height="106" fill="oklch(0.18 0.03 255)"/>
      <path d="M180 106 A75 75 0 0 1 310 106" fill="none" stroke="oklch(0.46 0.10 190)" stroke-width="1" stroke-dasharray="3 3"/>
      <g fill="oklch(0.28 0.02 255)">
        <rect x="10" y="64" width="24" height="42"/><rect x="38" y="50" width="28" height="56"/>
        <rect x="70" y="60" width="22" height="46"/><rect x="96" y="44" width="30" height="62"/>
        <rect x="130" y="68" width="24" height="38"/><rect x="248" y="58" width="28" height="48"/>
        <rect x="280" y="66" width="26" height="40"/>
      </g>
      <polygon points="94,76 112,38 130,76" fill="oklch(0.62 0.21 35)"/>
      <polygon points="101,76 112,50 123,76" fill="oklch(0.84 0.18 75)"/>
      <circle cx="116" cy="34" r="11" fill="oklch(0.42 0.01 260)" opacity="0.8"/>
      <polygon points="168,36 190,41 168,46 174,41" fill="oklch(0.80 0.16 75)"/>
      <polygon points="204,24 224,28 204,32 209,28" fill="oklch(0.80 0.16 75)"/>
      <polygon points="234,42 256,47 234,52 240,47" fill="oklch(0.80 0.16 75)"/>
      <line x1="258" y1="84" x2="210" y2="36" stroke="oklch(0.84 0.16 80)" stroke-width="1.3" stroke-dasharray="3 3"/>
      <rect x="8" y="7" width="196" height="22" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="106" y="22" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="12.5" fill="white">UKRAINE: 148 DRONES</text>
      <rect x="210" y="7" width="100" height="22" rx="2" fill="white"/>
      <text x="260" y="22" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="11.5" fill="oklch(0.18 0.01 260)">3 MISSILES</text>
    </svg>""",
    'hormuz_scene': """
    <svg viewBox="0 0 318 106" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="hsky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="oklch(0.94 0.025 85)"/>
          <stop offset="100%" stop-color="oklch(0.87 0.045 78)"/>
        </linearGradient>
        <linearGradient id="hsea" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="oklch(0.72 0.08 228)"/>
          <stop offset="100%" stop-color="oklch(0.58 0.09 232)"/>
        </linearGradient>
      </defs>
      <rect width="318" height="50" fill="url(#hsky)"/>
      <rect y="50" width="318" height="56" fill="url(#hsea)"/>
      <path d="M0 46 L28 40 L56 48 L90 54 L72 106 L0 106 Z" fill="oklch(0.78 0.06 78)"/>
      <path d="M214 106 L254 78 L290 68 L318 62 L318 106 Z" fill="oklch(0.78 0.06 78)"/>
      <text x="10" y="96" font-family="Roboto, sans-serif" font-weight="900" font-size="10" fill="oklch(0.24 0.04 75)">IRAN COAST</text>
      <text x="242" y="98" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="oklch(0.24 0.04 75)">OMAN</text>
      <g transform="translate(106,42)">
        <path d="M0,14 L64,14 L56,23 L8,23 Z" fill="oklch(0.20 0.015 260)"/>
        <rect x="6" y="12" width="52" height="2" fill="oklch(0.48 0.18 24)"/>
        <rect x="8" y="5" width="12" height="7" fill="oklch(0.95 0.01 90)"/>
        <circle cx="34" cy="1" r="8" fill="oklch(0.36 0.01 260)" opacity="0.85"/>
        <polygon points="28,12 34,-2 40,12" fill="oklch(0.64 0.21 35)"/>
      </g>
      <g transform="translate(194,64)">
        <path d="M0,14 L60,14 L52,22 L8,22 Z" fill="oklch(0.20 0.015 260)"/>
        <rect x="6" y="12" width="48" height="2" fill="oklch(0.48 0.18 24)"/>
        <rect x="8" y="5" width="11" height="7" fill="oklch(0.95 0.01 90)"/>
        <polygon points="28,12 34,-1 40,12" fill="oklch(0.64 0.21 35)"/>
      </g>
      <rect x="108" y="7" width="202" height="22" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="209" y="22" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="12.5" fill="white">HORMUZ: 3 TANKERS HIT</text>
    </svg>""",
    'hk_vote': """
    <svg viewBox="0 0 184 74" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="184" height="74" fill="oklch(0.95 0.01 85)"/>
      <rect x="16" y="34" width="56" height="32" rx="2" fill="oklch(0.46 0.16 24)"/>
      <rect x="28" y="36" width="32" height="4" fill="oklch(0.22 0.01 260)"/>
      <rect x="34" y="22" width="20" height="16" fill="white" stroke="oklch(0.22 0.01 260)" stroke-width="1.2"/>
      <text x="126" y="45" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="18" fill="oklch(0.18 0.01 260)">856</text>
      <text x="126" y="60" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="700" font-size="9.5" fill="oklch(0.36 0.02 260)">FOR 723 SEATS</text>
      <rect x="5" y="5" width="96" height="15" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="53" y="15.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="white">HONG KONG: VOTE</text>
    </svg>""",
    'cricket_720': """
    <svg viewBox="0 0 184 74" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="184" height="74" fill="oklch(0.93 0.035 145)"/>
      <line x1="28" y1="28" x2="42" y2="62" stroke="oklch(0.55 0.09 55)" stroke-width="5" stroke-linecap="round"/>
      <circle cx="56" cy="56" r="6" fill="oklch(0.48 0.18 24)"/>
      <text x="120" y="52" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="22" fill="oklch(0.18 0.01 260)">720/9</text>
      <rect x="5" y="5" width="94" height="15" rx="2" fill="oklch(0.46 0.12 170)"/>
      <text x="52" y="15.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="white">CRICKET: RECORD</text>
    </svg>""",
    'vegas_f1': """
    <svg viewBox="0 0 184 74" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="184" height="74" fill="oklch(0.20 0.02 260)"/>
      <rect y="52" width="184" height="22" fill="oklch(0.30 0.01 260)"/>
      <line x1="0" y1="63" x2="184" y2="63" stroke="oklch(0.84 0.16 80)" stroke-width="1.5" stroke-dasharray="6 4"/>
      <path d="M22,52 L64,52 L56,43 L30,43 Z" fill="oklch(0.46 0.16 250)"/>
      <circle cx="30" cy="54" r="5" fill="oklch(0.14 0.01 260)" stroke="white" stroke-width="1"/>
      <circle cx="58" cy="54" r="5" fill="oklch(0.14 0.01 260)" stroke="white" stroke-width="1"/>
      <text x="128" y="47" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="14" fill="white">P1 MAX</text>
      <rect x="5" y="5" width="88" height="15" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="49" y="15.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="white">VEGAS F1: WIN</text>
    </svg>""",
    'indonesia_fire': """
    <svg viewBox="0 0 184 74" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="184" height="50" fill="oklch(0.90 0.025 85)"/>
      <rect y="50" width="184" height="24" fill="oklch(0.40 0.04 145)"/>
      <rect x="18" y="32" width="64" height="18" fill="oklch(0.38 0.02 250)"/>
      <polygon points="18,32 30,24 42,32 54,24 66,32 82,32" fill="oklch(0.32 0.02 250)"/>
      <circle cx="62" cy="16" r="8" fill="oklch(0.40 0.01 260)" opacity="0.82"/>
      <polygon points="50,36 62,16 74,36" fill="oklch(0.62 0.21 35)"/>
      <text x="132" y="45" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="15" fill="oklch(0.48 0.18 24)">3 DEAD</text>
      <text x="132" y="65" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="white">36 MISSING</text>
      <rect x="5" y="5" width="96" height="15" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="53" y="15.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="white">INDONESIA: FIRE</text>
    </svg>""",
    'iran_power': """
    <svg viewBox="0 0 184 74" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="184" height="74" fill="oklch(0.18 0.02 260)"/>
      <polygon points="56,24 40,46 52,46 44,66 70,40 58,40" fill="oklch(0.80 0.17 78)"/>
      <line x1="38" y1="26" x2="70" y2="62" stroke="oklch(0.55 0.22 25)" stroke-width="3" stroke-linecap="round"/>
      <text x="122" y="48" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="16" fill="white">2 HRS</text>
      <text x="122" y="62" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="700" font-size="8.5" fill="oklch(0.78 0.03 85)">DAILY CUTS</text>
      <rect x="5" y="5" width="92" height="15" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="51" y="15.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="white">IRAN: POWER CUTS</text>
    </svg>""",
    'fbi_cyber': """
    <svg viewBox="0 0 184 74" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="184" height="74" fill="oklch(0.19 0.03 255)"/>
      <g transform="translate(14,26)">
        <ellipse cx="20" cy="6" rx="16" ry="4.5" fill="oklch(0.36 0.06 245)" stroke="oklch(0.68 0.12 230)" stroke-width="1.2"/>
        <path d="M4,6 V32 A16,4.5 0 0 0 36,32 V6" fill="oklch(0.30 0.05 245)" stroke="oklch(0.68 0.12 230)" stroke-width="1.2"/>
        <polygon points="36,20 46,36 26,36" fill="oklch(0.55 0.21 25)" stroke="white" stroke-width="0.9"/>
        <text x="36" y="34" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9" fill="white">!</text>
      </g>
      <text x="118" y="48" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="15" fill="oklch(0.80 0.15 78)">NCIC HACK</text>
      <rect x="5" y="5" width="88" height="15" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="49" y="15.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="white">FBI: BREACH</text>
    </svg>""",
    'belgium_strike': """
    <svg viewBox="0 0 184 74" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="184" height="74" fill="oklch(0.94 0.015 240)"/>
      <g transform="translate(22,34)">
        <path d="M4,14 L22,14 L34,4 L40,4 L33,14 L46,14 L50,10 L54,10 L52,16 L54,22 L50,22 L46,18 L33,18 L40,28 L34,28 L22,18 L4,18 Z" fill="oklch(0.34 0.03 250)"/>
        <circle cx="28" cy="16" r="16" fill="none" stroke="oklch(0.52 0.20 24)" stroke-width="2.5"/>
        <line x1="17" y1="5" x2="39" y2="27" stroke="oklch(0.52 0.20 24)" stroke-width="2.5"/>
      </g>
      <text x="128" y="48" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="14" fill="oklch(0.18 0.01 260)">07–21H</text>
      <text x="128" y="61" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="700" font-size="8.5" fill="oklch(0.36 0.02 260)">GROUNDED</text>
      <rect x="5" y="5" width="94" height="15" rx="2" fill="oklch(0.46 0.13 245)"/>
      <text x="52" y="15.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="white">BELGIUM: STRIKE</text>
    </svg>""",
    'gaza_van': """
    <svg viewBox="0 0 184 74" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="184" height="50" fill="oklch(0.92 0.02 85)"/>
      <rect y="50" width="184" height="24" fill="oklch(0.78 0.03 80)"/>
      <g transform="translate(14,32)">
        <rect x="0" y="3" width="38" height="18" rx="2" fill="white" stroke="oklch(0.32 0.02 260)" stroke-width="1.3"/>
        <path d="M38,6 L50,6 L55,14 L55,21 L38,21 Z" fill="white" stroke="oklch(0.32 0.02 260)" stroke-width="1.3"/>
        <rect x="4" y="10" width="30" height="3.5" fill="oklch(0.48 0.18 24)"/>
        <circle cx="12" cy="23" r="4.5" fill="oklch(0.22 0.01 260)"/>
        <circle cx="46" cy="23" r="4.5" fill="oklch(0.22 0.01 260)"/>
      </g>
      <text x="128" y="45" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="16" fill="oklch(0.48 0.18 24)">1,671</text>
      <text x="128" y="59" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="700" font-size="8.5" fill="oklch(0.30 0.02 260)">TRUCE TOLL</text>
      <rect x="5" y="5" width="84" height="15" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="47" y="15.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="white">GAZA: AID VAN</text>
    </svg>""",
    'nigeria_boat': """
    <svg viewBox="0 0 184 74" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="184" height="44" fill="oklch(0.88 0.03 220)"/>
      <rect y="44" width="184" height="30" fill="oklch(0.56 0.08 225)"/>
      <path d="M22,52 L74,46 L68,58 L28,58 Z" fill="oklch(0.30 0.04 55)"/>
      <circle cx="88" cy="54" r="6" fill="none" stroke="oklch(0.64 0.20 35)" stroke-width="2.5"/>
      <text x="136" y="55" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="16" fill="oklch(0.48 0.18 24)">26 DEAD</text>
      <rect x="5" y="5" width="92" height="15" rx="2" fill="oklch(0.46 0.13 150)"/>
      <text x="51" y="15.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="white">NIGERIA: BOAT</text>
    </svg>""",
    'aukus_sub': """
    <svg viewBox="0 0 184 74" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="184" height="38" fill="oklch(0.88 0.03 225)"/>
      <rect y="38" width="184" height="36" fill="oklch(0.44 0.09 235)"/>
      <ellipse cx="64" cy="54" rx="44" ry="9" fill="oklch(0.22 0.02 250)"/>
      <rect x="52" y="38" width="18" height="10" rx="2" fill="oklch(0.22 0.02 250)"/>
      <line x1="60" y1="30" x2="60" y2="38" stroke="oklch(0.22 0.02 250)" stroke-width="2"/>
      <text x="142" y="58" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="13" fill="white">AUKUS</text>
      <rect x="5" y="5" width="90" height="15" rx="2" fill="oklch(0.46 0.12 170)"/>
      <text x="50" y="15.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="white">AUSTRALIA: SUBS</text>
    </svg>""",
}


def badge_html(status: str, kind: str, overlay: bool = False) -> str:
    cls = 'badge-official' if kind == 'official' else 'badge-confirmed'
    pos = 'badge-overlay' if overlay else ''
    return f'<span class="badge {cls} {pos}">{html.escape(status)}</span>'


def build_world_map_svg(pins: list[dict]) -> str:
    w, h = 286, 162

    def proj(lon: float, lat: float) -> tuple[float, float]:
        px = ((lon + 180.0) / 360.0) * w
        py = ((82.0 - lat) / 142.0) * h
        return max(8, min(w - 8, px)), max(8, min(h - 8, py))

    landmasses = [
        [
            (-168, 65), (-162, 71), (-140, 70), (-125, 71), (-110, 74), (-95, 72), (-82, 68),
            (-78, 62), (-92, 60), (-90, 54), (-79, 52), (-76, 60), (-64, 60), (-55, 52),
            (-60, 46), (-67, 45), (-70, 42), (-75, 38), (-81, 31), (-80, 25), (-82, 27),
            (-85, 30), (-90, 29), (-97, 26), (-96, 19), (-90, 21), (-87, 21), (-84, 15),
            (-83, 10), (-78, 8), (-80, 9), (-86, 11), (-92, 14), (-105, 19), (-110, 24),
            (-114, 31), (-117, 32), (-122, 38), (-124, 48), (-132, 54), (-140, 60),
            (-152, 60), (-162, 55), (-166, 60),
        ],
        [(-56, 76), (-42, 82), (-20, 81), (-18, 70), (-36, 65), (-44, 60), (-52, 65)],
        [
            (-78, 9), (-72, 12), (-62, 10), (-52, 4), (-48, 0), (-35, -6), (-38, -14),
            (-41, -22), (-48, -28), (-54, -34), (-62, -40), (-66, -46), (-68, -54),
            (-74, -52), (-74, -42), (-71, -30), (-70, -18), (-77, -12), (-81, -5), (-79, 2),
        ],
        [
            (-9, 37), (-9, 43), (-2, 44), (-4, 48), (2, 51), (8, 54), (8, 57), (12, 56),
            (10, 60), (5, 62), (14, 68), (25, 71), (32, 70), (42, 67), (58, 70), (72, 73),
            (102, 77), (138, 73), (170, 68), (178, 64), (162, 59), (156, 51), (142, 54),
            (136, 44), (129, 40), (126, 35), (129, 35), (124, 39), (118, 39), (122, 31),
            (118, 24), (109, 20), (109, 12), (104, 10), (103, 2), (100, 6), (98, 14),
            (94, 16), (91, 22), (85, 19), (80, 13), (77, 8), (73, 18), (68, 23), (62, 25),
            (56, 26), (51, 25), (49, 30), (56, 23), (59, 21), (53, 16), (44, 13), (40, 19),
            (35, 29), (33, 31), (36, 36), (27, 37), (26, 41), (22, 37), (20, 40), (14, 45),
            (16, 40), (12, 42), (9, 44), (4, 43), (0, 39), (-5, 36),
        ],
        [(-6, 50), (1, 51), (1, 53), (-2, 57), (-6, 58), (-7, 54)],
        [(-10, 52), (-6, 52), (-6, 55), (-10, 54)],
        [
            (-6, 36), (10, 37), (12, 33), (25, 32), (32, 31), (36, 26), (42, 12), (51, 12),
            (48, 4), (41, -2), (40, -11), (35, -20), (32, -28), (26, -34), (18, -34),
            (15, -26), (12, -16), (12, -6), (9, 4), (2, 6), (-8, 5), (-15, 11),
            (-17, 15), (-16, 22), (-10, 30),
        ],
        [(44, -25), (47, -25), (50, -15), (48, -12), (44, -18)],
        [(130, 32), (136, 34), (141, 36), (142, 41), (145, 44), (140, 43), (136, 37), (130, 34)],
        [(120, 18), (123, 14), (126, 7), (122, 6), (120, 13)],
        [(109, 2), (118, 6), (117, -3), (110, -3)],
        [(95, 5), (104, -2), (114, -8), (106, -7), (98, 1)],
        [
            (114, -22), (122, -17), (130, -12), (136, -12), (137, -15), (142, -11),
            (146, -18), (153, -26), (150, -36), (145, -38), (138, -36), (130, -32),
            (122, -34), (115, -34), (113, -27),
        ],
        [(173, -35), (178, -38), (175, -42), (167, -46), (170, -42), (174, -39)],
    ]

    grid_lines = ''
    for lat in (-30, 0, 30, 60):
        _, gy = proj(0, lat)
        grid_lines += f'<line x1="0" y1="{gy:.1f}" x2="{w}" y2="{gy:.1f}" stroke="oklch(0.88 0.015 225)" stroke-width="0.6" stroke-dasharray="2 2"/>'
    for lon in (-120, -60, 0, 60, 120):
        gx, _ = proj(lon, 0)
        grid_lines += f'<line x1="{gx:.1f}" y1="0" x2="{gx:.1f}" y2="{h}" stroke="oklch(0.88 0.015 225)" stroke-width="0.6" stroke-dasharray="2 2"/>'

    polys = ''.join(
        '<polygon points="'
        + ' '.join(f'{proj(lo, la)[0]:.1f},{proj(lo, la)[1]:.1f}' for lo, la in poly)
        + '" fill="oklch(0.91 0.018 85)" stroke="oklch(0.68 0.02 85)" stroke-width="0.75" stroke-linejoin="round"/>'
        for poly in landmasses
    )
    pin_els = ''
    for p in pins:
        px, py = proj(p['lon'], p['lat'])
        col = REGION_OKLCH.get(p['r'], 'oklch(0.24 0.01 260)')
        pin_els += (
            f'<g transform="translate({px:.1f},{py:.1f})">'
            f'<circle r="6.2" fill="{col}" stroke="white" stroke-width="1"/>'
            f'<text y="2.8" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="7.5" fill="white">{p["id"]}</text>'
            f'</g>'
        )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" xmlns="http://www.w3.org/2000/svg">'
        f'<rect width="{w}" height="{h}" fill="oklch(0.955 0.014 225)"/>{grid_lines}{polys}{pin_els}</svg>'
    )


def generate_html(data_path: Path, out_html: Path) -> None:
    data = json.loads(data_path.read_text(encoding='utf-8'))

    kpi_html = ''.join(
        f'<div class="kpi-item" style="border-left:3px solid {k["color"]}"><div class="kpi-num">{html.escape(k["num"])}</div><div class="kpi-lbl">{html.escape(k["label"])}</div></div>'
        for k in data['kpi_stats']
    )

    reg_html = ''.join(
        f'<div class="reg-seg" style="flex:{r["count"]} 0 auto;background:{r["color"]}">{html.escape(r["name"])}</div>'
        for r in data['region_bar']
    )

    leads_html = ''.join(
        f'''<article class="lead-card">
          <div class="lead-art">{SVGS[l["art"]]}</div>
          <div class="meta-row">
            <span class="kicker">{html.escape(l["kicker"])}</span>
            {badge_html(l["status"], l["status_kind"])}
          </div>
          <h2>{html.escape(l["title"])}</h2>
          <p>{html.escape(l["body"])}</p>
        </article>'''
        for l in data['leads']
    )

    cards_html = ''.join(
        f'''<article class="mini-card">
          <div class="mini-art">
            {SVGS[c["art"]]}
            {badge_html(c["status"], c["status_kind"], overlay=True)}
          </div>
          <div class="kicker-sm">{html.escape(c["kicker"])}</div>
          <h3>{html.escape(c["title"])}</h3>
          <p>{html.escape(c["sub"])}</p>
        </article>'''
        for c in data['cards']
    )

    col1 = ''.join(
        f'<div class="brief"><span class="b-id">{b[0]}</span> <span class="b-loc">{html.escape(b[1])}:</span> {html.escape(b[2])}</div>'
        for b in data['briefs'][:11]
    )
    col2 = ''.join(
        f'<div class="brief"><span class="b-id">{b[0]}</span> <span class="b-loc">{html.escape(b[1])}:</span> {html.escape(b[2])}</div>'
        for b in data['briefs'][11:]
    )

    legend_html = ''.join(
        f'<span class="leg-item"><i style="background:{col}"></i>{name.title()}</span>'
        for name, col in REGION_OKLCH.items()
    )

    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg-paper: oklch(0.992 0.004 90);
    --bg-panel: oklch(0.955 0.006 85);
    --ink-primary: oklch(0.18 0.01 260);
    --ink-secondary: oklch(0.30 0.01 260);
    --ink-muted: oklch(0.46 0.01 260);
    --rule: oklch(0.84 0.008 85);
    --scarlet: oklch(0.48 0.18 24);
    --badge-confirmed: oklch(0.42 0.12 152);
    --badge-official: oklch(0.46 0.13 65);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1024px;
    height: 1024px;
    overflow: hidden;
    background: var(--bg-paper);
    color: var(--ink-primary);
    font-family: "Roboto", sans-serif;
    text-rendering: optimizeLegibility;
  }}
  .page {{
    width: 1024px;
    height: 1024px;
    padding: 6px 18px 5px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 2px;
  }}
  .eyebrow {{
    display: flex;
    justify-content: space-between;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.025em;
    padding-bottom: 2px;
    border-bottom: 1px solid var(--ink-primary);
  }}
  .eyebrow-left {{ color: var(--scarlet); }}
  .eyebrow-right {{ color: var(--ink-primary); }}
  h1.masthead {{
    font-weight: 900;
    font-size: 36px;
    line-height: 1.02;
    text-align: center;
    letter-spacing: -0.015em;
    padding: 2px 0 1px;
  }}
  .deck {{
    text-align: center;
    font-size: 11.5px;
    font-weight: 500;
    color: var(--scarlet);
    padding-bottom: 2px;
    border-bottom: 2px solid var(--ink-primary);
  }}
  .kpi-strip {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 6px;
    padding: 2.5px 0;
    border-bottom: 1px solid var(--rule);
  }}
  .kpi-item {{
    padding-left: 5px;
  }}
  .kpi-num {{
    font-weight: 900;
    font-size: 18px;
    line-height: 1.02;
    color: var(--scarlet);
  }}
  .kpi-lbl {{
    font-weight: 600;
    font-size: 10.5px;
    line-height: 1.15;
    color: var(--ink-secondary);
    margin-top: 1px;
  }}
  .reg-bar {{
    display: flex;
    gap: 2px;
    margin-top: 2px;
  }}
  .reg-seg {{
    color: white;
    font-weight: 700;
    font-size: 11px;
    text-align: center;
    white-space: nowrap;
    padding: 1.5px 5px;
    border-radius: 1px;
  }}
  .leads {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    padding: 2px 0 3px;
    border-bottom: 1px solid var(--rule);
  }}
  .lead-art {{
    height: 106px;
    border: 1px solid var(--ink-secondary);
    overflow: hidden;
  }}
  .lead-art svg, .mini-art svg {{
    display: block;
    width: 100%;
    height: 100%;
  }}
  .meta-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 2px 0 1.5px;
  }}
  .kicker {{
    font-weight: 700;
    font-size: 10.5px;
    color: var(--scarlet);
  }}
  .badge {{
    font-weight: 700;
    font-size: 9.5px;
    color: white;
    padding: 1px 5px;
    border-radius: 2px;
  }}
  .badge-confirmed {{ background: var(--badge-confirmed); }}
  .badge-official {{ background: var(--badge-official); }}
  .badge-overlay {{
    position: absolute;
    top: 3px;
    right: 3px;
  }}
  .lead-card h2 {{
    font-weight: 900;
    font-size: 18px;
    line-height: 1.07;
    margin-bottom: 2px;
  }}
  .lead-card p {{
    font-weight: 400;
    font-size: 11px;
    line-height: 1.24;
    color: var(--ink-secondary);
  }}
  .cards {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 5px 10px;
    padding: 2px 0 3px;
    border-bottom: 2px solid var(--ink-primary);
  }}
  .mini-art {{
    position: relative;
    height: 74px;
    border: 1px solid var(--ink-secondary);
    overflow: hidden;
  }}
  .kicker-sm {{
    font-weight: 700;
    font-size: 10px;
    color: var(--scarlet);
    margin-top: 2px;
  }}
  .mini-card h3 {{
    font-weight: 900;
    font-size: 13.5px;
    line-height: 1.08;
    margin: 1px 0;
  }}
  .mini-card p {{
    font-weight: 500;
    font-size: 10.5px;
    line-height: 1.2;
    color: var(--ink-secondary);
  }}
  .bottom {{
    display: grid;
    grid-template-columns: 286px 1fr;
    gap: 12px;
    align-items: start;
  }}
  .sec-hd {{
    font-weight: 700;
    font-size: 11px;
    color: var(--scarlet);
    margin-bottom: 2px;
  }}
  .map-box {{
    border: 1px solid var(--rule);
    line-height: 0;
  }}
  .legend {{
    display: flex;
    flex-wrap: wrap;
    gap: 2px 7px;
    margin-top: 2px;
    font-size: 10px;
    font-weight: 600;
    color: var(--ink-secondary);
  }}
  .leg-item {{
    display: inline-flex;
    align-items: center;
    gap: 3px;
  }}
  .leg-item i {{
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
  }}
  .briefs-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0 10px;
    border-top: 1px solid var(--ink-primary);
    padding-top: 2px;
  }}
  .brief {{
    font-weight: 400;
    font-size: 10.5px;
    line-height: 1.22;
    padding: 1.5px 0;
    border-bottom: 1px solid var(--rule);
    color: var(--ink-primary);
  }}
  .b-id {{
    font-weight: 700;
    color: var(--scarlet);
  }}
  .b-loc {{
    font-weight: 700;
    color: var(--ink-primary);
  }}
  .date-check {{
    background: var(--bg-panel);
    border: 1px solid var(--scarlet);
    border-left: 3px solid var(--scarlet);
    padding: 3.5px 7px;
    font-size: 10px;
    line-height: 1.24;
    color: var(--ink-primary);
  }}
  .footer {{
    display: flex;
    justify-content: space-between;
    border-top: 1px solid var(--ink-primary);
    padding-top: 2px;
    font-size: 10px;
    color: var(--ink-muted);
  }}
</style>
</head>
<body>
  <div class="page">
    <div>
      <div class="eyebrow">
        <span class="eyebrow-left">{html.escape(data["eyebrow_left"])}</span>
        <span class="eyebrow-right">{html.escape(data["eyebrow_right"])}</span>
      </div>
      <h1 class="masthead">{html.escape(data["masthead"])}</h1>
      <div class="deck">{html.escape(data["deck"])}</div>
      <div class="kpi-strip">{kpi_html}</div>
      <div class="reg-bar">{reg_html}</div>
    </div>

    <div class="leads">{leads_html}</div>

    <div class="cards">{cards_html}</div>

    <div class="bottom">
      <div>
        <div class="sec-hd">WHERE IT HAPPENED · PINS 1–13</div>
        <div class="map-box">{build_world_map_svg(data["pins"])}</div>
        <div class="legend">{legend_html}</div>
      </div>
      <div>
        <div class="sec-hd">ALSO ON SUNDAY 22 NOVEMBER · 22 MORE STORIES</div>
        <div class="briefs-grid">
          <div>{col1}</div>
          <div>{col2}</div>
        </div>
      </div>
    </div>

    <div class="date-check">{html.escape(data["date_check"])}</div>

    <div class="footer">
      <span>Every story happened or was first reported on Sun 22 Nov 2026 in at least one time zone; claims labelled.</span>
      <span>Sources: Reuters, AP, AFP, BBC, Al Jazeera, SCMP, RFE/RL, EMSC, Darfur24 · Original vector art</span>
    </div>
  </div>
</body>
</html>'''
    out_html.write_text(page, encoding='utf-8')


if __name__ == '__main__':
    base = Path(__file__).resolve().parent
    generate_html(base / 'edition-data.json', base / 'index.html')
    print('Wrote index.html')
