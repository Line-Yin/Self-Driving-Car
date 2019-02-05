import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import time


def detect_mid(img):

    s = time.time()

    img = img[int(img.shape[0]/2):img.shape[0], :]

    h, w = img.shape

    img = gaussian_filter(img, sigma=0.5)

    R, C = np.where(img >= 180)

    # filtered_R = []
    # filtered_C = []
    #
    # for i in range(len(R)):
    #     f_r, f_c = np.where(img[R[i]-50:R[i]+50, C[i]-50:C[i]+50] >= 180)
    #     if len(f_r) >= 100:
    #         filtered_R.append(R[i])
    #         filtered_C.append(C[i])
    #
    # for i in range(len(filtered_R)):
    #     img[filtered_R[i]][filtered_C[i]] = 0

    # bottom = max(filtered_R)
    # left = min(filtered_C)
    # right = max(filtered_C)

    bottom = max(R)
    left = min(C)
    right = max(C)



    max_rb_idx = np.where(np.array(C) == right)

    max_rb = max(np.array(R)[max_rb_idx])

    if max_rb <= (h * 2/3):
        print('One Side Detected')
        right = w
        mid = int(left + ((right - left) / 2))
    else:
        print('Two Sides Detected')
        mid = int(left + ((right - left) / 2))

    print(time.time() - s)

    img[bottom-30:bottom-20, left:right] = 0
    img[bottom-30:bottom-20, mid-10:mid+10] = 255

    return [mid, img]


def main():

    detected_imgs = []

    for i in range(8, 16):

    # for i in range(0, 8):

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
