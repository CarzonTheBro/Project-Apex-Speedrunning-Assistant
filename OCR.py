import easyocr
import cv2

class OCR:
    def __init__(self):
        self.reader = easyocr.Reader(["en"], gpu=False)

    def read(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

        results = self.reader.readtext(gray)

        return " ".join(
            text for _, text, _ in results
        ).strip()