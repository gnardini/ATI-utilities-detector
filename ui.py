from tkinter import *
from tkinter import filedialog
import numpy as np

import image_io
import image_management as im
import characteristics_points as cp

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

def apply_sift():
    logo, img = cp.sift_matcher(manager.get_image('image'))
    resultVar.set('Resultado: %s' % logo)
    manager.put_into('image', img)


root = Tk()

manager = im.ImageManagement()

btn = Button(root, text='SIFT', command=apply_sift)
btn.grid(row=0, column=0)

resultVar = StringVar()
result = Label(root, textvariable=resultVar)
result.grid(row=0, column=1)

chooseImgButton = Button(root, text="Elegir imagen", command=lambda: assign_image('image'))
chooseImgButton.grid(row=1, column=0)

manager.set_panel('image', Label(root))
manager.get_panel('image').grid(row=2, column=0, columnspan=3)
manager.put_into('image', image_io.read('./images/cable-1.png'))

root.mainloop()
