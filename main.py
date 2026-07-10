import json
import time
import threading
from ui import PASAWindow
from capture import ScreenCapture
from OCR import OCR
import outroAudioInterpreter as OpenAI
import livesplitInterface as LSI

with open("config.json") as f:
    config = json.load(f)

stopSignal = threading.Event()
audioEndingDetected = threading.Event()
audioMonitorThread = None
videoMonitorThread = None
def on_ending():
    audioEndingDetected.set()   # or push to a queue, trigger overlay, etc.

def overlayCheckThread(capture, ocr, lsiInterface, fps, targets, exitEvent):
    while not exitEvent.is_set():
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

        if audioEndingDetected.is_set():
            lsiInterface.finish()
            break
        
        time.sleep(1 / fps)

def startThreads(thread1, thread2):
    thread1.start()
    thread2.start()
def stopThreads():
    stopSignal.set()
def main():
    app = PASAWindow()
    capture = ScreenCapture()
    ocr = OCR()
    lsiInterface = LSI.LiveSplitInterface()
    fps = config["ocr"]["capture_fps"]
    targets = [
        ("START", config["start"]),
        ("DEATH", config["death"]),
    ]
    audioMonitorThread = threading.Thread(
        target=OpenAI.monitor_roblox_audio,
        kwargs={"on_ending": on_ending},
        args = [stopSignal],
        daemon=True,
    )
    videoMonitorThread = threading.Thread(
        target=overlayCheckThread,
        args=[capture, ocr, lsiInterface, fps, targets, stopSignal],
        daemon=True,
    )

    app.run()
    

    

if __name__ == "__main__":
    main()