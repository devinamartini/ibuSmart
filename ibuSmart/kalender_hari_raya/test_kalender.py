from datetime import date
from kalender_hari_raya.hitung_kalender import hitung_kalender

tanggal_awal = date(2026, 6, 17)
jumlah_siklus = 7

hasil = hitung_kalender(tanggal_awal, jumlah_siklus)

for data in hasil:
    print(data)