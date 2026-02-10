from crud import tambah_data

sample_data = [
    ("Nyoman Hendrajaya, S.Pd", "SMP", "SMP N 3 DENPASAR", "Kota Denpasar", 2022),
    ("Kadek Astuyasa, S.Pd.", "SMP", "SMP N 7 DENPASAR", "Kota Denpasar", 2022),
    ("Drs. Ida Bagus Putu Sudiasa, M.Pd", "SMP", "PENGAWAS BADUNG", "Kabupaten Badung", 2022),
    ("I Gusti Ngurah Purnama Adi Putra, S.Pd.", "SMP", "SMP N ABIANSEMAL", "Kabupaten Badung", 2022),
    ("I Putu Wiarsayana, S.Pd.B.,M.Pd.", "SMP", "SMP N 2 ABIANSEMAL", "Kabupaten Badung", 2022),
]

print("Uploading sample data...")
for data in sample_data:
    nama, jenjang, instansi, kabupaten, tahun = data
    if tambah_data(nama, jenjang, instansi, kabupaten, tahun):
        print(f"✅ {nama}")
    else:
        print(f"❌ Gagal: {nama}")

print("Done!")