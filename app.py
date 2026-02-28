import os
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ===== DEBUG SUPABASE (SEMENTARA) =====
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
st.write("DEBUG SUPABASE_URL:", SUPABASE_URL)
# =====================================

# Import fungsi CRUD (TIDAK DIUBAH)
from crud import (
    tambah_data, get_all_data, get_data_by_id,
    update_data, delete_data,
    statistik_per_tahun, statistik_per_jenjang,
    statistik_per_kabupaten, bulk_insert
)
from validation import validate_input

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="RDB BBP Bali 2026",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== COLOR PALETTE — KEMENDIKDASMEN OFFICIAL ====================
# Diambil langsung dari screenshot kemendikdasmen.go.id
NAVY_900  = "#060f1e"   # Terdalam — sidebar background
NAVY_800  = "#0a1628"   # Background utama header (dominant)
NAVY_700  = "#0d1f3c"   # Gradient tengah
NAVY_600  = "#0e2d5a"   # Gradient bawah / card bg
NAVY_500  = "#1a3d72"   # Hover states
NAVY_400  = "#1e4d8c"   # Border accent
GOLD_500  = "#f5c518"   # Kuning emas utama (Kemen"dik"dasmen)
GOLD_400  = "#ffd740"   # Gold terang
GOLD_300  = "#ffe57a"   # Gold muda
WHITE     = "#ffffff"
MUTED     = "#94a3b8"   # Teks sekunder
BORDER    = "rgba(255,255,255,0.10)"
BORDER_GOLD = "rgba(245,197,24,0.30)"

# Logo Kemendikdasmen (URL resmi)
LOGO_URL = "https://kemendikdasmen.go.id/web/image/res.company/1/logo/unique_id"

st.markdown(f"""
<style>
/* ================================================================
   KEMENDIKDASMEN PREMIUM DESIGN SYSTEM v2
   Dominan: Dark Navy (#0a1628) + Gold (#f5c518)
   Referensi: kemendikdasmen.go.id
   ================================================================ */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

:root {{
  --navy-900: {NAVY_900};
  --navy-800: {NAVY_800};
  --navy-700: {NAVY_700};
  --navy-600: {NAVY_600};
  --navy-500: {NAVY_500};
  --gold:     {GOLD_500};
  --gold-l:   {GOLD_400};
  --white:    {WHITE};
  --muted:    {MUTED};
  --border:   {BORDER};
  --bg:       {NAVY_800};
}}

/* ── Base ───────────────────────────────────────────────────── */
html, body {{
  background: {NAVY_800} !important;
  font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif !important;
}}

[data-testid="stAppViewContainer"] {{
  background: linear-gradient(160deg, {NAVY_800} 0%, {NAVY_700} 55%, {NAVY_900} 100%) !important;
  min-height: 100vh;
}}

[data-testid="stMain"] {{
  background: transparent !important;
}}

.block-container {{
  padding-top: 0 !important;
  padding-bottom: 3rem;
  max-width: 1500px;
}}

h1, h2, h3, h4, h5 {{
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 800 !important;
  color: {WHITE} !important;
}}

p, span, div, label, li {{
  font-family: 'Plus Jakarta Sans', sans-serif;
}}

/* ── TOP NAVBAR ─────────────────────────────────────────────── */
.kmd-navbar {{
  background: linear-gradient(90deg, {NAVY_900} 0%, {NAVY_800} 45%, {NAVY_700} 100%);
  border-bottom: 1px solid {BORDER_GOLD};
  margin: -1rem -1rem 0 -1rem;
  padding: 0 30px;
  display: flex;
  align-items: center;
  gap: 16px;
  height: 78px;
  box-shadow: 0 4px 40px rgba(0,0,0,.60);
  position: relative;
  overflow: hidden;
  z-index: 100;
}}

.kmd-navbar::before {{
  content:'';
  position:absolute; top:0; left:0; right:0;
  height:2px;
  background: linear-gradient(90deg, transparent 0%, {GOLD_500} 30%, {GOLD_400} 60%, transparent 100%);
  opacity:.70;
}}

.kmd-navbar::after {{
  content:'';
  position:absolute; bottom:0; left:0; right:0;
  height:1px;
  background: linear-gradient(90deg, transparent, rgba(245,197,24,.40), transparent);
}}

.kmd-nb-logo {{
  height: 50px; width: auto;
  object-fit: contain;
  filter: brightness(1.05) drop-shadow(0 2px 8px rgba(245,197,24,.20));
  flex-shrink: 0;
}}

.kmd-nb-brand {{
  font-size: 21px;
  font-weight: 900;
  letter-spacing: -.3px;
  flex-shrink: 0;
}}

.kmd-nb-brand .k {{ color: {WHITE}; }}
.kmd-nb-brand .d {{ color: {GOLD_500}; text-shadow: 0 0 20px rgba(245,197,24,.50); }}
.kmd-nb-brand .s {{ color: {WHITE}; }}

.kmd-nb-sep {{
  width: 1px; height: 38px;
  background: linear-gradient(180deg, transparent, rgba(255,255,255,.18), transparent);
  margin: 0 6px;
}}

.kmd-nb-sub {{
  font-size: 11px;
  color: {MUTED};
  font-weight: 500;
  line-height: 1.5;
}}

.kmd-nb-right {{
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 14px;
}}

.kmd-nb-date {{
  text-align: right;
  font-size: 11px;
  color: {MUTED};
  font-weight: 600;
  line-height: 1.6;
}}

.kmd-nb-live {{
  background: linear-gradient(135deg, {GOLD_500}, {GOLD_400});
  color: {NAVY_900};
  font-size: 10px;
  font-weight: 900;
  padding: 5px 14px;
  border-radius: 999px;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  box-shadow: 0 4px 16px rgba(245,197,24,.45);
  white-space: nowrap;
}}

/* ── Page Header ────────────────────────────────────────────── */
.kmd-ph {{
  background: linear-gradient(135deg,
    rgba(255,255,255,.035) 0%,
    rgba(245,197,24,.05) 100%);
  border: 1px solid rgba(255,255,255,.08);
  border-left: 4px solid {GOLD_500};
  border-radius: 18px;
  padding: 17px 24px;
  margin: 20px 0 22px 0;
  display: flex;
  align-items: center;
  gap: 16px;
  backdrop-filter: blur(16px);
  box-shadow: 0 8px 32px rgba(0,0,0,.25),
              inset 0 1px 0 rgba(255,255,255,.04);
}}

.kmd-ph-icon {{
  width: 52px; height: 52px;
  background: linear-gradient(135deg, {GOLD_500} 0%, {GOLD_400} 100%);
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
  flex-shrink: 0;
  box-shadow: 0 6px 22px rgba(245,197,24,.35);
}}

.kmd-ph-title {{
  font-size: 19px;
  font-weight: 900;
  color: {WHITE};
  line-height: 1.2;
}}

.kmd-ph-sub {{
  font-size: 12px;
  color: {MUTED};
  margin-top: 3px;
  font-weight: 500;
}}

.kmd-ph-tag {{
  margin-left: auto;
  background: rgba(245,197,24,.10);
  border: 1px solid {BORDER_GOLD};
  color: {GOLD_500};
  font-size: 9px;
  font-weight: 900;
  padding: 5px 12px;
  border-radius: 999px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}}

/* ── Section title ──────────────────────────────────────────── */
.kmd-sec {{
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  font-weight: 800;
  color: {WHITE};
  margin: 8px 0 16px 0;
}}

.kmd-sec::before {{
  content:'';
  display:inline-block;
  width:4px; height:20px;
  background: linear-gradient(180deg, {GOLD_500}, {GOLD_400});
  border-radius: 4px;
  flex-shrink: 0;
}}

/* ── Sidebar ────────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
  background: {NAVY_900} !important;
  border-right: 1px solid rgba(245,197,24,.12) !important;
}}

[data-testid="stSidebar"] > div:first-child {{
  background: {NAVY_900} !important;
}}

.kmd-sb-hdr {{
  background: linear-gradient(145deg, rgba(14,45,90,.90) 0%, {NAVY_900} 100%);
  border: 1px solid {BORDER_GOLD};
  border-radius: 18px;
  padding: 20px 16px;
  margin-bottom: 6px;
  position: relative;
  overflow: hidden;
}}

.kmd-sb-hdr::before {{
  content:'';
  position:absolute; top:-50px; right:-50px;
  width:150px; height:150px; border-radius:50%;
  background: radial-gradient(circle, rgba(245,197,24,.10), transparent 70%);
}}

.kmd-sb-hdr::after {{
  content:'';
  position:absolute; bottom:0; left:10%; right:10%;
  height:1px;
  background: linear-gradient(90deg, transparent, {GOLD_500}, transparent);
  opacity:.35;
}}

.kmd-sb-logo-box {{
  width:58px; height:58px;
  background: rgba(255,255,255,.06);
  border: 1px solid {BORDER_GOLD};
  border-radius: 16px;
  display:flex; align-items:center; justify-content:center;
  margin-bottom: 14px;
  box-shadow: 0 4px 18px rgba(245,197,24,.12);
  overflow: hidden;
}}

.kmd-sb-logo-box img {{
  width:44px; height:44px;
  object-fit: contain;
  filter: brightness(1.1);
}}

.kmd-sb-title {{
  font-size:15px; font-weight:900; color:{WHITE}; line-height:1.2; margin-bottom:4px;
}}

.kmd-sb-sub {{
  font-size:11px; color:{MUTED}; font-weight:500; line-height:1.5;
}}

.kmd-sb-date {{
  margin-top:12px; padding-top:10px;
  border-top:1px solid rgba(255,255,255,.08);
  font-size:11px; color:rgba(245,197,24,.65); font-weight:600;
}}

.kmd-nav-lbl {{
  font-size:10px; font-weight:800;
  letter-spacing:2px; text-transform:uppercase;
  color:rgba(245,197,24,.45); padding:0 4px;
  margin:14px 0 6px 0;
}}

/* Nav radio pills */
div[role="radiogroup"] > label {{
  background: rgba(255,255,255,.025) !important;
  border: 1px solid rgba(255,255,255,.07) !important;
  border-radius: 13px !important;
  padding: 10px 13px !important;
  margin: 3px 0 !important;
  cursor: pointer;
  transition: all .20s cubic-bezier(.4,0,.2,1) !important;
  font-weight: 600 !important;
  color: {MUTED} !important;
}}

div[role="radiogroup"] > label:hover {{
  border-color: rgba(245,197,24,.38) !important;
  background: rgba(245,197,24,.07) !important;
  color: {GOLD_500} !important;
  transform: translateX(4px) !important;
  box-shadow: 4px 0 16px rgba(245,197,24,.08) !important;
}}

div[role="radiogroup"] input:checked + div {{
  color: {GOLD_500} !important;
  font-weight: 800 !important;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {{
  color: {MUTED};
}}

.kmd-sb-foot {{
  background: rgba(255,255,255,.025);
  border: 1px solid rgba(255,255,255,.07);
  border-radius: 14px;
  padding: 13px;
  text-align: center;
  margin-top: 8px;
}}

/* ── Metric Cards ───────────────────────────────────────────── */
[data-testid="stMetric"] {{
  background: linear-gradient(145deg,
    rgba(255,255,255,.04) 0%,
    rgba(245,197,24,.045) 100%) !important;
  border: 1px solid rgba(255,255,255,.08) !important;
  border-top: 3px solid {GOLD_500} !important;
  border-radius: 18px !important;
  padding: 18px 20px !important;
  box-shadow: 0 8px 30px rgba(0,0,0,.28),
              inset 0 1px 0 rgba(255,255,255,.04) !important;
  transition: transform .22s ease, box-shadow .22s ease;
}}

[data-testid="stMetric"]:hover {{
  transform: translateY(-5px) !important;
  box-shadow: 0 16px 42px rgba(0,0,0,.38),
              0 0 0 1px rgba(245,197,24,.18) !important;
}}

[data-testid="stMetricLabel"] > div {{
  color: {MUTED} !important;
  font-weight: 700 !important;
  font-size: 11px !important;
  letter-spacing: .6px;
  text-transform: uppercase;
}}

[data-testid="stMetricValue"] > div {{
  color: {GOLD_500} !important;
  font-weight: 900 !important;
  font-size: 32px !important;
  letter-spacing: -1px;
  text-shadow: 0 0 30px rgba(245,197,24,.25);
}}

/* ── Generic Card/Container ─────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {{
  background: rgba(255,255,255,.025) !important;
  border: 1px solid rgba(255,255,255,.07) !important;
  border-radius: 20px !important;
  box-shadow: 0 10px 36px rgba(0,0,0,.28) !important;
  backdrop-filter: blur(10px);
}}

/* ── Buttons ────────────────────────────────────────────────── */
.stButton > button {{
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 800 !important;
  border-radius: 12px !important;
  padding: 0.55rem 1.3rem !important;
  transition: all .20s cubic-bezier(.4,0,.2,1) !important;
  letter-spacing: .3px;
}}

.stButton > button[kind="primary"] {{
  background: linear-gradient(135deg, {GOLD_500} 0%, {GOLD_400} 100%) !important;
  color: {NAVY_900} !important;
  border: none !important;
  box-shadow: 0 6px 22px rgba(245,197,24,.38) !important;
}}

.stButton > button[kind="primary"]:hover {{
  box-shadow: 0 12px 32px rgba(245,197,24,.55) !important;
  transform: translateY(-3px) !important;
  filter: brightness(1.06);
}}

.stButton > button[kind="secondary"] {{
  background: rgba(245,197,24,.06) !important;
  color: {GOLD_500} !important;
  border: 1.5px solid {BORDER_GOLD} !important;
}}

.stButton > button[kind="secondary"]:hover {{
  background: rgba(245,197,24,.12) !important;
  border-color: {GOLD_500} !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 22px rgba(245,197,24,.18) !important;
}}

/* ── Inputs ─────────────────────────────────────────────────── */
input, textarea {{
  background: rgba(255,255,255,.05) !important;
  border: 1.5px solid rgba(255,255,255,.11) !important;
  border-radius: 12px !important;
  color: {WHITE} !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  transition: border-color .18s ease, box-shadow .18s ease !important;
}}

input:focus, textarea:focus {{
  border-color: {GOLD_500} !important;
  box-shadow: 0 0 0 3px rgba(245,197,24,.14) !important;
  background: rgba(255,255,255,.07) !important;
}}

input::placeholder, textarea::placeholder {{
  color: rgba(148,163,184,.45) !important;
}}

[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stRadio"] > label,
[data-testid="stFileUploader"] label {{
  color: rgba(148,163,184,.85) !important;
  font-weight: 700 !important;
  font-size: 11px !important;
  letter-spacing: .5px;
  text-transform: uppercase;
}}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {{
  background: rgba(255,255,255,.05) !important;
  border: 1.5px solid rgba(255,255,255,.11) !important;
  border-radius: 12px !important;
  color: {WHITE} !important;
  transition: border-color .18s ease !important;
}}

[data-testid="stSelectbox"] > div > div:focus-within {{
  border-color: {GOLD_500} !important;
  box-shadow: 0 0 0 3px rgba(245,197,24,.14) !important;
}}

/* Number input */
[data-testid="stNumberInput"] > div {{
  background: rgba(255,255,255,.05) !important;
  border: 1.5px solid rgba(255,255,255,.11) !important;
  border-radius: 12px !important;
}}

/* ── Dataframe ──────────────────────────────────────────────── */
[data-testid="stDataFrame"] {{
  border-radius: 16px !important;
  overflow: hidden !important;
  border: 1px solid rgba(255,255,255,.08) !important;
  box-shadow: 0 8px 28px rgba(0,0,0,.28) !important;
}}

/* ── Tabs ───────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {{
  background: rgba(255,255,255,.03) !important;
  border: 1px solid rgba(255,255,255,.07) !important;
  border-radius: 14px;
  padding: 4px;
  gap: 4px;
}}

[data-testid="stTabs"] button {{
  font-weight: 700 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  border-radius: 10px !important;
  color: {MUTED} !important;
  transition: all .18s ease !important;
}}

[data-testid="stTabs"] button:hover {{
  color: {GOLD_500} !important;
  background: rgba(245,197,24,.07) !important;
}}

[data-testid="stTabs"] button[aria-selected="true"] {{
  background: linear-gradient(135deg,
    rgba(245,197,24,.18), rgba(245,197,24,.08)) !important;
  color: {GOLD_500} !important;
  font-weight: 900 !important;
  border: 1px solid {BORDER_GOLD} !important;
}}

/* ── Alerts ─────────────────────────────────────────────────── */
[data-testid="stAlert"] {{
  background: rgba(255,255,255,.03) !important;
  border: 1px solid rgba(255,255,255,.07) !important;
  border-left: 4px solid {GOLD_500} !important;
  border-radius: 14px !important;
  color: {WHITE} !important;
}}

[data-testid="stAlert"] p {{ color: {WHITE} !important; }}
div[role="alert"]         {{ color: {WHITE} !important; }}

/* ── File Uploader ──────────────────────────────────────────── */
[data-testid="stFileUploaderDropzone"] {{
  background: rgba(255,255,255,.025) !important;
  border: 2px dashed {BORDER_GOLD} !important;
  border-radius: 18px !important;
  transition: all .20s ease !important;
}}

[data-testid="stFileUploaderDropzone"]:hover {{
  background: rgba(245,197,24,.05) !important;
  border-color: {GOLD_500} !important;
  box-shadow: 0 0 0 4px rgba(245,197,24,.07) !important;
}}

[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] p {{
  color: {MUTED} !important;
}}

/* ── Download Button ────────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {{
  border-radius: 12px !important;
  font-weight: 800 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}}

/* ── Progress bar ───────────────────────────────────────────── */
[data-testid="stProgressBar"] > div {{
  background: rgba(255,255,255,.08) !important;
  border-radius: 999px !important;
}}

[data-testid="stProgressBar"] > div > div {{
  background: linear-gradient(90deg, {GOLD_500}, {GOLD_400}) !important;
  border-radius: 999px !important;
  box-shadow: 0 0 12px rgba(245,197,24,.40);
}}

/* ── Divider ────────────────────────────────────────────────── */
hr {{
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg,
    transparent, rgba(255,255,255,.10), transparent) !important;
  margin: 22px 0 !important;
}}

/* ── Spinner ────────────────────────────────────────────────── */
.stSpinner > div {{
  border-top-color: {GOLD_500} !important;
}}

/* ── Markdown Text ──────────────────────────────────────────── */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {{
  color: {MUTED} !important;
}}

[data-testid="stMarkdownContainer"] strong {{
  color: {WHITE} !important; font-weight: 800;
}}

[data-testid="stMarkdownContainer"] h3 {{
  color: {WHITE} !important; font-weight: 800 !important;
}}

/* ── Form ───────────────────────────────────────────────────── */
[data-testid="stForm"] {{
  background: rgba(255,255,255,.02) !important;
  border: 1px solid rgba(255,255,255,.07) !important;
  border-radius: 20px !important;
  padding: 22px !important;
  box-shadow: 0 8px 34px rgba(0,0,0,.22) !important;
}}

/* ── Radio inside form ──────────────────────────────────────── */
[data-testid="stRadio"] > div > label {{
  color: {MUTED} !important;
  background: rgba(255,255,255,.03) !important;
  border: 1px solid rgba(255,255,255,.08) !important;
  border-radius: 10px !important;
  padding: 7px 12px !important;
  transition: all .16s ease !important;
}}

[data-testid="stRadio"] > div > label:hover {{
  color: {GOLD_500} !important;
  border-color: {BORDER_GOLD} !important;
  background: rgba(245,197,24,.06) !important;
}}

/* ── Scrollbar ──────────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {NAVY_900}; }}
::-webkit-scrollbar-thumb {{
  background: rgba(245,197,24,.28); border-radius: 999px;
}}
::-webkit-scrollbar-thumb:hover {{
  background: rgba(245,197,24,.50);
}}

/* ── Misc fixes ─────────────────────────────────────────────── */
[data-testid="stDecoration"] {{ display: none !important; }}
[data-testid="stHeader"]      {{ background: transparent !important; }}
</style>
""", unsafe_allow_html=True)

# ==================== PLOTLY DARK THEME ====================
def style_plotly(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=WHITE, family="Plus Jakarta Sans"),
        title_font=dict(color=WHITE, family="Plus Jakarta Sans"),
        margin=dict(l=20, r=20, t=44, b=20),
        legend=dict(
            bgcolor="rgba(6,15,30,.88)",
            bordercolor="rgba(255,255,255,.10)",
            borderwidth=1,
            font=dict(color=WHITE, size=12)
        )
    )
    fig.update_xaxes(
        showgrid=True, gridcolor="rgba(255,255,255,.06)",
        zeroline=False, tickfont=dict(color=MUTED, size=11),
        linecolor="rgba(255,255,255,.08)"
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="rgba(255,255,255,.06)",
        zeroline=False, tickfont=dict(color=MUTED, size=11),
        linecolor="rgba(255,255,255,.08)"
    )
    return fig

COLOR_SEQ = [GOLD_500, GOLD_400, "#e8a820", "#ffd740", "#b8860b", "#ffe57a", "#c8960c"]

# ==================== HELPER COMPONENTS ====================
def page_header(icon, title, subtitle, tag=""):
    tag_html = f'<div class="kmd-ph-tag">{tag}</div>' if tag else ""
    st.markdown(f"""
    <div class="kmd-ph">
      <div class="kmd-ph-icon">{icon}</div>
      <div>
        <div class="kmd-ph-title">{title}</div>
        <div class="kmd-ph-sub">{subtitle}</div>
      </div>
      {tag_html}
    </div>
    """, unsafe_allow_html=True)

def section(label):
    st.markdown(f'<div class="kmd-sec">{label}</div>', unsafe_allow_html=True)

# ==================== TOP NAVBAR ====================
st.markdown(f"""
<div class="kmd-navbar">

  <!-- Logo Kemendikdasmen -->
  <img
    src="{LOGO_URL}"
    class="kmd-nb-logo"
    alt="Kemendikdasmen"
    onerror="this.style.display='none'"
  />

  <!-- Brand text -->
  <div class="kmd-nb-brand">
    <span class="k">Kemen</span><span class="d">dik</span><span class="s">dasmen</span>
  </div>

  <div class="kmd-nb-sep"></div>

  <div class="kmd-nb-sub">
    Balai Besar Penjaminan Mutu Pendidikan<br/>
    Provinsi Bali &nbsp;•&nbsp; RDB 2026
  </div>

  <div class="kmd-nb-right">
    <div class="kmd-nb-date">
      {datetime.now().strftime('%A, %d %B')}<br/>
      <strong style="color:{WHITE};">{datetime.now().strftime('%Y')}</strong>
    </div>
    <div class="kmd-nb-live">● LIVE</div>
  </div>

</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown(f"""
    <div class="kmd-sb-hdr">
      <div class="kmd-sb-logo-box">
        <img src="{LOGO_URL}" alt="Logo Kemendikdasmen"
             onerror="this.outerHTML='<span style=\'font-size:28px\'>🏛️</span>'" />
      </div>
      <div class="kmd-sb-title">RDB BBP Bali 2026</div>
      <div class="kmd-sb-sub">
        Sistem Informasi Pendataan<br/>Peserta Rapat Dinas Bersama
      </div>
      <div class="kmd-sb-date">
        🗓️&nbsp; <strong>{datetime.now().strftime('%d %B %Y')}</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="kmd-nav-lbl">⬡ Navigasi</div>', unsafe_allow_html=True)

    menu = st.radio(
        "Menu",
        ["🏠 Dashboard", "🔍 Filter Data", "➕ Tambah Data",
         "✏️ Edit Data", "🗑️ Hapus Data", "📊 Rekapan", "📤 Upload Excel"],
        label_visibility="collapsed"
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kmd-sb-foot">
      <div style="font-size:9px;font-weight:900;letter-spacing:2px;text-transform:uppercase;
                  color:rgba(245,197,24,.40);margin-bottom:6px;">KEMENDIKDASMEN</div>
      <div style="font-size:11px;font-weight:800;color:{GOLD_500};line-height:1.4;">
        Dasar dan Menengah
      </div>
      <div style="font-size:10px;color:{MUTED};margin-top:5px;line-height:1.5;">
        BBPMP Provinsi Bali
      </div>
      <div style="margin-top:8px;font-size:10px;font-weight:700;
                  color:rgba(245,197,24,.30);">kemendikdasmen.go.id</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== DASHBOARD ====================
if menu == "🏠 Dashboard":
    page_header("🏠", "Dashboard Statistik RDB BBP Bali",
                "Ringkasan data & visualisasi peserta secara real-time", "OVERVIEW")

    data = get_all_data()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Total Peserta", len(df))
        with col2:
            st.metric("📚 Total Jenjang", df["Jenjang"].nunique())
        with col3:
            st.metric("🏛️ Total Instansi", df["Instansi"].nunique())
        with col4:
            st.metric("📍 Total Kabupaten", df["Kabupaten"].nunique())

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            section("Distribusi per Jenjang")
            jenjang_count = df["Jenjang"].value_counts()
            fig = px.pie(
                values=jenjang_count.values,
                names=jenjang_count.index,
                hole=0.48,
                color_discrete_sequence=COLOR_SEQ
            )
            fig.update_traces(
                textposition="inside", textinfo="percent+label",
                textfont_size=12, textfont_color=NAVY_900,
                marker=dict(line=dict(color=NAVY_800, width=2))
            )
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        with col2:
            section("Peserta per Tahun")
            tahun_count = df["Tahun"].value_counts().sort_index()
            fig = px.bar(
                x=tahun_count.index,
                y=tahun_count.values,
                labels={"x": "Tahun", "y": "Jumlah Peserta"},
            )
            fig.update_traces(
                marker_color=GOLD_500,
                marker_line_color=NAVY_800,
                marker_line_width=1.5,
                opacity=0.92
            )
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            section("Distribusi per Kabupaten")
            kab_count = df["Kabupaten"].value_counts()
            fig = px.bar(
                x=kab_count.values, y=kab_count.index, orientation="h",
                labels={"x": "Jumlah", "y": "Kabupaten"},
            )
            fig.update_traces(marker_color=GOLD_500, opacity=0.92)
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        with col2:
            section("Top 10 Instansi")
            top_inst = df["Instansi"].value_counts().head(10)
            fig = px.bar(
                x=top_inst.values, y=top_inst.index, orientation="h",
                labels={"x": "Jumlah Peserta", "y": "Instansi"},
            )
            fig.update_traces(marker_color=GOLD_400, opacity=0.92)
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        st.markdown("---")
        section("Data Terbaru (10 Terakhir)")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)

    else:
        st.info("📭 Belum ada data. Silakan tambah data terlebih dahulu.")

# ==================== FILTER DATA ====================
elif menu == "🔍 Filter Data":
    page_header("🔍", "Filter & Cari Data Peserta",
                "Temukan data dengan pencarian dan filter yang presisi", "SEARCH")

    data = get_all_data()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])

        section("🎯 Parameter Filter")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            search_nama = st.text_input("🔎 Cari Nama", placeholder="Ketik nama...")
        with col2:
            all_jenjang = ["Semua"] + sorted(df["Jenjang"].unique().tolist())
            filter_jenjang = st.selectbox("📚 Jenjang", options=all_jenjang)
        with col3:
            all_kabupaten = ["Semua"] + sorted(df["Kabupaten"].unique().tolist())
            filter_kabupaten = st.selectbox("📍 Kabupaten", options=all_kabupaten)
        with col4:
            filter_tahun = st.selectbox(
                "📅 Tahun",
                options=["Semua"] + sorted(df["Tahun"].unique().tolist(), reverse=True)
            )

        df_filtered = df.copy()
        if search_nama:
            df_filtered = df_filtered[df_filtered["Nama"].str.contains(search_nama, case=False, na=False)]
        if filter_jenjang != "Semua":
            df_filtered = df_filtered[df_filtered["Jenjang"] == filter_jenjang]
        if filter_kabupaten != "Semua":
            df_filtered = df_filtered[df_filtered["Kabupaten"] == filter_kabupaten]
        if filter_tahun != "Semua":
            df_filtered = df_filtered[df_filtered["Tahun"] == filter_tahun]

        st.markdown("---")
        st.info(f"📊 Menampilkan **{len(df_filtered)}** dari **{len(df)}** data")

        if len(df_filtered) > 0:
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            csv = df_filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Hasil Filter (CSV)",
                data=csv,
                file_name=f"filter_peserta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                type="primary"
            )
        else:
            st.warning("❌ Tidak ada data yang sesuai dengan filter.")
    else:
        st.info("📭 Belum ada data.")

# ==================== TAMBAH DATA ====================
elif menu == "➕ Tambah Data":
    page_header("➕", "Tambah Data Peserta Baru",
                "Input data peserta baru ke dalam sistem database", "NEW ENTRY")

    with st.form("form_tambah", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            nama = st.text_input("👤 Nama Lengkap*", placeholder="Contoh: Nyoman Hendrajaya, S.Pd")
            jenjang_type = st.radio("Tipe Jenjang", ["Pilih dari list", "Ketik manual"], horizontal=True)
            if jenjang_type == "Pilih dari list":
                jenjang = st.selectbox("📚 Jenjang*", ["SD", "SMP", "SMA", "SMK", "TK", "PAUD", "Disdikpora"])
            else:
                jenjang = st.text_input("📚 Jenjang*", placeholder="Contoh: Disdikpora, DISDIK TABANAN, dll")
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
    page_header("✏️", "Edit Data Peserta",
                "Muat data berdasarkan ID kemudian perbarui informasinya", "EDIT")

    data = get_all_data()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])

        section("🔍 Cari Data")
        search = st.text_input("🔎 Cari berdasarkan Nama", placeholder="Ketik nama...")

        if search:
            df_search = df[df["Nama"].str.contains(search, case=False, na=False)]
        else:
            df_search = df.head(20)

        st.dataframe(df_search, use_container_width=True, hide_index=True)

        st.markdown("---")
        section("✏️ Form Edit")

        id_edit = st.number_input("🆔 Masukkan ID yang ingin diedit", min_value=1, step=1)

        if st.button("📥 Load Data", type="secondary"):
            data_edit = get_data_by_id(id_edit)
            if data_edit:
                st.session_state["edit_data"] = data_edit
                st.success(f"✅ Data ID {id_edit} berhasil dimuat!")
            else:
                st.error(f"❌ Data dengan ID {id_edit} tidak ditemukan.")

        if "edit_data" in st.session_state:
            data_edit = st.session_state["edit_data"]

            with st.form("form_edit"):
                col1, col2 = st.columns(2)

                with col1:
                    nama = st.text_input("👤 Nama", value=data_edit["nama"])
                    jenjang_current = data_edit["jenjang"]
                    if jenjang_current in ["SD", "SMP", "SMA", "SMK", "TK", "PAUD", "Disdikpora"]:
                        jenjang_type = st.radio("Tipe Jenjang", ["Pilih dari list", "Ketik manual"], horizontal=True, index=0)
                    else:
                        jenjang_type = st.radio("Tipe Jenjang", ["Pilih dari list", "Ketik manual"], horizontal=True, index=1)

                    if jenjang_type == "Pilih dari list":
                        try:
                            idx = ["SD", "SMP", "SMA", "SMK", "TK", "PAUD", "Disdikpora"].index(jenjang_current)
                        except:
                            idx = 0
                        jenjang = st.selectbox("📚 Jenjang", ["SD", "SMP", "SMA", "SMK", "TK", "PAUD", "Disdikpora"], index=idx)
                    else:
                        jenjang = st.text_input("📚 Jenjang", value=jenjang_current)

                    instansi = st.text_input("🏫 Instansi", value=data_edit["instansi"])

                with col2:
                    kabupaten = st.text_input("📍 Kabupaten", value=data_edit["kabupaten"])
                    tahun = st.number_input("📅 Tahun", value=data_edit["tahun"], min_value=2000, max_value=2100)

                submitted = st.form_submit_button("💾 Update Data", type="primary", use_container_width=True)

                if submitted:
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
    page_header("🗑️", "Hapus Data Peserta",
                "Penghapusan bersifat permanen — pastikan ID yang dipilih sudah benar", "DELETE")

    data = get_all_data()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])

        st.warning("⚠️ **Perhatian:** Penghapusan data bersifat permanen dan tidak dapat dibatalkan!")

        section("🔍 Cari Data yang Akan Dihapus")
        search = st.text_input("🔎 Cari berdasarkan Nama", placeholder="Ketik nama...")

        if search:
            df_search = df[df["Nama"].str.contains(search, case=False, na=False)]
        else:
            df_search = df.head(20)

        st.dataframe(df_search, use_container_width=True, hide_index=True)

        st.markdown("---")
        col1, col2 = st.columns([3, 1])

        with col1:
            id_delete = st.number_input("🆔 Masukkan ID yang ingin dihapus", min_value=1, step=1)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ HAPUS", type="primary", use_container_width=True):
                data_check = get_data_by_id(id_delete)
                if data_check:
                    if delete_data(id_delete):
                        st.success(f"✅ Data **{data_check['nama']}** (ID: {id_delete}) berhasil dihapus!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal menghapus data.")
                else:
                    st.error(f"❌ Data dengan ID {id_delete} tidak ditemukan.")
    else:
        st.info("📭 Belum ada data.")

# ==================== REKAPAN ====================
elif menu == "📊 Rekapan":
    page_header("📊", "Rekapan Statistik Lengkap",
                "Statistik komprehensif per kategori beserta unduhan laporan resmi", "REPORT")

    data = get_all_data()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])

        section("📈 Ringkasan Umum")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Peserta", len(df))
        with col2:
            st.metric("Jenjang Berbeda", df["Jenjang"].nunique())
        with col3:
            st.metric("Instansi Berbeda", df["Instansi"].nunique())
        with col4:
            st.metric("Kabupaten Berbeda", df["Kabupaten"].nunique())

        st.markdown("---")
        tab1, tab2, tab3, tab4 = st.tabs(["📚 Per Jenjang", "📅 Per Tahun", "📍 Per Kabupaten", "🏫 Per Instansi"])

        with tab1:
            stats = statistik_per_jenjang()
            if stats:
                df_stats = pd.DataFrame(stats, columns=["Jenjang", "Jumlah"])
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(df_stats, use_container_width=True, hide_index=True)
                with col2:
                    fig = px.bar(df_stats, x="Jenjang", y="Jumlah")
                    fig.update_traces(marker_color=GOLD_500, opacity=0.92)
                    st.plotly_chart(style_plotly(fig), use_container_width=True)

        with tab2:
            stats = statistik_per_tahun()
            if stats:
                df_stats = pd.DataFrame(stats, columns=["Tahun", "Jumlah"])
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(df_stats, use_container_width=True, hide_index=True)
                with col2:
                    fig = px.line(df_stats, x="Tahun", y="Jumlah", markers=True)
                    fig.update_traces(
                        line=dict(color=GOLD_500, width=3),
                        marker=dict(color=GOLD_400, size=10,
                                    line=dict(color=NAVY_800, width=2))
                    )
                    st.plotly_chart(style_plotly(fig), use_container_width=True)

        with tab3:
            stats = statistik_per_kabupaten()
            if stats:
                df_stats = pd.DataFrame(stats, columns=["Kabupaten", "Jumlah"])
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(df_stats, use_container_width=True, hide_index=True)
                with col2:
                    fig = px.bar(df_stats, y="Kabupaten", x="Jumlah", orientation="h")
                    fig.update_traces(marker_color=GOLD_500, opacity=0.92)
                    st.plotly_chart(style_plotly(fig), use_container_width=True)

        with tab4:
            inst_count = df["Instansi"].value_counts().reset_index()
            inst_count.columns = ["Instansi", "Jumlah"]
            st.dataframe(inst_count, use_container_width=True, hide_index=True)

        st.markdown("---")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Laporan Lengkap (CSV)",
            data=csv,
            file_name=f"laporan_rdb_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            type="primary"
        )
    else:
        st.info("📭 Belum ada data.")

# ==================== UPLOAD EXCEL ====================
elif menu == "📤 Upload Excel":
    page_header("📤", "Upload Data dari Excel / CSV",
                "Unggah data peserta massal dengan validasi otomatis sebelum disimpan", "IMPORT")

    st.markdown("""
    ### 📋 Format File Excel
    File harus memiliki kolom berikut (urutan bebas, **case-insensitive**):
    - **nama** — Nama lengkap peserta
    - **jenjang** — Jenjang pendidikan
    - **instansi** — Nama sekolah / instansi
    - **kabupaten** — Nama kabupaten / kota
    - **tahun** — Tahun (angka)
    """)

    template_data = {
        "nama": ["Nyoman Hendrajaya, S.Pd", "Kadek Astuyasa, S.Pd."],
        "jenjang": ["SMP", "Disdikpora"],
        "instansi": ["SMP N 3 DENPASAR", "DISDIK TABANAN"],
        "kabupaten": ["Kota Denpasar", "Kabupaten Tabanan"],
        "tahun": [2022, 2022]
    }
    template_df = pd.DataFrame(template_data)

    st.download_button(
        label="📥 Download Template Excel",
        data=template_df.to_csv(index=False).encode("utf-8"),
        file_name="template_upload_rdb.csv",
        mime="text/csv",
        type="secondary"
    )

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "📂 Pilih file Excel atau CSV",
        type=["xlsx", "xls", "csv"],
        help="Upload file Excel (.xlsx, .xls) atau CSV"
    )

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)

            st.success(f"✅ File berhasil dibaca! Total: {len(df_upload)} baris")

            df_upload.columns = df_upload.columns.str.lower().str.strip()
            st.info(f"📋 Kolom yang terdeteksi: {', '.join(df_upload.columns.tolist())}")

            section("👀 Preview Data")
            st.dataframe(df_upload.head(10), use_container_width=True)

            required_cols = ["nama", "jenjang", "instansi", "kabupaten", "tahun"]
            missing_cols = []
            for col in required_cols:
                if col not in df_upload.columns:
                    similar = [c for c in df_upload.columns if col in c or c in col]
                    if similar:
                        st.warning(f"⚠️ Kolom '{col}' tidak ditemukan, tapi ada '{similar[0]}'. Akan digunakan.")
                        df_upload.rename(columns={similar[0]: col}, inplace=True)
                    else:
                        missing_cols.append(col)

            if missing_cols:
                st.error(f"❌ Kolom tidak ditemukan: {', '.join(missing_cols)}")
                st.info("💡 Pastikan nama kolom sesuai: nama, jenjang, instansi, kabupaten, tahun")
            else:
                st.success("✅ Semua kolom required tersedia!")

                df_upload = df_upload[required_cols].copy()
                for col in ["nama", "jenjang", "instansi", "kabupaten"]:
                    df_upload[col] = df_upload[col].astype(str).str.strip()
                df_upload["tahun"] = pd.to_numeric(df_upload["tahun"], errors="coerce").fillna(0).astype(int)

                section("📊 Hasil Validasi Data")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    null_count = df_upload[required_cols].isnull().sum().sum()
                    st.metric("Data Kosong", null_count,
                              delta="harus 0" if null_count > 0 else "✓", delta_color="inverse")
                with col2:
                    jenjang_unique = df_upload["jenjang"].nunique()
                    st.metric("Jenjang Unik", jenjang_unique)
                with col3:
                    duplicates = df_upload.duplicated(subset=["nama", "tahun"]).sum()
                    st.metric("Duplikat", duplicates,
                              delta="harus 0" if duplicates > 0 else "✓", delta_color="inverse")
                with col4:
                    invalid_tahun = (df_upload["tahun"] < 2000).sum() + (df_upload["tahun"] > 2100).sum()
                    st.metric("Tahun Valid", f"{len(df_upload) - invalid_tahun}/{len(df_upload)}")

                if null_count > 0:
                    st.warning("⚠️ Data dengan nilai kosong:")
                    st.dataframe(df_upload[df_upload.isnull().any(axis=1)], use_container_width=True)

                if duplicates > 0:
                    st.warning("⚠️ Data duplikat (nama + tahun sama):")
                    st.dataframe(df_upload[df_upload.duplicated(subset=["nama", "tahun"], keep=False)], use_container_width=True)

                unique_jenjang = df_upload["jenjang"].unique().tolist()
                if len(unique_jenjang) <= 10:
                    st.info(f"📚 Jenjang ditemukan: {', '.join(unique_jenjang)}")
                else:
                    st.info(f"📚 Jenjang ditemukan: {', '.join(unique_jenjang[:10])} ... (+{len(unique_jenjang)-10})")

                st.markdown("---")
                col1, col2 = st.columns([3, 1])
                with col1:
                    section("📤 Upload ke Database")
                    st.info(f"Siap mengupload **{len(df_upload)}** data ke database")
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    upload_btn = st.button("📤 UPLOAD", type="primary", use_container_width=True)

                if upload_btn:
                    if null_count > 0:
                        st.error("❌ Masih ada data yang kosong!")
                    elif invalid_tahun > 0:
                        st.error("❌ Ada tahun tidak valid! Harus 2000–2100")
                    else:
                        with st.spinner("⏳ Mengupload data ke database..."):
                            data_to_insert = df_upload[required_cols].to_dict("records")
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            success_count = 0
                            failed_count = 0

                            for idx, record in enumerate(data_to_insert):
                                if tambah_data(
                                    record["nama"], record["jenjang"],
                                    record["instansi"], record["kabupaten"], record["tahun"]
                                ):
                                    success_count += 1
                                else:
                                    failed_count += 1

                                progress = (idx + 1) / len(data_to_insert)
                                progress_bar.progress(progress)
                                status_text.text(f"Uploading... {idx+1}/{len(data_to_insert)}")

                            progress_bar.empty()
                            status_text.empty()

                            if success_count == len(data_to_insert):
                                st.success(f"🎉 Berhasil mengupload semua {success_count} data!")
                                st.balloons()
                            elif success_count > 0:
                                st.warning(f"⚠️ Berhasil: {success_count} | Gagal: {failed_count}")
                            else:
                                st.error("❌ Gagal mengupload semua data.")

        except Exception as e:
            st.error(f"❌ Error membaca file: {str(e)}")
            st.info("💡 Pastikan file tidak corrupt dan format sesuai template")
