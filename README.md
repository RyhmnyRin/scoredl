# 🎼 scoredl

CLI tool sederhana berbasis Python untuk mengunduh partitur musik dari **MuseScore** dan mengonversinya langsung menjadi satu file PDF utuh berkualitas tinggi (lossless SVG).

![Python](https://img.shields.io/badge/python-3.x-blue)
![Playwright](https://img.shields.io/badge/automation-Playwright-2EAD33)

## Fitur

- 🔄 Auto-scroll & lazy load handling via Playwright
- 🖼️ Konversi vektor SVG murni langsung ke lembaran PDF (lossless)
- 🏷️ Penamaan file otomatis berdasarkan metadata judul lagu
- 🧹 Pembersihan file temporary otomatis setelah proses selesai

## Instalasi

**1. Clone repositori**
```bash
git clone https://github.com/RyhmnyRin/scoredl.git
cd scoredl
```

**2. Buat & aktifkan virtual environment**
```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate
```

**3. Pasang dependensi & browser**
```bash
pip install -r requirements.txt
playwright install chromium
```

## Penggunaan

Jalankan script dengan URL partitur target:

```bash
python main.py "https://musescore.com/user/xxxx/scores/yyyy"
```

Tentukan nama file output (opsional):

```bash
python main.py "https://musescore.com/user/xxxx/scores/yyyy" -o "NamaLagu.pdf"
```

| Argumen | Deskripsi | Wajib |
|---|---|---|
| `url` | URL partitur MuseScore | ✅ |
| `-o`, `--output` | Nama file PDF output | ❌ |

## Kontributor

- [RyhmnyRin](https://github.com/RyhmnyRin)
