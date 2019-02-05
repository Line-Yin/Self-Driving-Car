import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


def main():

    img = np.array(Image.open('path_00.jpg').convert('L'))

    print(img.shape)

    img = img[int(img.shape[0] / 2):img.shape[0], :]

    R, C = np.where(img >= 210)

    for i in range(len(R)):
        img[R[i]][C[i]] = 0

    plt.imshow(img, cmap='gray')

    plt.show()


main()
