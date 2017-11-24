# shybot.py
from __future__ import print_function
from imutils.video import  VideoStream
from gpiozero import AngularServo
import argparse
import imutils
import time
import cv2
from random import randint

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--display",dest="display", action="store_true")
ap.set_defaults(display=False)
args = vars(ap.parse_args())

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

display = args["display"]

print("[INFO] Display=",display)
print("[INFO] Waiting for pi cam to warmup...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)


print("[INFO] Waking up servos...")

#
# Change this servo settings for your bots
#
sv = AngularServo(3,min_angle=-50,max_angle=50)
sh = AngularServo(2, min_angle=-50, max_angle=50)

v=0
h=0
d=10

#init the first frame in the video stream
firstFrame = None

print("[INFO] start detection...")
while True:

    isEye = False

    # grab the next frame from the video stream
    frame = vs.read()

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    frame = imutils.rotate(frame, 180)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        if display:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_color = frame[y:y+h, x:x+w]
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            if display:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            isEye = True
            break

    if isEye:
        print("[INFO] Face detected.")
        # move to random position
        sh.angle = randint(-50,50)
        sv.angle = randint(-50,50)
    else:
        sh.detach()
        sv.detach()

    if display:
        cv2.imshow("Shybot's view", frame)

    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        break


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

