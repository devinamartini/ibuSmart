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

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    tanggal_acuan = Column(
        Date,
        nullable=False
    )

    siklus_ke = Column(
        Integer,
        nullable=False
    )

    galungan = Column(
        Date,
        nullable=False
    )

    kuningan = Column(
        Date,
        nullable=False
    )

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