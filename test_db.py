import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Test 1: Direct Connection
print("=" * 50)
print("TEST 1: Direct Connection (Port 5432)")
print("=" * 50)
try:
    conn = psycopg2.connect(
        host="db.zpxdftzbesvcluspgbgp.supabase.co",
        port=5432,
        database="postgres",
        user="postgres",
        password="tejaK123!!!k",
        sslmode="require"
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print(f"✅ BERHASIL: {cur.fetchone()[0][:50]}...")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ GAGAL: {e}")

print("\n")

# Test 2: Pooling Connection
print("=" * 50)
print("TEST 2: Pooling Connection (Port 6543)")
print("=" * 50)
try:
    conn = psycopg2.connect(
        host="aws-0-ap-southeast-1.pooler.supabase.com",
        port=6543,
        database="postgres",
        user="postgres.zpxdftzbesvcluspgbgp",
        password="tejaK123!!!k",
        sslmode="require"
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print(f"✅ BERHASIL: {cur.fetchone()[0][:50]}...")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ GAGAL: {e}")