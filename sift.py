import cv2
import image_io as io

import os
import pytesseract
from PIL import Image

from pprint import pprint

# price_Rect format: (start_x, start_y), (end_x, end_y)
def sift_matcher(img, price_rect):
    print(price_rect)
    logos = ['cablevision', 'itba', 'medicus', 'movistar']
    # logos = ['cablevision']
    matches = 0
    company = None
    result_img = None
    for logo in logos:
        logo_img = io.read('./images/logos/%s.jpg' % logo)
        res_img, score = sift_comparison(img, logo_img)
        print('%s: %d' % (logo, score))
        if score > matches:
            matches = score
            company = logo
            result_img = res_img

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    filename = "{}.png".format(os.getpid())
    start = price_rect[0]
    end = price_rect[1]
    cv2.imwrite(filename, gray[start[0]:end[0], start[1]:end[1]])

    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    print(text)

    return [company, text, result_img]

def apply_sift(img):
    # orb = cv2.ORB_create()
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # kp, des = orb.detectAndCompute(gray, None)
    # return [kp, des, img]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(gray, None)
    return [kp, des, img]

def sift_comparison(img2, img1):
    kp1, des1, _ = apply_sift(img1)
    kp2, des2, _ = apply_sift(img2)

    # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    bf = cv2.BFMatcher()
    matches = bf.match(des1, des2)

    max_near_kps = 0
    max_x_dist = img1.shape[1]
    max_y_dist = img1.shape[0]

    matches = list(filter(lambda x: x.distance < 150, matches))

    for match in matches:
        x, y = kp2[match.trainIdx].pt
        near_kps = 0
        for match2 in matches:
            x2, y2 = kp2[match2.trainIdx].pt
            if abs(x-x2) < max_x_dist and abs(y-y2) < max_y_dist:
                near_kps += 1
        if near_kps > max_near_kps:
            max_near_kps = near_kps

    img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches, flags=2, outImg=img1)
    # cv2.imshow("Matches", img3)
    # cv2.waitKey(0)
    return img3, max_near_kps