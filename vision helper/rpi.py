from picamera import PiCamera
import serial
import time
import numpy as np
from PIL import Image


def main():

    port = '/dev/cu.usbmodem14101'
    ser = serial.Serial(port, 9600, timeout=2)

    ml = 100
    mr = 100

    motor_command = str(ml) + ' ' + str(mr)
    ser.write(motor_command.encode())

    camera = PiCamera()
    camera.color_effects = (128, 128)
    # camera.framerate = 10
    camera.start_preview()

    path = '/home/pi/Desktop/503/path.jpg'

    prev = 640 / 2

    while True:

        s = time.time()
        camera.capture(path)
        img = np.array(Image.open(path).convert('L'))
        mid = detect_mid(img)
        print('= = = = = = =')
        e = time.time()
        print(e`-s)
        # print(img.shape)

    camera.stop_preview()


main()
