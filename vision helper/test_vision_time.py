from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from detect_rgb5 import detect


X_RESOLUTION = 960
Y_RESOLUTION = 720

camera = PiCamera()
camera.resolution = (X_RESOLUTION, Y_RESOLUTION)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(X_RESOLUTION, Y_RESOLUTION))

time.sleep(0.1)
i = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    start = time.time()

    img = frame.array

    h, _, _ = img.shape

    img = img[int(h / 2):h, :, :]

    key = cv2.waitKey(1) & 0xFF

    center, mid, command, ratio = detect(img)

    end = time.time()

    if i % 3 == 0:
        print('= = = = =')
        print(command)
        print(ratio)
        print(end - start)

    rawCapture.truncate(0)

    i += 1
