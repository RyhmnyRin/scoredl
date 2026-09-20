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
        def handle_response(response):
            url = response.url
            if "scoredata" in url and ".svg" in url:
                try:
                    # Ambil bytes data SVG langsung tanpa download ulang
                    svg_content = response.body()
                    page_index = len(svg_files)
                    file_path = os.path.join(output_dir, f"page_{page_index}.svg")
                    
                    with open(file_path, "wb") as f:
                        f.write(svg_content)
                    
                    svg_files.append(file_path)
                    print(f"[+] Berhasil menyimpan halaman {page_index + 1} -> {file_path}")
                except Exception as e:
                    print(f"[!] Gagal mengekstrak body SVG: {e}")

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
        step_size = 400

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

            time.sleep(random.uniform(1.2, 1.8))

            total_height = page.evaluate("""() => {
                const scroller = document.querySelector('#jmuse-scroller-component');
                return scroller ? scroller.scrollHeight : document.body.scrollHeight;
            }""")

        print("[*] Menunggu finalisasi asset...")
        time.sleep(3)

        metadata["pages"] = len(svg_files)
        context.close()

    return metadata, svg_files

if __name__ == "__main__":
    target = "https://musescore.com/user/40260509/scores/7121958"
    meta, files = extract_score_data(target)
    print("\n" + "=" * 40)
    print(f"Hasil Ekstraksi:")
    print(f"Judul : {meta['title']}")
    print(f"Total : {meta['pages']} file SVG tersimpan di folder lokal")
    print("=" * 40)