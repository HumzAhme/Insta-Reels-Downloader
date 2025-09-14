import os
import sys
import subprocess
import socket
import time
from tkinter import Tk, filedialog

# --- Auto install required libraries ---
def install_and_import(package, import_name=None):
    try:
        __import__(import_name or package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[import_name or package] = __import__(import_name or package)

install_and_import("beautifulsoup4", "bs4")
install_and_import("yt_dlp")
install_and_import("lxml")

from bs4 import BeautifulSoup
import yt_dlp

# --- Internet waiting helper ---
def wait_for_connection(host="www.instagram.com", port=80, delay=5):
    """Wait until the internet/IP is reachable before continuing."""
    while True:
        try:
            socket.create_connection((host, port), timeout=5)
            return  # connection successful
        except OSError:
            print(f"🌐 No internet/IP connection. Retrying in {delay} seconds...")
            time.sleep(delay)

# --- Ask user to pick saved_collections.html ---
Tk().withdraw()
html_file = filedialog.askopenfilename(
    title="Select saved_collections.html file",
    filetypes=[("HTML files", "*.html")]
)

if not html_file:
    print("❌ No file selected. Exiting.")
    sys.exit()

print(f"📂 Selected file: {html_file}")

# --- Output folder ---
output_dir = os.path.join(os.path.dirname(html_file), "Instagram_Collections")
os.makedirs(output_dir, exist_ok=True)

# --- Parse HTML file ---
with open(html_file, "r", encoding="utf-8") as f:
    try:
        soup = BeautifulSoup(f, "lxml")
    except Exception:
        print("⚠️ lxml not available, falling back to html.parser")
        soup = BeautifulSoup(f, "html.parser")

collections = []
current_collection = None

for block in soup.find_all("div", class_="pam"):
    header = block.find("h2")
    if header and "Collection" in header.get_text():
        table = block.find("table")
        if table:
            name_row = table.find("div")
            if name_row:
                collection_name = name_row.get_text(strip=True)
                current_collection = {"name": collection_name, "links": []}
                collections.append(current_collection)
        continue

    link = block.find("a", href=True)
    if link and current_collection:
        current_collection["links"].append(link["href"])

# --- Summary ---
for col in collections:
    print(f"📌 Collection: {col['name']} ({len(col['links'])} links)")

if not collections:
    print("⚠️ No collections found in the file. Exiting.")
    sys.exit()

# --- Cookie Handling ---
cookie_file = os.path.join(os.path.dirname(__file__), "cookies.txt")
use_cookies = os.path.exists(cookie_file)

if use_cookies:
    print("🍪 Using cookies.txt for authentication.")
else:
    print("⚠️ No cookies.txt found. Only some public reels may download.")

# --- yt-dlp Downloader with retry + logging + skip existing ---
def download_post(url, folder, fail_log):
    ydl_opts = {
        "outtmpl": os.path.join(folder, "%(id)s.%(ext)s"),
        "quiet": True,
        "noplaylist": True,
        "merge_output_format": "mp4",
    }
    if use_cookies:
        ydl_opts["cookiefile"] = cookie_file

    # Pre-check if already downloaded
    info_opts = {"quiet": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info.get("id")
            ext = info.get("ext", "mp4")
            out_file = os.path.join(folder, f"{video_id}.{ext}")
            if os.path.exists(out_file):
                print(f"⏭ Skipped (already exists): {url}")
                return
    except Exception as e:
        print(f"⚠️ Could not pre-check {url}: {e}")

    while True:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"✅ Downloaded: {url}")
            break  # success → exit loop
        except Exception as e:
            err_str = str(e).lower()
            if "getaddrinfo failed" in err_str or "http error" in err_str or "timed out" in err_str:
                print(f"⚠️ Network/IP error for {url}, waiting to retry...")
                wait_for_connection()
                continue  # retry same post
            elif "login" in err_str or "empty media response" in err_str:
                print(f"🔒 Private or inaccessible post: {url}")
                with open(fail_log, "a", encoding="utf-8") as f:
                    f.write(url + "\n")
                break  # skip permanently
            else:
                print(f"⚠️ Failed to download {url}: {e}")
                with open(fail_log, "a", encoding="utf-8") as f:
                    f.write(url + "\n")
                break  # skip permanently

# --- Downloading ---
for col in collections:
    folder_path = os.path.join(output_dir, col["name"])
    os.makedirs(folder_path, exist_ok=True)

    fail_log = os.path.join(folder_path, f"{col['name']}_failed.txt")

    print(f"\n⬇️ Downloading collection: {col['name']} ({len(col['links'])} posts)")

    for link in col["links"]:
        download_post(link, folder_path, fail_log)

print("\n🎉 Done! All collections downloaded into:", output_dir)
input("\n✅ All done! Press Enter to exit...")
