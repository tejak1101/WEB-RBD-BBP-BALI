import os
import streamlit as st
from supabase import create_client

# Baca Supabase credentials
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validasi
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("❌ Supabase credentials tidak ditemukan!")
    st.stop()

# Buat koneksi
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
