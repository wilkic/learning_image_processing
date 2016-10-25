
cc = contour_info[1][0]
x,y,w,h = cv2.boundingRect(cc)
mask = np.zeros(im.shape,np.uint8)
mask[y:y+h,x:x+w] = im[y:y+h,x:x+w]


M = cv2.moments( contour_info[0][0] )
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])


