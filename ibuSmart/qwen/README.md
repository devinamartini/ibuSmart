# Qwen - Ekstraksi Transaksi IbuSmart

Folder ini berisi modul Qwen untuk mengubah teks hasil transkripsi Whisper menjadi data transaksi berformat JSON, sesuai skema tabel `transaksi` di PostgreSQL.

## Alur

```text
Teks Whisper -> Qwen (prompt_ekstraksi.txt) -> JSON -> validasi_transaksi.py -> backend FastAPI
```

Contoh:

| Masukan | Keluaran |
|---|---|
| jual janur lima ikat lima puluh ribu | `{"tipe": "pemasukan", "barang": "janur", "satuan": "ikat", "jumlah": 5, "nominal": 50000}` |

Jika informasi tidak disebutkan (misalnya nominal), Qwen mengisi `null`. Validator lalu menandai transaksi sebagai `perlu_konfirmasi` agar pedagang diminta melengkapi data sebelum disimpan.

## Isi folder

| File | Fungsi |
|---|---|
| `prompt_ekstraksi.txt` | Instruksi dan contoh untuk Qwen |
| `ekstrak_transaksi.py` | Memanggil Qwen, mengambil JSON dari keluaran, lalu memvalidasi |
| `validasi_transaksi.py` | Aturan validasi yang disamakan dengan tabel `transaksi` |
| `test_ekstrak.py` | Pengujian validasi dan parsing (tanpa memuat model) |
| `evaluasi_qwen.py` | Menjalankan Qwen pada data uji dan menulis `hasil_evaluasi.md` |
| `data_uji/contoh_transkripsi.jsonl` | Contoh kalimat beserta JSON yang diharapkan |

## Cara menjalankan

Dari folder utama proyek:

```powershell
pip install transformers torch

# Pengujian validasi (cepat, tanpa model)
python -m qwen.test_ekstrak

# Mencoba satu kalimat
python -m qwen.ekstrak_transaksi

# Evaluasi pada data uji (memuat model Qwen, menghasilkan qwen/hasil_evaluasi.md)
python -m qwen.evaluasi_qwen
```

Model default adalah `Qwen/Qwen2.5-1.5B-Instruct`. Untuk memakai model lain:

```powershell
set QWEN_MODEL=Qwen/Qwen2.5-3B-Instruct
```

## Status

| Bagian | Status |
|---|---|
| Prompt ekstraksi transaksi | Sudah dibuat |
| Kode ekstraksi (Qwen -> JSON) | Sudah dibuat |
| Validasi JSON sesuai skema tabel `transaksi` | Sudah dibuat dan lulus pengujian |
| Data uji awal (12 kalimat) | Sudah dibuat |
| Skrip evaluasi | Sudah dibuat |
| Hasil evaluasi Qwen | Belum dijalankan |
| Integrasi dengan backend FastAPI | Dalam pengembangan |
| Integrasi dengan keluaran Whisper | Dalam pengembangan |
| Qwen Holiday Advisor | Tahap berikutnya |

## Catatan

- Qwen hanya mengekstrak transaksi. Prediksi kebutuhan stok dikerjakan modul AI Demand Predictor yang terpisah.
- Data uji saat ini kecil dan berisi teks bersih. Perlu diperluas dengan variasi ucapan pedagang dan salah dengar dari Whisper.
- Jangan unggah bobot model, file `.env`, atau data transaksi asli pedagang ke GitHub.
