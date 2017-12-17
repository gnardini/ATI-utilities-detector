from tkinter import *
from tkinter import filedialog
import numpy as np

import image_management as im
import motion_handler as mh
import io_manager
import sift

def assign_image(key):
    manager.put_into(key, io.select_image())
    motion_handler.start(apply_sift)

def apply_sift():
    company, price, img = sift.sift_matcher(manager.get_image('image'), motion_handler.get_rect())
    print(price)
    io.save_image(manager.get_image('image'), company, price)
    resultVar.set('Resultado: %s - %s' % (company, price))
    manager.put_into('image', img)
    manager.clear_cache()

root = Tk()

manager = im.ImageManagement(700)
motion_handler = mh.MotionHandler(manager, 700)
io = io_manager.IOManager()

resultVar = StringVar()
result = Label(root, textvariable=resultVar)
result.grid(row=0, column=1)

chooseImgButton = Button(root, text="Elegir imagen", command=lambda: assign_image('image'))
chooseImgButton.grid(row=0, column=0)

manager.set_panel('image', Label(root))
manager.get_panel('image').grid(row=1, column=0, columnspan=3)

root.mainloop()
