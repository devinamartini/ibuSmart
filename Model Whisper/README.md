# Whisper Small - Kustom STT Bahasa Bali (Domain Navigasi & Pasar)

Model ini adalah hasil *fine-tuning* (adaptasi kustom) dari **OpenAI Whisper-Small** menggunakan teknik **LoRA (Low-Rank Adaptation)** untuk mendeteksi ucapan frasa, kosakata, dan dialek lokal Bahasa Bali dalam kondisi bising latar belakang.

## Detail Model
- **Model Dasar (Base Model):** `openai/whisper-small`
- **Metode Pelatihan:** PEFT / LoRA (Hanya melatih ~1.44% parameter modul `q_proj` dan `v_proj`)
- **Bahasa Target:** Bahasa Bali (Diintegrasikan menggunakan token dasar Bahasa Indonesia)
- **Framework Pendukung:** PEFT 0.21.2, Transformers, PyTorch

## Domain Penggunaan (Uses)
Model ini dikustomisasi khusus untuk dua kebutuhan utama:
1. **Domain Pasar Bali:** Mengenali kosakata belanja lokal seperti *Canang, Gemitir, Kwangen, Sodan, Pejati, Janur*, beserta nominal angka rupiah.
2. **Domain Navigasi:** Mengenali frasa arah perintah navigasi jalan (seperti *ngiring, memargi, nuju, belok kiwa/tenawan*).

## Hasil Evaluasi Akurasi (Evaluation Results)
Pengujian mandiri dilakukan menggunakan metode *Blind Test* pada dataset asing yang belum pernah dipelajari model sebelumnya:

| Domain Pengujian | Word Error Rate (WER) | Akurasi Kata (Accuracy) |
| :--- | :---: | :---: |
| **Domain Jual-Beli Pasar Bali** | **1.53%** | ⭐️ **98.47%** |
| **Domain Instruksi Navigasi** | **58.97%** | ⭐️ **41.03%** |

*Catatan: Model sangat kuat pada domain pasar, namun membutuhkan perluasan korpus teks perintah navigasi formal pada pengembangan selanjutnya.*

## Spesifikasi Teknis Training
- **Hardware:** GPU NVIDIA T4 (Google Colab Environment)
- **Hyperparameters:** 25 Epochs, Batch Size 4, Learning Rate 1e-4, Warmup Steps 10, Mixed Precision (FP16).
