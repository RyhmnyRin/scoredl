# 🎼 scoredl

CLI tool sederhana berbasis Python untuk mengunduh partitur musik dari **MuseScore** dan mengonversinya langsung menjadi satu file PDF utuh berkualitas tinggi (lossless SVG).

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Playwright](https://img.shields.io/badge/automation-Playwright-2EAD33)

## Fitur

- 🔄 Auto-scroll & lazy load handling via Playwright
- 🖼️ Konversi vektor SVG murni langsung ke lembaran PDF (lossless)
- 🏷️ Penamaan file otomatis berdasarkan metadata judul lagu
- 📂 Opsi simpan file SVG mentah ke subfolder terpisah (`--keep-svg`)
- 🧹 Pembersihan file temporary otomatis setelah proses selesai

## Instalasi

**Metode 1 — via PyPI (disarankan)**
```bash
pip install scoredl
playwright install chromium
```

**Metode 2 — manual (mode developer)**
```bash
git clone https://github.com/RyhmnyRin/scoredl.git
cd scoredl
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

pip install -e .
playwright install chromium
```

## Penggunaan

```bash
scoredl "https://musescore.com/user/xxxx/scores/yyyy"
```

Tentukan nama file output:
```bash
scoredl "https://musescore.com/user/xxxx/scores/yyyy" -o "NamaLagu.pdf"
```

Simpan juga file SVG mentahnya (tersimpan di `saved_svgs/<Judul Lagu>/`):
```bash
scoredl "https://musescore.com/user/xxxx/scores/yyyy" --keep-svg
```

## Argumen CLI

| Argumen | Opsi Panjang | Deskripsi | Wajib |
|---|---|---|---|
| `url` | – | URL partitur MuseScore | ✅ |
| `-o` | `--output` | Nama file PDF output | ❌ |
| – | `--keep-svg` | Simpan file SVG mentah per halaman | ❌ |

## ⚠️ Disclaimer

Tool ini dibuat murni untuk **tujuan edukasi dan pembelajaran teknik automasi browser**. Pengembang tidak bertanggung jawab atas penyalahgunaan software ini untuk pelanggaran hak cipta pihak ketiga. Harap dukung para musisi dan arranger dengan membeli lisensi resmi di MuseScore.

## Kontributor

- [RyhmnyRin](https://github.com/RyhmnyRin)
