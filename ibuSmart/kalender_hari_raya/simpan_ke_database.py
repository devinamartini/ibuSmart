
from datetime import date

from sqlalchemy.dialects.postgresql import insert

from backend.database import SessionLocal
from backend.models import Kalender
from kalender_hari_raya.hitung_kalender import hitung_kalender


def simpan_kalender():
    db = SessionLocal()

    try:
        tanggal_awal = date(2026, 6, 17)
        hasil = hitung_kalender(tanggal_awal, 7)

        for data in hasil:
            pernyataan = insert(Kalender).values(
                tanggal_acuan=date.fromisoformat(data["tanggal_acuan"]),
                siklus_ke=data["siklus_ke"],
                galungan=date.fromisoformat(data["galungan"]),
                kuningan=date.fromisoformat(data["kuningan"]),
                status_verifikasi=data["status_verifikasi"]
            )

            pernyataan = pernyataan.on_conflict_do_update(
                constraint="uq_kalender_acuan_siklus",
                set_={
                    "galungan": pernyataan.excluded.galungan,
                    "kuningan": pernyataan.excluded.kuningan,
                    "status_verifikasi": pernyataan.excluded.status_verifikasi
                }
            )

            db.execute(pernyataan)

        db.commit()
        print("Berhasil menyimpan atau memperbarui data kalender!")

    except Exception as e:
        db.rollback()
        print("Gagal menyimpan kalender:", e)

    finally:
        db.close()


if __name__ == "__main__":
    simpan_kalender()
