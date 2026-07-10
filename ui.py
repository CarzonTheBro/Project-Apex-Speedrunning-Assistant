import json
import threading
import time
import tkinter as tk
from tkinter import ttk
from capture import ScreenCapture
from overlay import CaptureRegionEditor
from livesplitInterface import LiveSplitInterface
from OCR import OCR
import outroAudioInterpreter as OpenAI

CONFIG_PATH = "config.json"

DEFAULT_REGIONS = {
    "START": {"left": 0.30, "top": 0.52, "width": 0.40, "height": 0.06},
    "DEATH": {"left": 0.30, "top": 0.45, "width": 0.40, "height": 0.06},
}

REGION_COLORS = {"START": "#00ff00", "DEATH": "#ff0000"}

class PASAWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Apex Speedrunning Assistant")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        self.monitoring = False
        self.livesplit = LiveSplitInterface()
        self.config = self._load_config()

        self.ocr_testing = False
        self._ocr_stop_event = None
        self.debug_ocr_button = None

        self._active_region_editor = None
        self.edit_start_button = None
        self.edit_death_button = None

        self.main_frame = ttk.Frame(self.root)
        self.debug_frame = ttk.Frame(self.root)
        self.debug_status_text = tk.StringVar(value="Debug: Ready.")
        self.settings_frame = ttk.Frame(self.root)

        self.build_main_menu()
        self.build_debug_menu()
        self.build_settings_menu()
        self.show_main_menu()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_config(self):
        with open(CONFIG_PATH) as f:
            return json.load(f)

    def _save_config(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=4)

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
            text="Debug",
            command=self.show_debug_menu,
            width=30,
        ).pack(pady=5)

        ttk.Button(
            self.main_frame,
            text="Settings",
            command=self.show_settings_menu,
            width=30,
        ).pack()

        ttk.Separator(self.main_frame).pack(fill="x", padx=25, pady=20)

        ttk.Label(
            self.main_frame,
            text="Credits",
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(5, 2))

        ttk.Label(
            self.main_frame,
            text="CarzonTheBro   •   Mintysharky",
            font=("Segoe UI", 9),
        ).pack(pady=(0, 10))

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
 
        self.edit_start_button = ttk.Button(
            self.settings_frame,
            text="Edit Start Capture Area",
            command=self.edit_start_capture_area,
            width=30,
        )
        self.edit_start_button.pack(pady=5)
 
        self.edit_death_button = ttk.Button(
            self.settings_frame,
            text="Edit Death Capture Area",
            command=self.edit_death_capture_area,
            width=30,
        )
        self.edit_death_button.pack(pady=5)

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

            btn = ttk.Button(
                self.debug_frame,
                text=text,
                command=command,
                width=30,
            )
            btn.pack(pady=5)

            if title == "OCR" and text == "Test OCR":
                self.debug_ocr_button = btn

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
        #fix pls, start thread vs stop thread
        if(self.monitoring):
            pass
            # main.startThreads(main.audioMonitorThread,main.videoMonitorThread)
        else:
            pass
            # main.stopThreads(main.audioMonitorThread,main.videoMonitorThread)
        self.monitoring = not self.monitoring
        self.monitor_button.config(
            text="Stop Monitoring" if self.monitoring else "Start Monitoring"
        )
        self.set_debug_status(
            f"Monitoring {'started' if self.monitoring else 'stopped'}."
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
        if self.ocr_testing:
            self._stop_ocr_test()
        else:
            self._start_ocr_test()

    def _start_ocr_test(self):
        self.ocr_testing = True
        self._ocr_stop_event = threading.Event()
        if self.debug_ocr_button:
            self.debug_ocr_button.config(text="Stop OCR Test")
        self.set_debug_status("Starting OCR test...")
        threading.Thread(target=self._ocr_test_loop, daemon=True).start()

    def _stop_ocr_test(self):
        self.ocr_testing = False
        if self._ocr_stop_event:
            self._ocr_stop_event.set()
        if self.debug_ocr_button:
            self.debug_ocr_button.config(text="Test OCR")
        self.set_debug_status("OCR test stopped.")

    def _ocr_test_loop(self):
        stop_event = self._ocr_stop_event

        try:
            capture = ScreenCapture()
        except Exception as err:
            self._safe_status(f"Could not start capture: {err}")
            self._force_ocr_stopped()
            return

        try:
            ocr = OCR()
        except Exception as err:
            self._safe_status(f"Could not load OCR engine: {err}")
            self._force_ocr_stopped()
            return

        targets = [("START", self.config["start"]), ("DEATH", self.config["death"])]
        fps = self.config.get("ocr", {}).get("capture_fps", 15)

        last_message = None
        self._safe_status("Watching for START / DEATH text...")

        while not stop_event.is_set():
            found = None
            for name, target in targets:
                image = capture.grab(target["region"])
                text = ocr.read(image)
                if target["text"].lower() in text.lower():
                    found = name
                    break

            message = f"Detected {found}!" if found else "Watching for START / DEATH text..."
            if message != last_message:
                self._safe_status(message)
                last_message = message

            time.sleep(1 / fps)

    def _safe_status(self, message):
        self.root.after(0, lambda: self.set_debug_status(message))

    def _force_ocr_stopped(self):
        self.ocr_testing = False
        if self.debug_ocr_button:
            self.root.after(0, lambda: self.debug_ocr_button.config(text="Test OCR"))

    def _on_close(self):
        if self.ocr_testing:
            self._stop_ocr_test()
        if self._active_region_editor is not None:
            self._active_region_editor.destroy()
        self.root.destroy()

    def test_audio(self):
        
        if(OpenAI.crossTest()): self.set_debug_status("Cross Audio File Test Success")
        else: self.set_debug_status("Audio Failure")
        time.sleep(2)
        self.set_debug_status("Audio test not implemented yet.")

    def edit_start_capture_area(self):
        self._open_region_editor("START")

    def edit_death_capture_area(self):
        self._open_region_editor("DEATH")

    def _open_region_editor(self, name):
        if self._active_region_editor is not None:
            self.set_debug_status("Finish or cancel the current capture area edit first.")
            return
 
        key = "start" if name == "START" else "death"
 
        try:
            capture = ScreenCapture()
        except Exception as err:
            self.set_debug_status(f"Could not read monitor info: {err}")
            return
        monitor = capture.monitor
 
        def on_save(new_region):
            self.config[key]["region"] = new_region
            self._save_config()
            self.set_debug_status(f"{name} capture area saved.")
            self._active_region_editor = None
            self._set_edit_buttons_enabled(True)
 
        def on_cancel():
            self.set_debug_status(f"{name} capture area edit cancelled.")
            self._active_region_editor = None
            self._set_edit_buttons_enabled(True)
 
        self.set_debug_status(f"Editing {name.lower()} capture area...")
        self._set_edit_buttons_enabled(False)
        self._active_region_editor = CaptureRegionEditor(
            self.root,
            monitor["width"], monitor["height"],
            name=name,
            region=self.config[key]["region"],
            default_region=DEFAULT_REGIONS[name],
            color=REGION_COLORS[name],
            on_save=on_save,
            on_cancel=on_cancel,
        )
 
    def _set_edit_buttons_enabled(self, enabled: bool):
        state = ["!disabled"] if enabled else ["disabled"]
        if self.edit_start_button:
            self.edit_start_button.state(state)
        if self.edit_death_button:
            self.edit_death_button.state(state)
 
    def run(self):
        self.root.mainloop()