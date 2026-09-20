import os
import random
import time
from playwright.sync_api import sync_playwright

def extract_score_data(score_url: str, output_dir: str = "temp_svgs"):
    os.makedirs(output_dir, exist_ok=True)
    svg_files = []
    metadata = {
        "title": "Unknown Title",
        "pages": 0
    }

    user_data_dir = os.path.join(os.getcwd(), ".browser_session")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ],
            viewport={"width": 1280, "height": 850}
        )
        
        page = context.pages[0] if context.pages else context.new_page()

        # Intercept dan simpan konten SVG langsung dari memory browser
        seen_svg_urls = set()
        downloaded_files = []

        def handle_response(response):
            url = response.url
            if "scoredata" in url and ".svg" in url:
                if url in seen_svg_urls:
                    return
                seen_svg_urls.add(url)

                try:
                    svg_content = response.body()
                    # Beri nama unik sementara berdasarkan index URL yang ditemukan
                    idx = len(seen_svg_urls) - 1
                    file_path = os.path.join(output_dir, f"page_{idx}.svg")

                    with open(file_path, "wb") as f:
                        f.write(svg_content)

                    print(f"[+] Berhasil menyimpan lembar -> {file_path}")
                except Exception as e:
                    print(f"[!] Gagal ekstrak SVG: {e}")

        page.on("response", handle_response)

        print(f"[*] Mengakses target: {score_url}")
        page.goto(score_url, wait_until="domcontentloaded", timeout=60000)

        # Pemeriksaan Cloudflare
        print("[*] Memeriksa proteksi Cloudflare...")
        for _ in range(15):
            title = page.title()
            if "Just a moment" not in title and title.strip() != "":
                break
            time.sleep(1)

        try:
            metadata["title"] = page.title().split("|")[0].strip()
        except Exception:
            pass

        print(f"[*] Judul: {metadata['title']}")
        print("[*] Menunggu elemen lembar partitur...")
        
        try:
            page.wait_for_selector("#jmuse-scroller-component", timeout=15000)
            time.sleep(2)
        except Exception:
            pass

        print("[*] Menjalankan human scrolling...")

        total_height = page.evaluate("""() => {
            const scroller = document.querySelector('#jmuse-scroller-component');
            return scroller ? scroller.scrollHeight : document.body.scrollHeight;
        }""")

        current_scroll = 0
        step_size = 850

        while current_scroll < total_height:
            current_scroll += step_size
            
            page.evaluate(f"""(scrollVal) => {{
                const scroller = document.querySelector('#jmuse-scroller-component');
                if (scroller) {{
                    scroller.scrollTo({{
                        top: scrollVal,
                        behavior: 'smooth'
                    }});
                }} else {{
                    window.scrollTo({{
                        top: scrollVal,
                        behavior: 'smooth'
                    }});
                }}
            }}""", current_scroll)

            time.sleep(1)

            total_height = page.evaluate("""() => {
                const scroller = document.querySelector('#jmuse-scroller-component');
                return scroller ? scroller.scrollHeight : document.body.scrollHeight;
            }""")

        print("[*] Menunggu finalisasi asset...")
        time.sleep(0.4)

        metadata["pages"] = len(svg_files)
        context.close()
        
            # Ambil file fisik langsung dari disk agar tidak ada duplikat memori
        all_svgs = [
            os.path.join(output_dir, f) 
            for f in os.listdir(output_dir) 
            if f.endswith(".svg")
        ]
        
        # Urutkan berdasarkan angka halaman asli (page_0, page_1, dst)
        import re
        all_svgs.sort(key=lambda x: int(re.search(r'page_(\d+)', x).group(1)))
        
        # Update total halaman valid yang sebenarnya tersimpan
        metadata["pages"] = len(all_svgs)
        svg_files = all_svgs

    return metadata, svg_files

if __name__ == "__main__":
    target = "https://musescore.com/user/40260509/scores/7121958"
    meta, files = extract_score_data(target)
    print("\n" + "=" * 40)
    print(f"Hasil Ekstraksi:")
    print(f"Judul : {meta['title']}")
    print(f"Total : {meta['pages']} file SVG tersimpan di folder lokal")
    print("=" * 40)