import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from supabase import create_client

SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY"))

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
from crud import (
    tambah_data, get_all_data, get_data_by_id, 
    update_data, delete_data,
    statistik_per_tahun, statistik_per_jenjang, 
    statistik_per_kabupaten, bulk_insert
)
from validation import validate_input
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="RDB BBP Bali 2026",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Cards */
    .css-1r6slb0 {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2d3748;
        font-weight: 700;
    }
    
    /* Dataframe */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    # Logo dengan HTML custom
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="background: white; 
                        width: 120px; height: 120px; 
                        border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center;
                        margin: 0 auto; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                        border: 5px solid rgba(255,255,255,0.3);">
                <span style="font-size: 4rem;">📚</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: white;'>🎓 RDB BBP Bali</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio(
        "📋 Menu Navigasi",
        ["🏠 Dashboard", "🔍 Filter Data", "➕ Tambah Data", 
         "✏️ Edit Data", "🗑️ Hapus Data", "📊 Rekapan", "📤 Upload Excel"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: white;'><strong>📅 Sistem Pendataan Peserta</strong></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: rgba(255,255,255,0.8);'><em>Update: {datetime.now().strftime('%d %B %Y')}</em></p>", unsafe_allow_html=True)

# ==================== DASHBOARD ====================
if menu == "🏠 Dashboard":
    st.title("🏠 Dashboard Statistik RDB BBP Bali")
    
    # Load data
    data = get_all_data()
    
    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])
        
        # Metrics Row
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
        
        # Charts Row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Distribusi per Jenjang")
            jenjang_count = df["Jenjang"].value_counts()
            fig = px.pie(
                values=jenjang_count.values,
                names=jenjang_count.index,
                color_discrete_sequence=px.colors.sequential.RdBu,
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Peserta per Tahun")
            tahun_count = df["Tahun"].value_counts().sort_index()
            fig = px.bar(
                x=tahun_count.index,
                y=tahun_count.values,
                labels={"x": "Tahun", "y": "Jumlah Peserta"},
                color=tahun_count.values,
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Charts Row 2
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🗺️ Distribusi per Kabupaten")
            kab_count = df["Kabupaten"].value_counts()
            fig = px.bar(
                x=kab_count.values,
                y=kab_count.index,
                orientation='h',
                labels={"x": "Jumlah", "y": "Kabupaten"},
                color=kab_count.values,
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🏫 Top 10 Instansi")
            top_inst = df["Instansi"].value_counts().head(10)
            fig = px.bar(
                x=top_inst.values,
                y=top_inst.index,
                orientation='h',
                labels={"x": "Jumlah Peserta", "y": "Instansi"},
                color=top_inst.values,
                color_continuous_scale="Purples"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent Data
        st.markdown("---")
        st.subheader("📋 Data Terbaru (10 Terakhir)")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)
        
    else:
        st.info("📭 Belum ada data. Silakan tambah data terlebih dahulu.")

# ==================== FILTER DATA ====================
elif menu == "🔍 Filter Data":
    st.title("🔍 Filter & Cari Data Peserta")
    
    data = get_all_data()
    
    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])
        
        # Filter Section
        st.markdown("### 🎯 Filter Data")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            search_nama = st.text_input("🔎 Cari Nama", placeholder="Ketik nama...")
        
        with col2:
            # Ambil semua jenjang unik dari database
            all_jenjang = ["Semua"] + sorted(df["Jenjang"].unique().tolist())
            filter_jenjang = st.selectbox("📚 Jenjang", options=all_jenjang)
        
        with col3:
            # Ambil semua kabupaten unik dari database
            all_kabupaten = ["Semua"] + sorted(df["Kabupaten"].unique().tolist())
            filter_kabupaten = st.selectbox("📍 Kabupaten", options=all_kabupaten)
        
        with col4:
            filter_tahun = st.selectbox(
                "📅 Tahun",
                options=["Semua"] + sorted(df["Tahun"].unique().tolist(), reverse=True)
            )
        
        # Apply Filters
        df_filtered = df.copy()
        
        if search_nama:
            df_filtered = df_filtered[
                df_filtered["Nama"].str.contains(search_nama, case=False, na=False)
            ]
        
        if filter_jenjang != "Semua":
            df_filtered = df_filtered[df_filtered["Jenjang"] == filter_jenjang]
        
        if filter_kabupaten != "Semua":
            df_filtered = df_filtered[df_filtered["Kabupaten"] == filter_kabupaten]
        
        if filter_tahun != "Semua":
            df_filtered = df_filtered[df_filtered["Tahun"] == filter_tahun]
        
        # Results
        st.markdown("---")
        st.info(f"📊 Menampilkan **{len(df_filtered)}** dari **{len(df)}** data")
        
        if len(df_filtered) > 0:
            st.dataframe(
                df_filtered,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.NumberColumn("ID", width="small"),
                    "Nama": st.column_config.TextColumn("Nama", width="large"),
                    "Jenjang": st.column_config.TextColumn("Jenjang", width="medium"),
                    "Instansi": st.column_config.TextColumn("Instansi", width="large"),
                    "Kabupaten": st.column_config.TextColumn("Kabupaten", width="medium"),
                    "Tahun": st.column_config.NumberColumn("Tahun", width="small"),
                }
            )
            
            # Download
            csv = df_filtered.to_csv(index=False).encode('utf-8')
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
    st.title("➕ Tambah Data Peserta Baru")
    
    with st.form("form_tambah", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("👤 Nama Lengkap*", placeholder="Contoh: Nyoman Hendrajaya, S.Pd")
            
            # Jenjang bisa dipilih atau diketik manual
            jenjang_type = st.radio("Tipe Jenjang", ["Pilih dari list", "Ketik manual"], horizontal=True)
            
            if jenjang_type == "Pilih dari list":
                jenjang = st.selectbox(
                    "📚 Jenjang*", 
                    ["SD", "SMP", "SMA", "SMK", "TK", "PAUD", "Disdikpora"]
                )
            else:
                jenjang = st.text_input(
                    "📚 Jenjang*", 
                    placeholder="Contoh: Disdikpora, DISDIK TABANAN, dll"
                )
            
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
    st.title("✏️ Edit Data Peserta")

    data = get_all_data()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])

        # Select data to edit
        st.markdown("### 🔍 Pilih Data yang Ingin Diedit")
        search = st.text_input("🔎 Cari berdasarkan Nama", placeholder="Ketik nama...")

        if search:
            df_search = df[df["Nama"].str.contains(search, case=False, na=False)]
        else:
            df_search = df.head(20)

        st.dataframe(df_search, use_container_width=True, hide_index=True)

        # Edit form
        st.markdown("---")
        st.markdown("### ✏️ Form Edit")

        id_edit = st.number_input("🆔 Masukkan ID yang ingin diedit", min_value=1, step=1)

        if st.button("📥 Load Data", type="secondary"):
            data_edit = get_data_by_id(id_edit)
            if data_edit:
                st.session_state['edit_data'] = data_edit
                st.success(f"✅ Data ID {id_edit} berhasil dimuat!")
            else:
                st.error(f"❌ Data dengan ID {id_edit} tidak ditemukan.")

        if 'edit_data' in st.session_state:
            data_edit = st.session_state['edit_data']

            with st.form("form_edit"):
                col1, col2 = st.columns(2)

                with col1:
                    nama = st.text_input("👤 Nama", value=data_edit['nama'])

                    # Jenjang bisa pilih atau ketik
                    jenjang_current = data_edit['jenjang']

                    if jenjang_current in ["SD", "SMP", "SMA", "SMK", "TK", "PAUD", "Disdikpora"]:
                        jenjang_type = st.radio(
                            "Tipe Jenjang",
                            ["Pilih dari list", "Ketik manual"],
                            horizontal=True,
                            index=0
                        )
                    else:
                        jenjang_type = st.radio(
                            "Tipe Jenjang",
                            ["Pilih dari list", "Ketik manual"],
                            horizontal=True,
                            index=1
                        )

                    if jenjang_type == "Pilih dari list":
                        try:
                            idx = ["SD", "SMP", "SMA", "SMK", "TK", "PAUD", "Disdikpora"].index(jenjang_current)
                        except:
                            idx = 0

                        jenjang = st.selectbox(
                            "📚 Jenjang",
                            ["SD", "SMP", "SMA", "SMK", "TK", "PAUD", "Disdikpora"],
                            index=idx
                        )
                    else:
                        jenjang = st.text_input("📚 Jenjang", value=jenjang_current)

                    instansi = st.text_input("🏫 Instansi", value=data_edit['instansi'])

                with col2:
                    kabupaten = st.text_input("📍 Kabupaten", value=data_edit['kabupaten'])
                    tahun = st.number_input("📅 Tahun", value=data_edit['tahun'], min_value=2000, max_value=2100)

                submitted = st.form_submit_button("💾 Update Data", type="primary", use_container_width=True)

                if submitted:
                    if update_data(id_edit, nama, jenjang, instansi, kabupaten, tahun):
                        st.success(f"✅ Data ID {id_edit} berhasil diupdate!")
                        del st.session_state['edit_data']
                        st.rerun()
                    else:
                        st.error("❌ Gagal update data.")

    else:
        st.info("📭 Belum ada data.")

# ==================== HAPUS DATA ====================
elif menu == "🗑️ Hapus Data":
    st.title("🗑️ Hapus Data Peserta")
    
    data = get_all_data()
    
    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])
        
        st.warning("⚠️ **Perhatian:** Penghapusan data bersifat permanen dan tidak dapat dibatalkan!")
        
        # Select data to delete
        st.markdown("### 🔍 Pilih Data yang Ingin Dihapus")
        search = st.text_input("🔎 Cari berdasarkan Nama", placeholder="Ketik nama...")
        
        if search:
            df_search = df[df["Nama"].str.contains(search, case=False, na=False)]
        else:
            df_search = df.head(20)
        
        st.dataframe(df_search, use_container_width=True, hide_index=True)
        
        # Delete form
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
    st.title("📊 Rekapan Statistik Lengkap")
    
    data = get_all_data()
    
    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama", "Jenjang", "Instansi", "Kabupaten", "Tahun"])
        
        # Summary Cards
        st.markdown("### 📈 Ringkasan")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Peserta", len(df))
        
        with col2:
            st.metric("Jenjang Berbeda", df["Jenjang"].nunique())
        
        with col3:
            st.metric("Instansi Berbeda", df["Instansi"].nunique())
        
        with col4:
            st.metric("Kabupaten Berbeda", df["Kabupaten"].nunique())
        
        # Detailed Statistics
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
                    fig = px.bar(df_stats, x="Jenjang", y="Jumlah", color="Jumlah")
                    st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            stats = statistik_per_tahun()
            if stats:
                df_stats = pd.DataFrame(stats, columns=["Tahun", "Jumlah"])
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(df_stats, use_container_width=True, hide_index=True)
                with col2:
                    fig = px.line(df_stats, x="Tahun", y="Jumlah", markers=True)
                    st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            stats = statistik_per_kabupaten()
            if stats:
                df_stats = pd.DataFrame(stats, columns=["Kabupaten", "Jumlah"])
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(df_stats, use_container_width=True, hide_index=True)
                with col2:
                    fig = px.bar(df_stats, y="Kabupaten", x="Jumlah", orientation='h')
                    st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            inst_count = df["Instansi"].value_counts().reset_index()
            inst_count.columns = ["Instansi", "Jumlah"]
            st.dataframe(inst_count, use_container_width=True, hide_index=True)
        
        # Download Full Report
        st.markdown("---")
        csv = df.to_csv(index=False).encode('utf-8')
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
    st.title("📤 Upload Data dari Excel")
    
    st.markdown("""
    ### 📋 Format File Excel
    File Excel harus memiliki kolom berikut (urutan bebas, **case-insensitive**):
    - **nama** - Nama lengkap peserta
    - **jenjang** - Jenjang pendidikan (SD/SMP/SMA/SMK/Disdikpora/dll)
    - **instansi** - Nama sekolah/instansi
    - **kabupaten** - Nama kabupaten/kota
    - **tahun** - Tahun (angka)
    """)
    
    # Download Template
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
        data=template_df.to_csv(index=False).encode('utf-8'),
        file_name="template_upload_rdb.csv",
        mime="text/csv",
        type="secondary"
    )
    
    st.markdown("---")
    
    # Upload File
    uploaded_file = st.file_uploader(
        "📂 Pilih file Excel atau CSV",
        type=["xlsx", "xls", "csv"],
        help="Upload file Excel (.xlsx, .xls) atau CSV"
    )
    
    if uploaded_file:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)
            
            st.success(f"✅ File berhasil dibaca! Total: {len(df_upload)} baris")
            
            # Normalize column names (lowercase, strip whitespace)
            df_upload.columns = df_upload.columns.str.lower().str.strip()
            
            st.info(f"📋 Kolom yang terdeteksi: {', '.join(df_upload.columns.tolist())}")
            
            # Preview
            st.markdown("### 👀 Preview Data")
            st.dataframe(df_upload.head(10), use_container_width=True)
            
            # Validate columns
            required_cols = ["nama", "jenjang", "instansi", "kabupaten", "tahun"]
            
            # Check for missing columns
            missing_cols = []
            for col in required_cols:
                if col not in df_upload.columns:
                    # Try to find similar column names
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
                
                # Clean data
                df_upload = df_upload[required_cols].copy()
                
                # Strip whitespace from string columns
                for col in ["nama", "jenjang", "instansi", "kabupaten"]:
                    df_upload[col] = df_upload[col].astype(str).str.strip()
                
                # Convert tahun to int
                df_upload["tahun"] = pd.to_numeric(df_upload["tahun"], errors='coerce').fillna(0).astype(int)
                
                # Validation summary
                st.markdown("### 📊 Validasi Data")
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
                
                # Show invalid data if any
                if null_count > 0:
                    st.warning("⚠️ Data dengan nilai kosong:")
                    st.dataframe(df_upload[df_upload.isnull().any(axis=1)], use_container_width=True)
                
                if duplicates > 0:
                    st.warning("⚠️ Data duplikat (nama + tahun sama):")
                    st.dataframe(df_upload[df_upload.duplicated(subset=["nama", "tahun"], keep=False)], use_container_width=True)
                
                # Show unique jenjang
                unique_jenjang = df_upload['jenjang'].unique().tolist()
                if len(unique_jenjang) <= 10:
                    st.info(f"📚 Jenjang yang ditemukan: {', '.join(unique_jenjang)}")
                else:
                    st.info(f"📚 Jenjang yang ditemukan: {', '.join(unique_jenjang[:10])} ... (dan {len(unique_jenjang)-10} lainnya)")
                
                # Upload button
                st.markdown("---")
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown("### 📤 Upload ke Database")
                    st.info(f"Siap mengupload **{len(df_upload)}** data ke database")
                
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    upload_btn = st.button("📤 UPLOAD", type="primary", use_container_width=True)
                
                if upload_btn:
                    if null_count > 0:
                        st.error("❌ Masih ada data yang kosong! Hapus atau isi data yang kosong terlebih dahulu.")
                    elif invalid_tahun > 0:
                        st.error("❌ Ada tahun yang tidak valid! Harus antara 2000-2100")
                    else:
                        with st.spinner("⏳ Mengupload data ke database..."):
                            # Prepare data
                            data_to_insert = df_upload[required_cols].to_dict('records')
                            
                            # Progress bar
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            # Insert one by one with progress
                            success_count = 0
                            failed_count = 0
                            
                            for idx, record in enumerate(data_to_insert):
                                if tambah_data(
                                    record['nama'],
                                    record['jenjang'],
                                    record['instansi'],
                                    record['kabupaten'],
                                    record['tahun']
                                ):
                                    success_count += 1
                                else:
                                    failed_count += 1
                                
                                # Update progress
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
                                st.error("❌ Gagal mengupload semua data. Periksa koneksi database.")
        
        except Exception as e:
            st.error(f"❌ Error membaca file: {str(e)}")

            st.info("💡 Pastikan file Excel tidak corrupt dan format sesuai template")
