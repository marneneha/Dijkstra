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
canvas = cv2.rectangle(canvas, pt1=rectangle1[0], pt2=rectangle1[1], color=(0,255,0), thickness=-1)
canvas = cv2.rectangle(canvas, pt1=rectangle2[0], pt2=rectangle2[1], color=(0,255,0), thickness=-1)
canvas = cv2.fillPoly(canvas, [hexagon], color=(0,255,0))
canvas = cv2.fillPoly(canvas, [traingle], color=(0,255,0))
cv2.imshow('blank map', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows() 