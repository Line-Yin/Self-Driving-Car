from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
# from detect_rgb5 import detect


X_RESOLUTION = 960
Y_RESOLUTION = 720

camera = PiCamera()
camera.resolution = (X_RESOLUTION, Y_RESOLUTION)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(X_RESOLUTION, Y_RESOLUTION))

time.sleep(0.1)
i = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    img = frame.array

    h, w, _ = img.shape

    img = img[int(h/2):h, :, :]

    # center, mid, command, ratio = detect(img)

    cv2.imwrite('960/green' + str(i) + '.jpg', img)

    print('took image: ', i)

    rawCapture.truncate(0)

    i += 1

    if i == 5:
        break

    time.sleep(2)
