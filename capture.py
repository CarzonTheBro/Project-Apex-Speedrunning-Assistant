import mss
import numpy as np

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]

    def region_to_pixels(self, region):
        return {
            "left": int(self.monitor["width"] * region["left"]),
            "top": int(self.monitor["height"] * region["top"]),
            "width": int(self.monitor["width"] * region["width"]),
            "height": int(self.monitor["height"] * region["height"])
        }

    def grab(self, region):
        pixel_region = self.region_to_pixels(region)
        img = self.sct.grab(pixel_region)
        return np.array(img)