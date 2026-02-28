import os
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ===== DEBUG SUPABASE (SEMENTARA) =====
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
st.write("DEBUG SUPABASE_URL:", SUPABASE_URL)
# =====================================

from crud import (
    tambah_data, get_all_data, get_data_by_id,
    update_data, delete_data,
    statistik_per_tahun, statistik_per_jenjang,
    statistik_per_kabupaten, bulk_insert
)
from validation import validate_input

st.set_page_config(
    page_title="RDB BBP Bali 2026",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PALETTE ====================
NAVY_900    = "#060f1e"
NAVY_800    = "#0a1628"
NAVY_700    = "#0d1f3c"
NAVY_600    = "#0e2d5a"
GOLD_500    = "#f5c518"
GOLD_400    = "#ffd740"
WHITE       = "#ffffff"
MUTED       = "#94a3b8"
BORDER_GOLD = "rgba(245,197,24,0.30)"
LOGO_URL    = "https://kemendikdasmen.go.id/web/image/res.company/1/logo/unique_id"
HERO_IMG    = "https://balaibahasaprovinsibali.kemendikdasmen.go.id/wp-content/uploads/2024/10/WhatsApp-Image-2024-10-25-at-09.40.22-1024x576.jpeg"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

/* ── Keyframes ── */
@keyframes gradShift {{
  0%   {{ background-position: 0%   50%; }}
  50%  {{ background-position: 100% 50%; }}
  100% {{ background-position: 0%   50%; }}
}}
@keyframes goldPulse {{
  0%,100% {{ box-shadow: 0 0 18px rgba(245,197,24,.15), 0 0 0 1px rgba(245,197,24,.10); }}
  50%      {{ box-shadow: 0 0 38px rgba(245,197,24,.40), 0 0 0 1px rgba(245,197,24,.30); }}
}}
@keyframes shimmer {{
  0%   {{ transform: translateX(-100%); }}
  100% {{ transform: translateX(500%); }}
}}
@keyframes fadeUp {{
  from {{ opacity:0; transform:translateY(20px); }}
  to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes fadeIn {{
  from {{ opacity:0; }}
  to   {{ opacity:1; }}
}}
@keyframes navLine {{
  0%   {{ background-position:-200% center; }}
  100% {{ background-position: 200% center; }}
}}
@keyframes float {{
  0%,100% {{ transform:translateY(0px); }}
  50%      {{ transform:translateY(-5px); }}
}}
@keyframes kenBurns {{
  0%   {{ transform:scale(1.00) translateX(0);    }}
  50%  {{ transform:scale(1.07) translateX(-14px); }}
  100% {{ transform:scale(1.00) translateX(0);    }}
}}
@keyframes scan {{
  0%   {{ top:0%;   opacity:.5; }}
  100% {{ top:100%; opacity:0;  }}
}}
@keyframes pop {{
  0%   {{ transform:scale(.95); opacity:.5; }}
  60%  {{ transform:scale(1.02); }}
  100% {{ transform:scale(1);   opacity:1;  }}
}}
@keyframes borderFlow {{
  0%,100% {{ border-color:rgba(245,197,24,.20); }}
  50%      {{ border-color:rgba(245,197,24,.55); }}
}}
@keyframes rainbowGold {{
  0%   {{ background-position: 0%   50%; }}
  50%  {{ background-position: 100% 50%; }}
  100% {{ background-position: 0%   50%; }}
}}
@keyframes waveMove {{
  0%   {{ transform: translateX(0) translateY(0) rotate(0deg); }}
  33%  {{ transform: translateX(30px) translateY(-20px) rotate(120deg); }}
  66%  {{ transform: translateX(-20px) translateY(10px) rotate(240deg); }}
  100% {{ transform: translateX(0) translateY(0) rotate(360deg); }}
}}
@keyframes orb1 {{
  0%,100% {{ transform:translate(0,0) scale(1); opacity:.18; }}
  33%      {{ transform:translate(60px,-40px) scale(1.15); opacity:.30; }}
  66%      {{ transform:translate(-30px,50px) scale(.90); opacity:.22; }}
}}
@keyframes orb2 {{
  0%,100% {{ transform:translate(0,0) scale(1); opacity:.14; }}
  40%      {{ transform:translate(-80px,30px) scale(1.2); opacity:.25; }}
  70%      {{ transform:translate(40px,-60px) scale(.88); opacity:.18; }}
}}
@keyframes textGlow {{
  0%,100% {{ text-shadow: 0 0 20px rgba(245,197,24,.30), 0 4px 24px rgba(0,0,0,.60); }}
  50%      {{ text-shadow: 0 0 50px rgba(245,197,24,.65), 0 4px 24px rgba(0,0,0,.60); }}
}}
@keyframes borderGlow {{
  0%,100% {{ box-shadow: 0 0 0 1px rgba(245,197,24,.15), 0 8px 32px rgba(0,0,0,.40); }}
  50%      {{ box-shadow: 0 0 0 2px rgba(245,197,24,.45), 0 16px 50px rgba(0,0,0,.55), 0 0 60px rgba(245,197,24,.10); }}
}}
@keyframes statPulse {{
  0%,100% {{ transform:scale(1); }}
  50%      {{ transform:scale(1.03); }}
}}
@keyframes lineSlide {{
  0%   {{ width:0; opacity:0; }}
  100% {{ width:100%; opacity:1; }}
}}
@keyframes chipFloat {{
  0%,100% {{ transform:translateY(0) translateX(0); }}
  25%      {{ transform:translateY(-3px) translateX(2px); }}
  75%      {{ transform:translateY(2px) translateX(-2px); }}
}}

/* ── Base ── */
html,body {{ background:{NAVY_800}!important; font-family:'Plus Jakarta Sans','Segoe UI',sans-serif!important; }}
[data-testid="stAppViewContainer"] {{
  background:linear-gradient(160deg,{NAVY_800} 0%,{NAVY_700} 55%,{NAVY_900} 100%)!important;
  min-height:100vh;
}}
[data-testid="stMain"] {{ background:transparent!important; }}
.block-container {{ padding-top:0!important; padding-bottom:3rem; max-width:1500px; }}
h1,h2,h3,h4,h5 {{ font-family:'Plus Jakarta Sans',sans-serif!important; font-weight:800!important; color:{WHITE}!important; }}

/* ── Navbar ── */
.kmd-nav {{
  background:linear-gradient(270deg,{NAVY_900},{NAVY_700},{NAVY_600},{NAVY_800},{NAVY_900});
  background-size:400% 400%;
  animation:gradShift 14s ease infinite;
  border-bottom:1px solid rgba(245,197,24,.18);
  margin:-1rem -1rem 0 -1rem; padding:0 30px;
  display:flex; align-items:center; gap:16px;
  height:78px; position:relative; overflow:hidden; z-index:100;
}}
.kmd-nav::before {{
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background:linear-gradient(90deg,transparent,{GOLD_500},{GOLD_400},transparent);
  background-size:200% 100%;
  animation:navLine 3.5s linear infinite;
}}
.kmd-nav::after {{
  content:''; position:absolute; top:0; bottom:0; width:60px;
  background:linear-gradient(90deg,transparent,rgba(245,197,24,.06),transparent);
  animation:shimmer 5s ease-in-out infinite; pointer-events:none;
}}
.kmd-nav-logo {{ height:50px; width:auto; object-fit:contain; filter:brightness(1.1) drop-shadow(0 2px 10px rgba(245,197,24,.25)); flex-shrink:0; }}
.kmd-nav-brand {{ font-size:21px; font-weight:900; letter-spacing:-.3px; flex-shrink:0; }}
.kmd-nav-brand .k {{ color:{WHITE}; }}
.kmd-nav-brand .d {{ color:{GOLD_500}; text-shadow:0 0 20px rgba(245,197,24,.60); }}
.kmd-nav-brand .s {{ color:{WHITE}; }}
.kmd-nav-sep {{ width:1px; height:38px; background:linear-gradient(180deg,transparent,rgba(255,255,255,.18),transparent); margin:0 6px; }}
.kmd-nav-sub {{ font-size:11px; color:{MUTED}; font-weight:500; line-height:1.5; }}
.kmd-nav-right {{ margin-left:auto; display:flex; align-items:center; gap:14px; }}
.kmd-nav-date {{ text-align:right; font-size:11px; color:{MUTED}; font-weight:600; line-height:1.6; }}
.kmd-nav-live {{
  background:linear-gradient(135deg,{GOLD_500},{GOLD_400}); color:{NAVY_900};
  font-size:10px; font-weight:900; padding:5px 14px; border-radius:999px;
  letter-spacing:1.2px; text-transform:uppercase;
  box-shadow:0 4px 18px rgba(245,197,24,.45);
  animation:float 3s ease-in-out infinite;
}}

/* ── Page header ── */
.kmd-ph {{
  background:linear-gradient(135deg,rgba(255,255,255,.035) 0%,rgba(245,197,24,.05) 100%);
  border:1px solid rgba(255,255,255,.08);
  border-left:4px solid {GOLD_500}; border-radius:18px;
  padding:17px 24px; margin:20px 0 22px 0;
  display:flex; align-items:center; gap:16px;
  backdrop-filter:blur(16px);
  box-shadow:0 8px 32px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.04);
  animation:borderFlow 4s ease-in-out infinite;
}}
.kmd-ph-icon {{
  width:52px; height:52px;
  background:linear-gradient(135deg,{GOLD_500},{GOLD_400}); border-radius:16px;
  display:flex; align-items:center; justify-content:center; font-size:26px; flex-shrink:0;
  box-shadow:0 6px 22px rgba(245,197,24,.35);
}}
.kmd-ph-title {{ font-size:19px; font-weight:900; color:{WHITE}; line-height:1.2; }}
.kmd-ph-sub   {{ font-size:12px; color:{MUTED}; margin-top:3px; font-weight:500; }}
.kmd-ph-tag   {{
  margin-left:auto; background:rgba(245,197,24,.10);
  border:1px solid {BORDER_GOLD}; color:{GOLD_500};
  font-size:9px; font-weight:900; padding:5px 12px;
  border-radius:999px; letter-spacing:1.5px; text-transform:uppercase;
}}

/* ── Section title ── */
.kmd-sec {{
  display:flex; align-items:center; gap:10px;
  font-size:15px; font-weight:800; color:{WHITE}; margin:8px 0 16px 0;
}}
.kmd-sec::before {{
  content:''; display:inline-block; width:4px; height:20px;
  background:linear-gradient(180deg,{GOLD_500},{GOLD_400}); border-radius:4px; flex-shrink:0;
}}

/* ═══════════════════════════════════════════
   HERO SECTION — BALAI BAHASA BALI
   ═══════════════════════════════════════════ */
.hero-wrap {{
  position:relative; border-radius:28px; overflow:hidden;
  margin:20px 0 0 0;
  animation:borderGlow 5s ease-in-out infinite, fadeUp .6s ease both;
}}
.hero-img {{
  width:100%; height:460px; object-fit:cover; display:block;
  animation:kenBurns 22s ease-in-out infinite;
}}
/* Deep cinematic overlays */
.hero-ov1 {{
  position:absolute; inset:0;
  background:linear-gradient(135deg,rgba(6,15,30,.88) 0%,rgba(10,22,40,.45) 40%,rgba(6,15,30,.92) 100%);
}}
/* Animated prismatic color wash */
.hero-ov2 {{
  position:absolute; inset:0;
  background:linear-gradient(
    270deg,
    rgba(245,197,24,.00),
    rgba(14,45,90,.35),
    rgba(245,197,24,.06),
    rgba(6,15,30,.20),
    rgba(245,197,24,.04),
    rgba(14,45,90,.30),
    rgba(245,197,24,.00)
  );
  background-size:600% 600%;
  animation:gradShift 9s ease infinite; pointer-events:none;
}}
/* Animated orbs for depth */
.hero-orb1 {{
  position:absolute; width:420px; height:420px; border-radius:50%;
  background:radial-gradient(circle,rgba(245,197,24,.18) 0%,rgba(245,197,24,0) 70%);
  top:-80px; left:-80px; pointer-events:none;
  animation:orb1 12s ease-in-out infinite;
}}
.hero-orb2 {{
  position:absolute; width:340px; height:340px; border-radius:50%;
  background:radial-gradient(circle,rgba(14,45,90,.50) 0%,rgba(6,15,30,0) 70%);
  bottom:-60px; right:10%; pointer-events:none;
  animation:orb2 15s ease-in-out infinite;
}}
/* Scan line effect */
.hero-scan {{
  position:absolute; left:0; right:0; height:2px;
  background:linear-gradient(90deg,transparent,rgba(245,197,24,.35),transparent);
  animation:scan 4.5s linear infinite; pointer-events:none;
}}
/* Bottom fade-out */
.hero-fade {{
  position:absolute; bottom:0; left:0; right:0; height:260px;
  background:linear-gradient(to top,{NAVY_800},transparent); pointer-events:none;
}}
/* Content area */
.hero-content {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  justify-content:flex-end; padding:40px 48px;
}}
/* Animated accent chip */
.hero-chip {{
  display:inline-flex; align-items:center; gap:8px;
  background:rgba(245,197,24,.12); border:1px solid rgba(245,197,24,.35);
  border-radius:999px; padding:6px 16px; margin-bottom:16px;
  width:fit-content; backdrop-filter:blur(10px);
  animation:chipFloat 4s ease-in-out infinite;
}}
.hero-chip span {{ font-size:10px; font-weight:800; letter-spacing:1.8px; text-transform:uppercase; color:{GOLD_500}; }}
/* Headline with animated glow */
.hero-h1 {{
  font-size:38px; font-weight:900; color:{WHITE}; line-height:1.12;
  letter-spacing:-.6px; margin-bottom:8px;
  animation:textGlow 4s ease-in-out infinite;
}}
.hero-h1 .gold {{
  background:linear-gradient(90deg,{GOLD_500},{GOLD_400},#ffe57a,{GOLD_500});
  background-size:300% 100%;
  animation:rainbowGold 5s ease infinite;
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}}
.hero-sub {{
  font-size:14px; color:rgba(255,255,255,.75); font-weight:500;
  line-height:1.65; max-width:580px; margin-bottom:22px;
}}
.hero-tags {{ display:flex; flex-wrap:wrap; gap:8px; }}
.hero-tag {{
  background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.14);
  border-radius:999px; padding:5px 14px;
  font-size:11px; font-weight:700; color:rgba(255,255,255,.85);
  backdrop-filter:blur(8px); transition:all .22s ease;
}}
.hero-tag:hover {{ background:rgba(245,197,24,.15); border-color:rgba(245,197,24,.40); color:{GOLD_500}; transform:translateY(-2px); }}
.hero-tag.g {{
  background:linear-gradient(135deg,rgba(245,197,24,.22),rgba(255,215,64,.12));
  border-color:rgba(245,197,24,.45); color:{GOLD_500}; font-weight:800;
}}
/* Year + Live pill corner */
.hero-corner {{
  position:absolute; top:22px; right:28px;
  display:flex; flex-direction:column; align-items:flex-end; gap:10px;
}}
.hero-yr {{
  font-size:64px; font-weight:900; line-height:1; letter-spacing:-3px; user-select:none;
  background:linear-gradient(135deg,rgba(245,197,24,.12),rgba(255,215,64,.06));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}}
.hero-live-pill {{
  display:flex; align-items:center; gap:7px;
  background:rgba(6,15,30,.76); backdrop-filter:blur(10px);
  border:1px solid rgba(245,197,24,.28); border-radius:999px; padding:6px 14px;
}}
.hero-dot {{
  width:7px; height:7px; border-radius:50%; background:{GOLD_500};
  box-shadow:0 0 10px {GOLD_500};
  animation:goldPulse 1.5s ease-in-out infinite;
}}
.hero-live-txt {{ font-size:10px; font-weight:800; color:{GOLD_500}; letter-spacing:1.2px; text-transform:uppercase; }}

/* ═══════════════════════════════════════════
   ABOUT — BALAI BAHASA PROVINSI BALI
   (NEW — distinct from BBPMP card below)
   ═══════════════════════════════════════════ */
.bbb-about {{
  position:relative; border-radius:26px; overflow:hidden;
  margin:18px 0 14px 0;
  background:
    linear-gradient(135deg,rgba(14,45,90,.70) 0%,rgba(6,15,30,.85) 100%);
  border:1px solid rgba(245,197,24,.18);
  box-shadow:0 16px 50px rgba(0,0,0,.40), inset 0 1px 0 rgba(255,255,255,.04);
  animation:fadeUp .65s ease .05s both;
}}
/* Animated top-border shimmer */
.bbb-about::before {{
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
  background:linear-gradient(90deg,
    transparent,{GOLD_500},{GOLD_400},#ffe57a,{GOLD_500},transparent);
  background-size:300% 100%;
  animation:rainbowGold 4s ease infinite;
}}
/* Floating mesh background */
.bbb-about::after {{
  content:''; position:absolute; inset:0;
  background:
    radial-gradient(ellipse 60% 40% at 80% 20%,rgba(245,197,24,.07) 0%,transparent 70%),
    radial-gradient(ellipse 40% 60% at 10% 90%,rgba(14,45,90,.55) 0%,transparent 60%);
  pointer-events:none;
}}
.bbb-inner {{
  position:relative; z-index:1;
  display:flex; gap:0; flex-wrap:wrap;
}}
/* Left accent strip */
.bbb-strip {{
  width:6px; flex-shrink:0;
  background:linear-gradient(180deg,{GOLD_500},{GOLD_400},rgba(245,197,24,.20));
  border-radius:0 0 0 26px;
  animation:rainbowGold 5s ease infinite;
  background-size:200% 200%;
}}
/* Main content */
.bbb-body {{
  flex:1; padding:32px 36px;
  display:flex; gap:28px; align-items:flex-start; flex-wrap:wrap;
}}
.bbb-icon-wrap {{
  flex-shrink:0; position:relative;
}}
.bbb-icon {{
  width:80px; height:80px; border-radius:22px;
  background:linear-gradient(135deg,{GOLD_500},{GOLD_400});
  display:flex; align-items:center; justify-content:center; font-size:38px;
  box-shadow:0 10px 32px rgba(245,197,24,.40);
  animation:goldPulse 4s ease-in-out infinite;
}}
.bbb-icon-ring {{
  position:absolute; inset:-4px; border-radius:26px;
  border:1.5px solid rgba(245,197,24,.25);
  animation:borderFlow 3s ease-in-out infinite;
  pointer-events:none;
}}
.bbb-text {{ flex:1; min-width:240px; }}
.bbb-badge-row {{ display:flex; gap:8px; flex-wrap:wrap; margin-bottom:12px; }}
.bbb-badge {{
  display:inline-flex; align-items:center; gap:5px;
  background:rgba(245,197,24,.10); border:1px solid rgba(245,197,24,.22);
  border-radius:999px; padding:4px 12px;
}}
.bbb-badge span {{ font-size:10px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; color:{GOLD_500}; }}
.bbb-badge.alt {{ background:rgba(255,255,255,.04); border-color:rgba(255,255,255,.10); }}
.bbb-badge.alt span {{ color:{MUTED}; }}
.bbb-title {{
  font-size:24px; font-weight:900; color:{WHITE}; line-height:1.18;
  letter-spacing:-.4px; margin-bottom:12px;
}}
.bbb-title .gold-text {{
  background:linear-gradient(90deg,{GOLD_500},{GOLD_400},#ffe57a);
  background-size:200% 100%;
  animation:rainbowGold 6s ease infinite;
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}}
.bbb-desc {{
  font-size:13.5px; color:rgba(255,255,255,.72); line-height:1.82; font-weight:400;
  margin-bottom:18px;
}}
.bbb-desc strong {{ color:{GOLD_400}; font-weight:700; }}
/* Divider line with animation */
.bbb-divider {{
  height:1px; margin:4px 0 18px 0;
  background:linear-gradient(90deg,transparent,rgba(245,197,24,.22),rgba(255,255,255,.08),transparent);
  background-size:300% 100%;
  animation:rainbowGold 8s ease infinite;
}}
/* Stats row */
.bbb-stats {{ display:flex; gap:12px; flex-wrap:wrap; }}
.bbb-stat {{
  flex:1; min-width:80px; max-width:120px;
  background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.07);
  border-radius:16px; padding:14px 16px; text-align:center;
  transition:all .24s cubic-bezier(.4,0,.2,1);
  position:relative; overflow:hidden; cursor:default;
}}
.bbb-stat::before {{
  content:''; position:absolute; inset:0; border-radius:16px;
  background:linear-gradient(135deg,rgba(245,197,24,.08),transparent);
  opacity:0; transition:opacity .24s ease;
}}
.bbb-stat:hover {{ border-color:rgba(245,197,24,.35); transform:translateY(-4px); box-shadow:0 12px 28px rgba(0,0,0,.30); }}
.bbb-stat:hover::before {{ opacity:1; }}
.bbb-num {{
  font-size:22px; font-weight:900; line-height:1; letter-spacing:-.5px;
  background:linear-gradient(135deg,{GOLD_500},{GOLD_400});
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}}
.bbb-lbl {{ font-size:9.5px; color:{MUTED}; font-weight:700; text-transform:uppercase; letter-spacing:.6px; margin-top:5px; }}
/* Visi-Misi pills row */
.bbb-pills {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:14px; }}
.bbb-pill {{
  background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09);
  border-radius:10px; padding:8px 14px;
  font-size:11.5px; font-weight:600; color:rgba(255,255,255,.72);
  transition:all .20s ease; cursor:default;
}}
.bbb-pill:hover {{ background:rgba(245,197,24,.07); border-color:rgba(245,197,24,.25); color:{GOLD_500}; }}
.bbb-pill .pi {{ margin-right:5px; }}

/* ── BBPMP About card (original) ── */
.kmd-about {{
  background:linear-gradient(135deg,rgba(14,45,90,.55) 0%,rgba(6,15,30,.72) 100%);
  border:1px solid rgba(245,197,24,.14); border-radius:22px;
  padding:32px 36px; margin:0 0 24px 0;
  position:relative; overflow:hidden;
  backdrop-filter:blur(12px);
  box-shadow:0 12px 40px rgba(0,0,0,.32);
  animation:fadeUp .7s ease .2s both;
}}
.kmd-about::before {{
  content:''; position:absolute; inset:0; border-radius:22px; padding:1px;
  background:linear-gradient(270deg,rgba(245,197,24,.50),rgba(245,197,24,.06),rgba(245,197,24,.50));
  background-size:300% 300%;
  animation:gradShift 6s ease infinite;
  -webkit-mask:linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor; mask-composite:exclude; pointer-events:none;
}}
.about-inner {{ position:relative; z-index:1; display:flex; gap:32px; align-items:flex-start; }}
.about-icon {{
  flex-shrink:0; width:72px; height:72px;
  background:linear-gradient(135deg,{GOLD_500},{GOLD_400}); border-radius:22px;
  display:flex; align-items:center; justify-content:center; font-size:34px;
  box-shadow:0 8px 28px rgba(245,197,24,.35);
  animation:goldPulse 4s ease-in-out infinite;
}}
.about-body {{ flex:1; }}
.about-badge {{
  display:inline-flex; align-items:center; gap:6px;
  background:rgba(245,197,24,.10); border:1px solid rgba(245,197,24,.25);
  border-radius:999px; padding:4px 12px; margin-bottom:10px;
}}
.about-badge span {{ font-size:10px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; color:{GOLD_500}; }}
.about-title {{ font-size:22px; font-weight:900; color:{WHITE}; line-height:1.2; margin-bottom:10px; letter-spacing:-.3px; }}
.about-desc {{ font-size:13.5px; color:rgba(255,255,255,.72); line-height:1.78; font-weight:400; }}
.about-desc strong {{ color:{GOLD_400}; font-weight:700; }}
.about-stats {{ display:flex; gap:14px; margin-top:20px; flex-wrap:wrap; }}
.about-stat {{
  background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08);
  border-radius:14px; padding:12px 18px; text-align:center; min-width:88px;
  transition:all .22s ease; cursor:default;
}}
.about-stat:hover {{
  background:rgba(245,197,24,.08); border-color:rgba(245,197,24,.25);
  transform:translateY(-3px); box-shadow:0 8px 22px rgba(0,0,0,.25);
}}
.about-num {{ font-size:20px; font-weight:900; color:{GOLD_500}; line-height:1; letter-spacing:-.5px; }}
.about-lbl {{ font-size:10px; color:{MUTED}; font-weight:700; text-transform:uppercase; letter-spacing:.5px; margin-top:4px; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{ background:{NAVY_900}!important; border-right:1px solid rgba(245,197,24,.10)!important; }}
[data-testid="stSidebar"] > div:first-child {{ background:{NAVY_900}!important; }}
.kmd-sb {{
  background:linear-gradient(270deg,rgba(14,45,90,.90),{NAVY_700},{NAVY_900});
  background-size:300% 300%; animation:gradShift 10s ease infinite;
  border:1px solid {BORDER_GOLD}; border-radius:18px; padding:20px 16px;
  margin-bottom:6px; position:relative; overflow:hidden;
}}
.kmd-sb::after {{
  content:''; position:absolute; bottom:0; left:10%; right:10%; height:1px;
  background:linear-gradient(90deg,transparent,{GOLD_500},transparent); opacity:.35;
}}
.kmd-sb-logo {{ width:58px; height:58px; background:rgba(255,255,255,.06); border:1px solid {BORDER_GOLD}; border-radius:16px; display:flex; align-items:center; justify-content:center; margin-bottom:14px; overflow:hidden; }}
.kmd-sb-logo img {{ width:44px; height:44px; object-fit:contain; filter:brightness(1.1); }}
.kmd-sb-t {{ font-size:15px; font-weight:900; color:{WHITE}; line-height:1.2; margin-bottom:4px; }}
.kmd-sb-s {{ font-size:11px; color:{MUTED}; font-weight:500; line-height:1.5; }}
.kmd-sb-d {{ margin-top:12px; padding-top:10px; border-top:1px solid rgba(255,255,255,.08); font-size:11px; color:rgba(245,197,24,.65); font-weight:600; }}
.kmd-nl {{ font-size:10px; font-weight:800; letter-spacing:2px; text-transform:uppercase; color:rgba(245,197,24,.40); padding:0 4px; margin:14px 0 6px 0; }}
div[role="radiogroup"] > label {{ background:rgba(255,255,255,.025)!important; border:1px solid rgba(255,255,255,.07)!important; border-radius:13px!important; padding:10px 13px!important; margin:3px 0!important; cursor:pointer; transition:all .20s cubic-bezier(.4,0,.2,1)!important; font-weight:600!important; color:{MUTED}!important; }}
div[role="radiogroup"] > label:hover {{ border-color:rgba(245,197,24,.38)!important; background:rgba(245,197,24,.07)!important; color:{GOLD_500}!important; transform:translateX(4px)!important; }}
div[role="radiogroup"] input:checked + div {{ color:{GOLD_500}!important; font-weight:800!important; }}
[data-testid="stSidebar"] p,[data-testid="stSidebar"] span,[data-testid="stSidebar"] label {{ color:{MUTED}; }}
.kmd-sb-foot {{ background:rgba(255,255,255,.025); border:1px solid rgba(255,255,255,.07); border-radius:14px; padding:13px; text-align:center; margin-top:8px; }}

/* ── Metrics ── */
[data-testid="stMetric"] {{
  background:linear-gradient(270deg,rgba(255,255,255,.04),rgba(245,197,24,.045),rgba(14,45,90,.50),rgba(255,255,255,.04))!important;
  background-size:400% 400%!important;
  animation:gradShift 8s ease infinite, pop .6s ease both!important;
  border:1px solid rgba(255,255,255,.07)!important;
  border-top:3px solid {GOLD_500}!important;
  border-radius:18px!important; padding:18px 20px!important;
  box-shadow:0 8px 30px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.04)!important;
  transition:transform .22s ease, box-shadow .22s ease!important;
}}
[data-testid="stMetric"]:hover {{ transform:translateY(-6px)!important; box-shadow:0 22px 50px rgba(0,0,0,.42), 0 0 0 1px rgba(245,197,24,.22)!important; }}
[data-testid="stMetricLabel"] > div {{ color:{MUTED}!important; font-weight:700!important; font-size:11px!important; letter-spacing:.6px; text-transform:uppercase; }}
[data-testid="stMetricValue"] > div {{ color:{GOLD_500}!important; font-weight:900!important; font-size:32px!important; letter-spacing:-1px; text-shadow:0 0 30px rgba(245,197,24,.25); }}
[data-testid="stVerticalBlockBorderWrapper"] {{ background:rgba(255,255,255,.025)!important; border:1px solid rgba(255,255,255,.07)!important; border-radius:20px!important; box-shadow:0 10px 36px rgba(0,0,0,.28)!important; backdrop-filter:blur(10px); }}

/* ── Buttons ── */
.stButton > button {{ font-family:'Plus Jakarta Sans',sans-serif!important; font-weight:800!important; border-radius:12px!important; padding:.55rem 1.3rem!important; transition:all .20s cubic-bezier(.4,0,.2,1)!important; letter-spacing:.3px; position:relative; overflow:hidden; }}
.stButton > button[kind="primary"] {{ background:linear-gradient(135deg,{GOLD_500},{GOLD_400})!important; color:{NAVY_900}!important; border:none!important; box-shadow:0 6px 22px rgba(245,197,24,.38)!important; }}
.stButton > button[kind="primary"]:hover {{ box-shadow:0 12px 34px rgba(245,197,24,.55)!important; transform:translateY(-3px)!important; }}
.stButton > button[kind="secondary"] {{ background:rgba(245,197,24,.06)!important; color:{GOLD_500}!important; border:1.5px solid {BORDER_GOLD}!important; }}
.stButton > button[kind="secondary"]:hover {{ background:rgba(245,197,24,.12)!important; border-color:{GOLD_500}!important; transform:translateY(-2px)!important; }}

/* ── Inputs ── */
input,textarea {{ background:rgba(255,255,255,.05)!important; border:1.5px solid rgba(255,255,255,.11)!important; border-radius:12px!important; color:{WHITE}!important; font-family:'Plus Jakarta Sans',sans-serif!important; transition:border-color .18s ease,box-shadow .18s ease!important; }}
input:focus,textarea:focus {{ border-color:{GOLD_500}!important; box-shadow:0 0 0 3px rgba(245,197,24,.14)!important; background:rgba(255,255,255,.07)!important; }}
input::placeholder {{ color:rgba(148,163,184,.45)!important; }}
[data-testid="stTextInput"] label,[data-testid="stNumberInput"] label,[data-testid="stSelectbox"] label,[data-testid="stRadio"] > label,[data-testid="stFileUploader"] label {{ color:rgba(148,163,184,.85)!important; font-weight:700!important; font-size:11px!important; letter-spacing:.5px; text-transform:uppercase; }}
[data-testid="stSelectbox"] > div > div {{ background:rgba(255,255,255,.05)!important; border:1.5px solid rgba(255,255,255,.11)!important; border-radius:12px!important; color:{WHITE}!important; }}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{ border-radius:16px!important; overflow:hidden!important; border:1px solid rgba(255,255,255,.08)!important; box-shadow:0 8px 28px rgba(0,0,0,.28)!important; }}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {{ background:rgba(255,255,255,.03)!important; border:1px solid rgba(255,255,255,.07)!important; border-radius:14px; padding:4px; gap:4px; }}
[data-testid="stTabs"] button {{ font-weight:700!important; font-family:'Plus Jakarta Sans',sans-serif!important; border-radius:10px!important; color:{MUTED}!important; transition:all .18s ease!important; }}
[data-testid="stTabs"] button:hover {{ color:{GOLD_500}!important; background:rgba(245,197,24,.07)!important; }}
[data-testid="stTabs"] button[aria-selected="true"] {{ background:linear-gradient(135deg,rgba(245,197,24,.18),rgba(245,197,24,.08))!important; color:{GOLD_500}!important; font-weight:900!important; border:1px solid {BORDER_GOLD}!important; }}

/* ── Alerts ── */
[data-testid="stAlert"] {{ background:rgba(255,255,255,.03)!important; border:1px solid rgba(255,255,255,.07)!important; border-left:4px solid {GOLD_500}!important; border-radius:14px!important; color:{WHITE}!important; }}
[data-testid="stAlert"] p,div[role="alert"] {{ color:{WHITE}!important; }}

/* ── File uploader ── */
[data-testid="stFileUploaderDropzone"] {{ background:rgba(255,255,255,.025)!important; border:2px dashed {BORDER_GOLD}!important; border-radius:18px!important; transition:all .20s ease!important; }}
[data-testid="stFileUploaderDropzone"]:hover {{ background:rgba(245,197,24,.05)!important; border-color:{GOLD_500}!important; }}
[data-testid="stFileUploaderDropzone"] span,[data-testid="stFileUploaderDropzone"] p {{ color:{MUTED}!important; }}

/* ── Download ── */
[data-testid="stDownloadButton"] > button {{ border-radius:12px!important; font-weight:800!important; font-family:'Plus Jakarta Sans',sans-serif!important; }}

/* ── Progress ── */
[data-testid="stProgressBar"] > div {{ background:rgba(255,255,255,.08)!important; border-radius:999px!important; }}
[data-testid="stProgressBar"] > div > div {{ background:linear-gradient(90deg,{GOLD_500},{GOLD_400})!important; border-radius:999px!important; box-shadow:0 0 14px rgba(245,197,24,.40); }}

/* ── Misc ── */
hr {{ border:none!important; height:1px!important; background:linear-gradient(90deg,transparent,rgba(245,197,24,.18),transparent)!important; margin:22px 0!important; }}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li {{ color:{MUTED}!important; }}
[data-testid="stMarkdownContainer"] strong {{ color:{WHITE}!important; font-weight:800; }}
[data-testid="stMarkdownContainer"] h3 {{ color:{WHITE}!important; font-weight:800!important; }}
[data-testid="stForm"] {{ background:rgba(255,255,255,.02)!important; border:1px solid rgba(255,255,255,.07)!important; border-radius:20px!important; padding:22px!important; box-shadow:0 8px 34px rgba(0,0,0,.22)!important; }}
[data-testid="stRadio"] > div > label {{ color:{MUTED}!important; background:rgba(255,255,255,.03)!important; border:1px solid rgba(255,255,255,.08)!important; border-radius:10px!important; padding:7px 12px!important; transition:all .16s ease!important; }}
[data-testid="stRadio"] > div > label:hover {{ color:{GOLD_500}!important; border-color:{BORDER_GOLD}!important; background:rgba(245,197,24,.06)!important; }}
.stSpinner > div {{ border-top-color:{GOLD_500}!important; }}
::-webkit-scrollbar {{ width:5px; height:5px; }}
::-webkit-scrollbar-track {{ background:{NAVY_900}; }}
::-webkit-scrollbar-thumb {{ background:rgba(245,197,24,.28); border-radius:999px; }}
::-webkit-scrollbar-thumb:hover {{ background:rgba(245,197,24,.50); }}
[data-testid="stDecoration"] {{ display:none!important; }}
[data-testid="stHeader"] {{ background:transparent!important; }}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ==================== HELPERS ====================
def style_plotly(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=WHITE, family="Plus Jakarta Sans"),
        title_font=dict(color=WHITE, family="Plus Jakarta Sans"),
        margin=dict(l=20, r=20, t=44, b=20),
        legend=dict(bgcolor="rgba(6,15,30,.88)", bordercolor="rgba(255,255,255,.10)",
                    borderwidth=1, font=dict(color=WHITE, size=12))
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,.06)", zeroline=False,
                     tickfont=dict(color=MUTED, size=11), linecolor="rgba(255,255,255,.08)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,.06)", zeroline=False,
                     tickfont=dict(color=MUTED, size=11), linecolor="rgba(255,255,255,.08)")
    return fig

COLORS = [GOLD_500, GOLD_400, "#e8a820", "#ffd740", "#b8860b", "#ffe57a", "#c8960c"]

def ph(icon, title, subtitle, tag=""):
    t = f'<div class="kmd-ph-tag">{tag}</div>' if tag else ""
    st.markdown(f"""<div class="kmd-ph">
      <div class="kmd-ph-icon">{icon}</div>
      <div><div class="kmd-ph-title">{title}</div><div class="kmd-ph-sub">{subtitle}</div></div>
      {t}
    </div>""", unsafe_allow_html=True)

def sec(label):
    st.markdown(f'<div class="kmd-sec">{label}</div>', unsafe_allow_html=True)

# ==================== NAVBAR ====================
st.markdown(f"""
<div class="kmd-nav">
  <img src="{LOGO_URL}" class="kmd-nav-logo" alt="Kemendikdasmen"
       onerror="this.style.display='none'" />
  <div class="kmd-nav-brand"><span class="k">Kemen</span><span class="d">dik</span><span class="s">dasmen</span></div>
  <div class="kmd-nav-sep"></div>
  <div class="kmd-nav-sub">Balai Bahasa Provinsi Bali<br/>RDB 2026</div>
  <div class="kmd-nav-right">
    <div class="kmd-nav-date">{datetime.now().strftime('%A, %d %B')}<br/><strong style="color:{WHITE};">{datetime.now().strftime('%Y')}</strong></div>
    <div class="kmd-nav-live">● LIVE</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown(f"""
    <div class="kmd-sb">
      <div class="kmd-sb-logo">
        <img src="{LOGO_URL}" alt="Logo"
             onerror="this.outerHTML='<span style=&quot;font-size:28px&quot;>🏛️</span>'" />
      </div>
      <div class="kmd-sb-t">RDB BBP Bali 2026</div>
      <div class="kmd-sb-s">Sistem Informasi Pendataan<br/>Peserta Rapat Dinas Bersama</div>
      <div class="kmd-sb-d">🗓️&nbsp; <strong>{datetime.now().strftime('%d %B %Y')}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="kmd-nl">⬡ Navigasi Utama</div>', unsafe_allow_html=True)

    menu = st.radio("Menu",
        ["🏠 Dashboard", "🔍 Filter Data", "➕ Tambah Data",
         "✏️ Edit Data", "🗑️ Hapus Data", "📊 Rekapan", "📤 Upload Excel"],
        label_visibility="collapsed")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="kmd-sb-foot">
      <div style="font-size:9px;font-weight:900;letter-spacing:2px;text-transform:uppercase;color:rgba(245,197,24,.38);margin-bottom:6px;">KEMENDIKDASMEN RI</div>
      <div style="font-size:11px;font-weight:800;color:{GOLD_500};line-height:1.4;">Balai Bahasa Provinsi Bali</div>
      <div style="font-size:10px;color:{MUTED};margin-top:5px;line-height:1.5;">Jl. Trengguli I No.34, Denpasar</div>
      <div style="margin-top:8px;font-size:10px;font-weight:700;color:rgba(245,197,24,.28);">kemendikdasmen.go.id</div>
    </div>""", unsafe_allow_html=True)

# ==================== DASHBOARD ====================
if menu == "🏠 Dashboard":

    # ─── HERO ──────────────────────────────────────────────────
    st.markdown(f"""
    <div class="hero-wrap">
      <img src="{HERO_IMG}" class="hero-img"
           alt="Balai Bahasa Provinsi Bali"
           onerror="this.style.cssText='width:100%;height:460px;display:block;background:linear-gradient(135deg,{NAVY_700},{NAVY_900})'" />
      <div class="hero-ov1"></div>
      <div class="hero-ov2"></div>
      <div class="hero-orb1"></div>
      <div class="hero-orb2"></div>
      <div class="hero-scan"></div>
      <div class="hero-fade"></div>
      <div class="hero-corner">
        <div class="hero-yr">{datetime.now().year}</div>
        <div class="hero-live-pill">
          <div class="hero-dot"></div>
          <span class="hero-live-txt">Live Data</span>
        </div>
      </div>
      <div class="hero-content">
        <div class="hero-chip"><span>📚 Kemendikdasmen · Provinsi Bali</span></div>
        <div class="hero-h1">Balai Bahasa<br/><span class="gold">Provinsi Bali</span></div>
        <div class="hero-sub">Lembaga resmi di bawah Kemendikdasmen RI yang mengemban misi pelindungan, pembinaan, dan pengembangan bahasa &amp; sastra Indonesia di Bali — menjaga warisan budaya serta memperkuat identitas kebangsaan.</div>
        <div class="hero-tags">
          <span class="hero-tag g">📚 RDB 2026</span>
          <span class="hero-tag">🎓 Balai Bahasa Bali</span>
          <span class="hero-tag">📍 Provinsi Bali</span>
          <span class="hero-tag">🔤 Bahasa &amp; Sastra</span>
          <span class="hero-tag">📊 Data Peserta</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ─── ABOUT — BALAI BAHASA PROVINSI BALI (NEW) ─────────────
    st.markdown(f"""
    <div class="bbb-about">
      <div class="bbb-inner">
        <div class="bbb-strip"></div>
        <div class="bbb-body">
          <div class="bbb-icon-wrap">
            <div class="bbb-icon">📚</div>
            <div class="bbb-icon-ring"></div>
          </div>
          <div class="bbb-text">
            <div class="bbb-badge-row">
              <div class="bbb-badge"><span>✦ Tentang Lembaga</span></div>
              <div class="bbb-badge alt"><span>Kemendikdasmen RI</span></div>
              <div class="bbb-badge alt"><span>Est. 1979</span></div>
            </div>
            <div class="bbb-title">
              Balai Bahasa <span class="gold-text">Provinsi Bali</span>
            </div>
            <div class="bbb-desc">
              <strong>Balai Bahasa Provinsi Bali</strong> adalah unit pelaksana teknis di bawah
              <strong>Kementerian Pendidikan Dasar dan Menengah (Kemendikdasmen)</strong>
              yang menjalankan tugas pokok di bidang <strong>pelindungan, pembinaan, dan pengembangan bahasa serta sastra Indonesia</strong>
              di wilayah Provinsi Bali. Lembaga ini berperan aktif dalam
              <strong>penelitian kebahasaan</strong>, penyuluhan bahasa kepada masyarakat dan dunia pendidikan,
              serta <strong>pelestarian sastra daerah Bali</strong> sebagai bagian dari kekayaan budaya nasional.
              Melalui program strategisnya, Balai Bahasa Provinsi Bali turut berkontribusi dalam
              <strong>peningkatan literasi</strong>, pemasyarakatan penggunaan bahasa Indonesia yang baik dan benar,
              serta penguatan identitas kebangsaan di era globalisasi.
            </div>
            <div class="bbb-divider"></div>
            <div class="bbb-stats">
              <div class="bbb-stat"><div class="bbb-num">45+</div><div class="bbb-lbl">Tahun Berdiri</div></div>
              <div class="bbb-stat"><div class="bbb-num">9</div><div class="bbb-lbl">Kab / Kota</div></div>
              <div class="bbb-stat"><div class="bbb-num">500+</div><div class="bbb-lbl">Penelitian</div></div>
              <div class="bbb-stat"><div class="bbb-num">RDB</div><div class="bbb-lbl">2026</div></div>
              <div class="bbb-stat"><div class="bbb-num">SNP</div><div class="bbb-lbl">Standar Mutu</div></div>
            </div>
            <div class="bbb-pills">
              <div class="bbb-pill"><span class="pi">🔤</span> Pembinaan Bahasa</div>
              <div class="bbb-pill"><span class="pi">📖</span> Penelitian Sastra</div>
              <div class="bbb-pill"><span class="pi">🌿</span> Pelestarian Budaya</div>
              <div class="bbb-pill"><span class="pi">🎓</span> Penyuluhan &amp; Literasi</div>
              <div class="bbb-pill"><span class="pi">🤝</span> Kemitraan Pendidikan</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── BBPMP ABOUT (original, kept below) ─────────────────
    st.markdown(f"""
    <div class="kmd-about">
      <div class="about-inner">
        <div class="about-icon">🏛️</div>
        <div class="about-body">
          <div class="about-badge"><span>✦ Unit Induk</span></div>
          <div class="about-title">Balai Besar Penjaminan Mutu Pendidikan<br/>Provinsi Bali</div>
          <div class="about-desc">
            <strong>BBPMP Provinsi Bali</strong> adalah unit pelaksana teknis di bawah
            <strong>Kementerian Pendidikan Dasar dan Menengah (Kemendikdasmen)</strong>
            yang mengemban tugas strategis dalam <strong>penjaminan mutu pendidikan</strong>
            di seluruh wilayah Provinsi Bali. Lembaga ini menjalankan fungsi fasilitasi,
            pendampingan, supervisi, dan monitoring kepada satuan pendidikan serta dinas
            pendidikan kabupaten/kota — guna mewujudkan <strong>pendidikan berkualitas</strong>
            yang merata, inklusif, dan berkarakter Pancasila sesuai
            <strong>Standar Nasional Pendidikan (SNP)</strong>.
          </div>
          <div class="about-stats">
            <div class="about-stat"><div class="about-num">9</div><div class="about-lbl">Kab / Kota</div></div>
            <div class="about-stat"><div class="about-num">5K+</div><div class="about-lbl">Sekolah</div></div>
            <div class="about-stat"><div class="about-num">2026</div><div class="about-lbl">Tahun RDB</div></div>
            <div class="about-stat"><div class="about-num">SNP</div><div class="about-lbl">Standar Mutu</div></div>
            <div class="about-stat"><div class="about-num">RDB</div><div class="about-lbl">Rapat Dinas</div></div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── STATS SECTION ─────────────────────────────────────────
    ph("📊", "Dashboard Statistik Peserta RDB",
       "Ringkasan data & visualisasi peserta secara real-time", "OVERVIEW")

    data = get_all_data()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("👥 Total Peserta",   len(df))
        with col2: st.metric("📚 Total Jenjang",   df["Jenjang"].nunique())
        with col3: st.metric("🏛️ Total Instansi",  df["Instansi"].nunique())
        with col4: st.metric("📍 Total Kabupaten", df["Kabupaten"].nunique())

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            sec("Distribusi per Jenjang")
            jc = df["Jenjang"].value_counts()
            fig = px.pie(values=jc.values, names=jc.index, hole=0.48, color_discrete_sequence=COLORS)
            fig.update_traces(textposition="inside", textinfo="percent+label",
                              textfont_size=12, textfont_color=NAVY_900,
                              marker=dict(line=dict(color=NAVY_800, width=2)))
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        with col2:
            sec("Peserta per Tahun")
            tc = df["Tahun"].value_counts().sort_index()
            fig = px.bar(x=tc.index, y=tc.values, labels={"x":"Tahun","y":"Jumlah Peserta"})
            fig.update_traces(marker_color=GOLD_500, marker_line_color=NAVY_800,
                              marker_line_width=1.5, opacity=0.92)
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            sec("Distribusi per Kabupaten")
            kc = df["Kabupaten"].value_counts()
            fig = px.bar(x=kc.values, y=kc.index, orientation="h", labels={"x":"Jumlah","y":"Kabupaten"})
            fig.update_traces(marker_color=GOLD_500, opacity=0.92)
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        with col2:
            sec("Top 10 Instansi")
            ti = df["Instansi"].value_counts().head(10)
            fig = px.bar(x=ti.values, y=ti.index, orientation="h", labels={"x":"Jumlah Peserta","y":"Instansi"})
            fig.update_traces(marker_color=GOLD_400, opacity=0.92)
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        st.markdown("---")
        sec("Data Terbaru (10 Terakhir)")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)

    else:
        st.info("📭 Belum ada data. Silakan tambah data terlebih dahulu.")

# ==================== FILTER DATA ====================
elif menu == "🔍 Filter Data":
    ph("🔍", "Filter & Cari Data Peserta", "Temukan data dengan pencarian dan filter yang presisi", "SEARCH")
    data = get_all_data()
    if data:
        df = pd.DataFrame(data, columns=["ID","Nama","Jenjang","Instansi","Kabupaten","Tahun"])
        sec("🎯 Parameter Filter")
        col1,col2,col3,col4 = st.columns(4)
        with col1: search_nama   = st.text_input("🔎 Cari Nama", placeholder="Ketik nama...")
        with col2:
            all_j = ["Semua"] + sorted(df["Jenjang"].unique().tolist())
            filter_jenjang = st.selectbox("📚 Jenjang", options=all_j)
        with col3:
            all_k = ["Semua"] + sorted(df["Kabupaten"].unique().tolist())
            filter_kabupaten = st.selectbox("📍 Kabupaten", options=all_k)
        with col4:
            filter_tahun = st.selectbox("📅 Tahun",
                options=["Semua"] + sorted(df["Tahun"].unique().tolist(), reverse=True))

        df_f = df.copy()
        if search_nama:    df_f = df_f[df_f["Nama"].str.contains(search_nama, case=False, na=False)]
        if filter_jenjang   != "Semua": df_f = df_f[df_f["Jenjang"]   == filter_jenjang]
        if filter_kabupaten != "Semua": df_f = df_f[df_f["Kabupaten"] == filter_kabupaten]
        if filter_tahun     != "Semua": df_f = df_f[df_f["Tahun"]     == filter_tahun]

        st.markdown("---")
        st.info(f"📊 Menampilkan **{len(df_f)}** dari **{len(df)}** data")
        if len(df_f) > 0:
            st.dataframe(df_f, use_container_width=True, hide_index=True)
            csv = df_f.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Hasil Filter (CSV)", csv,
                file_name=f"filter_peserta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv", type="primary")
        else:
            st.warning("❌ Tidak ada data yang sesuai dengan filter.")
    else:
        st.info("📭 Belum ada data.")

# ==================== TAMBAH DATA ====================
elif menu == "➕ Tambah Data":
    ph("➕", "Tambah Data Peserta Baru", "Input data peserta baru ke dalam sistem database", "NEW ENTRY")
    with st.form("form_tambah", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("👤 Nama Lengkap*", placeholder="Contoh: Nyoman Hendrajaya, S.Pd")
            jenjang_type = st.radio("Tipe Jenjang", ["Pilih dari list","Ketik manual"], horizontal=True)
            if jenjang_type == "Pilih dari list":
                jenjang = st.selectbox("📚 Jenjang*", ["SD","SMP","SMA","SMK","TK","PAUD","Disdikpora"])
            else:
                jenjang = st.text_input("📚 Jenjang*", placeholder="Contoh: Disdikpora, DISDIK TABANAN")
            instansi = st.text_input("🏫 Instansi*", placeholder="Contoh: SMP N 3 DENPASAR")
        with col2:
            kabupaten = st.text_input("📍 Kabupaten/Kota*", placeholder="Contoh: Kota Denpasar")
            tahun = st.number_input("📅 Tahun*", min_value=2000, max_value=2100, value=2024, step=1)
        submitted = st.form_submit_button("💾 Simpan Data", type="primary", use_container_width=True)
        if submitted:
            valid, msg = validate_input(nama, jenjang, instansi, kabupaten, tahun)
            if not valid:
                st.error(f"❌ {msg}")
            else:
                with st.spinner("Menyimpan data..."):
                    if tambah_data(nama, jenjang, instansi, kabupaten, tahun):
                        st.success(f"✅ Data **{nama}** berhasil disimpan!")
                        st.balloons()
                    else:
                        st.error("❌ Gagal menyimpan data.")

# ==================== EDIT DATA ====================
elif menu == "✏️ Edit Data":
    ph("✏️", "Edit Data Peserta", "Muat data berdasarkan ID kemudian perbarui informasinya", "EDIT")
    data = get_all_data()
    if data:
        df = pd.DataFrame(data, columns=["ID","Nama","Jenjang","Instansi","Kabupaten","Tahun"])
        sec("🔍 Cari Data")
        search = st.text_input("🔎 Cari berdasarkan Nama", placeholder="Ketik nama...")
        df_s = df[df["Nama"].str.contains(search, case=False, na=False)] if search else df.head(20)
        st.dataframe(df_s, use_container_width=True, hide_index=True)
        st.markdown("---")
        sec("✏️ Form Edit")
        id_edit = st.number_input("🆔 Masukkan ID yang ingin diedit", min_value=1, step=1)
        if st.button("📥 Load Data", type="secondary"):
            de = get_data_by_id(id_edit)
            if de:
                st.session_state["edit_data"] = de
                st.success(f"✅ Data ID {id_edit} berhasil dimuat!")
            else:
                st.error(f"❌ Data dengan ID {id_edit} tidak ditemukan.")
        if "edit_data" in st.session_state:
            de = st.session_state["edit_data"]
            with st.form("form_edit"):
                col1, col2 = st.columns(2)
                with col1:
                    nama = st.text_input("👤 Nama", value=de["nama"])
                    jc = de["jenjang"]
                    idx_r = 0 if jc in ["SD","SMP","SMA","SMK","TK","PAUD","Disdikpora"] else 1
                    jenjang_type = st.radio("Tipe Jenjang", ["Pilih dari list","Ketik manual"], horizontal=True, index=idx_r)
                    if jenjang_type == "Pilih dari list":
                        try:   idx = ["SD","SMP","SMA","SMK","TK","PAUD","Disdikpora"].index(jc)
                        except: idx = 0
                        jenjang = st.selectbox("📚 Jenjang", ["SD","SMP","SMA","SMK","TK","PAUD","Disdikpora"], index=idx)
                    else:
                        jenjang = st.text_input("📚 Jenjang", value=jc)
                    instansi = st.text_input("🏫 Instansi", value=de["instansi"])
                with col2:
                    kabupaten = st.text_input("📍 Kabupaten", value=de["kabupaten"])
                    tahun = st.number_input("📅 Tahun", value=de["tahun"], min_value=2000, max_value=2100)
                if st.form_submit_button("💾 Update Data", type="primary", use_container_width=True):
                    if update_data(id_edit, nama, jenjang, instansi, kabupaten, tahun):
                        st.success(f"✅ Data ID {id_edit} berhasil diupdate!")
                        del st.session_state["edit_data"]
                        st.rerun()
                    else:
                        st.error("❌ Gagal update data.")
    else:
        st.info("📭 Belum ada data.")

# ==================== HAPUS DATA ====================
elif menu == "🗑️ Hapus Data":
    ph("🗑️", "Hapus Data Peserta", "Penghapusan bersifat permanen — pastikan ID sudah benar", "DELETE")
    data = get_all_data()
    if data:
        df = pd.DataFrame(data, columns=["ID","Nama","Jenjang","Instansi","Kabupaten","Tahun"])
        st.warning("⚠️ **Perhatian:** Penghapusan data bersifat permanen dan tidak dapat dibatalkan!")
        sec("🔍 Cari Data yang Akan Dihapus")
        search = st.text_input("🔎 Cari berdasarkan Nama", placeholder="Ketik nama...")
        df_s = df[df["Nama"].str.contains(search, case=False, na=False)] if search else df.head(20)
        st.dataframe(df_s, use_container_width=True, hide_index=True)
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1: id_delete = st.number_input("🆔 Masukkan ID yang ingin dihapus", min_value=1, step=1)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ HAPUS", type="primary", use_container_width=True):
                dc = get_data_by_id(id_delete)
                if dc:
                    if delete_data(id_delete):
                        st.success(f"✅ Data **{dc['nama']}** (ID:{id_delete}) berhasil dihapus!")
                        st.rerun()
                    else: st.error("❌ Gagal menghapus data.")
                else: st.error(f"❌ Data ID {id_delete} tidak ditemukan.")
    else:
        st.info("📭 Belum ada data.")

# ==================== REKAPAN ====================
elif menu == "📊 Rekapan":
    ph("📊", "Rekapan Statistik Lengkap", "Statistik komprehensif per kategori beserta unduhan laporan", "REPORT")
    data = get_all_data()
    if data:
        df = pd.DataFrame(data, columns=["ID","Nama","Jenjang","Instansi","Kabupaten","Tahun"])
        sec("📈 Ringkasan Umum")
        col1,col2,col3,col4 = st.columns(4)
        with col1: st.metric("Total Peserta",    len(df))
        with col2: st.metric("Jenjang Berbeda",  df["Jenjang"].nunique())
        with col3: st.metric("Instansi Berbeda", df["Instansi"].nunique())
        with col4: st.metric("Kabupaten Berbeda",df["Kabupaten"].nunique())
        st.markdown("---")
        tab1,tab2,tab3,tab4 = st.tabs(["📚 Per Jenjang","📅 Per Tahun","📍 Per Kabupaten","🏫 Per Instansi"])
        with tab1:
            stats = statistik_per_jenjang()
            if stats:
                dfs = pd.DataFrame(stats, columns=["Jenjang","Jumlah"])
                c1,c2 = st.columns([1,2])
                with c1: st.dataframe(dfs, use_container_width=True, hide_index=True)
                with c2:
                    fig = px.bar(dfs, x="Jenjang", y="Jumlah")
                    fig.update_traces(marker_color=GOLD_500, opacity=0.92)
                    st.plotly_chart(style_plotly(fig), use_container_width=True)
        with tab2:
            stats = statistik_per_tahun()
            if stats:
                dfs = pd.DataFrame(stats, columns=["Tahun","Jumlah"])
                c1,c2 = st.columns([1,2])
                with c1: st.dataframe(dfs, use_container_width=True, hide_index=True)
                with c2:
                    fig = px.line(dfs, x="Tahun", y="Jumlah", markers=True)
                    fig.update_traces(line=dict(color=GOLD_500,width=3),
                                      marker=dict(color=GOLD_400,size=10,line=dict(color=NAVY_800,width=2)))
                    st.plotly_chart(style_plotly(fig), use_container_width=True)
        with tab3:
            stats = statistik_per_kabupaten()
            if stats:
                dfs = pd.DataFrame(stats, columns=["Kabupaten","Jumlah"])
                c1,c2 = st.columns([1,2])
                with c1: st.dataframe(dfs, use_container_width=True, hide_index=True)
                with c2:
                    fig = px.bar(dfs, y="Kabupaten", x="Jumlah", orientation="h")
                    fig.update_traces(marker_color=GOLD_500, opacity=0.92)
                    st.plotly_chart(style_plotly(fig), use_container_width=True)
        with tab4:
            ic = df["Instansi"].value_counts().reset_index()
            ic.columns = ["Instansi","Jumlah"]
            st.dataframe(ic, use_container_width=True, hide_index=True)
        st.markdown("---")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Laporan Lengkap (CSV)", csv,
            file_name=f"laporan_rdb_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv", type="primary")
    else:
        st.info("📭 Belum ada data.")

# ==================== UPLOAD EXCEL ====================
elif menu == "📤 Upload Excel":
    ph("📤", "Upload Data dari Excel / CSV", "Unggah data massal dengan validasi otomatis sebelum disimpan", "IMPORT")
    st.markdown("""
    ### 📋 Format File Excel
    File harus memiliki kolom: **nama**, **jenjang**, **instansi**, **kabupaten**, **tahun**
    """)
    tdf = pd.DataFrame({
        "nama":["Nyoman Hendrajaya, S.Pd","Kadek Astuyasa, S.Pd."],
        "jenjang":["SMP","Disdikpora"], "instansi":["SMP N 3 DENPASAR","DISDIK TABANAN"],
        "kabupaten":["Kota Denpasar","Kabupaten Tabanan"], "tahun":[2022,2022]
    })
    st.download_button("📥 Download Template Excel", tdf.to_csv(index=False).encode("utf-8"),
        file_name="template_upload_rdb.csv", mime="text/csv", type="secondary")
    st.markdown("---")
    uploaded_file = st.file_uploader("📂 Pilih file Excel atau CSV", type=["xlsx","xls","csv"])
    if uploaded_file:
        try:
            dfu = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            st.success(f"✅ File berhasil dibaca! Total: {len(dfu)} baris")
            dfu.columns = dfu.columns.str.lower().str.strip()
            st.info(f"📋 Kolom terdeteksi: {', '.join(dfu.columns.tolist())}")
            sec("👀 Preview Data")
            st.dataframe(dfu.head(10), use_container_width=True)
            required_cols = ["nama","jenjang","instansi","kabupaten","tahun"]
            missing = []
            for col in required_cols:
                if col not in dfu.columns:
                    sim = [c for c in dfu.columns if col in c or c in col]
                    if sim:
                        st.warning(f"⚠️ '{col}' tidak ditemukan, menggunakan '{sim[0]}'")
                        dfu.rename(columns={sim[0]:col}, inplace=True)
                    else: missing.append(col)
            if missing:
                st.error(f"❌ Kolom tidak ditemukan: {', '.join(missing)}")
            else:
                st.success("✅ Semua kolom tersedia!")
                dfu = dfu[required_cols].copy()
                for col in ["nama","jenjang","instansi","kabupaten"]:
                    dfu[col] = dfu[col].astype(str).str.strip()
                dfu["tahun"] = pd.to_numeric(dfu["tahun"], errors="coerce").fillna(0).astype(int)
                sec("📊 Hasil Validasi")
                c1,c2,c3,c4 = st.columns(4)
                null_count  = dfu[required_cols].isnull().sum().sum()
                duplicates  = dfu.duplicated(subset=["nama","tahun"]).sum()
                invalid_t   = (dfu["tahun"]<2000).sum()+(dfu["tahun"]>2100).sum()
                with c1: st.metric("Data Kosong", null_count, delta="harus 0" if null_count>0 else "✓", delta_color="inverse")
                with c2: st.metric("Jenjang Unik", dfu["jenjang"].nunique())
                with c3: st.metric("Duplikat", duplicates, delta="harus 0" if duplicates>0 else "✓", delta_color="inverse")
                with c4: st.metric("Tahun Valid", f"{len(dfu)-invalid_t}/{len(dfu)}")
                if null_count>0: st.warning("⚠️ Data kosong:"); st.dataframe(dfu[dfu.isnull().any(axis=1)], use_container_width=True)
                if duplicates>0: st.warning("⚠️ Duplikat:"); st.dataframe(dfu[dfu.duplicated(subset=["nama","tahun"],keep=False)], use_container_width=True)
                uj = dfu["jenjang"].unique().tolist()
                st.info(f"📚 Jenjang: {', '.join(uj[:10])}{'...' if len(uj)>10 else ''}")
                st.markdown("---")
                cc1,cc2 = st.columns([3,1])
                with cc1: sec("📤 Upload ke Database"); st.info(f"Siap upload **{len(dfu)}** data")
                with cc2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    upload_btn = st.button("📤 UPLOAD", type="primary", use_container_width=True)
                if upload_btn:
                    if null_count>0: st.error("❌ Masih ada data kosong!")
                    elif invalid_t>0: st.error("❌ Tahun tidak valid!")
                    else:
                        with st.spinner("⏳ Mengupload..."):
                            rows = dfu[required_cols].to_dict("records")
                            pb = st.progress(0); st_txt = st.empty()
                            ok=0; fail=0
                            for i,r in enumerate(rows):
                                if tambah_data(r["nama"],r["jenjang"],r["instansi"],r["kabupaten"],r["tahun"]): ok+=1
                                else: fail+=1
                                pb.progress((i+1)/len(rows)); st_txt.text(f"Uploading... {i+1}/{len(rows)}")
                            pb.empty(); st_txt.empty()
                            if ok==len(rows): st.success(f"🎉 Berhasil upload {ok} data!"); st.balloons()
                            elif ok>0: st.warning(f"⚠️ Berhasil:{ok} | Gagal:{fail}")
                            else: st.error("❌ Gagal upload semua data.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Pastikan file tidak corrupt dan format sesuai template")
