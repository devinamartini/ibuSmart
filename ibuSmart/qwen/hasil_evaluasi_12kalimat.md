# Hasil Evaluasi Qwen - Ekstraksi Transaksi

- Tanggal evaluasi: 2026-11-17 08:26
- Model: `Qwen/Qwen2.5-1.5B-Instruct`
- Data uji: `contoh_transkripsi.jsonl` (12 kalimat)

## Ringkasan

| Metrik | Hasil |
|---|---|
| Keluaran berupa JSON yang dapat dibaca | 12/12 (100.0%) |
| Lolos validasi (status valid) | 11/12 (91.7%) |
| Seluruh field cocok dengan harapan | 8/12 (66.7%) |

## Akurasi per field

| Field | Benar |
|---|---|
| tipe | 11/12 (91.7%) |
| barang | 12/12 (100.0%) |
| satuan | 10/12 (83.3%) |
| jumlah | 11/12 (91.7%) |
| nominal | 11/12 (91.7%) |

## Kasus yang salah

- Kalimat: `beli jeruk tiga kilo seratus lima puluh ribu`
  - Harapan: `{"tipe": "pengeluaran", "barang": "jeruk", "satuan": "kilo", "jumlah": 3, "nominal": 150000}`
  - Hasil: `{"tipe": "pengeluaran", "barang": "jeruk", "satuan": "kilogram", "jumlah": 3, "nominal": 105000}`
  - Field berbeda: satuan, nominal
- Kalimat: `beli janur dua puluh ikat dua ratus ribu`
  - Harapan: `{"tipe": "pengeluaran", "barang": "janur", "satuan": "ikat", "jumlah": 20, "nominal": 200000}`
  - Hasil: `{"tipe": "pengeluaran", "barang": "janur", "satuan": "ikat", "jumlah": 2, "nominal": 200000}`
  - Field berbeda: jumlah
- Kalimat: `beli beras lima kilo enam puluh dua ribu lima ratus`
  - Harapan: `{"tipe": "pengeluaran", "barang": "beras", "satuan": "kilo", "jumlah": 5, "nominal": 62500}`
  - Hasil: `{"tipe": "pengeluaran", "barang": "beras", "satuan": "kilogram", "jumlah": 5, "nominal": 62500}`
  - Field berbeda: satuan
- Kalimat: `pembeli bayar tujuh puluh ribu untuk bunga pacah empat ikat`
  - Harapan: `{"tipe": "pemasukan", "barang": "bunga pacah", "satuan": "ikat", "jumlah": 4, "nominal": 70000}`
  - Hasil: `{"tipe": "pengeluaran", "barang": "bunga pacah", "satuan": "ikat", "jumlah": 4, "nominal": 70000}`
  - Field berbeda: tipe

## Catatan

- Data uji berukuran kecil, jadi hasil ini hanya gambaran awal.
- Evaluasi memakai teks yang sudah bersih, belum memakai keluaran Whisper yang mungkin berisi salah dengar.
