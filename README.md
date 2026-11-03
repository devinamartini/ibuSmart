# IbuSmart – Asisten Operasional dan Prediksi Kebutuhan Pedagang Perempuan di Pasar Tradisional Bali

## 1. Tentang IbuSmart

**IbuSmart** merupakan proyek pengembangan sistem cerdas berbasis kecerdasan buatan (Artificial Intelligence/AI) yang dirancang untuk membantu pedagang perempuan di pasar tradisional Bali dalam mengelola transaksi, keuangan usaha, serta memperkirakan kebutuhan barang dagangan menjelang hari raya keagamaan.

Sistem ini menggabungkan teknologi Speech-to-Text, Large Language Model (LLM), pengolahan data transaksi, kalender Saka Bali, dan prediksi permintaan barang.

IbuSmart dirancang agar pedagang dapat mencatat transaksi melalui suara, memantau kondisi keuangan usaha, serta memperoleh rekomendasi persiapan stok berdasarkan pola transaksi dan momentum hari raya.

## 2. Tujuan Pengembangan

Tujuan utama pengembangan IbuSmart adalah:

1. Mempermudah pencatatan transaksi melalui input suara.
2. Membantu memisahkan keuangan usaha dan kebutuhan rumah tangga.
3. Membantu memperkirakan kebutuhan stok barang berdasarkan riwayat transaksi.
4. Mengintegrasikan kalender Saka Bali untuk mempertimbangkan momentum Galungan dan Kuningan.
5. Memberikan rekomendasi persiapan stok dan keuangan dengan bahasa yang sederhana.
6. Mengembangkan sistem yang tetap dapat digunakan untuk pencatatan ketika koneksi internet tidak tersedia.

## 3. Alur Kerja Sistem IbuSmart

Alur kerja sistem IbuSmart dirancang menjadi beberapa tahapan utama.

### 3.1 Pencatatan Transaksi Menggunakan Suara

1. Pedagang membuka aplikasi IbuSmart.
2. Pedagang memasukkan transaksi melalui suara.
3. Aplikasi merekam suara pedagang.
4. Model Whisper melakukan proses Speech-to-Text untuk mengubah suara menjadi teks.
5. Hasil transkripsi dikirimkan ke Qwen.
6. Qwen mengidentifikasi informasi transaksi, seperti:
   - Jenis transaksi (pemasukan atau pengeluaran).
   - Nama barang.
   - Jumlah barang.
   - Satuan barang.
   - Nominal transaksi.
7. Qwen menghasilkan data transaksi dalam format JSON.
8. Backend FastAPI memvalidasi data yang diterima.
9. Jika data tidak valid atau belum lengkap, sistem meminta pedagang melakukan konfirmasi atau memperbaiki informasi transaksi.
10. Jika data valid, transaksi disimpan ke database lokal menggunakan Room/SQLite.
11. Ketika perangkat kembali terhubung ke internet, data direncanakan untuk disinkronkan ke PostgreSQL.

### 3.2 Pengolahan Data Transaksi

Data transaksi yang telah disimpan digunakan sebagai sumber informasi untuk mengetahui pola kegiatan usaha pedagang.

Data tersebut dapat digunakan untuk:
- Melihat riwayat pemasukan dan pengeluaran.
- Mengetahui barang yang sering terjual.
- Mengamati perubahan jumlah permintaan barang.
- Menjadi data masukan untuk model prediksi kebutuhan stok.

### 3.3 AI Demand Predictor

AI Demand Predictor merupakan modul yang dirancang untuk memperkirakan kebutuhan barang dagangan berdasarkan riwayat transaksi.

Informasi yang digunakan meliputi:
- Riwayat transaksi.
- Jumlah barang yang terjual.
- Pola penjualan berdasarkan waktu.
- Kalender Saka Bali.
- Momentum menjelang Galungan dan Kuningan.

Beberapa pendekatan yang dipertimbangkan untuk pengembangan model adalah:
- ARIMA atau ETS sebagai metode pembanding.
- Prophet sebagai salah satu kandidat model peramalan.
- LSTM atau Gradient Boosting sebagai pendekatan pembanding lainnya.

Hasil prediksi akan menjadi salah satu masukan bagi modul Holiday Advisor.

**Catatan:** AI Demand Predictor merupakan modul terpisah dari Qwen. Qwen tidak bertugas menghitung prediksi permintaan barang.

### 3.4 Qwen LLM Holiday Advisor

Modul Holiday Advisor dirancang untuk memberikan rekomendasi kepada pedagang berdasarkan informasi yang telah diolah oleh sistem.

Informasi masukan yang direncanakan meliputi:
- Hasil prediksi kebutuhan barang.
- Informasi kalender Galungan dan Kuningan.
- Pengetahuan mengenai hari raya dan kebutuhan upakara.
- Informasi kondisi keuangan atau dompet usaha dan rumah tangga.

Qwen digunakan untuk memahami informasi tersebut dan menyusun rekomendasi dalam bahasa Indonesia yang sederhana.

Rekomendasi selanjutnya melewati proses validasi sebelum ditampilkan kepada pedagang.

Qwen berfungsi sebagai pemberi penjelasan dan rekomendasi, bukan sebagai pengganti model prediksi atau pengambil keputusan otomatis.

### 3.5 Notifikasi Kalender Hari Raya

Sistem kalender dirancang untuk mendukung pemberitahuan berdasarkan jarak hari menuju hari raya.

Periode pemberitahuan yang digunakan adalah:
- H-7 sampai H-1: pemberitahuan sebelum hari raya.
- H: tanggal hari raya.
- H+1: satu hari setelah hari raya.

Informasi tersebut dapat digunakan sebagai dasar pengembangan notifikasi persiapan stok dan rekomendasi kepada pedagang.

**Catatan:** Pada tahap pengembangan saat ini, perhitungan dan penampilan tanggal H-7 sampai H+1 sudah dapat dilakukan melalui SQL di PostgreSQL. Pengiriman notifikasi otomatis ke aplikasi Android masih merupakan tahap pengembangan berikutnya.

## 4. Arsitektur Teknologi

Teknologi yang digunakan atau direncanakan dalam pengembangan IbuSmart:

| Komponen | Teknologi | Fungsi |
|---|---|---|
| Speech-to-Text | Whisper | Mengubah suara menjadi teks |
| Pengolahan teks transaksi | Qwen | Mengekstrak informasi transaksi ke JSON |
| Backend | Python dan FastAPI | Mengelola API dan validasi data |
| ORM | SQLAlchemy | Menghubungkan backend dengan database |
| Database backend | PostgreSQL | Menyimpan data kalender dan transaksi |
| Database lokal aplikasi | Room/SQLite | Mendukung penyimpanan transaksi lokal |
| AI Demand Predictor | Prophet, ARIMA/ETS, LSTM atau Gradient Boosting | Memperkirakan permintaan barang |
| LLM Holiday Advisor | Qwen | Menyusun rekomendasi berdasarkan informasi sistem |
| Aplikasi | Android | Antarmuka yang digunakan pedagang |

## 5. Modul Kalender Saka Bali

Salah satu bagian yang telah dikembangkan adalah modul kalender hari raya Galungan dan Kuningan.

Modul ini dibuat untuk menghitung dan menyimpan proyeksi tanggal hari raya ke dalam database PostgreSQL.

### 5.1 Dasar Perhitungan

Pada implementasi awal, perhitungan menggunakan pendekatan aritmetika:

- Jarak siklus Galungan: 210 hari.
- Jarak Kuningan dari Galungan: 10 hari.

Rumus dasar:

```python
tanggal_galungan_berikutnya = tanggal_galungan_sebelumnya + 210 hari

tanggal_kuningan = tanggal_galungan + 10 hari
```

Perhitungan dilakukan secara otomatis ketika endpoint perhitungan kalender dipanggil.

**Penting:** Pendekatan 210 hari ini merupakan proyeksi aritmetika, bukan algoritma lengkap penentuan Pawukon. Karena itu, tanggal hasil perhitungan diberi status `PROYEKSI_BELUM_TERVERIFIKASI` sampai diverifikasi menggunakan sumber kalender resmi atau otoritatif.

### 5.2 Struktur File Kalender

```text
kalender_hari_raya/
├── __init__.py
├── hitung_kalender.py
├── test_kalender.py
└── simpan_ke_database.py
```

### 5.3 Kode Perhitungan Kalender

File: `kalender_hari_raya/hitung_kalender.py`

```python
from datetime import date, timedelta

SIKLUS_GALUNGAN = 210
JARAK_KUNINGAN = 10

def hitung_kalender(tanggal_galungan_awal: date, jumlah_siklus: int):
    hasil = []

    for i in range(jumlah_siklus):
        tanggal_galungan = (
            tanggal_galungan_awal
            + timedelta(days=SIKLUS_GALUNGAN * i)
        )

        tanggal_kuningan = (
            tanggal_galungan
            + timedelta(days=JARAK_KUNINGAN)
        )

        hasil.append({
            "tanggal_acuan": tanggal_galungan_awal.isoformat(),
            "siklus_ke": i + 1,
            "galungan": tanggal_galungan.isoformat(),
            "kuningan": tanggal_kuningan.isoformat(),
            "status_verifikasi": "PROYEKSI_BELUM_TERVERIFIKASI"
        })

    return hasil
```

### 5.4 Pengujian Perhitungan Kalender

File: `kalender_hari_raya/test_kalender.py`

```python
from datetime import date
from kalender_hari_raya.hitung_kalender import hitung_kalender

tanggal_awal = date(2026, 6, 17)
jumlah_siklus = 7

hasil = hitung_kalender(tanggal_awal, jumlah_siklus)

for data in hasil:
    print(data)
```

Perintah untuk menjalankan pengujian melalui terminal:

```powershell
python -m kalender_hari_raya.test_kalender
```

### 5.5 Hasil Proyeksi Kalender

Perhitungan telah berhasil dijalankan menggunakan tanggal acuan 17 Juni 2026 dengan jumlah 20 siklus.

Hasil proyeksi disimpan ke PostgreSQL dengan tanggal sampai tahun 2037.

Contoh beberapa hasil:

| Siklus | Galungan | Kuningan |
|---|---|---|
| 1 | 17 Juni 2026 | 27 Juni 2026 |
| 2 | 13 Januari 2027 | 23 Januari 2027 |
| 3 | 11 Agustus 2027 | 21 Agustus 2027 |
| 4 | 8 Maret 2028 | 18 Maret 2028 |
| 5 | 4 Oktober 2028 | 14 Oktober 2028 |

Seluruh hasil proyeksi yang belum diverifikasi menggunakan status:

```text
PROYEKSI_BELUM_TERVERIFIKASI
```

## 6. Backend IbuSmart

Backend dibuat menggunakan Python dan FastAPI.

Backend bertugas:
- Menyediakan endpoint API.
- Menjalankan perhitungan kalender.
- Memvalidasi masukan.
- Menyimpan data kalender ke PostgreSQL.
- Menampilkan data kalender yang sudah tersimpan.

### 6.1 Struktur Folder Backend

```text
backend/
├── __init__.py
├── main.py
├── database.py
├── models.py
├── requirements.txt
└── .env
```

### 6.2 Koneksi Database

File: `backend/database.py`

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

### 6.3 Konfigurasi Database

File: `backend/.env`

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/ibuSmart_db
```

Ganti `YOUR_PASSWORD` dengan password PostgreSQL milik masing-masing pengguna.

**Keamanan:** File `.env` berisi informasi rahasia dan tidak boleh diunggah ke GitHub. Gunakan `.env.example` sebagai contoh konfigurasi.

### 6.4 Model Database Kalender

File: `backend/models.py`

```python
from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
    DateTime,
    UniqueConstraint,
    func
)

from backend.database import Base

class Kalender(Base):
    __tablename__ = "kalender"

    id = Column(Integer, primary_key=True, index=True)
    tanggal_acuan = Column(Date, nullable=False)
    siklus_ke = Column(Integer, nullable=False)
    galungan = Column(Date, nullable=False)
    kuningan = Column(Date, nullable=False)

    status_verifikasi = Column(
        String(50),
        nullable=False,
        default="PROYEKSI_BELUM_TERVERIFIKASI"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "tanggal_acuan",
            "siklus_ke",
            name="uq_kalender_acuan_siklus"
        ),
    )
```

Constraint unik digunakan agar kombinasi tanggal acuan dan nomor siklus tidak tersimpan sebagai data ganda.

### 6.5 Endpoint Backend

File: `backend/main.py`

Backend menyediakan beberapa endpoint:

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/` | Memeriksa apakah backend berjalan |
| POST | `/kalender/hitung` | Menghitung dan menyimpan proyeksi kalender |
| GET | `/kalender` | Menampilkan seluruh data kalender |
| GET | `/kalender/{tanggal_acuan}` | Menampilkan kalender berdasarkan tanggal acuan |

Endpoint `POST /kalender/hitung` menerima:
- `tanggal_galungan`: tanggal awal perhitungan.
- `jumlah_siklus`: jumlah siklus yang ingin dihitung.

Endpoint menggunakan SQLAlchemy dan PostgreSQL untuk menyimpan data. Mekanisme `ON CONFLICT DO UPDATE` digunakan agar data dengan kombinasi tanggal acuan dan siklus yang sama dapat diperbarui, bukan menambah duplikasi.

## 7. Database PostgreSQL

Database yang digunakan:

```text
Nama database: ibuSmart_db
DBMS: PostgreSQL
Port: 5432
```

Pada tahap ini terdapat tabel utama berikut:

### 7.1 Tabel `kalender`

| Kolom | Tipe Data | Keterangan |
|---|---|---|
| id | Integer | Primary key |
| tanggal_acuan | Date | Tanggal awal perhitungan |
| siklus_ke | Integer | Nomor siklus |
| galungan | Date | Tanggal Galungan |
| kuningan | Date | Tanggal Kuningan |
| status_verifikasi | Varchar | Status verifikasi proyeksi |
| created_at | Timestamp with time zone | Waktu penyimpanan |

### 7.2 Tabel `transaksi`

| Kolom | Tipe Data | Keterangan |
|---|---|---|
| id | Serial | Primary key |
| tipe | Varchar(20) | Pemasukan atau pengeluaran |
| barang | Varchar(100) | Nama barang |
| satuan | Varchar(30) | Satuan barang |
| jumlah | Integer | Jumlah barang |
| nominal | Numeric(12,2) | Nominal transaksi |
| created_at | Timestamp with time zone | Waktu pencatatan |
| tanggal_transaksi | Date | Tanggal transaksi |

Kolom `tipe` dibatasi menggunakan nilai `pemasukan` dan `pengeluaran`. Kolom `jumlah` harus lebih besar dari nol, sedangkan nominal tidak boleh negatif.

### 7.3 SQL Membuat Tabel Transaksi

```sql
CREATE TABLE transaksi (
    id SERIAL PRIMARY KEY,
    tipe VARCHAR(20) NOT NULL
        CHECK (tipe IN ('pemasukan', 'pengeluaran')),
    barang VARCHAR(100) NOT NULL,
    satuan VARCHAR(30) NOT NULL,
    jumlah INTEGER NOT NULL CHECK (jumlah > 0),
    nominal NUMERIC(12,2) NOT NULL CHECK (nominal >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

Kolom tanggal transaksi ditambahkan menggunakan:

```sql
ALTER TABLE transaksi
ADD COLUMN tanggal_transaksi DATE;

UPDATE transaksi
SET tanggal_transaksi = CURRENT_DATE
WHERE tanggal_transaksi IS NULL;
```

### 7.4 Contoh Data Transaksi

```sql
INSERT INTO transaksi (
    tipe,
    barang,
    satuan,
    jumlah,
    nominal
)
VALUES (
    'pemasukan',
    'janur',
    'ikat',
    5,
    50000
);
```

Contoh tersebut menggambarkan transaksi pemasukan dari penjualan 5 ikat janur dengan nominal Rp50.000.

### 7.5 Melihat Data Database di pgAdmin 4

Untuk melihat data kalender:

```sql
SELECT * FROM kalender;
```

Untuk melihat data transaksi:

```sql
SELECT * FROM transaksi;
```

Untuk melihat seluruh nama kolom dan tipe datanya:

```sql
SELECT
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
```

## 8. Perhitungan Periode H-7 sampai H+1

Sistem IbuSmart membutuhkan informasi jarak hari sebelum dan sesudah hari raya untuk mendukung pengembangan rekomendasi serta notifikasi persiapan stok.

Periode yang digunakan:

| Periode | Arti |
|---|---|
| H-7 | Tujuh hari sebelum hari raya |
| H-6 | Enam hari sebelum hari raya |
| H-5 | Lima hari sebelum hari raya |
| H-4 | Empat hari sebelum hari raya |
| H-3 | Tiga hari sebelum hari raya |
| H-2 | Dua hari sebelum hari raya |
| H-1 | Satu hari sebelum hari raya |
| H | Hari raya |
| H+1 | Satu hari setelah hari raya |

### 8.1 Contoh Perhitungan Galungan

Dengan tanggal Galungan contoh 17 Juni 2026, hasil perhitungannya:

| Periode | Tanggal |
|---|---|
| H-7 | 10 Juni 2026 |
| H-6 | 11 Juni 2026 |
| H-5 | 12 Juni 2026 |
| H-4 | 13 Juni 2026 |
| H-3 | 14 Juni 2026 |
| H-2 | 15 Juni 2026 |
| H-1 | 16 Juni 2026 |
| H | 17 Juni 2026 |
| H+1 | 18 Juni 2026 |

Tanggal di atas merupakan contoh berdasarkan tanggal acuan yang digunakan dalam pengujian proyeksi kalender.

### 8.2 SQL Menampilkan H-7 sampai H+1 di PostgreSQL

Perhitungan periode dapat dilakukan langsung melalui Query Tool pgAdmin 4 tanpa menambahkan sembilan kolom baru ke tabel kalender.

Gunakan query berikut:

```sql
SELECT
    k.id,
    h.jenis_hari_raya,
    h.tanggal_hari_raya,
    h.tanggal_hari_raya + s.hari AS tanggal_pemberitahuan,
    CASE
        WHEN s.hari < 0 THEN 'H' || s.hari
        WHEN s.hari = 0 THEN 'H'
        ELSE 'H+' || s.hari
    END AS periode
FROM kalender k
CROSS JOIN LATERAL (
    VALUES
        ('Galungan', k.galungan),
        ('Kuningan', k.kuningan)
) AS h(jenis_hari_raya, tanggal_hari_raya)
CROSS JOIN generate_series(-7, 1) AS s(hari)
ORDER BY
    h.tanggal_hari_raya,
    h.jenis_hari_raya,
    s.hari;
```

### 8.3 Cara Menjalankan Query di pgAdmin 4

1. Buka aplikasi pgAdmin 4.
2. Masuk ke `Servers`.
3. Pilih `PostgreSQL 18`.
4. Buka database `ibuSmart_db`.
5. Klik kanan pada database `ibuSmart_db`.
6. Pilih **Query Tool**.
7. Salin SQL perhitungan H-7 sampai H+1.
8. Tempelkan SQL ke area editor.
9. Tekan tombol **Execute** atau tekan `F5`.
10. Buka tab **Data Output** pada bagian bawah.
11. Hasil perhitungan akan menampilkan:
    - id data kalender.
    - jenis hari raya.
    - tanggal hari raya.
    - tanggal pemberitahuan.
    - periode H-7 sampai H+1.

Query tersebut menghitung periode untuk Galungan dan Kuningan dari seluruh data yang terdapat pada tabel `kalender`.

**Catatan penting:** Query ini hanya menghasilkan dan menampilkan perhitungan periode. Query ini belum mengirimkan notifikasi ke perangkat pedagang dan tidak menambahkan kolom H-7 sampai H+1 secara permanen ke tabel kalender.

## 9. Pengujian Backend Menggunakan Swagger UI

FastAPI menyediakan Swagger UI untuk menguji endpoint tanpa harus membuat antarmuka aplikasi terlebih dahulu.

### 9.1 Menjalankan Backend

Buka terminal pada folder utama proyek IbuSmart.

Jalankan:

```powershell
python -m uvicorn backend.main:app --reload
```

Jika berhasil, server akan berjalan di alamat lokal:

```text
http://127.0.0.1:8000
```

### 9.2 Membuka Swagger UI

Buka browser dan akses:

```text
http://127.0.0.1:8000/docs
```

### 9.3 Menguji Perhitungan Kalender

Pilih endpoint:

```text
POST /kalender/hitung
```

Masukkan contoh JSON berikut:

```json
{
    "tanggal_galungan": "2026-06-17",
    "jumlah_siklus": 20
}
```

Klik **Execute**.

Jika berhasil, sistem mengembalikan status sukses, jumlah siklus, hasil proyeksi kalender, dan informasi bahwa data berhasil disimpan ke PostgreSQL.

### 9.4 Menguji Pengambilan Data Kalender

Gunakan:

```text
GET /kalender
```

Untuk melihat seluruh data kalender.

Gunakan:

```text
GET /kalender/2026-06-17
```

Untuk melihat data berdasarkan tanggal acuan tertentu.

## 10. Pengembangan Whisper dan Qwen

### 10.1 Whisper Speech-to-Text

Whisper digunakan untuk mengubah suara pedagang menjadi teks agar informasi transaksi dapat diproses oleh sistem.

Pengujian Whisper telah dilakukan menggunakan 84 file audio yang mencakup audio bersih dan audio dengan gangguan/noise.

Hasil evaluasi yang dilaporkan:

| Metrik | Hasil Pengujian |
|---|---|
| Jumlah file audio | 84 file |
| Word Error Rate (WER) | 0,00% |
| Character Error Rate (CER) | 0,00% |
| Akurasi kata yang dilaporkan | 100% |
| Akurasi karakter yang dilaporkan | 100% |

Hasil tersebut merupakan hasil pada kumpulan data pengujian 84 file audio, bukan jaminan bahwa model akan memperoleh akurasi yang sama pada seluruh kondisi penggunaan nyata.

### 10.2 Qwen untuk Ekstraksi Transaksi

Qwen digunakan untuk mengolah teks hasil transkripsi Whisper.

Tugas Qwen adalah mengekstrak informasi transaksi menjadi struktur JSON, misalnya:

```json
{
    "tipe": "pemasukan",
    "barang": "janur",
    "satuan": "ikat",
    "jumlah": 5,
    "nominal": 50000
}
```

Data tersebut kemudian diteruskan ke backend untuk divalidasi sebelum disimpan.

### 10.3 Qwen untuk Holiday Advisor

Selain ekstraksi transaksi, Qwen juga digunakan pada modul Holiday Advisor.

Pada modul ini, Qwen dirancang untuk memberikan penjelasan dan rekomendasi berdasarkan hasil prediksi, informasi kalender, pengetahuan hari raya, serta informasi keuangan pedagang.

Kedua penggunaan Qwen memiliki tugas berbeda:
1. Ekstraksi informasi transaksi dari teks hasil Whisper.
2. Penyusunan rekomendasi melalui Holiday Advisor.

Qwen tidak menggantikan fungsi model AI Demand Predictor.

**Catatan:** Pengembangan dan pengujian model Whisper serta Qwen telah dilakukan oleh tim. Integrasi menyeluruh model dengan backend dan aplikasi masih menjadi bagian dari proses pengembangan sistem.

## 11. Keamanan dan Pengelolaan Data

Pengembangan IbuSmart memperhatikan keamanan informasi transaksi dan data pribadi pedagang.

Beberapa hal yang perlu diterapkan:
- Tidak mengunggah password database ke GitHub.
- Menggunakan file `.env` untuk konfigurasi rahasia.
- Membatasi akses ke data transaksi.
- Meminta persetujuan pengguna untuk pemrosesan data yang diperlukan.
- Mempertimbangkan anonimisasi data untuk proses pengujian dan pelatihan.
- Menyediakan mekanisme pengelolaan data pengguna sesuai ketentuan perlindungan data pribadi yang berlaku.
- Mempertimbangkan penyimpanan lokal ketika perangkat tidak memiliki koneksi internet.

## 12. Struktur Folder Proyek

Struktur proyek saat ini:

```text
ibuSmart/
│
├── kalender_hari_raya/
│   ├── __init__.py
│   ├── hitung_kalender.py
│   ├── test_kalender.py
│   └── simpan_ke_database.py
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── requirements.txt
│   └── .env
│
├── .gitignore
├── .env.example
└── README.md
```

Struktur tersebut menggambarkan modul kalender dan backend yang telah dikembangkan. Folder model AI dan aplikasi Android dapat ditambahkan sesuai perkembangan integrasi tim.

## 13. Instalasi dan Menjalankan Proyek

### 13.1 Persyaratan

Pastikan perangkat telah memiliki:
- Python.
- PostgreSQL.
- pgAdmin 4.
- Visual Studio Code atau editor kode lainnya.
- Git.

### 13.2 Menginstal Library Python

Jalankan perintah:

```powershell
pip install sqlalchemy "psycopg[binary]" python-dotenv apscheduler fastapi uvicorn
```

### 13.3 Menyiapkan Database

1. Buka pgAdmin 4.
2. Buat database dengan nama `ibuSmart_db`.
3. Pastikan PostgreSQL berjalan pada port `5432`.
4. Siapkan konfigurasi koneksi database pada file `.env`.

### 13.4 Menjalankan Backend

Dari folder utama proyek:

```powershell
python -m uvicorn backend.main:app --reload
```

### 13.5 Mengakses API

Buka:

```text
http://127.0.0.1:8000/docs
```

## 14. Status Pengembangan Proyek

Berikut perkembangan fitur IbuSmart berdasarkan implementasi saat ini.

| Komponen | Status |
|---|---|
| Konsep dan rancangan alur sistem | Sudah dirancang |
| Pengembangan modul perhitungan kalender | Sudah dibuat |
| Pengujian perhitungan kalender | Sudah dilakukan |
| Koneksi backend ke PostgreSQL | Sudah berhasil |
| Pembuatan tabel kalender | Sudah dilakukan |
| Penyimpanan proyeksi kalender | Sudah berhasil |
| Endpoint perhitungan kalender | Sudah berhasil diuji |
| Endpoint pengambilan data kalender | Sudah dibuat |
| Query periode H-7 sampai H+1 | Sudah dapat dijalankan di PostgreSQL |
| Tabel transaksi | Sudah dibuat |
| Contoh penyimpanan transaksi | Sudah dilakukan |
| Pengujian Whisper 84 file audio | Sudah dilakukan |
| Pengembangan/pelatihan Qwen | Sudah dilakukan oleh tim |
| Integrasi Whisper dan Qwen secara menyeluruh dengan backend | Dalam pengembangan |
| Validasi JSON transaksi secara terintegrasi | Dalam pengembangan |
| Integrasi Room/SQLite dan sinkronisasi PostgreSQL | Direncanakan |
| AI Demand Predictor | Tahap pengembangan berikutnya |
| Qwen Holiday Advisor terintegrasi | Tahap pengembangan berikutnya |
| Integrasi kalender dengan prediksi stok | Tahap pengembangan berikutnya |
| Notifikasi otomatis H-7 sampai H+1 ke Android | Direncanakan |
| Aplikasi Android secara menyeluruh | Dalam pengembangan |

## 15. Rencana Pengembangan Selanjutnya

Pengembangan berikutnya akan difokuskan pada:

1. Menyelesaikan integrasi Whisper dengan backend FastAPI.
2. Mengintegrasikan Qwen untuk ekstraksi data transaksi dari hasil transkripsi.
3. Menambahkan validasi dan konfirmasi transaksi sebelum penyimpanan.
4. Mengintegrasikan database lokal Room/SQLite pada aplikasi Android.
5. Mengembangkan mekanisme sinkronisasi data ketika perangkat kembali online.
6. Mengumpulkan dan menyiapkan data historis transaksi untuk kebutuhan prediksi.
7. Mengembangkan AI Demand Predictor.
8. Mengintegrasikan kalender Saka Bali dengan model prediksi permintaan barang.
9. Mengembangkan Qwen Holiday Advisor dengan basis pengetahuan hari raya dan kebutuhan upakara.
10. Mengembangkan notifikasi otomatis berdasarkan periode H-7 sampai H+1.
11. Mengembangkan antarmuka aplikasi Android agar mudah digunakan pedagang.
12. Melakukan pengujian sistem secara menyeluruh pada lingkungan penggunaan yang sesuai.

## 16. Dokumentasi Alur Kerja

Diagram alur kerja sistem IbuSmart dapat disimpan di dalam folder `docs`.

Contoh struktur:

```text
docs/
└── alur-kerja-ibu-smart.png
```

Untuk menampilkan diagram di README GitHub, gunakan:

```markdown
![Alur Kerja Sistem IbuSmart](docs/alur-kerja-ibu-smart.png)
```

## 17. Kesimpulan

IbuSmart dikembangkan sebagai sistem cerdas yang menggabungkan pencatatan transaksi berbasis suara, pengelolaan keuangan, prediksi kebutuhan stok, dan kalender Saka Bali.

Pada tahap pengembangan saat ini, tim telah berhasil membuat modul perhitungan proyeksi kalender Galungan dan Kuningan, menghubungkan backend FastAPI dengan PostgreSQL, menyimpan data kalender, serta menampilkan perhitungan periode H-7 sampai H+1 melalui Query Tool PostgreSQL.

Tim juga telah melakukan pengujian Whisper menggunakan 84 file audio dengan hasil WER dan CER yang dilaporkan sebesar 0,00%, serta melakukan pengembangan dan pengujian Qwen untuk mendukung pengolahan informasi transaksi.

Tahap selanjutnya adalah mengintegrasikan seluruh modul tersebut ke dalam satu sistem yang terhubung dengan aplikasi Android, sehingga IbuSmart dapat membantu pedagang dalam mencatat transaksi, memperkirakan kebutuhan stok, dan mempersiapkan usaha menjelang hari raya.

---

**IbuSmart – Membantu Pedagang Mengelola Usaha dengan Lebih Mudah dan Cerdas.**
