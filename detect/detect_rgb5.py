import numpy as np
import cv2
# from PIL import Image
# import matplotlib.pyplot as plt


def detect(img):
    h, w, _ = img.shape
    img = cv2.GaussianBlur(img, (5, 5), 0)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # latest
    yellow_low = np.array([20, 43, 46])
    yellow_high = np.array([34, 255, 255])

    # latest
    white_low = np.array([0, 0, 221])
    white_high = np.array([180, 30, 255])

    # latest
    red_low = np.array([0, 43, 46])
    red_high = np.array([10, 255, 255])

    # latest
    green_low = np.array([10, 80, 80])
    green_high = np.array([77, 255, 255])

    r_thresh = float(0.05)
    y_thresh = float(0.015)
    w_thresh = float(0.015)
    g_thresh = float(0.02)

    center = int(w / 2)

    # detect red
    mask_red = cv2.inRange(hsv_img, red_low, red_high)

    r_ratio = float(format((mask_red > 0).sum() / float(w * h), '.4f'))

    # if red detected
    if r_ratio >= r_thresh:

        hsv_img = hsv_img[:, int(w / 4):int(w), :]

        mask_green = cv2.inRange(hsv_img, green_low, green_high)

        g_ratio = float(format((mask_green > 0).sum() / float(h * 3/4), '.4f'))

        ratio = [r_ratio, g_ratio]

        # if green detected
        if g_ratio >= g_thresh:
            command = 'green'
            return center, -1, command, ratio

        # if green not detected
        else:
            command = 'stop'
            return center, -1, command, ratio

    # if red not detected
    else:

        mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
        mask_white = cv2.inRange(hsv_img, white_low, white_high)

        y_ratio = float(format((mask_yellow > 0).sum() / float(w * h), '.4f'))
        w_ratio = float(format((mask_white > 0).sum() / float(w * h), '.4f'))

        ratio = [y_ratio, w_ratio]

        # if no yellow detected
        if y_ratio < y_thresh:

            _, white_pix_c = np.where(mask_white > 0)

            if len(white_pix_c) == 0:
                command = 'stop'
                return center, -1, command, ratio
            else:
                command = 'left'
                return center, int(np.median(white_pix_c) / 2), command, ratio

        # if no white detected, yellow detected
        elif y_ratio >= y_thresh and w_ratio < w_thresh:

            _, yellow_pix_c = np.where(mask_yellow > 0)

            if len(yellow_pix_c) == 0:
                command = 'stop'
                return center, -1, command, ratio
            else:
                command = 'right'
                myc = np.median(yellow_pix_c)
                return center, int(myc + ((w - myc) / 2)), command, ratio

        # yellow, white detected
        elif y_ratio >= y_thresh and w_ratio >= w_thresh:

            _, white_pix_c = np.where(mask_white > 0)
            _, yellow_pix_c = np.where(mask_yellow > 0)

            if len(white_pix_c) == 0 or len(yellow_pix_c) == 0:
                command = 'stop'
                return center, -1, command, ratio

            # elif int(max(white_pix_c) - min(white_pix_c)) < int(150):
            elif int(min(white_pix_c)) > int(h / 2):
                command = 'straight'
                myc = np.median(yellow_pix_c)
                return center, int(myc + ((w - myc) / 2)), command, ratio
            else:
                command = 'right'
                mwc = np.median(white_pix_c)
                myc = np.median(yellow_pix_c)
                return center, int(myc + ((mwc - myc) / 2)), command, ratio

        else:
            command = 'unknown'
            return center, -1, command, []


# fname = 'small/'
#
# for i in range(5):
#     img = np.array(Image.open(fname + str(i) + '.jpg'))
#
#     # img, center, mid, command, ratio = detect(img)
#
#     img = detect(img)
#
#     plt.subplot(3, 3, i + 1)
#     plt.imshow(img)
#     # plt.title(ratio)
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()







    # r_ratio = float(format((mask_red > 0).sum() / float(w * h), '.4f'))

    # if r_ratio >= r_thresh:
    #
    #     mask_green = cv2.inRange(hsv_img, green_low, green_high)
    #     g_ratio = float(format((mask_green > 0).sum() / float(w * h), '.4f'))
    #
    #     ratio = [r_ratio, g_ratio]
    #
    #     if g_ratio >= g_thresh:
    #         command = 'green light'
    #         return center, 0, command, ratio
    #     else:
    #         command = 'stop'
    #         return center, 0, command, ratio
    #
    # else:
    #     mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
    #     mask_white = cv2.inRange(hsv_img, white_low, white_high)
    #     y_ratio = float(format((mask_yellow > 0).sum() / float(w * h), '.4f'))
    #     w_ratio = float(format((mask_white > 0).sum() / float(w * h), '.4f'))
    #
    #     ratio = [y_ratio, w_ratio]
    #
    #     if y_ratio < y_thresh:
    #
    #         _, white_pix_c = np.where(mask_white > 0)
    #
    #         if len(white_pix_c) == 0:
    #             command = 'stop'
    #             return center, center, command, ratio
    #         else:
    #             command = 'turn left'
    #             return center, int(np.median(white_pix_c) / 2), command, ratio
    #
    #     elif y_ratio >= y_thresh and w_ratio < w_thresh:
    #
    #         _, yellow_pix_c = np.where(mask_yellow > 0)
    #
    #         if len(yellow_pix_c) == 0:
    #             command = 'stop'
    #             return center, center, command, ratio
    #         else:
    #             command = 'turn right'
    #             myc = np.median(yellow_pix_c)
    #             return center, int(myc + ((w - myc) / 2)), command, ratio
    #
    #     elif y_ratio >= y_thresh and w_ratio >= w_thresh:
    #
    #         _, white_pix_c = np.where(mask_white > 0)
    #         _, yellow_pix_c = np.where(mask_yellow > 0)
    #
    #         if len(white_pix_c) == 0 or len(yellow_pix_c) == 0:
    #             command = 'stop'
    #             return center, center, command, ratio
    #
    #         # elif int(max(white_pix_c) - min(white_pix_c)) < int(150):
    #         elif int(min(white_pix_c)) > int(h/2):
    #             command = 'turn right'
    #             myc = np.median(yellow_pix_c)
    #             return center, int(myc + ((w - myc) / 2)), command, ratio
    #         else:
    #             command = 'straight'
    #             mwc = np.median(white_pix_c)
    #             myc = np.median(yellow_pix_c)
    #             return center, int(myc + ((mwc - myc) / 2)), command, ratio
    #
    #     else:
    #         command = 'unknown state'
    #         return center, -1, command, []
