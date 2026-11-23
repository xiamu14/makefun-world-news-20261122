from __future__ import annotations

import html
import json
import math
from pathlib import Path

REGION_OKLCH = {
    'EUROPE': 'oklch(0.45 0.19 258)',
    'ASIA': 'oklch(0.50 0.14 202)',
    'MIDDLE EAST': 'oklch(0.47 0.21 322)',
    'AFRICA': 'oklch(0.48 0.16 148)',
    'N. AMERICA': 'oklch(0.50 0.21 24)',
    'S. AMERICA': 'oklch(0.54 0.17 55)',
    'OCEANIA': 'oklch(0.50 0.19 355)',
    'GLOBAL': 'oklch(0.22 0.01 260)',
}

SVGS: dict[str, str] = {
    'cop31_collapse': """
    <svg viewBox="0 0 318 118" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="318" height="118" fill="oklch(0.96 0.012 85)"/>
      <rect x="8" y="8" width="94" height="72" rx="3" fill="white" stroke="oklch(0.84 0.01 85)" stroke-width="1"/>
      <text x="55" y="21" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="oklch(0.24 0.01 260)">COP31 · ANTALYA</text>
      <rect x="14" y="26" width="38" height="24" rx="1.5" fill="oklch(0.49 0.20 25)"/>
      <circle cx="30" cy="38" r="6" fill="white"/>
      <circle cx="32.2" cy="38" r="4.8" fill="oklch(0.49 0.20 25)"/>
      <polygon points="37,38 39,37 38,39 39.5,39.5 37.5,39.5" fill="white"/>
      <rect x="58" y="26" width="38" height="24" rx="1.5" fill="oklch(0.32 0.12 255)"/>
      <rect x="58" y="26" width="18" height="12" fill="oklch(0.26 0.11 255)"/>
      <line x1="58" y1="26" x2="76" y2="38" stroke="white" stroke-width="1.8"/>
      <line x1="76" y1="26" x2="58" y2="38" stroke="white" stroke-width="1.8"/>
      <line x1="67" y1="26" x2="67" y2="38" stroke="oklch(0.52 0.21 25)" stroke-width="2.2"/>
      <line x1="58" y1="32" x2="76" y2="32" stroke="oklch(0.52 0.21 25)" stroke-width="2.2"/>
      <circle cx="84" cy="43" r="1.4" fill="white"/><circle cx="89" cy="40" r="1.2" fill="white"/><circle cx="83" cy="37" r="1.2" fill="white"/>
      <rect x="14" y="55" width="82" height="18" rx="2" fill="oklch(0.93 0.03 24)"/>
      <text x="55" y="67" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="oklch(0.48 0.18 24)">+48H OVERTIME</text>

      <rect x="110" y="8" width="112" height="72" rx="3" fill="white" stroke="oklch(0.76 0.015 250)" stroke-width="1.2"/>
      <text x="166" y="21" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="8.5" fill="oklch(0.30 0.02 250)">FINAL SUMMIT DRAFT</text>
      <line x1="120" y1="28" x2="212" y2="28" stroke="oklch(0.86 0.01 250)" stroke-width="2"/>
      <rect x="120" y="34" width="92" height="17" rx="2" fill="oklch(0.95 0.03 24)"/>
      <text x="166" y="46" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="oklch(0.48 0.18 24)">FOSSIL FUELS</text>
      <line x1="124" y1="42.5" x2="208" y2="42.5" stroke="oklch(0.48 0.18 24)" stroke-width="2"/>
      <line x1="120" y1="58" x2="194" y2="58" stroke="oklch(0.86 0.01 250)" stroke-width="2"/>
      <line x1="120" y1="66" x2="180" y2="66" stroke="oklch(0.86 0.01 250)" stroke-width="2"/>
      <path d="M162,52 L167,61 L161,71 L166,80" fill="none" stroke="oklch(0.96 0.012 85)" stroke-width="2.2"/>

      <rect x="230" y="8" width="80" height="72" rx="3" fill="white" stroke="oklch(0.84 0.01 85)" stroke-width="1"/>
      <circle cx="270" cy="34" r="18" fill="none" stroke="oklch(0.48 0.18 24)" stroke-width="2.5"/>
      <line x1="257" y1="21" x2="283" y2="47" stroke="oklch(0.48 0.18 24)" stroke-width="2.5"/>
      <text x="270" y="64" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="10" fill="oklch(0.48 0.18 24)">NO DEAL</text>
      <text x="270" y="74" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="700" font-size="7.5" fill="oklch(0.36 0.02 260)">TALKS COLLAPSE</text>

      <rect x="8" y="87" width="302" height="22" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="159" y="102" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="10.5" fill="white">TALKS COLLAPSE OVER FOSSIL FUELS · LONGEST COP</text>
    </svg>""",
    'ukraine_strikes': """
    <svg viewBox="0 0 318 118" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="318" height="118" fill="oklch(0.18 0.025 255)"/>
      <g fill="oklch(0.25 0.02 255)">
        <rect x="0" y="54" width="24" height="64"/>
        <rect x="28" y="42" width="28" height="76"/>
        <rect x="220" y="48" width="30" height="70"/>
        <rect x="256" y="38" width="26" height="80"/>
        <rect x="286" y="52" width="32" height="66"/>
      </g>
      <rect x="64" y="44" width="52" height="58" fill="oklch(0.34 0.02 250)"/>
      <polygon points="116,54 148,74 148,102 116,102" fill="oklch(0.29 0.02 250)"/>
      <g fill="oklch(0.78 0.12 75)">
        <rect x="70" y="52" width="7" height="7"/><rect x="83" y="52" width="7" height="7"/>
        <rect x="70" y="66" width="7" height="7"/><rect x="83" y="66" width="7" height="7"/>
      </g>
      <polygon points="56,102 92,84 128,88 168,102" fill="oklch(0.46 0.02 70)"/>
      <polygon points="88,102 114,82 146,92 162,102" fill="oklch(0.54 0.02 75)"/>
      <line x1="184" y1="102" x2="184" y2="48" stroke="oklch(0.78 0.16 78)" stroke-width="3.5"/>
      <line x1="184" y1="50" x2="128" y2="68" stroke="oklch(0.78 0.16 78)" stroke-width="2.5"/>
      <line x1="138" y1="65" x2="138" y2="85" stroke="white" stroke-width="1.2" stroke-dasharray="2 2"/>
      <circle cx="156" cy="84" r="4" fill="oklch(0.78 0.16 78)"/>
      <rect x="152" y="88" width="8" height="12" rx="2" fill="oklch(0.62 0.20 35)"/>
      <polygon points="98,84 112,56 126,84" fill="oklch(0.66 0.22 38)"/>
      <path d="M238,34 Q188,42 122,64" fill="none" stroke="oklch(0.76 0.16 75)" stroke-width="1.5" stroke-dasharray="4 3"/>
      <polygon points="236,34 252,27 248,39" fill="oklch(0.72 0.18 65)"/>
      <polygon points="204,41 218,35 214,45" fill="oklch(0.72 0.18 65)"/>
      <rect x="0" y="102" width="318" height="16" fill="oklch(0.14 0.02 255)"/>
      <text x="159" y="113" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9" fill="oklch(0.90 0.02 85)">DYMER FIVE-STOREY BLOCK HIT · RESCUERS DIG RUBBLE</text>
      <rect x="10" y="9" width="166" height="20" rx="2" fill="oklch(0.48 0.18 24)"/>
      <text x="93" y="23" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="11" fill="white">186 DRONES · 161 DOWNED</text>
    </svg>""",
    'us_house_lead': """
    <svg viewBox="0 0 318 112" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="318" height="112" fill="oklch(0.955 0.012 240)"/>
      <text x="16" y="18" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="oklch(0.24 0.02 250)">U.S. HOUSE OF REPRESENTATIVES · 435 SEATS</text>
      <!-- Hemicycle (left-center) -->
      <path d="M26,98 A68,68 0 0,1 162,98" fill="none" stroke="oklch(0.86 0.015 240)" stroke-width="18"/>
      <path d="M26,98 A68,68 0 0,1 124,37" fill="none" stroke="oklch(0.46 0.15 250)" stroke-width="18"/>
      <path d="M124,37 A68,68 0 0,1 162,98" fill="none" stroke="oklch(0.50 0.19 25)" stroke-width="18"/>
      <!-- 218 Majority dashed line at top center -->
      <line x1="94" y1="22" x2="94" y2="42" stroke="oklch(0.18 0.01 260)" stroke-width="1.8" stroke-dasharray="2.5 2"/>
      <text x="94" y="51" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="7.5" fill="oklch(0.28 0.02 250)">218 MAJ.</text>
      <!-- Capitol dome silhouette -->
      <rect x="74" y="83" width="40" height="15" fill="oklch(0.84 0.015 250)"/>
      <rect x="81" y="75" width="26" height="8" fill="oklch(0.76 0.015 250)"/>
      <path d="M82,75 Q94,58 106,75 Z" fill="oklch(0.68 0.02 250)"/>
      <line x1="94" y1="58" x2="94" y2="64" stroke="oklch(0.40 0.02 250)" stroke-width="1.6"/>
      <!-- Right-side stat card -->
      <rect x="182" y="24" width="126" height="78" rx="3" fill="white" stroke="oklch(0.82 0.02 245)" stroke-width="1.2"/>
      <text x="245" y="50" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="25" fill="oklch(0.46 0.15 250)">258+</text>
      <text x="245" y="64" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="oklch(0.20 0.02 260)">DEMOCRAT SEATS</text>
      <line x1="194" y1="71" x2="296" y2="71" stroke="oklch(0.88 0.01 250)" stroke-width="1"/>
      <text x="245" y="83" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="8.5" fill="oklch(0.48 0.18 24)">LARGEST SINCE 1992</text>
      <text x="245" y="95" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="700" font-size="8" fill="oklch(0.36 0.02 260)">NC RECOUNT FLIP</text>
    </svg>""",
    'benghazi_mini': """
    <svg viewBox="0 0 188 72" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="188" height="41" fill="oklch(0.90 0.02 220)"/>
      <rect y="41" width="188" height="31" fill="oklch(0.48 0.09 235)"/>
      <g transform="translate(18,34)">
        <polygon points="0,14 78,14 71,24 7,24" fill="oklch(0.22 0.02 250)"/>
        <rect x="18" y="6" width="20" height="8" fill="oklch(0.36 0.02 250)"/>
        <polygon points="46,14 55,-3 64,14" fill="oklch(0.62 0.21 35)"/>
        <circle cx="57" cy="-5" r="5" fill="oklch(0.38 0.01 260)" opacity="0.8"/>
      </g>
      <text x="142" y="51" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="13" fill="white">MERKURY</text>
      <text x="142" y="62" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="7.5" fill="oklch(0.94 0.03 85)">CORVETTE HIT</text>
    </svg>""",
    'hormuz_mini': """
    <svg viewBox="0 0 188 72" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="188" height="39" fill="oklch(0.92 0.025 85)"/>
      <rect y="39" width="188" height="33" fill="oklch(0.68 0.08 228)"/>
      <path d="M0 40 L44 40 L34 72 L0 72 Z" fill="oklch(0.80 0.05 78)"/>
      <text x="18" y="61" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="7.5" fill="oklch(0.32 0.03 65)">OMAN</text>
      <g transform="translate(46,33)">
        <path d="M0,11 L46,11 L40,18 L6,18 Z" fill="oklch(0.20 0.015 260)"/>
        <rect x="6" y="9" width="34" height="2" fill="oklch(0.48 0.18 24)"/>
        <polygon points="22,9 27,-2 32,9" fill="oklch(0.64 0.21 35)"/>
      </g>
      <g transform="translate(94,45)">
        <path d="M0,10 L36,10 L31,16 L5,16 Z" fill="oklch(0.20 0.015 260)"/>
        <polygon points="15,8 20,-2 25,8" fill="oklch(0.64 0.21 35)"/>
      </g>
      <text x="158" y="51" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="12.5" fill="white">3 HIT</text>
      <text x="158" y="63" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="7.5" fill="oklch(0.96 0.02 85)">TRAFFIC -65%</text>
    </svg>""",
    'indonesia_fire': """
    <svg viewBox="0 0 188 72" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="188" height="49" fill="oklch(0.92 0.02 85)"/>
      <rect y="49" width="188" height="23" fill="oklch(0.42 0.04 145)"/>
      <rect x="14" y="38" width="66" height="15" fill="oklch(0.38 0.02 250)"/>
      <polygon points="14,38 27,30 40,38 53,30 66,38 80,38" fill="oklch(0.32 0.02 250)"/>
      <rect x="20" y="43" width="8" height="5" fill="oklch(0.75 0.12 75)"/>
      <rect x="34" y="43" width="8" height="5" fill="oklch(0.75 0.12 75)"/>
      <circle cx="58" cy="28" r="6" fill="oklch(0.40 0.01 260)" opacity="0.78"/>
      <polygon points="46,41 58,27 70,41" fill="oklch(0.62 0.21 35)"/>
      <text x="134" y="43" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="15.5" fill="oklch(0.48 0.18 24)">3 DEAD</text>
      <text x="134" y="61" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9" fill="white">36 MISSING</text>
    </svg>""",
    'korea_resign': """
    <svg viewBox="0 0 188 72" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="188" height="72" fill="oklch(0.95 0.01 85)"/>
      <rect x="18" y="28" width="38" height="35" rx="2" fill="white" stroke="oklch(0.38 0.03 250)" stroke-width="1.3"/>
      <line x1="24" y1="36" x2="48" y2="36" stroke="oklch(0.72 0.02 250)" stroke-width="1.6"/>
      <line x1="24" y1="42" x2="48" y2="42" stroke="oklch(0.72 0.02 250)" stroke-width="1.6"/>
      <line x1="24" y1="48" x2="40" y2="48" stroke="oklch(0.72 0.02 250)" stroke-width="1.6"/>
      <rect x="44" y="46" width="22" height="16" rx="2" fill="oklch(0.46 0.15 250)"/>
      <text x="55" y="57.5" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="9.5" fill="white">AI</text>
      <text x="128" y="46" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="15" fill="oklch(0.48 0.18 24)">RESIGNS</text>
      <text x="128" y="59" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="700" font-size="8.5" fill="oklch(0.32 0.02 260)">EXAM CHEATING</text>
    </svg>""",
    'iran_power': """
    <svg viewBox="0 0 188 72" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="188" height="72" fill="oklch(0.94 0.015 80)"/>
      <path d="M36,63 L46,30 L56,63 M34,42 L58,42 M38,52 L54,52" fill="none" stroke="oklch(0.38 0.02 260)" stroke-width="2" stroke-linejoin="round"/>
      <polygon points="72,30 62,46 70,46 65,61 81,43 73,43" fill="oklch(0.70 0.16 78)"/>
      <line x1="60" y1="32" x2="80" y2="59" stroke="oklch(0.48 0.18 24)" stroke-width="2.4" stroke-linecap="round"/>
      <text x="134" y="46" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="16" fill="oklch(0.20 0.02 260)">2 HRS</text>
      <text x="134" y="58" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="8" fill="oklch(0.36 0.02 260)">DAILY BLACKOUT</text>
    </svg>""",
    'alcaraz_atp': """
    <svg viewBox="0 0 188 72" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="188" height="72" fill="oklch(0.44 0.11 235)"/>
      <path d="M24,32 H50 L46,48 Q37,54 28,48 Z" fill="oklch(0.82 0.16 82)"/>
      <rect x="35" y="51" width="4" height="8" fill="oklch(0.82 0.16 82)"/>
      <rect x="28" y="59" width="18" height="4" rx="1" fill="oklch(0.82 0.16 82)"/>
      <circle cx="66" cy="49" r="8" fill="oklch(0.86 0.18 100)"/>
      <path d="M60,44 Q66,49 60,54 M72,44 Q66,49 72,54" fill="none" stroke="white" stroke-width="1"/>
      <text x="132" y="46" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="14.5" fill="white">6–2, 7–6</text>
      <text x="132" y="59" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="700" font-size="8.5" fill="oklch(0.93 0.02 230)">ATP FINALS</text>
    </svg>""",
    'cricket_720': """
    <svg viewBox="0 0 188 72" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="188" height="72" fill="oklch(0.93 0.03 145)"/>
      <g stroke="oklch(0.55 0.08 65)" stroke-width="2.5" stroke-linecap="round">
        <line x1="22" y1="32" x2="22" y2="61"/>
        <line x1="29" y1="32" x2="29" y2="61"/>
        <line x1="36" y1="32" x2="36" y2="61"/>
      </g>
      <line x1="21" y1="31" x2="37" y2="31" stroke="oklch(0.45 0.06 60)" stroke-width="2"/>
      <line x1="48" y1="30" x2="58" y2="60" stroke="oklch(0.52 0.09 55)" stroke-width="4.5" stroke-linecap="round"/>
      <circle cx="70" cy="54" r="5.5" fill="oklch(0.48 0.18 24)"/>
      <text x="132" y="48" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="20" fill="oklch(0.18 0.01 260)">720/9</text>
      <text x="132" y="60" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="8" fill="oklch(0.32 0.03 145)">DECLARED · NZ</text>
    </svg>""",
    'hk_polls': """
    <svg viewBox="0 0 188 72" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="188" height="72" fill="oklch(0.95 0.012 210)"/>
      <rect x="24" y="40" width="44" height="23" rx="2" fill="white" stroke="oklch(0.38 0.04 240)" stroke-width="1.5"/>
      <line x1="32" y1="45" x2="60" y2="45" stroke="oklch(0.28 0.02 250)" stroke-width="2.2" stroke-linecap="round"/>
      <polygon points="39,28 53,28 53,45 39,45" fill="oklch(0.98 0.005 90)" stroke="oklch(0.46 0.12 195)" stroke-width="1.3"/>
      <path d="M42,36 L45,39 L50,33" fill="none" stroke="oklch(0.46 0.12 195)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="128" y="46" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="16.5" fill="oklch(0.48 0.12 195)">856</text>
      <text x="128" y="59" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="8" fill="oklch(0.24 0.02 260)">FOR 723 SEATS</text>
    </svg>""",
    'motogp_8': """
    <svg viewBox="0 0 188 72" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="188" height="72" fill="oklch(0.95 0.015 35)"/>
      <circle cx="28" cy="53" r="8" fill="none" stroke="oklch(0.24 0.02 260)" stroke-width="2.6"/>
      <circle cx="62" cy="53" r="8" fill="none" stroke="oklch(0.24 0.02 260)" stroke-width="2.6"/>
      <path d="M28,53 L41,40 L58,42 L62,53" fill="none" stroke="oklch(0.52 0.20 26)" stroke-width="3.6" stroke-linecap="round"/>
      <circle cx="48" cy="34" r="4" fill="oklch(0.24 0.02 260)"/>
      <line x1="80" y1="32" x2="80" y2="60" stroke="oklch(0.30 0.02 260)" stroke-width="1.6"/>
      <rect x="81" y="32" width="14" height="10" fill="white" stroke="oklch(0.24 0.02 260)" stroke-width="0.8"/>
      <rect x="81" y="32" width="7" height="5" fill="oklch(0.24 0.02 260)"/>
      <rect x="88" y="37" width="7" height="5" fill="oklch(0.24 0.02 260)"/>
      <text x="140" y="46" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="18" fill="oklch(0.20 0.02 260)">8TH</text>
      <text x="140" y="59" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="700" font-size="8.5" fill="oklch(0.40 0.04 26)">MOTOGP TITLE</text>
    </svg>""",
    'sudan_mine': """
    <svg viewBox="0 0 188 72" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <rect width="188" height="46" fill="oklch(0.92 0.025 82)"/>
      <rect y="46" width="188" height="26" fill="oklch(0.76 0.05 75)"/>
      <polygon points="30,56 44,32 58,56" fill="oklch(0.62 0.21 35)"/>
      <polygon points="36,56 44,41 52,56" fill="oklch(0.84 0.17 80)"/>
      <path d="M22,56 L30,49 M66,56 L58,49" stroke="oklch(0.32 0.03 55)" stroke-width="1.8" stroke-linecap="round"/>
      <text x="130" y="45" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="15.5" fill="oklch(0.48 0.18 24)">22 DEAD</text>
      <text x="130" y="59" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="800" font-size="8" fill="oklch(0.24 0.02 260)">LANDMINE BLAST</text>
    </svg>""",
}


def badge_html(status: str, kind: str) -> str:
    cls = 'badge-official' if kind == 'official' else 'badge-confirmed'
    return f'<span class="badge {cls}">{html.escape(status)}</span>'


def build_world_map_svg(pins: list[dict]) -> str:
    w, h = 364, 148

    def proj(lon: float, lat: float) -> tuple[float, float]:
        # Robinson-like pseudocylindrical projection (crisp Natural Earth look)
        lat_c = max(-58.0, min(83.0, lat))
        rad = math.radians(lat_c)
        x_scale = 0.8487 + 0.1513 * math.cos(rad * 1.15)
        px = w * 0.5 + ((lon / 180.0) * (w * 0.495) * x_scale)
        py = ((83.0 - lat_c) / 141.0) * (h - 6.0) + 3.0
        return max(4.0, min(w - 4.0, px)), max(4.0, min(h - 4.0, py))

    topo_path = Path('/tmp/countries-110m.json')
    country_paths = ''
    if topo_path.exists():
        topo = json.loads(topo_path.read_text(encoding='utf-8'))
        sx, sy = topo['transform']['scale']
        tx, ty = topo['transform']['translate']
        decoded_arcs: list[list[tuple[float, float]]] = []
        for arc in topo['arcs']:
            x = y = 0
            pts: list[tuple[float, float]] = []
            for dx, dy in arc:
                x += dx
                y += dy
                pts.append((x * sx + tx, y * sy + ty))
            decoded_arcs.append(pts)

        def ring_to_path(ring: list[int]) -> str:
            coords: list[tuple[float, float]] = []
            for idx in ring:
                pts = decoded_arcs[idx] if idx >= 0 else list(reversed(decoded_arcs[~idx]))
                if coords:
                    coords.extend(pts[1:])
                else:
                    coords.extend(pts)
            if len(coords) < 3:
                return ''
            segs: list[str] = []
            prev_lon = None
            for lon, lat in coords:
                if lat < -58.0:
                    lat = -58.0
                px, py = proj(lon, lat)
                if prev_lon is None or abs(lon - prev_lon) > 90.0:
                    segs.append(f'M{px:.1f},{py:.1f}')
                else:
                    segs.append(f'L{px:.1f},{py:.1f}')
                prev_lon = lon
            return ''.join(segs) + 'Z'

        parts: list[str] = []
        for geom in topo['objects']['countries']['geometries']:
            if geom.get('id') == '010':  # Exclude Antarctica
                continue
            gtype = geom.get('type')
            if gtype == 'Polygon':
                d = ''.join(ring_to_path(r) for r in geom['arcs'])
                if d:
                    parts.append(f'<path d="{d}"/>')
            elif gtype == 'MultiPolygon':
                d = ''.join(ring_to_path(r) for poly in geom['arcs'] for r in poly)
                if d:
                    parts.append(f'<path d="{d}"/>')
        country_paths = (
            '<g fill="oklch(0.915 0.015 85)" stroke="oklch(0.76 0.014 85)" '
            'stroke-width="0.48" stroke-linejoin="round">'
            + ''.join(parts)
            + '</g>'
        )

    grid_lines = ''
    for lat in (-30, 0, 30, 60):
        _, gy = proj(0, lat)
        grid_lines += f'<line x1="0" y1="{gy:.1f}" x2="{w}" y2="{gy:.1f}" stroke="oklch(0.89 0.012 225)" stroke-width="0.5" stroke-dasharray="2 2"/>'
    for lon in (-120, -60, 0, 60, 120):
        gx, _ = proj(lon, 0)
        grid_lines += f'<line x1="{gx:.1f}" y1="0" x2="{gx:.1f}" y2="{h}" stroke="oklch(0.89 0.012 225)" stroke-width="0.5" stroke-dasharray="2 2"/>'

    dot_els = ''
    pin_els = ''
    for p in pins:
        px, py = proj(p['lon'], p['lat'])
        col = REGION_OKLCH.get(p['r'], 'oklch(0.24 0.01 260)')
        if p.get('dot'):
            dot_els += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.2" fill="{col}" stroke="white" stroke-width="0.8"/>'
        else:
            pin_els += (
                f'<g transform="translate({px:.1f},{py:.1f})">'
                f'<circle r="6.2" fill="{col}" stroke="white" stroke-width="1"/>'
                f'<text y="2.8" text-anchor="middle" font-family="Roboto, sans-serif" font-weight="900" font-size="7.8" fill="white">{p["id"]}</text>'
                f'</g>'
            )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" xmlns="http://www.w3.org/2000/svg">'
        f'<rect width="{w}" height="{h}" fill="oklch(0.962 0.012 225)"/>{grid_lines}{country_paths}{dot_els}{pin_els}</svg>'
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
            <span class="meta-left">
              <span class="num-circle" style="background:{l["weight_color"]}">{html.escape(l["id"])}</span>
              <span class="loc-txt" style="color:{l["weight_color"]}">{html.escape(l["loc"])}</span>
            </span>
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
            <div class="mini-top">
              <span class="mini-top-left">
                <span class="num-circle-sm" style="background:{c["weight_color"]}">{html.escape(c["id"])}</span>
                <span class="mini-loc" style="color:{c["weight_color"]}">{html.escape(c["loc"])}</span>
              </span>
              {badge_html(c["status"], c["status_kind"])}
            </div>
            <div class="mini-svg-wrap">{SVGS[c["art"]]}</div>
          </div>
          <h3>{html.escape(c["title"])}</h3>
          <p>{html.escape(c["sub"])}</p>
        </article>'''
        for c in data['cards']
    )

    col1 = ''.join(
        f'<div class="brief"><span class="num-circle-xs" style="background:{b[3]}">{b[0]}</span> <span class="b-loc" style="color:{b[3]}">{html.escape(b[1])}:</span> {html.escape(b[2])}</div>'
        for b in data['briefs'][:10]
    )
    col2 = ''.join(
        f'<div class="brief"><span class="num-circle-xs" style="background:{b[3]}">{b[0]}</span> <span class="b-loc" style="color:{b[3]}">{html.escape(b[1])}:</span> {html.escape(b[2])}</div>'
        for b in data['briefs'][10:]
    )

    legend_html = ''.join(
        f'<span class="leg-item"><i style="background:{col}"></i>{name.title()}</span>'
        for name, col in REGION_OKLCH.items()
    )

    dc_escaped = html.escape(data['date_check'])
    for key in ('DATE CHECK', '(NOT SUN 22 NOV)', '(Fri 20 Nov)', '(Sat 21 Nov)', '(Fri/Sat)', '(Sat 18:24 UTC)'):
        dc_escaped = dc_escaped.replace(key, f'<span class="dc-key">{key}</span>')

    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&family=Source+Serif+4:opsz,wght@8..60,700;8..60,800;8..60,900&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg-paper: oklch(0.992 0.004 90);
    --bg-panel: oklch(0.962 0.005 85);
    --ink-primary: oklch(0.18 0.01 260);
    --ink-secondary: oklch(0.30 0.01 260);
    --ink-muted: oklch(0.46 0.01 260);
    --rule: oklch(0.18 0.01 260 / 0.14);
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
    padding: 6px 16px 5px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 10px;
  }}
  .eyebrow {{
    display: flex;
    justify-content: space-between;
    font-weight: 700;
    font-size: 12px;
    font-variant-numeric: tabular-nums;
    padding-bottom: 2px;
    border-bottom: 1px solid var(--ink-primary);
  }}
  .eyebrow-left {{ color: var(--scarlet); }}
  .eyebrow-right {{ color: var(--ink-primary); }}
  h1.masthead {{
    font-family: "Source Serif 4", Georgia, serif;
    font-weight: 900;
    font-size: 52px;
    line-height: 1.02;
    text-align: center;
    letter-spacing: -0.015em;
    padding: 4px 0;
  }}
  .deck {{
    text-align: center;
    font-size: 12px;
    font-weight: 500;
    color: var(--scarlet);
    padding-bottom: 2px;
    border-bottom: 2px solid var(--ink-primary);
  }}
  .kpi-strip {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 8px;
    padding: 2px 0;
    border-bottom: 1px solid var(--rule);
  }}
  .kpi-item {{
    padding-left: 6px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}
  .kpi-num {{
    font-weight: 900;
    font-size: 18px;
    line-height: 1.04;
    font-variant-numeric: tabular-nums;
    color: var(--scarlet);
  }}
  .kpi-lbl {{
    font-weight: 600;
    font-size: 12px;
    line-height: 1.12;
    color: var(--ink-secondary);
    margin-top: 1px;
  }}
  .reg-bar {{
    display: flex;
    gap: 2px;
    margin-top: 2px;
  }}
  .utc-strip {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 3px;
    padding: 3px 6px;
    background: var(--bg-panel);
    border-top: 1px solid var(--rule);
    border-bottom: 1px solid var(--rule);
    font-size: 12px;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
    overflow: hidden;
  }}
  .utc-label {{
    background: var(--ink-primary);
    color: white;
    font-weight: 800;
    font-size: 12px;
    padding: 1px 6px;
    border-radius: 2px;
    flex-shrink: 0;
  }}
  .utc-items {{
    display: flex;
    align-items: center;
    flex: 1;
    gap: 5px;
    color: var(--ink-secondary);
  }}
  .utc-node {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    flex-shrink: 0;
  }}
  .utc-dot {{
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--scarlet);
    border: 2px solid white;
    box-shadow: 0 0 0 1.2px oklch(0.62 0.01 260);
    flex-shrink: 0;
  }}
  .utc-line {{
    flex: 1;
    min-width: 10px;
    height: 1.5px;
    background: oklch(0.68 0.01 260);
  }}
  .utc-items b {{
    color: var(--scarlet);
    font-weight: 800;
  }}
  .reg-seg {{
    color: white;
    font-weight: 700;
    font-size: 12px;
    text-align: center;
    white-space: nowrap;
    padding: 2px 6px;
    border-radius: 2px;
  }}
  .leads {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    padding: 2px 0 4px;
    border-bottom: 1px solid var(--rule);
  }}
  .lead-art {{
    height: 108px;
    border: 1px solid var(--rule);
    overflow: hidden;
  }}
  .lead-art svg, .mini-svg-wrap svg {{
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
  .meta-left {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
  }}
  .num-circle {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    color: white;
    font-weight: 900;
    font-size: 12px;
    font-variant-numeric: tabular-nums;
  }}
  .loc-txt {{
    font-weight: 700;
    font-size: 12px;
  }}
  .badge {{
    font-weight: 900;
    font-size: 12px;
    color: white;
    padding: 1px 6px;
    border-radius: 2px;
    letter-spacing: 0.02em;
  }}
  .badge-confirmed {{ background: var(--badge-confirmed); }}
  .badge-official {{ background: var(--badge-official); }}
  .lead-card h2 {{
    font-family: "Source Serif 4", Georgia, serif;
    font-weight: 800;
    font-size: 20px;
    line-height: 1.06;
    margin-bottom: 2px;
  }}
  .lead-card p {{
    font-weight: 400;
    font-size: 14px;
    line-height: 1.2;
    color: var(--ink-secondary);
  }}
  .cards {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 4px 12px;
    padding: 1px 0 3px;
    border-bottom: 1px solid var(--rule);
  }}
  .mini-art {{
    position: relative;
    height: 72px;
    border: 1px solid var(--rule);
    overflow: hidden;
    background: white;
  }}
  .mini-top {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 5px;
    background: transparent;
  }}
  .mini-top-left {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    min-width: 0;
  }}
  .num-circle-sm {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    color: white;
    font-weight: 900;
    font-size: 12px;
    font-variant-numeric: tabular-nums;
    flex-shrink: 0;
  }}
  .mini-loc {{
    font-weight: 900;
    font-size: 12px;
    white-space: nowrap;
    overflow: hidden;
    background: oklch(0.992 0.004 90 / 0.88);
    padding: 0 4px;
    border-radius: 2px;
  }}
  .mini-top .badge {{
    font-size: 12px;
    font-weight: 900;
    padding: 1px 6px;
    line-height: 1.2;
  }}
  .mini-svg-wrap {{
    height: 72px;
    overflow: hidden;
  }}
  .mini-card h3 {{
    font-family: "Source Serif 4", Georgia, serif;
    font-weight: 800;
    font-size: 17px;
    line-height: 1.06;
    margin: 2px 0 1px;
  }}
  .mini-card p {{
    font-weight: 400;
    font-size: 14px;
    line-height: 1.16;
    color: var(--ink-secondary);
  }}
  .bottom {{
    display: grid;
    grid-template-columns: 364px 1fr;
    gap: 10px;
    align-items: start;
  }}
  .sec-hd {{
    display: flex;
    justify-content: flex-start;
    gap: 8px;
    align-items: center;
    margin-bottom: 3px;
  }}
  .sec-title {{
    background: var(--bg-panel);
    border-left: 3px solid var(--scarlet);
    padding: 1px 6px;
    font-weight: 800;
    font-size: 12px;
    color: var(--scarlet);
  }}
  .sec-sub {{
    font-weight: 600;
    font-size: 12px;
    color: var(--ink-secondary);
  }}
  .map-box {{
    border: 1px solid var(--rule);
    line-height: 0;
  }}
  .legend {{
    display: flex;
    flex-wrap: wrap;
    gap: 2px 8px;
    margin-top: 2px;
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
    font-size: 13px;
    line-height: 1.15;
    padding: 3.5px 0;
    border-bottom: 1px solid var(--rule);
    color: var(--ink-primary);
    white-space: nowrap;
    overflow: hidden;
  }}
  .num-circle-xs {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 17px;
    height: 17px;
    border-radius: 50%;
    color: white;
    font-weight: 500;
    font-size: 11px;
    font-variant-numeric: tabular-nums;
    vertical-align: middle;
  }}
  .b-loc {{
    font-weight: 700;
  }}
  .date-check {{
    background: var(--bg-panel);
    border: 2px solid var(--scarlet);
    border-left-width: 2px;
    padding: 4px 7px;
    margin-top: 3px;
    font-weight: 400;
    font-size: 12px;
    line-height: 1.2;
    color: var(--ink-primary);
  }}
  .dc-key {{
    font-weight: 600;
    color: var(--scarlet);
  }}
  .footer {{
    display: flex;
    justify-content: space-between;
    padding-top: 2px;
    font-size: 12px;
    font-weight: 600;
    color: var(--ink-primary);
  }}
  .footer-date {{
    font-weight: 800;
    color: var(--scarlet);
  }}
</style>
</head>
<body>
  <div class="page">
    <div>
      <div class="eyebrow">
        <span class="eyebrow-left">{html.escape(data["eyebrow_left"])}</span>
        <span class="eyebrow-left">DAY 326 OF 2026</span>
        <span class="eyebrow-right">{html.escape(data["eyebrow_right"])}</span>
      </div>
      <h1 class="masthead">{html.escape(data["masthead"])}</h1>
      <div class="deck">{html.escape(data["deck"])}</div>
      <div class="kpi-strip">{kpi_html}</div>
      <div class="reg-bar">{reg_html}</div>
      <div class="utc-strip">
        <span class="utc-label">THE DAY IN UTC</span>
        <div class="utc-items">
          <span class="utc-node"><i class="utc-dot"></i><b>01:00</b> HK polls</span>
          <i class="utc-line"></i>
          <span class="utc-node"><i class="utc-dot"></i><b>06:00</b> 186 drones</span>
          <i class="utc-line"></i>
          <span class="utc-node"><i class="utc-dot"></i><b>14:00</b> Márquez 8th</span>
          <i class="utc-line"></i>
          <span class="utc-node"><i class="utc-dot"></i><b>18:30</b> Alcaraz ATP</span>
          <i class="utc-line"></i>
          <span class="utc-node"><i class="utc-dot"></i><b>22:00</b> COP31 fails</span>
        </div>
      </div>
    </div>

    <div class="leads">{leads_html}</div>

    <div class="cards">{cards_html}</div>

    <div class="bottom">
      <div>
        <div class="sec-hd">
          <span class="sec-title">Where It Happened</span>
          <span class="sec-sub">Pins 1–13 · Dots 14–33</span>
        </div>
        <div class="map-box">{build_world_map_svg(data["pins"])}</div>
        <div class="legend">{legend_html}</div>
        <div class="date-check">{dc_escaped}</div>
      </div>
      <div>
        <div class="sec-hd">
          <span class="sec-title">Also on Sunday 22 November</span>
          <span class="sec-sub">20 More Stories</span>
        </div>
        <div class="briefs-grid">
          <div>{col1}</div>
          <div>{col2}</div>
        </div>
      </div>
    </div>

    <div class="footer">
      <span>REPORTED = confirmed; CLAIM = one side's claim · All <span class="footer-date">Sun 22 Nov 2026</span></span>
      <span>Sources: BBC, Reuters, AP, AFP, Al Jazeera, Xinhua, RIA, SCMP · Original vector art</span>
    </div>
  </div>
</body>
</html>'''
    out_html.write_text(page, encoding='utf-8')


if __name__ == '__main__':
    base = Path(__file__).resolve().parent
    generate_html(base / 'edition-data.json', base / 'index.html')
    print('Wrote index.html')
