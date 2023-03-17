import numpy as np
import matplotlib.pyplot as plt
import cv2
rectangle1 = [(100,0), (150, 100)]
rectangle2 = [(100,250), (150, 150)]
hexagon = np.array([[300, 200], [365, 162],
                    [365, 88], [300, 50],
                    [235, 88], [235, 162]],
                    np.int32)
traingle = np.array([[460, 25], [460, 225],
                    [510, 125]],
                    np.int32)
canvas = np.ones((250, 600, 3))
canvas = cv2.rectangle(canvas, pt1=rectangle1[0], pt2=rectangle1[1], color=(0,0,0), thickness=-1)
canvas = cv2.rectangle(canvas, pt1=rectangle2[0], pt2=rectangle2[1], color=(0,0,0), thickness=-1)
canvas = cv2.fillPoly(canvas, [hexagon], color=(0,0,0))
canvas = cv2.fillPoly(canvas, [traingle], color=(0,0,0))
canvas = np.float32(canvas)
canvas[0:5,:]=(0,0,0)
canvas[:,0:5]=(0,0,0)
canvas[-5:-1,:]=(0,0,0)
canvas[:,-5:-1]=(0,0,0)
print(canvas.shape)
gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
gausBlur = cv2.GaussianBlur(gray_canvas, (11,11),0) 
dest_and = cv2.bitwise_and(gausBlur, gray_canvas, mask = None)

cv2.imshow('original map', canvas)
cv2.imshow('gray map', gray_canvas)
cv2.imshow('gauss', gausBlur)
cv2.imshow('dest_and', dest_and)
cv2.waitKey(0)
cv2.destroyAllWindows() 