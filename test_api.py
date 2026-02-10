from dotenv import load_dotenv
import os
import requests

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("Testing Supabase REST API...")
print("=" * 60)
print(f"URL: {SUPABASE_URL}")
print(f"KEY: {SUPABASE_KEY[:20]}..." if SUPABASE_KEY else "KEY: NOT FOUND")
print("=" * 60)

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

try:
    # Test 1: Cek koneksi
    url = f"{SUPABASE_URL}/rest/v1/"
    response = requests.get(url, headers=headers, timeout=10)
    print(f"✅ Koneksi API: {response.status_code}")
    
    # Test 2: Insert data
    url = f"{SUPABASE_URL}/rest/v1/peserta_rdb"
    data = {
        "nama": "Test User API",
        "jenjang": "SMA",
        "instansi": "SMAN 1 Test",
        "kabupaten": "Kota Denpasar",
        "tahun": 2024
    }
    response = requests.post(url, headers=headers, json=data, timeout=10)
    print(f"✅ Insert data: {response.status_code}")
    
    # Test 3: Get data
    url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?select=*&limit=5"
    response = requests.get(url, headers=headers, timeout=10)
    print(f"✅ Get data: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total data: {len(data)} baris")
        if data:
            print(f"✅ Sample data: {data[0]}")
    
    print("=" * 60)
    print("🎉 SEMUA TEST BERHASIL!")
    
except Exception as e:
    print(f"❌ Error: {e}")