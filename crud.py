import os
import requests
import streamlit as st

# ==================== SUPABASE CONFIG ====================
# Baca dari Streamlit secrets atau environment variable
try:
    # Prioritas: baca dari Streamlit secrets
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    st.sidebar.success(f"✅ Secrets loaded")
    st.sidebar.text(f"URL: {SUPABASE_URL}")
    st.sidebar.text(f"Key: {SUPABASE_KEY[:30]}...")
except Exception as e:
    # Fallback: baca dari .env (untuk testing lokal)
    st.sidebar.error(f"❌ Failed to load secrets: {str(e)}")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        st.sidebar.info("📁 Loaded from .env")
    except:
        pass

# Validasi credentials
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("❌ Supabase credentials tidak ditemukan! Periksa Secrets di Streamlit Cloud")
    st.stop()

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# ==================== CRUD FUNCTIONS ====================

def tambah_data(nama, jenjang, instansi, kabupaten, tahun):
    """Tambah data peserta baru"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb"
        data = {
            "nama": nama,
            "jenjang": jenjang,
            "instansi": instansi,
            "kabupaten": kabupaten,
            "tahun": tahun
        }
        
        # DEBUG: Tampilkan detail request
        with st.expander("🔍 DEBUG - Tambah Data"):
            st.write("**URL:**", url)
            st.json(data)
            st.write("**Headers:**")
            st.json({
                "apikey": SUPABASE_KEY[:30] + "...",
                "Authorization": f"Bearer {SUPABASE_KEY[:30]}...",
                "Content-Type": "application/json"
            })
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        # DEBUG: Tampilkan response
        with st.expander("📡 DEBUG - Response"):
            st.write(f"**Status Code:** {response.status_code}")
            st.write("**Response Text:**")
            st.code(response.text)
            st.write("**Response Headers:**")
            st.json(dict(response.headers))
        
        if response.status_code == 201:
            return True
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        st.error("❌ Koneksi timeout. Periksa jaringan internet Anda.")
        return False
    except requests.exceptions.ConnectionError:
        st.error("❌ Gagal terhubung ke Supabase. Periksa SUPABASE_URL.")
        return False
    except Exception as e:
        st.error(f"❌ Error tambah data: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return False


def get_all_data():
    """Ambil semua data peserta"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?select=id,nama,jenjang,instansi,kabupaten,tahun&order=id.desc"
        
        # DEBUG
        st.sidebar.write("---")
        st.sidebar.write("**🔍 GET All Data**")
        st.sidebar.text(f"URL: {url[:50]}...")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # DEBUG
        st.sidebar.write(f"Status: **{response.status_code}**")
        
        if response.status_code == 200:
            data = response.json()
            st.sidebar.success(f"✅ {len(data)} records")
            return [(d['id'], d['nama'], d['jenjang'], d['instansi'], d['kabupaten'], d['tahun']) for d in data]
        else:
            st.sidebar.error(f"❌ Error: {response.status_code}")
            with st.sidebar.expander("Error Details"):
                st.code(response.text)
            return []
            
    except Exception as e:
        st.sidebar.error(f"❌ Exception in get_all_data")
        with st.sidebar.expander("Exception Details"):
            st.write(str(e))
        return []


def get_data_by_id(id_peserta):
    """Ambil data peserta berdasarkan ID"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?id=eq.{id_peserta}&select=*"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]
        else:
            st.warning(f"⚠️ Error get by ID: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        st.error(f"❌ Error get data by id: {str(e)}")
        return None


def update_data(id_peserta, nama, jenjang, instansi, kabupaten, tahun):
    """Update data peserta"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?id=eq.{id_peserta}"
        data = {
            "nama": nama,
            "jenjang": jenjang,
            "instansi": instansi,
            "kabupaten": kabupaten,
            "tahun": tahun
        }
        response = requests.patch(url, headers=headers, json=data, timeout=10)
        
        if response.status_code not in [200, 204]:
            st.error(f"❌ Update Error {response.status_code}: {response.text}")
        
        return response.status_code in [200, 204]
    except Exception as e:
        st.error(f"❌ Error update data: {str(e)}")
        return False


def delete_data(id_peserta):
    """Hapus data peserta"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?id=eq.{id_peserta}"
        response = requests.delete(url, headers=headers, timeout=10)
        
        if response.status_code not in [200, 204]:
            st.error(f"❌ Delete Error {response.status_code}: {response.text}")
        
        return response.status_code in [200, 204]
    except Exception as e:
        st.error(f"❌ Error delete data: {str(e)}")
        return False


def statistik_per_tahun():
    """Statistik jumlah peserta per tahun"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?select=tahun"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            stats = {}
            for item in data:
                tahun = item['tahun']
                stats[tahun] = stats.get(tahun, 0) + 1
            
            return sorted([(tahun, count) for tahun, count in stats.items()])
        return []
    except Exception as e:
        st.error(f"❌ Error statistik tahun: {str(e)}")
        return []


def statistik_per_jenjang():
    """Statistik jumlah peserta per jenjang"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?select=jenjang"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            stats = {}
            for item in data:
                jenjang = item['jenjang']
                stats[jenjang] = stats.get(jenjang, 0) + 1
            
            return sorted([(jenjang, count) for jenjang, count in stats.items()], key=lambda x: x[1], reverse=True)
        return []
    except Exception as e:
        st.error(f"❌ Error statistik jenjang: {str(e)}")
        return []


def statistik_per_kabupaten():
    """Statistik jumlah peserta per kabupaten"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?select=kabupaten"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            stats = {}
            for item in data:
                kabupaten = item['kabupaten']
                stats[kabupaten] = stats.get(kabupaten, 0) + 1
            
            return sorted([(kabupaten, count) for kabupaten, count in stats.items()], key=lambda x: x[1], reverse=True)
        return []
    except Exception as e:
        st.error(f"❌ Error statistik kabupaten: {str(e)}")
        return []


def bulk_insert(data_list):
    """Insert multiple records at once"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb"
        
        # Convert data list ke format yang benar
        formatted_data = []
        for item in data_list:
            formatted_data.append({
                "nama": str(item.get('nama', '')),
                "jenjang": str(item.get('jenjang', '')),
                "instansi": str(item.get('instansi', '')),
                "kabupaten": str(item.get('kabupaten', '')),
                "tahun": int(item.get('tahun', 2024))
            })
        
        # DEBUG
        st.info(f"📤 Bulk inserting {len(formatted_data)} records...")
        
        response = requests.post(url, headers=headers, json=formatted_data, timeout=30)
        
        if response.status_code != 201:
            st.error(f"❌ Bulk insert error {response.status_code}: {response.text}")
            return False
        
        return True
    except Exception as e:
        st.error(f"❌ Error bulk insert: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return False


def test_connection():
    """Test koneksi ke Supabase"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?select=id&limit=1"
        
        st.sidebar.write("---")
        st.sidebar.write("**🔌 Testing Connection...**")
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            st.sidebar.success("✅ Connection OK!")
            return True
        else:
            st.sidebar.error(f"❌ Connection Failed: {response.status_code}")
            with st.sidebar.expander("Error Details"):
                st.code(response.text)
            return False
    except Exception as e:
        st.sidebar.error(f"❌ Connection Error: {str(e)}")
        return False
