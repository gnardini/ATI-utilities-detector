import numpy as np
from PIL import Image
from PIL import ImageTk
import cv2

class ImageManagement:

    def __init__(self):
        self.panels = {
            'original-up': None,
            'original-down': None,
            'result-up': None,
            'result-down': None
        }
        self.images = {
            'original-up': None,
            'original-down': None,
            'result-up': None,
            'result-down': None
        }

    def get_panel(self, name):
        return self.panels[name]

    def set_panel(self, name, panel):
        self.panels[name] = panel

    def get_image(self, name):
        return self.images[name]

    def set_image(self, name, image):
        self.images[name] = image

    def to_tk_image(self, img):
        return ImageTk.PhotoImage(Image.fromarray(img))

    def put_into(self, key, img):
        self.set_image(key, img)
        max_width = 700

        height, width = img.shape[:2]
        img = cv2.resize(img, (max_width, int(max_width * (height / width))))

        img = self.to_tk_image(img)
        panel = self.get_panel(key)
        panel.configure(image=img)
        panel.image = img
