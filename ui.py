from tkinter import *
from tkinter import filedialog
import numpy as np

import image_io
import image_management as im
import motion_handler as mh
import sift

def select_image():
    path = filedialog.askopenfilename()
    if len(path) > 0:
        return image_io.read(path)
    else:
        print('Invalid image')
        return None

def put_into(key, img):
    manager.put_into(key, img)

def put_into_a(keys, imgs):
    manager.put_into(keys[0], imgs[0])
    manager.put_into(keys[1], imgs[1])

def assign_image(key):
    manager.put_into(key, select_image())
    motion_handler.start()

def apply_sift():
    company, price, img = sift.sift_matcher(manager.get_image('image'), motion_handler.get_rect())
    resultVar.set('Resultado: %s - %s' % (company, price))
    manager.put_into('image', img)

root = Tk()

manager = im.ImageManagement(700)
motion_handler = mh.MotionHandler(manager, 700)

btn = Button(root, text='SIFT', command=apply_sift)
btn.grid(row=0, column=0)

resultVar = StringVar()
result = Label(root, textvariable=resultVar)
result.grid(row=0, column=1)

chooseImgButton = Button(root, text="Elegir imagen", command=lambda: assign_image('image'))
chooseImgButton.grid(row=1, column=0)

manager.set_panel('image', Label(root))
manager.get_panel('image').grid(row=2, column=0, columnspan=3)
# manager.put_into('image', image_io.read('./images/cable-1.png'))

root.mainloop()
