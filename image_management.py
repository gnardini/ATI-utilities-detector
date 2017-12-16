import numpy as np
from PIL import Image
from PIL import ImageTk
import cv2

class ImageManagement:

    def __init__(self, scale):
        self.panels = {
            'image': None
        }
        self.images = {
            'image': None
        }
        self.saved_original = None
        self.scale = scale

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
        max_width = self.scale

        height, width = img.shape[:2]
        img = cv2.resize(img, (max_width, int(max_width * (height / width))))

        img = self.to_tk_image(img)
        panel = self.get_panel(key)
        panel.configure(image=img)
        panel.image = img


    def save_original(self):
        self.saved_original = np.copy(self.get_image('image'))

    def restore_original(self):
        if self.saved_original is not None:
            self.put_into('image', np.copy(self.saved_original))

    def clear_cache(self):
        self.saved_original = None