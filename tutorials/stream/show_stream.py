
import cv2
import matplotlib.pyplot as plt


def nothing(x):
    pass



#fgbg = cv2.createBackgroundSubtractorMOG2()
#fgbg = cv2.BackgroundSubtractorMOG(history=2000,nmixtures=5,backgroundRatio=0.9)
fgbg = cv2.BackgroundSubtractorMOG()

#vcap = cv2.VideoCapture('rtsp://108.45.109.111:8504/live0.264')
vcap = cv2.VideoCapture(0)

cv2.namedWindow('frame')
cv2.namedWindow('fg')
cv2.namedWindow('thresh')
cv2.namedWindow('cont')

hw_blur = 1
hw_min = 1
cv2.createTrackbar('blur','frame',hw_blur,200,nothing)

nitr_dilation = 20
cv2.createTrackbar('dil-itr','thresh',nitr_dilation,100,nothing)

learning_rate = 8
cv2.createTrackbar('learning-rate','fg',learning_rate,100,nothing)

min_area = 400
cv2.createTrackbar('min-area','cont',min_area,10000,nothing)

firstFrame = None
while(1):

    ret, frame = vcap.read()

    # Our operations on the frame come here
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Blur it
    #blur = cv2.GaussianBlur(imgray, (21, 21), 0)
    hw = int(hw_blur)
    hw = max( hw, hw_min )
    if (hw % 2 == 0):
        hw += 1
    #blur = cv2.GaussianBlur(imgray, (hw, hw), 0)
    #blur = cv2.bilateralFilter(imgray, hw, 75, 75)
    blur = cv2.medianBlur(imgray, hw)
    #blur = imgray.copy()

    # Subtract the background
    #fgmask = fgbg.apply(blur)
    if learning_rate < 2:
        rate = 0.5
    else:
        rate = 1. / learning_rate
    fgmask = fgbg.apply(blur, learningRate=rate)
    #thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = fgmask
    
#    # if the first frame is None, initialize it
#    if firstFrame is None:
#        firstFrame = blur
#        continue
#    frameDelta = cv2.absdiff(firstFrame, blur )
#    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=nitr_dilation)
 
    # find contours
    # on thresholded image
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	    cv2.CHAIN_APPROX_SIMPLE)
    
    cim = frame.copy()

    # loop over the contours
    for c in cnts:
	    # if the contour is too small, ignore it
	    if cv2.contourArea(c) < min_area:
		continue

	    # compute the bounding box for the contour, draw it on the frame,
	    (x, y, w, h) = cv2.boundingRect(c)
	    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # draw the contour
	    cv2.drawContours( cim, c, -1, (0,255,0), 5 )

    # Display the resulting frame
    cv2.imshow('fg', fgmask)
    cv2.imshow('thresh', thresh)
    cv2.imshow('frame', frame)
    cv2.imshow('cont', cim)
    #cv2.imshow('you',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    nitr_dilation = cv2.getTrackbarPos('dil-itr','thresh')
    hw_blur = cv2.getTrackbarPos('blur','frame')
    min_area = cv2.getTrackbarPos('min-area','cont')
    learning_rate = cv2.getTrackbarPos('learning-rate','fg')


# When everything done, release the capture
vcap.release()
cv2.waitKey(-1)
cv2.destroyAllWindows()


