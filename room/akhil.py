import tkinter as tk
from tkinter import filedialog
import os
import pygame
import threading

class MusicPlayerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Player")
        self.geometry("400x300")
        self.music_file = ""
        self.playlist = []
        self.current_track = 0
        self.is_playing = False

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Music Player", font=("Helvetica", 20))
        self.label.pack(pady=10)

        self.select_button = tk.Button(self, text="Select Music", command=self.select_music)
        self.select_button.pack(pady=5)

        self.play_button = tk.Button(self, text="Play", command=self.play_music)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(self, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=5)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=5)

        self.next_button = tk.Button(self, text="Next", command=self.next_track)
        self.next_button.pack(pady=5)

        self.prev_button = tk.Button(self, text="Previous", command=self.previous_track)
        self.prev_button.pack(pady=5)

        self.playlist_label = tk.Label(self, text="Playlist")
        self.playlist_label.pack(pady=5)

        self.playlist_box = tk.Listbox(self, selectmode=tk.SINGLE)
        self.playlist_box.pack(padx=10, pady=5)

    def select_music(self):
        self.music_file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Music", filetypes=(("MP3 Files", "*.mp3"),))

        if self.music_file:
            self.playlist.append(self.music_file)
            self.playlist_box.insert(tk.END, os.path.basename(self.music_file))

    def play_music(self):
        if not self.playlist:
            return

        if self.is_playing:
            return

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
        else:
            self.is_playing = True
            self.current_track = 0
            self.play_current_track()

    def pause_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False

    def stop_music(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False

    def next_track(self):
        if self.is_playing:
            self.current_track += 1
            if self.current_track >= len(self.playlist):
                self.current_track = 0
            self.play_current_track()

    def previous_track(self):
        if self.is_playing:
            self.current_track -= 1
            if self.current_track < 0:
                self.current_track = len(self.playlist) - 1
            self.play_current_track()

    def play_current_track(self):
        if self.playlist:
            self.music_file = self.playlist[self.current_track]
            pygame.mixer.init()
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play()
            self.is_playing = True

    def on_closing(self):
        self.stop_music()
        self.destroy()

if __name__ == "__main__":
    app = MusicPlayerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
