import subprocess
import sys
import os
import threading
import time
import locale
from pathlib import Path

def get_strings():
    lang = locale.getdefaultlocale()[0]
    
    # Standard: Englisch
    texts = {
        "title": "YouTube Downloader",
        "placeholder": "Paste link here...",
        "btn_path": "Select Path",
        "btn_dl": "START DOWNLOAD",
        "status_ready": "Ready",
        "status_check": "Checking",
        "status_install": "Installing",
        "status_init": "Initializing UI...",
        "status_ffmpeg_info": "FFmpeg is needed for HD & MP3...",
        "status_ffmpeg_missing": "FFmpeg NOT FOUND! Use the Fix-Button later.",
        "status_loading": "Downloading",
        "status_finish": "Success!",
        "status_error": "Error!",
        "msg_error": "Download failed:"
    }
    
    if lang and lang.startswith("de"):
        texts.update({
            "placeholder": "Link hier einfügen...",
            "btn_path": "Pfad wählen",
            "btn_dl": "DOWNLOAD STARTEN",
            "status_ready": "Bereit",
            "status_check": "Prüfe",
            "status_install": "Installiere",
            "status_init": "Initialisiere UI...",
            "status_ffmpeg_info": "FFmpeg wird für HD & MP3 benötigt...",
            "status_ffmpeg_missing": "FFmpeg FEHLT! Nutze später den Fix-Button.",
            "status_loading": "Lädt",
            "status_finish": "Erfolg!",
            "status_error": "Fehler!",
            "msg_error": "Download fehlgeschlagen:"
        })
    return texts

T = get_strings()

# --- 2. BOOT LOGIK FFmpeg CHECK ---
def check_all_dependencies(splash_callback):
    # 1. Python Module
    dependencies = ["yt-dlp", "customtkinter"]
    for package in dependencies:
        splash_callback(f"{T['status_check']} {package}...")
        try:
            if package == "yt-dlp": import yt_dlp
            else: import customtkinter
        except ImportError:
            splash_callback(f"{T['status_install']} {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    # 2. FFmpeg Check & Info
    splash_callback(T["status_ffmpeg_info"])
    time.sleep(1.5) # Zeit zum Lesen der Info
    
    ffmpeg_found = False
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        ffmpeg_found = True
        splash_callback("FFmpeg OK!")
    except:
        splash_callback(T["status_ffmpeg_missing"])
        time.sleep(2)

    splash_callback(T["status_init"])
    time.sleep(0.5)

# --- 3. SPLASH SCREEN ---
class SplashScreen:
    def __init__(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        width, height = 450, 250
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg="#1a1a1a")
        
        tk.Label(self.root, text="YTDL-PRO", fg="#1f538d", bg="#1a1a1a", font=("Arial", 28, "bold")).pack(pady=(40, 5))
        tk.Label(self.root, text="v2.0 Professional Edition", fg="gray", bg="#1a1a1a", font=("Arial", 9)).pack()
        
        self.status_label = tk.Label(self.root, text="...", fg="white", bg="#1a1a1a", font=("Arial", 10))
        self.status_label.pack(pady=30)
        
        threading.Thread(target=self.run_check, daemon=True).start()
        self.root.mainloop()

    def safe_destroy(self):
        self.root.quit()
        self.root.destroy()

    def run_check(self):
        check_all_dependencies(lambda t: self.root.after(0, self.status_label.config, {"text": t}))
        self.root.after(0, self.safe_destroy)

if __name__ == "__main__":
    SplashScreen()

    # MAIN PROGRAM
    import customtkinter as ctk
    from tkinter import filedialog, messagebox
    import yt_dlp

    class YTDLPro(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("YTDL-Pro")
            self.geometry("600x580")
            self.grid_columnconfigure(0, weight=1)
            
            self.music_path = str(Path.home() / "Music")
            self.video_path = str(Path.home() / "Videos")
            self.download_path = self.video_path
            self.is_downloading = False
            self.setup_ui()

        def setup_ui(self):
            ctk.CTkLabel(self, text=T["title"], font=("Arial", 22, "bold")).grid(row=0, column=0, pady=20)
            
            self.url_entry = ctk.CTkEntry(self, placeholder_text=T["placeholder"], width=500, height=35)
            self.url_entry.grid(row=1, column=0, padx=20, pady=10)

            self.opt_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.opt_frame.grid(row=2, column=0, pady=5)
            self.format_menu = ctk.CTkOptionMenu(self.opt_frame, values=["MP4 (Video)", "MP3 (Audio)"], command=self.update_path)
            self.format_menu.pack(side="left", padx=5)
            ctk.CTkButton(self.opt_frame, text=T["btn_path"], command=self.browse_path, fg_color="gray").pack(side="left", padx=5)

            self.status_box = ctk.CTkFrame(self, fg_color="#121212", corner_radius=8)
            self.status_box.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
            self.term_info = ctk.CTkLabel(self.status_box, text=T["status_ready"], font=("Consolas", 12), text_color="#00FF00")
            self.term_info.pack(pady=15)

            self.p_bar = ctk.CTkProgressBar(self, width=450)
            self.p_bar.set(0)
            self.p_bar.grid(row=4, column=0, pady=10)

            self.dl_btn = ctk.CTkButton(self, text=T["btn_dl"], command=self.start_download, height=45, font=("Arial", 12, "bold"))
            self.dl_btn.grid(row=5, column=0, pady=10)

            # FFmpeg Fix Button (only Windows)
            self.ffmpeg_fix = ctk.CTkButton(self, text="Install FFmpeg (Fix)", command=self.install_ffmpeg_logic, fg_color="#cc7a00", height=25)
            self.ffmpeg_fix.grid(row=6, column=0, pady=5)

        def update_path(self, choice):
            self.download_path = self.music_path if "MP3" in choice else self.video_path

        def browse_path(self):
            p = filedialog.askdirectory()
            if p: self.download_path = p

        def progress_hook(self, d):
            if d['status'] == 'downloading':
                p = d.get('_percent_str', '0%').strip()
                self.term_info.configure(text=f"{T['status_loading']}: {p} | {d.get('_speed_str', 'N/A')}")
                try: self.p_bar.set(float(p.replace('%','')) / 100)
                except: pass

        def download(self):
            url = self.url_entry.get().strip()
            if not url: return
            self.is_downloading = True
            self.dl_btn.configure(state="disabled", text="...")
            
            opts = {'outtmpl': f'{self.download_path}/%(title)s.%(ext)s', 'progress_hooks': [self.progress_hook]}
            if "MP3" in self.format_menu.get():
                opts.update({'format': 'bestaudio', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]})
            else:
                opts.update({'format': 'bestvideo+bestaudio/best'})

            try:
                with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([url])
                self.term_info.configure(text=T["status_finish"], text_color="#00FF00")
                self.url_entry.delete(0, 'end')
            except Exception as e:
                self.term_info.configure(text=T["status_error"], text_color="red")
                messagebox.showerror(T["status_error"], f"{T['msg_error']} {e}")
            finally:
                self.is_downloading = False
                self.dl_btn.configure(state="normal", text=T["btn_dl"])
                self.p_bar.set(0)

        def start_download(self):
            if not self.is_downloading:
                threading.Thread(target=self.download, daemon=True).start()

        def install_ffmpeg_logic(self):
            def run():
                try:
                    subprocess.run(["powershell", "winget install ffmpeg --source winget"], check=True)
                    messagebox.showinfo("Success", "FFmpeg installed! Please restart the app.")
                except:
                    messagebox.showerror("Error", "Winget failed. Please install FFmpeg manually.")
            threading.Thread(target=run, daemon=True).start()

    app = YTDLPro()
    app.mainloop()
