"""Ekstraksi transaksi: teks hasil Whisper -> JSON transaksi memakai Qwen.

Model dimuat sekali saat pertama dipakai. Nama model dapat diganti lewat
variabel lingkungan QWEN_MODEL, misalnya:
    set QWEN_MODEL=Qwen/Qwen2.5-3B-Instruct

Kebutuhan: pip install transformers torch
"""

import json
import os
import re
from pathlib import Path

from qwen.validasi_transaksi import validasi_transaksi

NAMA_MODEL = os.getenv("QWEN_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")
FILE_PROMPT = Path(__file__).resolve().parent / "prompt_ekstraksi.txt"

_tokenizer = None
_model = None


def _muat_model():
    global _tokenizer, _model
    if _model is None:
        from transformers import AutoModelForCausalLM, AutoTokenizer

        _tokenizer = AutoTokenizer.from_pretrained(NAMA_MODEL)
        _model = AutoModelForCausalLM.from_pretrained(NAMA_MODEL, torch_dtype="auto")
    return _tokenizer, _model


def panggil_qwen(teks: str) -> str:
    """Mengirim teks transaksi ke Qwen dan mengembalikan keluaran mentahnya."""
    tokenizer, model = _muat_model()
    instruksi = FILE_PROMPT.read_text(encoding="utf-8")

    pesan = [
        {"role": "system", "content": instruksi},
        {"role": "user", "content": f"Kalimat: {teks}\nJSON:"},
    ]
    masukan = tokenizer.apply_chat_template(
        pesan, add_generation_prompt=True, return_tensors="pt"
    ).to(model.device)

    keluaran = model.generate(masukan, max_new_tokens=128, do_sample=False)
    baru = keluaran[0][masukan.shape[1]:]
    return tokenizer.decode(baru, skip_special_tokens=True).strip()


def ambil_json(teks: str):
    """Mengambil objek JSON pertama dari keluaran model. None jika gagal."""
    cocok = re.search(r"\{.*?\}", teks, flags=re.DOTALL)
    if not cocok:
        return None
    try:
        return json.loads(cocok.group(0))
    except json.JSONDecodeError:
        return None


def ekstrak_transaksi(teks: str) -> dict:
    """Alur lengkap: Qwen -> parse JSON -> validasi.

    status 'valid'            : siap disimpan ke database
    status 'perlu_konfirmasi' : data belum lengkap/valid, tanyakan ke pedagang
    """
    mentah = panggil_qwen(teks)
    data = ambil_json(mentah)

    if data is None:
        return {
            "status": "perlu_konfirmasi",
            "transaksi": None,
            "masalah": ["Keluaran model bukan JSON yang valid."],
            "keluaran_mentah": mentah,
        }

    valid, bersih, masalah = validasi_transaksi(data)
    return {
        "status": "valid" if valid else "perlu_konfirmasi",
        "transaksi": bersih if valid else data,
        "masalah": masalah,
        "keluaran_mentah": mentah,
    }


if __name__ == "__main__":
    contoh = "jual janur lima ikat lima puluh ribu"
    print(json.dumps(ekstrak_transaksi(contoh), ensure_ascii=False, indent=2))
