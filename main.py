import argparse
import os
import re
import shutil
from extractor import extract_score_data
from builder import compile_svgs_to_pdf

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def main():
    parser = argparse.ArgumentParser(
        prog="scoredl",
        description="CLI Tool untuk mengekstrak partitur MuseScore menjadi PDF berkualitas tinggi."
    )
    parser.add_argument("url", type=str, help="URL lembar musik MuseScore target")
    parser.add_argument("-o", "--output", type=str, default=None, help="Nama file PDF output")
    parser.add_argument("--keep-svg", action="store_true", help="Simpan file SVG ke folder tersendiri sesuai judul")

    args = parser.parse_args()

    print("=" * 50)
    print("       Score-dl - MuseScore Sheet Extractor       ")
    print("=" * 50)

    # Gunakan folder sementara unik
    temp_dir = ".temp_extract"
    meta, svg_files = extract_score_data(args.url, output_dir=temp_dir)

    if not svg_files:
        print("[!] Gagal mengekstrak halaman partitur. Proses dibatalkan.")
        return

    clean_title = sanitize_filename(meta["title"])
    final_pdf_name = args.output if args.output else f"{clean_title}.pdf"
    if not final_pdf_name.endswith(".pdf"):
        final_pdf_name += ".pdf"

    # Compile ke PDF
    compile_svgs_to_pdf(svg_files, final_pdf_name, title=meta["title"])

    # Penanganan folder SVG jika user memilih --keep-svg
    if args.keep_svg:
        # Buat folder khusus sesuai judul lagu agar tidak tertukar
        svg_dest_dir = os.path.join("saved_svgs", clean_title)
        os.makedirs(svg_dest_dir, exist_ok=True)
        
        for idx, old_path in enumerate(svg_files):
            new_file_name = f"{clean_title}_page_{idx + 1}.svg"
            new_path = os.path.join(svg_dest_dir, new_file_name)
            shutil.copy2(old_path, new_path)
            
        print(f"[✓] Salinan SVG resolusi tinggi tersimpan di: {svg_dest_dir}")

    # Bersihkan folder sementara
    shutil.rmtree(temp_dir, ignore_errors=True)

    print("\n" + "=" * 50)
    print(f"[✓] SUKSES! Partitur siap cetak: {final_pdf_name}")
    print("=" * 50)

if __name__ == "__main__":
    main()