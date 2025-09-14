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




## 🔮 Future Additions

Planned improvements for upcoming versions of the scripts:

### 1. Save skipped links into text files
- When a link cannot be downloaded (private, deleted, inaccessible, etc.), it will be stored in a `.txt` file.  
- The `.txt` file will be named after the collection, so you can easily identify which collection had missing/skipped posts.

### 2. Handle API rate limits automatically
- If the library (`yt-dlp`) triggers an API limit error (rate limiting), the script will automatically detect it.  
- In such cases, the script will attempt to change the computer’s IP by reconnecting to a VPN before retrying.

### 3. Improved error handling and reporting
- Instead of just showing errors in the terminal, a structured log file will be created.  
- This log will include details of:
  - Which downloads failed  
  - Why they failed  
  - Whether they were retried  

### 4. Optional retry mechanism
- Links that failed due to temporary errors (e.g., connection drops) will be retried automatically.  
- Retries will be configurable (number of attempts) before writing to the skipped links file.

### 5. Configuration file support
A `config.json` or `.ini` file will be added so users can set preferences such as:
- Download path  
- VPN auto-reconnect settings  
- Retry limits  
- Whether to use cookies by default  



## ⚙️ Installation

Clone or download this repository:

```bash
git clone https://github.com/yourusername/instagram-collections-downloader.git
cd instagram-collections-downloader


