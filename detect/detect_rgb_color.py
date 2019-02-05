import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2


def detect(img):
    img = img[int(img.shape[0]/2):int(img.shape[0]), :, :]
    h, w, _ = img.shape
    img = cv2.GaussianBlur(img, (5, 5), 0)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # yellow_low = np.array([26, 57, 46])
    # yellow_high = np.array([34, 255, 255])

    # latest
    yellow_low = np.array([26, 30, 46])
    yellow_high = np.array([34, 255, 255])

    # latest
    white_low = np.array([0, 0, 200])
    white_high = np.array([180, 30, 255])

    # latest
    red_low = np.array([0, 90, 0])
    red_high = np.array([10, 255, 255])

    mask_white = cv2.inRange(hsv_img, white_low, white_high)
    mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
    mask_red = cv2.inRange(hsv_img, red_low, red_high)
    mask = mask_yellow + mask_white + mask_red

    y_ratio = float(format((mask_yellow > 0).sum() / float(w*h), '.4f'))
    w_ratio = float(format((mask_white > 0).sum() / float(w*h), '.4f'))
    r_ratio = float(format((mask_red > 0).sum() / float(w*h), '.4f'))

    y_thresh = float(0.01)
    w_thresh = float(0.02)
    r_thresh = float(0.25)

    result = cv2.bitwise_and(img, img, mask=mask_red)
    # command += ' ' + str([y_ratio, w_ratio, r_ratio])
    # print([y_ratio, w_ratio, r_ratio])
    return result, r_ratio

fname = 'polar_img'

# for i in range(9):
#     img = np.array(Image.open(fname+'/0/path_' + str(i) + '.png'))
#     img, ratios = detect(img)
#
#     plt.subplot(3, 3, i+1)
#     plt.imshow(img)
#     plt.title(ratios)
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()
#
# for i in range(9):
#     img = np.array(Image.open(fname+'/1/path_' + str(i) + '.png'))
#     img, ratios = detect(img)
#
#     plt.subplot(3, 3, i+1)
#     plt.imshow(img)
#     plt.title(ratios)
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()

for i in range(9):
    img = np.array(Image.open(fname+'/2/path_' + str(i) + '.png'))
    img, ratios = detect(img)

    plt.subplot(3, 3, i+1)
    plt.imshow(img)
    plt.title(ratios)

plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()