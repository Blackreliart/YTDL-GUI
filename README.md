# 📺 yt-dlp UI

> **A modern YouTube Downloader for Windows.**
> Designed to be simple, reliable, and easy to use.

---

## 🛠 Project Overview

YTDL-GUI is a user-friendly wrapper around yt-dlp that handles the complexities of video downloading with minimal user intervention.

| Feature               | Description                                                              |
| :-------------------- | :----------------------------------------------------------------------- |
| **Self-Healing**      | Automatically detects and installs missing Python modules on boot.       |
| **Integrated FFmpeg** | Checks for system-wide FFmpeg and provides an automated Winget fix.      |
| **Professional Boot** | A borderless splash screen with real-time initialization logs.           |
| **Multi-Language**    | Native support for English and German based on system locale.            |
| **Stealth Mode**      | Hides background terminal windows for a cleaner GUI experience.          |

---

## 🏗️ Technical Credits

This project makes use of the following excellent tools and libraries:

* **Core Engine:** [yt-dlp](https://github.com/yt-dlp/yt-dlp) – A reliable video extraction tool.
* **UI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) – Providing modern "Dark Mode" aesthetics.
* **Multimedia:** [FFmpeg](https://ffmpeg.org/) – Handling stream muxing and conversions.

---
## ▶️ Run from Source

To start the app, simply run the Python file:

```powershell
python "Yt-dl UI.py"
```

Or just double-click the .py file if Python is properly installed.

### ⚠️ Requirements
- Python 3.10+ installed
- Recommended:
  - FFmpeg (for audio/video processing)
  - Node.js (for yt-dlp compatibility)
  - EXE file in RELEASES doesn't require Python installation

### 📝 Notes
- Missing dependencies are installed automatically (self-healing).
- If something doesn't work, use the FFmpeg Fix inside the app.

## 🚀 Building the Executable

Follow these steps to compile the source code into a single, portable Windows `.exe` file.

### 1. Environment Setup

Clone the repository and ensure you have **Python 3.10+** installed:

```powershell
git clone https://github.com/YOUR_USERNAME/YTDL-GUI.git
cd YTDL-GUI
pip install pyinstaller
```

---

### 2. The Build Command

Execute this PyInstaller command to bundle the app. This configuration hides the terminal and requests UAC admin rights for the FFmpeg installer:

```powershell
python -m PyInstaller --noconsole --onefile --uac-admin --name "YTDL-GUI" ".\Yt-dl UI.py"
```

**Note:**
The finished executable will be generated in the `/dist` folder. You can safely delete the `/build` folder and the `.spec` file after the build is complete.

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

**Method:** This triggers a `winget install ffmpeg` command to set up the environment.

---

## 📜 License & Disclaimer

This project is released under the **MIT License**.

**Disclaimer:**
This software is intended for educational and private use only. Users are responsible for complying with the Terms of Service of any platform they interact with. We do not encourage the violation of copyright or terms of service.

---

Developed for the Open Source Community.
