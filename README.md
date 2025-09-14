# Instagram Collections Downloader

This repository contains Python scripts to download different types of Instagram content from your **saved collections** using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

The main script parses the `saved_collections.html` file that you can export from Instagram, organizes collections into folders, and downloads each post.

---

## ✨ Features

- 📂 Organizes downloaded posts by collection name  
- 🍪 Supports Instagram authentication via `cookies.txt`  
- ⚡ Auto-installs required Python libraries if missing  
- 🎥 Downloads videos, reels, and images with `yt-dlp`  
- 🖱️ GUI file picker for selecting your exported `saved_collections.html`  

---

## 📋 Scripts in This Repo

- **`instagram_collections_downloader.py`** → Downloads posts from `saved_collections.html`  
- **`insta3.py`** → Downloads **thumbnails** from Instagram posts  
- **`insta4.py`** → Downloads **reels** directly  

---

## 📋 Requirements

- Python **3.8+**  
- Exported `saved_collections.html` file from Instagram  
- (Optional) `cookies.txt` file for private or restricted posts  

---

## ⚙️ Installation

Clone or download this repository:

```bash
git clone https://github.com/yourusername/instagram-collections-downloader.git
cd instagram-collections-downloader
