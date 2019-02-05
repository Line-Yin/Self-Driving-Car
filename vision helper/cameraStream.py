from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from detect_rgb2 import detect
import serial


X_RESOLUTION = 1280
Y_RESOLUTION = 960

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (X_RESOLUTION, Y_RESOLUTION)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(X_RESOLUTION, Y_RESOLUTION))

# Allow camera to warmup
time.sleep(0.1)

#Capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Grab the raw NumPy array representing the image
    start = time.time()
    img = frame.array
    key = cv2.waitKey(1) & 0xFF
    # Clear the stream so it is ready to receive the next frame
    rawCapture.truncate(0)
    center, mid, command = detect(img)
    print(command + ' ' + str([center, mid[1]]))
    end = time.time()
    print('time: ' + str(end - start))
    time.sleep(1)
    # If the 'q' key was pressed, break from the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
