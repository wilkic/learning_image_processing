
import cv2

vcap = cv2.VideoCapture('rtsp://108.45.109.111:561/live0.264')

while(1):

    ret, frame = vcap.read()
    cv2.imshow('VIDEO', frame)
    cv2.waitKey(1)

