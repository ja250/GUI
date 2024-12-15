import tkinter as tk
from tkinter import messagebox
import cv2
import threading
import os
import subprocess
import subprocess

# Function to play audio only
def play_audio(video_path):
    if not os.path.exists(video_path):
        messagebox.showerror("Error", "Video file not found!")
        return

    try:
        # Run ffplay in a subprocess to play audio
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", video_path],
            stderr=subprocess.DEVNULL,  # Suppress unnecessary output
            stdout=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        messagebox.showerror(
            "Error",
            "FFmpeg/FFplay not found. Please ensure it is installed and added to your PATH.",
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while playing audio: {e}")

# Function to download video from a URL
def download_video(url):
    output_path = "downloaded_video.mp4"
    try:
        subprocess.run(["yt-dlp", "-f", "mp4", "-o", output_path, url], check=True)
        return output_path
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")
        return None

# Function to play the video
def play_video(video_path, resolution):
    if not os.path.exists(video_path):
        messagebox.showerror("Error", "Video file not found!")
        return

    cap = cv2.VideoCapture(video_path)

    if resolution == 'low':
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    elif resolution == 'high':
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Video Player", frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to handle button click
def handle_button_click(resolution):
    video_url = entry.get()
    if not video_url:
        messagebox.showerror("Error", "Please enter a video URL.")
        return

    # Download the video
    video_path = download_video(video_url)
    if not video_path:
        return

    # Play the video/audio
    if resolution == 'audio':
        threading.Thread(target=play_audio, args=(video_path,)).start()
    else:
        threading.Thread(target=play_video, args=(video_path, resolution)).start()

# Create the GUI window
root = tk.Tk()
root.title("Video Player")

# Entry to input video link
entry_label = tk.Label(root, text="Enter Video URL:")
entry_label.pack(pady=5)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Buttons
btn_high = tk.Button(root, text="High Resolution", command=lambda: handle_button_click('high'))
btn_high.pack(pady=5)

btn_low = tk.Button(root, text="Low Resolution", command=lambda: handle_button_click('low'))
btn_low.pack(pady=5)

btn_audio = tk.Button(root, text="Audio Only", command=lambda: handle_button_click('audio'))
btn_audio.pack(pady=5)

# Run the GUI
root.mainloop()
