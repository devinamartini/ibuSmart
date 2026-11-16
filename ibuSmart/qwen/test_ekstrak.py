"""Pengujian sederhana untuk validasi dan parsing (tanpa memuat model Qwen).

Cara menjalankan (dari folder utama proyek):
    python -m qwen.test_ekstrak
"""

from qwen.ekstrak_transaksi import ambil_json
from qwen.validasi_transaksi import validasi_transaksi


def cek(nama, kondisi):
    print(("LULUS  " if kondisi else "GAGAL  ") + nama)
    assert kondisi, nama


# --- validasi_transaksi ---
valid, bersih, masalah = validasi_transaksi(
    {"tipe": "Pemasukan", "barang": "Janur", "satuan": "ikat", "jumlah": 5, "nominal": 50000}
)
cek("data lengkap dinyatakan valid", valid and masalah == [])
cek("tipe dan barang dirapikan ke huruf kecil", bersih["tipe"] == "pemasukan" and bersih["barang"] == "janur")

valid, _, masalah = validasi_transaksi(
    {"tipe": "pemasukan", "barang": "dupa", "satuan": "bungkus", "jumlah": 3, "nominal": None}
)
cek("nominal null -> perlu konfirmasi", not valid and any("nominal" in m for m in masalah))

valid, _, _ = validasi_transaksi(
    {"tipe": "hutang", "barang": "x", "satuan": "y", "jumlah": 1, "nominal": 1}
)
cek("tipe selain pemasukan/pengeluaran ditolak", not valid)

valid, _, _ = validasi_transaksi(
    {"tipe": "pemasukan", "barang": "x", "satuan": "y", "jumlah": 0, "nominal": 1}
)
cek("jumlah 0 ditolak", not valid)

valid, _, _ = validasi_transaksi(
    {"tipe": "pemasukan", "barang": "x", "satuan": "y", "jumlah": 1, "nominal": -5}
)
cek("nominal negatif ditolak", not valid)

valid, _, _ = validasi_transaksi(
    {"tipe": "pemasukan", "barang": "x", "satuan": "y", "jumlah": 2.5, "nominal": 1}
)
cek("jumlah pecahan ditolak", not valid)

valid, _, _ = validasi_transaksi(
    {"tipe": "pemasukan", "barang": "x", "satuan": "y", "jumlah": True, "nominal": 1}
)
cek("jumlah bertipe boolean ditolak", not valid)

valid, _, _ = validasi_transaksi("bukan dict")
cek("masukan bukan objek ditolak", not valid)

valid, _, _ = validasi_transaksi(
    {"tipe": "pemasukan", "barang": "a" * 101, "satuan": "y", "jumlah": 1, "nominal": 1}
)
cek("barang lebih dari 100 karakter ditolak", not valid)

# --- ambil_json ---
cek("ambil_json membaca JSON polos", ambil_json('{"a": 1}') == {"a": 1})
cek("ambil_json membaca JSON di dalam teks", ambil_json('Hasil: {"a": 1} selesai') == {"a": 1})
cek("ambil_json mengembalikan None jika tidak ada JSON", ambil_json("tidak ada json") is None)
cek("ambil_json mengembalikan None jika JSON rusak", ambil_json("{rusak}") is None)

print("\nSemua pengujian lulus.")
