import os
import sys
import subprocess
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
    soup = BeautifulSoup(f, "lxml")

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

# --- yt-dlp Downloader ---
def download_post(url, folder):
    ydl_opts = {
        "outtmpl": os.path.join(folder, "%(id)s.%(ext)s"),
        "quiet": False,
        "noplaylist": True,
        "merge_output_format": "mp4",
    }
    if use_cookies:
        ydl_opts["cookiefile"] = cookie_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"✅ Downloaded: {url}")
    except Exception as e:
        if "login" in str(e).lower() or "empty media response" in str(e).lower():
            print(f"🔒 Private or inaccessible post: {url}")
        else:
            print(f"⚠️ Failed to download {url}: {e}")

# --- Downloading ---
for col in collections:
    folder_path = os.path.join(output_dir, col["name"])
    os.makedirs(folder_path, exist_ok=True)

    print(f"\n⬇️ Downloading collection: {col['name']} ({len(col['links'])} posts)")

    for link in col["links"]:
        download_post(link, folder_path)

print("\n🎉 Done! All collections downloaded into:", output_dir)
input("\n✅ All done! Press Enter to exit...")
