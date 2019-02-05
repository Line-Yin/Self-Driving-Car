import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time
import cv2


def detect(img, green):

    h, w, _ = img.shape
    img = cv2.GaussianBlur(img, (5, 5), 0)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # # latest
    # yellow_low = np.array([26, 57, 46])
    # yellow_high = np.array([34, 255, 255])
    #
    # # latest
    # white_low = np.array([0, 0, 200])
    # white_high = np.array([180, 60, 255])
    #
    # # latest
    # red_low = np.array([170, 90, 0])
    # red_high = np.array([180, 255, 255])

    # latest
    yellow_low = np.array([20, 43, 46])
    yellow_high = np.array([34, 255, 255])

    # latest
    white_low = np.array([0, 0, 223])
    white_high = np.array([180, 30, 255])

    # # latest
    # red_low = np.array([0, 43, 46])
    # red_high = np.array([10, 255, 255])

    if green:
        # latest
        red_low = np.array([0, 43, 46])
        red_high = np.array([15, 255, 255])
    else:
        # latest
        red_low = np.array([170, 50, 0])
        red_high = np.array([180, 255, 250])

    # latest
    green_low = np.array([20, 0, 180])
    green_high = np.array([80, 120, 254])

    mask_white = cv2.inRange(hsv_img, white_low, white_high)
    mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
    mask_red = cv2.inRange(hsv_img, red_low, red_high)
    mask_green = cv2.inRange(hsv_img, green_low, green_high)

    if green:
        mask = mask_green
    else:
        mask = mask_red + mask_yellow + mask_white

    y_ratio = float(format((mask_yellow > 0).sum() / float(w*h), '.4f'))
    w_ratio = float(format((mask_white > 0).sum() / float(w*h), '.4f'))
    r_ratio = float(format((mask_red > 0).sum() / float(w*h), '.4f'))
    g_ratio = float(format((mask_green > 0).sum() / float(w * h), '.4f'))

    print(r_ratio)

    y_thresh = float(0.005)
    w_thresh = float(0.044)
    r_thresh = float(0.18)

    if green:
        result = cv2.bitwise_and(img, img, mask=mask)
        return result, int(w / 2), [0, 0], 'green', [y_ratio, w_ratio, r_ratio]

    if r_ratio >= r_thresh:
        mid = [0, 0]
        command = 'stop'

    elif y_ratio < y_thresh:
        white_pix_r, white_pix_c = np.where(mask_white > 0)
        print(min(white_pix_c))
        print(max(white_pix_c))
        print(np.median(white_pix_c))
        mid = [int(np.median(white_pix_r)), int(np.median(white_pix_c)-900)]
        command = 'left'

    elif y_ratio >= y_thresh and w_ratio < w_thresh:
        yellow_pix_r, yellow_pix_c = np.where(mask_yellow > 0)
        myc = np.median(yellow_pix_c)
        mid = [int(np.median(yellow_pix_r)), int(myc) + 900]
        command = 'right'

    elif y_ratio >= y_thresh and w_ratio >= w_thresh:
        white_pix_r, white_pix_c = np.where(mask_white > 0)
        mwr = np.median(white_pix_r)
        mwc = np.median(white_pix_c)
        yellow_pix_r, yellow_pix_c = np.where(mask_yellow > 0)
        myr = np.median(yellow_pix_r)
        myc = np.median(yellow_pix_c)
        print(mwr, myr)
        mid = [int(max(mwr, myr)), int(myc + ((mwc - myc) / 2))]
        command = 'straight'

    else:
        mid = [-1, -1]

    result = cv2.bitwise_and(img, img, mask=mask)
    # command += ' ' + str([y_ratio, w_ratio, r_ratio])
    # print([y_ratio, w_ratio, r_ratio])
    return result, int(w/2), mid, command, [y_ratio, w_ratio, r_ratio]

fname = '1920'

# for i in range(9):
#     img = np.array(Image.open(fname+'/test_img/path_' + str(i) + '.jpg'))
#     img, center, mid, command, ratios = detect(img)
#
#     img[:, center-5:center+5, :] = [255, 0, 0]
#
#     # if command == 'straight ' + str(ratios):
#     #     mid_r, mid_c = mid
#     #     img[mid_r - 60:mid_r - 40, mid_c-150:mid_c+150, :] = [255, 255, 255]
#     #     img[mid_r - 85:mid_r - 20, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     # elif command == 'turn left ' + str(ratios):
#     #     mid_r, mid_c = mid
#     #     img[mid_r - 60:mid_r - 40, mid_c-200:mid_c+200, :] = [255, 255, 255]
#     #     img[mid_r - 80:mid_r - 20, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     # elif command == 'turn right ' + str(ratios):
#     #     mid_r, mid_c = mid
#     #     img[mid_r - 60:mid_r - 40, mid_c-200:mid_c+200, :] = [255, 255, 255]
#     #     img[mid_r - 80:mid_r - 20, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
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
#     plt.title(command + ' ' + str([center, mid[1]]))
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()


# for i in range(9, 18):
#     img = np.array(Image.open(fname+'/test_img/path_' + str(i) + '.jpg'))
#     img, center, mid, command, ratios = detect(img)
#
#     img[:, center - 5:center + 5, :] = [255, 0, 0]
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
#     plt.subplot(3, 3, i-8)
#     plt.imshow(img)
#     plt.title(command + ' ' + str([center, mid[1]]))
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()

# for i in range(9):
#     img = np.array(Image.open(fname+'/test_img2/path_' + str(i) + '.jpg'))
#     img, center, mid, command, ratios = detect(img)
#
#     img[:, center - 5:center + 5, :] = [255, 0, 0]
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
#     plt.title(command + ' ' + str([center, mid[1]]))
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()
#
# for i in range(9, 18):
#     img = np.array(Image.open(fname+'/test_img2/path_' + str(i) + '.jpg'))
#     img, center, mid, command, ratios = detect(img)
#
#     img[:, center - 5:center + 5, :] = [255, 0, 0]
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
#     plt.subplot(3, 3, i - 8)
#     plt.imshow(img)
#     plt.title(command + ' ' + str([center, mid[1]]))
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()

# fname = '1920'

# commands = ['straight', 'left', 'right', 'stop']
#
# for i in range(3):
#     img = np.array(Image.open(fname+'/demo/path_' + str(i) + '.jpg'))
#
#     plt.subplot(2, 3, i + 1)
#     plt.imshow(img)
#     plt.title(commands[i])
#
#     img, center, mid, command, ratios = detect(img)
#
#     img[:, center - 5:center + 5, :] = [255, 0, 0]
#
#     if command == 'straight':
#         mid_r, mid_c = mid
#         img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
#         img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     elif command == 'left':
#         mid_r, mid_c = mid
#         img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
#         img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#     elif command == 'right':
#         mid_r, mid_c = mid
#         img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
#         img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
#
#     plt.subplot(2, 3, i+4)
#     plt.imshow(img)
#     plt.title(command + ' ' + str([center, mid[1]]))
#
# plt.subplots_adjust(hspace=0.3, wspace=0.3)
# plt.show()


commands = ['straight', 'left', 'right']

for i in range(3):

    f_name = '1920/demo/'
    name = 'path_' + str(i) + '.jpg'
    img = np.array(Image.open(f_name + name))

    plt.subplot(2, 3, i+1)
    plt.imshow(img)
    plt.title(commands[i])

    if name == 'path_5.jpg':
        img, center, mid, command, ratios = detect(img, green=True)
    else:
        img = img[int(img.shape[0] / 2):int(img.shape[0]), :, :]
        img, center, mid, command, ratios = detect(img, green=False)

    if command == 'straight':
        print('yessssss')
        mid_r, mid_c = mid
        img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
        img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
        img[:, center - 5:center + 5, :] = [255, 0, 0]
        plt.subplot(2, 3, i + 4)
        plt.imshow(img)
        # plt.title(command + ' ' + str([center, mid[1]]))
        plt.title(command)
    elif command == 'left':
        mid_r, mid_c = mid
        img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
        img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
        img[:, center - 5:center + 5, :] = [255, 0, 0]
        plt.subplot(2, 3, i + 4)
        plt.imshow(img)
        # plt.title(command + ' ' + str([center, mid[1]]))
        plt.title(command)
    elif command == 'right':
        mid_r, mid_c = mid
        img[mid_r - 10:mid_r + 10, mid_c - 150:mid_c + 150, :] = [255, 255, 255]
        img[mid_r - 32:mid_r + 32, mid_c - 30:mid_c + 30, :] = [10, 255, 255]
        img[:, center - 5:center + 5, :] = [255, 0, 0]
        plt.subplot(2, 3, i + 4)
        plt.imshow(img)
        # plt.title(command + ' ' + str([center, mid[1]]))
        plt.title(command)
    else:
        plt.subplot(2, 3, i + 4)
        plt.imshow(img)
        plt.title(command)

plt.subplots_adjust(hspace=0.3, wspace=0.3)
plt.show()
