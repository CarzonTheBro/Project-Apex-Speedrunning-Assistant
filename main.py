import json
import time
import threading

from ui import PASAWindow
from capture import ScreenCapture
from OCR import OCR
import outroAudioInterpreter as OpenAI
import livesplitInterface as LSI

class MonitorController:
    def __init__(self, config):
        self.config = config
        self.capture = ScreenCapture()
        self.ocr = None
        self.lsi = LSI.LiveSplitInterface()
        self.lsi.connect()

        self.fps = config["ocr"]["capture_fps"]
        self.targets = [
            ("START", config["start"]),
            ("DEATH", config["death"]),
        ]

        self._stop_signal = None
        self._audio_ending = None
        self._audio_thread = None
        self._video_thread = None

    def is_running(self):
        return self._video_thread is not None and self._video_thread.is_alive()

    def start(self):
        if self.is_running():
            return
        if self.ocr is None:
            self.ocr = OCR()

        self._stop_signal = threading.Event()
        self._audio_ending = threading.Event()

        self._audio_thread = threading.Thread(
            target=OpenAI.monitor_roblox_audio,
            kwargs={"on_ending": self._audio_ending.set},
            args=[self._stop_signal],
            daemon=True,
        )
        self._video_thread = threading.Thread(target=self._video_loop, daemon=True)

        self._audio_thread.start()
        self._video_thread.start()

    def stop(self):
        if self._stop_signal:
            self._stop_signal.set()
        if self._audio_thread:
            self._audio_thread.join(timeout=2)
        if self._video_thread:
            self._video_thread.join(timeout=2)
        self._audio_thread = None
        self._video_thread = None

    def _video_loop(self):
        while not self._stop_signal.is_set():
            camOn = False
            for name, target in self.targets:
                image = self.capture.grab(target["region"])
                text = self.ocr.read(image)

                print(f"{name}: {text}")

                if target["text"].lower() in text.lower():
                    if name == "START":
                        camOn = True
                        print("Starting!")
                        self.lsi.start()
                    elif name == "DEATH":
                        print("Died lol")
                        self.lsi.reset()
                    print(f">>> {name} DETECTED")

            if self._audio_ending.is_set():
                self.lsi.finish()
                break

            time.sleep(1 / self.fps)

def main():
    with open("config.json") as f:
        config = json.load(f)

    controller = MonitorController(config)
    app = PASAWindow(
        on_start_monitoring=controller.start,
        on_stop_monitoring=controller.stop,
    )
    app.run()
    

if __name__ == "__main__":
    main()