import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2


def detect(img):
    h, w, _ = img.shape
    img = cv2.GaussianBlur(img, (5, 5), 0)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    #
    # # # latest
    yellow_low = np.array([26, 30, 100])
    yellow_high = np.array([34, 255, 255])
    #
    # latest
    # yellow_low = np.array([20, 43, 46])
    # yellow_high = np.array([34, 255, 255])

    mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
    #
    _, col = np.where(mask_yellow > 0)

    result = cv2.bitwise_and(img, img, mask=mask_yellow)

    return result, int(np.median(col))


# for i in range(5):

img = np.array(Image.open('test_mid.jpg'))

# img, center, mid = detect(img)

img, m = detect(img)

# print([center, mid])

img[:, m-5:m+5, :] = [255, 0, 0]

# plt.subplot(3, 3, i+1)
plt.imshow(img)
plt.title(m)

plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()
