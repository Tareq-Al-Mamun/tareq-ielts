#!/usr/bin/env python3
"""Generate TAREQ_IELTS_Speaking_Practice.html with embedded question data."""
import json
import html
import base64

DATA_FILE = "/home/z/my-project/scripts/data.json"
OUT_FILE = "/home/z/my-project/download/TAREQ_IELTS_Speaking_Practice.html"

with open(DATA_FILE, encoding="utf-8") as f:
    DATA = json.load(f)

# Compact JSON string for embedding
DATA_JS = json.dumps(DATA, ensure_ascii=False, separators=(",", ":"))

# All categories from cue cards
ALL_CATEGORIES = sorted({c for cc in DATA["part2"] for c in cc.get("categories", [])})

# ---- Embed the brand logo + contact photo as base64 data URIs ----
# Logo: optimized PNG of the TAREQ IELTS brand mark (graduation cap + soundwave)
# Photo: optimized JPEG headshot of the founder for the contact card on the dashboard
def _b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

LOGO_B64 = _b64("/home/z/my-project/scripts/logo_optimized.png")
PHOTO_B64 = _b64("/home/z/my-project/scripts/photo_square.jpg")
THUMB_B64 = _b64("/home/z/my-project/scripts/photo_thumb.jpg")
LOGO_DATA_URI = "data:image/png;base64," + LOGO_B64
PHOTO_DATA_URI = "data:image/jpeg;base64," + PHOTO_B64
THUMB_DATA_URI = "data:image/jpeg;base64," + THUMB_B64

# Build the HTML
HTML = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TAREQ IELTS — Speaking Practice Platform</title>
<style>
/* ============================================================
   TAREQ IELTS — Speaking Practice Platform
   Single-file HTML/CSS/JS application
   ============================================================ */
:root {
  --navy:        #14213D;
  --blue:        #2563EB;
  --blue-dark:   #1E40AF;
  --blue-light:  #DBEAFE;
  --bg:          #F5F7FB;
  --card:        #FFFFFF;
  --text:        #1F2937;
  --text-soft:   #6B7280;
  --border:      #E5E7EB;
  --green:       #16A34A;
  --green-bg:    #DCFCE7;
  --orange:      #EA580C;
  --orange-bg:   #FFEDD5;
  --red:         #DC2626;
  --red-bg:      #FEE2E2;
  --yellow:      #CA8A04;
  --yellow-bg:   #FEF9C3;
  --purple:      #7C3AED;
  --purple-bg:   #EDE9FE;
  --shadow:      0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.04);
  --shadow-lg:   0 4px 12px rgba(0,0,0,.08), 0 2px 4px rgba(0,0,0,.04);
  --radius:      10px;
  --radius-sm:   6px;
}
[data-theme="dark"] {
  --navy:        #0F172A;
  --blue:        #3B82F6;
  --blue-dark:   #2563EB;
  --blue-light:  #1E3A8A;
  --bg:          #0B1220;
  --card:        #131C2E;
  --text:        #E5E7EB;
  --text-soft:   #9CA3AF;
  --border:      #1F2937;
  --green-bg:    #052E16;
  --orange-bg:   #431407;
  --red-bg:      #450A0A;
  --yellow-bg:   #422006;
  --purple-bg:   #2E1065;
  --shadow:      0 1px 3px rgba(0,0,0,.4);
  --shadow-lg:   0 4px 12px rgba(0,0,0,.5);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  font-size: 15px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  transition: background .2s, color .2s;
}
button { font-family: inherit; cursor: pointer; border: none; background: none; color: inherit; }
a { color: var(--blue); text-decoration: none; }
input, textarea, select { font-family: inherit; font-size: 14px; }

/* ===== Layout ===== */
.app { display: flex; min-height: 100vh; }
.sidebar {
  width: 240px; background: var(--navy); color: #fff;
  display: flex; flex-direction: column; flex-shrink: 0;
  position: fixed; top: 0; bottom: 0; left: 0; z-index: 100;
  transition: transform .25s;
}
.sidebar .brand {
  padding: 14px 18px; font-size: 18px; font-weight: 700; letter-spacing: .3px;
  border-bottom: 1px solid rgba(255,255,255,.08);
  display: flex; align-items: center; gap: 10px;
}
.sidebar .brand .logo {
  width: 40px; height: 40px; border-radius: 8px;
  background: linear-gradient(135deg, var(--blue), #60A5FA);
  display: grid; place-items: center; font-size: 14px; font-weight: 800;
  overflow: hidden; flex-shrink: 0;
}
.sidebar .brand .logo img {
  width: 100%; height: 100%; object-fit: contain; display: block;
}
.sidebar .brand .sub { font-size: 11px; font-weight: 400; opacity: .65; letter-spacing: .2px; }
.sidebar .brand .brand-text { display: flex; flex-direction: column; line-height: 1.15; min-width: 0; }
.sidebar .brand .brand-text .brand-name { font-size: 16px; font-weight: 800; letter-spacing: .3px; }
.nav { flex: 1; padding: 12px 0; overflow-y: auto; }
.nav-item {
  display: flex; align-items: center; gap: 12px;
  padding: 11px 20px; color: rgba(255,255,255,.75); font-size: 14px;
  cursor: pointer; border-left: 3px solid transparent; transition: all .15s;
  width: 100%; text-align: left;
}
.nav-item:hover { background: rgba(255,255,255,.06); color: #fff; }
.nav-item.active { background: rgba(37,99,235,.18); color: #fff; border-left-color: var(--blue); }
.nav-item .icon { width: 18px; text-align: center; font-size: 15px; opacity: .9; }
.nav-item .count {
  margin-left: auto; font-size: 11px; padding: 2px 7px; border-radius: 10px;
  background: rgba(255,255,255,.12); color: rgba(255,255,255,.8);
}
.sidebar-footer {
  padding: 12px 20px; border-top: 1px solid rgba(255,255,255,.08);
  font-size: 11px; color: rgba(255,255,255,.55); line-height: 1.5;
}

.main {
  flex: 1; margin-left: 240px; padding: 28px 32px 60px;
  max-width: 100%; min-width: 0;
}
.page { display: none; }
.page.active { display: block; }
.page-header { margin-bottom: 22px; }
.page-header h1 { font-size: 24px; font-weight: 700; color: var(--text); }
.page-header .sub { color: var(--text-soft); font-size: 14px; margin-top: 4px; }

/* ===== Cards / Stats ===== */
.card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); box-shadow: var(--shadow); padding: 20px;
}
.card-hover:hover { box-shadow: var(--shadow-lg); transform: translateY(-1px); transition: all .15s; }

.stat-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 14px; margin-bottom: 24px;
}
.stat {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px 18px; box-shadow: var(--shadow);
}
.stat .label { font-size: 12px; color: var(--text-soft); text-transform: uppercase; letter-spacing: .5px; }
.stat .value { font-size: 26px; font-weight: 700; margin-top: 4px; color: var(--text); }
.stat .value.small { font-size: 18px; }
.stat .progress-bar {
  margin-top: 8px; height: 6px; background: var(--border); border-radius: 4px; overflow: hidden;
}
.stat .progress-bar .fill { height: 100%; background: var(--blue); transition: width .3s; }
.stat.green .fill { background: var(--green); }
.stat.orange .fill { background: var(--orange); }
.stat.purple .fill { background: var(--purple); }

/* ===== Dashboard nav cards ===== */
.nav-cards {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px; margin-bottom: 24px;
}
.nav-card {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 22px; box-shadow: var(--shadow); cursor: pointer;
  transition: all .15s; position: relative; overflow: hidden;
}
.nav-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-2px); border-color: var(--blue); }
.nav-card .badge {
  width: 46px; height: 46px; border-radius: 12px; display: grid; place-items: center;
  font-size: 22px; margin-bottom: 12px; color: #fff;
}
.nav-card.p1 .badge { background: linear-gradient(135deg, #2563EB, #60A5FA); }
.nav-card.p2 .badge { background: linear-gradient(135deg, #7C3AED, #A78BFA); }
.nav-card.p3 .badge { background: linear-gradient(135deg, #EA580C, #FB923C); }
.nav-card h3 { font-size: 17px; font-weight: 700; margin-bottom: 4px; }
.nav-card p { font-size: 13px; color: var(--text-soft); }
.nav-card .stats-mini {
  display: flex; gap: 14px; margin-top: 12px; font-size: 12px; color: var(--text-soft);
}
.nav-card .stats-mini b { color: var(--text); font-weight: 600; }

/* ============================================================
   PREMIUM FULL MOCK TEST BANNER (dashboard hero)
   Glassmorphism + animated gradient + glowing border + micro-anim
   ============================================================ */
.mock-hero {
  position: relative;
  margin-bottom: 24px;
  border-radius: 18px;
  overflow: hidden;
  isolation: isolate; /* keep blur layers contained */
  /* Glassmorphism base — works in both light & dark themes */
  background: linear-gradient(135deg, rgba(20, 33, 61, .96) 0%, rgba(30, 58, 138, .92) 50%, rgba(76, 29, 149, .92) 100%);
  /* Subtle outer glow */
  box-shadow: 0 10px 40px rgba(37, 99, 235, .25), 0 4px 12px rgba(0, 0, 0, .18), inset 0 1px 0 rgba(255, 255, 255, .08);
  border: 1px solid rgba(96, 165, 250, .25);
  /* Entrance animation */
  opacity: 0;
  transform: translateY(14px);
  animation: mockHeroEnter .7s cubic-bezier(.22, 1, .36, 1) .08s forwards;
  will-change: transform, opacity;
}
@keyframes mockHeroEnter {
  to { opacity: 1; transform: translateY(0); }
}

/* Animated gradient layer — slow drifting sheen across the surface */
.mock-hero::before {
  content: '';
  position: absolute; inset: -50%;
  background: conic-gradient(from 0deg at 50% 50%,
    rgba(96, 165, 250, 0) 0deg,
    rgba(96, 165, 250, .12) 60deg,
    rgba(167, 139, 250, .14) 120deg,
    rgba(96, 165, 250, 0) 200deg,
    rgba(251, 146, 60, .08) 280deg,
    rgba(96, 165, 250, 0) 360deg);
  animation: mockHeroSheen 16s linear infinite;
  z-index: 0;
  pointer-events: none;
}
@keyframes mockHeroSheen {
  to { transform: rotate(360deg); }
}

/* Moving light beam (diagonal sweep) */
.mock-hero::after {
  content: '';
  position: absolute; top: -50%; left: -60%;
  width: 40%; height: 200%;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(255, 255, 255, .08) 45%,
    rgba(255, 255, 255, .14) 50%,
    rgba(255, 255, 255, .08) 55%,
    transparent 100%);
  transform: rotate(18deg);
  animation: mockHeroBeam 7s ease-in-out infinite;
  z-index: 1;
  pointer-events: none;
  filter: blur(2px);
}
@keyframes mockHeroBeam {
  0%   { left: -60%; opacity: 0; }
  20%  { opacity: 1; }
  80%  { opacity: 1; }
  100% { left: 130%; opacity: 0; }
}

/* Inner content wrapper — sits above the ::before / ::after layers */
.mock-hero .mh-inner {
  position: relative; z-index: 2;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 24px;
  align-items: center;
  padding: 28px 32px;
}

/* Left column — text content */
.mock-hero .mh-text { min-width: 0; }
.mock-hero .mh-eyebrow {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 11px; font-weight: 700; letter-spacing: 1.6px;
  text-transform: uppercase; color: #BFDBFE;
  padding: 5px 11px; border-radius: 999px;
  background: rgba(96, 165, 250, .14); border: 1px solid rgba(96, 165, 250, .35);
  margin-bottom: 14px;
}
.mock-hero .mh-eyebrow .dot {
  width: 6px; height: 6px; border-radius: 50%; background: #60A5FA;
  box-shadow: 0 0 8px #60A5FA;
  animation: mhDotPulse 1.6s ease-in-out infinite;
}
@keyframes mhDotPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%      { opacity: .55; transform: scale(.85); }
}
.mock-hero h2.mh-title {
  font-size: 28px; line-height: 1.15; font-weight: 800;
  color: #fff; letter-spacing: -.3px;
  margin-bottom: 6px;
  background: linear-gradient(135deg, #FFFFFF 0%, #BFDBFE 70%, #A78BFA 100%);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
}
.mock-hero .mh-subtitle {
  font-size: 15px; color: #DBEAFE; font-weight: 500;
  margin-bottom: 8px;
}
.mock-hero .mh-desc {
  font-size: 13.5px; color: rgba(219, 234, 254, .82); line-height: 1.55;
  margin-bottom: 16px; max-width: 540px;
}
.mock-hero .mh-chips {
  display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 18px;
}
.mock-hero .mh-chip {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 11.5px; font-weight: 600; color: #E0E7FF;
  padding: 5px 10px; border-radius: 8px;
  background: rgba(255, 255, 255, .07);
  border: 1px solid rgba(255, 255, 255, .1);
  backdrop-filter: blur(4px);
}
.mock-hero .mh-chip .mh-chip-num {
  width: 18px; height: 18px; border-radius: 50%;
  display: grid; place-items: center; font-size: 10px; font-weight: 800;
  background: linear-gradient(135deg, #60A5FA, #A78BFA);
  color: #fff;
}

/* CTA button — large, premium, with hover lift + glow */
.mock-hero .mh-cta {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 14px 26px;
  font-size: 15px; font-weight: 700; letter-spacing: .3px;
  color: #fff;
  background: linear-gradient(135deg, #2563EB 0%, #1E40AF 50%, #7C3AED 100%);
  border: 1px solid rgba(255, 255, 255, .25);
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(37, 99, 235, .45), inset 0 1px 0 rgba(255, 255, 255, .25);
  transition: transform .25s cubic-bezier(.22, 1, .36, 1), box-shadow .25s, filter .25s;
  position: relative; overflow: hidden;
  white-space: nowrap;
}
.mock-hero .mh-cta::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, .25) 50%, transparent 100%);
  transform: translateX(-100%);
  transition: transform .8s ease;
}
.mock-hero .mh-cta:hover {
  transform: translateY(-2px) scale(1.015);
  box-shadow: 0 12px 32px rgba(37, 99, 235, .6), 0 0 0 4px rgba(96, 165, 250, .15), inset 0 1px 0 rgba(255, 255, 255, .35);
  filter: brightness(1.08);
}
.mock-hero .mh-cta:hover::before { transform: translateX(100%); }
.mock-hero .mh-cta:active { transform: translateY(0) scale(.99); }
.mock-hero .mh-cta .mh-cta-icon {
  font-size: 18px; display: inline-block;
  animation: mhMicFloat 3s ease-in-out infinite;
}
@keyframes mhMicFloat {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-3px); }
}

/* Right column — large floating microphone visual */
.mock-hero .mh-visual {
  display: grid; place-items: center;
  position: relative;
  min-width: 140px;
}
.mock-hero .mh-mic-wrap {
  position: relative;
  width: 120px; height: 120px;
  display: grid; place-items: center;
}
.mock-hero .mh-mic-ring {
  position: absolute; inset: 0;
  border-radius: 50%;
  border: 1.5px solid rgba(96, 165, 250, .35);
  animation: mhRingPulse 3.5s ease-out infinite;
}
.mock-hero .mh-mic-ring:nth-child(2) { animation-delay: 1.2s; }
.mock-hero .mh-mic-ring:nth-child(3) { animation-delay: 2.4s; }
@keyframes mhRingPulse {
  0%   { transform: scale(.6); opacity: .9; border-color: rgba(96, 165, 250, .55); }
  100% { transform: scale(1.55); opacity: 0; border-color: rgba(167, 139, 250, 0); }
}
.mock-hero .mh-mic-core {
  position: relative; z-index: 2;
  width: 84px; height: 84px;
  border-radius: 50%;
  display: grid; place-items: center;
  background: radial-gradient(circle at 30% 30%, #60A5FA 0%, #2563EB 55%, #1E40AF 100%);
  box-shadow: 0 0 30px rgba(96, 165, 250, .55), 0 8px 22px rgba(0, 0, 0, .35), inset 0 -3px 8px rgba(0, 0, 0, .25), inset 0 2px 4px rgba(255, 255, 255, .3);
  font-size: 38px;
  animation: mhMicBob 4s ease-in-out infinite;
}
@keyframes mhMicBob {
  0%, 100% { transform: translateY(0) rotate(-2deg); }
  50%      { transform: translateY(-6px) rotate(2deg); }
}

/* ===== Responsive — tablet ===== */
@media (max-width: 880px) {
  .mock-hero .mh-inner { grid-template-columns: 1fr; padding: 24px; gap: 18px; }
  .mock-hero .mh-visual { order: -1; min-width: 0; }
  .mock-hero .mh-mic-wrap { width: 96px; height: 96px; }
  .mock-hero .mh-mic-core { width: 68px; height: 68px; font-size: 30px; }
  .mock-hero h2.mh-title { font-size: 24px; }
  .mock-hero .mh-desc { font-size: 13px; }
  .mock-hero .mh-cta { width: 100%; justify-content: center; padding: 15px 20px; font-size: 15px; }
}

/* ===== Responsive — mobile ===== */
@media (max-width: 560px) {
  .mock-hero .mh-inner { padding: 20px 16px; }
  .mock-hero h2.mh-title { font-size: 21px; }
  .mock-hero .mh-subtitle { font-size: 13px; }
  .mock-hero .mh-desc { font-size: 12.5px; }
  .mock-hero .mh-eyebrow { font-size: 10px; letter-spacing: 1.2px; padding: 4px 9px; }
  .mock-hero .mh-chip { font-size: 10.5px; padding: 4px 8px; }
  .mock-hero .mh-cta { padding: 14px 16px; font-size: 14px; gap: 8px; }
  .mock-hero .mh-mic-wrap { width: 80px; height: 80px; }
  .mock-hero .mh-mic-core { width: 58px; height: 58px; font-size: 26px; }
}

/* ===== Reduced motion — disable ALL non-essential animation ===== */
@media (prefers-reduced-motion: reduce) {
  .mock-hero,
  .mock-hero::before,
  .mock-hero::after,
  .mock-hero .mh-eyebrow .dot,
  .mock-hero .mh-cta,
  .mock-hero .mh-cta::before,
  .mock-hero .mh-cta-icon,
  .mock-hero .mh-mic-ring,
  .mock-hero .mh-mic-core {
    animation: none !important;
  }
  .mock-hero {
    opacity: 1 !important;
    transform: none !important;
  }
}

/* ============================================================
   FOUNDER CONTACT CARD (dashboard)
   Shows the founder's photo + WhatsApp number + Facebook link.
   Subtle, on-brand, sits below the mock-test hero banner.
   ============================================================ */
.founder-card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 16px;
  align-items: center;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 24px;
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
}
.founder-card::before {
  content: '';
  position: absolute; top: 0; left: 0; bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #25D366 0%, #128C7E 50%, #1877F2 100%);
}
.founder-photo {
  width: 64px; height: 64px;
  border-radius: 50%;
  object-fit: cover; object-position: center top;
  border: 2px solid var(--border);
  flex-shrink: 0;
  background: var(--bg);
}
.founder-info { min-width: 0; }
.founder-info .fc-label {
  font-size: 10.5px; font-weight: 700; letter-spacing: 1.2px;
  text-transform: uppercase; color: var(--text-soft); margin-bottom: 4px;
}
.founder-info .fc-name {
  font-size: 16px; font-weight: 700; color: var(--text);
  display: inline-flex; align-items: center; gap: 6px; flex-wrap: wrap;
  margin-bottom: 4px;
}
.founder-info .fc-name a {
  color: var(--blue); text-decoration: none;
  display: inline-flex; align-items: center; gap: 4px;
  border-bottom: 1.5px solid transparent;
  transition: border-color .15s, color .15s;
}
.founder-info .fc-name a:hover { border-bottom-color: var(--blue); }
.founder-info .fc-name .fb-ico {
  width: 16px; height: 16px;
  display: inline-grid; place-items: center;
  border-radius: 50%; background: #1877F2; color: #fff;
  font-size: 9px; font-weight: 800;
}
.founder-info .fc-tagline {
  font-size: 12.5px; color: var(--text-soft); line-height: 1.5;
}
.founder-actions {
  display: flex; flex-direction: column; gap: 8px;
  align-items: stretch; min-width: 0;
}
.founder-actions .fc-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 9px 14px; border-radius: 10px;
  font-size: 13px; font-weight: 600;
  border: 1px solid transparent; cursor: pointer;
  text-decoration: none; white-space: nowrap;
  transition: transform .15s, box-shadow .15s, filter .15s;
}
.founder-actions .fc-btn:hover { transform: translateY(-1px); filter: brightness(1.05); }
.founder-actions .fc-btn:active { transform: translateY(0); }
.founder-actions .fc-wa {
  background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
  color: #fff;
  box-shadow: 0 4px 12px rgba(37, 211, 102, .25);
}
.founder-actions .fc-wa .fc-wa-ico {
  width: 18px; height: 18px; flex-shrink: 0;
}
.founder-actions .fc-fb {
  background: #1877F2; color: #fff;
  box-shadow: 0 4px 12px rgba(24, 119, 242, .25);
}
.founder-actions .fc-fb .fc-fb-ico {
  width: 16px; height: 16px; flex-shrink: 0;
  background: #fff; color: #1877F2;
  border-radius: 50%; display: grid; place-items: center;
  font-size: 10px; font-weight: 800;
}
@media (max-width: 700px) {
  .founder-card { grid-template-columns: auto 1fr; padding: 14px; gap: 12px; }
  .founder-actions {
    grid-column: 1 / -1;
    flex-direction: row; flex-wrap: wrap; justify-content: stretch;
  }
  .founder-actions .fc-btn { flex: 1 1 auto; justify-content: center; min-width: 140px; }
  .founder-photo { width: 56px; height: 56px; }
}
@media (max-width: 420px) {
  .founder-card { grid-template-columns: auto 1fr; }
  .founder-photo { width: 48px; height: 48px; }
  .founder-info .fc-name { font-size: 14px; }
  .founder-info .fc-tagline { font-size: 11.5px; }
  .founder-actions .fc-btn { font-size: 12px; padding: 8px 10px; }
}

/* ===== Buttons ===== */
.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 14px; border-radius: var(--radius-sm); font-size: 13px; font-weight: 500;
  background: var(--card); border: 1px solid var(--border); color: var(--text);
  transition: all .15s; cursor: pointer; white-space: nowrap;
}
.btn:hover { background: var(--bg); border-color: var(--text-soft); }
.btn.primary { background: var(--blue); color: #fff; border-color: var(--blue); }
.btn.primary:hover { background: var(--blue-dark); }
.btn.success { background: var(--green); color: #fff; border-color: var(--green); }
.btn.warning { background: var(--orange); color: #fff; border-color: var(--orange); }
.btn.danger { background: var(--red); color: #fff; border-color: var(--red); }
.btn.sm { padding: 5px 10px; font-size: 12px; }
.btn.icon-btn { padding: 6px 8px; font-size: 14px; }
.btn.active { background: var(--blue); color: #fff; border-color: var(--blue); }
.btn-row { display: flex; flex-wrap: wrap; gap: 8px; }

/* ===== Forms ===== */
.input, .textarea, .select {
  width: 100%; padding: 8px 12px; border: 1px solid var(--border); border-radius: var(--radius-sm);
  background: var(--card); color: var(--text); font-size: 14px;
}
.input:focus, .textarea:focus, .select:focus { outline: none; border-color: var(--blue); box-shadow: 0 0 0 3px rgba(37,99,235,.12); }
.textarea { resize: vertical; min-height: 80px; font-family: inherit; }
.field { margin-bottom: 12px; }
.field label { display: block; font-size: 12px; color: var(--text-soft); margin-bottom: 4px; font-weight: 500; }

/* ===== Question card ===== */
.q-card {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px 18px; margin-bottom: 10px; box-shadow: var(--shadow); transition: all .15s;
}
.q-card:hover { box-shadow: var(--shadow-lg); }
.q-card.completed { border-left: 4px solid var(--green); }
.q-card.bookmarked { border-left: 4px solid var(--yellow); }
.q-card.revision { border-left: 4px solid var(--orange); }
.q-card.mastered { border-left: 4px solid var(--purple); }
.q-card .q-head {
  display: flex; align-items: flex-start; gap: 10px; margin-bottom: 8px;
}
.q-card .q-num {
  flex-shrink: 0; width: 26px; height: 26px; border-radius: 50%;
  background: var(--blue-light); color: var(--blue-dark); font-size: 12px; font-weight: 700;
  display: grid; place-items: center;
}
[data-theme="dark"] .q-card .q-num { background: var(--blue-light); color: #BFDBFE; }
.q-card .q-text { flex: 1; font-size: 15px; line-height: 1.55; color: var(--text); }
.q-card .q-meta { display: flex; gap: 8px; align-items: center; margin-top: 10px; flex-wrap: wrap; }
.q-card .status-pill {
  font-size: 11px; padding: 2px 8px; border-radius: 10px; font-weight: 500;
}
.status-pill.not-practised { background: var(--border); color: var(--text-soft); }
.status-pill.practised { background: var(--green-bg); color: var(--green); }
.status-pill.needs-revision { background: var(--orange-bg); color: var(--orange); }
.status-pill.mastered { background: var(--purple-bg); color: var(--purple); }

.notes-area {
  margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--border);
  display: none;
}
.notes-area.open { display: block; }

/* ===== Answer area (sample answers from the book) ===== */
.answer-area {
  margin-top: 10px; padding: 12px 14px; border-radius: var(--radius-sm);
  background: var(--bg); border-left: 3px solid var(--blue);
  display: none;
}
.answer-area.open { display: block; }
.answer-area .answer-label {
  font-size: 12px; font-weight: 600; color: var(--blue); margin-bottom: 6px;
  text-transform: uppercase; letter-spacing: .3px;
}
.answer-area .answer-text {
  font-size: 14px; line-height: 1.7; color: var(--text); white-space: pre-wrap;
}

/* ===== Audio Recording UI ===== */
.recorder-block {
  margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--border);
}
.recorder-controls {
  display: flex; flex-wrap: wrap; gap: 6px; align-items: center;
}
.rec-btn {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 6px 12px; border-radius: var(--radius-sm); font-size: 12px; font-weight: 500;
  border: 1px solid var(--border); background: var(--card); color: var(--text);
  cursor: pointer; transition: all .15s; white-space: nowrap;
}
.rec-btn:hover { background: var(--bg); }
.rec-btn.rec-start { background: #DC2626; color: #fff; border-color: #DC2626; }
.rec-btn.rec-start:hover { background: #B91C1C; }
.rec-btn.rec-stop { background: #DC2626; color: #fff; border-color: #DC2626; }
.rec-btn.rec-stop:hover { background: #B91C1C; }
.rec-btn:disabled { opacity: .4; cursor: not-allowed; }
.rec-btn.rec-active { animation: pulse-rec 1.5s infinite; }
@keyframes pulse-rec {
  0%, 100% { box-shadow: 0 0 0 0 rgba(220,38,38,.4); }
  50% { box-shadow: 0 0 0 6px rgba(220,38,38,0); }
}
.rec-indicator {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 12px; color: #DC2626; font-weight: 600;
}
.rec-dot {
  width: 8px; height: 8px; border-radius: 50%; background: #DC2626;
  animation: blink 1s infinite;
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: .3; } }
.rec-duration {
  font-size: 13px; font-variant-numeric: tabular-nums; color: var(--text);
  font-weight: 600; min-width: 50px;
}
.waveform-container {
  margin-top: 8px; height: 40px; background: var(--bg); border-radius: var(--radius-sm);
  overflow: hidden; position: relative;
}
.waveform-canvas { width: 100%; height: 100%; display: block; }
.transcript-area {
  margin-top: 8px;
}
.transcript-text {
  font-size: 13px; line-height: 1.6; color: var(--text);
  background: var(--bg); padding: 10px 12px; border-radius: var(--radius-sm);
  min-height: 40px; border: 1px solid var(--border);
}
.transcript-text:empty::before {
  content: "Live transcript will appear here as you speak...";
  color: var(--text-soft); font-style: italic;
}
.rec-audio-player {
  margin-top: 8px; width: 100%;
}
.rec-status {
  font-size: 11px; color: var(--text-soft); margin-top: 4px;
}

/* ===== AI Evaluation Results Dashboard ===== */
.eval-band-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px; margin: 16px 0;
}
.eval-band-card {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px; text-align: center; box-shadow: var(--shadow);
}
.eval-band-card .criterion-name {
  font-size: 11px; color: var(--text-soft); text-transform: uppercase; letter-spacing: .5px;
  margin-bottom: 6px;
}
.eval-band-circle {
  width: 60px; height: 60px; border-radius: 50%; margin: 0 auto 8px;
  display: grid; place-items: center; font-size: 20px; font-weight: 800; color: #fff;
  position: relative;
}
.eval-band-circle.high { background: linear-gradient(135deg, #16A34A, #22C55E); }
.eval-band-circle.mid { background: linear-gradient(135deg, #2563EB, #3B82F6); }
.eval-band-circle.low { background: linear-gradient(135deg, #EA580C, #F97316); }
.eval-overall {
  text-align: center; margin: 20px 0; padding: 24px;
  background: linear-gradient(135deg, var(--navy), #1E3A5F); border-radius: var(--radius); color: #fff;
}
.eval-overall .overall-score {
  font-size: 48px; font-weight: 800; line-height: 1;
}
.eval-overall .overall-label {
  font-size: 13px; opacity: .8; margin-top: 4px;
}
.eval-feedback-section {
  margin-top: 16px;
}
.eval-feedback-section h4 {
  font-size: 14px; font-weight: 600; color: var(--text); margin-bottom: 8px;
  padding-bottom: 6px; border-bottom: 2px solid var(--blue);
}
.eval-correction {
  background: var(--bg); border-radius: var(--radius-sm); padding: 10px 12px; margin-bottom: 8px;
  font-size: 13px; line-height: 1.6;
}
.eval-correction .orig { color: #DC2626; text-decoration: line-through; }
.eval-correction .corr { color: #16A34A; font-weight: 500; }
.eval-correction .expl { color: var(--text-soft); font-size: 12px; margin-top: 4px; }
.eval-strength-weakness {
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 12px 0;
}
.eval-strength-weakness .sw-card {
  padding: 12px; border-radius: var(--radius-sm); font-size: 13px; line-height: 1.6;
}
.eval-strength-weakness .sw-card.strengths { background: var(--green-bg); }
.eval-strength-weakness .sw-card.weaknesses { background: var(--orange-bg); }
.eval-strength-weakness .sw-card h5 { font-size: 12px; font-weight: 700; margin-bottom: 6px; text-transform: uppercase; }
.eval-strength-weakness .sw-card.strengths h5 { color: var(--green); }
.eval-strength-weakness .sw-card.weaknesses h5 { color: var(--orange); }
.eval-strength-weakness .sw-card ul { margin: 0; padding-left: 18px; }
.eval-strength-weakness .sw-card li { margin-bottom: 3px; }
.eval-disclaimer {
  background: var(--yellow-bg); border-radius: var(--radius-sm); padding: 10px 14px;
  font-size: 12px; color: var(--yellow); margin-top: 16px; text-align: center;
}
.eval-question-item {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 14px; margin-bottom: 10px; box-shadow: var(--shadow);
}
.eval-question-item .eq-head {
  display: flex; gap: 10px; align-items: flex-start; margin-bottom: 6px;
}
.eval-question-item .eq-band {
  flex-shrink: 0; width: 36px; height: 36px; border-radius: 8px;
  display: grid; place-items: center; font-weight: 700; font-size: 14px; color: #fff;
}
.eval-question-item .eq-text { flex: 1; font-size: 13px; line-height: 1.5; }
.eval-question-item .eq-transcript {
  font-size: 12px; color: var(--text-soft); margin-top: 6px; padding: 8px 10px;
  background: var(--bg); border-radius: var(--radius-sm); line-height: 1.5;
  max-height: 80px; overflow-y: auto;
}
.eval-chart-bar {
  display: flex; align-items: center; gap: 10px; margin-bottom: 8px;
}
.eval-chart-bar .label { font-size: 12px; width: 140px; text-align: right; color: var(--text-soft); }
.eval-chart-bar .bar-container { flex: 1; height: 20px; background: var(--bg); border-radius: 4px; overflow: hidden; }
.eval-chart-bar .bar-fill { height: 100%; border-radius: 4px; transition: width .5s; }
.eval-chart-bar .score { font-size: 13px; font-weight: 700; width: 40px; }
.server-status {
  display: inline-flex; align-items: center; gap: 5px; font-size: 11px; padding: 3px 8px;
  border-radius: 10px; font-weight: 500;
}
.server-status.online { background: var(--green-bg); color: var(--green); }
.server-status.offline { background: var(--orange-bg); color: var(--orange); }

/* ===== Mock Test Interface ===== */
.mock-welcome {
  text-align: center; padding: 40px 20px;
}
.mock-welcome .icon-big { font-size: 64px; margin-bottom: 16px; }
.mock-welcome h2 { font-size: 22px; margin-bottom: 8px; }
.mock-welcome p { color: var(--text-soft); font-size: 14px; max-width: 450px; margin: 0 auto 20px; line-height: 1.6; }
.mock-timer-display {
  font-size: 56px; font-weight: 800; font-variant-numeric: tabular-nums; color: var(--text);
  line-height: 1; text-align: center;
}
.mock-timer-display.warning { color: var(--orange); }
.mock-timer-display.danger { color: var(--red); animation: blink 0.5s infinite; }
.mock-timer-label {
  font-size: 13px; color: var(--text-soft); text-transform: uppercase; letter-spacing: .5px;
  text-align: center; margin-bottom: 8px;
}
.mock-progress-bar {
  height: 6px; background: var(--border); border-radius: 4px; overflow: hidden; margin: 12px 0;
}
.mock-progress-bar .fill { height: 100%; background: var(--blue); transition: width .3s; }
.mock-progress-label {
  font-size: 13px; color: var(--text-soft); text-align: center; margin-bottom: 16px;
}
.mock-question-display {
  font-size: 20px; font-weight: 600; line-height: 1.5; text-align: center;
  padding: 24px; background: var(--bg); border-radius: var(--radius); margin: 16px 0;
}
.mock-cue-card-display {
  background: var(--bg); border-radius: var(--radius); padding: 20px; margin: 16px 0;
  border: 2px solid var(--blue);
}
.mock-cue-card-display .cue-title { font-size: 17px; font-weight: 700; margin-bottom: 10px; text-align: center; }
.mock-cue-card-display .cue-bullets { list-style: none; padding: 0; }
.mock-cue-card-display .cue-bullets li {
  padding: 4px 0 4px 20px; position: relative; font-size: 14px;
}
.mock-cue-card-display .cue-bullets li::before {
  content: "▸"; position: absolute; left: 4px; color: var(--blue); font-weight: bold;
}
.mock-transcript-preview {
  font-size: 13px; color: var(--text-soft); padding: 10px 12px; background: var(--bg);
  border-radius: var(--radius-sm); margin-top: 8px; max-height: 100px; overflow-y: auto;
  line-height: 1.5;
}
.mock-phase-badge {
  display: inline-block; padding: 4px 12px; border-radius: 14px; font-size: 12px; font-weight: 600;
  background: var(--blue-light); color: var(--blue-dark); margin-bottom: 8px;
}
[data-theme="dark"] .mock-phase-badge { background: var(--blue-light); color: #BFDBFE; }
.mock-test-result {
  text-align: center;
}
.mock-part-analysis {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 16px 0;
}
.mock-part-card {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 14px; text-align: center;
}
.mock-part-card .part-name { font-size: 11px; color: var(--text-soft); text-transform: uppercase; margin-bottom: 4px; }
.mock-part-card .part-score { font-size: 24px; font-weight: 800; }
.mock-history-item {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px; margin-bottom: 12px; box-shadow: var(--shadow); cursor: pointer; transition: all .12s;
}
.mock-history-item:hover { box-shadow: var(--shadow-lg); border-color: var(--blue); }
.mock-history-item .mhi-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.mock-history-item .mhi-date { font-size: 13px; color: var(--text-soft); }
.mock-history-item .mhi-band {
  font-size: 24px; font-weight: 800; padding: 4px 12px; border-radius: 8px; color: #fff;
}
.mock-history-item .mhi-meta { font-size: 12px; color: var(--text-soft); display: flex; gap: 12px; }
.mock-history-detail {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px; margin-bottom: 12px;
}

/* ============================================================
   GEMINI AUTO-EVALUATION UI — inline per-question result,
   loading animation, improvement plan, history page
   ============================================================ */
/* Inline evaluation result block inside each question card */
.q-eval-result {
  margin-top: 12px; padding: 14px 16px;
  background: linear-gradient(135deg, rgba(37,99,235,.04), rgba(124,58,237,.04));
  border: 1px solid var(--border); border-left: 4px solid var(--blue);
  border-radius: var(--radius); font-size: 13px;
}
[data-theme="dark"] .q-eval-result { background: linear-gradient(135deg, rgba(37,99,235,.08), rgba(124,58,237,.08)); }
.q-eval-result.eval-failed { border-left-color: #DC2626; background: var(--red-bg); }
.q-eval-result.eval-loading { border-left-color: var(--yellow); background: var(--yellow-bg); }
.q-eval-head { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap; }
.q-eval-band {
  font-size: 22px; font-weight: 800; padding: 4px 12px; border-radius: 8px; color: #fff;
  background: linear-gradient(135deg, #2563EB, #7C3AED); min-width: 52px; text-align: center;
}
.q-eval-band.band-high { background: linear-gradient(135deg, #16A34A, #22C55E); }
.q-eval-band.band-mid  { background: linear-gradient(135deg, #2563EB, #3B82F6); }
.q-eval-band.band-low { background: linear-gradient(135deg, #EA580C, #F97316); }
.q-eval-band.band-fail { background: linear-gradient(135deg, #DC2626, #EF4444); }
.q-eval-title { font-weight: 700; font-size: 14px; flex: 1; min-width: 0; }
.q-eval-meta { font-size: 11px; color: var(--text-soft); margin-left: auto; }
.q-eval-criteria-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 10px; }
.q-eval-crit {
  text-align: center; padding: 8px 6px; background: var(--card);
  border: 1px solid var(--border); border-radius: 6px;
}
.q-eval-crit .crit-label { font-size: 10px; color: var(--text-soft); text-transform: uppercase; letter-spacing: .3px; }
.q-eval-crit .crit-score { font-size: 16px; font-weight: 700; margin-top: 2px; }
.q-eval-crit .crit-score.score-high { color: #16A34A; }
.q-eval-crit .crit-score.score-mid { color: #2563EB; }
.q-eval-crit .crit-score.score-low { color: #EA580C; }
.q-eval-crit .crit-score.score-na { color: var(--text-soft); font-size: 13px; }
.q-eval-toggle {
  font-size: 12px; color: var(--blue); cursor: pointer; margin-top: 4px;
  display: inline-flex; align-items: center; gap: 4px; user-select: none;
}
.q-eval-toggle:hover { text-decoration: underline; }
.q-eval-detail { margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--border); display: none; }
.q-eval-detail.open { display: block; }
.q-eval-actions { display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap; }

/* Loading animation — three bouncing dots */
.eval-loading-anim { display: inline-flex; align-items: center; gap: 4px; margin-left: 8px; }
.eval-loading-anim .dot {
  width: 7px; height: 7px; border-radius: 50%; background: var(--blue);
  animation: eval-bounce 1.4s infinite ease-in-out both;
}
.eval-loading-anim .dot:nth-child(1) { animation-delay: -.32s; }
.eval-loading-anim .dot:nth-child(2) { animation-delay: -.16s; }
@keyframes eval-bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: .4; }
  40%           { transform: scale(1.0); opacity: 1; }
}

/* Improvement plan */
.eval-improvement-plan {
  margin-top: 12px; padding: 14px 16px; background: var(--card);
  border: 1px solid var(--border); border-left: 4px solid var(--purple);
  border-radius: var(--radius);
}
.eval-improvement-plan h4 {
  font-size: 14px; font-weight: 700; color: var(--purple); margin-bottom: 10px;
  text-transform: uppercase; letter-spacing: .5px;
}
.eval-improvement-plan .ip-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 10px; }
.eval-improvement-plan .ip-section h5 {
  font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 6px; letter-spacing: .3px;
}
.eval-improvement-plan .ip-section.weaknesses h5 { color: var(--orange); }
.eval-improvement-plan .ip-section.strengths h5 { color: var(--green); }
.eval-improvement-plan .ip-section ul { margin: 0; padding-left: 18px; font-size: 12.5px; line-height: 1.6; }
.eval-improvement-plan .ip-exercises { font-size: 12.5px; line-height: 1.7; padding-left: 18px; margin: 6px 0; }
.eval-improvement-plan .ip-tips {
  background: var(--blue-light); padding: 8px 12px; border-radius: 6px; font-size: 12.5px; line-height: 1.6;
}
[data-theme="dark"] .eval-improvement-plan .ip-tips { background: rgba(37,99,235,.15); }

/* Fluency + Pronunciation feedback sub-sections */
.eval-fluency-feedback, .eval-pron-feedback {
  margin-top: 10px; padding: 10px 12px; border-radius: 6px; font-size: 12.5px; line-height: 1.6;
}
.eval-fluency-feedback { background: var(--blue-light); }
.eval-pron-feedback { background: var(--purple-bg); }
[data-theme="dark"] .eval-fluency-feedback { background: rgba(37,99,235,.15); }
[data-theme="dark"] .eval-pron-feedback { background: rgba(124,58,237,.15); }
.eval-fluency-feedback h5, .eval-pron-feedback h5 { font-size: 12px; font-weight: 700; margin-bottom: 6px; text-transform: uppercase; }
.eval-fluency-feedback h5 { color: var(--blue-dark); }
.eval-pron-feedback h5 { color: var(--purple); }
.eval-fluency-feedback ul, .eval-pron-feedback ul { margin: 4px 0 0 0; padding-left: 18px; }
.eval-pron-feedback .na-notice {
  font-style: italic; color: var(--text-soft); font-size: 12px;
  padding: 4px 8px; background: var(--bg); border-radius: 4px;
}

/* Vocabulary improvement card */
.eval-vocab-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 6px;
  padding: 10px 12px; margin-bottom: 8px;
}
.eval-vocab-card .vc-head { font-size: 13px; margin-bottom: 4px; }
.eval-vocab-card .vc-head .orig { color: #DC2626; text-decoration: line-through; }
.eval-vocab-card .vc-head .corr { color: #16A34A; font-weight: 600; }
.eval-vocab-card .vc-reason { font-size: 12px; color: var(--text-soft); margin-top: 4px; line-height: 1.5; }
.eval-vocab-card .vc-collocations {
  font-size: 11px; color: var(--blue-dark); margin-top: 4px;
  background: var(--blue-light); padding: 4px 8px; border-radius: 4px; display: inline-block;
}
[data-theme="dark"] .eval-vocab-card .vc-collocations { background: rgba(37,99,235,.15); color: #BFDBFE; }
.eval-vocab-card .vc-example {
  font-size: 12px; color: var(--text); margin-top: 4px; font-style: italic;
  padding-left: 8px; border-left: 2px solid var(--border);
}

/* Grammar correction card */
.eval-grammar-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 6px;
  padding: 10px 12px; margin-bottom: 8px;
}
.eval-grammar-card .gc-head { font-size: 13px; margin-bottom: 4px; }
.eval-grammar-card .gc-head .orig { color: #DC2626; text-decoration: line-through; }
.eval-grammar-card .gc-head .corr { color: #16A34A; font-weight: 600; }
.eval-grammar-card .gc-expl { font-size: 12px; color: var(--text-soft); margin-top: 4px; line-height: 1.5; }
.eval-grammar-card .gc-natural {
  font-size: 12px; color: var(--blue-dark); margin-top: 4px; padding: 4px 8px;
  background: var(--blue-light); border-radius: 4px;
}
[data-theme="dark"] .eval-grammar-card .gc-natural { background: rgba(37,99,235,.15); color: #BFDBFE; }

/* Provider badge */
.provider-badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 10px; font-weight: 700; letter-spacing: .5px;
  padding: 3px 8px; border-radius: 10px; text-transform: uppercase;
}
.provider-badge.gemini { background: rgba(217,119,6,.15); color: #D97706; }
.provider-badge.zai    { background: rgba(37,99,235,.15); color: var(--blue); }
.provider-badge::before { content: '●'; font-size: 8px; }

/* Evaluation history page */
.eval-history-list { display: flex; flex-direction: column; gap: 12px; }
.eval-history-item {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 14px 16px; box-shadow: var(--shadow); cursor: pointer; transition: all .15s;
  display: grid; grid-template-columns: auto 1fr auto; gap: 12px; align-items: center;
}
.eval-history-item:hover { box-shadow: var(--shadow-lg); border-color: var(--blue); transform: translateY(-1px); }
.eval-history-item .ehi-band {
  font-size: 20px; font-weight: 800; padding: 6px 12px; border-radius: 8px; color: #fff;
  background: linear-gradient(135deg, #2563EB, #7C3AED); min-width: 56px; text-align: center;
}
.eval-history-item .ehi-band.band-high { background: linear-gradient(135deg, #16A34A, #22C55E); }
.eval-history-item .ehi-band.band-mid  { background: linear-gradient(135deg, #2563EB, #3B82F6); }
.eval-history-item .ehi-band.band-low { background: linear-gradient(135deg, #EA580C, #F97316); }
.eval-history-item .ehi-info { min-width: 0; }
.eval-history-item .ehi-q { font-size: 13px; font-weight: 600; color: var(--text); margin-bottom: 4px; }
.eval-history-item .ehi-meta { font-size: 11px; color: var(--text-soft); display: flex; gap: 10px; flex-wrap: wrap; }
.eval-history-item .ehi-actions { display: flex; gap: 6px; }
.eval-history-item .ehi-actions button {
  padding: 4px 10px; font-size: 11px; border-radius: 4px; background: var(--bg);
  border: 1px solid var(--border); color: var(--text); cursor: pointer; transition: all .15s;
}
.eval-history-item .ehi-actions .ehi-view:hover { background: var(--blue-light); color: var(--blue); border-color: var(--blue); }
.eval-history-item .ehi-actions .ehi-del:hover { background: var(--red-bg); color: var(--red); border-color: var(--red); }
[data-theme="dark"] .eval-history-item .ehi-actions .ehi-view:hover { background: rgba(37,99,235,.2); }

@media (max-width: 560px) {
  .q-eval-criteria-row { grid-template-columns: repeat(2, 1fr); }
  .eval-improvement-plan .ip-grid { grid-template-columns: 1fr; }
  .eval-history-item { grid-template-columns: auto 1fr; }
  .eval-history-item .ehi-actions { grid-column: 1 / -1; }
}

/* ===== Topic sidebar / list ===== */
.layout-2col { display: grid; grid-template-columns: 280px 1fr; gap: 20px; align-items: start; }
.topic-list {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  box-shadow: var(--shadow); max-height: calc(100vh - 130px); overflow-y: auto; position: sticky; top: 20px;
}
.topic-list .topic-item {
  padding: 10px 14px; border-bottom: 1px solid var(--border); cursor: pointer; transition: background .12s;
  display: flex; align-items: center; gap: 8px;
}
.topic-list .topic-item:hover { background: var(--bg); }
.topic-list .topic-item.active { background: var(--blue-light); color: var(--blue-dark); border-left: 3px solid var(--blue); padding-left: 11px; }
[data-theme="dark"] .topic-list .topic-item.active { background: var(--blue-light); color: #BFDBFE; }
.topic-list .topic-item .name { flex: 1; font-size: 13px; }
.topic-list .topic-item .count { font-size: 11px; color: var(--text-soft); }
.topic-list .topic-item .check { font-size: 12px; color: var(--green); }
.topic-list .topic-search { padding: 10px; border-bottom: 1px solid var(--border); position: sticky; top: 0; background: var(--card); z-index: 1; }

/* ===== Cue card ===== */
.cue-card {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 22px; box-shadow: var(--shadow); margin-bottom: 14px; transition: all .15s;
}
.cue-card:hover { box-shadow: var(--shadow-lg); }
.cue-card .cue-head { display: flex; align-items: flex-start; gap: 14px; margin-bottom: 14px; }
.cue-card .cue-num {
  flex-shrink: 0; width: 38px; height: 38px; border-radius: 10px;
  background: linear-gradient(135deg, var(--purple), #A78BFA); color: #fff;
  font-weight: 700; font-size: 14px; display: grid; place-items: center;
}
.cue-card .cue-title { flex: 1; font-size: 17px; font-weight: 700; color: var(--text); line-height: 1.4; }
.cue-card .cue-task {
  background: var(--bg); border-radius: var(--radius-sm); padding: 12px 14px; margin-bottom: 12px;
  font-size: 13px; color: var(--text-soft);
}
.cue-card .cue-bullets { list-style: none; margin-bottom: 14px; }
.cue-card .cue-bullets li {
  padding: 5px 0 5px 22px; position: relative; font-size: 14px; color: var(--text);
}
.cue-card .cue-bullets li::before {
  content: "▸"; position: absolute; left: 4px; color: var(--blue); font-weight: bold;
}
.cue-card .cue-cats { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
.cue-card .cue-cats .cat-pill {
  font-size: 11px; padding: 2px 8px; border-radius: 10px; background: var(--blue-light);
  color: var(--blue-dark); font-weight: 500;
}
[data-theme="dark"] .cue-card .cue-cats .cat-pill { background: var(--blue-light); color: #BFDBFE; }
.cue-card .cue-actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.cue-card .cue-related { margin-top: 14px; padding-top: 12px; border-top: 1px dashed var(--border); }
.cue-card .cue-related h4 { font-size: 13px; color: var(--text-soft); margin-bottom: 6px; font-weight: 600; }
.cue-card .cue-related .q-mini { font-size: 13px; padding: 5px 0; color: var(--text); border-bottom: 1px dotted var(--border); }

/* ===== Practice mode overlay ===== */
.overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,.55); z-index: 200;
  display: none; padding: 20px; overflow-y: auto;
}
.overlay.open { display: block; }
.overlay .modal {
  background: var(--card); border-radius: 12px; max-width: 800px; margin: 20px auto;
  padding: 28px; box-shadow: 0 12px 40px rgba(0,0,0,.25);
}
.overlay .modal h2 { font-size: 20px; margin-bottom: 6px; }
.overlay .modal .sub { color: var(--text-soft); font-size: 13px; margin-bottom: 16px; }

/* ===== Timer ===== */
.timer {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  padding: 20px; background: var(--bg); border-radius: var(--radius); margin: 16px 0;
}
.timer .display { font-size: 56px; font-weight: 800; font-variant-numeric: tabular-nums; color: var(--text); line-height: 1; }
.timer .display.warning { color: var(--orange); }
.timer .display.danger { color: var(--red); }
.timer .phase { font-size: 13px; color: var(--text-soft); text-transform: uppercase; letter-spacing: .5px; }
.timer .controls { display: flex; gap: 8px; margin-top: 8px; }

/* ===== Self-assessment ===== */
.assessment-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin: 14px 0; }
.assessment-item { background: var(--bg); padding: 12px; border-radius: var(--radius-sm); }
.assessment-item label { display: block; font-size: 12px; color: var(--text-soft); margin-bottom: 6px; font-weight: 500; }
.assessment-item select { width: 100%; padding: 4px 8px; }
.rating-display { font-size: 20px; font-weight: 700; color: var(--blue); margin-top: 4px; }

/* ===== Focus mode ===== */
.focus-mode {
  position: fixed; inset: 0; z-index: 250; background: var(--bg);
  display: none; flex-direction: column; padding: 40px;
}
.focus-mode.open { display: flex; }
.focus-mode .focus-content {
  flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center;
  max-width: 800px; margin: 0 auto; width: 100%;
}
.focus-mode .focus-num { font-size: 14px; color: var(--text-soft); margin-bottom: 14px; }
.focus-mode .focus-q { font-size: 30px; font-weight: 600; line-height: 1.4; text-align: center; margin-bottom: 30px; color: var(--text); }
.focus-mode .focus-controls { display: flex; gap: 12px; align-items: center; justify-content: center; flex-wrap: wrap; }
.focus-mode .focus-close { position: absolute; top: 20px; right: 20px; }

/* ===== Filter chips ===== */
.chip-row { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
.chip {
  font-size: 12px; padding: 5px 12px; border-radius: 14px;
  background: var(--card); border: 1px solid var(--border); color: var(--text-soft);
  cursor: pointer; transition: all .12s;
}
.chip:hover { border-color: var(--text-soft); }
.chip.active { background: var(--blue); color: #fff; border-color: var(--blue); }

/* ===== Search results ===== */
.search-result {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 12px 14px; margin-bottom: 8px; cursor: pointer; transition: all .12s;
  display: flex; gap: 12px; align-items: flex-start;
}
.search-result:hover { box-shadow: var(--shadow); border-color: var(--blue); }
.search-result .badge {
  flex-shrink: 0; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; color: #fff;
}
.search-result .badge.p1 { background: var(--blue); }
.search-result .badge.p2 { background: var(--purple); }
.search-result .badge.p3 { background: var(--orange); }
.search-result .info { flex: 1; }
.search-result .info .topic { font-size: 11px; color: var(--text-soft); margin-bottom: 2px; }
.search-result .info .q { font-size: 14px; color: var(--text); }

/* ===== Toast ===== */
.toast {
  position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
  background: var(--text); color: var(--card); padding: 10px 18px; border-radius: var(--radius-sm);
  font-size: 13px; box-shadow: var(--shadow-lg); z-index: 300; opacity: 0;
  transition: opacity .2s, transform .2s; pointer-events: none;
}
.toast.show { opacity: 1; transform: translateX(-50%) translateY(-4px); }

/* ===== Recently practised list ===== */
.recent-list { display: flex; flex-direction: column; gap: 6px; }
.recent-item {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-sm);
  padding: 10px 12px; font-size: 13px; cursor: pointer; transition: all .12s;
  display: flex; gap: 10px; align-items: center;
}
.recent-item:hover { border-color: var(--blue); background: var(--bg); }
.recent-item .badge { padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; color: #fff; }
.recent-item .badge.p1 { background: var(--blue); }
.recent-item .badge.p2 { background: var(--purple); }
.recent-item .badge.p3 { background: var(--orange); }
.recent-item .text { flex: 1; color: var(--text); }
.recent-item .time { font-size: 11px; color: var(--text-soft); }

/* ===== Mobile ===== */
.mobile-header { display: none; }
.menu-toggle { display: none; }
@media (max-width: 900px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .main { margin-left: 0; padding: 70px 16px 60px; }
  .mobile-header {
    display: flex; align-items: center; gap: 12px; padding: 12px 16px;
    background: var(--navy); color: #fff; position: fixed; top: 0; left: 0; right: 0; z-index: 90;
  }
  .mobile-header .menu-toggle {
    display: inline-block; background: rgba(255,255,255,.1); color: #fff; padding: 6px 10px;
    border-radius: var(--radius-sm); font-size: 18px; cursor: pointer;
  }
  .mobile-header .title { font-weight: 700; font-size: 16px; }
  .layout-2col { grid-template-columns: 1fr; }
  .topic-list { position: static; max-height: 300px; }
  .focus-mode .focus-q { font-size: 22px; }
  /* Stack dashboard's 2-column rows on narrow screens to prevent overflow */
  .dashboard-row, .settings-grid { grid-template-columns: 1fr !important; }
  /* Ensure long question text wraps rather than overflowing */
  .card, .q-card { min-width: 0; }
}
@media print {
  .sidebar, .mobile-header, .no-print { display: none !important; }
  .main { margin-left: 0; padding: 0; }
  .page { display: none !important; }
  .page.print-active { display: block !important; }
  .q-card, .cue-card { box-shadow: none; border: 1px solid #ccc; page-break-inside: avoid; }
  body { background: #fff; }
}
</style>
</head>
<body>
<div class="app">
  <!-- ============== SIDEBAR ============== -->
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <div class="logo"><img src="__LOGO_DATA_URI__" alt="TAREQ IELTS logo"></div>
      <div class="brand-text">
        <div class="brand-name">TAREQ IELTS</div>
        <div class="sub">Speaking Practice</div>
      </div>
    </div>
    <nav class="nav" id="nav">
      <button class="nav-item active" data-page="dashboard"><span class="icon">▦</span> Dashboard</button>
      <button class="nav-item" data-page="part1"><span class="icon">1</span> Speaking Part 1 <span class="count" id="nav-p1-count">0</span></button>
      <button class="nav-item" data-page="part2"><span class="icon">2</span> Speaking Part 2 <span class="count" id="nav-p2-count">0</span></button>
      <button class="nav-item" data-page="part3"><span class="icon">3</span> Speaking Part 3 <span class="count" id="nav-p3-count">0</span></button>
      <button class="nav-item" data-page="all"><span class="icon">≡</span> All Questions</button>
      <button class="nav-item" data-page="bookmarks"><span class="icon">★</span> Bookmarks <span class="count" id="nav-bm-count">0</span></button>
      <button class="nav-item" data-page="revision"><span class="icon">!</span> Needs Revision <span class="count" id="nav-rv-count">0</span></button>
      <button class="nav-item" data-page="history"><span class="icon">⏱</span> Practice History</button>
      <button class="nav-item" data-page="ai-eval"><span class="icon">🎙</span> AI Evaluation</button>
      <button class="nav-item" data-page="eval-history"><span class="icon">📈</span> Evaluation History</button>
      <button class="nav-item" data-page="mock-test"><span class="icon">📝</span> Full Mock Test</button>
      <button class="nav-item" data-page="test-history"><span class="icon">📊</span> Test History</button>
      <button class="nav-item" data-page="settings"><span class="icon">⚙</span> Settings</button>
    </nav>
    <div class="sidebar-footer">
      <div>Source: Makkar IELTS</div>
      <div>Sep–Dec 2026 (Final)</div>
      <div style="margin-top:6px;"><button class="btn sm" id="quick-theme-toggle" style="background:rgba(255,255,255,.1);color:#fff;border:none;">🌙 Dark</button></div>
    </div>
  </aside>

  <!-- ============== MAIN ============== -->
  <main class="main">
    <div class="mobile-header">
      <button class="menu-toggle" id="menu-toggle">☰</button>
      <img src="__LOGO_DATA_URI__" alt="TAREQ IELTS" style="height:28px;width:auto;border-radius:6px;object-fit:contain;">
      <div class="title">TAREQ IELTS</div>
    </div>

    <!-- ===== Dashboard ===== -->
    <section class="page active" id="page-dashboard">
      <div class="page-header">
        <h1>Dashboard</h1>
        <div class="sub">Your personal IELTS Speaking practice platform — practise every question from the Sep–Dec 2026 Makkar IELTS book.</div>
      </div>

      <!-- ===== Premium Full Mock Test hero banner ===== -->
      <div class="mock-hero" id="dashboard-mock-hero">
        <div class="mh-inner">
          <div class="mh-text">
            <span class="mh-eyebrow"><span class="dot"></span>Complete Speaking Examination</span>
            <h2 class="mh-title">FULL IELTS MOCK TEST</h2>
            <div class="mh-subtitle">Experience the real IELTS Speaking examination.</div>
            <div class="mh-desc">Practise all three speaking parts with an examiner in a realistic exam environment. Get automatic voice questions, timed answers, and AI-estimated band scores.</div>
            <div class="mh-chips">
              <span class="mh-chip"><span class="mh-chip-num">1</span>Part 1 — Interview</span>
              <span class="mh-chip"><span class="mh-chip-num">2</span>Part 2 — Cue Card</span>
              <span class="mh-chip"><span class="mh-chip-num">3</span>Part 3 — Discussion</span>
            </div>
            <button class="mh-cta" id="dashboard-mock-start" type="button" aria-label="Start Full IELTS Mock Test">
              <span class="mh-cta-icon" aria-hidden="true">🎙</span>
              <span>START FULL MOCK TEST</span>
            </button>
          </div>
          <div class="mh-visual" aria-hidden="true">
            <div class="mh-mic-wrap">
              <div class="mh-mic-ring"></div>
              <div class="mh-mic-ring"></div>
              <div class="mh-mic-ring"></div>
              <div class="mh-mic-core">🎤</div>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== Founder contact card — WhatsApp + Facebook ===== -->
      <div class="founder-card" id="dashboard-founder-card">
        <img class="founder-photo" src="__PHOTO_DATA_URI__" alt="Tareq Al Ma-mun Jr. — founder of TAREQ IELTS">
        <div class="founder-info">
          <div class="fc-label">Need help or feedback?</div>
          <div class="fc-name">
            <a href="https://web.facebook.com/tareq.almamun.77" target="_blank" rel="noopener noreferrer" title="Open Facebook profile">
              <span class="fb-ico" aria-hidden="true">f</span>
              Tareq Al Ma-mun Jr.
            </a>
            <span style="color:var(--text-soft);font-weight:500;font-size:12.5px;">— Founder, TAREQ IELTS</span>
          </div>
          <div class="fc-tagline">Reach out anytime for course help, suggestions, or to share your feedback. I personally read every message.</div>
        </div>
        <div class="founder-actions">
          <a class="fc-btn fc-wa" href="https://wa.me/8801745020285" target="_blank" rel="noopener noreferrer" id="founder-wa-btn">
            <svg class="fc-wa-ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.71.306 1.263.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.549 4.142 1.595 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
            </svg>
            <span id="founder-wa-text">WhatsApp: +880 1745-020285</span>
          </a>
          <a class="fc-btn fc-fb" href="https://web.facebook.com/tareq.almamun.77" target="_blank" rel="noopener noreferrer">
            <span class="fc-fb-ico" aria-hidden="true">f</span>
            <span>Message on Facebook</span>
          </a>
        </div>
      </div>

      <div class="stat-grid" id="dashboard-stats"></div>

      <div class="nav-cards">
        <div class="nav-card p1" data-go="part1">
          <div class="badge">1</div>
          <h3>Speaking Part 1</h3>
          <p>Intro questions — short answers on familiar topics.</p>
          <div class="stats-mini"><span><b id="dc-p1-topics">0</b> topics</span><span><b id="dc-p1-q">0</b> questions</span></div>
        </div>
        <div class="nav-card p2" data-go="part2">
          <div class="badge">2</div>
          <h3>Speaking Part 2</h3>
          <p>Cue cards — speak for 2 minutes with a 1-minute prep.</p>
          <div class="stats-mini"><span><b id="dc-p2-cards">0</b> cue cards</span><span><b id="dc-p2-cats">0</b> categories</span></div>
        </div>
        <div class="nav-card p3" data-go="part3">
          <div class="badge">3</div>
          <h3>Speaking Part 3</h3>
          <p>Follow-up discussion questions — extended answers.</p>
          <div class="stats-mini"><span><b id="dc-p3-q">0</b> questions</span></div>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px;" class="dashboard-row">
        <div class="card">
          <h3 style="margin-bottom:10px;font-size:16px;">Question of the Day</h3>
          <div id="qotd" style="font-size:15px;line-height:1.6;margin-bottom:12px;color:var(--text);word-wrap:break-word;overflow-wrap:break-word;min-width:0;"></div>
          <div class="btn-row">
            <button class="btn primary sm" id="qotd-practice">Practise this</button>
            <button class="btn sm" id="qotd-new">Another question</button>
          </div>
        </div>
        <div class="card">
          <h3 style="margin-bottom:10px;font-size:16px;">Quick Actions</h3>
          <div class="btn-row" style="flex-direction:column;align-items:stretch;">
            <button class="btn primary" id="action-random">🎲 Random Practice</button>
            <button class="btn" id="action-continue">▶ Continue Practising</button>
            <button class="btn" id="action-focus">📝 Strict Practice</button>
          </div>
        </div>
      </div>

      <div class="card">
        <h3 style="margin-bottom:10px;font-size:16px;">Recently Practised</h3>
        <div id="recent-practised" class="recent-list"></div>
      </div>
    </section>

    <!-- ===== Part 1 ===== -->
    <section class="page" id="page-part1">
      <div class="page-header">
        <h1>Speaking Part 1 — Intro Questions</h1>
        <div class="sub">Topic-wise practice. Click a topic to see all its questions.</div>
      </div>
      <div class="layout-2col">
        <div>
          <div class="topic-list">
            <div class="topic-search">
              <input class="input" id="p1-topic-search" placeholder="Filter topics..." style="margin-bottom:8px;">
              <div class="chip-row" style="margin-bottom:0;">
                <button class="chip active" data-p1-filter="all">All</button>
                <button class="chip" data-p1-filter="incomplete">Incomplete</button>
                <button class="chip" data-p1-filter="completed">Completed</button>
              </div>
            </div>
            <div id="p1-topics"></div>
          </div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px;">
            <h2 id="p1-current-topic" style="font-size:18px;">Select a topic</h2>
            <div class="btn-row">
              <button class="btn sm" id="p1-shuffle">🔀 Shuffle</button>
              <button class="btn primary" id="p1-strict" style="font-size:15px;font-weight:700;padding:10px 20px;">🎙 START STRICT PRACTICE</button>
              <button class="btn sm" id="p1-answers">📖 Show All Answers</button>
              <button class="btn sm" id="p1-print">🖨 Print</button>
            </div>
          </div>
          <div id="p1-questions"></div>
        </div>
      </div>
    </section>

    <!-- ===== Part 2 ===== -->
    <section class="page" id="page-part2">
      <div class="page-header">
        <h1>Speaking Part 2 — Cue Cards</h1>
        <div class="sub">Categorised by type. Click any cue card to open the practice screen with timer & self-assessment.</div>
      </div>
      <div class="card" style="margin-bottom:16px;padding:14px 16px;">
        <div class="field" style="margin-bottom:10px;">
          <input class="input" id="p2-search" placeholder="Search cue cards by title or keyword...">
        </div>
        <div class="chip-row" id="p2-categories"></div>
        <div class="chip-row" style="margin-top:6px;">
          <button class="chip active" data-p2-filter="all">All</button>
          <button class="chip" data-p2-filter="incomplete">Incomplete</button>
          <button class="chip" data-p2-filter="completed">Completed</button>
          <button class="chip" data-p2-filter="bookmarked">Bookmarked</button>
        </div>
      </div>
      <div id="p2-cards"></div>
    </section>

    <!-- ===== Part 3 ===== -->
    <section class="page" id="page-part3">
      <div class="page-header">
        <h1>Speaking Part 3 — Discussion Questions</h1>
        <div class="sub">Follow-up questions, organised by their Part 2 cue card topic where possible.</div>
      </div>
      <div class="layout-2col">
        <div>
          <div class="topic-list">
            <div class="topic-search">
              <input class="input" id="p3-topic-search" placeholder="Filter topics..." style="margin-bottom:8px;">
              <div class="chip-row" style="margin-bottom:0;">
                <button class="chip active" data-p3-filter="all">All</button>
                <button class="chip" data-p3-filter="incomplete">Incomplete</button>
                <button class="chip" data-p3-filter="completed">Completed</button>
              </div>
            </div>
            <div id="p3-topics"></div>
          </div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px;">
            <h2 id="p3-current-topic" style="font-size:18px;">Select a topic</h2>
            <div class="btn-row">
              <button class="btn primary" id="p3-strict" style="font-size:15px;font-weight:700;padding:10px 20px;">🎙 START STRICT PRACTICE</button>
              <button class="btn sm" id="p3-shuffle">🔀 Shuffle</button>
              <button class="btn sm" id="p3-answers">📖 Show All Answers</button>
              <button class="btn sm" id="p3-print">🖨 Print</button>
            </div>
          </div>
          <div id="p3-questions"></div>
        </div>
      </div>
    </section>

    <!-- ===== All Questions ===== -->
    <section class="page" id="page-all">
      <div class="page-header">
        <h1>All Questions</h1>
        <div class="sub">Search across all 3 parts of the speaking test.</div>
      </div>
      <div class="card" style="margin-bottom:16px;">
        <div class="field">
          <input class="input" id="global-search" placeholder="Search questions, topics, cue cards, keywords...">
        </div>
        <div class="chip-row">
          <button class="chip active" data-search-part="all">All Parts</button>
          <button class="chip" data-search-part="1">Part 1</button>
          <button class="chip" data-search-part="2">Part 2</button>
          <button class="chip" data-search-part="3">Part 3</button>
        </div>
        <div class="chip-row" style="margin-top:6px;">
          <button class="chip active" data-search-status="all">All Status</button>
          <button class="chip" data-search-status="completed">Completed</button>
          <button class="chip" data-search-status="incomplete">Incomplete</button>
          <button class="chip" data-search-status="bookmarked">Bookmarked</button>
          <button class="chip" data-search-status="revision">Needs Revision</button>
        </div>
      </div>
      <div id="search-results"></div>
    </section>

    <!-- ===== Bookmarks ===== -->
    <section class="page" id="page-bookmarks">
      <div class="page-header">
        <h1>Bookmarks</h1>
        <div class="sub">Questions you've saved for later.</div>
      </div>
      <div id="bookmarks-list"></div>
    </section>

    <!-- ===== Revision ===== -->
    <section class="page" id="page-revision">
      <div class="page-header">
        <h1>Needs Revision</h1>
        <div class="sub">Questions you've marked for revision. Practise them one by one.</div>
      </div>
      <div class="btn-row" style="margin-bottom:16px;">
        <button class="btn primary" id="rev-practice-all">▶ Start Revision Practice</button>
      </div>
      <div id="revision-list"></div>
    </section>

    <!-- ===== History ===== -->
    <section class="page" id="page-history">
      <div class="page-header">
        <h1>Practice History</h1>
        <div class="sub">Last 50 questions practised.</div>
      </div>
      <div class="btn-row" style="margin-bottom:16px;">
        <button class="btn sm" id="clear-history">Clear History</button>
      </div>
      <div id="history-list"></div>
    </section>

    <!-- ===== Settings ===== -->
    <section class="page" id="page-settings">
      <div class="page-header">
        <h1>Settings</h1>
        <div class="sub">Customise your practice experience.</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;" class="settings-grid">
        <div class="card">
          <h3 style="margin-bottom:14px;font-size:16px;">Appearance</h3>
          <div class="field">
            <label>Theme</label>
            <select class="select" id="setting-theme">
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </div>
        </div>
        <div class="card">
          <h3 style="margin-bottom:14px;font-size:16px;">Cue Card Timers</h3>
          <div class="field">
            <label>Preparation time (seconds)</label>
            <input type="number" class="input" id="setting-prep-time" min="30" max="300" step="10">
          </div>
          <div class="field">
            <label>Speaking time (seconds)</label>
            <input type="number" class="input" id="setting-speak-time" min="60" max="600" step="15">
          </div>
        </div>
        <div class="card">
          <h3 style="margin-bottom:14px;font-size:16px;">Mock Test Timer Limits</h3>
          <div class="field">
            <label>Part 1 — per answer (seconds)</label>
            <input type="number" class="input" id="setting-mock-p1" min="15" max="120" step="5" value="30">
          </div>
          <div class="field">
            <label>Part 2 — preparation (seconds)</label>
            <input type="number" class="input" id="setting-mock-p2-prep" min="30" max="180" step="10" value="60">
          </div>
          <div class="field">
            <label>Part 2 — speaking (seconds)</label>
            <input type="number" class="input" id="setting-mock-p2-speak" min="60" max="300" step="15" value="120">
          </div>
          <div class="field">
            <label>Part 3 — per answer (seconds)</label>
            <input type="number" class="input" id="setting-mock-p3" min="20" max="120" step="5" value="45">
          </div>
        </div>
        <div class="card">
          <h3 style="margin-bottom:14px;font-size:16px;">Examiner Voice (TTS)</h3>
          <div class="field">
            <label>Enable examiner voice during mock tests</label>
            <select class="select" id="setting-tts-enabled">
              <option value="true">Yes — read questions aloud</option>
              <option value="false">No — silent mode</option>
            </select>
          </div>
          <div class="field">
            <label>Voice selection</label>
            <select class="select" id="setting-tts-voice"><option value="">Default English voice</option></select>
          </div>
          <div class="field">
            <label>Speech speed</label>
            <select class="select" id="setting-tts-speed">
              <option value="0.8">Slow (0.8x)</option>
              <option value="0.9">Slightly slow (0.9x)</option>
              <option value="1.0" selected>Normal (1.0x)</option>
              <option value="1.1">Slightly fast (1.1x)</option>
              <option value="1.2">Fast (1.2x)</option>
            </select>
          </div>
          <button class="btn sm" id="test-tts">🔊 Test Voice</button>
        </div>
        <div class="card">
          <h3 style="margin-bottom:14px;font-size:16px;">AI Evaluation Server</h3>
          <p style="font-size:12.5px;color:var(--text-soft);margin-bottom:10px;line-height:1.6;">
            The Gemini AI evaluation runs on a separate backend. If you host this website on Netlify / Vercel / GitHub Pages, set the backend URL here so the website knows where to send evaluation requests.
          </p>
          <div class="field">
            <label>Backend API URL</label>
            <input type="text" class="input" id="setting-api-url" placeholder="https://your-backend.up.railway.app">
          </div>
          <div class="btn-row">
            <button class="btn primary" id="save-api-url">💾 Save & Test Connection</button>
            <button class="btn" id="reset-api-url">↺ Reset to Local</button>
          </div>
          <div id="api-url-status" style="margin-top:10px;font-size:12.5px;"></div>
        </div>
        <div class="card">
          <h3 style="margin-bottom:14px;font-size:16px;">Backup & Restore</h3>
          <p style="font-size:13px;color:var(--text-soft);margin-bottom:10px;">Export your progress, notes, bookmarks, and self-assessments as a JSON file.</p>
          <div class="btn-row">
            <button class="btn primary" id="export-data">⬇ Export Progress</button>
            <button class="btn" id="import-data">⬆ Import Progress</button>
            <input type="file" id="import-file" accept=".json" style="display:none;">
          </div>
        </div>
        <div class="card">
          <h3 style="margin-bottom:14px;font-size:16px;">Reset</h3>
          <p style="font-size:13px;color:var(--text-soft);margin-bottom:10px;">Permanently delete all progress, bookmarks, notes and history. This cannot be undone.</p>
          <button class="btn danger" id="reset-progress">🗑 Reset All Progress</button>
        </div>
        <div class="card">
          <h3 style="margin-bottom:14px;font-size:16px;">Keyboard Shortcuts</h3>
          <div style="font-size:13px;line-height:1.9;">
            <div><kbd>←</kbd> / <kbd>→</kbd> — Previous / Next question</div>
            <div><kbd>Space</kbd> — Start / Pause timer</div>
            <div><kbd>B</kbd> — Bookmark current question</div>
            <div><kbd>F</kbd> — Toggle Focus Mode</div>
            <div><kbd>Esc</kbd> — Close overlay / exit focus</div>
          </div>
        </div>
        <div class="card">
          <h3 style="margin-bottom:14px;font-size:16px;">About</h3>
          <p style="font-size:13px;color:var(--text-soft);line-height:1.6;">
            <b>TAREQ IELTS Speaking Practice</b><br>
            Question bank sourced from <i>Makkar IELTS Speaking Guesswork, Sep–Dec 2026 (Final Version)</i> by Dr Kiranpreet Kaur Makkar.<br><br>
            All practice data is stored locally in your browser (localStorage). No account, no internet, no server required.
          </p>
        </div>
      </div>
    </section>

    <!-- ===== AI Evaluation ===== -->
    <section class="page" id="page-ai-eval">
      <div class="page-header">
        <h1>🎙 AI Speaking Evaluation</h1>
        <div class="sub">Record your answers, get AI-powered IELTS band scores and detailed feedback. <span id="ai-server-status" class="server-status offline">● Checking server...</span></div>
      </div>

      <div class="card" style="margin-bottom:16px;">
        <h3 style="margin-bottom:10px;font-size:16px;">How It Works</h3>
        <div style="font-size:13px;color:var(--text-soft);line-height:1.7;">
          <b>1.</b> Go to any Part 1, Part 2, or Part 3 question and click <b>🎙 Record Answer</b>.<br>
          <b>2.</b> Speak your answer — you'll see a live transcript as you talk.<br>
          <b>3.</b> When done, edit any transcription errors in the transcript box.<br>
          <b>4.</b> Come back here and click <b>Submit My Answers for AI Evaluation</b> below.<br>
          <b>5.</b> Get your estimated IELTS band scores, grammar corrections, vocabulary improvements, and pronunciation feedback.
        </div>
        <div class="btn-row" style="margin-top:14px;">
          <button class="btn primary" id="ai-submit-eval">🤖 Submit My Answers for AI Evaluation</button>
          <button class="btn" id="ai-clear-eval">🗑 Clear All Recordings & Evaluations</button>
        </div>
      </div>

      <div id="ai-eval-results"></div>
    </section>

    <!-- ===== Full Mock Test ===== -->
    <section class="page" id="page-mock-test">
      <div class="page-header">
        <h1>📝 Full IELTS Speaking Mock Test</h1>
        <div class="sub">Take a complete simulated IELTS Speaking examination with automatic timers and AI evaluation.</div>
      </div>

      <div class="card" style="margin-bottom:16px;">
        <h3 style="margin-bottom:10px;font-size:16px;">How the Full Mock Test Works</h3>
        <div style="font-size:13px;color:var(--text-soft);line-height:1.8;">
          <b>Part 1 — Introduction & Interview</b> (4–5 questions, 30s each)<br>
          <b>Part 2 — Individual Long Turn</b> (1 cue card, 1 min prep + 2 min speaking)<br>
          <b>Part 3 — Two-way Discussion</b> (3–5 follow-up questions, 45s each)<br><br>
          The system automatically selects questions from your existing database, randomizes them, and organizes them into a complete test. After finishing, get your AI-estimated IELTS band scores.
        </div>
        <div class="btn-row" style="margin-top:14px;">
          <button class="btn primary" id="mock-start">📝 Start Full Mock Test</button>
          <button class="btn" id="mock-generate-new">🎲 Generate New Test Set</button>
        </div>
      </div>

      <div id="mock-test-content"></div>
    </section>

    <!-- ===== Test History ===== -->
    <section class="page" id="page-test-history">
      <div class="page-header">
        <h1>📊 Test History</h1>
        <div class="sub">View your completed mock tests, compare scores, and review past performance.</div>
      </div>
      <div class="btn-row" style="margin-bottom:16px;">
        <button class="btn sm" id="clear-test-history">🗑 Clear All Test History</button>
      </div>
      <div id="test-history-list"></div>
    </section>

    <!-- ===== Evaluation History (per-question Gemini evaluations) ===== -->
    <section class="page" id="page-eval-history">
      <div class="page-header">
        <h1>📈 Evaluation History</h1>
        <div class="sub">All your AI-evaluated speaking answers. Compare your progress, review feedback, and re-listen to recordings.</div>
      </div>
      <div class="card" style="margin-bottom:16px;background:var(--blue-light);border:none;">
        <div style="font-size:13px;line-height:1.7;color:var(--blue-dark);">
          <b>🔒 Where your data is stored:</b> All evaluations, transcripts, and audio recordings are saved locally in your browser (localStorage + IndexedDB). Nothing is uploaded to any external server except for the brief moment when the transcript is sent to Google Gemini for evaluation. Clearing your browser data, or clicking the button below, will permanently delete everything.
        </div>
      </div>
      <div class="btn-row" style="margin-bottom:16px;">
        <button class="btn sm" id="clear-eval-history">🗑 Clear All Evaluation History</button>
        <button class="btn sm" id="refresh-eval-history">🔄 Refresh</button>
      </div>
      <div id="eval-history-list" class="eval-history-list"></div>
    </section>
  </main>
</div>

<!-- ============== Mock Test Overlay ============== -->
<div class="overlay" id="mock-overlay" style="z-index:250;">
  <div class="modal" id="mock-modal" style="max-width:700px;"></div>
</div>

<!-- ============== Cue card practice overlay ============== -->
<div class="overlay" id="cue-overlay">
  <div class="modal" id="cue-modal"></div>
</div>

<!-- ============== Part 3 practice overlay ============== -->
<div class="overlay" id="p3-overlay">
  <div class="modal" id="p3-modal"></div>
</div>

<!-- ============== Random practice overlay ============== -->
<div class="overlay" id="random-overlay">
  <div class="modal" id="random-modal" style="max-width:600px;"></div>
</div>

<!-- ============== Strict Examiner Mode ============== -->
<div class="overlay" id="strict-overlay" style="z-index:260;">
  <div class="modal" id="strict-modal" style="max-width:700px;"></div>
</div>

<!-- ============== Toast ============== -->
<div class="toast" id="toast"></div>

<script>
/* ============================================================
   TAREQ IELTS — App Logic
   ============================================================ */

// ===== Embedded question data =====
const DATA = __DATA_JSON__;

const ALL_CATEGORIES = __CATS_JSON__;

// ===== State management =====
const STORE_KEY = 'tareq_ielts_v1';
const DEFAULT_STATE = {
  progress: {},      // { 'p1-3-2': { status:'practised', bookmarked:false, notes:'', lastPractised:0, assessment:{} } }
  history: [],       // [{id, text, part, topic, ts}]
  lastVisited: { part:null, topic:null, cueNum:null },
  settings: { theme:'light', prepTime:60, speakTime:120 },
  qotdDate: '',
  qotdId: '',
};
let state = loadState();

function loadState() {
  try {
    const s = JSON.parse(localStorage.getItem(STORE_KEY));
    if (!s) return JSON.parse(JSON.stringify(DEFAULT_STATE));
    return Object.assign(JSON.parse(JSON.stringify(DEFAULT_STATE)), s);
  } catch (e) {
    return JSON.parse(JSON.stringify(DEFAULT_STATE));
  }
}
function saveState() {
  localStorage.setItem(STORE_KEY, JSON.stringify(state));
}
function getQ(id) { return state.progress[id] || { status:'not-practised', bookmarked:false, notes:'', lastPractised:0, assessment:{} }; }
function setQ(id, q) { state.progress[id] = q; saveState(); }

// ===== Helpers =====
function $(sel) { return document.querySelector(sel); }
function $$(sel) { return Array.from(document.querySelectorAll(sel)); }
function esc(s) { return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function toast(msg) {
  const t = $('#toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toast._t);
  toast._t = setTimeout(() => t.classList.remove('show'), 2200);
}

// Build flat question ID -> question map for fast lookups
const Q_INDEX = (function() {
  const idx = { byId:{}, p1:[], p2:[], p3:[], all:[] };
  DATA.part1.forEach(t => {
    t.questions.forEach((item, qi) => {
      const id = `p1-${t.num}-${qi}`;
      const qItem = { id, part:1, topicNum:t.num, topic:t.name, q:item.q||'', a:item.a||'', qi };
      idx.byId[id] = qItem; idx.p1.push(qItem); idx.all.push(qItem);
    });
  });
  DATA.part2.forEach(c => {
    const id = `p2-${c.num}`;
    const item = { id, part:2, cueNum:c.num, title:c.title, bullets:c.bullets, categories:c.categories, part3:c.part3, sampleAnswers:c.sampleAnswers||[] };
    idx.byId[id] = item; idx.p2.push(item); idx.all.push(item);
  });
  // Part 3 questions: each cue card's follow-ups are tagged with that cue card's number
  DATA.part2.forEach(c => {
    c.part3.forEach((item, qi) => {
      const id = `p3-${c.num}-${qi}`;
      const qItem = { id, part:3, cueNum:c.num, topic:`Follow-ups: ${c.title}`, q:item.q||'', a:item.a||'', qi };
      idx.byId[id] = qItem; idx.p3.push(qItem); idx.all.push(qItem);
    });
  });
  return idx;
})();

const STATS = (function() {
  const p1q = Q_INDEX.p1.length;
  const p2q = Q_INDEX.p2.length;
  const p3q = Q_INDEX.p3.length;
  return {
    p1Topics: DATA.part1.length,
    p1Questions: p1q,
    p2Cards: DATA.part2.length,
    p3Questions: p3q,
    total: p1q + p2q + p3q,
  };
})();

// ===== Navigation =====
function showPage(name) {
  $$('.page').forEach(p => p.classList.remove('active'));
  const page = $('#page-' + name);
  if (page) page.classList.add('active');
  $$('.nav-item').forEach(n => n.classList.toggle('active', n.dataset.page === name));
  if (name === 'dashboard') renderDashboard();
  if (name === 'part1') renderPart1();
  if (name === 'part2') renderPart2();
  if (name === 'part3') renderPart3();
  if (name === 'all') renderAllQuestions();
  if (name === 'bookmarks') renderBookmarks();
  if (name === 'revision') renderRevision();
  if (name === 'history') renderHistory();
  if (name === 'settings') renderSettings();
  state.lastVisited = state.lastVisited || {};
  state.lastVisited.page = name;
  saveState();
  // close mobile sidebar
  $('#sidebar').classList.remove('open');
  window.scrollTo(0, 0);
}

document.addEventListener('click', e => {
  const navItem = e.target.closest('.nav-item');
  if (navItem) { showPage(navItem.dataset.page); return; }
  const navCard = e.target.closest('.nav-card');
  if (navCard) { showPage(navCard.dataset.go); return; }
});

// Mobile menu toggle
$('#menu-toggle').addEventListener('click', () => $('#sidebar').classList.toggle('open'));

// ===== Theme =====
function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  $('#quick-theme-toggle').textContent = theme === 'dark' ? '☀ Light' : '🌙 Dark';
  state.settings.theme = theme;
  saveState();
}
$('#quick-theme-toggle').addEventListener('click', () => {
  applyTheme(state.settings.theme === 'dark' ? 'light' : 'dark');
});

// ===== Dashboard =====
function renderDashboard() {
  const totalQ = STATS.total;
  let completed = 0, bookmarked = 0, revision = 0;
  Q_INDEX.all.forEach(item => {
    const q = getQ(item.id);
    if (q.status === 'practised' || q.status === 'mastered') completed++;
    if (q.bookmarked) bookmarked++;
    if (q.status === 'needs-revision') revision++;
  });
  const pct = totalQ ? Math.round(completed / totalQ * 100) : 0;

  $('#dashboard-stats').innerHTML = `
    <div class="stat">
      <div class="label">Total Questions</div>
      <div class="value">${totalQ}</div>
    </div>
    <div class="stat">
      <div class="label">Topics / Cue Cards</div>
      <div class="value">${STATS.p1Topics + STATS.p2Cards}</div>
    </div>
    <div class="stat green">
      <div class="label">Completed</div>
      <div class="value">${completed} <span style="font-size:14px;color:var(--text-soft);">/ ${totalQ}</span></div>
      <div class="progress-bar"><div class="fill" style="width:${pct}%"></div></div>
    </div>
    <div class="stat">
      <div class="label">Overall Progress</div>
      <div class="value">${pct}%</div>
      <div class="progress-bar"><div class="fill" style="width:${pct}%"></div></div>
    </div>
    <div class="stat" style="background:var(--yellow-bg);border-color:transparent;">
      <div class="label">Bookmarked</div>
      <div class="value">${bookmarked}</div>
    </div>
    <div class="stat" style="background:var(--orange-bg);border-color:transparent;">
      <div class="label">Needs Revision</div>
      <div class="value">${revision}</div>
    </div>
  `;

  $('#dc-p1-topics').textContent = STATS.p1Topics;
  $('#dc-p1-q').textContent = STATS.p1Questions;
  $('#dc-p2-cards').textContent = STATS.p2Cards;
  $('#dc-p2-cats').textContent = ALL_CATEGORIES.length;
  $('#dc-p3-q').textContent = STATS.p3Questions;

  $('#nav-p1-count').textContent = STATS.p1Questions;
  $('#nav-p2-count').textContent = STATS.p2Cards;
  $('#nav-p3-count').textContent = STATS.p3Questions;
  $('#nav-bm-count').textContent = bookmarked;
  $('#nav-rv-count').textContent = revision;

  // Question of the day
  renderQOTD();

  // Recently practised
  const recent = (state.history || []).slice(-10).reverse();
  $('#recent-practised').innerHTML = recent.length === 0
    ? '<div style="color:var(--text-soft);font-size:13px;">No questions practised yet. Start with the dashboard cards above.</div>'
    : recent.map(h => `
      <div class="recent-item" onclick="openQuestionById('${h.id}')">
        <span class="badge p${h.part}">P${h.part}</span>
        <span class="text">${esc(h.text.length > 90 ? h.text.slice(0,90)+'…' : h.text)}</span>
        <span class="time">${new Date(h.ts).toLocaleDateString()} ${new Date(h.ts).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</span>
      </div>`).join('');
}

function renderQOTD() {
  const today = new Date().toDateString();
  if (state.qotdDate !== today || !state.qotdId || !Q_INDEX.byId[state.qotdId]) {
    const pool = Q_INDEX.all.filter(it => it.part !== 2 || true);
    const pick = pool[Math.floor(Math.random() * pool.length)];
    state.qotdDate = today;
    state.qotdId = pick.id;
    saveState();
  }
  const item = Q_INDEX.byId[state.qotdId];
  const text = item.part === 2 ? item.title : item.q;
  $('#qotd').innerHTML = `<div style="font-size:11px;color:var(--text-soft);margin-bottom:4px;">Part ${item.part} • ${esc(item.topic || item.title || '')}</div>${esc(text)}`;
}
$('#qotd-new').addEventListener('click', () => {
  const pool = Q_INDEX.all;
  let pick;
  do { pick = pool[Math.floor(Math.random() * pool.length)]; } while (pick.id === state.qotdId);
  state.qotdId = pick.id; saveState(); renderQOTD();
});
$('#qotd-practice').addEventListener('click', () => openQuestionById(state.qotdId));

$('#action-random').addEventListener('click', () => openRandomPicker());
$('#action-continue').addEventListener('click', () => {
  // jump to last visited topic / cue card
  const lv = state.lastVisited || {};
  if (lv.cueNum) { showPage('part2'); setTimeout(() => openCueCard(lv.cueNum), 200); }
  else if (lv.part === 1 && lv.topic != null) { showPage('part1'); setTimeout(() => selectPart1Topic(lv.topic), 100); }
  else if (lv.part === 3 && lv.topic != null) { showPage('part3'); setTimeout(() => selectPart3TopicByCue(lv.topic), 100); }
  else { showPage('part1'); }
});
$('#action-focus').addEventListener('click', () => { showPage('part1'); toast('Select a topic and click "🎙 START STRICT PRACTICE"'); });

// ===== Part 1 =====
let p1CurrentTopic = null;
let p1Shuffled = false;
let p1Filter = 'all';
let p1TopicFilterText = '';

function renderPart1() {
  if (p1CurrentTopic == null) {
    // pick first topic
    p1CurrentTopic = DATA.part1[0] ? DATA.part1[0].num : null;
  }
  renderPart1Topics();
  renderPart1Questions();
}

function renderPart1Topics() {
  const container = $('#p1-topics');
  let topics = DATA.part1;
  if (p1TopicFilterText) {
    const t = p1TopicFilterText.toLowerCase();
    topics = topics.filter(tp => tp.name.toLowerCase().includes(t));
  }
  if (p1Filter === 'completed' || p1Filter === 'incomplete') {
    topics = topics.filter(tp => {
      const total = tp.questions.length;
      const done = tp.questions.filter((_, qi) => {
        const q = getQ(`p1-${tp.num}-${qi}`);
        return q.status === 'practised' || q.status === 'mastered';
      }).length;
      return p1Filter === 'completed' ? done === total && total > 0 : done < total;
    });
  }
  if (topics.length === 0) {
    container.innerHTML = '<div style="padding:14px;color:var(--text-soft);font-size:13px;">No topics match.</div>';
    return;
  }
  container.innerHTML = topics.map(tp => {
    const done = tp.questions.filter((_, qi) => {
      const q = getQ(`p1-${tp.num}-${qi}`);
      return q.status === 'practised' || q.status === 'mastered';
    }).length;
    const total = tp.questions.length;
    const isActive = tp.num === p1CurrentTopic;
    return `<div class="topic-item ${isActive?'active':''}" onclick="selectPart1Topic(${tp.num})">
      <span class="name">${esc(tp.name)}</span>
      <span class="count">${done}/${total}</span>
      ${done === total && total > 0 ? '<span class="check">✓</span>' : ''}
    </div>`;
  }).join('');
}

function selectPart1Topic(num) {
  p1CurrentTopic = num;
  p1Shuffled = false;
  state.lastVisited = state.lastVisited || {};
  state.lastVisited.part = 1;
  state.lastVisited.topic = num;
  saveState();
  renderPart1Topics();
  renderPart1Questions();
}
window.selectPart1Topic = selectPart1Topic;

function renderPart1Questions() {
  const tp = DATA.part1.find(t => t.num === p1CurrentTopic);
  if (!tp) {
    $('#p1-current-topic').textContent = 'No topic selected';
    $('#p1-questions').innerHTML = '';
    return;
  }
  $('#p1-current-topic').textContent = `${tp.name}`;
  let questions = tp.questions.map((q, qi) => ({ q, qi }));
  if (p1Shuffled) {
    questions = questions.slice().sort(() => Math.random() - 0.5);
  }
  const done = tp.questions.filter((_, qi) => {
    const q = getQ(`p1-${tp.num}-${qi}`);
    return q.status === 'practised' || q.status === 'mastered';
  }).length;
  const total = tp.questions.length;
  const pct = total ? Math.round(done/total*100) : 0;

  $('#p1-questions').innerHTML = `
    <div class="card" style="margin-bottom:14px;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
      <div style="font-size:13px;color:var(--text-soft);">
        ${done} of ${total} completed • <b>${pct}%</b>
      </div>
      <div style="height:8px;flex:1;max-width:200px;background:var(--border);border-radius:4px;overflow:hidden;">
        <div style="height:100%;width:${pct}%;background:var(--green);"></div>
      </div>
    </div>
    ${questions.map(({q, qi}) => renderPart1Question(tp, q.q, q.a, qi)).join('')}
  `;
  bindPart1Events();
}

// === Reusable recorder block — used by Part 1, Part 2, and Part 3 ===
function recorderHTML(id, questionText, part, existingTranscript) {
  return `<div class="recorder-block">
      <div class="recorder-controls" data-rec-controls="${id}">
        <button class="rec-btn rec-start" data-rec-act="start" data-rec-id="${id}" data-rec-q="${esc(questionText)}" data-rec-part="${part}">🎙 Record Answer</button>
        <button class="rec-btn" data-rec-act="stop" data-rec-id="${id}" disabled>⏹ Stop</button>
        <button class="rec-btn" data-rec-act="retake" data-rec-id="${id}" disabled>🔄 Retake</button>
        <span class="rec-indicator" data-rec-indicator="${id}" style="display:none;"><span class="rec-dot"></span> REC</span>
        <span class="rec-duration" data-rec-duration="${id}">00:00</span>
      </div>
      <div class="waveform-container" data-rec-waveform="${id}" style="display:none;">
        <canvas class="waveform-canvas" data-rec-canvas="${id}"></canvas>
      </div>
      <div class="transcript-area" data-rec-transcript-area="${id}" style="${existingTranscript ? '' : 'display:none;'}">
        <div class="answer-label" style="color:var(--blue);margin-bottom:4px;">📝 Your Transcript (edit if needed):</div>
        <div class="transcript-text" contenteditable="true" data-rec-transcript="${id}">${esc(existingTranscript || '')}</div>
        <div class="rec-audio-player" data-rec-player="${id}"></div>
        <div class="rec-status" data-rec-status="${id}"></div>
      </div>
    </div>`;
}

function renderPart1Question(tp, q, ans, qi) {
  const id = `p1-${tp.num}-${qi}`;
  const st = getQ(id);
  const hasAnswer = ans && ans.trim().length > 10;
  return `<div class="q-card ${st.status==='practised'?'completed':''} ${st.bookmarked?'bookmarked':''} ${st.status==='needs-revision'?'revision':''} ${st.status==='mastered'?'mastered':''}" data-qid="${id}">
    <div class="q-head">
      <div class="q-num">${qi+1}</div>
      <div class="q-text">${esc(q)}</div>
    </div>
    <div class="q-meta">
      <span class="status-pill ${st.status==='practised'?'practised':st.status==='needs-revision'?'needs-revision':st.status==='mastered'?'mastered':'not-practised'}">${st.status.replace('-',' ')}</span>
      <button class="btn sm" data-act="toggle-complete" data-id="${id}">${st.status==='practised'||st.status==='mastered'?'✓ Completed':'○ Mark Complete'}</button>
      <button class="btn sm ${st.bookmarked?'success':''}" data-act="toggle-bookmark" data-id="${id}">${st.bookmarked?'★ Saved':'☆ Bookmark'}</button>
      ${hasAnswer ? `<button class="btn sm" data-act="toggle-answer" data-id="${id}">📖 Show Answer</button>` : ''}
      <button class="btn sm" data-act="toggle-notes" data-id="${id}">📝 Notes</button>
      <select class="btn sm" data-act="set-status" data-id="${id}" style="padding:5px 8px;">
        <option value="not-practised" ${st.status==='not-practised'?'selected':''}>Not Practised</option>
        <option value="practised" ${st.status==='practised'?'selected':''}>Practised</option>
        <option value="needs-revision" ${st.status==='needs-revision'?'selected':''}>Needs Revision</option>
        <option value="mastered" ${st.status==='mastered'?'selected':''}>Mastered</option>
      </select>
    </div>
    ${hasAnswer ? `<div class="answer-area" data-answer-for="${id}">
      <div class="answer-label">📖 Sample Answer (from Makkar IELTS book):</div>
      <div class="answer-text">${esc(ans)}</div>
    </div>` : ''}
    ${recorderHTML(id, q, '1', st.transcript)}
    <div class="notes-area" data-notes-for="${id}">
      <textarea class="textarea" placeholder="Your personal notes for this question..." data-notes-input="${id}">${esc(st.notes || '')}</textarea>
    </div>
  </div>`;
}

function bindPart1Events() {
  $$('[data-act]').forEach(el => {
    if (el._bound) return;
    el._bound = true;
    el.addEventListener('click', e => {
      const act = el.dataset.act;
      const id = el.dataset.id;
      if (act === 'toggle-complete') toggleComplete(id);
      else if (act === 'toggle-bookmark') toggleBookmark(id);
      else if (act === 'toggle-notes') {
        const area = document.querySelector(`[data-notes-for="${id}"]`);
        if (area) area.classList.toggle('open');
      }
      else if (act === 'toggle-answer') {
        const area = document.querySelector(`[data-answer-for="${id}"]`);
        if (area) {
          area.classList.toggle('open');
          el.textContent = area.classList.contains('open') ? '📖 Hide Answer' : '📖 Show Answer';
        }
      }
    });
  });
  $$('[data-act="set-status"]').forEach(el => {
    if (el._bound) return;
    el._bound = true;
    el.addEventListener('change', e => {
      const id = el.dataset.id;
      const q = getQ(id);
      q.status = el.value;
      if (el.value === 'practised' || el.value === 'mastered') {
        q.lastPractised = Date.now();
        addHistory(id);
      }
      setQ(id, q);
      renderPart1Questions();
      renderPart1Topics();
    });
  });
  $$('[data-notes-input]').forEach(el => {
    if (el._bound) return;
    el._bound = true;
    el.addEventListener('input', () => {
      const id = el.dataset.notesInput;
      const q = getQ(id);
      q.notes = el.value;
      setQ(id, q);
    });
  });
}

function toggleComplete(id) {
  const q = getQ(id);
  if (q.status === 'practised' || q.status === 'mastered') {
    q.status = 'not-practised';
    q.lastPractised = 0;
  } else {
    q.status = 'practised';
    q.lastPractised = Date.now();
    addHistory(id);
  }
  setQ(id, q);
  renderPart1Questions();
  renderPart1Topics();
  refreshNavCounts();
}

function toggleBookmark(id) {
  const q = getQ(id);
  q.bookmarked = !q.bookmarked;
  setQ(id, q);
  renderPart1Questions();
  refreshNavCounts();
}

function refreshNavCounts() {
  let bookmarked = 0, revision = 0;
  Q_INDEX.all.forEach(item => {
    const q = getQ(item.id);
    if (q.bookmarked) bookmarked++;
    if (q.status === 'needs-revision') revision++;
  });
  $('#nav-bm-count').textContent = bookmarked;
  $('#nav-rv-count').textContent = revision;
}

function addHistory(id) {
  const item = Q_INDEX.byId[id];
  if (!item) return;
  state.history = state.history || [];
  state.history.push({
    id, part: item.part, ts: Date.now(),
    text: item.part === 2 ? item.title : item.q,
    topic: item.topic || item.title || '',
  });
  if (state.history.length > 50) state.history = state.history.slice(-50);
  saveState();
}

$('#p1-topic-search').addEventListener('input', e => { p1TopicFilterText = e.target.value; renderPart1Topics(); });
$$('[data-p1-filter]').forEach(el => el.addEventListener('click', () => {
  $$('[data-p1-filter]').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  p1Filter = el.dataset.p1Filter;
  renderPart1Topics();
}));
$('#p1-shuffle').addEventListener('click', () => { p1Shuffled = !p1Shuffled; renderPart1Questions(); toast(p1Shuffled ? 'Questions shuffled' : 'Original order'); });
$('#p1-answers').addEventListener('click', () => {
  const areas = $$('#p1-questions .answer-area');
  const btn = $('#p1-answers');
  const anyOpen = areas.length > 0 && Array.from(areas).some(a => a.classList.contains('open'));
  areas.forEach(a => {
    if (anyOpen) a.classList.remove('open');
    else a.classList.add('open');
  });
  $$('[data-act="toggle-answer"]').forEach(b => {
    const id = b.dataset.id;
    const area = document.querySelector(`[data-answer-for="${id}"]`);
    if (area) b.textContent = area.classList.contains('open') ? '📖 Hide Answer' : '📖 Show Answer';
  });
  btn.textContent = anyOpen ? '📖 Show All Answers' : '📖 Hide All Answers';
});
$('#p1-print').addEventListener('click', () => printTopic('p1', p1CurrentTopic));

// ===== Part 2 =====
let p2Category = 'all';
let p2Filter = 'all';
let p2Search = '';

function renderPart2() {
  // categories chips
  const catRow = $('#p2-categories');
  catRow.innerHTML = `<button class="chip ${p2Category==='all'?'active':''}" data-cat="all">All Categories</button>` +
    ALL_CATEGORIES.map(c => `<button class="chip ${p2Category===c?'active':''}" data-cat="${esc(c)}">${esc(c)}</button>`).join('');
  $$('[data-cat]').forEach(el => {
    if (el._bound) return;
    el._bound = true;
    el.addEventListener('click', () => { p2Category = el.dataset.cat; renderPart2(); });
  });
  renderPart2Cards();
}

function renderPart2Cards() {
  let cards = DATA.part2.slice();
  if (p2Category !== 'all') {
    cards = cards.filter(c => (c.categories || []).includes(p2Category));
  }
  if (p2Search) {
    const s = p2Search.toLowerCase();
    cards = cards.filter(c => c.title.toLowerCase().includes(s) || (c.bullets || []).some(b => b.toLowerCase().includes(s)));
  }
  if (p2Filter !== 'all') {
    cards = cards.filter(c => {
      const q = getQ(`p2-${c.num}`);
      if (p2Filter === 'completed') return q.status === 'practised' || q.status === 'mastered';
      if (p2Filter === 'incomplete') return q.status !== 'practised' && q.status !== 'mastered';
      if (p2Filter === 'bookmarked') return q.bookmarked;
      return true;
    });
  }
  const container = $('#p2-cards');
  if (cards.length === 0) {
    container.innerHTML = '<div class="card" style="text-align:center;padding:30px;color:var(--text-soft);">No cue cards match the filters.</div>';
    return;
  }
  container.innerHTML = cards.map(c => {
    const id = `p2-${c.num}`;
    const st = getQ(id);
    return `<div class="cue-card ${st.status==='practised'||st.status==='mastered'?'completed':''} ${st.bookmarked?'bookmarked':''} ${st.status==='needs-revision'?'revision':''} ${st.status==='mastered'?'mastered':''}">
      <div class="cue-head">
        <div class="cue-num">${c.num}</div>
        <div class="cue-title">${esc(c.title)}</div>
      </div>
      <div class="cue-cats">${(c.categories||[]).map(cat => `<span class="cat-pill">${esc(cat)}</span>`).join('')}</div>
      <div class="cue-task"><b>You should say:</b></div>
      <ul class="cue-bullets">${(c.bullets||[]).map(b => `<li>${esc(b)}</li>`).join('')}</ul>
      <div class="cue-actions">
        <button class="btn primary" style="font-size:14px;font-weight:700;padding:8px 16px;" onclick="startStrictPractice(2,${c.num})">🎙 STRICT PRACTICE</button>
        <button class="btn sm" onclick="openCueCard(${c.num})">▶ Practise Cue Card</button>
        <button class="btn sm" onclick="toggleComplete('${id}');renderPart2Cards();">${st.status==='practised'||st.status==='mastered'?'✓ Completed':'○ Mark Complete'}</button>
        <button class="btn sm ${st.bookmarked?'success':''}" onclick="toggleBookmark('${id}');renderPart2Cards();">${st.bookmarked?'★ Saved':'☆ Bookmark'}</button>
        ${(c.sampleAnswers && c.sampleAnswers.length) ? `<button class="btn sm" onclick="toggleAnswer('${id}',this)">📖 Show Sample Answer</button>` : ''}
        <button class="btn sm" onclick="document.querySelector('[data-notes-for=&quot;${id}&quot;]').classList.toggle('open')">📝 Notes</button>
        <span class="status-pill ${st.status==='practised'?'practised':st.status==='needs-revision'?'needs-revision':st.status==='mastered'?'mastered':'not-practised'}" style="margin-left:auto;">${st.status.replace('-',' ')}</span>
      </div>
      ${(c.sampleAnswers && c.sampleAnswers.length) ? `<div class="answer-area" data-answer-for="${id}">
        <div class="answer-label">📖 Sample Answer${c.sampleAnswers.length > 1 ? `s (${c.sampleAnswers.length})` : ''} (from Makkar IELTS book):</div>
        ${c.sampleAnswers.map((ans, ai) => `<div class="answer-text" style="margin-bottom:${c.sampleAnswers.length > 1 ? '12px' : '0'};${c.sampleAnswers.length > 1 ? 'padding-bottom:10px;border-bottom:1px dashed var(--border);' : ''}">${c.sampleAnswers.length > 1 ? `<b style="color:var(--text-soft);font-size:12px;">Answer ${ai+1}:</b><br>` : ''}${esc(ans)}</div>`).join('')}
      </div>` : ''}
      ${recorderHTML(id, c.title, '2', st.transcript)}
      <div class="notes-area" data-notes-for="${id}">
        <textarea class="textarea" placeholder="Your personal notes for this cue card..." oninput="updateNotes('${id}',this.value)">${esc(st.notes||'')}</textarea>
      </div>
      ${c.part3 && c.part3.length ? `<div class="cue-related">
        <h4>Related Part 3 Follow-ups (${c.part3.length})</h4>
        ${c.part3.slice(0,3).map((q,i) => `<div class="q-mini">${i+1}. ${esc(q.q)}</div>`).join('')}
        ${c.part3.length > 3 ? `<div style="font-size:12px;color:var(--text-soft);margin-top:4px;">+ ${c.part3.length - 3} more — open the cue card to see all.</div>` : ''}
      </div>` : ''}
    </div>`;
  }).join('');
}

window.updateNotes = function(id, val) {
  const q = getQ(id);
  q.notes = val;
  setQ(id, q);
};

$('#p2-search').addEventListener('input', e => { p2Search = e.target.value; renderPart2Cards(); });
$$('[data-p2-filter]').forEach(el => el.addEventListener('click', () => {
  $$('[data-p2-filter]').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  p2Filter = el.dataset.p2Filter;
  renderPart2Cards();
}));

// ===== Cue Card Practice Overlay =====
let cueTimer = null;
function openCueCard(num) {
  const c = DATA.part2.find(x => x.num === num);
  if (!c) return;
  state.lastVisited = state.lastVisited || {};
  state.lastVisited.cueNum = num;
  saveState();

  const id = `p2-${num}`;
  const st = getQ(id);

  $('#cue-modal').innerHTML = `
    <h2>Cue Card #${c.num}</h2>
    <div class="sub">Part 2 — Cue Card Practice</div>
    <div style="background:var(--bg);padding:18px;border-radius:var(--radius);margin-bottom:14px;">
      <div style="font-size:11px;color:var(--text-soft);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;">Cue Card</div>
      <div style="font-size:18px;font-weight:700;line-height:1.4;margin-bottom:14px;">${esc(c.title)}</div>
      <div style="font-size:13px;color:var(--text-soft);margin-bottom:6px;"><b>You should say:</b></div>
      <ul class="cue-bullets">${(c.bullets||[]).map(b => `<li>${esc(b)}</li>`).join('')}</ul>
    </div>
    <div class="timer" id="cue-timer">
      <div class="phase" id="cue-phase">Preparation</div>
      <div class="display" id="cue-display">${formatTime(state.settings.prepTime)}</div>
      <div class="controls">
        <button class="btn primary" id="cue-start">▶ Start</button>
        <button class="btn" id="cue-pause" disabled>⏸ Pause</button>
        <button class="btn" id="cue-reset">↻ Reset</button>
        <button class="btn" id="cue-skip-prep">⏭ Skip to Speaking</button>
      </div>
      <div style="margin-top:10px;display:flex;gap:12px;align-items:center;justify-content:center;font-size:12px;color:var(--text-soft);">
        <label>Prep: <input type="number" id="cue-prep-input" value="${state.settings.prepTime}" min="30" max="300" step="10" style="width:60px;padding:2px 4px;">s</label>
        <label>Speak: <input type="number" id="cue-speak-input" value="${state.settings.speakTime}" min="60" max="600" step="15" style="width:60px;padding:2px 4px;">s</label>
      </div>
    </div>
    <div class="field">
      <label>Preparation Notes (jot down key points)</label>
      <textarea class="textarea" id="cue-prep-notes" placeholder="e.g. who, when, where, why, key vocabulary...">${esc(st.prepNotes || '')}</textarea>
    </div>
    <h3 style="font-size:15px;margin:18px 0 10px;">🎙 Record Your Answer</h3>
    ${recorderHTML(id, c.title, '2', st.transcript)}
    <h3 style="font-size:15px;margin:18px 0 10px;">Self-Assessment</h3>
    <p style="font-size:12px;color:var(--text-soft);margin-bottom:8px;">Rate yourself 1–9 on each IELTS criterion (this is a self-evaluation only — not an official band score).</p>
    <div class="assessment-grid">
      <div class="assessment-item"><label>Fluency & Coherence</label><select id="self-fc">${[1,2,3,4,5,6,7,8,9].map(n=>`<option value="${n}" ${((st.assessment||{}).fc===n)?'selected':''}>${n}</option>`).join('')}</select></div>
      <div class="assessment-item"><label>Lexical Resource</label><select id="self-lr">${[1,2,3,4,5,6,7,8,9].map(n=>`<option value="${n}" ${((st.assessment||{}).lr===n)?'selected':''}>${n}</option>`).join('')}</select></div>
      <div class="assessment-item"><label>Grammatical Range & Accuracy</label><select id="self-gra">${[1,2,3,4,5,6,7,8,9].map(n=>`<option value="${n}" ${((st.assessment||{}).gra===n)?'selected':''}>${n}</option>`).join('')}</select></div>
      <div class="assessment-item"><label>Pronunciation</label><select id="self-pr">${[1,2,3,4,5,6,7,8,9].map(n=>`<option value="${n}" ${((st.assessment||{}).pr===n)?'selected':''}>${n}</option>`).join('')}</select></div>
    </div>
    <div class="field"><label>Average (self-estimate)</label><div class="rating-display" id="self-avg">—</div></div>
    <div class="field"><label>What did I do well?</label><textarea class="textarea" id="self-well" placeholder="...">${esc((st.assessment||{}).well || '')}</textarea></div>
    <div class="field"><label>Which vocabulary did I use?</label><textarea class="textarea" id="self-vocab" placeholder="...">${esc((st.assessment||{}).vocab || '')}</textarea></div>
    <div class="field"><label>Which grammar mistakes did I make?</label><textarea class="textarea" id="self-gramm" placeholder="...">${esc((st.assessment||{}).gramm || '')}</textarea></div>
    <div class="field"><label>What should I improve next time?</label><textarea class="textarea" id="self-improve" placeholder="...">${esc((st.assessment||{}).improve || '')}</textarea></div>
    <div class="btn-row" style="margin-top:18px;border-top:1px solid var(--border);padding-top:14px;">
      <button class="btn success" id="cue-complete">✓ Save & Mark Completed</button>
      <button class="btn" id="cue-save">💾 Save Only</button>
      ${(c.sampleAnswers && c.sampleAnswers.length) ? `<button class="btn" id="cue-show-answer">📖 Show Sample Answer</button>` : ''}
      <button class="btn" id="cue-close">Close</button>
    </div>
    ${(c.sampleAnswers && c.sampleAnswers.length) ? `
      <div class="answer-area" id="cue-answer-area" style="margin-top:14px;">
        <div class="answer-label">📖 Sample Answer${c.sampleAnswers.length > 1 ? `s (${c.sampleAnswers.length})` : ''} (from Makkar IELTS book):</div>
        ${c.sampleAnswers.map((ans, ai) => `<div class="answer-text" style="margin-bottom:${c.sampleAnswers.length > 1 ? '12px' : '0'};${c.sampleAnswers.length > 1 ? 'padding-bottom:10px;border-bottom:1px dashed var(--border);' : ''}">${c.sampleAnswers.length > 1 ? `<b style="color:var(--text-soft);font-size:12px;">Answer ${ai+1}:</b><br>` : ''}${esc(ans)}</div>`).join('')}
      </div>` : ''}
    ${c.part3 && c.part3.length ? `
      <div style="margin-top:18px;border-top:1px solid var(--border);padding-top:14px;">
        <h3 style="font-size:15px;margin-bottom:10px;">Part 3 Follow-up Questions (${c.part3.length})</h3>
        <div style="font-size:12px;color:var(--text-soft);margin-bottom:8px;">Practise these after your cue card. Click any to add it to your practice history.</div>
        ${c.part3.map((q,i) => {
          const pid = `p3-${c.num}-${i}`;
          const pst = getQ(pid);
          const pHasAns = q.a && q.a.trim().length > 10;
          return `<div class="q-card ${pst.status==='practised'||pst.status==='mastered'?'completed':''}" style="margin-bottom:6px;padding:10px 12px;">
            <div class="q-head"><div class="q-num">${i+1}</div><div class="q-text" style="font-size:14px;">${esc(q.q)}</div></div>
            <div class="q-meta">
              <button class="btn sm" onclick="toggleComplete('${pid}');openCueCard(${c.num});">${pst.status==='practised'||pst.status==='mastered'?'✓ Completed':'○ Mark Complete'}</button>
              <button class="btn sm ${pst.bookmarked?'success':''}" onclick="toggleBookmark('${pid}');openCueCard(${c.num});">${pst.bookmarked?'★ Saved':'☆ Bookmark'}</button>
              ${pHasAns ? `<button class="btn sm" onclick="toggleAnswer('${pid}',this)">📖 Show Answer</button>` : ''}
            </div>
            ${pHasAns ? `<div class="answer-area" data-answer-for="${pid}">
              <div class="answer-label">📖 Sample Answer:</div>
              <div class="answer-text">${esc(q.a)}</div>
            </div>` : ''}
          </div>`;
        }).join('')}
      </div>` : ''}
  `;
  $('#cue-overlay').classList.add('open');

  // bindings
  $('#cue-close').addEventListener('click', closeCueOverlay);
  $('#cue-save').addEventListener('click', saveCueCard);
  $('#cue-complete').addEventListener('click', () => { saveCueCard(); const q = getQ(id); q.status = 'practised'; q.lastPractised = Date.now(); setQ(id, q); addHistory(id); closeCueOverlay(); toast('Cue card marked as completed!'); renderPart2Cards(); });
  const cueAnsBtn = $('#cue-show-answer');
  if (cueAnsBtn) cueAnsBtn.addEventListener('click', () => {
    const area = $('#cue-answer-area');
    area.classList.toggle('open');
    cueAnsBtn.textContent = area.classList.contains('open') ? '📖 Hide Sample Answer' : '📖 Show Sample Answer';
  });
  $('#cue-start').addEventListener('click', () => startCueTimer());
  $('#cue-pause').addEventListener('click', () => pauseCueTimer());
  $('#cue-reset').addEventListener('click', () => resetCueTimer());
  $('#cue-skip-prep').addEventListener('click', () => skipToSpeak());
  $('#cue-prep-notes').addEventListener('input', e => { const q = getQ(id); q.prepNotes = e.target.value; setQ(id, q); });
  ['fc','lr','gra','pr'].forEach(k => $('#self-'+k).addEventListener('change', updateSelfAvg));
  $('#cue-prep-input').addEventListener('change', e => { state.settings.prepTime = +e.target.value; saveState(); resetCueTimer(); });
  $('#cue-speak-input').addEventListener('change', e => { state.settings.speakTime = +e.target.value; saveState(); if (cuePhase === 'speak') resetCueTimer(); });
  updateSelfAvg();
}
window.openCueCard = openCueCard;

function closeCueOverlay() {
  $('#cue-overlay').classList.remove('open');
  if (cueTimer) { clearInterval(cueTimer); cueTimer = null; }
}
function saveCueCard() {
  const num = state.lastVisited.cueNum;
  const id = `p2-${num}`;
  const q = getQ(id);
  q.prepNotes = $('#cue-prep-notes').value;
  q.assessment = q.assessment || {};
  ['fc','lr','gra','pr'].forEach(k => q.assessment[k] = +$('#self-'+k).value);
  q.assessment.well = $('#self-well').value;
  q.assessment.vocab = $('#self-vocab').value;
  q.assessment.gramm = $('#self-gramm').value;
  q.assessment.improve = $('#self-improve').value;
  q.assessment.avg = (+q.assessment.fc + q.assessment.lr + q.assessment.gra + q.assessment.pr) / 4;
  setQ(id, q);
  toast('Saved!');
}
function updateSelfAvg() {
  const vals = ['fc','lr','gra','pr'].map(k => +$('#self-'+k).value);
  const avg = (vals[0]+vals[1]+vals[2]+vals[3]) / 4;
  $('#self-avg').textContent = avg.toFixed(1);
}
let cuePhase = 'prep';
let cueSecondsLeft = 0;
function startCueTimer() {
  if (cueTimer) return;
  if (cueSecondsLeft <= 0) cueSecondsLeft = cuePhase === 'prep' ? state.settings.prepTime : state.settings.speakTime;
  $('#cue-start').disabled = true;
  $('#cue-pause').disabled = false;
  cueTimer = setInterval(() => {
    cueSecondsLeft--;
    updateCueDisplay();
    if (cueSecondsLeft <= 0) {
      clearInterval(cueTimer); cueTimer = null;
      if (cuePhase === 'prep') {
        cuePhase = 'speak';
        cueSecondsLeft = state.settings.speakTime;
        $('#cue-phase').textContent = 'Speaking';
        toast('Prep time over — start speaking now!');
        startCueTimer();
      } else {
        $('#cue-phase').textContent = 'Finished';
        $('#cue-start').disabled = true;
        $('#cue-pause').disabled = true;
        toast('Speaking time finished!');
      }
    }
  }, 1000);
}
function pauseCueTimer() {
  if (cueTimer) { clearInterval(cueTimer); cueTimer = null; $('#cue-start').disabled = false; $('#cue-pause').disabled = true; }
}
function resetCueTimer() {
  if (cueTimer) { clearInterval(cueTimer); cueTimer = null; }
  cuePhase = 'prep';
  cueSecondsLeft = state.settings.prepTime;
  $('#cue-start').disabled = false;
  $('#cue-pause').disabled = true;
  $('#cue-phase').textContent = 'Preparation';
  updateCueDisplay();
}
function skipToSpeak() {
  if (cueTimer) { clearInterval(cueTimer); cueTimer = null; }
  cuePhase = 'speak';
  cueSecondsLeft = state.settings.speakTime;
  $('#cue-phase').textContent = 'Speaking';
  $('#cue-start').disabled = false;
  $('#cue-pause').disabled = true;
  updateCueDisplay();
}
function updateCueDisplay() {
  const el = $('#cue-display');
  el.textContent = formatTime(cueSecondsLeft);
  el.classList.remove('warning', 'danger');
  if (cueSecondsLeft <= 10) el.classList.add('danger');
  else if (cueSecondsLeft <= 30) el.classList.add('warning');
}
function formatTime(s) {
  const m = Math.floor(s / 60);
  const sec = s % 60;
  return `${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
}

// ===== Part 3 =====
let p3CurrentCue = null;
let p3Filter = 'all';
let p3Shuffled = false;
let p3TopicFilterText = '';
let p3PracticeIdx = 0;

function renderPart3() {
  if (p3CurrentCue == null) p3CurrentCue = DATA.part2[0] ? DATA.part2[0].num : null;
  renderPart3Topics();
  renderPart3Questions();
}
function renderPart3Topics() {
  // Topics are the cue cards that HAVE Part 3 follow-ups
  let topics = DATA.part2.filter(c => c.part3 && c.part3.length);
  if (p3TopicFilterText) {
    const t = p3TopicFilterText.toLowerCase();
    topics = topics.filter(c => c.title.toLowerCase().includes(t));
  }
  if (p3Filter === 'completed' || p3Filter === 'incomplete') {
    topics = topics.filter(c => {
      const total = c.part3.length;
      const done = c.part3.filter((_, qi) => {
        const q = getQ(`p3-${c.num}-${qi}`);
        return q.status === 'practised' || q.status === 'mastered';
      }).length;
      return p3Filter === 'completed' ? done === total : done < total;
    });
  }
  const container = $('#p3-topics');
  if (topics.length === 0) {
    container.innerHTML = '<div style="padding:14px;color:var(--text-soft);font-size:13px;">No topics match.</div>';
    return;
  }
  container.innerHTML = topics.map(c => {
    const done = c.part3.filter((_, qi) => {
      const q = getQ(`p3-${c.num}-${qi}`);
      return q.status === 'practised' || q.status === 'mastered';
    }).length;
    const total = c.part3.length;
    return `<div class="topic-item ${c.num===p3CurrentCue?'active':''}" onclick="selectPart3TopicByCue(${c.num})">
      <span class="name" style="font-size:12px;">${esc(c.title.length>50?c.title.slice(0,50)+'…':c.title)}</span>
      <span class="count">${done}/${total}</span>
    </div>`;
  }).join('');
}
function selectPart3TopicByCue(num) {
  p3CurrentCue = num;
  p3Shuffled = false;
  state.lastVisited = state.lastVisited || {};
  state.lastVisited.part = 3;
  state.lastVisited.topic = num;
  saveState();
  renderPart3Topics();
  renderPart3Questions();
}
window.selectPart3TopicByCue = selectPart3TopicByCue;
function renderPart3Questions() {
  const c = DATA.part2.find(x => x.num === p3CurrentCue);
  if (!c) { $('#p3-questions').innerHTML = ''; return; }
  $('#p3-current-topic').textContent = c.title;
  let qs = c.part3.map((q, i) => ({ q, i }));
  if (p3Shuffled) qs = qs.slice().sort(() => Math.random() - 0.5);
  const done = c.part3.filter((_, qi) => {
    const qq = getQ(`p3-${c.num}-${qi}`);
    return qq.status === 'practised' || qq.status === 'mastered';
  }).length;
  const total = c.part3.length;
  const pct = total ? Math.round(done/total*100) : 0;
  $('#p3-questions').innerHTML = `
    <div class="card" style="margin-bottom:14px;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
      <div style="font-size:13px;color:var(--text-soft);">${done} of ${total} completed • <b>${pct}%</b></div>
      <div style="height:8px;flex:1;max-width:200px;background:var(--border);border-radius:4px;overflow:hidden;"><div style="height:100%;width:${pct}%;background:var(--orange);"></div></div>
    </div>
    ${qs.map(({q, i}) => {
      const id = `p3-${c.num}-${i}`;
      const st = getQ(id);
      const hasAnswer = q.a && q.a.trim().length > 10;
      return `<div class="q-card ${st.status==='practised'?'completed':''} ${st.bookmarked?'bookmarked':''} ${st.status==='needs-revision'?'revision':''} ${st.status==='mastered'?'mastered':''}">
        <div class="q-head"><div class="q-num">${i+1}</div><div class="q-text">${esc(q.q)}</div></div>
        <div class="q-meta">
          <span class="status-pill ${st.status==='practised'?'practised':st.status==='needs-revision'?'needs-revision':st.status==='mastered'?'mastered':'not-practised'}">${st.status.replace('-',' ')}</span>
          <button class="btn sm" onclick="toggleComplete('${id}');renderPart3Questions();renderPart3Topics();">${st.status==='practised'||st.status==='mastered'?'✓ Completed':'○ Mark Complete'}</button>
          <button class="btn sm ${st.bookmarked?'success':''}" onclick="toggleBookmark('${id}');renderPart3Questions();">${st.bookmarked?'★ Saved':'☆ Bookmark'}</button>
          ${hasAnswer ? `<button class="btn sm" onclick="toggleAnswer('${id}',this)">📖 Show Answer</button>` : ''}
          <button class="btn sm" onclick="document.querySelector('[data-notes-for=&quot;${id}&quot;]').classList.toggle('open')">📝 Notes</button>
          <select class="btn sm" onchange="setStatus('${id}',this.value);renderPart3Questions();renderPart3Topics();" style="padding:5px 8px;">
            <option value="not-practised" ${st.status==='not-practised'?'selected':''}>Not Practised</option>
            <option value="practised" ${st.status==='practised'?'selected':''}>Practised</option>
            <option value="needs-revision" ${st.status==='needs-revision'?'selected':''}>Needs Revision</option>
            <option value="mastered" ${st.status==='mastered'?'selected':''}>Mastered</option>
          </select>
        </div>
        ${hasAnswer ? `<div class="answer-area" data-answer-for="${id}">
          <div class="answer-label">📖 Sample Answer (from Makkar IELTS book):</div>
          <div class="answer-text">${esc(q.a)}</div>
        </div>` : ''}
        ${recorderHTML(id, q.q, '3', st.transcript)}
        <div class="notes-area" data-notes-for="${id}"><textarea class="textarea" placeholder="Your notes..." oninput="updateNotes('${id}',this.value)">${esc(st.notes||'')}</textarea></div>
      </div>`;
    }).join('')}
  `;
}

function toggleAnswer(id, btn) {
  const area = document.querySelector(`[data-answer-for="${id}"]`);
  if (area) {
    area.classList.toggle('open');
    if (btn) btn.textContent = area.classList.contains('open') ? '📖 Hide Answer' : '📖 Show Answer';
  }
}
window.toggleAnswer = toggleAnswer;

function setStatus(id, val) {
  const q = getQ(id);
  q.status = val;
  if (val === 'practised' || val === 'mastered') { q.lastPractised = Date.now(); addHistory(id); }
  setQ(id, q);
  refreshNavCounts();
}
window.setStatus = setStatus;

$('#p3-topic-search').addEventListener('input', e => { p3TopicFilterText = e.target.value; renderPart3Topics(); });
$$('[data-p3-filter]').forEach(el => el.addEventListener('click', () => {
  $$('[data-p3-filter]').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  p3Filter = el.dataset.p3Filter;
  renderPart3Topics();
}));
$('#p3-shuffle').addEventListener('click', () => { p3Shuffled = !p3Shuffled; renderPart3Questions(); toast(p3Shuffled ? 'Questions shuffled' : 'Original order'); });
$('#p3-answers').addEventListener('click', () => {
  const areas = $$('#p3-questions .answer-area');
  const btn = $('#p3-answers');
  const anyOpen = areas.length > 0 && Array.from(areas).some(a => a.classList.contains('open'));
  areas.forEach(a => {
    if (anyOpen) a.classList.remove('open');
    else a.classList.add('open');
  });
  $$('#p3-questions button').forEach(b => {
    if (b.textContent.includes('Answer')) {
      const id = b.getAttribute('onclick')?.match(/'([^']+)'/)?.[1];
      if (id) {
        const area = document.querySelector(`[data-answer-for="${id}"]`);
        if (area) b.textContent = area.classList.contains('open') ? '📖 Hide Answer' : '📖 Show Answer';
      }
    }
  });
  btn.textContent = anyOpen ? '📖 Show All Answers' : '📖 Hide All Answers';
});
$('#p3-print').addEventListener('click', () => printTopic('p3', p3CurrentCue));
// p3-practice button replaced with p3-strict — handler bound in strict mode section

// ===== Part 3 Practice Mode =====
function openP3Practice() {
  const c = DATA.part2.find(x => x.num === p3CurrentCue);
  if (!c || !c.part3.length) { toast('No Part 3 questions for this topic.'); return; }
  p3PracticeIdx = 0;
  renderP3PracticeModal(c);
}
function renderP3PracticeModal(c) {
  const q = c.part3[p3PracticeIdx];
  const id = `p3-${c.num}-${p3PracticeIdx}`;
  const st = getQ(id);
  const hasAns = q.a && q.a.trim().length > 10;
  $('#p3-modal').innerHTML = `
    <h2>Part 3 Practice</h2>
    <div class="sub">${esc(c.title)} — Question ${p3PracticeIdx + 1} of ${c.part3.length}</div>
    <div style="background:var(--bg);padding:18px;border-radius:var(--radius);margin-bottom:14px;">
      <div class="q-text" style="font-size:17px;line-height:1.5;">${esc(q.q)}</div>
    </div>
    <div class="timer" id="p3-timer">
      <div class="phase">Speaking Timer</div>
      <div class="display" id="p3-display">00:00</div>
      <div class="controls">
        <button class="btn primary" id="p3-start">▶ Start</button>
        <button class="btn" id="p3-pause" disabled>⏸ Pause</button>
        <button class="btn" id="p3-reset">↻ Reset</button>
      </div>
    </div>
    <div class="field"><label>Your notes / answer outline</label><textarea class="textarea" id="p3-notes" placeholder="Jot ideas...">${esc(st.notes||'')}</textarea></div>
    ${hasAns ? `<div class="answer-area" id="p3-answer-area">
      <div class="answer-label">📖 Sample Answer (from Makkar IELTS book):</div>
      <div class="answer-text">${esc(q.a)}</div>
    </div>` : ''}
    <div class="btn-row" style="margin-top:14px;">
      <button class="btn" id="p3-prev" ${p3PracticeIdx===0?'disabled':''}>← Previous</button>
      <button class="btn success" id="p3-mark">✓ Mark Completed</button>
      <button class="btn ${st.bookmarked?'success':''}" id="p3-bm">${st.bookmarked?'★ Saved':'☆ Bookmark'}</button>
      ${hasAns ? `<button class="btn" id="p3-show-ans">📖 Show Answer</button>` : ''}
      <button class="btn" id="p3-rand">🎲 Random</button>
      <button class="btn" id="p3-next" ${p3PracticeIdx===c.part3.length-1?'disabled':''}>Next →</button>
      <button class="btn" id="p3-close" style="margin-left:auto;">Close</button>
    </div>
  `;
  $('#p3-overlay').classList.add('open');
  $('#p3-close').addEventListener('click', () => { $('#p3-overlay').classList.remove('open'); if (window._p3Timer) clearInterval(window._p3Timer); renderPart3Questions(); });
  $('#p3-prev').addEventListener('click', () => { if (p3PracticeIdx > 0) { p3PracticeIdx--; renderP3PracticeModal(c); } });
  $('#p3-next').addEventListener('click', () => { if (p3PracticeIdx < c.part3.length - 1) { p3PracticeIdx++; renderP3PracticeModal(c); } });
  $('#p3-rand').addEventListener('click', () => { p3PracticeIdx = Math.floor(Math.random() * c.part3.length); renderP3PracticeModal(c); });
  const p3AnsBtn = $('#p3-show-ans');
  if (p3AnsBtn) p3AnsBtn.addEventListener('click', () => {
    const area = $('#p3-answer-area');
    area.classList.toggle('open');
    p3AnsBtn.textContent = area.classList.contains('open') ? '📖 Hide Answer' : '📖 Show Answer';
  });
  $('#p3-mark').addEventListener('click', () => { const q = getQ(id); q.status = 'practised'; q.lastPractised = Date.now(); q.notes = $('#p3-notes').value; setQ(id, q); addHistory(id); toast('Marked completed!'); if (p3PracticeIdx < c.part3.length-1) { p3PracticeIdx++; renderP3PracticeModal(c); } });
  $('#p3-bm').addEventListener('click', () => { const q = getQ(id); q.bookmarked = !q.bookmarked; setQ(id, q); renderP3PracticeModal(c); });
  $('#p3-notes').addEventListener('input', e => { const q = getQ(id); q.notes = e.target.value; setQ(id, q); });
  $('#p3-start').addEventListener('click', () => startP3Timer());
  $('#p3-pause').addEventListener('click', () => { if (window._p3Timer) { clearInterval(window._p3Timer); window._p3Timer = null; $('#p3-start').disabled = false; $('#p3-pause').disabled = true; } });
  $('#p3-reset').addEventListener('click', () => { if (window._p3Timer) { clearInterval(window._p3Timer); window._p3Timer = null; } window._p3Secs = 0; $('#p3-display').textContent = '00:00'; $('#p3-start').disabled = false; $('#p3-pause').disabled = true; });
}
function startP3Timer() {
  if (window._p3Timer) return;
  if (window._p3Secs == null) window._p3Secs = 0;
  $('#p3-start').disabled = true;
  $('#p3-pause').disabled = false;
  window._p3Timer = setInterval(() => {
    window._p3Secs++;
    const m = Math.floor(window._p3Secs / 60);
    const s = window._p3Secs % 60;
    $('#p3-display').textContent = `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
  }, 1000);
}

// ===== All Questions / Search =====
let searchPart = 'all';
let searchStatus = 'all';
function renderAllQuestions() {
  const val = $('#global-search').value || '';
  doSearch(val);
}
$('#global-search').addEventListener('input', () => doSearch($('#global-search').value));
$$('[data-search-part]').forEach(el => el.addEventListener('click', () => {
  $$('[data-search-part]').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  searchPart = el.dataset.searchPart;
  doSearch($('#global-search').value);
}));
$$('[data-search-status]').forEach(el => el.addEventListener('click', () => {
  $$('[data-search-status]').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  searchStatus = el.dataset.searchStatus;
  doSearch($('#global-search').value);
}));
function doSearch(query) {
  const q = (query || '').toLowerCase().trim();
  let pool = Q_INDEX.all;
  if (searchPart !== 'all') pool = pool.filter(it => it.part === +searchPart);
  if (searchStatus !== 'all') {
    pool = pool.filter(it => {
      const st = getQ(it.id);
      if (searchStatus === 'completed') return st.status === 'practised' || st.status === 'mastered';
      if (searchStatus === 'incomplete') return st.status !== 'practised' && st.status !== 'mastered';
      if (searchStatus === 'bookmarked') return st.bookmarked;
      if (searchStatus === 'revision') return st.status === 'needs-revision';
      return true;
    });
  }
  let results = [];
  if (q) {
    pool.forEach(it => {
      const text = (it.part === 2 ? it.title : it.q || '').toLowerCase();
      const topic = (it.topic || it.title || '').toLowerCase();
      if (text.includes(q) || topic.includes(q)) results.push(it);
    });
  } else {
    results = pool.slice(0, 200);
  }
  results = results.slice(0, 300);
  const container = $('#search-results');
  if (results.length === 0) {
    container.innerHTML = '<div class="card" style="text-align:center;padding:30px;color:var(--text-soft);">No questions match your search.</div>';
    return;
  }
  container.innerHTML = `<div style="font-size:13px;color:var(--text-soft);margin-bottom:10px;">${results.length} result${results.length===1?'':'s'}${q?` for "${esc(q)}"`:''}</div>` +
    results.map(it => {
      const text = it.part === 2 ? it.title : it.q;
      const topic = it.topic || it.title || '';
      return `<div class="search-result" onclick="openQuestionById('${it.id}')">
        <span class="badge p${it.part}">P${it.part}</span>
        <div class="info">
          <div class="topic">${esc(topic)}</div>
          <div class="q">${esc(text.length > 140 ? text.slice(0,140)+'…' : text)}</div>
        </div>
      </div>`;
    }).join('');
}

function openQuestionById(id) {
  const item = Q_INDEX.byId[id];
  if (!item) return;
  if (item.part === 1) {
    showPage('part1');
    setTimeout(() => selectPart1Topic(item.topicNum), 80);
    setTimeout(() => {
      const el = document.querySelector(`[data-qid="${id}"]`);
      if (el) el.scrollIntoView({behavior:'smooth', block:'center'});
    }, 200);
  } else if (item.part === 2) {
    showPage('part2');
    setTimeout(() => openCueCard(item.cueNum), 200);
  } else if (item.part === 3) {
    showPage('part3');
    setTimeout(() => selectPart3TopicByCue(item.cueNum), 80);
    setTimeout(() => {
      const el = document.querySelector(`[data-qid="${id}"]`);
      if (el) el.scrollIntoView({behavior:'smooth', block:'center'});
    }, 200);
  }
}
window.openQuestionById = openQuestionById;

// ===== Bookmarks =====
function renderBookmarks() {
  const bm = Q_INDEX.all.filter(it => getQ(it.id).bookmarked);
  const container = $('#bookmarks-list');
  if (bm.length === 0) {
    container.innerHTML = '<div class="card" style="text-align:center;padding:30px;color:var(--text-soft);">No bookmarks yet. Use the ☆ Bookmark button on any question to save it here.</div>';
    return;
  }
  container.innerHTML = bm.map(it => {
    const text = it.part === 2 ? it.title : it.q;
    const topic = it.topic || it.title || '';
    return `<div class="search-result" onclick="openQuestionById('${it.id}')">
      <span class="badge p${it.part}">P${it.part}</span>
      <div class="info">
        <div class="topic">${esc(topic)}</div>
        <div class="q">${esc(text.length > 140 ? text.slice(0,140)+'…' : text)}</div>
      </div>
      <button class="btn sm danger" onclick="event.stopPropagation();toggleBookmark('${it.id}');renderBookmarks();">✕</button>
    </div>`;
  }).join('');
}

// ===== Revision =====
function renderRevision() {
  const rv = Q_INDEX.all.filter(it => getQ(it.id).status === 'needs-revision');
  const container = $('#revision-list');
  if (rv.length === 0) {
    container.innerHTML = '<div class="card" style="text-align:center;padding:30px;color:var(--text-soft);">No questions need revision. Mark questions as "Needs Revision" using the status dropdown to add them here.</div>';
    return;
  }
  container.innerHTML = rv.map(it => {
    const text = it.part === 2 ? it.title : it.q;
    const topic = it.topic || it.title || '';
    return `<div class="search-result" onclick="openQuestionById('${it.id}')">
      <span class="badge p${it.part}">P${it.part}</span>
      <div class="info">
        <div class="topic">${esc(topic)}</div>
        <div class="q">${esc(text.length > 140 ? text.slice(0,140)+'…' : text)}</div>
      </div>
    </div>`;
  }).join('');
}
$('#rev-practice-all').addEventListener('click', () => {
  const rv = Q_INDEX.all.filter(it => getQ(it.id).status === 'needs-revision');
  if (rv.length === 0) { toast('No revision questions.'); return; }
  // open focus mode on revision questions
  toast('Use the Needs Revision page to review questions. Select a topic in Part 1, 2, or 3 and click Strict Practice.');
});

// ===== History =====
function renderHistory() {
  const hist = (state.history || []).slice().reverse();
  const container = $('#history-list');
  if (hist.length === 0) {
    container.innerHTML = '<div class="card" style="text-align:center;padding:30px;color:var(--text-soft);">No practice history yet.</div>';
    return;
  }
  container.innerHTML = hist.map(h => `
    <div class="search-result" onclick="openQuestionById('${h.id}')">
      <span class="badge p${h.part}">P${h.part}</span>
      <div class="info">
        <div class="topic">${esc(h.topic || '')}</div>
        <div class="q">${esc(h.text.length > 140 ? h.text.slice(0,140)+'…' : h.text)}</div>
      </div>
      <span class="time" style="font-size:11px;color:var(--text-soft);">${new Date(h.ts).toLocaleString()}</span>
    </div>
  `).join('');
}
$('#clear-history').addEventListener('click', () => {
  if (confirm('Clear all practice history? This will not affect your completion status, bookmarks, or notes.')) {
    state.history = [];
    saveState();
    renderHistory();
    toast('History cleared.');
  }
});

// ===== Settings =====
function renderSettings() {
  $('#setting-theme').value = state.settings.theme;
  $('#setting-prep-time').value = state.settings.prepTime;
  $('#setting-speak-time').value = state.settings.speakTime;
}
$('#setting-theme').addEventListener('change', e => applyTheme(e.target.value));
$('#setting-prep-time').addEventListener('change', e => { state.settings.prepTime = +e.target.value; saveState(); });
$('#setting-speak-time').addEventListener('change', e => { state.settings.speakTime = +e.target.value; saveState(); });

// ===== Export / Import =====
$('#export-data').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `tareq_ielts_backup_${new Date().toISOString().slice(0,10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
  toast('Backup exported.');
});
$('#import-data').addEventListener('click', () => $('#import-file').click());
$('#import-file').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const imported = JSON.parse(reader.result);
      if (!imported.progress || !imported.settings) throw new Error('Invalid file');
      if (confirm('This will REPLACE your current progress. Continue?')) {
        state = Object.assign(JSON.parse(JSON.stringify(DEFAULT_STATE)), imported);
        saveState();
        applyTheme(state.settings.theme);
        showPage('dashboard');
        toast('Backup restored!');
      }
    } catch (err) {
      toast('Invalid backup file: ' + err.message);
    }
  };
  reader.readAsText(file);
  e.target.value = '';
});

$('#reset-progress').addEventListener('click', () => {
  if (confirm('⚠️ This will permanently delete ALL your progress, bookmarks, notes, and history. This CANNOT be undone.\\n\\nType OK in the next prompt to confirm.')) {
    const ans = prompt('Type OK to confirm reset:');
    if (ans === 'OK') {
      state = JSON.parse(JSON.stringify(DEFAULT_STATE));
      saveState();
      applyTheme('light');
      showPage('dashboard');
      toast('All progress reset.');
    }
  }
});

// ===== Random Practice =====
function openRandomPicker() {
  $('#random-modal').innerHTML = `
    <h2>🎲 Random Practice</h2>
    <div class="sub">Pick a question at random to practise.</div>
    <div style="display:flex;flex-direction:column;gap:10px;margin-top:14px;">
      <button class="btn primary" onclick="randomPick('p1')">Part 1 — Random Question</button>
      <button class="btn primary" onclick="randomPick('p2')">Part 2 — Random Cue Card</button>
      <button class="btn primary" onclick="randomPick('p3')">Part 3 — Random Question</button>
      <button class="btn" onclick="randomPick('all')">Any Part (1/2/3)</button>
      <button class="btn" onclick="randomPick('bookmark')">From Bookmarks</button>
      <button class="btn" onclick="randomPick('revision')">From Needs Revision</button>
      <button class="btn" onclick="randomPick('topic')">From a specific Part 1 topic</button>
    </div>
    <button class="btn" id="random-close" style="margin-top:18px;">Close</button>
  `;
  $('#random-overlay').classList.add('open');
  $('#random-close').addEventListener('click', () => $('#random-overlay').classList.remove('open'));
}
window.randomPick = function(kind) {
  let pool = [];
  if (kind === 'p1') pool = Q_INDEX.p1;
  else if (kind === 'p2') pool = Q_INDEX.p2;
  else if (kind === 'p3') pool = Q_INDEX.p3;
  else if (kind === 'all') pool = Q_INDEX.all;
  else if (kind === 'bookmark') pool = Q_INDEX.all.filter(it => getQ(it.id).bookmarked);
  else if (kind === 'revision') pool = Q_INDEX.all.filter(it => getQ(it.id).status === 'needs-revision');
  else if (kind === 'topic') {
    // pick a topic
    const tps = DATA.part1;
    const tp = tps[Math.floor(Math.random() * tps.length)];
    const qi = Math.floor(Math.random() * tp.questions.length);
    $('#random-overlay').classList.remove('open');
    openQuestionById(`p1-${tp.num}-${qi}`);
    return;
  }
  if (pool.length === 0) { toast('No questions available for this option.'); return; }
  const pick = pool[Math.floor(Math.random() * pool.length)];
  $('#random-overlay').classList.remove('open');
  openQuestionById(pick.id);
};

// ===== STRICT EXAMINER PRACTICE MODE =====
// STRICT INVARIANT: The countdown timer is the ONLY automatic authority for ending
// an answer period. Speech Recognition ending, silence, or inactivity MUST NEVER
// trigger completion. Only the timer reaching 00:00 OR an explicit click on the
// "Finish Answer" button can complete the current answer.
const strictState = {
  active: false, part: 0, topicNum: null, questions: [], currentIdx: 0,
  examiner: null, phase: '', paused: false, startTime: 0,
  completedCount: 0, previouslyCompleted: 0, totalCount: 0,
  timer: null, timerSeconds: 0, timerDuration: 0, timerEndsAt: 0, timerPausedRemaining: 0,
  recordingId: null, recognition: null,
  // completionToken is a per-question guard: incremented each time we move to a new
  // question. finishCurrentAnswer captures the token at entry and refuses to run
  // twice for the same question.
  completionToken: 0,
  transitioning: false,
};

function startStrictPractice(part, topicNum) {
  let allQuestions = [];
  let topicName = '', prevCompleted = 0, totalInTopic = 0;

  if (part === 1) {
    const tp = DATA.part1.find(t => t.num === topicNum);
    if (!tp) { toast('Topic not found.'); return; }
    topicName = tp.name; totalInTopic = tp.questions.length;
    tp.questions.forEach((item, qi) => {
      const id = 'p1-' + tp.num + '-' + qi;
      const st = getQ(id);
      if (st.status !== 'practised' && st.status !== 'mastered')
        allQuestions.push({ id, text: item.q, part: 1 });
      else prevCompleted++;
    });
  } else if (part === 2) {
    const c = DATA.part2.find(x => x.num === topicNum);
    if (!c) { toast('Cue card not found.'); return; }
    topicName = c.title; totalInTopic = 1;
    allQuestions.push({ id: 'p2-' + c.num, text: c.title, bullets: c.bullets, part: 2, cueNum: c.num });
  } else if (part === 3) {
    const c = DATA.part2.find(x => x.num === topicNum);
    if (!c || !c.part3 || c.part3.length === 0) { toast('No Part 3 questions for this topic.'); return; }
    topicName = c.title; totalInTopic = c.part3.length;
    c.part3.forEach((item, qi) => {
      const id = 'p3-' + c.num + '-' + qi;
      const st = getQ(id);
      if (st.status !== 'practised' && st.status !== 'mastered')
        allQuestions.push({ id, text: item.q, part: 3 });
      else prevCompleted++;
    });
  }

  if (allQuestions.length === 0) { toast('All questions in this topic are already completed! 🎉'); return; }

  strictState.active = true; strictState.part = part; strictState.topicNum = topicNum;
  strictState.questions = allQuestions; strictState.currentIdx = 0;
  strictState.examiner = generateExaminerIdentity(); strictState.phase = 'intro';
  strictState.paused = false; strictState.startTime = Date.now();
  strictState.completedCount = 0; strictState.previouslyCompleted = prevCompleted;
  strictState.totalCount = totalInTopic || allQuestions.length;
  strictState.recordingId = null; strictState.timer = null; strictState.recognition = null;
  strictState.transitioning = false;
  strictState.completionToken = 0;
  strictState.timerEndsAt = 0; strictState.timerPausedRemaining = 0;

  renderStrictPhase();
  document.getElementById('strict-overlay').classList.add('open');
}

function closeStrictPractice() {
  if (strictState.recordingId) { try { stopRecording(strictState.recordingId); } catch(e){} }
  if (strictState.timer) { clearInterval(strictState.timer); strictState.timer = null; }
  if (strictState.recognition) {
    try { strictState.recognition.onend = null; strictState.recognition.onresult = null; strictState.recognition.onerror = null; strictState.recognition.stop(); } catch(e){}
  }
  stopSpeaking();
  strictState.active = false; strictState.transitioning = false;
  strictState.completionToken++; // invalidate any in-flight completion
  document.getElementById('strict-overlay').classList.remove('open');
}

function clearStrictTimers() {
  if (strictState.timer) { clearInterval(strictState.timer); strictState.timer = null; }
}

function getTopicName() {
  if (strictState.part === 1) { const tp = DATA.part1.find(t => t.num === strictState.topicNum); return tp ? tp.name : ''; }
  const c = DATA.part2.find(x => x.num === strictState.topicNum); return c ? c.title : '';
}

function getTimeLimit() {
  if (strictState.part === 1) return 30;
  if (strictState.part === 2) return getMockSettings().p2Speak;
  return 60; // Part 3
}

function renderStrictPhase() {
  const modal = document.getElementById('strict-modal');
  if (!modal) return;
  if (strictState.phase === 'intro') renderStrictIntro(modal);
  else if (strictState.phase === 'asking' || strictState.phase === 'recording') renderStrictQuestion(modal);
  else if (strictState.phase === 'prep') renderStrictPart2Prep(modal);
  else if (strictState.phase === 'speaking') renderStrictPart2Speaking(modal);
  else if (strictState.phase === 'done') showStrictReport();
}

function renderStrictIntro(modal) {
  const ex = strictState.examiner;
  const partLabel = strictState.part === 1 ? 'Part 1 — Introduction & Interview' : strictState.part === 2 ? 'Part 2 — Individual Long Turn' : 'Part 3 — Two-way Discussion';
  const introText = strictState.part === 1
    ? 'Good morning. My name is ' + ex.name + '. I will be your speaking examiner today. Let us begin with some questions about ' + getTopicName() + '.'
    : strictState.part === 2
    ? 'Good morning. My name is ' + ex.name + '. I will be your speaking examiner today. Now let us move on to Part Two. I am going to give you a topic card.'
    : 'Good morning. My name is ' + ex.name + '. I will be your speaking examiner today. Let us discuss some questions related to ' + getTopicName() + '.';

  modal.innerHTML = '<div style="text-align:center;padding:20px;">' +
    '<div style="width:64px;height:64px;border-radius:50%;background:linear-gradient(135deg,var(--blue),#60A5FA);display:grid;place-items:center;font-size:28px;color:#fff;font-weight:800;margin:0 auto 16px;">' + esc(ex.name.charAt(0)) + '</div>' +
    '<h2 style="font-size:20px;margin-bottom:4px;">' + esc(ex.name) + '</h2>' +
    '<div style="font-size:12px;color:var(--text-soft);margin-bottom:16px;">IELTS Speaking Examiner • ID: ' + esc(ex.id) + '</div>' +
    '<div style="display:inline-block;padding:4px 12px;border-radius:14px;background:var(--blue-light);color:var(--blue-dark);font-size:12px;font-weight:600;margin-bottom:16px;">' + partLabel + '</div>' +
    '<div style="font-size:14px;color:var(--text-soft);margin-bottom:8px;">Topic: <b>' + esc(getTopicName()) + '</b></div>' +
    '<div style="font-size:13px;color:var(--text-soft);margin-bottom:20px;">Questions in this session: <b>' + strictState.questions.length + '</b><br>Previously completed: ' + strictState.previouslyCompleted + ' • Total in topic: ' + strictState.totalCount + '</div>' +
    ttsIndicatorHTML() +
    '<div class="btn-row" style="justify-content:center;">' +
    (TTS.enabled ? '<button class="btn" id="strict-skip-intro">Skip Introduction →</button>' : '<button class="btn primary" id="strict-skip-intro">Begin Practice</button>') +
    '</div><div style="text-align:center;margin-top:10px;"><button class="btn danger sm" id="strict-exit">End Examination</button></div></div>';

  document.getElementById('strict-exit').addEventListener('click', () => { if (confirm('End the examination?')) showStrictReport(); });
  document.getElementById('strict-skip-intro').addEventListener('click', () => { stopSpeaking(); goToNextQuestion(); });

  if (TTS.enabled) {
    speak(introText, { onend: () => { if (strictState.phase === 'intro' && !strictState.transitioning) goToNextQuestion(); } });
  } else {
    // Auto-start after 2s if no TTS — but only once
    setTimeout(() => { if (strictState.phase === 'intro' && !strictState.transitioning) goToNextQuestion(); }, 2000);
  }
}

function goToNextQuestion() {
  if (strictState.transitioning) return;
  strictState.transitioning = true;

  if (strictState.currentIdx >= strictState.questions.length) {
    strictState.phase = 'done'; strictState.transitioning = false;
    showStrictReport(); return;
  }

  if (strictState.part === 2) {
    strictState.phase = 'prep'; strictState.transitioning = false;
    renderStrictPhase(); return;
  }

  // Part 1 or Part 3
  strictState.phase = 'asking';
  strictState.transitioning = false;
  renderStrictPhase();
  // askCurrentQuestion is called from within renderStrictQuestion when phase === 'asking'
}

function renderStrictQuestion(modal) {
  const q = strictState.questions[strictState.currentIdx];
  if (!q) { showStrictReport(); return; }
  const total = strictState.questions.length;
  const ex = strictState.examiner;
  const partLabel = 'Part ' + strictState.part;
  const timeLimit = getTimeLimit();
  // When rendering during recording (e.g. on pause/resume), use the live remaining
  // time instead of resetting the display back to the full limit.
  const displaySeconds = (strictState.phase === 'recording' && strictState.timerSeconds > 0)
    ? strictState.timerSeconds : timeLimit;
  const minStr = String(Math.floor(displaySeconds / 60)).padStart(2, '0');
  const secStr = String(displaySeconds % 60).padStart(2, '0');
  const isRecording = strictState.phase === 'recording';
  const statusHTML = isRecording
    ? (strictState.paused
        ? '<span style="color:#EA580C;font-weight:600;">⏸ Paused — click Resume to continue</span>'
        : '<span style="color:#DC2626;font-weight:600;">● Recording — Please answer now</span>')
    : '<span style="color:var(--blue);">🔊 Examiner is speaking...</span>';
  // Compute progress bar width based on current state (so pause/resume doesn't reset it)
  let barPct = 0;
  if (isRecording && strictState.timerDuration > 0) {
    barPct = Math.min(100, Math.max(0, ((strictState.timerDuration - displaySeconds) / strictState.timerDuration) * 100));
  }

  modal.innerHTML = '<div style="text-align:center;padding:16px;">' +
    '<div style="display:flex;gap:10px;align-items:center;justify-content:center;margin-bottom:12px;">' +
    '<div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--blue),#60A5FA);display:grid;place-items:center;font-size:16px;color:#fff;font-weight:700;">' + esc(ex.name.charAt(0)) + '</div>' +
    '<div style="text-align:left;"><div style="font-size:13px;font-weight:600;">' + esc(ex.name) + '</div>' +
    '<div style="font-size:11px;color:var(--text-soft);">Examiner ID: ' + esc(ex.id) + '</div></div></div>' +
    '<div style="display:inline-block;padding:3px 10px;border-radius:12px;background:var(--blue-light);color:var(--blue-dark);font-size:11px;font-weight:600;margin-bottom:8px;">' + partLabel + ' • ' + esc(getTopicName()) + '</div>' +
    '<div style="font-size:13px;color:var(--text-soft);margin-bottom:12px;">Question ' + (strictState.currentIdx + 1) + ' of ' + total + ' • Remaining: ' + (total - strictState.currentIdx) + '</div>' +
    '<div class="mock-question-display">' + esc(q.text) + '</div>' +
    ttsIndicatorHTML() +
    '<div id="strict-rec-status" style="margin:10px 0;font-size:14px;">' + statusHTML + '</div>' +
    '<div id="strict-timer-display" style="font-size:36px;font-weight:800;font-variant-numeric:tabular-nums;color:' + (displaySeconds <= 10 ? '#DC2626' : displaySeconds <= 20 ? '#EA580C' : 'var(--text)') + ';">' + minStr + ':' + secStr + '</div>' +
    '<div style="height:6px;background:var(--border);border-radius:4px;overflow:hidden;margin:8px auto;max-width:300px;"><div id="strict-progress-bar" style="height:100%;width:' + barPct + '%;background:var(--blue);transition:width .3s;"></div></div>' +
    '<div class="btn-row" style="justify-content:center;margin-top:16px;">' +
    (isRecording ? '<button class="btn success" id="strict-finished">✓ Finish Answer</button>' : '') +
    '<button class="btn sm" id="strict-repeat">Repeat Question</button>' +
    '<button class="btn sm" id="strict-skip">Skip Question</button>' +
    (strictState.paused ? '<button class="btn primary" id="strict-resume">Resume</button>' : '<button class="btn sm" id="strict-pause">Pause</button>') +
    '<button class="btn sm" id="strict-mute">' + (TTS.enabled ? '🔇 Mute' : '🔊 Unmute') + '</button>' +
    '</div><div style="text-align:center;margin-top:10px;"><button class="btn danger sm" id="strict-exit">End Examination</button></div></div>';

  // Bind controls — use null-safe binding
  const bindSafe = (id, evt, handler) => { const el = document.getElementById(id); if (el) el.addEventListener(evt, handler); };
  bindSafe('strict-exit', 'click', () => { if (confirm('End examination?')) showStrictReport(); });
  bindSafe('strict-repeat', 'click', () => {
    stopSpeaking(); clearStrictTimers();
    // Detach recognition handlers BEFORE stopping so onend can't trigger anything weird
    if (strictState.recognition) { try { strictState.recognition.onend = null; strictState.recognition.onresult = null; strictState.recognition.onerror = null; strictState.recognition.stop(); } catch(e){} strictState.recognition = null; }
    if (strictState.recordingId) { try { stopRecording(strictState.recordingId); } catch(e){} strictState.recordingId = null; }
    strictState.completionToken++; // invalidate any in-flight completion
    strictState._completedToken = null;
    strictState.phase = 'asking'; strictState.transitioning = false;
    renderStrictQuestion(modal);
  });
  bindSafe('strict-skip', 'click', () => {
    stopSpeaking(); clearStrictTimers();
    if (strictState.recognition) { try { strictState.recognition.onend = null; strictState.recognition.onresult = null; strictState.recognition.onerror = null; strictState.recognition.stop(); } catch(e){} strictState.recognition = null; }
    if (strictState.recordingId) { try { stopRecording(strictState.recordingId); } catch(e){} strictState.recordingId = null; }
    strictState.completionToken++; // invalidate any in-flight completion
    strictState._completedToken = null;
    toast('Question skipped (not marked completed).');
    strictState.currentIdx++; strictState.transitioning = false;
    goToNextQuestion();
  });
  bindSafe('strict-pause', 'click', () => {
    // PAUSE: keep the timer alive but freeze the end-time so the countdown stops.
    // Recognition is paused (not torn down) so it can resume.
    if (!strictState.paused) pauseStrictTimer();
    stopSpeaking();
    if (strictState.recognition) { try { strictState.recognition.stop(); } catch(e){} }
    renderStrictQuestion(modal);
  });
  bindSafe('strict-resume', 'click', () => {
    // RESUME: if recording, resume the timer from the same remaining time.
    if (strictState.paused) resumeStrictTimer();
    if (strictState.phase === 'asking') askCurrentQuestion();
    else if (strictState.phase === 'recording') {
      // Restart recognition for live transcript (timer already resumed)
      if (!strictState.recognition) startStrictRecognition();
    }
  });
  bindSafe('strict-mute', 'click', () => {
    TTS.enabled = !TTS.enabled;
    state.settings = state.settings || {}; state.settings.tts = state.settings.tts || {}; state.settings.tts.enabled = TTS.enabled; saveState();
    renderStrictQuestion(modal);
  });
  const finBtn = document.getElementById('strict-finished');
  if (finBtn) finBtn.addEventListener('click', () => { finishCurrentAnswer('manual'); });

  // Auto-start asking if in asking phase (NOT recording phase)
  if (strictState.phase === 'asking') {
    askCurrentQuestion();
  }
}

function askCurrentQuestion() {
  const q = strictState.questions[strictState.currentIdx];
  if (!q) { showStrictReport(); return; }

  if (TTS.enabled) {
    speak(q.text, { onend: () => {
      // Only start recording if we're still in 'asking' phase (not skipped/paused)
      if (strictState.phase === 'asking' && !strictState.paused) startRecordingPhase();
    } });
  } else {
    setTimeout(() => { if (strictState.phase === 'asking' && !strictState.paused) startRecordingPhase(); }, 1500);
  }
}

function startRecordingPhase() {
  const q = strictState.questions[strictState.currentIdx];
  if (!q) return;
  strictState.phase = 'recording';
  strictState.recordingId = q.id;
  // Invalidate any in-flight completion from a previous question and arm a fresh token
  strictState.completionToken++;

  // Update UI to show recording status
  const statusEl = document.getElementById('strict-rec-status');
  if (statusEl) statusEl.innerHTML = '<span style="color:#DC2626;font-weight:600;">● Recording — Please answer now</span>';

  // Show Finish button
  const btnRow = document.querySelector('#strict-modal .btn-row');
  if (btnRow && !document.getElementById('strict-finished')) {
    const finBtn = document.createElement('button');
    finBtn.className = 'btn success'; finBtn.id = 'strict-finished'; finBtn.textContent = '✓ Finish Answer';
    finBtn.addEventListener('click', () => finishCurrentAnswer('manual'));
    btnRow.insertBefore(finBtn, btnRow.firstChild);
  }

  // Try to start recording (may fail if no mic — that's OK, timer still runs)
  if (typeof startRecording === 'function') {
    startRecording(q.id, q.text, strictState.part).catch(() => {});
  }

  // Start continuous speech recognition for live transcript — NEVER completes the answer.
  startStrictRecognition();

  // Start the countdown timer — this is the SOLE automatic authority for completion.
  startAnswerTimer();
}

// Date-based countdown timer. We compute remaining time from Date.now() against a
// fixed end timestamp, so browser throttling of setInterval cannot cause the
// displayed/elapsed time to drift.
function startAnswerTimer() {
  clearStrictTimers();
  const timeLimit = getTimeLimit();
  strictState.timerSeconds = timeLimit;
  strictState.timerDuration = timeLimit;
  strictState.timerEndsAt = Date.now() + timeLimit * 1000;
  strictState.timerPausedRemaining = 0;
  updateStrictTimerDisplay();
  strictState.timer = setInterval(() => {
    if (strictState.paused) return; // pause: do not advance the clock
    const remainingMs = strictState.timerEndsAt - Date.now();
    const remainingSec = Math.max(0, Math.ceil(remainingMs / 1000));
    strictState.timerSeconds = remainingSec;
    updateStrictTimerDisplay();
    if (remainingMs <= 0) {
      clearStrictTimers();
      // Timer expiration — automatic completion. Source labelled 'timer'.
      finishCurrentAnswer('timer');
    }
  }, 250);
}

function pauseStrictTimer() {
  if (!strictState.timerEndsAt) return;
  strictState.timerPausedRemaining = Math.max(0, strictState.timerEndsAt - Date.now());
  strictState.paused = true;
}

function resumeStrictTimer() {
  if (!strictState.timerPausedRemaining) return;
  strictState.timerEndsAt = Date.now() + strictState.timerPausedRemaining;
  strictState.timerPausedRemaining = 0;
  strictState.paused = false;
}

function updateStrictTimerDisplay() {
  const el = document.getElementById('strict-timer-display');
  if (!el) return;
  const min = Math.floor(strictState.timerSeconds / 60);
  const sec = strictState.timerSeconds % 60;
  el.textContent = String(min).padStart(2, '0') + ':' + String(sec).padStart(2, '0');
  el.style.color = strictState.timerSeconds <= 10 ? '#DC2626' : strictState.timerSeconds <= 20 ? '#EA580C' : 'var(--text)';
  const bar = document.getElementById('strict-progress-bar');
  if (bar && strictState.timerDuration > 0) {
    const pct = ((strictState.timerDuration - strictState.timerSeconds) / strictState.timerDuration) * 100;
    bar.style.width = Math.min(100, Math.max(0, pct)) + '%';
  }
}

// Continuous SpeechRecognition for live transcript ONLY.
// This NEVER triggers answer completion. If the browser stops recognition
// (silence, no-speech, automatic timeout, network hiccup) we simply restart
// it as long as we are still in the recording phase. The countdown timer
// remains the only authority that can finish the answer.
function startStrictRecognition() {
  // Tear down any previous recognition instance and detach handlers
  if (strictState.recognition) {
    try { strictState.recognition.onend = null; strictState.recognition.onresult = null; strictState.recognition.onerror = null; strictState.recognition.stop(); } catch(e){}
    strictState.recognition = null;
  }
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return;
  try {
    const rec = new SR();
    rec.continuous = true;
    rec.interimResults = true;
    rec.lang = 'en-US';
    rec.onresult = (event) => {
      // We do NOT call finishCurrentAnswer here. Just keep transcript alive.
      // (Transcript display handled by the global startRecording() live transcription.)
    };
    rec.onerror = (e) => {
      // no-speech, aborted, network, audio-capture — all non-fatal. Do nothing; onend will fire and we restart.
    };
    rec.onend = () => {
      // Browser stopped listening (silence, timeout, etc.). This does NOT mean the
      // candidate has finished answering. Restart recognition if still recording.
      if (strictState.phase === 'recording' && !strictState.paused && strictState.active) {
        try { rec.start(); } catch(e) {}
      }
    };
    strictState.recognition = rec;
    rec.start();
  } catch(e) {
    // Recognition not available — timer still runs; that's fine.
    strictState.recognition = null;
  }
}

// finishCurrentAnswer completes the current answer exactly once per question.
// Two trigger paths:
//   - 'timer' : countdown reached 00:00 (automatic)
//   - 'manual': candidate clicked the Finish Answer button
// Speech Recognition onend / onerror / onresult MUST NEVER call this.
function finishCurrentAnswer(source) {
  if (strictState.phase !== 'recording') return;
  if (strictState.transitioning) return;
  // Per-question guard: capture the token at entry; if any other caller already
  // advanced the question, the token will have incremented and this call is a no-op.
  const myToken = strictState.completionToken;
  if (strictState._completedToken === myToken) return; // already completed for this question
  strictState._completedToken = myToken;
  strictState.transitioning = true;

  const q = strictState.questions[strictState.currentIdx];
  if (!q) { strictState.transitioning = false; showStrictReport(); return; }

  // Stop everything: timer, recognition (detach handlers first), media recorder
  clearStrictTimers();
  if (strictState.recognition) {
    try { strictState.recognition.onend = null; strictState.recognition.onresult = null; strictState.recognition.onerror = null; strictState.recognition.stop(); } catch(e){}
    strictState.recognition = null;
  }
  if (strictState.recordingId) { try { stopRecording(strictState.recordingId); } catch(e){} }
  strictState.recordingId = null;

  // Mark as completed
  const qState = getQ(q.id);
  qState.status = 'practised'; qState.lastPractised = Date.now();
  setQ(q.id, qState); addHistory(q.id);
  strictState.completedCount++;

  // Show completion
  const statusEl = document.getElementById('strict-rec-status');
  if (statusEl) statusEl.innerHTML = '<span style="color:#16A34A;font-weight:600;">✓ Completed! Next question...</span>';

  // Advance after delay
  setTimeout(() => {
    strictState.currentIdx++;
    strictState.transitioning = false;
    strictState.completionToken++; // arm a fresh token for the next question
    strictState._completedToken = null;
    goToNextQuestion();
  }, 1200);
}

// Part 2 Strict Practice
function renderStrictPart2Prep(modal) {
  const q = strictState.questions[0];
  if (!q) { showStrictReport(); return; }
  const settings = getMockSettings();
  const ex = strictState.examiner;
  const cueCardText = 'Here is your topic: ' + q.text + '. You should say: ' + (q.bullets || []).join('. ') + '. You have one minute to prepare.';

  modal.innerHTML = '<div style="text-align:center;padding:16px;">' +
    '<div style="display:flex;gap:10px;align-items:center;justify-content:center;margin-bottom:12px;">' +
    '<div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--blue),#60A5FA);display:grid;place-items:center;font-size:16px;color:#fff;font-weight:700;">' + esc(ex.name.charAt(0)) + '</div>' +
    '<div style="text-align:left;"><div style="font-size:13px;font-weight:600;">' + esc(ex.name) + '</div>' +
    '<div style="font-size:11px;color:var(--text-soft);">Part 2 — Cue Card</div></div></div>' +
    '<div class="mock-cue-card-display"><div class="cue-title">' + esc(q.text) + '</div>' +
    '<div style="font-size:12px;color:var(--text-soft);text-align:center;margin-bottom:8px;"><b>You should say:</b></div>' +
    '<ul class="cue-bullets">' + (q.bullets || []).map(b => '<li>' + esc(b) + '</li>').join('') + '</ul></div>' +
    ttsIndicatorHTML() +
    '<div class="mock-timer-label">Preparation Time</div>' +
    '<div class="mock-timer-display" id="strict-timer-display">' + String(Math.floor(settings.p2Prep/60)).padStart(2,'0') + ':' + String(settings.p2Prep%60).padStart(2,'0') + '</div>' +
    '<div id="strict-rec-status" style="margin:10px;font-size:13px;">Preparation time — plan your answer</div>' +
    '<div class="btn-row" style="justify-content:center;margin-top:16px;">' +
    '<button class="btn sm" id="strict-mute">' + (TTS.enabled ? '🔇 Mute' : '🔊 Unmute') + '</button>' +
    '<button class="btn sm" id="strict-skip-prep">Skip to Speaking →</button>' +
    '<button class="btn danger sm" id="strict-exit">End</button></div></div>';

  document.getElementById('strict-exit').addEventListener('click', () => { if (confirm('End examination?')) showStrictReport(); });
  document.getElementById('strict-skip-prep').addEventListener('click', () => { stopSpeaking(); clearStrictTimers(); startStrictPart2Speaking(); });
  document.getElementById('strict-mute').addEventListener('click', () => {
    TTS.enabled = !TTS.enabled;
    state.settings = state.settings || {}; state.settings.tts = state.settings.tts || {}; state.settings.tts.enabled = TTS.enabled; saveState();
    renderStrictPart2Prep(modal);
  });

  if (TTS.enabled) {
    speak(cueCardText, { onend: () => { startStrictPrepTimer(); } });
  } else {
    startStrictPrepTimer();
  }

  function startStrictPrepTimer() {
    clearStrictTimers();
    const prepSecs = settings.p2Prep;
    strictState.timerSeconds = prepSecs; strictState.timerDuration = prepSecs;
    strictState.timerEndsAt = Date.now() + prepSecs * 1000;
    updateStrictTimerDisplay();
    strictState.timer = setInterval(() => {
      const remainingSec = Math.max(0, Math.ceil((strictState.timerEndsAt - Date.now()) / 1000));
      strictState.timerSeconds = remainingSec;
      updateStrictTimerDisplay();
      if (remainingSec <= 0) { clearStrictTimers(); startStrictPart2Speaking(); }
    }, 250);
  }
}

function startStrictPart2Speaking() {
  strictState.phase = 'speaking';
  const modal = document.getElementById('strict-modal');
  const q = strictState.questions[0];
  if (!q) { showStrictReport(); return; }
  const settings = getMockSettings();
  const beginText = 'Now, please begin speaking. You have up to two minutes.';

  modal.innerHTML = '<div style="text-align:center;padding:16px;">' +
    '<div class="mock-cue-card-display"><div class="cue-title">' + esc(q.text) + '</div>' +
    '<ul class="cue-bullets">' + (q.bullets || []).map(b => '<li>' + esc(b) + '</li>').join('') + '</ul></div>' +
    ttsIndicatorHTML() +
    '<div class="mock-timer-label">Speaking Time</div>' +
    '<div class="mock-timer-display" id="strict-timer-display">' + String(Math.floor(settings.p2Speak/60)).padStart(2,'0') + ':' + String(settings.p2Speak%60).padStart(2,'0') + '</div>' +
    '<div id="strict-rec-status" style="margin:10px;font-size:14px;"><span style="color:#DC2626;font-weight:600;">● Recording — please speak now</span></div>' +
    '<div class="btn-row" style="justify-content:center;margin-top:16px;">' +
    '<button class="btn success" id="strict-finished">✓ Finish Speaking</button>' +
    '<button class="btn danger sm" id="strict-exit">End</button></div></div>';

  document.getElementById('strict-exit').addEventListener('click', () => { if (confirm('End examination?')) showStrictReport(); });
  document.getElementById('strict-finished').addEventListener('click', () => finishStrictPart2());

  function autoStart() {
    if (TTS.enabled) {
      speak(beginText, { onend: () => beginRecording() });
    } else {
      setTimeout(() => beginRecording(), 1500);
    }
  }

  function beginRecording() {
    strictState.recordingId = q.id;
    // Start continuous speech recognition for live transcript — NEVER auto-completes.
    startStrictRecognition();
    if (typeof startRecording === 'function') {
      startRecording(q.id, q.text, 2).catch(() => {});
    }
    // Start speaking timer (Date-based, throttling-safe)
    clearStrictTimers();
    const speakSecs = settings.p2Speak;
    strictState.timerSeconds = speakSecs; strictState.timerDuration = speakSecs;
    strictState.timerEndsAt = Date.now() + speakSecs * 1000;
    updateStrictTimerDisplay();
    strictState.timer = setInterval(() => {
      const remainingSec = Math.max(0, Math.ceil((strictState.timerEndsAt - Date.now()) / 1000));
      strictState.timerSeconds = remainingSec;
      updateStrictTimerDisplay();
      if (remainingSec <= 0) { clearStrictTimers(); finishStrictPart2(); }
    }, 250);
  }

  autoStart();
}

function finishStrictPart2() {
  if (strictState.transitioning) return;
  strictState.transitioning = true;
  strictState.completionToken++; // invalidate any in-flight completion
  const q = strictState.questions[0];
  if (!q) { strictState.transitioning = false; showStrictReport(); return; }
  clearStrictTimers();
  if (strictState.recognition) {
    try { strictState.recognition.onend = null; strictState.recognition.onresult = null; strictState.recognition.onerror = null; strictState.recognition.stop(); } catch(e){}
    strictState.recognition = null;
  }
  if (strictState.recordingId) { try { stopRecording(strictState.recordingId); } catch(e){} }
  strictState.recordingId = null;
  const qState = getQ(q.id);
  qState.status = 'practised'; qState.lastPractised = Date.now();
  setQ(q.id, qState); addHistory(q.id);
  strictState.completedCount++;
  strictState.phase = 'done'; strictState.transitioning = false;
  showStrictReport();
}

function showStrictReport() {
  clearStrictTimers();
  strictState.completionToken++; // invalidate any in-flight completion
  strictState._completedToken = null;
  if (strictState.recordingId) { try { stopRecording(strictState.recordingId); } catch(e){} }
  if (strictState.recognition) {
    try { strictState.recognition.onend = null; strictState.recognition.onresult = null; strictState.recognition.onerror = null; strictState.recognition.stop(); } catch(e){}
    strictState.recognition = null;
  }
  stopSpeaking();

  const durationSec = Math.floor((Date.now() - strictState.startTime) / 1000);
  const min = Math.floor(durationSec / 60), sec = durationSec % 60;
  const totalCompleted = strictState.previouslyCompleted + strictState.completedCount;
  const pct = strictState.totalCount > 0 ? Math.round((totalCompleted / strictState.totalCount) * 100) : 100;
  const allDone = strictState.completedCount >= strictState.questions.length;
  const modal = document.getElementById('strict-modal');

  modal.innerHTML = '<div style="text-align:center;padding:20px;">' +
    '<div style="font-size:48px;margin-bottom:10px;">' + (allDone ? '🎉' : '📋') + '</div>' +
    '<h2 style="font-size:20px;margin-bottom:8px;">' + (allDone ? 'Session Complete!' : 'Examination Ended') + '</h2>' +
    '<div style="font-size:14px;color:var(--text-soft);margin-bottom:20px;">' + (allDone ? 'Congratulations! You have completed all the unpractised questions in this topic.' : 'Your progress has been saved.') + '</div>' +
    '<div class="card" style="text-align:left;margin-bottom:16px;"><h3 style="font-size:15px;margin-bottom:12px;">Session Report</h3>' +
    '<div style="font-size:13px;color:var(--text-soft);line-height:2;">' +
    '<b>Part:</b> Part ' + strictState.part + '<br>' +
    '<b>Topic:</b> ' + esc(getTopicName()) + '<br>' +
    '<b>Examiner:</b> ' + esc(strictState.examiner.name) + ' (' + esc(strictState.examiner.id) + ')<br>' +
    '<b>Session Duration:</b> ' + min + 'm ' + sec + 's<br>' +
    '<b>Questions completed this session:</b> ' + strictState.completedCount + '<br>' +
    '<b>Previously completed:</b> ' + strictState.previouslyCompleted + '<br>' +
    '<b>Total completed in topic:</b> ' + totalCompleted + ' / ' + strictState.totalCount + '<br>' +
    '<b>Remaining:</b> ' + Math.max(0, strictState.totalCount - totalCompleted) + '<br>' +
    '<b>Completion:</b> ' + pct + '%</div>' +
    '<div style="height:8px;background:var(--border);border-radius:4px;overflow:hidden;margin-top:8px;"><div style="height:100%;width:' + pct + '%;background:var(--green);transition:width .3s;"></div></div></div>' +
    '<div class="btn-row" style="justify-content:center;"><button class="btn primary" id="strict-close-session">Done</button></div></div>';

  document.getElementById('strict-close-session').addEventListener('click', () => {
    closeStrictPractice();
    if (strictState.part === 1) { renderPart1Questions(); renderPart1Topics(); }
    else if (strictState.part === 2) { renderPart2Cards(); }
    else if (strictState.part === 3) { renderPart3Questions(); renderPart3Topics(); }
    refreshNavCounts();
    toast('Practice session ended. ' + strictState.completedCount + ' question(s) completed.');
  });
  strictState.phase = 'done';
}

// Bind strict practice buttons
$('#p1-strict').addEventListener('click', () => {
  if (p1CurrentTopic == null) { toast('Please select a topic first.'); return; }
  startStrictPractice(1, p1CurrentTopic);
});
$('#p3-strict').addEventListener('click', () => {
  if (p3CurrentCue == null) { toast('Please select a topic first.'); return; }
  startStrictPractice(3, p3CurrentCue);
});

window.startStrictPractice = startStrictPractice;
window.closeStrictPractice = closeStrictPractice;

// ===== Print =====
function printTopic(part, num) {
  // Build a printable page in a hidden iframe / new window
  const w = window.open('', '_blank');
  let html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>TAREQ IELTS — Print</title><style>
    body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;padding:30px;color:#222;line-height:1.5;}
    h1{font-size:22px;margin-bottom:6px;}
    .meta{color:#666;font-size:13px;margin-bottom:18px;}
    .q{padding:10px 0;border-bottom:1px solid #ddd;font-size:14px;}
    .q-num{display:inline-block;width:24px;color:#2563EB;font-weight:700;}
    .cue{padding:14px;border:1px solid #ddd;border-radius:6px;margin-bottom:14px;}
    .cue h3{margin:0 0 8px;font-size:16px;}
    .cue ul{margin:6px 0 0 18px;font-size:14px;}
    .footer{margin-top:30px;color:#999;font-size:11px;text-align:center;}
  </style></head><body>`;
  if (part === 'p1') {
    const tp = DATA.part1.find(t => t.num === num);
    if (!tp) return;
    html += `<h1>Part 1 — ${esc(tp.name)}</h1><div class="meta">${tp.questions.length} questions • Makkar IELTS Sep–Dec 2026</div>`;
    tp.questions.forEach((q, i) => { html += `<div class="q"><span class="q-num">${i+1}.</span>${esc(q)}</div>`; });
  } else if (part === 'p3') {
    const c = DATA.part2.find(x => x.num === num);
    if (!c) return;
    html += `<h1>Part 3 — Follow-ups: ${esc(c.title)}</h1><div class="meta">${c.part3.length} questions • Makkar IELTS Sep–Dec 2026</div>`;
    c.part3.forEach((q, i) => { html += `<div class="q"><span class="q-num">${i+1}.</span>${esc(q)}</div>`; });
  } else if (part === 'all-p1') {
    html += `<h1>Part 1 — All Topics</h1><div class="meta">${DATA.part1.length} topics • Makkar IELTS Sep–Dec 2026</div>`;
    DATA.part1.forEach(tp => {
      html += `<h2 style="font-size:16px;margin:18px 0 6px;">${esc(tp.name)}</h2>`;
      tp.questions.forEach((q, i) => { html += `<div class="q"><span class="q-num">${i+1}.</span>${esc(q)}</div>`; });
    });
  } else if (part === 'all-p2') {
    html += `<h1>Part 2 — All Cue Cards</h1><div class="meta">${DATA.part2.length} cue cards • Makkar IELTS Sep–Dec 2026</div>`;
    DATA.part2.forEach(c => {
      html += `<div class="cue"><h3>${c.num}. ${esc(c.title)}</h3><b>You should say:</b><ul>${(c.bullets||[]).map(b=>`<li>${esc(b)}</li>`).join('')}</ul></div>`;
    });
  } else if (part === 'all-p3') {
    html += `<h1>Part 3 — All Follow-up Questions</h1><div class="meta">${Q_INDEX.p3.length} questions • Makkar IELTS Sep–Dec 2026</div>`;
    DATA.part2.forEach(c => {
      if (!c.part3 || !c.part3.length) return;
      html += `<h2 style="font-size:16px;margin:18px 0 6px;">${esc(c.title)}</h2>`;
      c.part3.forEach((q, i) => { html += `<div class="q"><span class="q-num">${i+1}.</span>${esc(q)}</div>`; });
    });
  }
  html += `<div class="footer">Generated by TAREQ IELTS Speaking Practice Platform</div></body></html>`;
  w.document.write(html);
  w.document.close();
  setTimeout(() => w.print(), 300);
}
window.printTopic = printTopic;

// ===== Keyboard shortcuts =====
document.addEventListener('keydown', e => {
  // ignore when typing in inputs/textareas
  const t = e.target.tagName;
  const isTyping = t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT' || e.target.isContentEditable;
  // ESC always works
  if (e.key === 'Escape') {
    if ($('#cue-overlay').classList.contains('open')) { closeCueOverlay(); return; }
    if ($('#p3-overlay').classList.contains('open')) { $('#p3-overlay').classList.remove('open'); if (window._p3Timer) clearInterval(window._p3Timer); return; }
    if ($('#random-overlay').classList.contains('open')) { $('#random-overlay').classList.remove('open'); return; }
    if ($('#strict-overlay').classList.contains('open')) { closeStrictPractice(); return; }
    if ($('#sidebar').classList.contains('open')) { $('#sidebar').classList.remove('open'); return; }
  }
  if (isTyping) return;
  // Strict practice shortcuts
  if ($('#strict-overlay').classList.contains('open')) {
    if (e.key === 'Escape') { e.preventDefault(); closeStrictPractice(); }
    return;
  }
  // Cue card timer space
  if ($('#cue-overlay').classList.contains('open')) {
    if (e.key === ' ') {
      e.preventDefault();
      if ($('#cue-pause').disabled) $('#cue-start').click();
      else $('#cue-pause').click();
    }
    return;
  }
  // Global shortcuts (when no overlay open)
  if (e.key.toLowerCase() === 'f' && !e.ctrlKey && !e.metaKey) {
    e.preventDefault();
    showPage('part1');
    toast('Select a topic and click "🎙 START STRICT PRACTICE"');
  }
});

// ============================================================
// ===== AI AUDIO RECORDING & EVALUATION SYSTEM =====
// ============================================================

// --- Config ---
// AI_SERVER_URL resolution order (highest priority first):
//   1. URL query parameter ?api=https://your-backend.example.com
//   2. localStorage value 'tareq_api_url' (set via the Settings page)
//   3. window.location.origin if hosted on a non-static backend (rare)
//   4. localhost:3001 for local file:// development
//
// This makes it easy to host the frontend on Netlify and connect to a
// backend running on Railway/Render/Fly.io — just visit:
//   https://your-site.netlify.app/?api=https://your-backend.up.railway.app
// or set the API URL permanently in the Settings page.
let AI_SERVER_URL = (function() {
  // 1. URL query parameter
  try {
    const url = new URL(window.location.href);
    const apiParam = url.searchParams.get('api');
    if (apiParam) {
      // Persist for next visit
      try { localStorage.setItem('tareq_api_url', apiParam); } catch(e) {}
      // Clean the URL (remove the ?api=... param) for nicer sharing
      url.searchParams.delete('api');
      try { window.history.replaceState({}, '', url.toString()); } catch(e) {}
      return apiParam.replace(/\/+$/, ''); // strip trailing slash
    }
  } catch(e) {}
  // 2. localStorage
  try {
    const saved = localStorage.getItem('tareq_api_url');
    if (saved && saved.trim()) return saved.trim().replace(/\/+$/, '');
  } catch(e) {}
  // 3. Local file:// → localhost:3001
  if (window.location.protocol === 'file:') return 'http://localhost:3001';
  // 4. Same-origin (if backend served from same domain, e.g. on Railway)
  //    Assume the API lives on the same origin (port-free).
  //    Otherwise fall back to localhost:3001 for development.
  return 'http://localhost:3001';
})();

// Allow runtime updates from the Settings page without page reload
function setApiServerUrl(newUrl) {
  const cleaned = (newUrl || '').trim().replace(/\/+$/, '');
  if (cleaned) {
    try { localStorage.setItem('tareq_api_url', cleaned); } catch(e) {}
  } else {
    try { localStorage.removeItem('tareq_api_url'); } catch(e) {}
  }
  AI_SERVER_URL = cleaned || 'http://localhost:3001';
  return AI_SERVER_URL;
}
window.setApiServerUrl = setApiServerUrl;

// --- IndexedDB for audio blobs ---
const AUDIO_DB_NAME = 'tareq_ielts_audio';
const AUDIO_STORE = 'recordings';
let audioDB = null;

function initAudioDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(AUDIO_DB_NAME, 1);
    req.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains(AUDIO_STORE)) {
        db.createObjectStore(AUDIO_STORE, { keyPath: 'id' });
      }
    };
    req.onsuccess = (e) => { audioDB = e.target.result; resolve(audioDB); };
    req.onerror = (e) => reject(e.target.error);
  });
}

function saveAudioToDB(id, blob, metrics) {
  return new Promise((resolve, reject) => {
    if (!audioDB) { reject(new Error('DB not ready')); return; }
    const tx = audioDB.transaction([AUDIO_STORE], 'readwrite');
    const store = tx.objectStore(AUDIO_STORE);
    const req = store.put({ id, blob, metrics, ts: Date.now() });
    req.onsuccess = () => resolve();
    req.onerror = (e) => reject(e.target.error);
  });
}

function getAudioFromDB(id) {
  return new Promise((resolve, reject) => {
    if (!audioDB) { reject(new Error('DB not ready')); return; }
    const tx = audioDB.transaction([AUDIO_STORE], 'readonly');
    const store = tx.objectStore(AUDIO_STORE);
    const req = store.get(id);
    req.onsuccess = (e) => resolve(e.target.result);
    req.onerror = (e) => reject(e.target.error);
  });
}

function deleteAudioFromDB(id) {
  return new Promise((resolve, reject) => {
    if (!audioDB) { reject(new Error('DB not ready')); return; }
    const tx = audioDB.transaction([AUDIO_STORE], 'readwrite');
    const store = tx.objectStore(AUDIO_STORE);
    const req = store.delete(id);
    req.onsuccess = () => resolve();
    req.onerror = (e) => reject(e.target.error);
  });
}

function getAllAudioKeys() {
  return new Promise((resolve, reject) => {
    if (!audioDB) { reject(new Error('DB not ready')); return; }
    const tx = audioDB.transaction([AUDIO_STORE], 'readonly');
    const store = tx.objectStore(AUDIO_STORE);
    const req = store.getAllKeys();
    req.onsuccess = (e) => resolve(e.target.result);
    req.onerror = (e) => reject(e.target.error);
  });
}

// --- Recording State ---
const recState = {
  activeId: null,
  mediaRecorder: null,
  audioChunks: [],
  stream: null,
  startTime: 0,
  pausedDuration: 0,
  durationTimer: null,
  recognition: null,
  transcriptText: '',
  audioContext: null,
  analyser: null,
  waveformCanvas: null,
  waveformCtx: null,
  animationId: null,
  volumeSamples: [],
  pitchSamples: [],
};

// --- Recording Functions ---
async function startRecording(id, questionText, part) {
  if (recState.activeId && recState.activeId !== id) {
    stopRecording(recState.activeId);
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recState.stream = stream;
    recState.activeId = id;
    recState.audioChunks = [];
    recState.transcriptText = '';
    recState.volumeSamples = [];
    recState.pitchSamples = [];
    recState.startTime = Date.now();
    recState.pausedDuration = 0;

    recState.mediaRecorder = new MediaRecorder(stream);
    recState.mediaRecorder.ondataavailable = (e) => { if (e.data.size > 0) recState.audioChunks.push(e.data); };
    recState.mediaRecorder.onstop = () => onRecordingStop(id, questionText, part);
    recState.mediaRecorder.start();

    // Web Audio API for waveform + pronunciation metrics
    recState.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const source = recState.audioContext.createMediaStreamSource(stream);
    recState.analyser = recState.audioContext.createAnalyser();
    recState.analyser.fftSize = 256;
    source.connect(recState.analyser);

    // Waveform canvas
    const canvas = document.querySelector('[data-rec-canvas="' + id + '"]');
    const waveformContainer = document.querySelector('[data-rec-waveform="' + id + '"]');
    if (canvas && waveformContainer) {
      waveformContainer.style.display = 'block';
      canvas.width = waveformContainer.offsetWidth;
      canvas.height = 40;
      recState.waveformCanvas = canvas;
      recState.waveformCtx = canvas.getContext('2d');
      drawWaveform();
    }

    // Live transcription
    startLiveTranscription(id);

    // Duration timer
    recState.durationTimer = setInterval(() => {
      const elapsed = Math.floor((Date.now() - recState.startTime - recState.pausedDuration) / 1000);
      const min = Math.floor(elapsed / 60);
      const sec = elapsed % 60;
      const durEl = document.querySelector('[data-rec-duration="' + id + '"]');
      if (durEl) durEl.textContent = String(min).padStart(2,'0') + ':' + String(sec).padStart(2,'0');
    }, 200);

    updateRecorderUI(id, 'recording');
    toast('🎙 Recording started — speak now!');
  } catch (err) {
    console.error('Recording error:', err);
    toast('❌ Microphone access denied or unavailable. ' + err.message);
  }
}

function startLiveTranscription(id) {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { console.log('Web Speech API not available'); return; }
  recState.recognition = new SR();
  recState.recognition.continuous = true;
  recState.recognition.interimResults = true;
  recState.recognition.lang = 'en-US';
  recState.recognition.onresult = (event) => {
    let interim = '', final = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const tr = event.results[i][0].transcript;
      if (event.results[i].isFinal) final += tr + ' ';
      else interim += tr;
    }
    if (final) recState.transcriptText += final;
    const full = (recState.transcriptText + interim).trim();
    const el = document.querySelector('[data-rec-transcript="' + id + '"]');
    if (el) { el.textContent = full; el.scrollTop = el.scrollHeight; }
  };
  recState.recognition.onerror = (e) => { if (e.error === 'no-speech' || e.error === 'aborted') return; console.log('SR error:', e.error); };
  recState.recognition.onend = () => {
    if (recState.activeId === id && recState.mediaRecorder && recState.mediaRecorder.state === 'recording') {
      try { recState.recognition.start(); } catch(e) {}
    }
  };
  try { recState.recognition.start(); } catch(e) { console.log('SR start error:', e); }
}

function drawWaveform() {
  if (!recState.analyser || !recState.waveformCtx) return;
  const analyser = recState.analyser;
  const bufLen = analyser.frequencyBinCount;
  const dataArr = new Uint8Array(bufLen);
  const canvas = recState.waveformCanvas;
  const ctx = recState.waveformCtx;
  const w = canvas.width, h = canvas.height;
  const draw = () => {
    recState.animationId = requestAnimationFrame(draw);
    analyser.getByteTimeDomainData(dataArr);
    let sum = 0;
    for (let i = 0; i < bufLen; i++) sum += Math.abs(dataArr[i] - 128);
    recState.volumeSamples.push(sum / bufLen);
    const freqData = new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteFrequencyData(freqData);
    let maxF = 0, maxI = 0;
    for (let i = 0; i < freqData.length; i++) { if (freqData[i] > maxF) { maxF = freqData[i]; maxI = i; } }
    if (maxF > 30) recState.pitchSamples.push(maxI);
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg').trim() || '#F5F7FB';
    ctx.fillRect(0, 0, w, h);
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#2563EB';
    ctx.beginPath();
    const sw = w / bufLen;
    let x = 0;
    for (let i = 0; i < bufLen; i++) {
      const v = dataArr[i] / 128.0;
      const y = (v * h) / 2;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      x += sw;
    }
    ctx.lineTo(w, h/2);
    ctx.stroke();
  };
  draw();
}

function stopRecording(id) {
  if (recState.activeId !== id) return;
  if (recState.mediaRecorder && recState.mediaRecorder.state !== 'inactive') recState.mediaRecorder.stop();
  if (recState.stream) recState.stream.getTracks().forEach(t => t.stop());
  if (recState.recognition) { try { recState.recognition.stop(); } catch(e) {} }
  if (recState.animationId) { cancelAnimationFrame(recState.animationId); recState.animationId = null; }
  if (recState.audioContext) { try { recState.audioContext.close(); } catch(e) {} }
  if (recState.durationTimer) { clearInterval(recState.durationTimer); recState.durationTimer = null; }
  updateRecorderUI(id, 'stopped');
}

async function onRecordingStop(id, questionText, part) {
  const durationSec = Math.floor((Date.now() - recState.startTime - recState.pausedDuration) / 1000);
  const blob = new Blob(recState.audioChunks, { type: 'audio/webm' });
  const audioUrl = URL.createObjectURL(blob);

  const ta = document.querySelector('[data-rec-transcript-area="' + id + '"]');
  if (ta) ta.style.display = 'block';

  const pe = document.querySelector('[data-rec-player="' + id + '"]');
  if (pe) pe.innerHTML = '<audio controls src="' + audioUrl + '" style="width:100%;"></audio>';

  const te = document.querySelector('[data-rec-transcript="' + id + '"]');
  if (te && !te.textContent.trim()) {
    te.textContent = recState.transcriptText || '(No live transcript captured. Submit for AI Evaluation to transcribe from audio.)';
  }

  const wc = (recState.transcriptText || '').split(/\\s+/).filter(w => w).length;
  const wpm = durationSec > 0 ? Math.round((wc / durationSec) * 60) : 0;
  let volMean = 0, volVar = 0;
  if (recState.volumeSamples.length > 0) {
    volMean = recState.volumeSamples.reduce((a,b) => a+b, 0) / recState.volumeSamples.length;
    volVar = Math.sqrt(recState.volumeSamples.reduce((a,b) => a + Math.pow(b - volMean, 2), 0) / recState.volumeSamples.length);
  }
  let pitchMean = 0, pitchRange = 0;
  if (recState.pitchSamples.length > 0) {
    pitchMean = recState.pitchSamples.reduce((a,b) => a+b, 0) / recState.pitchSamples.length;
    pitchRange = Math.max(...recState.pitchSamples) - Math.min(...recState.pitchSamples);
  }

  const audioMetrics = {
    audioDurationSec: durationSec, wordsPerMinute: wpm, wordCount: wc,
    volumeVariation: Math.round(volVar * 100) / 100,
    pitchRange: Math.round(pitchRange), pitchMean: Math.round(pitchMean),
    totalSamples: recState.volumeSamples.length,
  };

  try { await saveAudioToDB(id, blob, audioMetrics); } catch (e) { console.error('Save audio failed:', e); }

  const q = getQ(id);
  q.transcript = recState.transcriptText || '';
  q.audioMetrics = audioMetrics;
  q.hasRecording = true;
  setQ(id, q);

  const se = document.querySelector('[data-rec-status="' + id + '"]');
  if (se) se.textContent = '✓ Recorded (' + durationSec + 's, ' + wc + ' words, ~' + wpm + ' WPM). Transcript saved — edit if needed.';

  recState.activeId = null;

  if (!recState.transcriptText) {
    // Live transcript was empty — try server transcription first, THEN auto-evaluate
    tryServerTranscription(id, blob).then(() => autoEvaluateAnswer(id));
  } else {
    // We have a live transcript — auto-evaluate immediately (small delay so UI updates first)
    setTimeout(() => autoEvaluateAnswer(id), 200);
  }
  toast('✓ Recording saved! Evaluating with Gemini AI...');
}

// ============================================================
// ===== GEMINI AUTO-EVALUATION (per-question) =====
// Called automatically after each Part 1/2/3 recording stops.
// Renders an inline result block inside the question card with:
// overall band, 4 criteria, grammar corrections, vocab improvements,
// fluency feedback, pronunciation feedback, improvement plan.
// Also saves the evaluation to state.evalHistory for the History page.
// Includes a Retry button in case of failure.
// ============================================================
const EVAL_INFLIGHT = new Set(); // question IDs currently being evaluated — prevents duplicate submissions

async function autoEvaluateAnswer(id) {
  // Guard: don't evaluate the same ID twice in parallel
  if (EVAL_INFLIGHT.has(id)) {
    console.log('[AutoEval] Already evaluating ' + id + ', skipping.');
    return;
  }
  const q = getQ(id);
  if (!q.transcript || q.transcript.trim().length < 5) {
    console.log('[AutoEval] Transcript too short for ' + id + ', skipping.');
    return;
  }

  EVAL_INFLIGHT.add(id);

  // Resolve question metadata from Q_INDEX
  const item = Q_INDEX.byId[id] || Q_INDEX.all.find(x => x.id === id);
  const part = item ? item.part : 0;
  const questionText = item ? (item.q || item.title || '') : '';
  const cueCardBullets = (item && item.bullets) ? item.bullets : null;

  // Render the loading state
  renderInlineEvalLoading(id);

  try {
    const payload = {
      transcript: q.transcript,
      audioMetrics: q.audioMetrics || {},
      questionText: questionText,
      questionPart: 'Part ' + part,
    };
    if (cueCardBullets) payload.cueCardBullets = cueCardBullets;

    const resp = await fetch(AI_SERVER_URL + '/api/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(120000), // 2-min timeout
    });
    if (!resp.ok) throw new Error('Server responded with status ' + resp.status);
    const data = await resp.json();

    if (data.success && data.evaluation) {
      // Save evaluation on the question state
      q.evaluation = data.evaluation;
      q.evaluatedAt = data.evaluatedAt || new Date().toISOString();
      q.evalProvider = data.provider || 'unknown';
      setQ(id, q);

      // Append to eval history (dedupe by id — replace older entry if same question re-evaluated)
      if (!state.evalHistory) state.evalHistory = [];
      state.evalHistory = state.evalHistory.filter(e => e.id !== id);
      state.evalHistory.push({
        id: id,
        part: part,
        questionText: questionText,
        transcript: q.transcript,
        audioMetrics: q.audioMetrics || {},
        evaluation: data.evaluation,
        provider: data.provider || 'unknown',
        evaluatedAt: q.evaluatedAt,
      });
      // Cap history to 200 entries to keep localStorage small
      if (state.evalHistory.length > 200) state.evalHistory = state.evalHistory.slice(-200);
      saveState();

      renderInlineEvalResult(id, data.evaluation, data.provider);
      toast('✅ Gemini evaluation complete — Band ' + (data.evaluation.overallBand || '?'));
    } else if (data.rawFeedback) {
      renderInlineEvalError(id, 'Gemini returned unstructured feedback. Please retry.');
    } else {
      throw new Error(data.error || 'Unknown evaluation error');
    }
  } catch (err) {
    console.error('[AutoEval] Failed for ' + id + ':', err);
    renderInlineEvalError(id, err.message || 'Network error');
    toast('⚠ Evaluation failed — tap Retry to try again.');
    // IMPORTANT: we did NOT clear q.transcript or q.audioMetrics — the recording is preserved.
  } finally {
    EVAL_INFLIGHT.delete(id);
  }
}

function renderInlineEvalLoading(id) {
  let el = document.querySelector('[data-eval-result="' + id + '"]');
  if (!el) {
    el = document.createElement('div');
    el.setAttribute('data-eval-result', id);
    el.className = 'q-eval-result eval-loading';
    // Insert after the recorder-block (which is inside the question card)
    const card = document.querySelector('[data-rec-status="' + id + '"]')?.closest('.q-card, .cue-card');
    if (card) card.appendChild(el);
    else {
      // Fallback: append after the transcript area
      const ta = document.querySelector('[data-rec-transcript-area="' + id + '"]');
      if (ta) ta.parentElement.appendChild(el);
    }
  }
  el.className = 'q-eval-result eval-loading';
  el.innerHTML = '' +
    '<div class="q-eval-head">' +
      '<div class="q-eval-band band-mid">···</div>' +
      '<div class="q-eval-title">🤖 Analysing your speaking performance with Gemini AI…</div>' +
      '<div class="eval-loading-anim"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>' +
    '</div>' +
    '<div style="font-size:12.5px;color:var(--text-soft);line-height:1.6;">' +
      'Evaluating fluency, vocabulary, grammar, and pronunciation against the official IELTS Speaking band descriptors. This usually takes 15–30 seconds.' +
    '</div>';
  el.style.display = 'block';
  if (el.scrollIntoView) el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function renderInlineEvalError(id, errMsg) {
  let el = document.querySelector('[data-eval-result="' + id + '"]');
  if (!el) {
    el = document.createElement('div');
    el.setAttribute('data-eval-result', id);
    const card = document.querySelector('[data-rec-status="' + id + '"]')?.closest('.q-card, .cue-card');
    if (card) card.appendChild(el);
  }
  el.className = 'q-eval-result eval-failed';
  el.innerHTML = '' +
    '<div class="q-eval-head">' +
      '<div class="q-eval-band band-fail">!</div>' +
      '<div class="q-eval-title">⚠ Evaluation failed</div>' +
    '</div>' +
    '<div style="font-size:12.5px;color:var(--text-soft);margin-bottom:8px;">' + esc(errMsg) + '</div>' +
    '<div style="font-size:12px;color:var(--text-soft);margin-bottom:8px;">Your recording and transcript are preserved. Tap retry to evaluate again.</div>' +
    '<div class="q-eval-actions">' +
      '<button class="btn sm primary" data-eval-retry="' + id + '">🔄 Retry Evaluation</button>' +
    '</div>';
  el.style.display = 'block';
  const btn = el.querySelector('[data-eval-retry="' + id + '"]');
  if (btn) btn.addEventListener('click', () => autoEvaluateAnswer(id));
}

function renderInlineEvalResult(id, ev, provider) {
  let el = document.querySelector('[data-eval-result="' + id + '"]');
  if (!el) {
    el = document.createElement('div');
    el.setAttribute('data-eval-result', id);
    const card = document.querySelector('[data-rec-status="' + id + '"]')?.closest('.q-card, .cue-card');
    if (card) card.appendChild(el);
  }
  if (!ev) { renderInlineEvalError(id, 'No evaluation data'); return; }

  const band = ev.overallBand;
  const bandClass = band == null ? 'band-fail' : (band >= 7 ? 'band-high' : band >= 5 ? 'band-mid' : 'band-low');
  const reliability = ev.reliability || {};
  const c = ev.criteria || {};
  const fmtBand = (b) => (b == null ? 'N/A' : (typeof b === 'number' ? b.toFixed(1) : String(b)));
  const bandNum = (b) => (typeof b === 'number' ? b : null);
  const critClass = (b) => {
    const n = bandNum(b);
    if (n == null) return 'score-na';
    return n >= 7 ? 'score-high' : n >= 5 ? 'score-mid' : 'score-low';
  };

  let html = '' +
    '<div class="q-eval-head">' +
      '<div class="q-eval-band ' + bandClass + '">' + fmtBand(band) + '</div>' +
      '<div class="q-eval-title">🤖 AI-Estimated IELTS Speaking Band — For Practice Only</div>' +
      '<span class="provider-badge ' + (provider === 'gemini' ? 'gemini' : 'zai') + '">' + esc(provider || 'unknown') + '</span>' +
      '<div class="q-eval-meta">Evaluated ' + new Date(ev.evaluatedAt || Date.now()).toLocaleString() + '</div>' +
    '</div>';

  if (reliability.isReliable === false) {
    html += '<div class="eval-pron-feedback"><h5>⚠ Cannot reliably assess</h5>' +
            '<div style="font-size:12.5px;line-height:1.6;">' + esc(reliability.reasonIfUnreliable || 'The answer was too short, irrelevant, or unintelligible.') + '</div></div>';
  }

  // 4-criteria row
  html += '<div class="q-eval-criteria-row">' +
    renderCritCell('Fluency', c.fluency, fmtBand, critClass) +
    renderCritCell('Lexical', c.lexicalResource, fmtBand, critClass) +
    renderCritCell('Grammar', c.grammar, fmtBand, critClass) +
    renderCritCell('Pronun.', c.pronunciation, fmtBand, critClass) +
    '</div>';

  // Expandable detailed sections
  html += '<div class="q-eval-toggle" data-eval-toggle="' + id + '">▼ Show detailed feedback</div>';
  html += '<div class="q-eval-detail" data-eval-detail="' + id + '">';

  // Overall feedback
  if (ev.overallFeedback) {
    html += '<div style="font-size:13px;line-height:1.6;margin-bottom:10px;padding:8px 10px;background:var(--bg);border-radius:6px;">' + esc(ev.overallFeedback) + '</div>';
  }

  // 4 criteria details
  if (c.fluency) html += renderCriterionDetail('Fluency & Coherence', c.fluency);
  if (c.lexicalResource) html += renderCriterionDetail('Lexical Resource', c.lexicalResource);
  if (c.grammar) html += renderCriterionDetail('Grammatical Range & Accuracy', c.grammar);
  if (c.pronunciation) html += renderCriterionDetail('Pronunciation', c.pronunciation);

  // Fluency feedback
  if (ev.fluencyFeedback) {
    const f = ev.fluencyFeedback;
    html += '<div class="eval-fluency-feedback"><h5>🗣 Fluency Feedback</h5>';
    if (f.repetitions && f.repetitions.length) html += '<div style="font-size:12px;font-weight:600;margin-top:4px;">Repetition:</div><ul>' + f.repetitions.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
    if (f.hesitations && f.hesitations.length) html += '<div style="font-size:12px;font-weight:600;margin-top:4px;">Hesitation:</div><ul>' + f.hesitations.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
    if (f.weakDevelopment && f.weakDevelopment.length) html += '<div style="font-size:12px;font-weight:600;margin-top:4px;">Weak development:</div><ul>' + f.weakDevelopment.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
    if (f.naturalAlternatives && f.naturalAlternatives.length) html += '<div style="font-size:12px;font-weight:600;margin-top:4px;">More natural alternatives:</div><ul>' + f.naturalAlternatives.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
    html += '</div>';
  }

  // Pronunciation feedback
  if (ev.pronunciationFeedback) {
    const pf = ev.pronunciationFeedback;
    html += '<div class="eval-pron-feedback"><h5>🔊 Pronunciation Feedback</h5>';
    if (pf.assessedFromAudio === false) {
      html += '<div class="na-notice">Pronunciation could not be reliably assessed from the transcript alone. Record your answer with a working microphone to get pronunciation feedback.</div>';
    } else {
      if (pf.summary) html += '<div style="font-size:12.5px;line-height:1.6;margin-bottom:6px;">' + esc(pf.summary) + '</div>';
      if (pf.specificAreasForImprovement && pf.specificAreasForImprovement.length) {
        html += '<div style="font-size:12px;font-weight:600;">Specific areas for improvement:</div><ul>' + pf.specificAreasForImprovement.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
      }
    }
    html += '</div>';
  }

  // Grammar corrections
  if (ev.grammarCorrections && ev.grammarCorrections.length) {
    html += '<div class="eval-feedback-section"><h4>📝 Grammar Corrections</h4>';
    ev.grammarCorrections.forEach(gc => {
      html += '<div class="eval-grammar-card">' +
        '<div class="gc-head"><span class="orig">' + esc(gc.original || '') + '</span> → <span class="corr">' + esc(gc.corrected || '') + '</span></div>' +
        '<div class="gc-expl">' + esc(gc.explanation || '') + '</div>' +
        (gc.naturalAlternative ? '<div class="gc-natural">💡 Natural alt: ' + esc(gc.naturalAlternative) + '</div>' : '') +
        '</div>';
    });
    html += '</div>';
  }

  // Vocabulary improvements
  if (ev.vocabularyImprovements && ev.vocabularyImprovements.length) {
    html += '<div class="eval-feedback-section"><h4>📚 Vocabulary Improvements</h4>';
    ev.vocabularyImprovements.forEach(vi => {
      html += '<div class="eval-vocab-card">' +
        '<div class="vc-head"><span class="orig">' + esc(vi.original || '') + '</span> → <span class="corr">' + esc(vi.suggested || '') + '</span></div>' +
        '<div class="vc-reason">' + esc(vi.reason || '') + '</div>' +
        (vi.collocations && vi.collocations.length ? '<div class="vc-collocations">Collocations: ' + vi.collocations.map(c => esc(c)).join(', ') + '</div>' : '') +
        (vi.exampleSentence ? '<div class="vc-example">e.g. ' + esc(vi.exampleSentence) + '</div>' : '') +
        '</div>';
    });
    html += '</div>';
  }

  // Improvement plan
  if (ev.improvementPlan) {
    const ip = ev.improvementPlan;
    html += '<div class="eval-improvement-plan"><h4>🎯 Personalised Improvement Plan</h4>';
    html += '<div class="ip-grid">' +
      '<div class="ip-section weaknesses"><h5>⚠ Top weaknesses</h5><ul>' + (ip.topWeaknesses || []).map(s => '<li>' + esc(s) + '</li>').join('') + '</ul></div>' +
      '<div class="ip-section strengths"><h5>✓ Top strengths</h5><ul>' + (ip.topStrengths || []).map(s => '<li>' + esc(s) + '</li>').join('') + '</ul></div>' +
      '</div>';
    if (ip.exercises && ip.exercises.length) {
      html += '<div style="font-size:12px;font-weight:600;color:var(--purple);margin-bottom:4px;">💡 Practical exercises</div><ul class="ip-exercises">' + ip.exercises.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
    }
    if (ip.nextAnswerTips && ip.nextAnswerTips.length) {
      html += '<div style="font-size:12px;font-weight:600;color:var(--blue);margin-bottom:4px;">📝 Tips for your next answer</div><div class="ip-tips"><ul style="margin:0;padding-left:18px;">' + ip.nextAnswerTips.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul></div>';
    }
    html += '</div>';
  }

  // Disclaimer + actions
  html += '<div style="font-size:11px;color:var(--text-soft);margin-top:10px;font-style:italic;">AI-Estimated IELTS Speaking Band Score — For Practice Only. Not an official IELTS result.</div>';
  html += '<div class="q-eval-actions">' +
    '<button class="btn sm" data-eval-retry="' + id + '">🔄 Re-evaluate</button>' +
    '<button class="btn sm" data-eval-collapse="' + id + '">▲ Collapse</button>' +
    '</div>';
  html += '</div>'; // close q-eval-detail

  el.className = 'q-eval-result';
  el.innerHTML = html;
  el.style.display = 'block';

  // Bind toggle
  const toggle = el.querySelector('[data-eval-toggle="' + id + '"]');
  const detail = el.querySelector('[data-eval-detail="' + id + '"]');
  if (toggle && detail) {
    toggle.addEventListener('click', () => {
      const isOpen = detail.classList.toggle('open');
      toggle.textContent = isOpen ? '▲ Hide detailed feedback' : '▼ Show detailed feedback';
    });
  }
  // Bind retry
  const retryBtn = el.querySelector('[data-eval-retry="' + id + '"]');
  if (retryBtn) retryBtn.addEventListener('click', () => autoEvaluateAnswer(id));
  // Bind collapse
  const collapseBtn = el.querySelector('[data-eval-collapse="' + id + '"]');
  if (collapseBtn && toggle && detail) {
    collapseBtn.addEventListener('click', () => {
      detail.classList.remove('open');
      toggle.textContent = '▼ Show detailed feedback';
      if (el.scrollIntoView) el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
  }
}

function renderCritCell(label, c, fmtBand, critClass) {
  if (!c) return '<div class="q-eval-crit"><div class="crit-label">' + label + '</div><div class="crit-score score-na">N/A</div></div>';
  return '<div class="q-eval-crit"><div class="crit-label">' + label + '</div><div class="crit-score ' + critClass(c.band) + '">' + fmtBand(c.band) + '</div></div>';
}

async function tryServerTranscription(id, blob) {
  const se = document.querySelector('[data-rec-status="' + id + '"]');
  if (se) se.textContent = '🔄 Transcribing from audio (server-side)...';
  try {
    const fd = new FormData();
    fd.append('audio', blob, 'recording.webm');
    const resp = await fetch(AI_SERVER_URL + '/api/transcribe', { method: 'POST', body: fd });
    if (!resp.ok) throw new Error('Server ' + resp.status);
    const data = await resp.json();
    if (data.success && data.transcript) {
      const te = document.querySelector('[data-rec-transcript="' + id + '"]');
      if (te) te.textContent = data.transcript;
      const q = getQ(id); q.transcript = data.transcript; setQ(id, q);
      if (se) se.textContent = '✓ Transcribed by AI (' + data.wordCount + ' words). Edit if needed.';
      return true;
    }
  } catch (err) {
    console.error('Server transcription failed:', err);
    if (se) se.textContent = '⚠ Live transcript only (server unavailable). You can still submit for evaluation.';
  }
  return false;
}

function retakeRecording(id) {
  deleteAudioFromDB(id).catch(() => {});
  const q = getQ(id);
  q.transcript = ''; q.audioMetrics = null; q.hasRecording = false; q.evaluation = null; q.evaluatedAt = null;
  setQ(id, q);
  // Remove inline evaluation block
  const evalEl = document.querySelector('[data-eval-result="' + id + '"]');
  if (evalEl) evalEl.remove();
  const ta = document.querySelector('[data-rec-transcript-area="' + id + '"]');
  if (ta) ta.style.display = 'none';
  const wc = document.querySelector('[data-rec-waveform="' + id + '"]');
  if (wc) wc.style.display = 'none';
  const pe = document.querySelector('[data-rec-player="' + id + '"]');
  if (pe) pe.innerHTML = '';
  const de = document.querySelector('[data-rec-duration="' + id + '"]');
  if (de) de.textContent = '00:00';
  const se = document.querySelector('[data-rec-status="' + id + '"]');
  if (se) se.textContent = '';
  updateRecorderUI(id, 'idle');
  toast('🔄 Ready to record again');
}

function updateRecorderUI(id, mode) {
  const sb = document.querySelector('[data-rec-act="start"][data-rec-id="' + id + '"]');
  const stb = document.querySelector('[data-rec-act="stop"][data-rec-id="' + id + '"]');
  const rb = document.querySelector('[data-rec-act="retake"][data-rec-id="' + id + '"]');
  const ind = document.querySelector('[data-rec-indicator="' + id + '"]');
  if (mode === 'recording') {
    if (sb) { sb.textContent = '⏸ Pause'; sb.classList.add('rec-active'); }
    if (stb) stb.disabled = false;
    if (rb) rb.disabled = true;
    if (ind) ind.style.display = 'inline-flex';
  } else if (mode === 'paused') {
    if (sb) { sb.textContent = '▶ Resume'; sb.classList.remove('rec-active'); }
    if (stb) stb.disabled = false;
    if (ind) ind.style.display = 'none';
  } else if (mode === 'stopped') {
    if (sb) { sb.textContent = '🎙 Record Again'; sb.classList.remove('rec-active'); }
    if (stb) stb.disabled = true;
    if (rb) rb.disabled = false;
    if (ind) ind.style.display = 'none';
  } else {
    if (sb) { sb.textContent = '🎙 Record Answer'; sb.classList.remove('rec-active'); }
    if (stb) stb.disabled = true;
    if (rb) rb.disabled = true;
    if (ind) ind.style.display = 'none';
  }
}

// --- Delegated event binding for recording buttons ---
document.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-rec-act]');
  if (!btn) return;
  const act = btn.dataset.recAct;
  const id = btn.dataset.recId;
  const q = btn.dataset.recQ;
  const part = btn.dataset.recPart || '1';
  if (act === 'start') {
    if (recState.activeId === id && recState.mediaRecorder && recState.mediaRecorder.state === 'recording') {
      recState.mediaRecorder.pause();
      if (recState.recognition) { try { recState.recognition.stop(); } catch(e) {} }
      if (recState.durationTimer) { clearInterval(recState.durationTimer); recState.durationTimer = null; }
      if (recState.animationId) { cancelAnimationFrame(recState.animationId); recState.animationId = null; }
      recState.pausedDuration += Date.now() - recState.startTime - recState.pausedDuration;
      // Actually we need to track pause time properly
      recState._pauseStart = Date.now();
      updateRecorderUI(id, 'paused');
      toast('⏸ Paused');
    } else if (recState.activeId === id && recState.mediaRecorder && recState.mediaRecorder.state === 'paused') {
      recState.mediaRecorder.resume();
      if (recState._pauseStart) { recState.pausedDuration += Date.now() - recState._pauseStart; recState._pauseStart = 0; }
      startLiveTranscription(id);
      recState.durationTimer = setInterval(() => {
        const elapsed = Math.floor((Date.now() - recState.startTime - recState.pausedDuration) / 1000);
        const min = Math.floor(elapsed / 60), sec = elapsed % 60;
        const de = document.querySelector('[data-rec-duration="' + id + '"]');
        if (de) de.textContent = String(min).padStart(2,'0') + ':' + String(sec).padStart(2,'0');
      }, 200);
      drawWaveform();
      updateRecorderUI(id, 'recording');
      toast('▶ Resumed');
    } else {
      startRecording(id, q, part);
    }
  } else if (act === 'stop') {
    stopRecording(id);
  } else if (act === 'retake') {
    retakeRecording(id);
  }
});

// --- Transcript editing (delegated) ---
document.addEventListener('input', (e) => {
  const el = e.target.closest('[data-rec-transcript]');
  if (!el) return;
  const id = el.dataset.recTranscript;
  const q = getQ(id);
  q.transcript = el.textContent;
  setQ(id, q);
});

// --- Restore recordings after render ---
async function restoreRecordingUI(id) {
  try {
    const rec = await getAudioFromDB(id);
    const q = getQ(id);
    if (!rec && !q.transcript) return;
    if (rec) {
      const audioUrl = URL.createObjectURL(rec.blob);
      const pe = document.querySelector('[data-rec-player="' + id + '"]');
      if (pe) pe.innerHTML = '<audio controls src="' + audioUrl + '" style="width:100%;"></audio>';
      const ta = document.querySelector('[data-rec-transcript-area="' + id + '"]');
      if (ta) ta.style.display = 'block';
      const te = document.querySelector('[data-rec-transcript="' + id + '"]');
      if (te && q.transcript) te.textContent = q.transcript;
      const se = document.querySelector('[data-rec-status="' + id + '"]');
      if (se) {
        const m = rec.metrics || {};
        se.textContent = '✓ Recorded (' + (m.audioDurationSec||0) + 's, ' + (m.wordCount||0) + ' words, ~' + (m.wordsPerMinute||0) + ' WPM). Edit transcript if needed.';
      }
      updateRecorderUI(id, 'stopped');
    } else if (q.transcript) {
      const ta = document.querySelector('[data-rec-transcript-area="' + id + '"]');
      if (ta) ta.style.display = 'block';
      const te = document.querySelector('[data-rec-transcript="' + id + '"]');
      if (te) te.textContent = q.transcript;
      updateRecorderUI(id, 'stopped');
    }
  } catch (e) { console.error('Restore recording failed:', e); }
}

// Patch renderPart1Questions to restore recordings after render
const _origRenderP1Q = renderPart1Questions;
renderPart1Questions = function() {
  _origRenderP1Q.apply(this, arguments);
  const tp = DATA.part1.find(t => t.num === p1CurrentTopic);
  if (tp) {
    tp.questions.forEach((_, qi) => {
      const id = 'p1-' + tp.num + '-' + qi;
      if (getQ(id).hasRecording || getQ(id).transcript) restoreRecordingUI(id);
    });
  }
};

// Patch renderPart3Questions to restore recordings after render
const _origRenderP3Q = renderPart3Questions;
renderPart3Questions = function() {
  _origRenderP3Q.apply(this, arguments);
  const c = DATA.part2.find(x => x.num === p3CurrentCue);
  if (c && c.part3) {
    c.part3.forEach((_, qi) => {
      const id = 'p3-' + c.num + '-' + qi;
      if (getQ(id).hasRecording || getQ(id).transcript) restoreRecordingUI(id);
    });
  }
};

// Patch renderPart2Cards to restore recordings after render
const _origRenderP2C = renderPart2Cards;
renderPart2Cards = function() {
  _origRenderP2C.apply(this, arguments);
  // restore recordings for all visible cue cards
  DATA.part2.forEach(c => {
    const id = 'p2-' + c.num;
    if (getQ(id).hasRecording || getQ(id).transcript) restoreRecordingUI(id);
  });
};

// --- AI Evaluation Submission ---
async function submitForEvaluation() {
  const answers = [];
  DATA.part1.forEach(t => {
    t.questions.forEach((item, qi) => {
      const id = 'p1-' + t.num + '-' + qi;
      const q = getQ(id);
      if (q.transcript && q.transcript.trim().length > 5) {
        answers.push({ id, part: 1, questionText: item.q, transcript: q.transcript, audioMetrics: q.audioMetrics || {}, topic: t.name });
      }
    });
  });
  DATA.part2.forEach(c => {
    const id = 'p2-' + c.num;
    const q = getQ(id);
    if (q.transcript && q.transcript.trim().length > 5) {
      answers.push({ id, part: 2, questionText: c.title, transcript: q.transcript, audioMetrics: q.audioMetrics || {}, cueCardBullets: c.bullets || [] });
    }
  });
  DATA.part2.forEach(c => {
    c.part3.forEach((item, qi) => {
      const id = 'p3-' + c.num + '-' + qi;
      const q = getQ(id);
      if (q.transcript && q.transcript.trim().length > 5) {
        answers.push({ id, part: 3, questionText: item.q, transcript: q.transcript, audioMetrics: q.audioMetrics || {}, topic: c.title });
      }
    });
  });
  if (answers.length === 0) { toast('⚠ No recorded answers found. Record some answers first!'); return; }
  const btn = $('#ai-submit-eval');
  if (btn) { btn.disabled = true; btn.textContent = '⏳ Evaluating...'; }
  toast('🤖 Evaluating ' + answers.length + ' answer(s)... This may take a minute.');
  const results = [];
  for (const ans of answers) {
    try {
      const resp = await fetch(AI_SERVER_URL + '/api/evaluate', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript: ans.transcript, audioMetrics: ans.audioMetrics, questionText: ans.questionText, questionPart: 'Part ' + ans.part, cueCardTitle: ans.part === 2 ? ans.questionText : undefined, cueCardBullets: ans.cueCardBullets }),
      });
      if (!resp.ok) throw new Error('Server ' + resp.status);
      const data = await resp.json();
      if (data.success && data.evaluation) {
        const q = getQ(ans.id); q.evaluation = data.evaluation; q.evaluatedAt = data.evaluatedAt; setQ(ans.id, q);
        results.push({ id: ans.id, part: ans.part, questionText: ans.questionText, transcript: ans.transcript, evaluation: data.evaluation, audioMetrics: ans.audioMetrics });
      } else if (data.rawFeedback) {
        results.push({ id: ans.id, part: ans.part, questionText: ans.questionText, transcript: ans.transcript, rawFeedback: data.rawFeedback, audioMetrics: ans.audioMetrics });
      }
    } catch (err) {
      console.error('Eval failed for ' + ans.id + ':', err);
      results.push({ id: ans.id, part: ans.part, questionText: ans.questionText, transcript: ans.transcript, error: err.message, audioMetrics: ans.audioMetrics });
    }
  }
  if (btn) { btn.disabled = false; btn.textContent = '🤖 Submit My Answers for AI Evaluation'; }
  renderEvaluationResults(results);
  toast('✅ Evaluation complete! ' + results.length + ' answer(s) evaluated.');
}

function renderEvaluationResults(results) {
  const container = $('#ai-eval-results');
  if (!container || results.length === 0) return;
  const evaluated = results.filter(r => r.evaluation);
  let overallAvg = 0;
  if (evaluated.length > 0) overallAvg = evaluated.reduce((s, r) => s + (r.evaluation.overallBand || 0), 0) / evaluated.length;
  overallAvg = Math.round(overallAvg * 2) / 2;
  const cAvg = { fluency: 0, lexicalResource: 0, grammar: 0, pronunciation: 0 };
  if (evaluated.length > 0) {
    evaluated.forEach(r => {
      const c = r.evaluation.criteria || {};
      cAvg.fluency += (c.fluency && c.fluency.band) || 0;
      cAvg.lexicalResource += (c.lexicalResource && c.lexicalResource.band) || 0;
      cAvg.grammar += (c.grammar && c.grammar.band) || 0;
      cAvg.pronunciation += (c.pronunciation && c.pronunciation.band) || 0;
    });
    Object.keys(cAvg).forEach(k => cAvg[k] = Math.round((cAvg[k] / evaluated.length) * 2) / 2);
  }
  const bc = (s) => s >= 7 ? 'high' : s >= 5 ? 'mid' : 'low';
  const bcol = (s) => s >= 7 ? '#16A34A' : s >= 5 ? '#2563EB' : '#EA580C';

  container.innerHTML =
    '<div class="eval-overall"><div class="overall-score">' + overallAvg.toFixed(1) + '</div><div class="overall-label">Estimated Overall Speaking Band</div><div style="font-size:11px;opacity:.6;margin-top:6px;">Average across ' + evaluated.length + ' answer(s)</div></div>' +
    '<div class="eval-band-grid">' +
    '<div class="eval-band-card"><div class="criterion-name">Fluency & Coherence</div><div class="eval-band-circle ' + bc(cAvg.fluency) + '">' + cAvg.fluency.toFixed(1) + '</div></div>' +
    '<div class="eval-band-card"><div class="criterion-name">Lexical Resource</div><div class="eval-band-circle ' + bc(cAvg.lexicalResource) + '">' + cAvg.lexicalResource.toFixed(1) + '</div></div>' +
    '<div class="eval-band-card"><div class="criterion-name">Grammar</div><div class="eval-band-circle ' + bc(cAvg.grammar) + '">' + cAvg.grammar.toFixed(1) + '</div></div>' +
    '<div class="eval-band-card"><div class="criterion-name">Pronunciation</div><div class="eval-band-circle ' + bc(cAvg.pronunciation) + '">' + cAvg.pronunciation.toFixed(1) + '</div></div>' +
    '</div>' +
    '<div class="card" style="margin-bottom:16px;"><h4 style="font-size:14px;font-weight:600;color:var(--text);margin-bottom:12px;padding-bottom:6px;border-bottom:2px solid var(--blue);">📊 Performance Chart</h4>' +
    [['Fluency & Coherence', cAvg.fluency], ['Lexical Resource', cAvg.lexicalResource], ['Grammar', cAvg.grammar], ['Pronunciation', cAvg.pronunciation]].map(([n, s]) =>
      '<div class="eval-chart-bar"><span class="label">' + n + '</span><div class="bar-container"><div class="bar-fill" style="width:' + (s/9*100) + '%;background:' + bcol(s) + ';"></div></div><span class="score">' + s.toFixed(1) + '</span></div>'
    ).join('') + '</div>' +
    evaluated.map(r => renderSingleEvalResult(r)).join('') +
    '<div class="eval-disclaimer">⚠️ These are AI-estimated practice scores, not official IELTS results. Actual IELTS scores may vary. The pronunciation score is based on audio analysis metrics (speaking rate, pauses, pitch variation, volume rhythm) combined with transcript analysis. For an official assessment, take a real IELTS test.</div>';
}

function renderSingleEvalResult(r) {
  const ev = r.evaluation;
  if (!ev) return '<div class="eval-question-item"><div class="eq-head"><div class="eq-band" style="background:#DC2626;">!</div><div class="eq-text"><b>Part ' + r.part + ':</b> ' + esc(r.questionText.substring(0, 80)) + '</div></div><div style="font-size:12px;color:#DC2626;">Evaluation failed: ' + esc(r.error || 'Unknown error') + '</div></div>';
  const c = ev.criteria || {};
  const bcol = (s) => s >= 7 ? '#16A34A' : s >= 5 ? '#2563EB' : '#EA580C';
  return '<div class="eval-question-item">' +
    '<div class="eq-head"><div class="eq-band" style="background:' + bcol(ev.overallBand) + ';">' + ev.overallBand.toFixed(1) + '</div><div class="eq-text"><b>Part ' + r.part + ':</b> ' + esc(r.questionText.substring(0, 100)) + (r.questionText.length > 100 ? '...' : '') + '<br><span style="font-size:11px;color:var(--text-soft);">FC: ' + (c.fluency && c.fluency.band ? c.fluency.band.toFixed(1) : '?') + ' • LR: ' + (c.lexicalResource && c.lexicalResource.band ? c.lexicalResource.band.toFixed(1) : '?') + ' • GRA: ' + (c.grammar && c.grammar.band ? c.grammar.band.toFixed(1) : '?') + ' • PR: ' + (c.pronunciation && c.pronunciation.band ? c.pronunciation.band.toFixed(1) : '?') + '</span></div></div>' +
    '<div class="eq-transcript"><b>Your answer:</b> ' + esc(r.transcript.substring(0, 200)) + (r.transcript.length > 200 ? '...' : '') + '</div>' +
    (ev.overallFeedback ? '<div style="font-size:13px;line-height:1.6;margin-top:8px;padding:8px 10px;background:var(--bg);border-radius:6px;">' + esc(ev.overallFeedback) + '</div>' : '') +
    (c.fluency ? renderCriterionDetail('Fluency & Coherence', c.fluency) : '') +
    (c.lexicalResource ? renderCriterionDetail('Lexical Resource', c.lexicalResource) : '') +
    (c.grammar ? renderCriterionDetail('Grammatical Range & Accuracy', c.grammar) : '') +
    (c.pronunciation ? renderCriterionDetail('Pronunciation', c.pronunciation) : '') +
    (ev.grammarCorrections && ev.grammarCorrections.length > 0 ? '<div class="eval-feedback-section"><h4>📝 Grammar Corrections</h4>' + ev.grammarCorrections.map(gc => '<div class="eval-correction"><span class="orig">' + esc(gc.original) + '</span> → <span class="corr">' + esc(gc.corrected) + '</span><div class="expl">' + esc(gc.explanation) + '</div></div>').join('') + '</div>' : '') +
    (ev.vocabularyImprovements && ev.vocabularyImprovements.length > 0 ? '<div class="eval-feedback-section"><h4>📚 Vocabulary Improvements</h4>' + ev.vocabularyImprovements.map(vi => '<div class="eval-correction"><span class="orig">' + esc(vi.original) + '</span> → <span class="corr">' + esc(vi.suggested) + '</span><div class="expl">' + esc(vi.reason) + '</div></div>').join('') + '</div>' : '') +
    '</div>';
}

function renderCriterionDetail(name, detail) {
  if (!detail) return '';
  return '<div class="eval-feedback-section"><h4>' + name + ' — Band ' + (detail.band ? detail.band.toFixed(1) : '?') + '</h4>' +
    '<p style="font-size:13px;line-height:1.6;color:var(--text);margin-bottom:8px;">' + esc(detail.explanation || '') + '</p>' +
    '<div class="eval-strength-weakness"><div class="sw-card strengths"><h5>✓ Strengths</h5><ul>' + (detail.strengths || []).map(s => '<li>' + esc(s) + '</li>').join('') + '</ul></div>' +
    '<div class="sw-card weaknesses"><h5>✗ Weaknesses</h5><ul>' + (detail.weaknesses || []).map(w => '<li>' + esc(w) + '</li>').join('') + '</ul></div></div>' +
    (detail.improvements && detail.improvements.length > 0 ? '<div style="font-size:12px;font-weight:600;color:var(--blue);margin-bottom:4px;">💡 Suggestions:</div><ul style="font-size:13px;line-height:1.6;padding-left:18px;margin:0 0 8px;">' + detail.improvements.map(i => '<li>' + esc(i) + '</li>').join('') + '</ul>' : '') +
    '</div>';
}

function renderAIEvalPage() {
  checkServerStatus();
  const results = [];
  DATA.part1.forEach(t => { t.questions.forEach((item, qi) => { const id = 'p1-' + t.num + '-' + qi; const q = getQ(id); if (q.evaluation) results.push({ id, part: 1, questionText: item.q, transcript: q.transcript, evaluation: q.evaluation, audioMetrics: q.audioMetrics }); }); });
  DATA.part2.forEach(c => { const id = 'p2-' + c.num; const q = getQ(id); if (q.evaluation) results.push({ id, part: 2, questionText: c.title, transcript: q.transcript, evaluation: q.evaluation, audioMetrics: q.audioMetrics }); });
  DATA.part2.forEach(c => { c.part3.forEach((item, qi) => { const id = 'p3-' + c.num + '-' + qi; const q = getQ(id); if (q.evaluation) results.push({ id, part: 3, questionText: item.q, transcript: q.transcript, evaluation: q.evaluation, audioMetrics: q.audioMetrics }); }); });
  if (results.length > 0) { renderEvaluationResults(results); return; }
  let rc = 0;
  Q_INDEX.all.forEach(item => { const q = getQ(item.id); if (q.transcript && q.transcript.trim().length > 5) rc++; });
  $('#ai-eval-results').innerHTML = '<div class="card" style="text-align:center;padding:30px;"><div style="font-size:48px;margin-bottom:10px;">🎙</div><h3 style="font-size:18px;margin-bottom:8px;">No evaluations yet</h3><p style="color:var(--text-soft);font-size:14px;max-width:400px;margin:0 auto 16px;">You have <b>' + rc + '</b> recorded answer(s) ready for evaluation. ' + (rc === 0 ? 'Record some answers first on the Part 1, Part 2, or Part 3 pages.' : 'Click "Submit My Answers for AI Evaluation" above to get started.') + '</p></div>';
}

async function checkServerStatus() {
  const se = $('#ai-server-status'); if (!se) return;
  try {
    const resp = await fetch(AI_SERVER_URL + '/api/health', { signal: AbortSignal.timeout(3000) });
    if (resp.ok) { se.className = 'server-status online'; se.textContent = '● AI Server Online'; }
    else throw new Error('Server ' + resp.status);
  } catch (err) { se.className = 'server-status offline'; se.textContent = '● AI Server Offline (recording works, evaluation needs server)'; }
}

async function clearAllRecordings() {
  if (!confirm('⚠️ This will permanently delete ALL recordings, transcripts, and evaluations. This CANNOT be undone.\\n\\nType OK in the next prompt to confirm.')) return;
  const ans = prompt('Type OK to confirm deletion:'); if (ans !== 'OK') return;
  try { const keys = await getAllAudioKeys(); for (const k of keys) await deleteAudioFromDB(k); } catch (e) {}
  Q_INDEX.all.forEach(item => { const q = getQ(item.id); q.transcript = ''; q.audioMetrics = null; q.hasRecording = false; q.evaluation = null; q.evaluatedAt = null; setQ(item.id, q); });
  toast('🗑 All recordings and evaluations cleared.');
  renderAIEvalPage();
}

$('#ai-submit-eval').addEventListener('click', submitForEvaluation);
$('#ai-clear-eval').addEventListener('click', clearAllRecordings);

// Patch showPage for AI eval page + new Evaluation History page
const _origShowPageAI = showPage;
showPage = function(name) {
  _origShowPageAI.apply(this, arguments);
  if (name === 'ai-eval') renderAIEvalPage();
  if (name === 'eval-history') renderEvalHistoryPage();
  // When the user navigates to Part 1/2/3, re-render any existing inline evaluations
  // (so the user sees their previous AI feedback when they revisit a question)
  if (name === 'part1' || name === 'part2' || name === 'part3') {
    setTimeout(restoreInlineEvals, 300);
  }
};

// ============================================================
// Restore inline evaluation blocks for any question card that has an
// existing evaluation saved in localStorage but no [data-eval-result] element
// rendered yet. Called after page navigation + after question list re-renders.
// ============================================================
function restoreInlineEvals() {
  // Find all visible question-card containers (Part 1 + Part 2 cue cards + Part 3)
  const cards = document.querySelectorAll('.q-card[data-qid], .cue-card');
  cards.forEach(card => {
    const id = card.getAttribute('data-qid') || card.getAttribute('data-cue-id');
    if (!id) return;
    // Skip if an eval block already exists
    if (card.querySelector('[data-eval-result="' + id + '"]')) return;
    const q = getQ(id);
    if (q.evaluation) {
      renderInlineEvalResult(id, q.evaluation, q.evalProvider || 'unknown');
    }
  });
}

// ============================================================
// ===== EVALUATION HISTORY PAGE (per-question Gemini evaluations) =====
// ============================================================
function renderEvalHistoryPage() {
  const container = document.getElementById('eval-history-list');
  if (!container) return;
  const history = (state.evalHistory || []).slice().reverse(); // newest first
  if (history.length === 0) {
    container.innerHTML = '<div class="card" style="text-align:center;padding:30px;color:var(--text-soft);"><div style="font-size:48px;margin-bottom:10px;">📈</div><h3 style="font-size:18px;margin-bottom:8px;color:var(--text);">No evaluations yet</h3><p style="font-size:14px;">Record an answer on any Part 1, Part 2, or Part 3 question. After you stop recording, Gemini AI will automatically evaluate it and the result will appear here.</p></div>';
    return;
  }

  // Build summary stats
  const allBands = history.map(h => h.evaluation?.overallBand).filter(b => typeof b === 'number');
  const avgBand = allBands.length > 0 ? allBands.reduce((a, b) => a + b, 0) / allBands.length : null;
  const bestBand = allBands.length > 0 ? Math.max(...allBands) : null;

  let summaryHtml = '<div class="card" style="margin-bottom:16px;display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px;text-align:center;">';
  summaryHtml += '<div><div style="font-size:11px;color:var(--text-soft);text-transform:uppercase;letter-spacing:.5px;">Total evaluations</div><div style="font-size:24px;font-weight:800;color:var(--blue);">' + history.length + '</div></div>';
  summaryHtml += '<div><div style="font-size:11px;color:var(--text-soft);text-transform:uppercase;letter-spacing:.5px;">Average band</div><div style="font-size:24px;font-weight:800;color:var(--purple);">' + (avgBand ? avgBand.toFixed(1) : '—') + '</div></div>';
  summaryHtml += '<div><div style="font-size:11px;color:var(--text-soft);text-transform:uppercase;letter-spacing:.5px;">Best band</div><div style="font-size:24px;font-weight:800;color:#16A34A;">' + (bestBand ? bestBand.toFixed(1) : '—') + '</div></div>';
  summaryHtml += '</div>';
  container.innerHTML = summaryHtml + history.map((h, idx) => renderEvalHistoryItem(h, idx)).join('');

  // Bind View / Delete buttons
  container.querySelectorAll('[data-ehi-view]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = btn.getAttribute('data-ehi-view');
      viewEvalHistoryItem(id);
    });
  });
  container.querySelectorAll('[data-ehi-del]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = btn.getAttribute('data-ehi-del');
      deleteEvalHistoryItem(id);
    });
  });
  // Click on item row → open question
  container.querySelectorAll('.eval-history-item').forEach(item => {
    item.addEventListener('click', () => {
      const id = item.getAttribute('data-eval-id');
      if (id) openQuestionById(id);
    });
  });
}

function renderEvalHistoryItem(h, idx) {
  const ev = h.evaluation || {};
  const band = ev.overallBand;
  const bandClass = band == null ? '' : (band >= 7 ? 'band-high' : band >= 5 ? 'band-mid' : 'band-low');
  const bandStr = (typeof band === 'number') ? band.toFixed(1) : '?';
  const partLabel = h.part ? 'Part ' + h.part : '';
  const dateStr = h.evaluatedAt ? new Date(h.evaluatedAt).toLocaleString() : '';
  const c = ev.criteria || {};
  const fmtBand = (b) => (typeof b === 'number') ? b.toFixed(1) : '?';
  return '' +
    '<div class="eval-history-item" data-eval-id="' + esc(h.id) + '">' +
      '<div class="ehi-band ' + bandClass + '">' + bandStr + '</div>' +
      '<div class="ehi-info">' +
        '<div class="ehi-q">' + esc(partLabel ? partLabel + ': ' : '') + esc((h.questionText || '').slice(0, 90)) + (h.questionText && h.questionText.length > 90 ? '…' : '') + '</div>' +
        '<div class="ehi-meta">' +
          '<span class="provider-badge ' + (h.provider === 'gemini' ? 'gemini' : 'zai') + '">' + esc(h.provider || 'unknown') + '</span>' +
          (dateStr ? '<span>📅 ' + esc(dateStr) + '</span>' : '') +
          '<span>FC ' + fmtBand(c.fluency?.band) + ' • LR ' + fmtBand(c.lexicalResource?.band) + ' • GRA ' + fmtBand(c.grammar?.band) + ' • PR ' + fmtBand(c.pronunciation?.band) + '</span>' +
        '</div>' +
      '</div>' +
      '<div class="ehi-actions">' +
        '<button class="ehi-view" data-ehi-view="' + esc(h.id) + '" title="View full evaluation">👁 View</button>' +
        '<button class="ehi-del" data-ehi-del="' + esc(h.id) + '" title="Delete this evaluation">🗑</button>' +
      '</div>' +
    '</div>';
}

function viewEvalHistoryItem(id) {
  // Open the question and scroll to the inline eval result
  openQuestionById(id);
  // After the question card renders, scroll the eval-result into view
  setTimeout(() => {
    const el = document.querySelector('[data-eval-result="' + id + '"]');
    if (el) {
      // Open the detail if collapsed
      const detail = el.querySelector('[data-eval-detail="' + id + '"]');
      const toggle = el.querySelector('[data-eval-toggle="' + id + '"]');
      if (detail && !detail.classList.contains('open') && toggle) toggle.click();
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, 400);
}

function deleteEvalHistoryItem(id) {
  if (!confirm('Delete this evaluation? The recording will be preserved but the AI feedback will be removed.')) return;
  if (state.evalHistory) {
    state.evalHistory = state.evalHistory.filter(e => e.id !== id);
    saveState();
  }
  // Also clear the evaluation on the question state
  const q = getQ(id);
  q.evaluation = null; q.evaluatedAt = null;
  setQ(id, q);
  // Remove inline eval block if visible
  const el = document.querySelector('[data-eval-result="' + id + '"]');
  if (el) el.remove();
  renderEvalHistoryPage();
  toast('🗑 Evaluation deleted.');
}

function clearAllEvalHistory() {
  if (!confirm('⚠️ This will permanently delete ALL evaluation history (the AI feedback for every question). Your audio recordings will be preserved. This CANNOT be undone.\\n\\nType OK in the next prompt to confirm.')) return;
  const ans = prompt('Type OK to confirm deletion of all evaluations:');
  if (ans !== 'OK') return;
  state.evalHistory = [];
  // Clear evaluation field on every question
  Q_INDEX.all.forEach(item => {
    const q = getQ(item.id);
    if (q.evaluation) { q.evaluation = null; q.evaluatedAt = null; setQ(item.id, q); }
  });
  saveState();
  renderEvalHistoryPage();
  toast('🗑 All evaluation history cleared.');
}

function bindEvalHistoryButtons() {
  const clearBtn = document.getElementById('clear-eval-history');
  if (clearBtn && !clearBtn.__bound) {
    clearBtn.__bound = true;
    clearBtn.addEventListener('click', clearAllEvalHistory);
  }
  const refreshBtn = document.getElementById('refresh-eval-history');
  if (refreshBtn && !refreshBtn.__bound) {
    refreshBtn.__bound = true;
    refreshBtn.addEventListener('click', () => { renderEvalHistoryPage(); toast('🔄 Refreshed.'); });
  }
}
bindEvalHistoryButtons();
document.addEventListener('DOMContentLoaded', bindEvalHistoryButtons);

window.renderEvalHistoryPage = renderEvalHistoryPage;

// Initialize IndexedDB
initAudioDB().then(() => { console.log('✅ Audio IndexedDB initialized'); }).catch(err => { console.error('IndexedDB init failed:', err); });

// ============================================================
// ===== TTS EXAMINER VOICE SYSTEM =====
// ============================================================

const TTS = {
  voices: [],
  selectedVoice: null,
  enabled: true,
  speed: 1.0,
  speaking: false,
};

function initTTS() {
  if (!('speechSynthesis' in window)) { console.log('TTS not available'); return; }
  function loadVoices() {
    TTS.voices = speechSynthesis.getVoices().filter(v => v.lang.startsWith('en'));
    const sel = document.getElementById('setting-tts-voice');
    if (sel) {
      const current = sel.value;
      sel.innerHTML = '<option value="">Default English voice</option>';
      TTS.voices.forEach((v, i) => {
        const label = v.name + ' (' + v.lang + ')';
        sel.innerHTML += '<option value="' + i + '">' + label + '</option>';
      });
      if (current) sel.value = current;
    }
    // Load saved settings
    const saved = (state.settings && state.settings.tts) || {};
    TTS.enabled = saved.enabled !== false;
    TTS.speed = saved.speed || 1.0;
    if (saved.voiceIdx != null && TTS.voices[saved.voiceIdx]) TTS.selectedVoice = TTS.voices[saved.voiceIdx];
    const enSel = document.getElementById('setting-tts-enabled');
    const spSel = document.getElementById('setting-tts-speed');
    const vSel = document.getElementById('setting-tts-voice');
    if (enSel) enSel.value = String(TTS.enabled);
    if (spSel) spSel.value = String(TTS.speed);
    if (vSel && saved.voiceIdx != null) vSel.value = String(saved.voiceIdx);
  }
  loadVoices();
  if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = loadVoices;
  }
}

function speak(text, opts) {
  if (!TTS.enabled || !('speechSynthesis' in window) || !text) {
    // Use setTimeout to ensure DOM is ready before callback fires
    if (opts && opts.onend) setTimeout(() => opts.onend(), 100);
    return;
  }
  // Mark any previously active utterance as cancelled so its onend doesn't fire
  if (TTS._currentUtterance) TTS._currentUtterance._cancelled = true;
  // Cancel any ongoing speech
  speechSynthesis.cancel();
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = 'en-GB';
  utter.rate = TTS.speed || 1.0;
  if (TTS.selectedVoice) utter.voice = TTS.selectedVoice;
  else {
    const brit = TTS.voices.find(v => v.lang === 'en-GB');
    if (brit) utter.voice = brit;
  }
  TTS.speaking = true;
  TTS._currentUtterance = utter;
  const ind = document.getElementById('tts-indicator');
  if (ind) ind.style.display = 'flex';
  // Guard: opts.onend should fire AT MOST ONCE per speak() call.
  // Some browsers fire both onend AND onerror for the same utterance under
  // certain failure conditions (e.g., interrupt-induced cancellation). Without
  // this guard, downstream transitions could fire twice.
  let callbackFired = false;
  const fireCallbackSafely = () => {
    if (callbackFired) return;
    callbackFired = true;
    if (!utter._cancelled && opts && opts.onend) opts.onend();
  };
  utter.onend = function() {
    TTS.speaking = false;
    if (ind) ind.style.display = 'none';
    fireCallbackSafely();
  };
  utter.onerror = function() {
    TTS.speaking = false;
    if (ind) ind.style.display = 'none';
    console.error('[TTS] utterance onerror fired; text was:', (text || '').slice(0, 80) + '...');
    fireCallbackSafely();
  };
  speechSynthesis.speak(utter);
}

function stopSpeaking() {
  if ('speechSynthesis' in window) {
    speechSynthesis.cancel();
    TTS.speaking = false;
    const ind = document.getElementById('tts-indicator');
    if (ind) ind.style.display = 'none';
  }
}

// TTS settings change handlers
document.addEventListener('change', (e) => {
  if (e.target.id === 'setting-tts-enabled') {
    TTS.enabled = e.target.value === 'true';
    state.settings = state.settings || {};
    state.settings.tts = state.settings.tts || {};
    state.settings.tts.enabled = TTS.enabled;
    saveState();
  } else if (e.target.id === 'setting-tts-speed') {
    TTS.speed = parseFloat(e.target.value);
    state.settings = state.settings || {};
    state.settings.tts = state.settings.tts || {};
    state.settings.tts.speed = TTS.speed;
    saveState();
  } else if (e.target.id === 'setting-tts-voice') {
    const idx = parseInt(e.target.value);
    TTS.selectedVoice = isNaN(idx) ? null : TTS.voices[idx];
    state.settings = state.settings || {};
    state.settings.tts = state.settings.tts || {};
    state.settings.tts.voiceIdx = isNaN(idx) ? null : idx;
    saveState();
  }
});

// Test TTS button
document.addEventListener('click', (e) => {
  if (e.target.id === 'test-tts') {
    speak('Good morning. Welcome to the TAREQ IELTS Speaking Mock Examination. I will be your examiner today.');
  }
});

// ============================================================
// ===== EXAMINER IDENTITY SYSTEM =====
// ============================================================

const EXAMINER_NAMES = [
  'James Anderson', 'Margaret Thompson', 'David Clarke', 'Susan Wright',
  'Robert Hughes', 'Patricia Morgan', 'Michael Foster', 'Elizabeth Bennett',
  'Christopher Davies', 'Jennifer Scott', 'Richard Turner', 'Catherine Hall',
  'Andrew Mitchell', 'Sarah Evans', 'Thomas Baker', 'Rachel Cooper',
  'Nicholas Reed', 'Victoria Price', 'Oliver Brooks', 'Helen Russell',
];

function generateExaminerIdentity() {
  const name = EXAMINER_NAMES[Math.floor(Math.random() * EXAMINER_NAMES.length)];
  const id = 'EX-' + Math.floor(10000 + Math.random() * 90000);
  const sessionId = 'TAREQ-' + Date.now().toString(36).toUpperCase().slice(-8);
  return { name, id, sessionId };
}

// ============================================================
// ===== UPGRADED FULL SPEAKING MOCK TEST SYSTEM =====
// ============================================================

const mockTest = {
  active: false,
  testId: null,
  date: null,
  phase: 'welcome',
  questions: { p1: [], p2: null, p3: [] },
  answers: [],
  currentIdx: 0,
  timer: null,
  timerSeconds: 0,
  timerDuration: 0,
  timerPhase: '',
  recordingId: null,
  evaluation: null,
  examiner: null,
  candidateName: '',
  autoMode: true,
  submitting: false,
  // ----- Bug-fix guards (added) -----
  // introPlayed: ensures the examiner introduction is spoken exactly ONCE per
  // session. Reset to false only by startMockTest() (a genuinely new session).
  // renderMockInstructions checks this flag before calling speak(introText).
  introPlayed: false,
  // transitionToken: a per-phase-transition guard. Captured by speak()'s caller
  // at the moment of dispatching, and verified again inside the onend callback.
  // Prevents duplicate onend firings (Chrome bug) from causing double phase
  // transitions.
  transitionToken: 0,
  // introFallbackTimer: timeout-based safety net. If speechSynthesis swallows
  // the onend event for a long utterance (a known Chrome bug), this timer
  // advances the test automatically so the user is never left stuck.
  introFallbackTimer: null,
  // qFallbackTimer: same idea as introFallbackTimer, but for individual
  // questions spoken during Part 1, Part 2 prep, Part 2 speak, and Part 3.
  qFallbackTimer: null,
};

function getMockSettings() {
  return {
    p1Time: +(document.getElementById('setting-mock-p1')?.value || 30),
    p2Prep: +(document.getElementById('setting-mock-p2-prep')?.value || 60),
    p2Speak: +(document.getElementById('setting-mock-p2-speak')?.value || 120),
    p3Time: +(document.getElementById('setting-mock-p3')?.value || 45),
  };
}

function loadMockSettings() {
  const mt = (state.settings && state.settings.mockTimers) || {};
  if (mt.p1Time && document.getElementById('setting-mock-p1')) document.getElementById('setting-mock-p1').value = mt.p1Time;
  if (mt.p2Prep && document.getElementById('setting-mock-p2-prep')) document.getElementById('setting-mock-p2-prep').value = mt.p2Prep;
  if (mt.p2Speak && document.getElementById('setting-mock-p2-speak')) document.getElementById('setting-mock-p2-speak').value = mt.p2Speak;
  if (mt.p3Time && document.getElementById('setting-mock-p3')) document.getElementById('setting-mock-p3').value = mt.p3Time;
}

// Load current API URL into the Settings input
function loadApiUrlSetting() {
  const input = document.getElementById('setting-api-url');
  if (!input) return;
  try {
    const saved = localStorage.getItem('tareq_api_url');
    input.value = saved || '';
  } catch(e) {}
}

// Bind the Save & Reset buttons for the API URL
function bindApiUrlButtons() {
  const saveBtn = document.getElementById('save-api-url');
  const resetBtn = document.getElementById('reset-api-url');
  const statusEl = document.getElementById('api-url-status');
  if (saveBtn && !saveBtn.__bound) {
    saveBtn.__bound = true;
    saveBtn.addEventListener('click', async () => {
      const input = document.getElementById('setting-api-url');
      if (!input) return;
      const url = (input.value || '').trim().replace(/\/+$/, '');
      if (!url) {
        if (statusEl) statusEl.innerHTML = '<span style="color:#DC2626;">⚠ Please enter a URL.</span>';
        return;
      }
      // Basic URL validation
      try { new URL(url); } catch(e) {
        if (statusEl) statusEl.innerHTML = '<span style="color:#DC2626;">⚠ Invalid URL. Must start with http:// or https://</span>';
        return;
      }
      setApiServerUrl(url);
      if (statusEl) statusEl.innerHTML = '<span style="color:var(--text-soft);">⏳ Testing connection...</span>';
      // Test the connection by calling /api/health
      try {
        const resp = await fetch(url + '/api/health', { signal: AbortSignal.timeout(8000) });
        if (!resp.ok) throw new Error('HTTP ' + resp.status);
        const data = await resp.json();
        if (data.status === 'ok') {
          if (statusEl) statusEl.innerHTML = '<span style="color:#16A34A;font-weight:600;">✓ Connected — provider: ' + esc(data.provider || 'unknown') + (data.geminiAvailable ? ' (Gemini)' : '') + '</span><br><span style="font-size:11px;color:var(--text-soft);">The website will use this backend for all AI evaluations. Reload the page to apply.</span>';
          toast('✓ API URL saved — backend connected!');
        } else {
          throw new Error('Bad response');
        }
      } catch (err) {
        if (statusEl) statusEl.innerHTML = '<span style="color:#DC2626;">✗ Saved, but could not reach backend: ' + esc(err.message) + '</span><br><span style="font-size:11px;color:var(--text-soft);">The URL was saved. Check that the backend is running and CORS is enabled.</span>';
        toast('⚠ Saved but backend unreachable');
      }
    });
  }
  if (resetBtn && !resetBtn.__bound) {
    resetBtn.__bound = true;
    resetBtn.addEventListener('click', () => {
      try { localStorage.removeItem('tareq_api_url'); } catch(e) {}
      AI_SERVER_URL = 'http://localhost:3001';
      const input = document.getElementById('setting-api-url');
      if (input) input.value = '';
      const statusEl = document.getElementById('api-url-status');
      if (statusEl) statusEl.innerHTML = '<span style="color:var(--text-soft);">↺ Reset to localhost:3001. Reload the page to apply.</span>';
      toast('↺ Reset to localhost');
    });
  }
}
bindApiUrlButtons();
document.addEventListener('DOMContentLoaded', () => { loadApiUrlSetting(); bindApiUrlButtons(); });

// Patch showPage to also load the API URL setting when Settings opens
const _origShowPageSettings = showPage;
showPage = function(name) {
  _origShowPageSettings.apply(this, arguments);
  if (name === 'settings') {
    setTimeout(() => { loadApiUrlSetting(); bindApiUrlButtons(); }, 100);
  }
};

document.addEventListener('change', (e) => {
  if (e.target.id && e.target.id.startsWith('setting-mock-')) {
    state.settings = state.settings || {};
    state.settings.mockTimers = getMockSettings();
    saveState();
  }
});

function generateMockTest() {
  const test = { p1: [], p2: null, p3: [] };
  const p1Pool = Q_INDEX.p1.slice();
  for (let i = p1Pool.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [p1Pool[i], p1Pool[j]] = [p1Pool[j], p1Pool[i]]; }
  const usedTopics = new Set();
  for (const q of p1Pool) {
    if (!usedTopics.has(q.topicNum) && test.p1.length < 5) { test.p1.push(q); usedTopics.add(q.topicNum); }
    if (test.p1.length >= 5) break;
  }
  if (test.p1.length < 4) { for (const q of p1Pool) { if (test.p1.length >= 5) break; if (!test.p1.find(x => x.id === q.id)) test.p1.push(q); } }
  const p2Pool = Q_INDEX.p2.slice();
  test.p2 = p2Pool[Math.floor(Math.random() * p2Pool.length)];
  if (test.p2 && test.p2.part3 && test.p2.part3.length > 0) {
    const p3Pool = test.p2.part3.slice();
    for (let i = p3Pool.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [p3Pool[i], p3Pool[j]] = [p3Pool[j], p3Pool[i]]; }
    test.p3 = p3Pool.slice(0, Math.min(4, p3Pool.length));
  }
  if (test.p3.length === 0) {
    const altP3 = Q_INDEX.p3.slice();
    for (let i = altP3.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [altP3[i], altP3[j]] = [altP3[j], altP3[i]]; }
    test.p3 = altP3.slice(0, 4);
  }
  return test;
}

function startMockTest() {
  // Defensive: if a previous session's fallback timer is somehow still pending,
  // clear it before starting a new session.
  if (mockTest.introFallbackTimer) { clearTimeout(mockTest.introFallbackTimer); mockTest.introFallbackTimer = null; }
  if (mockTest.qFallbackTimer) { clearTimeout(mockTest.qFallbackTimer); mockTest.qFallbackTimer = null; }
  if (mockTest.timer) { clearInterval(mockTest.timer); mockTest.timer = null; }
  stopSpeaking();

  mockTest.active = true;
  mockTest.testId = 'mock-' + Date.now();
  mockTest.date = new Date().toISOString();
  mockTest.phase = 'welcome';
  mockTest.questions = generateMockTest();
  mockTest.answers = [];
  mockTest.currentIdx = 0;
  mockTest.evaluation = null;
  mockTest.examiner = generateExaminerIdentity();
  mockTest.candidateName = '';
  mockTest.submitting = false;
  // Reset the one-time-introduction guard for the new session.
  // This is the ONLY place introPlayed is reset, so the introduction can play
  // exactly once per genuinely new session.
  mockTest.introPlayed = false;
  // Bump the transition token so any in-flight callbacks from the previous
  // session become no-ops.
  mockTest.transitionToken++;
  renderMockTestPhase();
  document.getElementById('mock-overlay').classList.add('open');
}

function closeMockTest() {
  if (mockTest.recordingId) stopRecording(mockTest.recordingId);
  if (mockTest.timer) { clearInterval(mockTest.timer); mockTest.timer = null; }
  if (mockTest.introFallbackTimer) { clearTimeout(mockTest.introFallbackTimer); mockTest.introFallbackTimer = null; }
  if (mockTest.qFallbackTimer) { clearTimeout(mockTest.qFallbackTimer); mockTest.qFallbackTimer = null; }
  stopSpeaking();
  // Invalidate any in-flight callbacks so they cannot re-enter the state machine
  // after the session has been torn down.
  mockTest.transitionToken++;
  mockTest.active = false;
  document.getElementById('mock-overlay').classList.remove('open');
}

function startMockTimer(seconds, phase, onComplete) {
  if (mockTest.timer) { clearInterval(mockTest.timer); mockTest.timer = null; }
  mockTest.timerSeconds = seconds;
  mockTest.timerDuration = seconds;
  mockTest.timerPhase = phase;
  updateMockTimerDisplay();
  mockTest.timer = setInterval(() => {
    mockTest.timerSeconds--;
    updateMockTimerDisplay();
    if (mockTest.timerSeconds <= 0) {
      clearInterval(mockTest.timer);
      mockTest.timer = null;
      if (onComplete) onComplete();
    }
  }, 1000);
}

function updateMockTimerDisplay() {
  const display = document.getElementById('mock-timer-display');
  if (!display) return;
  const min = Math.floor(mockTest.timerSeconds / 60);
  const sec = mockTest.timerSeconds % 60;
  display.textContent = String(min).padStart(2, '0') + ':' + String(sec).padStart(2, '0');
  display.classList.remove('warning', 'danger');
  if (mockTest.timerSeconds <= 10) display.classList.add('danger');
  else if (mockTest.timerSeconds <= 30) display.classList.add('warning');
  const bar = document.getElementById('mock-progress-fill');
  if (bar && mockTest.timerDuration > 0) {
    const pct = ((mockTest.timerDuration - mockTest.timerSeconds) / mockTest.timerDuration) * 100;
    bar.style.width = Math.min(100, pct) + '%';
  }
}

function saveMockAnswer(id, part, questionText, transcript, audioMetrics, cueCardBullets) {
  mockTest.answers.push({ id, part, questionText, transcript, audioMetrics: audioMetrics || {}, cueCardBullets: cueCardBullets || null });
}

function renderMockTestPhase() {
  const modal = document.getElementById('mock-modal');
  if (!modal) return;
  const settings = getMockSettings();
  switch (mockTest.phase) {
    case 'welcome': renderMockWelcome(modal); break;
    case 'instructions': renderMockInstructions(modal); break;
    case 'part1': renderMockPart1(modal, settings); break;
    case 'part2-prep': renderMockPart2Prep(modal, settings); break;
    case 'part2-speak': renderMockPart2Speak(modal, settings); break;
    case 'part3': renderMockPart3(modal, settings); break;
    case 'completion': renderMockCompletion(modal); break;
    case 'results': renderMockResults(modal); break;
  }
}

// TTS indicator HTML (shown when examiner is speaking)
function ttsIndicatorHTML() {
  return '<div id="tts-indicator" style="display:none;text-align:center;padding:8px;margin-bottom:10px;background:var(--blue-light);border-radius:6px;font-size:13px;color:var(--blue-dark);"><span style="display:inline-block;width:8px;height:8px;background:var(--blue);border-radius:50%;animation:blink 1s infinite;margin-right:6px;"></span>🔊 Examiner is speaking...</div>';
}

function renderMockWelcome(modal) {
  const ex = mockTest.examiner;
  modal.innerHTML = `
    <div class="mock-welcome">
      <div class="icon-big">📝</div>
      <h2>TAREQ IELTS Speaking Mock Examination</h2>
      <p>Welcome to your IELTS-style Speaking Practice Test. Please review your examination details below.</p>
    </div>
    <div class="card" style="margin-bottom:16px;">
      <h3 style="font-size:15px;margin-bottom:12px;">Examination Details</h3>
      <div style="font-size:13px;color:var(--text-soft);line-height:2;">
        <b>Examiner:</b> ${esc(ex.name)}<br>
        <b>Examiner ID:</b> ${esc(ex.id)}<br>
        <b>Session ID:</b> ${esc(ex.sessionId)}<br>
        <b>Date:</b> ${new Date(mockTest.date).toLocaleString()}<br><br>
        <label style="font-weight:600;color:var(--text);">Your Name (optional):</label><br>
        <input type="text" class="input" id="candidate-name" placeholder="Enter your name (optional)" style="margin-top:4px;max-width:300px;">
      </div>
    </div>
    <div class="card" style="margin-bottom:16px;">
      <h3 style="font-size:15px;margin-bottom:8px;">Test Structure</h3>
      <div style="font-size:13px;color:var(--text-soft);line-height:1.8;">
        <b>Part 1:</b> ${mockTest.questions.p1.length} questions (${getMockSettings().p1Time}s each)<br>
        <b>Part 2:</b> 1 cue card (${getMockSettings().p2Prep}s prep + ${getMockSettings().p2Speak}s speak)<br>
        <b>Part 3:</b> ${mockTest.questions.p3.length} discussion questions (${getMockSettings().p3Time}s each)
      </div>
    </div>
    <div class="card" style="margin-bottom:16px;background:var(--blue-light);border:none;">
      <div style="font-size:13px;line-height:1.7;color:var(--blue-dark);">
        <b>📋 How this test works:</b><br>
        • The examiner will speak each question aloud automatically<br>
        • Recording starts automatically after each question is read<br>
        • Timers count down and auto-stop your recording<br>
        • The test flows continuously — no need to press buttons between questions<br>
        • After completion, your answers are automatically submitted for AI evaluation
      </div>
    </div>
    ${ttsIndicatorHTML()}
    <div class="btn-row" style="justify-content:center;">
      <button class="btn primary" id="mock-begin">▶ Start Full Speaking Test</button>
      <button class="btn" id="mock-cancel">Cancel</button>
    </div>
    <div id="mock-emergency-stop" style="display:none;text-align:center;margin-top:10px;">
      <button class="btn danger sm" id="mock-emergency">⏹ Emergency Stop</button>
    </div>
  `;
  document.getElementById('mock-begin').addEventListener('click', () => {
    mockTest.candidateName = document.getElementById('candidate-name')?.value?.trim() || '';
    mockTest.phase = 'instructions';
    renderMockTestPhase();
  });
  document.getElementById('mock-cancel').addEventListener('click', closeMockTest);
}

function renderMockInstructions(modal) {
  const settings = getMockSettings();
  const ex = mockTest.examiner;
  const candidateRef = mockTest.candidateName ? ', ' + mockTest.candidateName : '';
  const introText = `Good morning. My name is ${ex.name}, and I will be your speaking examiner today. Welcome to the TAREQ IELTS Speaking Mock Examination. This is a simulated IELTS Speaking test designed to help you practise under realistic examination conditions. My examiner identification number is ${ex.id}. Before we begin, in Part One, I will ask you some general questions about yourself and familiar topics. In Part Two, you will receive a topic card and have one minute to prepare. You will then speak for up to two minutes. In Part Three, we will discuss some more general questions related to the topic. Please answer naturally and speak as clearly as possible. Let us begin Part One.`;

  modal.innerHTML = `
    <div class="mock-welcome">
      <div class="icon-big">🎤</div>
      <h2>Examination in Progress</h2>
      <p>The examiner is introducing the test. Please listen carefully.</p>
    </div>
    <div class="card" style="margin-bottom:16px;">
      <div style="display:flex;gap:12px;align-items:center;margin-bottom:10px;">
        <div style="width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,var(--blue),#60A5FA);display:grid;place-items:center;font-size:20px;color:#fff;font-weight:700;">${esc(ex.name.charAt(0))}</div>
        <div>
          <div style="font-size:14px;font-weight:600;">${esc(ex.name)}</div>
          <div style="font-size:12px;color:var(--text-soft);">Examiner ID: ${esc(ex.id)} • Session: ${esc(ex.sessionId)}</div>
        </div>
      </div>
    </div>
    ${ttsIndicatorHTML()}
    <div style="text-align:center;font-size:13px;color:var(--text-soft);margin:16px 0;">
      ${TTS.enabled ? '🔊 The examiner will now introduce the examination...' : '🔇 Examiner voice is disabled. Click Begin to start silently.'}
    </div>
    <div class="btn-row" style="justify-content:center;">
      ${TTS.enabled ? '<button class="btn" id="mock-skip-intro">Skip Introduction →</button>' : '<button class="btn primary" id="mock-skip-intro">▶ Begin Part 1</button>'}
    </div>
    <div style="text-align:center;margin-top:10px;">
      <button class="btn danger sm" id="mock-emergency">⏹ Emergency Stop</button>
    </div>
  `;

  // Bind emergency stop
  document.getElementById('mock-emergency').addEventListener('click', () => {
    if (confirm('Stop the test? Your progress will be saved.')) {
      stopSpeaking();
      closeMockTest();
    }
  });

  // ---- Bug fix: one-time introduction guard ----
  // If the intro has already been spoken for this session (e.g., because the
  // user navigated back to the instructions phase somehow, or because a
  // duplicate listener/call tried to re-render this phase), do NOT speak it
  // again. Skip straight to the Part 1 transition.
  if (mockTest.introPlayed) {
    console.warn('[MockTest] renderMockInstructions called but intro already played for this session — skipping re-introduction and advancing to Part 1.');
    mockTest.phase = 'part1';
    mockTest.currentIdx = 0;
    // Defer the render to avoid re-entrancy in the same synchronous tick.
    setTimeout(() => renderMockTestPhase(), 0);
    return;
  }
  mockTest.introPlayed = true;

  // ---- Bug fix: transition-token guard ----
  // Capture the token at the moment we dispatch speak(). Inside onend (and
  // inside the fallback timer), we verify the token is still current before
  // transitioning. If a new session started (bumping the token), or closeMockTest
  // was called (also bumping the token), the callback becomes a no-op.
  const myToken = mockTest.transitionToken;

  // Shared transition function — callable from either the onend callback OR
  // the fallback timer. Idempotent: once transitioned, subsequent calls are no-ops.
  let transitioned = false;
  function transitionToPart1(reason) {
    if (transitioned) return;
    if (myToken !== mockTest.transitionToken) {
      console.warn('[MockTest] transitionToPart1 ignored — token stale (session was reset or closed).');
      return;
    }
    if (mockTest.phase !== 'instructions') {
      console.warn('[MockTest] transitionToPart1 ignored — phase already advanced to:', mockTest.phase);
      return;
    }
    transitioned = true;
    // Clear the fallback timer — we don't need it any more.
    if (mockTest.introFallbackTimer) { clearTimeout(mockTest.introFallbackTimer); mockTest.introFallbackTimer = null; }
    console.log('[MockTest] Intro finished (' + reason + '). Transitioning to Part 1.');
    mockTest.phase = 'part1';
    mockTest.currentIdx = 0;
    renderMockTestPhase();
  }

  // Bind Skip Introduction button (only meaningful while intro is playing).
  // Skipping also clears the fallback timer and advances immediately.
  document.getElementById('mock-skip-intro').addEventListener('click', () => {
    stopSpeaking();
    transitionToPart1('skip button');
  });

  if (TTS.enabled) {
    speak(introText, { onend: () => { transitionToPart1('speak onend'); } });

    // ---- Bug fix: fallback safety net ----
    // Chrome's speechSynthesis has a well-documented bug where long utterances
    // (especially >15s, or when the tab is backgrounded) sometimes never fire
    // onend. The intro text above is ~600 characters and takes ~25-35s at
    // normal rate. As a safety net, we schedule a fallback timer that fires
    // after a generous upper-bound estimate of the intro duration. If onend
    // has not fired by then, the test advances anyway so the user is not left
    // stuck.
    const estimatedIntroMs = Math.max(15000, introText.length * 90); // ~90ms per char, min 15s
    mockTest.introFallbackTimer = setTimeout(() => {
      console.warn('[MockTest] Intro onend did not fire within ' + (estimatedIntroMs/1000) + 's — using fallback timer to advance to Part 1. (This is a Chrome speechSynthesis workaround.)');
      transitionToPart1('fallback timer');
    }, estimatedIntroMs);
  } else {
    // TTS disabled — immediately transition.
    transitionToPart1('tts disabled');
  }
}

function renderMockPart1(modal, settings) {
  const q = mockTest.questions.p1[mockTest.currentIdx];
  const id = 'mock-' + mockTest.testId + '-p1-' + mockTest.currentIdx;
  const total = mockTest.questions.p1.length;

  modal.innerHTML = `
    <div style="text-align:center;">
      <span class="mock-phase-badge">Part 1 — Introduction & Interview</span>
    </div>
    <div class="mock-progress-bar"><div class="fill" id="mock-progress-fill" style="width:0%"></div></div>
    <div class="mock-progress-label">Question ${mockTest.currentIdx + 1} of ${total}</div>
    <div class="mock-question-display">${esc(q.q)}</div>
    ${ttsIndicatorHTML()}
    <div class="mock-timer-label">Speaking Time Remaining</div>
    <div class="mock-timer-display" id="mock-timer-display">${String(Math.floor(settings.p1Time/60)).padStart(2,'0')}:${String(settings.p1Time%60).padStart(2,'0')}</div>
    <div id="mock-rec-status" style="text-align:center;font-size:13px;margin-top:10px;"></div>
    <div class="btn-row" style="justify-content:center;margin-top:16px;">
      <button class="btn danger sm" id="mock-emergency">⏹ Emergency Stop</button>
    </div>
  `;

  document.getElementById('mock-emergency').addEventListener('click', () => {
    if (confirm('Stop the test? Your progress will be saved.')) {
      if (mockTest.recordingId) stopRecording(mockTest.recordingId);
      stopSpeaking();
      if (mockTest.timer) { clearInterval(mockTest.timer); mockTest.timer = null; }
      closeMockTest();
    }
  });

  const statusEl = document.getElementById('mock-rec-status');

  // ---- Bug fix: transition-token guard + fallback timer ----
  // Captured at speak() dispatch time. If the test advances or closes by other
  // means, myToken becomes stale and the callback becomes a no-op.
  const myToken = mockTest.transitionToken;
  let advanced = false;
  function startRecordingAndTimer() {
    if (advanced) return;
    if (myToken !== mockTest.transitionToken) {
      console.warn('[MockTest Part1] startRecordingAndTimer ignored — token stale.');
      return;
    }
    advanced = true;
    // Clear the fallback timer — onend fired successfully.
    if (mockTest.qFallbackTimer) { clearTimeout(mockTest.qFallbackTimer); mockTest.qFallbackTimer = null; }
    statusEl.innerHTML = '<span style="color:#DC2626;font-weight:600;">● Recording — please answer now</span>';
    mockTest.recordingId = id;
    startRecording(id, q.q, 1).then(() => {
      // Defensive: ensure mockTest state is still consistent before starting timer
      if (myToken !== mockTest.transitionToken) {
        console.warn('[MockTest Part1] startMockTimer skipped — token stale after recording start.');
        return;
      }
      startMockTimer(settings.p1Time, 'speaking', () => {
        // Auto-stop
        try { stopRecording(id); } catch(e) { console.error('[MockTest Part1] stopRecording failed:', e); }
        statusEl.textContent = '⏰ Time up! Saving your answer...';
        setTimeout(() => { saveAndAdvance(id, 1, q.q); }, 1500);
      });
    }).catch(err => {
      console.error('[MockTest Part1] startRecording failed:', err);
      // Even if recording fails (mic permission denied, etc.), still run the
      // timer so the test continues. Use an empty recordingId.
      startMockTimer(settings.p1Time, 'speaking', () => {
        statusEl.textContent = '⏰ Time up! Saving your answer...';
        setTimeout(() => { saveAndAdvance(id, 1, q.q); }, 1500);
      });
    });
  }

  function autoFlowPart1() {
    if (TTS.enabled) {
      statusEl.textContent = '🔊 Examiner is asking the question...';
      speak(q.q, { onend: () => { startRecordingAndTimer(); } });
      // Fallback safety net: if speechSynthesis swallows onend (Chrome bug for
      // any utterance length, but especially relevant for medium-length ones),
      // advance after a generous estimate of the question's spoken duration.
      const estimatedMs = Math.max(4000, (q.q || '').length * 90);
      mockTest.qFallbackTimer = setTimeout(() => {
        console.warn('[MockTest Part1] Question onend did not fire within ' + (estimatedMs/1000) + 's — using fallback to start recording.');
        startRecordingAndTimer();
      }, estimatedMs);
    } else {
      startRecordingAndTimer();
    }
  }

  autoFlowPart1();
}

function renderMockPart2Prep(modal, settings) {
  const c = mockTest.questions.p2;
  const transitionText = "Now let us move on to Part Two. I am going to give you a topic card. You will have one minute to prepare, and then I would like you to speak for up to two minutes.";

  modal.innerHTML = `
    <div style="text-align:center;">
      <span class="mock-phase-badge">Part 2 — Individual Long Turn</span>
    </div>
    <div class="mock-progress-label">Preparation Phase</div>
    <div class="mock-cue-card-display">
      <div class="cue-title">${esc(c.title)}</div>
      <div style="font-size:12px;color:var(--text-soft);text-align:center;margin-bottom:8px;"><b>You should say:</b></div>
      <ul class="cue-bullets">${(c.bullets || []).map(b => '<li>' + esc(b) + '</li>').join('')}</ul>
    </div>
    ${ttsIndicatorHTML()}
    <div class="mock-timer-label">Preparation Time Remaining</div>
    <div class="mock-timer-display" id="mock-timer-display">${String(Math.floor(settings.p2Prep/60)).padStart(2,'0')}:${String(settings.p2Prep%60).padStart(2,'0')}</div>
    <div class="mock-progress-bar"><div class="fill" id="mock-progress-fill" style="width:0%"></div></div>
    <div id="mock-rec-status" style="text-align:center;font-size:13px;margin-top:10px;"></div>
    <div class="btn-row" style="justify-content:center;margin-top:16px;">
      <button class="btn danger sm" id="mock-emergency">⏹ Emergency Stop</button>
    </div>
  `;

  document.getElementById('mock-emergency').addEventListener('click', () => {
    if (confirm('Stop the test? Your progress will be saved.')) {
      stopSpeaking(); if (mockTest.timer) { clearInterval(mockTest.timer); mockTest.timer = null; } closeMockTest();
    }
  });

  const statusEl = document.getElementById('mock-rec-status');

  // ---- Bug fix: transition-token guard + fallback timer ----
  const myToken = mockTest.transitionToken;
  let advanced = false;
  function startPrepTimer() {
    if (advanced) return;
    if (myToken !== mockTest.transitionToken) {
      console.warn('[MockTest Part2Prep] startPrepTimer ignored — token stale.');
      return;
    }
    advanced = true;
    if (mockTest.qFallbackTimer) { clearTimeout(mockTest.qFallbackTimer); mockTest.qFallbackTimer = null; }
    statusEl.textContent = '⏳ Preparation time — plan your answer';
    startMockTimer(settings.p2Prep, 'prep', () => {
      mockTest.phase = 'part2-speak';
      renderMockTestPhase();
    });
  }

  // Speak transition + cue card instructions, then start prep timer
  if (TTS.enabled) {
    statusEl.textContent = '🔊 Examiner is introducing Part 2...';
    const fullText = transitionText + ' Here is your topic: ' + c.title + '. You should say: ' + (c.bullets || []).join('. ') + '. You have one minute to prepare.';
    speak(fullText, { onend: () => { startPrepTimer(); } });
    // Fallback safety net
    const estimatedMs = Math.max(6000, fullText.length * 90);
    mockTest.qFallbackTimer = setTimeout(() => {
      console.warn('[MockTest Part2Prep] onend did not fire within ' + (estimatedMs/1000) + 's — using fallback to start prep timer.');
      startPrepTimer();
    }, estimatedMs);
  } else {
    startPrepTimer();
  }
}

function renderMockPart2Speak(modal, settings) {
  const c = mockTest.questions.p2;
  const id = 'mock-' + mockTest.testId + '-p2';
  const beginText = 'Thank you. Now please begin speaking. You have up to two minutes.';

  modal.innerHTML = `
    <div style="text-align:center;">
      <span class="mock-phase-badge">Part 2 — Speaking</span>
    </div>
    <div class="mock-progress-label">Speak for up to 2 minutes</div>
    <div class="mock-cue-card-display">
      <div class="cue-title">${esc(c.title)}</div>
      <ul class="cue-bullets">${(c.bullets || []).map(b => '<li>' + esc(b) + '</li>').join('')}</ul>
    </div>
    ${ttsIndicatorHTML()}
    <div class="mock-timer-label">Speaking Time Remaining</div>
    <div class="mock-timer-display" id="mock-timer-display">${String(Math.floor(settings.p2Speak/60)).padStart(2,'0')}:${String(settings.p2Speak%60).padStart(2,'0')}</div>
    <div class="mock-progress-bar"><div class="fill" id="mock-progress-fill" style="width:0%"></div></div>
    <div id="mock-rec-status" style="text-align:center;font-size:13px;margin-top:10px;"></div>
    <div class="btn-row" style="justify-content:center;margin-top:16px;">
      <button class="btn danger sm" id="mock-emergency">⏹ Emergency Stop</button>
    </div>
  `;

  document.getElementById('mock-emergency').addEventListener('click', () => {
    if (confirm('Stop the test? Your progress will be saved.')) {
      if (mockTest.recordingId) stopRecording(mockTest.recordingId);
      stopSpeaking(); if (mockTest.timer) { clearInterval(mockTest.timer); mockTest.timer = null; } closeMockTest();
    }
  });

  const statusEl = document.getElementById('mock-rec-status');

  // ---- Bug fix: transition-token guard + fallback timer ----
  const myToken = mockTest.transitionToken;
  let advanced = false;
  function startRecordingAndTimer() {
    if (advanced) return;
    if (myToken !== mockTest.transitionToken) {
      console.warn('[MockTest Part2Speak] startRecordingAndTimer ignored — token stale.');
      return;
    }
    advanced = true;
    if (mockTest.qFallbackTimer) { clearTimeout(mockTest.qFallbackTimer); mockTest.qFallbackTimer = null; }
    statusEl.innerHTML = '<span style="color:#DC2626;font-weight:600;">● Recording — please speak now</span>';
    mockTest.recordingId = id;
    startRecording(id, c.title, 2).then(() => {
      if (myToken !== mockTest.transitionToken) {
        console.warn('[MockTest Part2Speak] startMockTimer skipped — token stale.');
        return;
      }
      startMockTimer(settings.p2Speak, 'speaking', () => {
        try { stopRecording(id); } catch(e) { console.error('[MockTest Part2Speak] stopRecording failed:', e); }
        statusEl.textContent = '⏰ Time up! Saving your answer...';
        setTimeout(() => { saveAndAdvance(id, 2, c.title, c.bullets); }, 1500);
      });
    }).catch(err => {
      console.error('[MockTest Part2Speak] startRecording failed:', err);
      startMockTimer(settings.p2Speak, 'speaking', () => {
        statusEl.textContent = '⏰ Time up! Saving your answer...';
        setTimeout(() => { saveAndAdvance(id, 2, c.title, c.bullets); }, 1500);
      });
    });
  }

  function autoFlowPart2Speak() {
    if (TTS.enabled) {
      statusEl.textContent = '🔊 Examiner is announcing...';
      speak(beginText, { onend: () => { startRecordingAndTimer(); } });
      // Fallback safety net
      const estimatedMs = Math.max(4000, beginText.length * 90);
      mockTest.qFallbackTimer = setTimeout(() => {
        console.warn('[MockTest Part2Speak] onend did not fire within ' + (estimatedMs/1000) + 's — using fallback.');
        startRecordingAndTimer();
      }, estimatedMs);
    } else {
      startRecordingAndTimer();
    }
  }

  autoFlowPart2Speak();
}

function renderMockPart3(modal, settings) {
  const q = mockTest.questions.p3[mockTest.currentIdx];
  const id = 'mock-' + mockTest.testId + '-p3-' + mockTest.currentIdx;
  const total = mockTest.questions.p3.length;
  const questionText = q.q || q;
  const transitionText = mockTest.currentIdx === 0 ? 'Thank you. Now we are going to discuss some more general questions related to the topic we have just discussed.' : '';

  modal.innerHTML = `
    <div style="text-align:center;">
      <span class="mock-phase-badge">Part 3 — Two-way Discussion</span>
    </div>
    <div class="mock-progress-bar"><div class="fill" id="mock-progress-fill" style="width:0%"></div></div>
    <div class="mock-progress-label">Question ${mockTest.currentIdx + 1} of ${total}</div>
    <div class="mock-question-display">${esc(questionText)}</div>
    ${ttsIndicatorHTML()}
    <div class="mock-timer-label">Speaking Time Remaining</div>
    <div class="mock-timer-display" id="mock-timer-display">${String(Math.floor(settings.p3Time/60)).padStart(2,'0')}:${String(settings.p3Time%60).padStart(2,'0')}</div>
    <div id="mock-rec-status" style="text-align:center;font-size:13px;margin-top:10px;"></div>
    <div class="btn-row" style="justify-content:center;margin-top:16px;">
      <button class="btn danger sm" id="mock-emergency">⏹ Emergency Stop</button>
    </div>
  `;

  document.getElementById('mock-emergency').addEventListener('click', () => {
    if (confirm('Stop the test? Your progress will be saved.')) {
      if (mockTest.recordingId) stopRecording(mockTest.recordingId);
      stopSpeaking(); if (mockTest.timer) { clearInterval(mockTest.timer); mockTest.timer = null; } closeMockTest();
    }
  });

  const statusEl = document.getElementById('mock-rec-status');

  // ---- Bug fix: transition-token guard + fallback timer ----
  const myToken = mockTest.transitionToken;
  let advanced = false;
  function startRecordingAndTimer() {
    if (advanced) return;
    if (myToken !== mockTest.transitionToken) {
      console.warn('[MockTest Part3] startRecordingAndTimer ignored — token stale.');
      return;
    }
    advanced = true;
    if (mockTest.qFallbackTimer) { clearTimeout(mockTest.qFallbackTimer); mockTest.qFallbackTimer = null; }
    statusEl.innerHTML = '<span style="color:#DC2626;font-weight:600;">● Recording — please answer now</span>';
    mockTest.recordingId = id;
    startRecording(id, questionText, 3).then(() => {
      if (myToken !== mockTest.transitionToken) {
        console.warn('[MockTest Part3] startMockTimer skipped — token stale.');
        return;
      }
      startMockTimer(settings.p3Time, 'speaking', () => {
        try { stopRecording(id); } catch(e) { console.error('[MockTest Part3] stopRecording failed:', e); }
        statusEl.textContent = '⏰ Time up! Saving your answer...';
        setTimeout(() => { saveAndAdvance(id, 3, questionText); }, 1500);
      });
    }).catch(err => {
      console.error('[MockTest Part3] startRecording failed:', err);
      startMockTimer(settings.p3Time, 'speaking', () => {
        statusEl.textContent = '⏰ Time up! Saving your answer...';
        setTimeout(() => { saveAndAdvance(id, 3, questionText); }, 1500);
      });
    });
  }

  function autoFlowPart3() {
    const speakText = (transitionText ? transitionText + ' ' : '') + questionText;
    if (TTS.enabled) {
      statusEl.textContent = '🔊 Examiner is asking the question...';
      speak(speakText, { onend: () => { startRecordingAndTimer(); } });
      // Fallback safety net
      const estimatedMs = Math.max(4000, speakText.length * 90);
      mockTest.qFallbackTimer = setTimeout(() => {
        console.warn('[MockTest Part3] onend did not fire within ' + (estimatedMs/1000) + 's — using fallback.');
        startRecordingAndTimer();
      }, estimatedMs);
    } else {
      startRecordingAndTimer();
    }
  }

  autoFlowPart3();
}

function saveAndAdvance(id, part, questionText, cueCardBullets) {
  const rec_q = getQ(id);
  saveMockAnswer(id, part, questionText, rec_q.transcript || '', rec_q.audioMetrics, cueCardBullets);
  mockTest.recordingId = null;

  if (part === 1) {
    mockTest.currentIdx++;
    if (mockTest.currentIdx >= mockTest.questions.p1.length) {
      mockTest.phase = 'part2-prep';
      mockTest.currentIdx = 0;
    }
  } else if (part === 2) {
    mockTest.phase = 'part3';
    mockTest.currentIdx = 0;
  } else if (part === 3) {
    mockTest.currentIdx++;
    if (mockTest.currentIdx >= mockTest.questions.p3.length) {
      mockTest.phase = 'completion';
    }
  }
  renderMockTestPhase();
}

function renderMockCompletion(modal) {
  // Auto-submit to AI evaluation
  modal.innerHTML = `
    <div class="mock-welcome">
      <div class="icon-big">🎉</div>
      <h2>Test Complete!</h2>
      <p>You answered ${mockTest.answers.length} questions. Automatically submitting for AI evaluation...</p>
      <div style="font-size:24px;margin-top:20px;">⏳</div>
      <div style="font-size:13px;color:var(--text-soft);margin-top:8px;">Please wait while your answers are evaluated.</div>
    </div>
    <div class="btn-row" style="justify-content:center;margin-top:16px;">
      <button class="btn sm" id="mock-review-answers">📋 Review Answers</button>
      <button class="btn danger sm" id="mock-skip-eval">Skip Evaluation</button>
    </div>
  `;

  document.getElementById('mock-review-answers').addEventListener('click', () => {
    let html = '<div class="mock-welcome"><div class="icon-big">📋</div><h2>Your Answers</h2></div>';
    mockTest.answers.forEach((ans, i) => {
      html += '<div class="card" style="margin-bottom:10px;padding:12px 16px;">';
      html += '<div style="font-size:11px;color:var(--text-soft);">Part ' + ans.part + ' — Answer ' + (i+1) + '</div>';
      html += '<div style="font-size:14px;font-weight:600;margin:4px 0;">' + esc(ans.questionText.substring(0, 100)) + '</div>';
      html += '<div class="mock-transcript-preview">' + esc(ans.transcript || '(no transcript)') + '</div>';
      html += '</div>';
    });
    html += '<div class="btn-row" style="justify-content:center;margin-top:16px;"><button class="btn" id="mock-back-complete">← Back</button></div>';
    modal.innerHTML = html;
    document.getElementById('mock-back-complete').addEventListener('click', () => renderMockCompletion(modal));
  });

  document.getElementById('mock-skip-eval').addEventListener('click', () => {
    saveMockTestToHistory(null);
    closeMockTest();
    toast('Test saved to history without evaluation.');
  });

  // Auto-submit after 2 seconds
  setTimeout(() => {
    if (mockTest.phase === 'completion' && !mockTest.submitting) {
      evaluateMockTest();
    }
  }, 2000);
}

async function evaluateMockTest() {
  if (mockTest.submitting) return;
  mockTest.submitting = true;
  const modal = document.getElementById('mock-modal');
  modal.innerHTML = `
    <div class="mock-welcome">
      <div class="icon-big">🤖</div>
      <h2>Analysing your speaking performance...</h2>
      <p>Google Gemini AI is evaluating your ${mockTest.answers.length} answers across all three parts of the IELTS Speaking test. This usually takes 30–60 seconds.</p>
      <div class="eval-loading-anim" style="justify-content:center;margin-top:20px;"><span class="dot" style="width:10px;height:10px;"></span><span class="dot" style="width:10px;height:10px;"></span><span class="dot" style="width:10px;height:10px;"></span></div>
      <div style="font-size:12px;color:var(--text-soft);margin-top:14px;">Evaluating Fluency, Lexical Resource, Grammatical Range & Accuracy, and Pronunciation against the official IELTS Speaking band descriptors.</div>
    </div>
  `;
  try {
    const resp = await fetch(AI_SERVER_URL + '/api/evaluate-mock-test', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ testSession: { testId: mockTest.testId, date: mockTest.date, answers: mockTest.answers } }),
      signal: AbortSignal.timeout(180000), // 3-min timeout for mock test (longer than single)
    });
    if (!resp.ok) throw new Error('Server responded ' + resp.status);
    const data = await resp.json();
    if (data.success && data.evaluation) {
      mockTest.evaluation = data.evaluation;
      mockTest.evalProvider = data.provider || 'unknown';
      mockTest.phase = 'results';
      saveMockTestToHistory(data.evaluation);
      renderMockTestPhase();
      toast('✅ Gemini evaluation complete — Band ' + (data.evaluation.overallBand || '?'));
    } else if (data.rawFeedback) {
      modal.innerHTML = '<div class="mock-welcome"><div class="icon-big">📝</div><h2>Evaluation Result</h2></div><div class="card">' + esc(data.rawFeedback) + '</div><div class="btn-row" style="justify-content:center;margin-top:16px;"><button class="btn" id="mock-close-eval">Close</button></div>';
      document.getElementById('mock-close-eval').addEventListener('click', () => { saveMockTestToHistory(null); closeMockTest(); });
    }
  } catch (err) {
    console.error('Mock test evaluation failed:', err);
    modal.innerHTML = `
      <div class="mock-welcome"><div class="icon-big">❌</div><h2>Evaluation Failed</h2>
      <p>Could not connect to the AI server, or the request timed out. Make sure the server is running (npm start in the server/ folder) and that your GEMINI_API_KEY is valid.</p>
      <p style="font-size:12px;color:var(--text-soft);">Error: ${esc(err.message)}</p>
      <div style="font-size:12px;color:var(--text-soft);margin-top:10px;background:var(--bg);padding:8px 10px;border-radius:6px;">✓ Your ${mockTest.answers.length} recorded answers are safely saved. You can retry evaluation now, or save the test without evaluation and retry later from Test History.</div>
      </div>
      <div class="btn-row" style="justify-content:center;">
        <button class="btn primary" id="mock-retry-eval">🔄 Retry Evaluation</button>
        <button class="btn" id="mock-save-no-eval">Save Without Evaluation</button>
      </div>
    `;
    mockTest.submitting = false;
    document.getElementById('mock-retry-eval').addEventListener('click', () => { mockTest.submitting = false; evaluateMockTest(); });
    document.getElementById('mock-save-no-eval').addEventListener('click', () => { saveMockTestToHistory(null); closeMockTest(); });
  }
}

function renderMockResults(modal) {
  const ev = mockTest.evaluation;
  if (!ev) { closeMockTest(); return; }
  const c = ev.criteria || {};
  const pbp = ev.partByPartAnalysis || {};
  const bcol = (s) => s >= 7 ? '#16A34A' : s >= 5 ? '#2563EB' : '#EA580C';
  const bc = (s) => s >= 7 ? 'high' : s >= 5 ? 'mid' : 'low';
  const endText = 'Thank you. That is the end of the speaking test. You may now finish the examination.';

  // Speak the end announcement
  if (TTS.enabled && mockTest.phase === 'results') {
    speak(endText);
  }

  // Build the optional sections
  let extraSections = '';

  // Overall feedback
  if (ev.overallFeedback) {
    extraSections += '<div class="card" style="margin:16px 0;"><h4 style="font-size:14px;margin-bottom:8px;">Overall Feedback</h4><div style="font-size:13px;line-height:1.7;">' + esc(ev.overallFeedback) + '</div></div>';
  }

  // Reliability warning
  if (ev.reliability && ev.reliability.isReliable === false) {
    extraSections += '<div class="eval-pron-feedback"><h5>⚠ Cannot reliably assess</h5><div style="font-size:12.5px;line-height:1.6;">' + esc(ev.reliability.reasonIfUnreliable || 'One or more answers were too short or unclear to evaluate reliably.') + '</div></div>';
  }

  // 4 criteria details
  if (c.fluency) extraSections += renderCriterionDetail('Fluency & Coherence', c.fluency);
  if (c.lexicalResource) extraSections += renderCriterionDetail('Lexical Resource', c.lexicalResource);
  if (c.grammar) extraSections += renderCriterionDetail('Grammatical Range & Accuracy', c.grammar);
  if (c.pronunciation) extraSections += renderCriterionDetail('Pronunciation', c.pronunciation);

  // Fluency feedback
  if (ev.fluencyFeedback) {
    const f = ev.fluencyFeedback;
    extraSections += '<div class="eval-fluency-feedback"><h5>🗣 Fluency Feedback</h5>';
    if (f.repetitions && f.repetitions.length) extraSections += '<div style="font-size:12px;font-weight:600;margin-top:4px;">Repetition:</div><ul>' + f.repetitions.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
    if (f.hesitations && f.hesitations.length) extraSections += '<div style="font-size:12px;font-weight:600;margin-top:4px;">Hesitation:</div><ul>' + f.hesitations.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
    if (f.weakDevelopment && f.weakDevelopment.length) extraSections += '<div style="font-size:12px;font-weight:600;margin-top:4px;">Weak development:</div><ul>' + f.weakDevelopment.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
    if (f.naturalAlternatives && f.naturalAlternatives.length) extraSections += '<div style="font-size:12px;font-weight:600;margin-top:4px;">More natural alternatives:</div><ul>' + f.naturalAlternatives.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
    extraSections += '</div>';
  }

  // Pronunciation feedback
  if (ev.pronunciationFeedback) {
    const pf = ev.pronunciationFeedback;
    extraSections += '<div class="eval-pron-feedback"><h5>🔊 Pronunciation Feedback</h5>';
    if (pf.assessedFromAudio === false) {
      extraSections += '<div class="na-notice">Pronunciation could not be reliably assessed from the transcript alone. Record your answers with a working microphone to get pronunciation feedback.</div>';
    } else {
      if (pf.summary) extraSections += '<div style="font-size:12.5px;line-height:1.6;margin-bottom:6px;">' + esc(pf.summary) + '</div>';
      if (pf.specificAreasForImprovement && pf.specificAreasForImprovement.length) {
        extraSections += '<div style="font-size:12px;font-weight:600;">Specific areas for improvement:</div><ul>' + pf.specificAreasForImprovement.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
      }
    }
    extraSections += '</div>';
  }

  // Grammar corrections (extended with natural alternatives)
  if (ev.grammarCorrections && ev.grammarCorrections.length) {
    extraSections += '<div class="eval-feedback-section"><h4>📝 Grammar Corrections</h4>';
    ev.grammarCorrections.forEach(gc => {
      extraSections += '<div class="eval-grammar-card">' +
        '<div class="gc-head"><span class="orig">' + esc(gc.original || '') + '</span> → <span class="corr">' + esc(gc.corrected || '') + '</span>' + (gc.part ? ' <span style="font-size:11px;color:var(--text-soft);">(Part ' + gc.part + ')</span>' : '') + '</div>' +
        '<div class="gc-expl">' + esc(gc.explanation || '') + '</div>' +
        (gc.naturalAlternative ? '<div class="gc-natural">💡 Natural alt: ' + esc(gc.naturalAlternative) + '</div>' : '') +
        '</div>';
    });
    extraSections += '</div>';
  }

  // Vocabulary improvements (extended with collocations + examples)
  if (ev.vocabularyImprovements && ev.vocabularyImprovements.length) {
    extraSections += '<div class="eval-feedback-section"><h4>📚 Vocabulary Improvements</h4>';
    ev.vocabularyImprovements.forEach(vi => {
      extraSections += '<div class="eval-vocab-card">' +
        '<div class="vc-head"><span class="orig">' + esc(vi.original || '') + '</span> → <span class="corr">' + esc(vi.suggested || '') + '</span>' + (vi.part ? ' <span style="font-size:11px;color:var(--text-soft);">(Part ' + vi.part + ')</span>' : '') + '</div>' +
        '<div class="vc-reason">' + esc(vi.reason || '') + '</div>' +
        (vi.collocations && vi.collocations.length ? '<div class="vc-collocations">Collocations: ' + vi.collocations.map(c => esc(c)).join(', ') + '</div>' : '') +
        (vi.exampleSentence ? '<div class="vc-example">e.g. ' + esc(vi.exampleSentence) + '</div>' : '') +
        '</div>';
    });
    extraSections += '</div>';
  }

  // Improvement plan
  if (ev.improvementPlan) {
    const ip = ev.improvementPlan;
    extraSections += '<div class="eval-improvement-plan"><h4>🎯 Personalised Improvement Plan</h4>';
    extraSections += '<div class="ip-grid">' +
      '<div class="ip-section weaknesses"><h5>⚠ Top weaknesses</h5><ul>' + (ip.topWeaknesses || []).map(s => '<li>' + esc(s) + '</li>').join('') + '</ul></div>' +
      '<div class="ip-section strengths"><h5>✓ Top strengths</h5><ul>' + (ip.topStrengths || []).map(s => '<li>' + esc(s) + '</li>').join('') + '</ul></div>' +
      '</div>';
    if (ip.exercises && ip.exercises.length) {
      extraSections += '<div style="font-size:12px;font-weight:600;color:var(--purple);margin-bottom:4px;">💡 Practical exercises</div><ul class="ip-exercises">' + ip.exercises.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul>';
    }
    if (ip.nextAnswerTips && ip.nextAnswerTips.length) {
      extraSections += '<div style="font-size:12px;font-weight:600;color:var(--blue);margin-bottom:4px;">📝 Tips for your next answer</div><div class="ip-tips"><ul style="margin:0;padding-left:18px;">' + ip.nextAnswerTips.map(s => '<li>' + esc(s) + '</li>').join('') + '</ul></div>';
    }
    extraSections += '</div>';
  }

  const providerBadge = '<span class="provider-badge ' + (mockTest.evalProvider === 'gemini' ? 'gemini' : 'zai') + '" style="display:inline-flex;margin:0 auto 12px;">' + esc(mockTest.evalProvider || 'unknown') + '</span>';

  modal.innerHTML = `
    <div class="mock-test-result">
      <div style="text-align:center;">${providerBadge}</div>
      <div class="eval-overall"><div class="overall-score">${ev.overallBand ? ev.overallBand.toFixed(1) : '?'}</div><div class="overall-label">Estimated Overall Speaking Band</div><div style="font-size:11px;opacity:.6;margin-top:6px;">AI-Estimated — For Practice Only</div></div>
      <div class="eval-band-grid">
        <div class="eval-band-card"><div class="criterion-name">Fluency & Coherence</div><div class="eval-band-circle ${bc(c.fluency?c.fluency.band:0)}">${c.fluency ? c.fluency.band.toFixed(1) : '?'}</div></div>
        <div class="eval-band-card"><div class="criterion-name">Lexical Resource</div><div class="eval-band-circle ${bc(c.lexicalResource?c.lexicalResource.band:0)}">${c.lexicalResource ? c.lexicalResource.band.toFixed(1) : '?'}</div></div>
        <div class="eval-band-card"><div class="criterion-name">Grammar</div><div class="eval-band-circle ${bc(c.grammar?c.grammar.band:0)}">${c.grammar ? c.grammar.band.toFixed(1) : '?'}</div></div>
        <div class="eval-band-card"><div class="criterion-name">Pronunciation</div><div class="eval-band-circle ${bc(c.pronunciation?c.pronunciation.band:0)}">${c.pronunciation ? c.pronunciation.band.toFixed(1) : '?'}</div></div>
      </div>
      ${pbp.part1 ? `<div class="mock-part-analysis">
        <div class="mock-part-card"><div class="part-name">Part 1</div><div class="part-score" style="color:${bcol(pbp.part1.band||0)}">${pbp.part1.band ? pbp.part1.band.toFixed(1) : '?'}</div></div>
        <div class="mock-part-card"><div class="part-name">Part 2</div><div class="part-score" style="color:${bcol(pbp.part2?pbp.part2.band:0)}">${pbp.part2 ? pbp.part2.band.toFixed(1) : '?'}</div></div>
        <div class="mock-part-card"><div class="part-name">Part 3</div><div class="part-score" style="color:${bcol(pbp.part3?pbp.part3.band:0)}">${pbp.part3 ? pbp.part3.band.toFixed(1) : '?'}</div></div>
      </div>` : ''}
      ${extraSections}
      <div class="eval-disclaimer">AI-Estimated IELTS Speaking Band Score — For Practice Only. Not an official IELTS result. The TAREQ IELTS Speaking Mock Examination is an independent practice tool and is not affiliated with or endorsed by IELTS, the British Council, or IDP.</div>
      <div class="btn-row" style="justify-content:center;margin-top:16px;">
        <button class="btn primary" id="mock-new-test">Take Another Test</button>
        <button class="btn" id="mock-close-results">Close</button>
      </div>
    </div>
  `;
  document.getElementById('mock-new-test').addEventListener('click', () => { closeMockTest(); setTimeout(startMockTest, 200); });
  document.getElementById('mock-close-results').addEventListener('click', closeMockTest);
}

function saveMockTestToHistory(evaluation) {
  state.mockTestHistory = state.mockTestHistory || [];
  state.mockTestHistory.push({
    testId: mockTest.testId, date: mockTest.date,
    examiner: mockTest.examiner, candidateName: mockTest.candidateName,
    questions: {
      p1: mockTest.questions.p1.map(q => ({ id: q.id, q: q.q, topic: q.topic })),
      p2: { id: mockTest.questions.p2.id, title: mockTest.questions.p2.title, bullets: mockTest.questions.p2.bullets },
      p3: mockTest.questions.p3.map(q => ({ id: q.id, q: q.q || q })),
    },
    answers: mockTest.answers, evaluation: evaluation, completedAt: new Date().toISOString(),
  });
  if (state.mockTestHistory.length > 50) state.mockTestHistory = state.mockTestHistory.slice(-50);
  saveState();
}

function renderTestHistoryPage() {
  const container = document.getElementById('test-history-list');
  const history = state.mockTestHistory || [];
  if (history.length === 0) {
    container.innerHTML = '<div class="card" style="text-align:center;padding:30px;color:var(--text-soft);"><div style="font-size:48px;margin-bottom:10px;">📊</div><h3 style="font-size:18px;margin-bottom:8px;">No mock tests yet</h3><p style="font-size:14px;">Take your first Full Mock Test to see your results here.</p></div>';
    return;
  }
  const bcol = (s) => s >= 7 ? '#16A34A' : s >= 5 ? '#2563EB' : '#EA580C';
  container.innerHTML = history.slice().reverse().map((t, idx) => {
    const realIdx = history.length - 1 - idx;
    const overall = t.evaluation ? t.evaluation.overallBand : null;
    const date = new Date(t.date).toLocaleDateString() + ' ' + new Date(t.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const exName = t.examiner ? t.examiner.name : 'N/A';
    return '<div class="mock-history-item" onclick="viewMockTestDetail(' + realIdx + ')"><div class="mhi-head"><div><div class="mhi-date">' + date + (exName !== 'N/A' ? ' • Examiner: ' + esc(exName) : '') + '</div><div class="mhi-meta"><span>📝 ' + t.answers.length + ' answers</span><span>P1: ' + t.answers.filter(a => a.part === 1).length + '</span><span>P2: ' + t.answers.filter(a => a.part === 2).length + '</span><span>P3: ' + t.answers.filter(a => a.part === 3).length + '</span></div></div>' + (overall !== null ? '<div class="mhi-band" style="background:' + bcol(overall) + ';">' + overall.toFixed(1) + '</div>' : '<div style="font-size:12px;color:var(--text-soft);">Not evaluated</div>') + '</div></div>';
  }).join('');
}

function viewMockTestDetail(idx) {
  const t = (state.mockTestHistory || [])[idx];
  if (!t) return;
  const ev = t.evaluation;
  const bcol = (s) => s >= 7 ? '#16A34A' : s >= 5 ? '#2563EB' : '#EA580C';
  const c = ev ? (ev.criteria || {}) : {};
  let html = '<div class="mock-history-detail"><div class="btn-row" style="margin-bottom:16px;"><button class="btn sm" id="back-to-history">← Back to History</button></div>';
  html += '<h2 style="font-size:20px;margin-bottom:8px;">Mock Test Results</h2>';
  html += '<div style="font-size:13px;color:var(--text-soft);margin-bottom:16px;">' + new Date(t.date).toLocaleString() + (t.examiner ? ' • Examiner: ' + esc(t.examiner.name) + ' (' + esc(t.examiner.id) + ')' : '') + '</div>';
  if (ev) {
    html += '<div class="eval-overall"><div class="overall-score">' + (ev.overallBand ? ev.overallBand.toFixed(1) : '?') + '</div><div class="overall-label">Estimated Overall Band</div></div>';
    html += '<div class="eval-band-grid">';
    html += '<div class="eval-band-card"><div class="criterion-name">Fluency</div><div class="eval-band-circle ' + (ev.overallBand >= 7 ? 'high' : ev.overallBand >= 5 ? 'mid' : 'low') + '">' + (c.fluency ? c.fluency.band.toFixed(1) : '?') + '</div></div>';
    html += '<div class="eval-band-card"><div class="criterion-name">Lexical</div><div class="eval-band-circle ' + (ev.overallBand >= 7 ? 'high' : ev.overallBand >= 5 ? 'mid' : 'low') + '">' + (c.lexicalResource ? c.lexicalResource.band.toFixed(1) : '?') + '</div></div>';
    html += '<div class="eval-band-card"><div class="criterion-name">Grammar</div><div class="eval-band-circle ' + (ev.overallBand >= 7 ? 'high' : ev.overallBand >= 5 ? 'mid' : 'low') + '">' + (c.grammar ? c.grammar.band.toFixed(1) : '?') + '</div></div>';
    html += '<div class="eval-band-card"><div class="criterion-name">Pronunciation</div><div class="eval-band-circle ' + (ev.overallBand >= 7 ? 'high' : ev.overallBand >= 5 ? 'mid' : 'low') + '">' + (c.pronunciation ? c.pronunciation.band.toFixed(1) : '?') + '</div></div>';
    html += '</div>';
    if (ev.overallFeedback) html += '<div class="card" style="margin:16px 0;"><h4 style="font-size:14px;margin-bottom:8px;">Overall Feedback</h4><div style="font-size:13px;line-height:1.7;">' + esc(ev.overallFeedback) + '</div></div>';
    if (ev.grammarCorrections && ev.grammarCorrections.length) { html += '<div class="eval-feedback-section"><h4>Grammar Corrections</h4>'; ev.grammarCorrections.forEach(gc => { html += '<div class="eval-correction"><span class="orig">' + esc(gc.original) + '</span> → <span class="corr">' + esc(gc.corrected) + '</span><div class="expl">' + esc(gc.explanation) + '</div></div>'; }); html += '</div>'; }
    if (ev.vocabularyImprovements && ev.vocabularyImprovements.length) { html += '<div class="eval-feedback-section"><h4>Vocabulary Improvements</h4>'; ev.vocabularyImprovements.forEach(vi => { html += '<div class="eval-correction"><span class="orig">' + esc(vi.original) + '</span> → <span class="corr">' + esc(vi.suggested) + '</span><div class="expl">' + esc(vi.reason) + '</div></div>'; }); html += '</div>'; }
  } else {
    html += '<div class="card" style="text-align:center;padding:20px;"><p style="color:var(--text-soft);">This test was not evaluated.</p><button class="btn primary" id="eval-old-test-' + idx + '">🤖 Evaluate Now</button></div>';
  }
  html += '<h3 style="font-size:16px;margin:20px 0 10px;">Your Answers</h3>';
  t.answers.forEach((ans, i) => {
    html += '<div class="card" style="margin-bottom:8px;padding:12px;"><div style="font-size:11px;color:var(--text-soft);">Part ' + ans.part + ' — Answer ' + (i + 1) + '</div><div style="font-size:14px;font-weight:600;margin:4px 0;">' + esc(ans.questionText.substring(0, 120)) + '</div><div class="mock-transcript-preview">' + esc(ans.transcript || '(no transcript)') + '</div></div>';
  });
  html += '<div class="btn-row" style="margin-top:16px;"><button class="btn danger sm" id="delete-test-' + idx + '">Delete This Test</button></div></div>';
  document.getElementById('test-history-list').innerHTML = html;
  document.getElementById('back-to-history').addEventListener('click', renderTestHistoryPage);
  const delBtn = document.getElementById('delete-test-' + idx);
  if (delBtn) delBtn.addEventListener('click', () => { if (confirm('Delete this test?')) { state.mockTestHistory.splice(idx, 1); saveState(); renderTestHistoryPage(); toast('Test deleted.'); } });
  const evalBtn = document.getElementById('eval-old-test-' + idx);
  if (evalBtn) evalBtn.addEventListener('click', async () => {
    evalBtn.disabled = true; evalBtn.textContent = '⏳ Evaluating...';
    try {
      const resp = await fetch(AI_SERVER_URL + '/api/evaluate-mock-test', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ testSession: { testId: t.testId, date: t.date, answers: t.answers } }) });
      const data = await resp.json();
      if (data.success && data.evaluation) { t.evaluation = data.evaluation; saveState(); viewMockTestDetail(idx); toast('✅ Evaluation complete!'); }
      else throw new Error('Evaluation failed');
    } catch (err) { evalBtn.disabled = false; evalBtn.textContent = '🤖 Evaluate Now'; toast('❌ Evaluation failed: ' + err.message); }
  });
}
window.viewMockTestDetail = viewMockTestDetail;

function clearTestHistory() {
  if (!confirm('Delete ALL test history? This cannot be undone.')) return;
  state.mockTestHistory = []; saveState(); renderTestHistoryPage(); toast('Test history cleared.');
}

// --- Bindings & Page Patches ---
// safeAddListener is idempotent: it checks a data-attribute on the element
// to avoid registering the SAME handler more than once. This prevents the
// "introduction plays twice / startMockTest runs multiple times" bug that
// occurs when addEventListener is called multiple times for the same element
// (which previously happened because bindMockTestButtons() was called both
// at top-level AND on DOMContentLoaded, plus a direct addEventListener call).
function safeAddListener(id, eventName, handler) {
  const el = document.getElementById(id);
  if (!el) return false;
  // Idempotency guard: mark the element with the handlers it has registered.
  el.__safeListeners = el.__safeListeners || {};
  const key = eventName + ':' + (handler.name || 'anon') + ':' + String(handler).length;
  if (el.__safeListeners[key]) return true; // already registered
  el.__safeListeners[key] = true;
  el.addEventListener(eventName, handler);
  return true;
}
function bindMockTestButtons() {
  safeAddListener('mock-start', 'click', startMockTest);
  safeAddListener('mock-generate-new', 'click', () => { generateMockTest(); renderMockTestContent(); });
  safeAddListener('clear-test-history', 'click', clearTestHistory);
}
bindMockTestButtons();
document.addEventListener('DOMContentLoaded', () => { loadMockSettings(); bindMockTestButtons(); initTTS(); });

const _origShowPageMock = showPage;
showPage = function(name) {
  _origShowPageMock.apply(this, arguments);
  if (name === 'mock-test') renderMockTestContent();
  if (name === 'test-history') renderTestHistoryPage();
  if (name === 'settings') { loadMockSettings(); initTTS(); }
};

function renderMockTestContent() {
  const container = document.getElementById('mock-test-content');
  if (!container) return;
  const history = state.mockTestHistory || [];
  const lastScore = history.length > 0 && history[history.length-1].evaluation ? history[history.length-1].evaluation.overallBand.toFixed(1) : 'N/A';
  container.innerHTML = `
    <div class="card">
      <h3 style="font-size:16px;margin-bottom:10px;">Ready to Take a Mock Test?</h3>
      <p style="font-size:13px;color:var(--text-soft);line-height:1.7;margin-bottom:14px;">
        ${history.length > 0 ? 'You have completed <b>' + history.length + '</b> mock test(s). Last score: <b>' + lastScore + '</b>' : "You haven't taken any mock tests yet. Click below to start!"}
      </p>
      <div style="font-size:12px;color:var(--text-soft);margin-bottom:14px;line-height:1.6;">
        <b>Examiner voice:</b> ${TTS.enabled ? '🔊 Enabled' : '🔇 Disabled'} (change in Settings)<br>
        <b>Auto-recording:</b> ✅ Questions flow automatically — no need to press buttons between answers
      </div>
      <div class="btn-row">
        <button class="btn primary" onclick="startMockTest()">▶ Start Full Speaking Test</button>
        <button class="btn" onclick="showPage('test-history')">📊 View Test History</button>
      </div>
    </div>
  `;
}

// Bug fix: previously these were direct addEventListener calls, which when
// combined with bindMockTestButtons() above (called both at top-level AND on
// DOMContentLoaded) resulted in #mock-start having 3 click listeners —
// clicking it would call startMockTest() 3 times, causing the welcome screen
// to be re-rendered 3 times and the examiner/questions to be re-shuffled.
// Use safeAddListener (which is idempotent) instead.
safeAddListener('mock-start', 'click', startMockTest);
safeAddListener('mock-generate-new', 'click', () => { renderMockTestContent(); });
safeAddListener('clear-test-history', 'click', clearTestHistory);

// Wire the dashboard hero banner's CTA to the SAME startMockTest() function
// used by the sidebar option and the mock-test page button. No mock-test logic
// is duplicated — both entry points trigger the identical setup process.
(function wireDashboardMockHero() {
  const heroBtn = document.getElementById('dashboard-mock-start');
  if (heroBtn) {
    heroBtn.addEventListener('click', () => {
      // Defensive: if for some reason startMockTest is not yet defined, fall
      // back to navigating to the mock-test page (sidebar's behaviour).
      if (typeof startMockTest === 'function') {
        startMockTest();
      } else {
        showPage('mock-test');
      }
    });
  }
})();

window.startMockTest = startMockTest;

// Initialize TTS on load
initTTS();

// ===== Init =====
applyTheme(state.settings.theme || 'light');
showPage(state.lastVisited && state.lastVisited.page ? state.lastVisited.page : 'dashboard');

// Expose for inline handlers
window.toggleComplete = toggleComplete;
window.toggleBookmark = toggleBookmark;
window.refreshNavCounts = refreshNavCounts;
window.renderPart2Cards = renderPart2Cards;
window.renderPart1Questions = renderPart1Questions;
window.renderPart1Topics = renderPart1Topics;
window.renderPart3Questions = renderPart3Questions;
window.renderPart3Topics = renderPart3Topics;
window.openCueCard = openCueCard;
window.startStrictPractice = startStrictPractice;

console.log('%cTAREQ IELTS loaded', 'color:#2563EB;font-weight:bold;font-size:14px');
console.log('Stats:', STATS);
</script>
</body>
</html>
"""

# Inject data
HTML = HTML.replace("__DATA_JSON__", DATA_JS)
HTML = HTML.replace("__CATS_JSON__", json.dumps(ALL_CATEGORIES, ensure_ascii=False))
# Inject embedded images (base64 data URIs)
HTML = HTML.replace("__LOGO_DATA_URI__", LOGO_DATA_URI)
HTML = HTML.replace("__PHOTO_DATA_URI__", PHOTO_DATA_URI)
HTML = HTML.replace("__THUMB_DATA_URI__", THUMB_DATA_URI)

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"Wrote {OUT_FILE}")
print(f"Size: {len(HTML):,} bytes ({len(HTML)//1024} KB)")
