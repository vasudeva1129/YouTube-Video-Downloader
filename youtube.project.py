import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp
import os


def download():
    url = url_entry.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    folder = filedialog.askdirectory(title="Select Download Folder")

    if not folder:
        return

    try:

        status_label.config(text="Fetching video information...")

        if download_type.get() == "Video":

            ydl_opts = {
                "format": "best[ext=mp4]",
                "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
            }

        else:

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)

            title_label.config(text="Title: " + info["title"])

            status_label.config(text="Downloading...")

            ydl.download([url])

        status_label.config(text="Download Completed!")

        messagebox.showinfo("Success", "Download Completed Successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("500x350")

tk.Label(root, text="YouTube Video Downloader",
         font=("Arial", 18, "bold")).pack(pady=15)

tk.Label(root, text="Enter Video URL").pack()

url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=10)

download_type = tk.StringVar(value="Video")

frame = tk.Frame(root)
frame.pack(pady=10)

video_radio = tk.Radiobutton(
    frame,
    text="Video (MP4)",
    variable=download_type,
    value="Video"
)
video_radio.pack(side="left", padx=20)

audio_radio = tk.Radiobutton(
    frame,
    text="Audio (MP3)",
    variable=download_type,
    value="Audio"
)
audio_radio.pack(side="left", padx=20)

tk.Button(root,
          text="Select Folder & Download",
          command=download,
          bg="green",
          fg="white",
           font=("Arial", 12)
).pack(pady=15)

title_label = tk.Label(root, text="")
title_label.pack()

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()
