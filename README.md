Markdown
# 🎬 YTDL-Pro Studio & Player

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-orange.svg)
![VLC](https://img.shields.io/badge/Player-VLC-red.svg)

A modern, user-friendly **YouTube Downloader & Streaming Player** featuring a sleek dark-mode user interface. Powered by `yt-dlp`, `python-vlc`, and `customtkinter`.

---

## ✨ Features & Highlights

### 📥 Downloader Features
* **Video & Audio Downloads:** Support for MP4 (HD) and high-quality MP3 audio conversions.
* **Smart Clipboard (Auto-Paste):** Automatically detects copied YouTube links and pastes them when focusing the application window.
* **Playlist Mirroring & Filtering:** Load playlists with video thumbnails, select/deselect specific tracks, or filter long lists in real time by title or artist.
* **Quick Folder Access:** Open your designated target folders (Music / Videos) with a single click directly in your file explorer.

### 🎧 Media Player Features (QoL)
* **In-App Streaming:** Stream and watch YouTube videos directly inside the application without downloading them first.
* **Interactive Seek Bar:** Smoothly scrub through video timelines with live timestamp displays (`00:00 / 00:00`).
* **Fullscreen & Quick Controls:** 
  * Double-click the video screen or use the `⛶ Fullscreen` button (press `Esc` to exit).
  * Single-click video playback to toggle Play/Pause.
  * Fast-forward and rewind buttons (`« 10s` / `10s »`).
* **Volume Controls:** Quick-mute button (`🔊` / `🔇`) with volume memory.

---

## 🖥️ Preview

> *Add application screenshots here!*
> 
> `![Screenshot](https://via.placeholder.com/800x450?text=YTDL-Pro+Preview)`

---

## 🛠️ Requirements

To ensure everything runs smoothly, make sure you have the following prerequisites installed:

1. **Python 3.8+**
2. **VLC Media Player:**
   * Required for video/audio streaming. Install it via [VideoLAN Official Site](https://www.videolan.org/vlc/).
3. **FFmpeg (Optional, but recommended):**
   * Needed for MP3 conversion and optimal HD video downloading. Can be installed automatically using the built-in fix button.

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/ytdl-pro.git](https://github.com/YOUR-USERNAME/ytdl-pro.git)
   cd ytdl-pro
Install dependencies:
The script features an automatic bootstrapper that checks and installs missing Python libraries upon launch. If you prefer to install them manually:

Bash
pip install yt-dlp customtkinter python-vlc pillow
Run the application:

Bash
python main.py
🎮 How to Use
Paste Link: Copy a YouTube video or playlist URL. The app will auto-paste it when focused.

Load Playlist (Optional): Click Load Playlist to pick specific songs to download or stream.

Stream Video: Click ► PLAY (or the green play button next to any playlist track) to start playback immediately.

Download: Select your preferred format (MP4 (Video) or MP3 (Audio)) and click START DOWNLOAD.

📜 License
This project is licensed under the MIT License – see the LICENSE file for details.

🙏 Acknowledgments & Credits
yt-dlp – Powerful YouTube downloading engine

CustomTkinter – Modern GUI framework for Python

python-vlc – Python bindings for LibVLC

Pillow – Image processing for thumbnails
