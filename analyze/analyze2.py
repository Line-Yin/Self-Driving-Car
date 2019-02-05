import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import time


def detect_mid(img):

    img = img[int(img.shape[0]/2):img.shape[0], :]

    # img = gaussian_filter(img, sigma=0.5)

    h, w = img.shape

    l_img = img[:, 0:int(w/2)]
    r_img = img[:, int(w/2):w]

    lr, lc = np.where(img[:, 0:int(w/2)] >= 200)
    rr, rc = np.where(img[:, int(w/2):w] >= 200)

    # for i in range(len(lr)):
    #     img[lr[i]][lc[i]] = 0

    for i in range(len(rr)):
        img[rr[i] + int(w/2)][rc[i] + int(w/2)] = 0

    # l_top = min(lr)
    # l_bottom = max(lr)
    # l_left = min(lc)
    # l_right = max(lc)



    # if right < (w * 3/4):
    #     print('One Side Detected')
    #     right = w
    #     mid = int(left + ((right - left) * (8/9)))
    # else:
    #     print('Two Sides Detected')
    #     mid = int(left + ((right - left) / 2))

    # mid = int(left + ((right - left) / 2))

    # img[l_bottom-20:l_bottom+20, l_left-20:l_left+20] = 0
    # img[l_top - 10:l_top + 10, l_right - 10:l_right + 10] = 0

    # img[bottom-30:bottom-20, left:right] = 0
    # img[bottom-30:bottom-20, mid-20:mid+20] = 255

    return [2, img]


def main():

    detected_imgs = []

    # for i in range(8, 16):

    for i in range(0, 8):

        img = np.array(Image.open('path_pi/path' + str(i) + '.jpg').convert('L'))

        detected_imgs.append(detect_mid(img))

    plt.subplot(331)
    plt.imshow(detected_imgs[0][1], cmap='gray')

    plt.subplot(332)
    plt.imshow(detected_imgs[1][1], cmap='gray')

    plt.subplot(333)
    plt.imshow(detected_imgs[2][1], cmap='gray')

    plt.subplot(334)
    plt.imshow(detected_imgs[3][1], cmap='gray')

    plt.subplot(335)
    plt.imshow(detected_imgs[4][1], cmap='gray')

    plt.subplot(336)
    plt.imshow(detected_imgs[5][1], cmap='gray')

    plt.subplot(337)
    plt.imshow(detected_imgs[6][1], cmap='gray')

    plt.subplot(338)
    plt.imshow(detected_imgs[7][1], cmap='gray')

    plt.show()


main()
