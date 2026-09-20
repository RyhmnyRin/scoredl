import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from pypdf import PdfWriter, PdfReader

def compile_svgs_to_pdf(svg_files: list, output_pdf_path: str, title: str = "Sheet Music"):
    print(f"[*] Mengonversi {len(svg_files)} halaman SVG ke PDF...")
    temp_pdf_pages = []

    # 1. Konversi tiap file SVG menjadi PDF lembaran sementara
    for idx, svg_path in enumerate(svg_files):
        print(f"[*] Memproses lembar {idx + 1}/{len(svg_files)}: {svg_path}")
        drawing = svg2rlg(svg_path)
        page_pdf_path = svg_path.replace(".svg", ".pdf")
        renderPDF.drawToFile(drawing, page_pdf_path)
        temp_pdf_pages.append(page_pdf_path)

    # 2. Gabungkan lembaran PDF individual ke dalam satu file utuh
    print("[*] Menggabungkan seluruh lembar ke file akhir...")
    writer = PdfWriter()

    for pdf_page in temp_pdf_pages:
        reader = PdfReader(pdf_page)
        for page in reader.pages:
            writer.add_page(page)

    # 3. Sematkan Metadata Dokumen (Sesuai ide awal lo buat preserve copyright)
    writer.add_metadata({
        "/Title": title,
        "/Producer": "Score-dl CLI Engine"
    })

    # Simpan file hasil akhir
    with open(output_pdf_path, "wb") as f_out:
        writer.write(f_out)

    # 4. Cleanup: Hapus file PDF per-halaman sementara
    for temp_pdf in temp_pdf_pages:
        try:
            os.remove(temp_pdf)
        except Exception:
            pass

    print(f"[✓] Selesai! Partitur utuh berhasil disimpan ke: {output_pdf_path}")

if __name__ == "__main__":
    # Test manual builder menggunakan file SVG yang sudah lo extract
    folder = "temp_svgs"
    files = [os.path.join(folder, f"page_{i}.svg") for i in range(6)]
    compile_svgs_to_pdf(files, "Non-Breath-Oblige.pdf", title="Non-Breath Oblige - PinocchioP")