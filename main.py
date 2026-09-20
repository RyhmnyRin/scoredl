import argparse
import os
import re
import shutil
from extractor import extract_score_data
from builder import compile_svgs_to_pdf

def sanitize_filename(name: str) -> str:
    # Membersihkan karakter ilegal untuk nama file Windows/Linux
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def main():
    parser = argparse.ArgumentParser(
        prog="Score-dl",
        description="CLI Tool untuk mengekstrak partitur MuseScore menjadi PDF berkualitas tinggi."
    )
    parser.add_argument(
        "url", 
        type=str, 
        help="URL lembar musik MuseScore target"
    )
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        default=None, 
        help="Nama file PDF output (opsional, default: sesuai judul partitur)"
    )
    parser.add_argument(
        "--keep-svg",
        action="store_true",
        help="Simpan file SVG sementara (default: dihapus setelah selesai)"
    )

    args = parser.parse_args()

    print("=" * 50)
    print("       Score-dl - MuseScore Sheet Extractor       ")
    print("=" * 50)

    # 1. Ekstraksi Data
    temp_dir = "temp_svgs"
    meta, svg_files = extract_score_data(args.url, output_dir=temp_dir)

    if not svg_files:
        print("[!] Gagal mengekstrak halaman partitur. Proses dibatalkan.")
        return

    # 2. Tentukan Nama Output
    if args.output:
        final_pdf_name = args.output if args.output.endswith(".pdf") else f"{args.output}.pdf"
    else:
        clean_title = sanitize_filename(meta["title"])
        final_pdf_name = f"{clean_title}.pdf"

    # 3. Compile ke PDF
    compile_svgs_to_pdf(svg_files, final_pdf_name, title=meta["title"])

    # 4. Housekeeping / Cleanup
    if not args.keep_svg:
        print("[*] Membersihkan cache file SVG sementara...")
        shutil.rmtree(temp_dir, ignore_errors=True)

    print("\n" + "=" * 50)
    print(f"[✓] SUKSES! Partitur siap cetak: {final_pdf_name}")
    print("=" * 50)

if __name__ == "__main__":
    main()