import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2


def detect(img):
    # img = img[int(img.shape[0] / 3):int(img.shape[0] * 2 / 3), :, :]
    # img = img[int(img.shape[0] / 2):int(img.shape[0]), :, :]
    h, w, _ = img.shape
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # latest
    yellow_low = np.array([26, 30, 46])
    yellow_high = np.array([34, 255, 255])

    # latest
    white_low = np.array([0, 0, 200])
    white_high = np.array([180, 30, 255])

    # latest
    red_low = np.array([0, 0, 0])
    red_high = np.array([10, 255, 100])

    # latest
    green_low = np.array([10, 50, 0])
    green_high = np.array([120, 255, 255])

    r_thresh = float(0.25)
    y_thresh = float(0.01)
    w_thresh = float(0.02)
    g_thresh = float(0.5)

    center = int(w / 2)

    mask_red = cv2.inRange(hsv_img, red_low, red_high)
    r_ratio = float(format((mask_red > 0).sum() / float(w * h), '.4f'))

    img = cv2.bitwise_and(img, img, mask=mask_red)

    return img, r_ratio

    # if r_ratio >= r_thresh:
    #
    #     mask_green = cv2.inRange(hsv_img, green_low, green_high)
    #     g_ratio = float(format((mask_green > 0).sum() / float(w * h), '.4f'))
    #
    #     ratio = [r_ratio, g_ratio]
    #
    #     mask = mask_red + mask_green
    #
    #     img = cv2.bitwise_and(img, img, mask=mask)
    #
    #     if g_ratio >= g_thresh:
    #         command = 'green light'
    #         return img, center, 0, command, ratio
    #     else:
    #         command = 'stop'
    #         return img, center, 0, command, ratio
    #
    # else:
    #     mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
    #     mask_white = cv2.inRange(hsv_img, white_low, white_high)
    #     y_ratio = float(format((mask_yellow > 0).sum() / float(w * h), '.4f'))
    #     w_ratio = float(format((mask_white > 0).sum() / float(w * h), '.4f'))
    #
    #     ratio = [y_ratio, w_ratio]
    #
    #     mask = mask_yellow + mask_white
    #
    #     img = cv2.bitwise_and(img, img, mask=mask)
    #
    #     if y_ratio < y_thresh:
    #
    #         _, white_pix_c = np.where(mask_white > 0)
    #
    #         if len(white_pix_c) == 0:
    #             command = 'straight'
    #             return img, center, center, command, ratio
    #         else:
    #             command = 'turn left'
    #             return img, center, int(np.median(white_pix_c) / 2), command, ratio
    #
    #     elif y_ratio >= y_thresh and w_ratio < w_thresh:
    #
    #         _, yellow_pix_c = np.where(mask_yellow > 0)
    #
    #         if len(yellow_pix_c) == 0:
    #             command = 'straight'
    #             return img, center, center, command, ratio
    #         else:
    #             command = 'turn right'
    #             myc = np.median(yellow_pix_c)
    #             return img, center, int(myc + ((w - myc) / 2)), command, ratio
    #
    #     elif y_ratio >= y_thresh and w_ratio >= w_thresh:
    #
    #         _, white_pix_c = np.where(mask_white > 0)
    #         _, yellow_pix_c = np.where(mask_yellow > 0)
    #
    #         if len(white_pix_c) == 0 or len(yellow_pix_c) == 0:
    #             command = 'straight'
    #             return img, center, center, command, ratio
    #         else:
    #             command = 'straight'
    #             mwc = np.median(white_pix_c)
    #             myc = np.median(yellow_pix_c)
    #             return img, center, int(myc + ((mwc - myc) / 2)), command, ratio
    #
    #     else:
    #         img = np.zeros((h, w))
    #         command = 'unknown state'
    #         return img, center, -1, command, []

fname = '5imgs/'

for i in range(5):
    img = np.array(Image.open(fname + str(i) + '.png'))

    # img, center, mid, command, ratio = detect(img)

    img, ratio = detect(img)

    # img[:, center-5:center+5, :] = [255, 0, 0]
    #
    # if command == 'straight':
    #     img[:, mid-5:mid+5, :] = [255, 255, 0]
    #     # img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
    # elif command == 'turn left':
    #     img[:, mid - 5:mid + 5, :] = [255, 255, 0]
    #     # img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
    # elif command == 'turn right':
    #     img[:, mid - 5:mid + 5, :] = [255, 255, 0]
    #     # img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]

    plt.subplot(3, 3, i+1)
    plt.imshow(img)
    plt.title(ratio)

plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()


# for i in range(9, 18):
#     img = np.array(Image.open(fname + str(i) + '.jpg'))
#
#     img, center, mid, command, ratio = detect(img)
#
#     img[:, center-5:center+5, :] = [255, 0, 0]
#
#     if command == 'straight':
#         img[:, mid-5:mid+5, :] = [255, 255, 0]
#         # img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     elif command == 'turn left':
#         img[:, mid - 5:mid + 5, :] = [255, 255, 0]
#         # img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     elif command == 'turn right':
#         img[:, mid - 5:mid + 5, :] = [255, 255, 0]
#         # img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#
#     plt.subplot(3, 3, i-8)
#     plt.imshow(img)
#     plt.title([command, ratio])
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()
#
#
# for i in range(18, 26):
#     img = np.array(Image.open(fname + str(i) + '.jpg'))
#
#     img, center, mid, command, ratio = detect(img)
#
#     img[:, center-5:center+5, :] = [255, 0, 0]
#
#     if command == 'straight':
#         img[:, mid-5:mid+5, :] = [255, 255, 0]
#         # img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     elif command == 'turn left':
#         img[:, mid - 5:mid + 5, :] = [255, 255, 0]
#         # img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     elif command == 'turn right':
#         img[:, mid - 5:mid + 5, :] = [255, 255, 0]
#         # img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#
#     plt.subplot(3, 3, i-17)
#     plt.imshow(img)
#     plt.title([command, ratio])
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()