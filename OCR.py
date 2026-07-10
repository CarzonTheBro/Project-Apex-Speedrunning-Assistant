import easyocr
import cv2
import json

class OCR:
    def __init__(self):
        with open("config.json") as f:
            config = json.load(f)
            f.close()
        
        self.reader = easyocr.Reader(["en"], gpu=config["hardwareUsage"]["useGPU"])

    def read(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

        results = self.reader.readtext(gray)

        return " ".join(
            text for _, text, _ in results
        ).strip()