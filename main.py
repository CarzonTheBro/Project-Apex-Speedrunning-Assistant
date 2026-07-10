import json
import time

from capture import ScreenCapture
from OCR import OCR


with open("config.json") as f:
    config = json.load(f)


capture = ScreenCapture()
ocr = OCR()

fps = config["ocr"]["capture_fps"]

targets = [
    ("START", config["start"]),
    ("DEATH", config["death"])
]


while True:
    for name, target in targets:
        image = capture.grab(target["region"])
        text = ocr.read(image)

        print(f"{name}: {text}")

        if target["text"].lower() in text.lower():
            print(f">>> {name} DETECTED")

    time.sleep(1 / fps)