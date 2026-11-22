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
    'hormuz_scene': """
    <svg viewBox="0 0 318 126" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
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
      <rect width="318" height="58" fill="url(#hsky)"/>
      <rect y="58" width="318" height="68" fill="url(#hsea)"/>
      <path d="M100 68 Q160 64 220 72" fill="none" stroke="oklch(0.86 0.04 220)" stroke-width="1.2" stroke-dasharray="4 3"/>
      <path d="M22 86 Q60 83 96 86 M145 104 Q185 101 225 104" fill="none" stroke="oklch(0.82 0.05 225)" stroke-width="1" opacity="0.65"/>
      <path d="M0 52 L28 46 L56 54 L94 60 L78 126 L0 126 Z" fill="oklch(0.78 0.06 78)"/>
      <path d="M0 62 L66 64 L54 126 L0 126 Z" fill="oklch(0.72 0.06 74)"/>
      <path d="M206 126 L248 92 L286 80 L318 74 L318 126 Z" fill="oklch(0.78 0.06 78)"/>
      <path d="M230 126 L276 96 L318 88 L318 126 Z" fill="oklch(0.72 0.06 74)"/>
      <text x="12" y="114" font-family="Roboto, sans-serif" font-weight="900" font-size="10.5" fill="oklch(0.24 0.04 75)">IRAN COAST</text>
      <text x="236" y="116" font-family="Roboto, sans-serif" font-weight="900" font-size="10" fill="oklch(0.24 0.04 75)">OMAN COAST</text>
      <g transform="translate(106,50)">
        <path d="M0,16 L70,16 L62,26 L8,26 Z" fill="oklch(0.20 0.015 260)"/>
        <rect x="6" y="14" width="58" height="2.5" fill="oklch(0.48 0.18 24)"/>
        <rect x="8" y="6" width="14" height="8" fill="oklch(0.95 0.01 90)"/>
        <rect x="11" y="8" width="8" height="3" fill="oklch(0.32 0.03 250)"/>
        <rect x="26" y="10" width="26" height="4" fill="oklch(0.42 0.02 250)"/>
        <circle cx="36" cy="2" r="9" fill="oklch(0.36 0.01 260)" opacity="0.85"/>
        <circle cx="46" cy="-6" r="11" fill="oklch(0.48 0.01 260)" opacity="0.72"/>
        <polygon points="30,14 37,-3 44,14" fill="oklch(0.64 0.21 35)"/>
        <polygon points="33,14 37,3 41,14" fill="oklch(0.82 0.18 75)"/>
      </g>
      <g transform="translate(194,74)">
        <path d="M0,15 L64,15 L56,24 L8,24 Z" fill="oklch(0.20 0.015 260)"/>
        <rect x="5" y="13" width="53" height="2" fill="oklch(0.48 0.18 24)"/>
        <rect x="8" y="6" width="12" height="7" fill="oklch(0.95 0.01 90)"/>
        <rect x="24" y="9" width="22" height="4" fill="oklch(0.42 0.02 250)"/>
        <circle cx="34" cy="1" r="7.5" fill="oklch(0.38 0.01 260)" opacity="0.8"/>
        <polygon points="28,13 34,-2 40,13" fill="oklch(0.64 0.21 35)"/>
        <polygon points="31,13 34,3 37,13" fill="oklch(0.82 0.18 75)"/>
      </g>
      <rect x="106" y="7" width="204" height="23" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="208" y="23" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="13" fill="white">HORMUZ: 3 TANKERS HIT</text>
    </svg>""",
    'cop31_scene': """
    <svg viewBox="0 0 318 126" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="318" height="126" fill="oklch(0.96 0.01 85)"/>
      <circle cx="159" cy="56" r="46" fill="none" stroke="oklch(0.88 0.02 220)" stroke-width="1" stroke-dasharray="3 3"/>
      <g transform="translate(14,30)">
        <rect width="78" height="50" rx="2" fill="oklch(0.48 0.21 25)"/>
        <circle cx="30" cy="25" r="12" fill="white"/>
        <circle cx="34" cy="25" r="9.5" fill="oklch(0.48 0.21 25)"/>
        <polygon points="48,25 54,23 50,28 50,22 54,27" fill="white"/>
        <text x="39" y="61" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="8.5" fill="oklch(0.35 0.02 260)">TÜRKİYE</text>
      </g>
      <g transform="translate(226,30)">
        <rect width="78" height="50" rx="2" fill="oklch(0.34 0.16 258)"/>
        <rect width="34" height="24" fill="oklch(0.30 0.14 258)"/>
        <path d="M0,0 L34,24 M34,0 L0,24" stroke="white" stroke-width="3"/>
        <path d="M0,0 L34,24 M34,0 L0,24" stroke="oklch(0.50 0.20 25)" stroke-width="1.2"/>
        <path d="M17,0 V24 M0,12 H34" stroke="white" stroke-width="4.5"/>
        <path d="M17,0 V24 M0,12 H34" stroke="oklch(0.50 0.20 25)" stroke-width="2.2"/>
        <circle cx="17" cy="37" r="4.2" fill="white"/>
        <circle cx="56" cy="14" r="2" fill="white"/><circle cx="64" cy="24" r="2" fill="white"/>
        <circle cx="52" cy="31" r="2" fill="white"/><circle cx="58" cy="40" r="2" fill="white"/>
        <text x="39" y="61" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="8.5" fill="oklch(0.35 0.02 260)">AUSTRALIA</text>
      </g>
      <g transform="translate(123,25)">
        <rect width="72" height="58" rx="3" fill="white" stroke="oklch(0.46 0.13 245)" stroke-width="1.6"/>
        <polygon points="56,0 72,16 56,16" fill="oklch(0.90 0.03 240)"/>
        <rect x="10" y="10" width="38" height="4" rx="1" fill="oklch(0.46 0.13 245)"/>
        <line x1="10" y1="22" x2="62" y2="22" stroke="oklch(0.65 0.04 250)" stroke-width="2"/>
        <line x1="10" y1="30" x2="62" y2="30" stroke="oklch(0.65 0.04 250)" stroke-width="2"/>
        <line x1="10" y1="38" x2="48" y2="38" stroke="oklch(0.65 0.04 250)" stroke-width="2"/>
        <line x1="10" y1="46" x2="40" y2="46" stroke="oklch(0.65 0.04 250)" stroke-width="2"/>
        <circle cx="56" cy="46" r="7" fill="oklch(0.42 0.12 152)"/>
        <polyline points="52.5,46 55,48.5 60,43.5" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
      </g>
      <text x="159" y="17" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="11" fill="oklch(0.22 0.01 260)">ANTALYA · PLENARY 06:00 GMT</text>
      <rect x="14" y="96" width="290" height="23" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="159" y="112" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="13" fill="white">COP31: NEW DEAL TEXT TABLED</text>
    </svg>""",
    'baltic_ship': """
    <svg viewBox="0 0 318 126" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="bsky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="oklch(0.84 0.03 235)"/>
          <stop offset="100%" stop-color="oklch(0.91 0.02 230)"/>
        </linearGradient>
        <linearGradient id="bsea" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="oklch(0.48 0.09 235)"/>
          <stop offset="100%" stop-color="oklch(0.36 0.08 240)"/>
        </linearGradient>
      </defs>
      <rect width="318" height="64" fill="url(#bsky)"/>
      <rect y="64" width="318" height="62" fill="url(#bsea)"/>
      <path d="M12 82 Q42 79 72 82 M176 92 Q216 89 256 92 M34 108 Q84 105 134 108" fill="none" stroke="oklch(0.72 0.05 230)" stroke-width="1.2" opacity="0.6"/>
      <g transform="translate(36,56)">
        <polygon points="0,24 148,24 136,44 12,44" fill="oklch(0.20 0.015 260)"/>
        <rect x="8" y="21" width="132" height="3" fill="oklch(0.48 0.18 24)"/>
        <rect x="16" y="4" width="26" height="17" fill="oklch(0.96 0.01 90)"/>
        <rect x="20" y="7" width="18" height="4" fill="oklch(0.32 0.03 250)"/>
        <rect x="22" y="-3" width="5" height="7" fill="oklch(0.28 0.01 260)"/>
        <rect x="48" y="13" width="22" height="8" fill="oklch(0.44 0.12 245)"/>
        <rect x="72" y="13" width="22" height="8" fill="oklch(0.48 0.16 25)"/>
        <rect x="96" y="13" width="22" height="8" fill="oklch(0.48 0.12 150)"/>
        <circle cx="96" cy="-16" r="13" fill="oklch(0.36 0.01 260)" opacity="0.88"/>
        <circle cx="114" cy="-26" r="15" fill="oklch(0.48 0.01 260)" opacity="0.76"/>
        <circle cx="130" cy="-34" r="14" fill="oklch(0.60 0.01 260)" opacity="0.6"/>
        <polygon points="78,20 92,-12 106,20" fill="oklch(0.62 0.21 35)"/>
        <polygon points="84,20 92,-1 100,20" fill="oklch(0.84 0.18 75)"/>
      </g>
      <g transform="translate(248,46)">
        <line x1="-26" y1="-10" x2="26" y2="-10" stroke="oklch(0.20 0.01 260)" stroke-width="2.2"/>
        <line x1="0" y1="-10" x2="0" y2="-4" stroke="oklch(0.20 0.01 260)" stroke-width="2.5"/>
        <ellipse cx="0" cy="2" rx="18" ry="7" fill="oklch(0.40 0.14 245)"/>
        <path d="M16,2 L34,-2 L36,-8" fill="none" stroke="oklch(0.40 0.14 245)" stroke-width="3" stroke-linecap="round"/>
        <line x1="-4" y1="9" x2="-4" y2="28" stroke="oklch(0.95 0.02 90)" stroke-width="1.2" stroke-dasharray="2 2"/>
      </g>
      <rect x="200" y="96" width="108" height="21" rx="2" fill="oklch(0.22 0.02 250)" opacity="0.85"/>
      <text x="254" y="110.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="11.5" fill="white">16 CREW SAFE</text>
      <rect x="8" y="7" width="186" height="23" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="101" y="23" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="13" fill="white">BALTIC: SHIP ABLAZE</text>
    </svg>""",
    'indonesia_fire': """
    <svg viewBox="0 0 236 92" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="236" height="60" fill="oklch(0.90 0.025 85)"/>
      <rect y="60" width="236" height="32" fill="oklch(0.40 0.04 145)"/>
      <rect x="26" y="38" width="84" height="22" fill="oklch(0.38 0.02 250)"/>
      <polygon points="26,38 40,28 54,38 68,28 82,38 96,28 110,38" fill="oklch(0.32 0.02 250)"/>
      <circle cx="84" cy="18" r="10" fill="oklch(0.40 0.01 260)" opacity="0.82"/>
      <circle cx="96" cy="12" r="11" fill="oklch(0.50 0.01 260)" opacity="0.68"/>
      <polygon points="68,42 82,18 96,42" fill="oklch(0.62 0.21 35)"/>
      <polygon points="74,42 82,26 90,42" fill="oklch(0.82 0.18 75)"/>
      <text x="172" y="54" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="18" fill="oklch(0.48 0.18 24)">3 DEAD</text>
      <text x="172" y="80" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="10" fill="white">DOZENS MISSING</text>
      <rect x="6" y="6" width="128" height="17" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="70" y="18" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="white">INDONESIA: FIRE</text>
    </svg>""",
    'iran_power': """
    <svg viewBox="0 0 236 92" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="236" height="92" fill="oklch(0.18 0.02 260)"/>
      <g fill="oklch(0.26 0.02 260)">
        <rect x="10" y="54" width="18" height="38"/><rect x="32" y="42" width="22" height="50"/>
        <rect x="58" y="60" width="16" height="32"/><rect x="180" y="48" width="22" height="44"/>
        <rect x="206" y="58" width="20" height="34"/>
      </g>
      <rect x="36" y="48" width="4" height="4" fill="oklch(0.78 0.16 75)"/>
      <rect x="186" y="56" width="4" height="4" fill="oklch(0.78 0.16 75)" opacity="0.4"/>
      <polygon points="76,28 58,56 72,56 62,80 94,48 78,48" fill="oklch(0.80 0.17 78)"/>
      <line x1="54" y1="32" x2="94" y2="74" stroke="oklch(0.55 0.22 25)" stroke-width="3.5" stroke-linecap="round"/>
      <text x="156" y="60" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="21" fill="white">2 HRS/DAY</text>
      <text x="156" y="76" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="700" font-size="9.5" fill="oklch(0.78 0.03 85)">ROLLING CUTS</text>
      <rect x="6" y="6" width="114" height="17" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="63" y="18" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="white">IRAN: POWER CUTS</text>
    </svg>""",
    'nato_poland': """
    <svg viewBox="0 0 236 92" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="236" height="92" fill="oklch(0.94 0.02 245)"/>
      <circle cx="52" cy="54" r="30" fill="none" stroke="oklch(0.82 0.05 245)" stroke-width="1" stroke-dasharray="3 2"/>
      <rect x="20" y="34" width="64" height="40" rx="2" fill="oklch(0.36 0.15 250)"/>
      <circle cx="52" cy="54" r="12" fill="none" stroke="white" stroke-width="1.4"/>
      <polygon points="52,38 55,51 68,54 55,57 52,70 49,57 36,54 49,51" fill="white"/>
      <rect x="114" y="64" width="96" height="9" fill="white" stroke="oklch(0.82 0.01 250)" stroke-width="0.6"/>
      <rect x="114" y="73" width="96" height="9" fill="oklch(0.50 0.21 25)"/>
      <text x="162" y="54" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="19" fill="oklch(0.20 0.02 250)">POLAND</text>
      <rect x="6" y="6" width="106" height="17" rx="2" fill="oklch(0.46 0.13 245)"/>
      <text x="59" y="18" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="white">NATO: PLEDGE</text>
    </svg>""",
    'drone_wave': """
    <svg viewBox="0 0 236 92" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="236" height="62" fill="oklch(0.18 0.03 255)"/>
      <rect y="62" width="236" height="30" fill="oklch(0.30 0.05 245)"/>
      <path d="M120 62 A46 46 0 0 1 206 62" fill="none" stroke="oklch(0.52 0.10 190)" stroke-width="1" stroke-dasharray="3 3"/>
      <rect x="22" y="42" width="24" height="20" rx="2" fill="oklch(0.38 0.02 250)"/>
      <rect x="52" y="36" width="28" height="26" rx="2" fill="oklch(0.44 0.02 250)"/>
      <circle cx="72" cy="24" r="9" fill="oklch(0.40 0.01 260)" opacity="0.8"/>
      <polygon points="58,42 72,22 86,42" fill="oklch(0.64 0.21 35)"/>
      <polygon points="118,32 138,37 118,42 124,37" fill="oklch(0.78 0.16 75)"/>
      <polygon points="148,22 166,26 148,30 153,26" fill="oklch(0.78 0.16 75)"/>
      <line x1="164" y1="62" x2="146" y2="34" stroke="oklch(0.84 0.16 80)" stroke-width="1.2" stroke-dasharray="3 3"/>
      <text x="166" y="81" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="11.5" fill="white">LENINGRAD</text>
      <rect x="6" y="6" width="108" height="17" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="60" y="18" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="white">RUSSIA: DRONES</text>
    </svg>""",
    'gaza_van': """
    <svg viewBox="0 0 236 92" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="236" height="60" fill="oklch(0.92 0.02 85)"/>
      <rect y="60" width="236" height="32" fill="oklch(0.78 0.03 80)"/>
      <path d="M0 60 L24 44 L44 52 L68 42 L88 60 Z" fill="oklch(0.84 0.02 82)"/>
      <g transform="translate(22,38)">
        <rect x="0" y="4" width="44" height="22" rx="2" fill="white" stroke="oklch(0.32 0.02 260)" stroke-width="1.5"/>
        <path d="M44,8 L58,8 L64,17 L64,26 L44,26 Z" fill="white" stroke="oklch(0.32 0.02 260)" stroke-width="1.5"/>
        <polygon points="47,11 56,11 60,17 47,17" fill="oklch(0.75 0.06 230)"/>
        <rect x="4" y="12" width="36" height="4" fill="oklch(0.48 0.18 24)"/>
        <circle cx="14" cy="28" r="5.5" fill="oklch(0.22 0.01 260)"/>
        <circle cx="14" cy="28" r="2.2" fill="oklch(0.78 0.01 260)"/>
        <circle cx="52" cy="28" r="5.5" fill="oklch(0.22 0.01 260)"/>
        <circle cx="52" cy="28" r="2.2" fill="oklch(0.78 0.01 260)"/>
      </g>
      <text x="160" y="54" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="20" fill="oklch(0.48 0.18 24)">1,671</text>
      <text x="160" y="70" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="9.5" fill="oklch(0.32 0.02 260)">SINCE TRUCE</text>
      <rect x="6" y="6" width="100" height="17" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="56" y="18" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="white">GAZA: AID VAN</text>
    </svg>""",
    'mexico_cartel': """
    <svg viewBox="0 0 236 92" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="236" height="52" fill="oklch(0.26 0.04 145)"/>
      <path d="M0 52 L38 36 L82 46 L132 34 L184 48 L236 38 L236 52 Z" fill="oklch(0.33 0.04 145)"/>
      <rect y="52" width="236" height="40" fill="oklch(0.38 0.05 140)"/>
      <polygon points="68,42 46,84 90,84" fill="oklch(0.85 0.08 90)" opacity="0.22"/>
      <line x1="30" y1="30" x2="106" y2="30" stroke="oklch(0.14 0.01 260)" stroke-width="2.2"/>
      <ellipse cx="68" cy="39" rx="19" ry="6.5" fill="oklch(0.18 0.02 145)"/>
      <line x1="86" y1="39" x2="112" y2="35" stroke="oklch(0.18 0.02 145)" stroke-width="2.5"/>
      <g fill="oklch(0.18 0.02 145)">
        <circle cx="56" cy="60" r="3"/><rect x="52" y="64" width="8" height="14" rx="1"/>
        <circle cx="74" cy="60" r="3"/><rect x="70" y="64" width="8" height="14" rx="1"/>
      </g>
      <rect x="174" y="38" width="11" height="22" fill="oklch(0.45 0.14 150)"/>
      <rect x="185" y="38" width="11" height="22" fill="white"/>
      <rect x="196" y="38" width="11" height="22" fill="oklch(0.50 0.21 25)"/>
      <circle cx="190.5" cy="49" r="2.2" fill="oklch(0.48 0.10 65)"/>
      <text x="168" y="80" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="11" fill="white">SINALOA RAID</text>
      <rect x="6" y="6" width="114" height="17" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="63" y="18" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="white">MEXICO: CAPTURE</text>
    </svg>""",
    'fbi_cyber': """
    <svg viewBox="0 0 236 92" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="236" height="92" fill="oklch(0.19 0.03 255)"/>
      <path d="M0 32 H236 M0 62 H236 M84 0 V92 M164 0 V92" stroke="oklch(0.26 0.04 250)" stroke-width="0.8"/>
      <g transform="translate(20,30)">
        <ellipse cx="26" cy="8" rx="22" ry="6" fill="oklch(0.36 0.06 245)" stroke="oklch(0.68 0.12 230)" stroke-width="1.4"/>
        <path d="M4,8 V40 A22,6 0 0 0 48,40 V8" fill="oklch(0.30 0.05 245)" stroke="oklch(0.68 0.12 230)" stroke-width="1.4"/>
        <path d="M4,20 A22,6 0 0 0 48,20 M4,31 A22,6 0 0 0 48,31" fill="none" stroke="oklch(0.68 0.12 230)" stroke-width="1.2"/>
        <polygon points="48,26 60,46 36,46" fill="oklch(0.55 0.21 25)" stroke="white" stroke-width="1"/>
        <text x="48" y="43.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="11" fill="white">!</text>
      </g>
      <text x="152" y="54" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="19" fill="oklch(0.80 0.15 78)">NCIC HACK</text>
      <text x="152" y="70" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="700" font-size="9.5" fill="oklch(0.75 0.04 240)">PROBE OPEN</text>
      <rect x="6" y="6" width="106" height="17" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="59" y="18" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="white">FBI: DATA BREACH</text>
    </svg>""",
    'sudan_mine': """
    <svg viewBox="0 0 236 92" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="236" height="56" fill="oklch(0.90 0.03 80)"/>
      <rect y="56" width="236" height="36" fill="oklch(0.74 0.06 75)"/>
      <path d="M0 56 L58 48 L124 56 L190 50 L236 56 Z" fill="oklch(0.80 0.04 78)"/>
      <g transform="translate(26,38)">
        <circle cx="24" cy="24" r="14" fill="none" stroke="oklch(0.56 0.18 30)" stroke-width="1.6" stroke-dasharray="3 2"/>
        <polygon points="24,0 29,16 42,10 31,21 44,28 28,27 24,40 20,27 4,28 17,21 6,10 19,16" fill="oklch(0.62 0.21 35)"/>
        <circle cx="24" cy="23" r="6" fill="oklch(0.22 0.01 260)"/>
      </g>
      <text x="154" y="56" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="20" fill="oklch(0.48 0.18 24)">22 DEAD</text>
      <text x="154" y="72" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="9.5" fill="oklch(0.28 0.03 75)">N. KORDOFAN</text>
      <rect x="6" y="6" width="112" height="17" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="62" y="18" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="white">SUDAN: LANDMINE</text>
    </svg>""",
}


def badge_html(status: str, kind: str, overlay: bool = False) -> str:
    cls = 'badge-official' if kind == 'official' else 'badge-confirmed'
    pos = 'badge-overlay' if overlay else ''
    return f'<span class="badge {cls} {pos}">{html.escape(status)}</span>'


def build_world_map_svg(pins: list[dict]) -> str:
    w, h = 290, 130

    def proj(lon: float, lat: float) -> tuple[float, float]:
        px = ((lon + 180.0) / 360.0) * w
        py = ((82.0 - lat) / 142.0) * h
        return max(8, min(w - 8, px)), max(8, min(h - 8, py))

    # Detailed multi-point continental & major island outlines
    landmasses = [
        # North & Central America
        [
            (-168, 65), (-162, 71), (-140, 70), (-125, 71), (-110, 74), (-95, 72), (-82, 68),
            (-78, 62), (-92, 60), (-90, 54), (-79, 52), (-76, 60), (-64, 60), (-55, 52),
            (-60, 46), (-67, 45), (-70, 42), (-75, 38), (-81, 31), (-80, 25), (-82, 27),
            (-85, 30), (-90, 29), (-97, 26), (-96, 19), (-90, 21), (-87, 21), (-84, 15),
            (-83, 10), (-78, 8), (-80, 9), (-86, 11), (-92, 14), (-105, 19), (-110, 24),
            (-114, 31), (-117, 32), (-122, 38), (-124, 48), (-132, 54), (-140, 60),
            (-152, 60), (-162, 55), (-166, 60),
        ],
        # Greenland
        [(-56, 76), (-42, 82), (-20, 81), (-18, 70), (-36, 65), (-44, 60), (-52, 65)],
        # South America
        [
            (-78, 9), (-72, 12), (-62, 10), (-52, 4), (-48, 0), (-35, -6), (-38, -14),
            (-41, -22), (-48, -28), (-54, -34), (-62, -40), (-66, -46), (-68, -54),
            (-74, -52), (-74, -42), (-71, -30), (-70, -18), (-77, -12), (-81, -5), (-79, 2),
        ],
        # Europe + Eurasia + India + SE Asia
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
        # UK & Ireland
        [(-6, 50), (1, 51), (1, 53), (-2, 57), (-6, 58), (-7, 54)],
        [(-10, 52), (-6, 52), (-6, 55), (-10, 54)],
        # Africa
        [
            (-6, 36), (10, 37), (12, 33), (25, 32), (32, 31), (36, 26), (42, 12), (51, 12),
            (48, 4), (41, -2), (40, -11), (35, -20), (32, -28), (26, -34), (18, -34),
            (15, -26), (12, -16), (12, -6), (9, 4), (2, 6), (-8, 5), (-15, 11),
            (-17, 15), (-16, 22), (-10, 30),
        ],
        # Madagascar
        [(44, -25), (47, -25), (50, -15), (48, -12), (44, -18)],
        # Japan
        [(130, 32), (136, 34), (141, 36), (142, 41), (145, 44), (140, 43), (136, 37), (130, 34)],
        # Philippines & Borneo & Sumatra/Java
        [(120, 18), (123, 14), (126, 7), (122, 6), (120, 13)],
        [(109, 2), (118, 6), (117, -3), (110, -3)],
        [(95, 5), (104, -2), (114, -8), (106, -7), (98, 1)],
        # Australia
        [
            (114, -22), (122, -17), (130, -12), (136, -12), (137, -15), (142, -11),
            (146, -18), (153, -26), (150, -36), (145, -38), (138, -36), (130, -32),
            (122, -34), (115, -34), (113, -27),
        ],
        # New Zealand
        [(173, -35), (178, -38), (175, -42), (167, -46), (170, -42), (174, -39)],
    ]

    # Subtle graticule lines for cartographic precision
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

    timeline_html = ''.join(
        f'<div class="tl-item"><div class="tl-time">{html.escape(t["time"])}</div><div class="tl-lbl">{html.escape(t["label"])}</div></div>'
        for t in data['timeline']
    )

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
        for b in data['briefs'][:5]
    )
    col2 = ''.join(
        f'<div class="brief"><span class="b-id">{b[0]}</span> <span class="b-loc">{html.escape(b[1])}:</span> {html.escape(b[2])}</div>'
        for b in data['briefs'][5:]
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
    font-size: 12px;
    letter-spacing: 0.03em;
    padding-bottom: 2px;
    border-bottom: 1px solid var(--ink-primary);
  }}
  .eyebrow-left {{ color: var(--scarlet); }}
  .eyebrow-right {{ color: var(--ink-primary); }}
  h1.masthead {{
    font-weight: 900;
    font-size: 32px;
    line-height: 1.03;
    text-align: center;
    letter-spacing: -0.015em;
    padding: 2px 0;
    border-bottom: 2px solid var(--ink-primary);
  }}
  .timeline {{
    display: grid;
    grid-template-columns: 64px repeat(5, 1fr);
    align-items: center;
    border-bottom: 1px solid var(--rule);
    padding: 1.5px 0;
  }}
  .kpi-strip {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 6px;
    padding: 1.5px 0;
    border-bottom: 1px solid var(--rule);
  }}
  .kpi-item {{
    padding-left: 6px;
  }}
  .kpi-num {{
    font-weight: 900;
    font-size: 18px;
    line-height: 1.05;
    color: var(--scarlet);
  }}
  .kpi-lbl {{
    font-weight: 600;
    font-size: 12px;
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
    font-size: 12px;
    text-align: center;
    white-space: nowrap;
    padding: 2px 6px;
    border-radius: 1px;
  }}
  .tl-badge {{
    background: var(--scarlet);
    color: white;
    font-weight: 700;
    font-size: 12px;
    line-height: 1.1;
    text-align: center;
    padding: 3px 2px;
    border-radius: 2px;
  }}
  .tl-item {{
    text-align: center;
    border-left: 1px solid var(--rule);
    padding: 0 3px;
  }}
  .tl-time {{
    font-weight: 800;
    font-size: 13px;
    color: var(--scarlet);
  }}
  .tl-lbl {{
    font-size: 12px;
    color: var(--ink-secondary);
    white-space: nowrap;
  }}
  .leads {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    padding: 2px 0 4px;
    border-bottom: 1px solid var(--rule);
  }}
  .lead-art {{
    height: 126px;
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
    margin: 3px 0 2px;
  }}
  .kicker {{
    font-weight: 700;
    font-size: 12px;
    color: var(--scarlet);
  }}
  .badge {{
    font-weight: 700;
    font-size: 12px;
    color: white;
    padding: 1px 6px;
    border-radius: 2px;
  }}
  .badge-confirmed {{ background: var(--badge-confirmed); }}
  .badge-official {{ background: var(--badge-official); }}
  .badge-overlay {{
    position: absolute;
    top: 4px;
    right: 4px;
  }}
  .lead-card h2 {{
    font-weight: 900;
    font-size: 19px;
    line-height: 1.06;
    margin-bottom: 2px;
  }}
  .lead-card p {{
    font-weight: 400;
    font-size: 12px;
    line-height: 1.24;
    color: var(--ink-secondary);
  }}
  .cards {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 4px 14px;
    padding: 1px 0 3px;
    border-bottom: 2px solid var(--ink-primary);
  }}
  .mini-art {{
    position: relative;
    height: 92px;
    border: 1px solid var(--ink-secondary);
    overflow: hidden;
  }}
  .kicker-sm {{
    font-weight: 700;
    font-size: 12px;
    color: var(--scarlet);
    margin-top: 2px;
  }}
  .mini-card h3 {{
    font-weight: 900;
    font-size: 15.5px;
    line-height: 1.08;
    margin: 1px 0 1px;
  }}
  .mini-card p {{
    font-weight: 500;
    font-size: 12px;
    line-height: 1.24;
    color: var(--ink-secondary);
  }}
  .bottom {{
    display: grid;
    grid-template-columns: 290px 1fr;
    gap: 14px;
    align-items: start;
  }}
  .sec-hd {{
    font-weight: 700;
    font-size: 12px;
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
    gap: 2px 8px;
    margin-top: 3px;
    font-size: 12px;
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
    width: 7px;
    height: 7px;
    border-radius: 50%;
  }}
  .briefs-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0 12px;
    border-top: 1px solid var(--ink-primary);
    padding-top: 2px;
  }}
  .brief {{
    font-weight: 400;
    font-size: 12px;
    line-height: 1.24;
    padding: 2px 0;
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
    margin-top: 4px;
    background: var(--bg-panel);
    border: 1px solid var(--rule);
    border-top: 2px solid var(--scarlet);
    padding: 3.5px 8px;
    font-size: 12px;
    line-height: 1.25;
    color: var(--ink-primary);
  }}
  .footer {{
    display: flex;
    justify-content: space-between;
    border-top: 1px solid var(--ink-primary);
    padding-top: 2.5px;
    font-size: 12px;
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
      <div class="timeline">
        <div class="tl-badge">THE DAY<br/>IN KEY</div>
        {timeline_html}
      </div>
      <div class="kpi-strip">{kpi_html}</div>
      <div class="reg-bar">{reg_html}</div>
    </div>

    <div class="leads">{leads_html}</div>

    <div class="cards">{cards_html}</div>

    <div class="bottom">
      <div>
        <div class="sec-hd">WHERE IT HAPPENED</div>
        <div class="map-box">{build_world_map_svg(data["pins"])}</div>
        <div class="legend">{legend_html}</div>
      </div>
      <div>
        <div class="sec-hd">ALSO ON SUNDAY 22 NOVEMBER · 10 MORE STORIES</div>
        <div class="briefs-grid">
          <div>{col1}</div>
          <div>{col2}</div>
        </div>
        <div class="date-check">{html.escape(data["date_check"])}</div>
      </div>
    </div>

    <div class="footer">
      <span>Every story happened or was first reported on Sun 22 Nov 2026; claims attributed.</span>
      <span>Sources: Reuters, AP, AFP, UKMTO, Finnish MoD, Darfur24 · Original vector art</span>
    </div>
  </div>
</body>
</html>'''
    out_html.write_text(page, encoding='utf-8')


if __name__ == '__main__':
    base = Path(__file__).resolve().parent
    generate_html(base / 'edition-data.json', base / 'index.html')
    print('Wrote index.html')
