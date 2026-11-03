
from datetime import date

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert

from backend.database import Base, engine, get_db
from backend.models import Kalender

from kalender_hari_raya.hitung_kalender import hitung_kalender


# =====================================
# MEMBUAT TABEL DATABASE
# =====================================

Base.metadata.create_all(bind=engine)


# =====================================
# MEMBUAT APLIKASI FASTAPI
# =====================================

app = FastAPI(
    title="IbuSmart API",
    description="API Kalender Hari Raya Galungan dan Kuningan",
    version="1.0.0"
)


# =====================================
# MODEL REQUEST
# =====================================

class KalenderRequest(BaseModel):

    tanggal_galungan: date

    jumlah_siklus: int = Field(
        default=20,
        ge=1,
        le=100
    )


# =====================================
# ENDPOINT ROOT
# =====================================

@app.get("/")
def home():

    return {
        "status": "success",
        "pesan": "Backend IbuSmart berhasil berjalan"
    }


# =====================================
# ENDPOINT HITUNG DAN SIMPAN KALENDER
# =====================================

@app.post("/kalender/hitung")
def endpoint_hitung_kalender(
    request: KalenderRequest,
    db: Session = Depends(get_db)
):

    try:

        # 1. Menghitung kalender Galungan dan Kuningan
        hasil = hitung_kalender(
            tanggal_galungan_awal=request.tanggal_galungan,
            jumlah_siklus=request.jumlah_siklus
        )

        # 2. Menyimpan atau memperbarui data kalender
        for item in hasil:

            pernyataan = insert(Kalender).values(
                tanggal_acuan=request.tanggal_galungan,
                siklus_ke=item["siklus_ke"],
                galungan=date.fromisoformat(item["galungan"]),
                kuningan=date.fromisoformat(item["kuningan"]),
                status_verifikasi=item["status_verifikasi"]
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

        # 3. Menyimpan perubahan ke PostgreSQL
        db.commit()

        # 4. Mengirim hasil ke pengguna
        return {
            "status": "success",
            "pesan": "Kalender berhasil dihitung dan disimpan ke PostgreSQL",
            "jumlah_siklus": len(hasil),
            "data_kalender": hasil,
            "database": {
                "nama_database": "ibuSmart_db",
                "nama_tabel": "kalender",
                "tersimpan": True
            }
        }

    except SQLAlchemyError:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Gagal menyimpan data ke PostgreSQL"
        )

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Terjadi kesalahan saat menghitung kalender"
        )


# =====================================
# ENDPOINT MELIHAT SELURUH DATA KALENDER
# =====================================

@app.get("/kalender")
def ambil_semua_kalender(
    db: Session = Depends(get_db)
):

    data = db.query(Kalender).order_by(
        Kalender.tanggal_acuan,
        Kalender.siklus_ke
    ).all()

    return {
        "status": "success",
        "total_data": len(data),
        "data_kalender": [
            {
                "id": item.id,
                "tanggal_acuan": item.tanggal_acuan.isoformat(),
                "siklus_ke": item.siklus_ke,
                "galungan": item.galungan.isoformat(),
                "kuningan": item.kuningan.isoformat(),
                "status_verifikasi": item.status_verifikasi
            }
            for item in data
        ]
    }


# =====================================
# ENDPOINT MELIHAT KALENDER BERDASARKAN
# TANGGAL ACUAN
# =====================================

@app.get("/kalender/{tanggal_acuan}")
def ambil_kalender_berdasarkan_tanggal(
    tanggal_acuan: date,
    db: Session = Depends(get_db)
):

    data = db.query(Kalender).filter(
        Kalender.tanggal_acuan == tanggal_acuan
    ).order_by(
        Kalender.siklus_ke
    ).all()

    if not data:

        raise HTTPException(
            status_code=404,
            detail="Data kalender tidak ditemukan"
        )

    return {
        "status": "success",
        "tanggal_acuan": tanggal_acuan.isoformat(),
        "total_data": len(data),
        "data_kalender": [
            {
                "id": item.id,
                "siklus_ke": item.siklus_ke,
                "galungan": item.galungan.isoformat(),
                "kuningan": item.kuningan.isoformat(),
                "status_verifikasi": item.status_verifikasi
            }
            for item in data
        ]
    }
