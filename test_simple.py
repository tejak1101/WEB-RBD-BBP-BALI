import psycopg2

print("Testing koneksi ke Supabase...")
print("=" * 60)

# Gunakan kredensial dari screenshot
try:
    conn = psycopg2.connect(
        host="db.zpxdftzbesvcluspgbgp.supabase.co",
        port=5432,
        database="postgres",
        user="postgres",
        password="tejaK123!!!k",  # Ganti dengan password asli Anda
        connect_timeout=10
    )
    
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    
    print("✅ KONEKSI BERHASIL!")
    print(f"Database version: {version[0][:80]}...")
    
    # Test create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS peserta_rdb (
            id SERIAL PRIMARY KEY,
            nama VARCHAR(255) NOT NULL,
            jenjang VARCHAR(10) NOT NULL,
            instansi VARCHAR(255) NOT NULL,
            kabupaten VARCHAR(100) NOT NULL,
            tahun INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    print("✅ Tabel peserta_rdb berhasil dibuat/sudah ada")
    
    cur.close()
    conn.close()
    
except psycopg2.OperationalError as e:
    print(f"❌ Error Operasional: {e}")
    print("\nKemungkinan penyebab:")
    print("1. Koneksi internet bermasalah")
    print("2. Firewall memblokir koneksi")
    print("3. Password salah")
    print("4. Project Supabase di-pause")
    
except Exception as e:
    print(f"❌ Error lain: {e}")

print("=" * 60)