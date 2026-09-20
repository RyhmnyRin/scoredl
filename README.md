# scoredl

CLI tool sederhana berbasis Python untuk mengunduh partitur musik dari MuseScore dan mengonversinya langsung menjadi satu file PDF utuh berkualitas tinggi (lossless SVG).

## Fitur
- Auto-scroll & lazy load handling via Playwright.
- Konversi vektor SVG murni langsung ke lembaran PDF.
- Penamaan otomatis berdasarkan metadata judul lagu.
- Pembersihan file temporary otomatis setelah proses selesai.

## Instalasi

1. Clone repositori ini:
   ```bash
   git clone [https://github.com/RyhmnyRin/scoredl.git](https://github.com/RyhmnyRin/scoredl.git)
   cd scoredl
2. Buat dan aktifkan virtual environment:
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows PowerShell
3. Pasang dependensi dan browser:
   pip install -r requirements.txt
   playwright install chromium

Cara Penggunaan
Cukup jalankan script dengan memasukkan URL partitur target:
- python main.py "[https://musescore.com/user/xxxx/scores/yyyy](https://musescore.com/user/xxxx/scores/yyyy)"
Opsi tambahan untuk menentukan nama output file:
2. python main.py "[https://musescore.com/user/xxxx/scores/yyyy](https://musescore.com/user/xxxx/scores/yyyy)" -o "NamaLagu.pdf"
