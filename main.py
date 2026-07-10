"""import json
import time
import threading

from capture import ScreenCapture
from OCR import OCR
from PyQt5.QtWidgets import QApplication
from overlay import Overlay
import outroAudioInterpreter as OpenAI
import livesplitInterface as LSI

with open("config.json") as f:
    config = json.load(f)

audio_ending_detected = threading.Event()


def on_ending():
    audio_ending_detected.set()   # or push to a queue, trigger overlay, etc.


def overlay_thread(capture, targets):
    app = QApplication([])
    overlay = Overlay(capture.monitor, targets)
    app.exec_()


def main():
    capture = ScreenCapture()
    ocr = OCR()
    lsiInterface = LSI.LiveSplitInterface()

    fps = config["ocr"]["capture_fps"]

    targets = [
        ("START", config["start"]),
        ("DEATH", config["death"]),
    ]

    threading.Thread(
        target=overlay_thread, args=(capture, targets), daemon=True
    ).start()

    threading.Thread(
        target=OpenAI.monitor_roblox_audio,
        kwargs={"on_ending": on_ending},
        daemon=True,
    ).start()

    while True:
        for name, target in targets:
            image = capture.grab(target["region"])
            text = ocr.read(image)

            print(f"{name}: {text}")

            if target["text"].lower() in text.lower():
                if(name == "CAM CONNECTED"):
                    lsiInterface.start()
                elif(name == "MISSION FAILED"):
                    lsiInterface.reset()
                print(f">>> {name} DETECTED")

        if audio_ending_detected.is_set():
            lsiInterface.finish()
            break
        
        time.sleep(1 / fps)"""

from ui import PASAWindow

def main():
    app = PASAWindow()
    app.run()


if __name__ == "__main__":
    main()