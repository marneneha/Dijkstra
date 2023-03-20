import numpy as np
import matplotlib.pyplot as plt
import cv2
import pprint
import heapq as hq

# global canvas
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
    # drawing all shape obstacle in the map
    canvas = cv2.rectangle(canvas, pt1=rectangle1[0], pt2=rectangle1[1], color=(0,0,0), thickness=-1)
    canvas = cv2.rectangle(canvas, pt1=rectangle2[0], pt2=rectangle2[1], color=(0,0,0), thickness=-1)
    canvas = cv2.fillPoly(canvas, [hexagon], color=(0,0,0))
    canvas = cv2.fillPoly(canvas, [traingle], color=(0,0,0))
    canvas = np.float32(canvas)
    # drawing the wall
    canvas[0:10,:]=(0,0,0)
    canvas[:,0:10]=(0,0,0)
    canvas[240:250,:]=(0,0,0)
    canvas[:,590:600]=(0,0,0)
    # convert to grayscale
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    # edge detection
    gray=np.uint8(gray)
    edged = cv2.Canny(gray, 200, 200, L2gradient =True)
    # find and draw contours
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(canvas, contours, -1, (255, 0, 0), 3)
    return canvas

def get_start_node(map):
    print("enter start node. entering convention should be x y where bottom left is the origin. keep space between the cordinate not comma")
    # after entering you should see the node updated on the map
    # start_node = input()
    start_node = np.array([50, 110])
    # start_node=[int(j) for j in input().split()]
    # print("start node is")
    # print(start_node)
    valid_node=node_validity(map, start_node)
    while(not valid_node):
        print("node you entered is in obstacle space. plese reenter a valid node")
        start_node=[int(j) for j in input().split()]
        valid_node=node_validity(map, start_node)
    map[start_node[1], start_node[0]] = (0, 255, 0)
    # cv2.circle(map, (start_node[0], start_node[1]), 0, (0, 255, 0), -1)
    # cv2.imshow('color_map',map)
    # cv2.waitKey(0)
    return map, start_node

def get_goal_node(map):
    print("enter goal node. entering convention should be x y where bottom left is the origin. keep space between the cordinate not comma")
    # after entering you should see the node updated on the map
    # start_node = input()
    # goal_node=[int(j) for j in input().split()]
    # print(start_node)
    goal_node = np.array([200, 200])
    valid_node=node_validity(map, goal_node)
    while(not valid_node):
        print("node you entered is in obstacle space. plese reenter a valid node")
        goal_node=[int(j) for j in input().split()]
        valid_node=node_validity(map, goal_node)
    map[goal_node[1], goal_node[0]] = (0, 0, 255)

    # cv2.circle(map, (goal_node[0], goal_node[1]), 1, (0, 0, 255), -1)
    return map, goal_node

def node_validity(map, node):
    # print("inside node availability")
    # print(map[node[1], node[0]])
    # print(node)
    if(np.sum(map[node[1], node[0]])):
        if(np.array_equal(map[node[1], node[0]], np.array([255,255,255]))):
            return True
        else:
            return False
    else:
        False

def explore_map(map, start_node, goal_node):
    print("inside explore")
    # parent_node = start_node
    # cost present node parent node
    open_list = [(0, start_node, start_node)]#heap data structure of tuples 
    closed_list = {}#dict
    hq.heapify(open_list)
    # hq.heappush(open_list)
    print(open_list)
    while(len(open_list)):
    # open_list.append(start_node)
        # newclosed list is a tuple of 3 element
        new_closed_list_element = hq.heappop(open_list)
        print(new_closed_list_element)
        closed_list[tuple(new_closed_list_element[1])]=tuple(new_closed_list_element[2])
        print(closed_list)
        parent_node = new_closed_list_element[1]
        parent_node_cost = new_closed_list_element[0]
        # explore and update the nbr
        open_list, map, node_up = add_node_up(open_list, closed_list, map, parent_node, parent_node_cost)
        open_list, map, node_up = add_node_down(open_list, closed_list, map, parent_node, parent_node_cost)
        open_list, map, node_up = add_node_right(open_list, closed_list, map, parent_node, parent_node_cost)
        open_list, map, node_up = add_node_left(open_list, closed_list, map, parent_node, parent_node_cost)

# only checks if node can be added
def add_node_up(open_list, closed_list, map, parent_node):
    print("checking to add node up")
    child_node = (parent_node[0], parent_node[1]+1)
    print(child_node)
    # if the node is present in the obstacle space and and is not present in closed list
    if(node_validity(map, child_node) and not closed_list.__contains__(child_node) ):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        # add /update elemnt in open list
        new_cost = parent_node[0]+1
        new_open_list_element = [new_cost, child_node, parent_node]
        hq.heappush(open_list, new_open_list_element)
        hq.heapify(open_list)
        # if (new_cost<child_node[0]):
            # new_open_list = (new_cost, child_node, parent_node)
        cv2.imshow('map', map)
        cv2.waitKey(0)
        #  print("m here")
        # open_list.append(new_open_list)
        return open_list, map, True
    else:
        return False
        # print("could not add node up")

# only checks if node can be added
def add_node_down(map, parent_node):
    # print("checking to add node up")
    child_node = np.array([parent_node[0], parent_node[1]-1])
    print(child_node)
    if(node_validity(map, child_node)):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        return map, True
    else:
        return False
        # print("could not add node up")

# only checks if node can be added
def add_node_right(map, parent_node):
    # print("checking to add node up")
    child_node = np.array([parent_node[0]+1, parent_node[1]])
    print(child_node)
    if(node_validity(map, child_node)):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        return map, True
    else:
        return False
        # print("could not add node up")

# only checks if node can be added
def add_node_left(map, parent_node):
    # print("checking to add node up")
    child_node = np.array([parent_node[0]-1, parent_node[1]])
    print(child_node)
    if(node_validity(map, child_node)):
        # print("up node can be added")
        # add/update cost
        # if 
        # child_node.cost = parent_node.cost+1
        # add/update parent
        # child_node.parent = parent_node
        # if the node has not been explored add it to the OL
        # OL.append(child_node)
        map[child_node[1], child_node[0]] = (0, 255, 0)
        return map, True
    else:
        return False
        # print("could not add node up")

# only checks if node can be added
def add_node_right_up(map, parent_node):
    # print("checking to add node up")
    child_node = np.array([parent_node[0]+1, parent_node[1]+1])
    print(child_node)
    if(node_validity(map, child_node)):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        return map, True
    else:
        return False
        # print("could not add node up")

# only checks if node can be added
def add_node_left_up(map, parent_node):
    # print("checking to add node up")
    child_node = np.array([parent_node[0]-1, parent_node[1]+1])
    print(child_node)
    if(node_validity(map, child_node)):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        return map, True
    else:
        return False
        # print("could not add node up")

# only checks if node can be added
def add_node_right_bottom(map, parent_node):
    # print("checking to add node up")
    child_node = np.array([parent_node[0]+1, parent_node[1]-1])
    print(child_node)
    if(node_validity(map, child_node)):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        return map, True
    else:
        return False
        # print("could not add node up")
# only checks if node can be added

def add_node_left_bottom(map, parent_node):
    # print("checking to add node up")
    child_node = np.array([parent_node[0]-1, parent_node[1]-1])
    print(child_node)
    if(node_validity(map, child_node)):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        return map, True
    else:
        return False
        # print("could not add node up")




map = draw_map()
# cv2.imshow('map', map)
map, start_node = get_start_node(map)
# cv2.imshow('map', map)
map, goal_node = get_goal_node(map)
explore_map(map, start_node, goal_node)
cv2.imshow('map', map)

cv2.waitKey(0)
cv2.destroyAllWindows() 