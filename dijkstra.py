import numpy as np
import matplotlib.pyplot as plt
import cv2
import pprint
import heapq as hq
import math
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
    start_node=[int(j) for j in input().split()]
    start_node = tuple(start_node)
    print("start node is")
    print(start_node)
    valid_node=node_validity(map, start_node)
    while(not valid_node):
        print("node you entered is in obstacle space. plese reenter a valid node")
        start_node=[int(j) for j in input().split()]
        valid_node=node_validity(map, start_node)
    map[start_node[1], start_node[0]] = (0, 255, 0)
    # cv2.circle(map, (start_node[0], start_node[1]), 0, (0, 255, 0), -1)
    # cv2.imshow('color_map',map)
    # cv2.waitKey(0)
    start_node = (50, 110)
    return map, start_node

def get_goal_node(map):
    print("enter goal node. entering convention should be x y where bottom left is the origin. keep space between the cordinate not comma")
    # after entering you should see the node updated on the map
    # start_node = input()
    goal_node=[int(j) for j in input().split()]
    goal_node = tuple(goal_node)
    print(goal_node)
    valid_node=node_validity(map, goal_node)
    while(not valid_node):
        print("node you entered is in obstacle space. plese reenter a valid node")
        goal_node=[int(j) for j in input().split()]
        valid_node=node_validity(map, goal_node)
    map[goal_node[1], goal_node[0]] = (0, 0, 255)

    # cv2.circle(map, (goal_node[0], goal_node[1]), 1, (0, 0, 255), -1)
    goal_node = (50, 200)
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

def h_cost_calc(node, goal_node):
    # print(node)
    # print(goal_node)
    x1,y1=node[0:2]
    x2,y2=goal_node[0:2]
    # print(x1, y1, x2, y2)
    dist = math.sqrt((x1-x2)**2+(y1-y2)**2)
    return dist

def explore_map(map, start_node, goal_node):
    print("inside explore")
    output_video = cv2.VideoWriter('Proj3_neha_anukriti.avi', cv2.VideoWriter_fourcc(*'XVID'), 800, (map.shape[1], map.shape[0])) 
    # parent_node = start_node
    # cost present node parent node
    open_list = [(0, start_node, start_node)]#heap data structure of tuples 
    closed_list = {}#dict
    hq.heapify(open_list)
    # hq.heappush(open_list)
    # print(open_list)
    while(len(open_list)):
    # open_list.append(start_node)
        # newclosed list is a tuple of 3 element
        new_closed_list_element = hq.heappop(open_list)
        # print(new_closed_list_element)
        closed_list[tuple(new_closed_list_element[1])]=tuple(new_closed_list_element[2])
        # print(closed_list)
        parent_node = new_closed_list_element[1]
        parent_node_cost = new_closed_list_element[0]
        if(h_cost_calc(parent_node, goal_node))<2:
            final_parent_node = parent_node
            # print(bcolors.FAIL+"Goal node has been reachead going to backtrack the path"+bcolors.ENDC)
            back_track(start_node, final_parent_node, output_video, closed_list, map)
            break
        # explore and update the nbr
        open_list, map, node_up, output_video = add_node_up(open_list, closed_list, map, output_video, parent_node, parent_node_cost)
        open_list, map, node_up, output_video = add_node_down(open_list, closed_list, map, output_video, parent_node, parent_node_cost)
        open_list, map, node_up, output_video = add_node_right(open_list, closed_list, map, output_video, parent_node, parent_node_cost)
        open_list, map, node_up, output_video = add_node_left(open_list, closed_list, map, output_video, parent_node, parent_node_cost)
        open_list, map, node_up, output_video = add_node_right_up(open_list, closed_list, map, output_video, parent_node, parent_node_cost)
        open_list, map, node_up, output_video = add_node_left_up(open_list, closed_list, map, output_video, parent_node, parent_node_cost)
        open_list, map, node_up, output_video = add_node_right_bottom(open_list, closed_list, map, output_video, parent_node, parent_node_cost)
        open_list, map, node_up, output_video = add_node_left_bottom(open_list, closed_list, map, output_video, parent_node, parent_node_cost)
        
    return map

def back_track(start_position, final_parent_node, output_video, closed_list, map):
    # print(bcolors.FAIL+"closted list is"+str(closed_list)+bcolors.ENDC)
    child_node = final_parent_node
    parent_node = closed_list[child_node]
    # print(child_node)
    # print(parent_node)
    # parent_node = final_parent_node
    # child_node = closed_list[final_parent_node]
    # cv2.circle(canvas,(int(parent_node[0]),int(parent_node[1])),2,(255,255,255),-1)
    while(child_node != parent_node):
        map[child_node[1], child_node[0]] = (0, 120, 120)
        # cv2.circle(map,(int(child_node[0]),int(child_node[1])),2,(0,120,120),-1)
        # cv2.imshow('canvas',canvas)
        # cv2.waitKey(0)
        child_node = parent_node
        parent_node = closed_list[child_node]
        # time.sleep(1)
        map=np.uint8(map)
        output_video.write(map)
    # for k in closed_list:
    #     canvas[k[1], k[0]] = [255] * 3
    #     cv2.imshow(canvas)
    output_video.release()

# only checks if node can be added
def add_node_up(open_list, closed_list, map, output_video, parent_node, parent_node_cost):
    # print("checking to add node up")
    child_node = (parent_node[0], parent_node[1]+1)
    # print(child_node)
    # if the node is present in the obstacle space and and is not present in closed list
    if(node_validity(map, child_node) and not closed_list.__contains__(child_node) ):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        # add /update elemnt in open list
        new_cost = parent_node_cost+1
        new_open_list_element = [new_cost, child_node, parent_node]
        hq.heappush(open_list, new_open_list_element)
        hq.heapify(open_list)
        # if (new_cost<child_node[0]):
            # new_open_list = (new_cost, child_node, parent_node)
       # print("open list is"+str(open_list))
       # cv2.imshow('map', map)
       # cv2.waitKey(0)
        #  print("m here")
        # open_list.append(new_open_list)
        map=np.uint8(map)
        output_video.write(map)
        return open_list, map, True, output_video
    else:
        return open_list, map, False, output_video
# only checks if node can be added
def add_node_down(open_list, closed_list, map, output_video, parent_node, parent_node_cost):
    # print("checking to add node down")
    child_node = (parent_node[0], parent_node[1]-1)
    # print(child_node)
    # if the node is present in the obstacle space and and is not present in closed list
    if(node_validity(map, child_node) and not closed_list.__contains__(child_node) ):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        # add /update elemnt in open list
        new_cost = parent_node_cost+1
        new_open_list_element = [new_cost, child_node, parent_node]
        hq.heappush(open_list, new_open_list_element)
        hq.heapify(open_list)
        # if (new_cost<child_node[0]):
            # new_open_list = (new_cost, child_node, parent_node)
       # print("open list is"+str(open_list))
       # cv2.imshow('map', map)
       # cv2.waitKey(0)
        #  print("m here")
        # open_list.append(new_open_list)
        map=np.uint8(map)
        output_video.write(map)
        return open_list, map, True, output_video
    else:
        return open_list, map, False, output_video
# only checks if node can be added
def add_node_right(open_list, closed_list, map, output_video, parent_node, parent_node_cost):
    # print("checking to add node right")
    child_node = (parent_node[0]+1, parent_node[1])
    # print(child_node)
    # print("open list is"+str(open_list))
    # if the node is present in the obstacle space and and is not present in closed list
    if(node_validity(map, child_node) and not closed_list.__contains__(child_node) ):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        # add /update elemnt in open list
        new_cost = parent_node_cost+1
        new_open_list_element = [new_cost, child_node, parent_node]
        hq.heappush(open_list, new_open_list_element)
        hq.heapify(open_list)
        # if (new_cost<child_node[0]):
            # new_open_list = (new_cost, child_node, parent_node)
       # print("open list is"+str(open_list))
       # cv2.imshow('map', map)
       # cv2.waitKey(0)
        #  print("m here")
        # open_list.append(new_open_list)
        map=np.uint8(map)
        output_video.write(map)
        return open_list, map, True, output_video
    else:
        return open_list, map, False, output_video
# only checks if node can be added
def add_node_left(open_list, closed_list, map, output_video, parent_node, parent_node_cost):
    # print("checking to add node left")
    child_node = (parent_node[0]-1, parent_node[1])
    # print(child_node)
    # if the node is present in the obstacle space and and is not present in closed list
    if(node_validity(map, child_node) and not closed_list.__contains__(child_node) ):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        # add /update elemnt in open list
        new_cost = parent_node_cost+1
        new_open_list_element = [new_cost, child_node, parent_node]
        hq.heappush(open_list, new_open_list_element)
        hq.heapify(open_list)
        # if (new_cost<child_node[0]):
            # new_open_list = (new_cost, child_node, parent_node)
       # print("open list is"+str(open_list))
       # cv2.imshow('map', map)
       # cv2.waitKey(0)
        #  print("m here")
        # open_list.append(new_open_list)
        map=np.uint8(map)
        output_video.write(map)
        return open_list, map, True, output_video
    else:
        return open_list, map, False, output_video
# only checks if node can be added
def add_node_right_up(open_list, closed_list, map, output_video, parent_node, parent_node_cost):
    # print("checking to add node up")
    child_node = (parent_node[0]+1, parent_node[1]+1)
    # print(child_node)
    # if the node is present in the obstacle space and and is not present in closed list
    if(node_validity(map, child_node) and not closed_list.__contains__(child_node) ):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        # add /update elemnt in open list
        new_cost = parent_node_cost+1.4
        new_open_list_element = [new_cost, child_node, parent_node]
        hq.heappush(open_list, new_open_list_element)
        hq.heapify(open_list)
        # if (new_cost<child_node[0]):
            # new_open_list = (new_cost, child_node, parent_node)
       # print("open list is"+str(open_list))
       # cv2.imshow('map', map)
       # cv2.waitKey(0)
        #  print("m here")
        # open_list.append(new_open_list)
        map=np.uint8(map)
        output_video.write(map)
        return open_list, map, True, output_video
    else:
        return open_list, map, False, output_video
# only checks if node can be added
def add_node_left_up(open_list, closed_list, map, output_video, parent_node, parent_node_cost):
    # print("checking to add node up")
    child_node = (parent_node[0]-1, parent_node[1]+1)
    # print(child_node)
    # if the node is present in the obstacle space and and is not present in closed list
    if(node_validity(map, child_node) and not closed_list.__contains__(child_node) ):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        # add /update elemnt in open list
        new_cost = parent_node_cost+1.4
        new_open_list_element = [new_cost, child_node, parent_node]
        hq.heappush(open_list, new_open_list_element)
        hq.heapify(open_list)
        # if (new_cost<child_node[0]):
            # new_open_list = (new_cost, child_node, parent_node)
       # print("open list is"+str(open_list))
       # cv2.imshow('map', map)
       # cv2.waitKey(0)
        #  print("m here")
        # open_list.append(new_open_list)
        map=np.uint8(map)
        output_video.write(map)
        return open_list, map, True, output_video
    else:
        return open_list, map, False, output_video
# only checks if node can be added
def add_node_right_bottom(open_list, closed_list, map, output_video, parent_node, parent_node_cost):
    # print("checking to add node up")
    child_node = (parent_node[0]+1, parent_node[1]-1)
    # print(child_node)
    # if the node is present in the obstacle space and and is not present in closed list
    if(node_validity(map, child_node) and not closed_list.__contains__(child_node) ):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        # add /update elemnt in open list
        new_cost = parent_node_cost+1.4
        new_open_list_element = [new_cost, child_node, parent_node]
        hq.heappush(open_list, new_open_list_element)
        hq.heapify(open_list)
        # if (new_cost<child_node[0]):
            # new_open_list = (new_cost, child_node, parent_node)
       # print("open list is"+str(open_list))
       # cv2.imshow('map', map)
       # cv2.waitKey(0)
        #  print("m here")
        # open_list.append(new_open_list)
        map=np.uint8(map)
        output_video.write(map)
        return open_list, map, True, output_video
    else:
        return open_list, map, False, output_video
# only checks if node can be added
def add_node_left_bottom(open_list, closed_list, map, output_video, parent_node, parent_node_cost):
    # print("checking to add node up")
    child_node = (parent_node[0]-1, parent_node[1]-1)
    # print(child_node)
    # if the node is present in the obstacle space and and is not present in closed list
    if(node_validity(map, child_node) and not closed_list.__contains__(child_node) ):
        # print("up node can be added")
        map[child_node[1], child_node[0]] = (0, 255, 0)
        # add /update elemnt in open list
        new_cost = parent_node_cost+1.4
        new_open_list_element = [new_cost, child_node, parent_node]
        hq.heappush(open_list, new_open_list_element)
        hq.heapify(open_list)
        # if (new_cost<child_node[0]):
            # new_open_list = (new_cost, child_node, parent_node)
       # print("open list is"+str(open_list))
       # cv2.imshow('map', map)
       # cv2.waitKey(0)
        #  print("m here")
        # open_list.append(new_open_list)
        map=np.uint8(map)
        output_video.write(map)
        return open_list, map, True, output_video
    else:
        return open_list, map, False, output_video

map = draw_map()
# cv2.imshow('map', map)
map, start_node = get_start_node(map)
# cv2.imshow('map', map)
map, goal_node = get_goal_node(map)
map = explore_map(map, start_node, goal_node)
cv2.imshow('map', map)

cv2.waitKey(0)
cv2.destroyAllWindows() 