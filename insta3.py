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
install_and_import("lxml")
install_and_import("requests")

from bs4 import BeautifulSoup
import requests

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

# --- Parse saved_collections.html ---
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

# --- Function to scrape og:image ---
def download_first_image(url, folder):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Failed to access {url}")
            return

        soup = BeautifulSoup(response.text, "lxml")
        og_image = soup.find("meta", property="og:image")

        if og_image and og_image.get("content"):
            img_url = og_image["content"]
            img_data = requests.get(img_url, timeout=10).content

            filename = os.path.join(folder, url.strip("/").split("/")[-1] + ".jpg")
            with open(filename, "wb") as f:
                f.write(img_data)

            print(f"✅ Saved first image from {url}")
        else:
            print(f"⚠️ No image found at {url}")

    except Exception as e:
        print(f"⚠️ Error fetching {url}: {e}")

# --- Downloading ---
for col in collections:
    folder_path = os.path.join(output_dir, col["name"])
    os.makedirs(folder_path, exist_ok=True)

    print(f"\n⬇️ Downloading first images from collection: {col['name']}")

    for link in col["links"]:
        download_first_image(link, folder_path)

print("\n🎉 Done! All collections downloaded into:", output_dir)
input("\n✅ All done! Press Enter to exit...")
