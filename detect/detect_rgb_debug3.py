import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2


def detect(img):
    # img = img[int(img.shape[0]/3):int(img.shape[0] * 2 / 3), :, :]
    h, w, _ = img.shape
    img = cv2.GaussianBlur(img, (5, 5), 0)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # latest
    yellow_low = np.array([26, 30, 46])
    yellow_high = np.array([34, 255, 255])

    # latest
    white_low = np.array([0, 0, 200])
    white_high = np.array([180, 30, 255])

    # latest
    red_low = np.array([0, 90, 0])
    red_high = np.array([10, 255, 255])

    # latest
    green_low = np.array([10, 50, 0])
    green_high = np.array([120, 255, 255])

    mask_white = cv2.inRange(hsv_img, white_low, white_high)
    mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
    mask_red = cv2.inRange(hsv_img, red_low, red_high)
    mask_green = cv2.inRange(hsv_img, green_low, green_high)

    mask = mask_green

    y_ratio = float(format((mask_yellow > 0).sum() / float(w*h), '.4f'))
    w_ratio = float(format((mask_white > 0).sum() / float(w*h), '.4f'))
    r_ratio = float(format((mask_red > 0).sum() / float(w*h), '.4f'))
    g_ratio = float(format((mask_green > 0).sum() / float(w * h), '.4f'))

    y_thresh = float(0.01)
    w_thresh = float(0.02)
    r_thresh = float(0.25)
    g_thresh = float(0.5)

    # if r_ratio >= r_thresh:
    #     command = 'stop'
    #     mid = [0, 0]
    #
    # elif y_ratio < y_thresh:
    #     white_pix_r, white_pix_c = np.where(mask_white > 0)
    #     mid = [int(np.median(white_pix_r)), int(np.median(white_pix_c)/2)]
    #     command = 'turn left'
    #
    # elif y_ratio >= y_thresh and w_ratio < w_thresh:
    #     yellow_pix_r, yellow_pix_c = np.where(mask_yellow > 0)
    #     myc = np.median(yellow_pix_c)
    #     mid = [int(np.median(yellow_pix_r)), int(myc+((w-myc)/2))]
    #     command = 'turn right'
    #
    # elif y_ratio >= y_thresh and y_ratio >= y_thresh:
    #     white_pix_r, white_pix_c = np.where(mask_white > 0)
    #     mwr = np.median(white_pix_r)
    #     mwc = np.median(white_pix_c)
    #     yellow_pix_r, yellow_pix_c = np.where(mask_yellow > 0)
    #     myr = np.median(yellow_pix_r)
    #     myc = np.median(yellow_pix_c)
    #     print(mwr, myr)
    #     mid = [int(max(mwr, myr)), int(myc + ((mwc - myc) / 2))]
    #     command = 'straight'
    #
    # else:
    #     mid = [-1, -1]

    result = cv2.bitwise_and(img, img, mask=mask_yellow)
    # command += ' ' + str([y_ratio, w_ratio, r_ratio])
    # print([y_ratio, w_ratio, r_ratio])
    # return result, int(w/2), mid, command, [y_ratio, w_ratio, r_ratio]
    return result, y_ratio

fname = 'debug/00/'

for i in range(9):
    img = np.array(Image.open(fname + str(i) + '.jpg'))

    # img, center, mid, command, ratios = detect(img)

    img, ratio = detect(img)

    # img[:, center-5:center+5, :] = [255, 0, 0]
    #
    # if command == 'straight':
    #     mid_r, mid_c = mid
    #     img[:, mid_c * 2, :] = [255, 255, 0]
    #     img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
    #     img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
    # elif command == 'turn left':
    #     mid_r, mid_c = mid
    #     img[:, mid_c * 2, :] = [255, 255, 0]
    #     img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
    #     img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
    # elif command == 'turn right':
    #     mid_r, mid_c = mid
    #     img[:, mid_c * 2, :] = [255, 255, 0]
    #     img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
    #     img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]

    plt.subplot(3, 3, i+1)
    plt.imshow(img)
    plt.title(ratio)

plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# for i in range(9):
#     img = np.array(Image.open(fname+'/1/path_' + str(i) + '.png'))
#     img, center, mid, command, ratios = detect(img)
#
#     img[:, center-5:center+5, :] = [255, 0, 0]
#
#     if command == 'straight':
#         mid_r, mid_c = mid
#         img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
#         img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     elif command == 'turn left':
#         mid_r, mid_c = mid
#         img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
#         img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     elif command == 'turn right':
#         mid_r, mid_c = mid
#         img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
#         img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#
#     plt.subplot(3, 3, i+1)
#     plt.imshow(img)
#     plt.title(command + ' ' + str([center, mid[1], center-mid[1]]))
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()
#
# for i in range(9):
#     img = np.array(Image.open(fname+'/2/path_' + str(i) + '.png'))
#     img, center, mid, command, ratios = detect(img)
#
#     img[:, center-5:center+5, :] = [255, 0, 0]
#
#     if command == 'straight':
#         mid_r, mid_c = mid
#         img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
#         img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     elif command == 'turn left':
#         mid_r, mid_c = mid
#         img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
#         img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     elif command == 'turn right':
#         mid_r, mid_c = mid
#         img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
#         img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#
#     plt.subplot(3, 3, i+1)
#     plt.imshow(img)
#     plt.title(command + ' ' + str([center, mid[1], center-mid[1]]))
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()