import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time
import operator
import cv2


img = np.array(Image.open('1028/yellow1/path_0.jpg'))
img = img[int(img.shape[0]/2):int(img.shape[0]), :, :]
img = cv2.GaussianBlur(img, (5, 5), 0)
hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

d = {}

# H = hsv_img[:, :, 0]

for r in hsv_img:
    for c in r:
        c = (c[0], c[1], c[2])
        if c in d.keys():
            d[c] += 1
        else:
            d[c] = 1

sorted_d = sorted(d.items(), key=operator.itemgetter(1),reverse=True)

# for k, v in sorted_d:
# #     if v >= 4000:
# #         print(k, v)

print(sorted_d)
