
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
