# 📺 YTDL-Pro UI

> **A high-performance, modern YouTube Downloader for Windows.**
> Optimized for simplicity, speed, and a seamless "native app" feel.

---

## 🛠 Project Overview

YTDL-Pro is more than just a wrapper. It is a standalone environment designed to handle all complexities of video downloading automatically.

| Feature               | Description                                                              |
| :-------------------- | :----------------------------------------------------------------------- |
| **Self-Healing**      | Automatically detects and installs missing Python modules on boot.       |
| **Integrated FFmpeg** | Checks for system-wide FFmpeg and provides an automated Winget fix.      |
| **Professional Boot** | A borderless splash screen with real-time initialization logs.           |
| **Multi-Language**    | Native support for English and German based on system locale.            |
| **Stealth Mode**      | Completely hides background terminal windows for a clean GUI experience. |

---

## 🏗️ Technical Credits

This project stands on the shoulders of giants. We gratefully acknowledge the following original works:

* **Core Engine:** [yt-dlp](https://github.com/yt-dlp/yt-dlp) – The industry standard for video extraction.
* **UI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) – Providing modern "Dark Mode" aesthetics.
* **Multimedia:** [FFmpeg](https://ffmpeg.org/) – Handling complex stream muxing and conversions.

---

## 🚀 Building the Executable

Follow these steps to compile the source code into a single, portable Windows `.exe` file.

### 1. Environment Setup

Clone the repository and ensure you have **Python 3.10+** installed:

```powershell
git clone https://github.com/YOUR_USERNAME/YTDL-Pro.git
cd YTDL-Pro
pip install pyinstaller
```

---

### 2. The Build Command

Execute this PyInstaller command to bundle the app. This configuration hides the terminal and requests UAC admin rights for the FFmpeg installer:

```powershell
python -m PyInstaller --noconsole --onefile --uac-admin --name "YTDL-Pro" ".\Yt-dl UI.py"
```

**Note:**
The finished executable will be generated in the `/dist` folder. You can safely delete the `/build` folder and the `.spec` file after the process is complete.

---

## 🔧 Troubleshooting & Requirements

### 🟢 JavaScript Runtime

If you encounter a `No JavaScript runtime found` warning:

**Solution:** Install Node.js

**Why?** yt-dlp requires a JavaScript runtime to decrypt YouTube's rolling signature algorithms.

---

### 🔴 FFmpeg Issues

If downloads fail to merge or MP3 conversion doesn't work:

**Solution:** Use the **"Install FFmpeg (Fix)"** button inside the app

**Method:** This triggers a `winget install ffmpeg` command to set up the environment automatically.

---

## 📜 License & Disclaimer

This project is released under the **MIT License**.

**Disclaimer:**
This software is intended for educational and private use only. Users are responsible for complying with the Terms of Service of any platform they interact with. We do not encourage the violation of copyrights.

---

Developed with ❤️ for the Open Source Community.
