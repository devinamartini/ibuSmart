"""Evaluasi Qwen pada data uji ekstraksi transaksi.

Menjalankan Qwen pada setiap kalimat di data_uji/contoh_transkripsi.jsonl,
membandingkan hasilnya dengan 'harapan', lalu menulis laporan ke
hasil_evaluasi.md. Angka di laporan HANYA berasal dari eksekusi nyata skrip ini.

Cara menjalankan (dari folder utama proyek):
    python -m qwen.evaluasi_qwen
    python -m qwen.evaluasi_qwen data_uji/contoh_transkripsi.jsonl

Kebutuhan: pip install transformers torch
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from qwen.ekstrak_transaksi import NAMA_MODEL, ekstrak_transaksi

FOLDER = Path(__file__).resolve().parent
FIELD = ["tipe", "barang", "satuan", "jumlah", "nominal"]


def bandingkan(hasil, harapan):
    """Mengembalikan daftar field yang berbeda dari harapan."""
    if hasil is None:
        return list(FIELD)
    salah = []
    for f in FIELD:
        h = hasil.get(f)
        if isinstance(h, str):
            h = h.strip().lower()
        if h != harapan.get(f):
            salah.append(f)
    return salah


def muat_data(path):
    data = []
    with open(path, encoding="utf-8") as fh:
        for baris in fh:
            baris = baris.strip()
            if baris:
                data.append(json.loads(baris))
    return data


def evaluasi(path_data):
    data = muat_data(path_data)
    rincian = []
    cocok_penuh = 0
    json_ok = 0
    valid_ok = 0
    benar_per_field = {f: 0 for f in FIELD}

    for item in data:
        hasil = ekstrak_transaksi(item["teks"])
        trx = hasil["transaksi"]
        if trx is not None:
            json_ok += 1
        if hasil["status"] == "valid":
            valid_ok += 1
        salah = bandingkan(trx, item["harapan"])
        for f in FIELD:
            if f not in salah:
                benar_per_field[f] += 1
        if not salah:
            cocok_penuh += 1
        rincian.append((item["teks"], item["harapan"], trx, salah))

    return {
        "n": len(data),
        "cocok_penuh": cocok_penuh,
        "json_ok": json_ok,
        "valid_ok": valid_ok,
        "per_field": benar_per_field,
        "rincian": rincian,
    }


def tulis_laporan(r, path_data, path_laporan):
    n = r["n"]
    pct = lambda x: f"{x / n * 100:.1f}%"
    baris = [
        "# Hasil Evaluasi Qwen - Ekstraksi Transaksi",
        "",
        f"- Tanggal evaluasi: {datetime.now():%Y-%m-%d %H:%M}",
        f"- Model: `{NAMA_MODEL}`",
        f"- Data uji: `{Path(path_data).name}` ({n} kalimat)",
        "",
        "## Ringkasan",
        "",
        "| Metrik | Hasil |",
        "|---|---|",
        f"| Keluaran berupa JSON yang dapat dibaca | {r['json_ok']}/{n} ({pct(r['json_ok'])}) |",
        f"| Lolos validasi (status valid) | {r['valid_ok']}/{n} ({pct(r['valid_ok'])}) |",
        f"| Seluruh field cocok dengan harapan | {r['cocok_penuh']}/{n} ({pct(r['cocok_penuh'])}) |",
        "",
        "## Akurasi per field",
        "",
        "| Field | Benar |",
        "|---|---|",
    ]
    for f in FIELD:
        baris.append(f"| {f} | {r['per_field'][f]}/{n} ({pct(r['per_field'][f])}) |")

    baris += ["", "## Kasus yang salah", ""]
    salah_semua = [x for x in r["rincian"] if x[3]]
    if not salah_semua:
        baris.append("Tidak ada.")
    for teks, harapan, hasil, salah in salah_semua:
        baris += [
            f"- Kalimat: `{teks}`",
            f"  - Harapan: `{json.dumps(harapan, ensure_ascii=False)}`",
            f"  - Hasil: `{json.dumps(hasil, ensure_ascii=False)}`",
            f"  - Field berbeda: {', '.join(salah)}",
        ]

    baris += [
        "",
        "## Catatan",
        "",
        "- Data uji berukuran kecil, jadi hasil ini hanya gambaran awal.",
        "- Evaluasi memakai teks yang sudah bersih, belum memakai keluaran Whisper yang mungkin berisi salah dengar.",
        "",
    ]
    Path(path_laporan).write_text("\n".join(baris), encoding="utf-8")


if __name__ == "__main__":
    path_data = sys.argv[1] if len(sys.argv) > 1 else FOLDER / "data_uji" / "contoh_transkripsi.jsonl"
    hasil = evaluasi(path_data)
    tulis_laporan(hasil, path_data, FOLDER / "hasil_evaluasi.md")
    print(f"Selesai. {hasil['cocok_penuh']}/{hasil['n']} cocok penuh. Laporan: qwen/hasil_evaluasi.md")
