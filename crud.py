import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def tambah_data(nama, jenjang, instansi, kabupaten, tahun):
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb"
        data = {
            "nama": nama,
            "jenjang": jenjang,
            "instansi": instansi,
            "kabupaten": kabupaten,
            "tahun": tahun
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        return response.status_code == 201
    except Exception as e:
        print(f"❌ Error tambah data: {e}")
        return False


def get_all_data():
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?select=id,nama,jenjang,instansi,kabupaten,tahun&order=tahun.desc,nama"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return [(d['id'], d['nama'], d['jenjang'], d['instansi'], d['kabupaten'], d['tahun']) for d in data]
        return []
    except Exception as e:
        print(f"❌ Error get data: {e}")
        return []


def get_data_by_id(id_peserta):
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?id=eq.{id_peserta}&select=*"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]
        return None
    except Exception as e:
        print(f"❌ Error get data by id: {e}")
        return None


def update_data(id_peserta, nama, jenjang, instansi, kabupaten, tahun):
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
        return response.status_code in [200, 204]
    except Exception as e:
        print(f"❌ Error update data: {e}")
        return False


def delete_data(id_peserta):
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?id=eq.{id_peserta}"
        response = requests.delete(url, headers=headers, timeout=10)
        return response.status_code in [200, 204]
    except Exception as e:
        print(f"❌ Error delete data: {e}")
        return False


def statistik_per_tahun():
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
        print(f"❌ Error statistik: {e}")
        return []


def statistik_per_jenjang():
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?select=jenjang"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            stats = {}
            for item in data:
                jenjang = item['jenjang']
                stats[jenjang] = stats.get(jenjang, 0) + 1
            
            return sorted([(jenjang, count) for jenjang, count in stats.items()])
        return []
    except Exception as e:
        print(f"❌ Error statistik jenjang: {e}")
        return []


def statistik_per_kabupaten():
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb?select=kabupaten"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            stats = {}
            for item in data:
                kabupaten = item['kabupaten']
                stats[kabupaten] = stats.get(kabupaten, 0) + 1
            
            return sorted([(kabupaten, count) for kabupaten, count in stats.items()])
        return []
    except Exception as e:
        print(f"❌ Error statistik kabupaten: {e}")
        return []


def bulk_insert(data_list):
    """Insert multiple records at once"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/peserta_rdb"
        response = requests.post(url, headers=headers, json=data_list, timeout=30)
        return response.status_code == 201
    except Exception as e:
        print(f"❌ Error bulk insert: {e}")
        return False