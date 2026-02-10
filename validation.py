def validate_input(nama, jenjang, instansi, kabupaten, tahun):
    """
    Validasi input data peserta.
    Tidak ada validasi strict untuk jenjang - semua jenjang diterima.
    """
    if not nama or not str(nama).strip():
        return False, "Nama wajib diisi"
    
    if not jenjang or not str(jenjang).strip():
        return False, "Jenjang wajib diisi"
    
    if not instansi or not str(instansi).strip():
        return False, "Instansi wajib diisi"
    
    if not kabupaten or not str(kabupaten).strip():
        return False, "Kabupaten wajib diisi"
    
    if not tahun:
        return False, "Tahun wajib diisi"
    
    try:
        tahun_int = int(tahun)
        if tahun_int < 2000 or tahun_int > 2100:
            return False, "Tahun harus antara 2000-2100"
    except (ValueError, TypeError):
        return False, "Tahun harus berupa angka"
    
    return True, ""