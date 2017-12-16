import cv2
import numpy as np

WINDOW_NAME = 'logos'
LOGO_NAME = 'logo'

path = './images/movistar-1.png'
company = 'movistar'

first_x = -1
first_y = -1

def click(event, x, y, flags, param):
    global first_x, first_y
    if event != cv2.EVENT_LBUTTONDOWN:
        return
    if first_x == -1:
        first_x = x
        first_y = y
        return
    x_start, x_end = min(x, first_x), max(x, first_x)
    y_start, y_end = min(y, first_y), max(y, first_y)
    copy = img[y_start:y_end, x_start:x_end]
    cv2.imshow(LOGO_NAME, copy)
    first_x = -1
    first_y = -1
    cv2.imwrite('./images/logos/%s.jpg' % company, copy)

cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, click)

img = cv2.imread(path)
cv2.imshow(WINDOW_NAME, img)
cv2.imshow(LOGO_NAME, np.zeros((100, 100, 3), np.uint8))
cv2.waitKey(0)

