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
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== KEMENDIKDASMEN OFFICIAL THEME ====================
# Palet warna resmi mengikuti kemendikdasmen.go.id
KMD_RED       = "#c0001a"      # Merah utama Kemendikdasmen
KMD_RED_DARK  = "#8b0013"      # Merah gelap (hover / gradient)
KMD_RED_LIGHT = "#f9e6e8"      # Merah muda (background aksen)
KMD_GOLD      = "#e8a020"      # Kuning emas (aksen)
KMD_GOLD_LIGHT= "#fef3dc"      # Kuning emas muda
KMD_NAVY      = "#1a2340"      # Biru tua / teks gelap
KMD_DARK      = "#0f1520"      # Teks utama (hampir hitam)
KMD_MUTED     = "#6b7280"      # Teks sekunder
KMD_BORDER    = "#e5e7eb"      # Border
KMD_BG        = "#f8f9fc"      # Background utama
KMD_CARD      = "#ffffff"      # Card background
KMD_SUCCESS   = "#16a34a"      # Hijau sukses

st.markdown(f"""
<style>
/* =====================================================
   KEMENDIKDASMEN OFFICIAL DESIGN SYSTEM
   Referensi: kemendikdasmen.go.id
   ===================================================== */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

:root {{
  --red:        {KMD_RED};
  --red-dark:   {KMD_RED_DARK};
  --red-light:  {KMD_RED_LIGHT};
  --gold:       {KMD_GOLD};
  --gold-light: {KMD_GOLD_LIGHT};
  --navy:       {KMD_NAVY};
  --dark:       {KMD_DARK};
  --muted:      {KMD_MUTED};
  --border:     {KMD_BORDER};
  --bg:         {KMD_BG};
  --card:       {KMD_CARD};
}}

/* ── Global ────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {{
  background: var(--bg) !important;
  font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif !important;
}}

.block-container {{
  padding-top: 0rem !important;
  padding-bottom: 2rem;
  max-width: 1440px;
}}

h1, h2, h3, h4, h5 {{
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 800 !important;
  color: var(--dark) !important;
  letter-spacing: -0.3px;
}}

p, li, span, div {{
  font-family: 'Plus Jakarta Sans', sans-serif;
}}

/* ── Hero Header Bar ────────────────────────────────── */
.kmd-hero {{
  background: linear-gradient(135deg, var(--red-dark) 0%, var(--red) 50%, #d4001f 100%);
  border-radius: 0 0 28px 28px;
  padding: 0;
  margin: -1rem -1rem 1.5rem -1rem;
  box-shadow: 0 8px 40px rgba(192,0,26,.25);
  position: relative;
  overflow: hidden;
}}

.kmd-hero::before {{
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 300px; height: 300px;
  border-radius: 50%;
  background: rgba(255,255,255,.06);
}}

.kmd-hero::after {{
  content: '';
  position: absolute;
  bottom: -80px; left: 30%;
  width: 400px; height: 200px;
  border-radius: 50%;
  background: rgba(232,160,32,.10);
}}

.kmd-hero-inner {{
  position: relative;
  z-index: 1;
  padding: 20px 28px;
  display: flex;
  align-items: center;
  gap: 18px;
}}

.kmd-hero-emblem {{
  width: 64px;
  height: 64px;
  background: rgba(255,255,255,.15);
  border: 2px solid rgba(255,255,255,.30);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  backdrop-filter: blur(8px);
  flex-shrink: 0;
}}

.kmd-hero-text .sup {{
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: rgba(255,255,255,.75);
  margin-bottom: 3px;
}}

.kmd-hero-text .title {{
  font-size: 20px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.15;
}}

.kmd-hero-text .sub {{
  font-size: 12px;
  color: rgba(255,255,255,.80);
  margin-top: 5px;
  font-weight: 500;
}}

.kmd-hero-badge {{
  margin-left: auto;
  background: var(--gold);
  color: var(--dark);
  font-size: 11px;
  font-weight: 800;
  padding: 6px 14px;
  border-radius: 999px;
  letter-spacing: .5px;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(232,160,32,.35);
}}

/* ── Page Title Banner ──────────────────────────────── */
.kmd-page-banner {{
  background: var(--card);
  border: 1px solid var(--border);
  border-left: 5px solid var(--red);
  border-radius: 16px;
  padding: 14px 20px;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 4px 18px rgba(15,21,32,.05);
}}

.kmd-page-banner .pg-icon {{
  width: 44px; height: 44px;
  background: var(--red-light);
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
}}

.kmd-page-banner .pg-title {{
  font-size: 17px;
  font-weight: 800;
  color: var(--dark);
  line-height: 1.2;
}}

.kmd-page-banner .pg-sub {{
  font-size: 12px;
  color: var(--muted);
  margin-top: 2px;
  font-weight: 500;
}}

/* ── Sidebar ────────────────────────────────────────── */
[data-testid="stSidebar"] {{
  background: #ffffff !important;
  border-right: 1px solid var(--border) !important;
}}

[data-testid="stSidebar"] > div:first-child {{
  background: #ffffff;
}}

.kmd-sidebar-brand {{
  background: linear-gradient(135deg, var(--red) 0%, var(--red-dark) 100%);
  border-radius: 20px;
  padding: 18px 16px;
  margin-bottom: 6px;
  position: relative;
  overflow: hidden;
}}

.kmd-sidebar-brand::after {{
  content: '';
  position: absolute;
  bottom: -25px; right: -25px;
  width: 100px; height: 100px;
  border-radius: 50%;
  background: rgba(255,255,255,.08);
}}

.kmd-sidebar-logo {{
  width: 54px; height: 54px;
  background: rgba(255,255,255,.15);
  border: 2px solid rgba(255,255,255,.25);
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
  margin-bottom: 12px;
}}

.kmd-sidebar-title {{
  font-size: 15px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.2;
}}

.kmd-sidebar-sub {{
  font-size: 11px;
  color: rgba(255,255,255,.75);
  margin-top: 4px;
  font-weight: 500;
}}

.kmd-sidebar-date {{
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid rgba(255,255,255,.20);
  font-size: 11px;
  color: rgba(255,255,255,.70);
  font-weight: 500;
}}

.kmd-nav-label {{
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--muted);
  padding: 0 4px;
  margin-bottom: 4px;
  margin-top: 16px;
}}

/* Radio as nav pills */
div[role="radiogroup"] > label {{
  background: #ffffff !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 14px !important;
  padding: 10px 14px !important;
  margin: 4px 0 !important;
  cursor: pointer;
  transition: all .18s ease !important;
  font-weight: 600 !important;
  color: var(--dark) !important;
}}

div[role="radiogroup"] > label:hover {{
  border-color: var(--red) !important;
  background: var(--red-light) !important;
  color: var(--red) !important;
  transform: translateX(3px) !important;
  box-shadow: 0 6px 14px rgba(192,0,26,.10) !important;
}}

div[role="radiogroup"] input:checked + div {{
  color: var(--red) !important;
  font-weight: 800 !important;
}}

/* ── Metric Cards ───────────────────────────────────── */
[data-testid="stMetric"] {{
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-top: 4px solid var(--red) !important;
  border-radius: 18px !important;
  padding: 16px 18px !important;
  box-shadow: 0 6px 20px rgba(15,21,32,.06) !important;
  transition: transform .2s ease, box-shadow .2s ease;
}}

[data-testid="stMetric"]:hover {{
  transform: translateY(-3px);
  box-shadow: 0 12px 28px rgba(192,0,26,.12) !important;
}}

[data-testid="stMetricLabel"] > div {{
  color: var(--muted) !important;
  font-weight: 700 !important;
  font-size: 13px !important;
  letter-spacing: .2px;
}}

[data-testid="stMetricValue"] > div {{
  color: var(--red) !important;
  font-weight: 900 !important;
  font-size: 28px !important;
  letter-spacing: -0.5px;
}}

/* ── Cards / Containers ─────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {{
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 20px !important;
  box-shadow: 0 8px 24px rgba(15,21,32,.06) !important;
}}

/* ── Buttons ────────────────────────────────────────── */
.stButton > button {{
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 800 !important;
  border-radius: 12px !important;
  padding: 0.55rem 1.2rem !important;
  transition: all .18s ease !important;
  letter-spacing: .2px;
  border: 2px solid transparent !important;
}}

.stButton > button[kind="primary"] {{
  background: linear-gradient(135deg, var(--red), var(--red-dark)) !important;
  color: #ffffff !important;
  box-shadow: 0 6px 18px rgba(192,0,26,.30) !important;
}}

.stButton > button[kind="primary"]:hover {{
  box-shadow: 0 10px 24px rgba(192,0,26,.40) !important;
  transform: translateY(-2px) !important;
  filter: brightness(1.05);
}}

.stButton > button[kind="secondary"] {{
  background: #ffffff !important;
  color: var(--red) !important;
  border: 2px solid var(--red) !important;
}}

.stButton > button[kind="secondary"]:hover {{
  background: var(--red-light) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 18px rgba(192,0,26,.12) !important;
}}

/* ── Inputs ─────────────────────────────────────────── */
input, textarea, select {{
  border-radius: 12px !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  border: 1.5px solid var(--border) !important;
  transition: border-color .18s ease !important;
}}

input:focus, textarea:focus {{
  border-color: var(--red) !important;
  box-shadow: 0 0 0 3px rgba(192,0,26,.10) !important;
}}

[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stRadio"] label {{
  font-weight: 700 !important;
  color: var(--dark) !important;
  font-size: 13px !important;
}}

/* ── Dataframe ──────────────────────────────────────── */
[data-testid="stDataFrame"] {{
  border-radius: 16px !important;
  overflow: hidden !important;
  border: 1px solid var(--border) !important;
  box-shadow: 0 4px 14px rgba(15,21,32,.05) !important;
}}

/* ── Tabs ───────────────────────────────────────────── */
[data-testid="stTabs"] button {{
  font-weight: 700 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  border-radius: 10px 10px 0 0 !important;
}}

[data-testid="stTabs"] button[aria-selected="true"] {{
  color: var(--red) !important;
  border-bottom: 3px solid var(--red) !important;
  font-weight: 900 !important;
}}

/* ── Alerts & Info Boxes ────────────────────────────── */
[data-testid="stAlert"] {{
  border-radius: 14px !important;
  border-left: 5px solid var(--red) !important;
  font-weight: 600 !important;
}}

/* File uploader */
[data-testid="stFileUploaderDropzone"] {{
  border-radius: 18px !important;
  border: 2px dashed rgba(192,0,26,.35) !important;
  background: rgba(192,0,26,.025) !important;
  transition: all .18s ease !important;
}}

[data-testid="stFileUploaderDropzone"]:hover {{
  border-color: var(--red) !important;
  background: rgba(192,0,26,.05) !important;
}}

/* Download button */
[data-testid="stDownloadButton"] > button {{
  border-radius: 12px !important;
  font-weight: 800 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}}

/* Divider */
hr {{
  border: none !important;
  border-top: 1.5px solid var(--border) !important;
  margin: 20px 0 !important;
}}

/* Subheader with red accent */
.kmd-section-title {{
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 800;
  color: var(--dark);
  margin: 4px 0 14px 0;
}}

.kmd-section-title::before {{
  content: '';
  display: inline-block;
  width: 4px;
  height: 20px;
  background: var(--red);
  border-radius: 4px;
  flex-shrink: 0;
}}

/* Gold accent info pill */
.kmd-info-pill {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--gold-light);
  color: #92610a;
  font-size: 12px;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 999px;
  border: 1px solid rgba(232,160,32,.25);
  margin-bottom: 10px;
}}

/* Status bar on sidebar bottom */
.kmd-sidebar-footer {{
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 10px 12px;
  text-align: center;
  margin-top: 8px;
}}

.kmd-stat-row {{
  display: flex;
  gap: 10px;
}}

.kmd-stat-card {{
  flex: 1;
  background: var(--card);
  border: 1px solid var(--border);
  border-top: 3px solid var(--gold);
  border-radius: 14px;
  padding: 12px;
  text-align: center;
}}

/* Spinner color override */
.stSpinner > div {{
  border-top-color: var(--red) !important;
}}

/* Warning border */
[data-testid="stAlert"][kind="warning"] {{
  border-left-color: var(--gold) !important;
}}

[data-testid="stAlert"][kind="success"] {{
  border-left-color: #16a34a !important;
}}

/* Progress bar */
[data-testid="stProgressBar"] > div > div {{
  background: linear-gradient(90deg, var(--red), var(--gold)) !important;
  border-radius: 999px !important;
}}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {{
  border-radius: 12px !important;
  border: 1.5px solid var(--border) !important;
}}

</style>
""", unsafe_allow_html=True)

# ==================== PLOTLY STYLE HELPER ====================
def style_plotly(fig):
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=KMD_DARK, family="Plus Jakarta Sans"),
        title_font=dict(color=KMD_DARK, family="Plus Jakarta Sans"),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            bgcolor="rgba(255,255,255,0.90)",
            bordercolor="rgba(229,231,235,1)",
            borderwidth=1,
            font=dict(size=12)
        )
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(229,231,235,0.8)", zeroline=False,
                     tickfont=dict(size=11))
    fig.update_yaxes(showgrid=True, gridcolor="rgba(229,231,235,0.8)", zeroline=False,
                     tickfont=dict(size=11))
    return fig

COLOR_SEQ = [KMD_RED, KMD_GOLD, KMD_RED_DARK, "#e85a6b", "#f4c055", "#8b0013", "#c0851a"]

def page_banner(icon, title, subtitle):
    st.markdown(f"""
    <div class="kmd-page-banner">
      <div class="pg-icon">{icon}</div>
      <div>
        <div class="pg-title">{title}</div>
        <div class="pg-sub">{subtitle}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown(f"""
    <div class="kmd-sidebar-brand">
      <div class="kmd-sidebar-logo">📚</div>
      <div class="kmd-sidebar-title">RDB BBP Bali 2026</div>
      <div class="kmd-sidebar-sub">Sistem Informasi Pendataan Peserta</div>
      <div class="kmd-sidebar-date">
        🗓️ <strong>{datetime.now().strftime('%d %B %Y')}</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="kmd-nav-label">🧭 Menu Navigasi</div>', unsafe_allow_html=True)

    menu = st.radio(
        "Menu",
        ["🏠 Dashboard", "🔍 Filter Data", "➕ Tambah Data",
         "✏️ Edit Data", "🗑️ Hapus Data", "📊 Rekapan", "📤 Upload Excel"],
        label_visibility="collapsed"
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kmd-sidebar-footer">
      <div style="font-size:10px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase;
                  color:{KMD_MUTED}; margin-bottom:4px;">Kementerian Pendidikan</div>
      <div style="font-size:12px; font-weight:700; color:{KMD_RED};">Dasar dan Menengah</div>
      <div style="font-size:10px; color:{KMD_MUTED}; margin-top:4px;">Balai Besar Penjaminan Mutu</div>
      <div style="font-size:10px; color:{KMD_MUTED};">Pendidikan Provinsi Bali</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== GLOBAL HERO HEADER ====================
st.markdown(f"""
<div class="kmd-hero">
  <div class="kmd-hero-inner">
    <div class="kmd-hero-emblem">🏛️</div>
    <div class="kmd-hero-text">
      <div class="sup">Kementerian Pendidikan Dasar dan Menengah • Republik Indonesia</div>
      <div class="title">Balai Besar Penjaminan Mutu Pendidikan Provinsi Bali</div>
      <div class="sub">Sistem Pendataan Peserta Rapat Dinas Bersama • Tahun 2026</div>
    </div>
    <div class="kmd-hero-badge">🔴 LIVE {datetime.now().strftime('%Y')}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ==================== DASHBOARD ====================
if menu == "🏠 Dashboard":
    page_banner("🏠", "Dashboard Statistik RDB BBP Bali", "Ringkasan data & visualisasi peserta secara real-time")

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
            st.markdown('<div class="kmd-section-title">Distribusi per Jenjang</div>', unsafe_allow_html=True)
            jenjang_count = df["Jenjang"].value_counts()
            fig = px.pie(
                values=jenjang_count.values,
                names=jenjang_count.index,
                hole=0.45,
                color_discrete_sequence=COLOR_SEQ
            )
            fig.update_traces(textposition="inside", textinfo="percent+label",
                              textfont_size=12, textfont_family="Plus Jakarta Sans")
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        with col2:
            st.markdown('<div class="kmd-section-title">Peserta per Tahun</div>', unsafe_allow_html=True)
            tahun_count = df["Tahun"].value_counts().sort_index()
            fig = px.bar(
                x=tahun_count.index,
                y=tahun_count.values,
                labels={"x": "Tahun", "y": "Jumlah Peserta"},
            )
            fig.update_traces(marker_color=KMD_RED, marker_line_color=KMD_RED_DARK,
                              marker_line_width=1.5)
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="kmd-section-title">Distribusi per Kabupaten</div>', unsafe_allow_html=True)
            kab_count = df["Kabupaten"].value_counts()
            fig = px.bar(
                x=kab_count.values,
                y=kab_count.index,
                orientation="h",
                labels={"x": "Jumlah", "y": "Kabupaten"},
            )
            fig.update_traces(marker_color=KMD_RED)
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        with col2:
            st.markdown('<div class="kmd-section-title">Top 10 Instansi</div>', unsafe_allow_html=True)
            top_inst = df["Instansi"].value_counts().head(10)
            fig = px.bar(
                x=top_inst.values,
                y=top_inst.index,
                orientation="h",
                labels={"x": "Jumlah Peserta", "y": "Instansi"},
            )
            fig.update_traces(marker_color=KMD_GOLD)
            st.plotly_chart(style_plotly(fig), use_container_width=True)

        st.markdown("---")
        st.markdown('<div class="kmd-section-title">Data Terbaru (10 Terakhir)</div>', unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)

    else:
        st.info("📭 Belum ada data. Silakan tambah data terlebih dahulu.")

# ==================== FILTER DATA ====================
elif menu == "🔍 Filter Data":
    page_banner("🔍", "Filter & Cari Data Peserta", "Cari dan filter data peserta dengan cepat dan akurat")

    data = get_all_data()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])

        st.markdown('<div class="kmd-section-title">🎯 Parameter Filter</div>', unsafe_allow_html=True)
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
    page_banner("➕", "Tambah Data Peserta Baru", "Input data peserta baru ke dalam sistem database")

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
    page_banner("✏️", "Edit Data Peserta", "Muat data berdasarkan ID lalu perbarui informasinya")

    data = get_all_data()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])

        st.markdown('<div class="kmd-section-title">🔍 Cari Data</div>', unsafe_allow_html=True)
        search = st.text_input("🔎 Cari berdasarkan Nama", placeholder="Ketik nama...")

        if search:
            df_search = df[df["Nama"].str.contains(search, case=False, na=False)]
        else:
            df_search = df.head(20)

        st.dataframe(df_search, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown('<div class="kmd-section-title">✏️ Form Edit</div>', unsafe_allow_html=True)

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
    page_banner("🗑️", "Hapus Data Peserta", "Penghapusan bersifat permanen — pastikan ID yang dipilih sudah benar")

    data = get_all_data()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])

        st.warning("⚠️ **Perhatian:** Penghapusan data bersifat permanen dan tidak dapat dibatalkan!")

        st.markdown('<div class="kmd-section-title">🔍 Cari Data yang Akan Dihapus</div>', unsafe_allow_html=True)
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
    page_banner("📊", "Rekapan Statistik Lengkap", "Statistik komprehensif per kategori beserta unduhan laporan resmi")

    data = get_all_data()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])

        st.markdown('<div class="kmd-section-title">📈 Ringkasan Umum</div>', unsafe_allow_html=True)
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
                    fig = px.bar(df_stats, x="Jenjang", y="Jumlah", color_discrete_sequence=[KMD_RED])
                    fig.update_traces(marker_color=KMD_RED)
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
                    fig.update_traces(line=dict(color=KMD_RED, width=3),
                                      marker=dict(color=KMD_GOLD, size=10, line=dict(color=KMD_RED, width=2)))
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
                    fig.update_traces(marker_color=KMD_RED)
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
    page_banner("📤", "Upload Data dari Excel / CSV", "Unggah data peserta massal dengan validasi otomatis sebelum disimpan")

    st.markdown("""
    ### 📋 Format File Excel
    File Excel harus memiliki kolom berikut (urutan bebas, **case-insensitive**):
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

            st.markdown('<div class="kmd-section-title">👀 Preview Data</div>', unsafe_allow_html=True)
            st.dataframe(df_upload.head(10), use_container_width=True)

            required_cols = ["nama", "jenjang", "instansi", "kabupaten", "tahun"]

            missing_cols = []
            for col in required_cols:
                if col not in df_upload.columns:
                    similar = [c for c in df_upload.columns if col in c or c in col]
                    if similar:
                        st.warning(f"⚠️ Kolom '{col}' tidak ditemukan, tapi ada '{similar[0]}'. Akan digunakan sebagai '{col}'.")
                        df_upload.rename(columns={similar[0]: col}, inplace=True)
                    else:
                        missing_cols.append(col)

            if missing_cols:
                st.error(f"❌ Kolom berikut tidak ditemukan: {', '.join(missing_cols)}")
                st.info("💡 Pastikan nama kolom di Excel sesuai: nama, jenjang, instansi, kabupaten, tahun")
            else:
                st.success("✅ Semua kolom required tersedia!")

                df_upload = df_upload[required_cols].copy()
                for col in ["nama", "jenjang", "instansi", "kabupaten"]:
                    df_upload[col] = df_upload[col].astype(str).str.strip()
                df_upload["tahun"] = pd.to_numeric(df_upload["tahun"], errors="coerce").fillna(0).astype(int)

                st.markdown('<div class="kmd-section-title">📊 Hasil Validasi Data</div>', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    null_count = df_upload[required_cols].isnull().sum().sum()
                    st.metric("Data Kosong", null_count, delta="harus 0" if null_count > 0 else "✓", delta_color="inverse")
                with col2:
                    jenjang_unique = df_upload["jenjang"].nunique()
                    st.metric("Jenjang Unik", jenjang_unique)
                with col3:
                    duplicates = df_upload.duplicated(subset=["nama", "tahun"]).sum()
                    st.metric("Duplikat", duplicates, delta="harus 0" if duplicates > 0 else "✓", delta_color="inverse")
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
                    st.info(f"📚 Jenjang yang ditemukan: {', '.join(unique_jenjang)}")
                else:
                    st.info(f"📚 Jenjang yang ditemukan: {', '.join(unique_jenjang[:10])} ... (dan {len(unique_jenjang)-10} lainnya)")

                st.markdown("---")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown('<div class="kmd-section-title">📤 Upload ke Database</div>', unsafe_allow_html=True)
                    st.info(f"Siap mengupload **{len(df_upload)}** data ke database")
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    upload_btn = st.button("📤 UPLOAD", type="primary", use_container_width=True)

                if upload_btn:
                    if null_count > 0:
                        st.error("❌ Masih ada data yang kosong!")
                    elif invalid_tahun > 0:
                        st.error("❌ Ada tahun yang tidak valid! Harus antara 2000-2100")
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
                                status_text.text(f"Uploading... {idx + 1}/{len(data_to_insert)}")

                            progress_bar.empty()
                            status_text.empty()

                            if success_count == len(data_to_insert):
                                st.success(f"🎉 Berhasil mengupload semua {success_count} data!")
                                st.balloons()
                            elif success_count > 0:
                                st.warning(f"⚠️ Berhasil: {success_count}, Gagal: {failed_count}")
                            else:
                                st.error("❌ Gagal mengupload semua data.")

        except Exception as e:
            st.error(f"❌ Error membaca file: {str(e)}")
            st.info("💡 Pastikan file Excel tidak corrupt dan format sesuai template")
