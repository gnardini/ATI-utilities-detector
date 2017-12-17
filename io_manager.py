from tkinter import filedialog
import image_io
import os
import cv2

class IOManager:

    def select_image(self):
        path = filedialog.askopenfilename()
        self.last_path = path
        if len(path) > 0:
            return image_io.read(path)
        else:
            print('Invalid image')
            return None

    def save_image(self, img, company, price):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.create_dir(company)
        filename = self.last_path.split('/')[-1]
        cv2.imwrite('./results/%s/%s' % (company, filename), img)
        with open('./results/%s/stats.dat' % company, 'a+') as f:
            f.write('%s\t%s\n' % (filename, price))

    def create_dir(self, company):
        directory = "./results/%s" % company
        if not os.path.exists(directory):
            os.makedirs(directory)
