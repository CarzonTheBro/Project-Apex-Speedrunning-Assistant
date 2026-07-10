import threading
import time
import tkinter as tk
from tkinter import ttk

from livesplitInterface import LiveSplitInterface


class PASAWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Apex Speedrunning Assistant")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        self.monitoring = False
        self.livesplit = LiveSplitInterface()

        self.main_frame = ttk.Frame(self.root)
        self.debug_frame = ttk.Frame(self.root)
        self.debug_status_text = tk.StringVar(value="Debug: Ready.")
        self.settings_frame = ttk.Frame(self.root)

        self.build_main_menu()
        self.build_settings_menu()
        self.build_debug_menu()
        self.show_main_menu()

    def clear_frames(self):
        for frame in (
            self.main_frame,
            self.settings_frame,
            self.debug_frame,
        ):
            frame.pack_forget()

    def show_main_menu(self):
        self.clear_frames()
        self.main_frame.pack(fill="both", expand=True)

    def show_debug_menu(self):
        self.clear_frames()
        self.debug_frame.pack(fill="both", expand=True)

    def show_settings_menu(self):
        self.clear_frames()
        self.settings_frame.pack(fill="both", expand=True)

    def build_main_menu(self):
        ttk.Label(
            self.main_frame,
            text="Project Apex Speedrunning Assistant",
            font=("Segoe UI", 20, "bold"),
        ).pack(pady=(30, 10))

        ttk.Label(
            self.main_frame,
            text="Automatically controls LiveSplit using OCR and audio detection.",
            font=("Segoe UI", 10),
        ).pack()

        ttk.Separator(self.main_frame).pack(fill="x", padx=25, pady=20)

        self.monitor_button = ttk.Button(
            self.main_frame,
            text="Start Monitoring",
            command=self.toggle_monitoring,
            width=30,
        )
        self.monitor_button.pack(pady=10)

        ttk.Button(
            self.main_frame,
            text="Settings",
            command=self.show_settings_menu,
            width=30,
        ).pack(pady=5)

        ttk.Button(
            self.main_frame,
            text="Debug",
            command=self.show_debug_menu,
            width=30,
        ).pack()

        ttk.Separator(self.main_frame).pack(fill="x", padx=25, pady=20)

    def build_settings_menu(self):
        ttk.Label(
            self.settings_frame,
            text="Settings",
            font=("Segoe UI", 20, "bold"),
        ).pack(pady=(20, 15))

        ttk.Button(
            self.settings_frame,
            text="← Back",
            command=self.show_main_menu,
            width=20,
        ).pack(pady=5)

        ttk.Separator(self.settings_frame).pack(fill="x", padx=25, pady=15)

        ttk.Button(
            self.settings_frame,
            text="Edit Start Capture Area",
            command=self.edit_start_capture_area,
            width=30,
        ).pack(pady=5)

        ttk.Button(
            self.settings_frame,
            text="Edit Death Capture Area",
            command=self.edit_death_capture_area,
            width=30,
        ).pack(pady=5)

    def build_debug_menu(self):
        ttk.Label(
            self.debug_frame,
            text="Debug",
            font=("Segoe UI", 20, "bold"),
        ).pack(pady=(20, 15))

        ttk.Button(
            self.debug_frame,
            text="← Back",
            command=self.show_main_menu,
            width=20,
        ).pack(pady=5)

        for title, text, command in [
            ("LiveSplit", "Test Connection", self.test_connection),
            ("LiveSplit", "Test Actions", self.test_actions),
            ("OCR", "Test OCR", self.test_ocr),
            ("Audio", "Test Audio", self.test_audio),
        ]:
            if title != getattr(self, "_last_title", None):
                ttk.Separator(self.debug_frame).pack(fill="x", padx=25, pady=15)
                ttk.Label(
                    self.debug_frame,
                    text=title,
                    font=("Segoe UI", 12, "bold"),
                ).pack()
                self._last_title = title

            ttk.Button(
                self.debug_frame,
                text=text,
                command=command,
                width=30,
            ).pack(pady=5)

        ttk.Separator(self.debug_frame).pack(fill="x", padx=25, pady=20)

        self.debug_status_label = ttk.Label(
            self.debug_frame,
            textvariable=self.debug_status_text,
            font=("Segoe UI", 10),
            anchor="w",
            justify="left",
        )
        self.debug_status_label.pack(fill="x", padx=20, pady=(0, 10))

    def toggle_monitoring(self):
        self.monitoring = not self.monitoring
        self.monitor_button.config(
            text="Stop Monitoring" if self.monitoring else "Start Monitoring"
        )
        self.debug_status_text.set(
            f"Debug: Monitoring {'started' if self.monitoring else 'stopped'}."
        )

    def set_debug_status(self, message):
        self.debug_status_text.set(f"Debug: {message}")
        self.root.update_idletasks()

    def debug(self, message):
        print(f"[UI] {message}")

    def test_connection(self):
        def worker():
            self.set_debug_status("Testing LiveSplit connection...")
            if self.livesplit.connect():
                self.set_debug_status("Successfully connected and disconnected from LiveSplit.")
                self.livesplit.disconnect()
            else:
                self.set_debug_status("Failed to connect to LiveSplit.")

        threading.Thread(target=worker, daemon=True).start()

    def test_actions(self):
        def worker():
            self.set_debug_status("Running LiveSplit action test...")

            if not self.livesplit.connect():
                self.set_debug_status("Could not connect to LiveSplit.")
                return

            for message, action in [
                ("Starting timer", self.livesplit.start),
                ("Finishing timer...", self.livesplit.finish),
                ("Resetting timer...", self.livesplit.reset),
            ]:
                self.set_debug_status(message)
                action()
                time.sleep(2)

            self.livesplit.disconnect()
            self.set_debug_status("Successfully ran LiveSplit actions.")

        threading.Thread(target=worker, daemon=True).start()

    def test_ocr(self):
        self.set_debug_status("OCR test not implemented yet.")

    def test_audio(self):
        self.set_debug_status("Audio test not implemented yet.")

    def edit_start_capture_area(self):
        self.set_debug_status("Editing start capture area...")

    def edit_death_capture_area(self):
        self.set_debug_status("Editing death capture area...")

    def run(self):
        self.root.mainloop()