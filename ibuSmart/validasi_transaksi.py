"""Validasi data transaksi hasil ekstraksi Qwen.

Aturan disamakan dengan tabel `transaksi` di PostgreSQL:
- tipe      : 'pemasukan' atau 'pengeluaran'
- barang    : teks, maksimal 100 karakter
- satuan    : teks, maksimal 30 karakter
- jumlah    : bilangan bulat > 0
- nominal   : angka >= 0
"""

FIELD_WAJIB = ["tipe", "barang", "satuan", "jumlah", "nominal"]
TIPE_VALID = {"pemasukan", "pengeluaran"}


def _angka(nilai):
    """True jika nilai berupa angka (bukan bool)."""
    return isinstance(nilai, (int, float)) and not isinstance(nilai, bool)


def validasi_transaksi(data):
    """Memeriksa data transaksi.

    Mengembalikan (valid, data_bersih, masalah).
    - valid       : True jika semua aturan terpenuhi
    - data_bersih : dict yang sudah dirapikan (None jika tidak valid)
    - masalah     : daftar pesan untuk ditampilkan ke pedagang
    """
    masalah = []

    if not isinstance(data, dict):
        return False, None, ["Data transaksi bukan objek JSON."]

    bersih = {}

    for field in FIELD_WAJIB:
        if data.get(field) is None:
            masalah.append(f"Field '{field}' belum terisi.")

    # tipe
    tipe = data.get("tipe")
    if tipe is not None:
        tipe = str(tipe).strip().lower()
        if tipe in TIPE_VALID:
            bersih["tipe"] = tipe
        else:
            masalah.append("Field 'tipe' harus 'pemasukan' atau 'pengeluaran'.")

    # barang dan satuan
    for field, batas in (("barang", 100), ("satuan", 30)):
        nilai = data.get(field)
        if nilai is None:
            continue
        nilai = str(nilai).strip().lower()
        if not nilai:
            masalah.append(f"Field '{field}' tidak boleh kosong.")
        elif len(nilai) > batas:
            masalah.append(f"Field '{field}' maksimal {batas} karakter.")
        else:
            bersih[field] = nilai

    # jumlah
    jumlah = data.get("jumlah")
    if jumlah is not None:
        if _angka(jumlah) and float(jumlah).is_integer() and jumlah > 0:
            bersih["jumlah"] = int(jumlah)
        else:
            masalah.append("Field 'jumlah' harus bilangan bulat lebih dari 0.")

    # nominal
    nominal = data.get("nominal")
    if nominal is not None:
        if _angka(nominal) and nominal >= 0:
            bersih["nominal"] = nominal
        else:
            masalah.append("Field 'nominal' harus angka dan tidak boleh negatif.")

    if masalah:
        return False, None, masalah
    return True, bersih, []
