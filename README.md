import subprocess
import sys
import os
import threading
import time
import locale
import urllib.request
from io import BytesIO
from pathlib import Path

# --- VORAB-CHECK FÜR VLC DLL UNTER WINDOWS ---
if sys.platform == "win32":
    vlc_paths = [
        r"C:\Program Files\VideoLAN\VLC",
        r"C:\Program Files (x86)\VideoLAN\VLC"
    ]
    for path in vlc_paths:
        if os.path.exists(path) and hasattr(os, 'add_dll_directory'):
            try:
                os.add_dll_directory(path)
                os.environ['PATH'] = path + os.pathsep + os.environ['PATH']
                break
            except Exception:
                pass

def get_strings():
    try:
        lang = locale.getlocale()[0]
    except Exception:
        lang = None
    
    texts = {
        "title": "YouTube Downloader & Player",
        "placeholder": "Paste Link here...",
        "btn_path": "Select Path",
        "btn_open_folder": "📁 Open",
        "btn_dl": "START DOWNLOAD",
        "btn_load_pl": "Load Playlist",
        "btn_play": "►",
        "btn_pause": "❚❚",
        "btn_stop": "◼",
        "btn_fullscreen": "⛶ Fullscreen",
        "btn_select_all": "Select All",
        "btn_deselect_all": "Deselect All",
        "search_pl_placeholder": "🔍 Filter playlist...",
        "status_ready": "Ready",
        "status_check": "Checking",
        "status_install": "Installing",
        "status_init": "Initializing UI...",
        "status_ffmpeg_info": "FFmpeg is needed for HD & MP3...",
        "status_ffmpeg_missing": "FFmpeg NOT FOUND!",
        "status_vlc_missing": "VLC Player NOT FOUND!",
        "status_loading": "Downloading",
        "status_loading_pl": "Fetching Playlist...",
        "status_streaming": "Loading stream...",
        "status_finish": "Success! Files saved.",
        "status_error": "Error!",
        "msg_error": "Action failed:"
    }
    
    if lang and lang.startswith("de"):
        texts.update({
            "placeholder": "Video- oder Playlist-Link einfügen...",
            "btn_path": "Pfad wählen",
            "btn_open_folder": "📁 Ordner öffnen",
            "btn_dl": "DOWNLOAD STARTEN",
            "btn_load_pl": "Playlist Laden",
            "btn_select_all": "Alle wählen",
            "btn_deselect_all": "Keine wählen",
            "search_pl_placeholder": "🔍 Durchsuchen...",
            "status_ready": "Bereit",
            "status_check": "Prüfe",
            "status_install": "Installiere",
            "status_init": "Initialisiere UI...",
            "status_ffmpeg_info": "FFmpeg wird benötigt...",
            "status_ffmpeg_missing": "FFmpeg FEHLT!",
            "status_vlc_missing": "VLC Player FEHLT!",
            "status_loading": "Lädt",
            "status_loading_pl": "Lade Playlist...",
            "status_streaming": "Lade Stream...",
            "status_finish": "Erfolg! Speichern abgeschlossen.",
            "status_error": "Fehler!",
            "msg_error": "Aktion fehlgeschlagen:"
        })
    return texts

T = get_strings()

# --- DEPENDENCY CHECK ---
def check_all_dependencies(splash_callback):
    dependencies = ["yt-dlp", "customtkinter", "python-vlc", "Pillow"]
    
    for package in dependencies:
        splash_callback(f"{T['status_check']} {package}...")
        need_install = False
        try:
            if package == "yt-dlp": __import__("yt_dlp")
            elif package == "customtkinter": __import__("customtkinter")
            elif package == "python-vlc": import vlc; vlc.Instance()
            elif package == "Pillow": __import__("PIL")
        except (ImportError, NameError, FileNotFoundError):
            need_install = True

        if need_install:
            splash_callback(f"{T['status_install']} {package}...")
            pip_name = "python-vlc" if package == "python-vlc" else package
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", pip_name])
            except Exception: pass

            if package == "python-vlc" and sys.platform == "win32":
                splash_callback(T["status_vlc_missing"])
                try:
                    subprocess.run(["powershell", "winget install VideoLAN.VLC --source winget --accept-package-agreements --accept-source-agreements"], check=True)
                    for path in [r"C:\Program Files\VideoLAN\VLC", r"C:\Program Files (x86)\VideoLAN\VLC"]:
                        if os.path.exists(path): os.add_dll_directory(path)
                except Exception: pass

    splash_callback(T["status_init"])
    time.sleep(0.3)

# --- SPLASH SCREEN ---
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
        tk.Label(self.root, text="v4.5 Advanced Player QoL", fg="gray", bg="#1a1a1a", font=("Arial", 9)).pack()
        
        self.status_label = tk.Label(self.root, text="...", fg="white", bg="#1a1a1a", font=("Arial", 10))
        self.status_label.pack(pady=30)
        self.run_check()

    def safe_destroy(self):
        self.root.quit()
        self.root.destroy()

    def run_check(self):
        def worker():
            check_all_dependencies(lambda t: self.root.after(0, self.status_label.config, {"text": t}))
            self.root.after(0, self.safe_destroy)
        threading.Thread(target=worker, daemon=True).start()
        self.root.mainloop()

if __name__ == "__main__":
    SplashScreen()

    import customtkinter as ctk
    from tkinter import filedialog, messagebox
    from PIL import Image
    import yt_dlp
    import vlc

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    class YTDLPro(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("YTDL-Pro Studio & Player")
            self.geometry("800x980")
            self.grid_columnconfigure(0, weight=1)
            
            self.music_path = str(Path.home() / "Music")
            self.video_path = str(Path.home() / "Videos")
            self.download_path = self.video_path
            self.is_downloading = False
            self.is_seeking = False
            self.is_muted = False
            self.last_volume = 80
            
            self.playlist_items = []

            # VLC Player Setup
            try:
                self.vlc_instance = vlc.Instance()
                self.player = self.vlc_instance.media_player_new()
            except Exception:
                messagebox.showerror("VLC Fehler", "VLC konnte nicht geladen werden.")
                sys.exit()

            self.setup_ui()
            
            # Events
            self.bind("<FocusIn>", self.auto_paste_clip)
            self.bind("<Escape>", lambda e: self.toggle_fullscreen(False))
            
            # Continuous Loop für Zeitanzeige & Seekbar Update
            self.update_player_time()

        def setup_ui(self):
            # HEADER
            ctk.CTkLabel(self, text=T["title"], font=("Arial", 22, "bold")).grid(row=0, column=0, pady=(15, 5))
            
            # LINK INPUT
            self.url_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.url_frame.grid(row=1, column=0, padx=20, pady=5)
            
            self.url_entry = ctk.CTkEntry(self.url_frame, placeholder_text=T["placeholder"], width=520, height=35)
            self.url_entry.pack(side="left", padx=(0, 5))
            ctk.CTkButton(self.url_frame, text="✕", width=35, height=35, fg_color="#333333", hover_color="#555555", command=lambda: self.url_entry.delete(0, 'end')).pack(side="left")

            # CONTROLS BAR
            self.opt_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.opt_frame.grid(row=2, column=0, pady=5)
            
            self.format_menu = ctk.CTkOptionMenu(self.opt_frame, values=["MP4 (Video)", "MP3 (Audio)"], command=self.update_path)
            self.format_menu.pack(side="left", padx=4)
            
            ctk.CTkButton(self.opt_frame, text=T["btn_path"], command=self.browse_path, fg_color="#444444").pack(side="left", padx=4)
            ctk.CTkButton(self.opt_frame, text=T["btn_open_folder"], command=self.open_target_folder, fg_color="#444444", width=100).pack(side="left", padx=4)
            
            self.btn_load_pl = ctk.CTkButton(self.opt_frame, text=T["btn_load_pl"], command=self.start_fetch_playlist, fg_color="#1f538d")
            self.btn_load_pl.pack(side="left", padx=4)

            # PLAYLIST BAR
            self.pl_tools_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.pl_tools_frame.grid(row=3, column=0, pady=(5, 0))
            
            self.search_entry = ctk.CTkEntry(self.pl_tools_frame, placeholder_text=T["search_pl_placeholder"], width=240, height=28)
            self.search_entry.pack(side="left", padx=5)
            self.search_entry.bind("<KeyRelease>", self.filter_playlist)

            ctk.CTkButton(self.pl_tools_frame, text=T["btn_select_all"], width=85, height=28, command=lambda: self.toggle_all_checkboxes(True)).pack(side="left", padx=2)
            ctk.CTkButton(self.pl_tools_frame, text=T["btn_deselect_all"], width=85, height=28, command=lambda: self.toggle_all_checkboxes(False)).pack(side="left", padx=2)
            
            self.count_label = ctk.CTkLabel(self.pl_tools_frame, text="0 Tracks", font=("Arial", 11, "bold"), text_color="#3b82f6")
            self.count_label.pack(side="left", padx=8)
            self.pl_tools_frame.grid_remove()

            self.pl_frame = ctk.CTkScrollableFrame(self, width=640, height=180, label_text="Playlist Spiegelung")
            self.pl_frame.grid(row=4, column=0, pady=5)
            self.pl_frame.grid_remove()

            # --- ADVANCED MEDIA PLAYER UI ---
            self.player_container = ctk.CTkFrame(self, fg_color="#111111", corner_radius=10)
            self.player_container.grid(row=5, column=0, pady=10, padx=20)

            # Video Canvas
            self.video_frame = ctk.CTkFrame(self.player_container, width=640, height=320, fg_color="#000000", corner_radius=8)
            self.video_frame.pack(padx=8, pady=(8, 2))
            self.video_frame.grid_propagate(False)
            self.video_frame.bind("<Button-1>", lambda e: self.toggle_pause())
            self.video_frame.bind("<Double-Button-1>", lambda e: self.toggle_fullscreen())

            # Timeline / Seekbar Bar
            self.seek_frame = ctk.CTkFrame(self.player_container, fg_color="transparent")
            self.seek_frame.pack(fill="x", padx=12, pady=2)

            self.time_lbl_curr = ctk.CTkLabel(self.seek_frame, text="00:00", font=("Consolas", 11), width=45)
            self.time_lbl_curr.pack(side="left")

            self.seek_slider = ctk.CTkSlider(self.seek_frame, from_=0, to=1000, command=self.on_seek_move)
            self.seek_slider.set(0)
            self.seek_slider.pack(side="left", fill="x", expand=True, padx=8)
            self.seek_slider.bind("<ButtonRelease-1>", self.on_seek_release)
            self.seek_slider.bind("<Button-1>", self.on_seek_press)

            self.time_lbl_tot = ctk.CTkLabel(self.seek_frame, text="00:00", font=("Consolas", 11), width=45)
            self.time_lbl_tot.pack(side="right")

            # Player Controls (Buttons & Volume)
            self.player_controls = ctk.CTkFrame(self.player_container, fg_color="transparent")
            self.player_controls.pack(fill="x", padx=12, pady=(2, 8))

            ctk.CTkButton(self.player_controls, text="« 10s", width=50, height=28, fg_color="#333333", command=lambda: self.seek_relative(-10000)).pack(side="left", padx=2)
            self.btn_play = ctk.CTkButton(self.player_controls, text=T["btn_play"], width=45, height=28, fg_color="#2b8a3e", command=self.start_stream)
            self.btn_play.pack(side="left", padx=2)
            self.btn_pause = ctk.CTkButton(self.player_controls, text=T["btn_pause"], width=45, height=28, fg_color="#d97706", command=self.toggle_pause)
            self.btn_pause.pack(side="left", padx=2)
            self.btn_stop = ctk.CTkButton(self.player_controls, text=T["btn_stop"], width=45, height=28, fg_color="#c92a2a", command=self.stop_stream)
            self.btn_stop.pack(side="left", padx=2)
            ctk.CTkButton(self.player_controls, text="10s »", width=50, height=28, fg_color="#333333", command=lambda: self.seek_relative(10000)).pack(side="left", padx=2)

            # Volume & Fullscreen (Right aligned)
            ctk.CTkButton(self.player_controls, text=T["btn_fullscreen"], width=90, height=28, fg_color="#444444", command=self.toggle_fullscreen).pack(side="right", padx=(5, 0))
            
            self.vol_slider = ctk.CTkSlider(self.player_controls, from_=0, to=100, width=80, command=self.change_volume)
            self.vol_slider.set(self.last_volume)
            self.vol_slider.pack(side="right", padx=2)

            self.btn_mute = ctk.CTkButton(self.player_controls, text="🔊", width=30, height=28, fg_color="transparent", hover_color="#333333", command=self.toggle_mute)
            self.btn_mute.pack(side="right", padx=2)

            # STATUS & DOWNLOAD BAR
            self.status_box = ctk.CTkFrame(self, fg_color="#121212", corner_radius=8)
            self.status_box.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
            self.term_info = ctk.CTkLabel(self.status_box, text=T["status_ready"], font=("Consolas", 12), text_color="#00FF00")
            self.term_info.pack(pady=4)

            self.p_bar = ctk.CTkProgressBar(self, width=640)
            self.p_bar.set(0)
            self.p_bar.grid(row=7, column=0, pady=4)

            self.dl_btn = ctk.CTkButton(self, text=T["btn_dl"], command=self.start_download, height=40, font=("Arial", 13, "bold"), fg_color="#1f538d")
            self.dl_btn.grid(row=8, column=0, pady=10)

        # --- PLAYER TIME & SEEK LOGIC ---
        def update_player_time(self):
            """ Aktualisiert Seekbar und Zeitangaben jede 500ms """
            if self.player.is_playing() and not self.is_seeking:
                curr_ms = self.player.get_time()
                tot_ms = self.player.get_length()

                if tot_ms > 0:
                    val = (curr_ms / tot_ms) * 1000
                    self.seek_slider.set(val)
                    
                    self.time_lbl_curr.configure(text=self.fmt_time(curr_ms))
                    self.time_lbl_tot.configure(text=self.fmt_time(tot_ms))

            self.after(500, self.update_player_time)

        def fmt_time(self, ms):
            sec = max(0, ms // 1000)
            m, s = divmod(sec, 60)
            h, m = divmod(m, 60)
            return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"

        def on_seek_press(self, event): self.is_seeking = True
        def on_seek_move(self, val):
            if self.is_seeking and self.player.get_length() > 0:
                target_ms = int((val / 1000) * self.player.get_length())
                self.time_lbl_curr.configure(text=self.fmt_time(target_ms))

        def on_seek_release(self, event):
            if self.player.get_length() > 0:
                target_ms = int((self.seek_slider.get() / 1000) * self.player.get_length())
                self.player.set_time(target_ms)
            self.is_seeking = False

        def seek_relative(self, offset_ms):
            if self.player.get_length() > 0:
                new_time = max(0, min(self.player.get_time() + offset_ms, self.player.get_length()))
                self.player.set_time(new_time)

        def change_volume(self, val):
            self.last_volume = int(val)
            if not self.is_muted:
                self.player.audio_set_volume(self.last_volume)

        def toggle_mute(self):
            if self.is_muted:
                self.player.audio_set_volume(self.last_volume)
                self.btn_mute.configure(text="🔊")
                self.vol_slider.set(self.last_volume)
                self.is_muted = False
            else:
                self.player.audio_set_volume(0)
                self.btn_mute.configure(text="🔇")
                self.vol_slider.set(0)
                self.is_muted = True

        def toggle_fullscreen(self, mode=None):
            is_full = self.attributes("-fullscreen")
            new_state = not is_full if mode is None else mode
            self.attributes("-fullscreen", new_state)

        # --- CORE LOGIC & PLAYLIST ---
        def auto_paste_clip(self, event=None):
            if not self.url_entry.get().strip():
                try:
                    clip = self.clipboard_get().strip()
                    if "youtube.com" in clip or "youtu.be" in clip:
                        self.url_entry.insert(0, clip)
                except Exception: pass

        def open_target_folder(self):
            path = os.path.abspath(self.download_path)
            if os.path.exists(path):
                if sys.platform == "win32": os.startfile(path)
                elif sys.platform == "darwin": subprocess.run(["open", path])
                else: subprocess.run(["xdg-open", path])

        def update_path(self, choice):
            self.download_path = self.music_path if "MP3" in choice else self.video_path

        def browse_path(self):
            p = filedialog.askdirectory()
            if p: self.download_path = p

        def update_count_label(self):
            selected = sum(1 for item in self.playlist_items if item["var"].get())
            self.count_label.configure(text=f"Gewählt: {selected} / {len(self.playlist_items)}")

        def filter_playlist(self, event=None):
            q = self.search_entry.get().lower().strip()
            for item in self.playlist_items:
                if q in item["title"].lower() or q in item["uploader"].lower():
                    item["card_frame"].pack(fill="x", pady=3, padx=5)
                else: item["card_frame"].pack_forget()

        def fetch_playlist_thread(self, url):
            self.term_info.configure(text=T["status_loading_pl"], text_color="#3b82f6")
            self.btn_load_pl.configure(state="disabled")
            for w in self.pl_frame.winfo_children(): w.destroy()
            self.playlist_items.clear()

            try:
                with yt_dlp.YoutubeDL({'extract_flat': True, 'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    if 'entries' in info:
                        for idx, entry in enumerate(info['entries']):
                            title = entry.get('title', f'Track {idx+1}')
                            video_url = entry.get('url') or entry.get('webpage_url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
                            uploader = entry.get('uploader') or "Unbekannt"
                            dur = f"{int(entry.get('duration',0))//60}:{int(entry.get('duration',0))%60:02d}"

                            card = ctk.CTkFrame(self.pl_frame, fg_color="#1e1e1e", corner_radius=6)
                            card.pack(fill="x", pady=3, padx=5)

                            var = ctk.BooleanVar(value=True)
                            ctk.CTkCheckBox(card, text="", variable=var, width=20, command=self.update_count_label).pack(side="left", padx=(8, 4))

                            img_label = ctk.CTkLabel(card, text="", width=55, height=40)
                            img_label.pack(side="left", padx=4)
                            
                            thumb = entry.get('thumbnails', [{}])[-1].get('url') if entry.get('thumbnails') else None
                            if thumb: threading.Thread(target=self.load_thumbnail, args=(thumb, img_label), daemon=True).start()

                            info_f = ctk.CTkFrame(card, fg_color="transparent")
                            info_f.pack(side="left", fill="both", expand=True, padx=4)
                            ctk.CTkLabel(info_f, text=title, font=("Arial", 11, "bold"), anchor="w").pack(fill="x")
                            ctk.CTkLabel(info_f, text=f"{uploader} • {dur}", font=("Arial", 9), text_color="gray", anchor="w").pack(fill="x")

                            ctk.CTkButton(card, text="►", width=32, height=28, fg_color="#2b8a3e", command=lambda u=video_url: self.start_direct_stream(u)).pack(side="right", padx=8)

                            self.playlist_items.append({"url": video_url, "title": title, "uploader": uploader, "var": var, "card_frame": card})

                        self.pl_frame.grid()
                        self.pl_tools_frame.grid()
                        self.update_count_label()
                        self.term_info.configure(text=f"Playlist geladen ({len(self.playlist_items)} Tracks)", text_color="#00FF00")
            except Exception as e:
                self.term_info.configure(text=T["status_error"], text_color="red")
            finally:
                self.btn_load_pl.configure(state="normal")

        def load_thumbnail(self, url, label):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as resp: data = resp.read()
                img = Image.open(BytesIO(data)).resize((55, 40), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(55, 40))
                label.configure(image=ctk_img, text="")
            except Exception: pass

        def start_fetch_playlist(self):
            u = self.url_entry.get().strip()
            if u: threading.Thread(target=self.fetch_playlist_thread, args=(u,), daemon=True).start()

        def toggle_all_checkboxes(self, state: bool):
            for item in self.playlist_items: item["var"].set(state)
            self.update_count_label()

        # --- STREAMING & DOWNLOAD LOGIC ---
        def play_stream_thread(self, url):
            self.term_info.configure(text=T["status_streaming"], text_color="#3b82f6")
            try:
                with yt_dlp.YoutubeDL({'format': 'best', 'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    stream_url = info['entries'][0]['url'] if 'entries' in info else info['url']
                    title = info.get('title', 'Stream')

                media = self.vlc_instance.media_new(stream_url)
                self.player.set_media(media)

                win_id = self.video_frame.winfo_id()
                if sys.platform.startswith("linux"): self.player.set_xwindow(win_id)
                elif sys.platform == "win32": self.player.set_hwnd(win_id)
                elif sys.platform == "darwin": self.player.set_nsobject(win_id)

                self.player.play()
                self.term_info.configure(text=f"Playing: {title[:40]}...", text_color="#00FF00")
            except Exception as e:
                self.term_info.configure(text=T["status_error"], text_color="red")

        def start_stream(self):
            u = self.url_entry.get().strip()
            if u: threading.Thread(target=self.play_stream_thread, args=(u,), daemon=True).start()

        def start_direct_stream(self, video_url):
            threading.Thread(target=self.play_stream_thread, args=(video_url,), daemon=True).start()

        def toggle_pause(self):
            if self.player.is_playing(): self.player.pause()
            else: self.player.play()

        def stop_stream(self):
            self.player.stop()
            self.seek_slider.set(0)
            self.time_lbl_curr.configure(text="00:00")
            self.term_info.configure(text=T["status_ready"], text_color="#00FF00")

        def progress_hook(self, d):
            if d['status'] == 'downloading':
                p = d.get('_percent_str', '0%').strip()
                self.term_info.configure(text=f"{T['status_loading']}: {p} | {d.get('_speed_str', 'N/A')}")
                try: self.p_bar.set(float(p.replace('%','')) / 100)
                except Exception: pass

        def download(self):
            url = self.url_entry.get().strip()
            if not url and not self.playlist_items: return
            
            self.is_downloading = True
            self.dl_btn.configure(state="disabled", text="Lädt...", fg_color="gray")

            selected_urls = [item["url"] for item in self.playlist_items if item["var"].get()]
            opts = {'outtmpl': f'{self.download_path}/%(title)s.%(ext)s', 'progress_hooks': [self.progress_hook]}
            
            if "MP3" in self.format_menu.get():
                opts.update({'format': 'bestaudio', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]})
            else:
                opts.update({'format': 'bestvideo+bestaudio/best'})

            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    if selected_urls:
                        for idx, item_url in enumerate(selected_urls, start=1):
                            self.term_info.configure(text=f"Download {idx}/{len(selected_urls)}...")
                            ydl.download([item_url])
                    else:
                        ydl.download([url])
                self.term_info.configure(text=T["status_finish"], text_color="#00FF00")
            except Exception as e:
                self.term_info.configure(text=T["status_error"], text_color="red")
            finally:
                self.is_downloading = False
                self.dl_btn.configure(state="normal", text=T["btn_dl"], fg_color="#1f538d")
                self.p_bar.set(0)

        def start_download(self):
            if not self.is_downloading: threading.Thread(target=self.download, daemon=True).start()

    app = YTDLPro()
    app.mainloop()
