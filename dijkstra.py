import numpy as np
import matplotlib.pyplot as plt
import cv2
import pprint
global canvas
def draw_map():
    #upper rectangle
    rectangle1 = [(100,0), (150, 100)]
    #lower rectangle
    rectangle2 = [(100,250), (150, 150)]
    hexagon = np.array([[300, 200], [365, 162],
                        [365, 88], [300, 50],
                        [235, 88], [235, 162]],
                        np.int32)
    traingle = np.array([[460, 25], [460, 225],
                        [510, 125]],
                        np.int32)
    canvas = 255*np.ones((250, 600, 3))
    canvas = cv2.rectangle(canvas, pt1=rectangle1[0], pt2=rectangle1[1], color=(0,0,0), thickness=-1)
    canvas = cv2.rectangle(canvas, pt1=rectangle2[0], pt2=rectangle2[1], color=(0,0,0), thickness=-1)
    canvas = cv2.fillPoly(canvas, [hexagon], color=(0,0,0))
    canvas = cv2.fillPoly(canvas, [traingle], color=(0,0,0))
    canvas = np.float32(canvas)
    canvas[0:10,:]=(0,0,0)
    canvas[:,0:10]=(0,0,0)
    canvas[240:250,:]=(0,0,0)
    canvas[:,590:600]=(0,0,0)
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    # canny = cv2.Canny(gray_transformed_image, 200, 220, L2gradient =True)
    gray=np.uint8(gray)
    edged = cv2.Canny(gray, 200, 200, L2gradient =True)
    cv2.imshow('edged',edged)
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    print("m here")
    print(contours)
    for i in range(len(contours)):
        cv2.drawContours(canvas, contours, i, (0, 255, 0), 3)
    # cv2.drawContours(canvas, contours, -1, (0, 0, 0), -1)
    cv2.imshow('Contours', canvas)
    cv2.waitKey(0)
    # print(canvas.shape)
    # gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray_canvas',gray_canvas)
    # gausBlur = cv2.blur(gray_canvas, (11,11),0) 
    # cv2.imshow('gausBlur',gausBlur)
    # dest_and = cv2.bitwise_and(gausBlur, gray_canvas, mask = None)
    # cv2.imshow('dest_and',dest_and)
    # cv2.waitKey(0)

    return canvas

def get_start_node(map):
    print("enter start node. entering convention should be x y where bottom left is the origin. keep space between the cordinate not comma")
    # after entering you should see the node updated on the map
    # start_node = input()
    start_node=[int(j) for j in input().split()]
    # print(start_node)
    valid_node=node_validity(map, start_node)
    while(not valid_node):
        print("node you entered is in obstacle space. plese reenter a valid node")
        start_node=[int(j) for j in input().split()]
        valid_node=node_validity(map, start_node)
    color_map = cv2.cvtColor(map, cv2.COLOR_GRAY2BGR)
    cv2.circle(color_map, (start_node[0], start_node[1]), 10, (255, 0, 0), -1)
    cv2.imshow('color_map',color_map)
    gray_map = cv2.cvtColor(color_map, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray_map',gray_map)
    retrun_color_map = cv2.cvtColor(gray_map, cv2.COLOR_GRAY2BGR)
    cv2.imshow('retrun_color_map',retrun_color_map)
    print("neha here")
    cv2.waitKey(0)
    return map, start_node

def get_goal_node(map):
    print("enter goal node. entering convention should be x y where bottom left is the origin. keep space between the cordinate not comma")
    # after entering you should see the node updated on the map
    # start_node = input()
    goal_node=[int(j) for j in input().split()]
    # print(start_node)
    # valid_node=node_validity(map, goal_node)
    while(not valid_node):
        print("node you entered is in obstacle space. plese reenter a valid node")
        goal_node=[int(j) for j in input().split()]
        valid_node=node_validity(map, goal_node)
    cv2.circle(map, (start_node[0], start_node[1]), 2, (255, 0, 0), -1)
    return map, goal_node

def node_validity(map, node):
            # if(np.array_equal(transformed_image[row, column], np.array([0, 0, 255]))):
    print("node is")
    print(node)
    print("map value is")
    print(map[node[1], node[0]])
    if(map[node[1], node[0]]==1):
        return True
    else:
        return False

map = draw_map()
print(map.shape)
# map, start_node = get_start_node(map)
# map, goal_node = get_goal_node(map)
# color_map = cv2.cvtColor(map, cv2.COLOR_GRAY2BGR)

# cv2.imshow('dest_and', color_map)

cv2.waitKey(0)
cv2.destroyAllWindows() 