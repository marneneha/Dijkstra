#Import important libraries 
import time
import copy
import cv2
# uncomment below line if running in colab
# from google.colab.patches import cv2_imshow
import heapq as hq
import numpy as np



# function to draw the obstacles on a canvas map 
def obstacles_map(canvas):
    # rectangle 1 obstacle with the given dimensions, the thickness of 5mm is considered inwards
    cv2.fillPoly(canvas, pts = [np.array([(100,150), (150,150), (150,250), (100,250)])], color = (255, 0, 0))
    # rectangle 2 obstacle with the given dimensions, the thickness of 5mm is considered inwards
    cv2.fillPoly(canvas, pts = [np.array([(100,0), (150,0), (150,100), (100,100)])], color = (255, 0, 0))
    # heaxgon obstacle with the given dimensions, the thickness of 5mm is considered inwards
    cv2.fillPoly(canvas, pts = [np.array([(235,87),(300,50),(365,87),(365,162),(300,200),(235,162)])], color = (255, 0, 0))
    # traingle obstacle with the given dimensions, the thickness of 5mm is considered inwards
    cv2.fillPoly(canvas, pts = [np.array([(460,225), (510,125), (460,25)])], color = (255, 0, 0))
    return canvas


# the function to take start and goal node coordinates and to check if the nodes are invalid
def coord_input(canvas):
  # initialize empty lists
    start_position = []
    goal_position = [] 
    # Get X and Y coordinates for the start node/position
    while True:
        state = input("Enter the X Coordinate of Start position: ")
        try:
            x = int(state)
        except ValueError:
            # if the coordinate entered is not integer, ask again
            print("Enter a valid integer for X Coordinate instead")
            continue
        if not (0 <= x < canvas.shape[1]):
            # to check if the coordinate value entered is greater than the canvas dimensions
            print("X Coordinate is out of bounds")
            continue
        state = input("Enter the Y Coordinate of Start position: ")
        try:
            y = int(state)
        except ValueError:
          # if the coordinate entered is not integer, ask again
            print("Please enter a valid integer for Y Coordinate instead")
            continue
        if not (0 <= y < canvas.shape[0]):
          # to check if the coordinate value entered is greater than the canvas dimensions
            print("Y Coordinate is out of bounds")
            continue        
        if(canvas[canvas.shape[0]-1-y][x][0]==255 or 0<=x<5 or 0<=y<5):
          # to check if the entered coordinates of x and y lie inside the obstacle space
            print("The entered start position is in the obstacle space, enter again")
            continue      
        start_position = [x, y]
        break   
    # now for final state    
    # Get X and Y coordinates for the final state
    while True:
        state = input("Enter the X Coordinate of Goal position: ")
        try:
            x = int(state)
        except ValueError:
          # if the coordinate entered is not integer, ask again
            print("Please enter a valid integer for X Coordinate instead")
            continue
        if not (0 <= x < canvas.shape[1]):
        # to check if the coordinate value entered is greater than the canvas dimensions
            print("X Coordinate is out of bounds")
            continue     
        state = input("Enter the Y Coordinate of Goal position: ")
        try:
            y = int(state)
        except ValueError:
          # if the coordinate entered is not integer, ask again
            print("Please enter a valid integer for Y Coordinate instead")
            continue
        if not (0 <= y < canvas.shape[0]):
            # to check if the coordinate value entered is greater than the canvas dimensions
            print("Y Coordinate is out of bounds")
            continue    
        if(canvas[canvas.shape[0]-1-y][x][0]==255 or 0<=x<5 or 0<=y<5):
          # to check if the entered coordinates of x and y lie inside the obstacle space
            print("The entered goal node is in the obstacle space, enter again")
            continue
        goal_position = [x, y]
        break  
    return start_position, goal_position


# this function again checks if the node lies in the opaque space and within the canvas space
def check_valid_move(node, canvas, step_x, step_y):
    x, y = node
    new_x, new_y = x + step_x, y + step_y
    return (0 <= new_x < canvas.shape[1] and
            0 <= new_y < canvas.shape[0] and
            canvas[new_y][new_x][0] < 255)


# This function tries to move a node in a given direction and checks if the move is valid using is_valid_move.
# If the move is valid, it returns a tuple of True (indicating a successful move) and the new node position.
# If the move is invalid, it returns a tuple of False and the original node position.
def move_node(node, canvas, step_x, step_y):
    next_node = (node[0] + step_x, node[1] + step_y)
    if check_valid_move(node, canvas, step_x, step_y):
        return True, next_node
    else:
        return False, node
# A function for each possible move
# move up
def action_move_up(node, canvas):
    return move_node(node, canvas, 0, -1)
# move down
def action_move_down(node, canvas):
    return move_node(node, canvas, 0, 1)
# move right
def action_move_right(node, canvas):
    return move_node(node, canvas, 1, 0)
# move left
def action_move_left(node, canvas):
    return move_node(node, canvas, -1, 0)
# move up and right
def action_move_up_right(node, canvas):
    return move_node(node, canvas, 1, -1)
# move down and right
def action_move_down_right(node, canvas):
    return move_node(node, canvas, 1, 1)
# move down and left
def action_move_down_left(node, canvas):
    return move_node(node, canvas, -1, 1)
# move down and up
def action_move_up_left(node, canvas):
    return move_node(node, canvas, -1, -1)


def back_track(start_position, goal_position, final_list, canvas):
    # Create video writer to generate a video.
    output_video = cv2.VideoWriter('Anukriti_Singh_project2.avi', cv2.VideoWriter_fourcc(*'XVID'), 800, (canvas.shape[1], canvas.shape[0])) 
    # Get all the nodes that are explored.
    for k in final_list:
        canvas[k[1], k[0]] = [255] * 3
        # cv2.imshow(canvas)
        # cv2_imshow(canvas)
        cv2.waitKey(1)
        output_video.write(canvas) 
    # Backtrack the path from goal to start.
    backtrack_stack = [goal_position]
    while backtrack_stack[-1] != start_position:
        backtrack_stack.append(final_list[tuple(backtrack_stack[-1])])  
    # Draw the start and goal nodes.
    for state in (start_position, goal_position):
        cv2.circle(canvas, tuple(state), 3, ([0, 255, 0], [0, 0, 255])[state == goal_position], -1)   
    # Draw the path from start to goal.
    while backtrack_stack:
        path_node = backtrack_stack.pop()
        canvas[path_node[1], path_node[0]] = [170, 51, 106]
        output_video.write(canvas)
    # cv2.imshow(canvas)
    # cv2_imshow(canvas)
    output_video.release()

def dijkstra_algo(start_position, goal_position, canvas):
  # List of nodes to be explored
    new_list = []
  # Dictionary to hold the nodes taht are explored and its parent node
    final_list = {}
  # Flag to check if path is found
    back_track_flag = False
    # heap to store the nodes based on their cost value
    hq.heapify(new_list)
    # Inserting the initial node with its cost and parent node
    hq.heappush(new_list, [0, start_position, start_position])

    while new_list:
        # 0: cost, 1: parent node, 2: present node
        cost, parent_node, present_node = hq.heappop(new_list)
        # Adding the present node to closed list with its parent node
        final_list[(present_node[0], present_node[1])] = parent_node
        if list(present_node) == goal_position:
            back_track_flag = True
            print("Back Track")
            break
        # now using the action functions to generate the next possible moves
        for flag, next_node in [
            action_move_up(present_node, canvas),
            action_move_up_right(present_node, canvas),
            action_move_right(present_node, canvas),
            action_move_down_right(present_node, canvas),
            action_move_down(present_node, canvas),
            action_move_up_left(present_node, canvas),
            action_move_left(present_node, canvas),
            action_move_down_left(present_node, canvas),]:
            if flag:
                if next_node not in final_list:
                # Checking if the next node is already explored or not
                    temp = False
                    for i, (cost_i, parent_node_i, present_node_i) in enumerate(new_list):
                        if present_node_i == list(next_node):
                            temp = True
                            if (cost + 1) < cost_i:
                                new_list[i] = [cost + 1, present_node, list(next_node)]
                                hq.heapify(new_list)
                            break
                    if not temp:
                        hq.heappush(new_list, [cost + 1, present_node, list(next_node)])
                        hq.heapify(new_list)
    if(back_track_flag):
        #Call the backtrack function
        back_track(start_position,goal_position,final_list,canvas)
    else:
        print("Solution does not exit")

if __name__ == '__main__':
  # start time of the code
    start_time = time.time() 
    # create blank  canvas
    canvas = np.ones((250,600,3),dtype="uint8")
    # draw the obstacle map
    canvas = obstacles_map(canvas)
    # start and goal node coordinates from the user
    start_position,goal_position = coord_input(canvas)
    #cartesian coordinates to image coordinates:
    # start node
    start_position[1] = canvas.shape[0]-1 - start_position[1]
    # goal node
    goal_position[1] = canvas.shape[0]-1 - goal_position[1]
    # Dijkstra Algorithm
    dijkstra_algo(start_position,goal_position,canvas) 
    # end the time taken
    end_time = time.time()
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 
    print("Total time taken to execute the code: ",end_time-start_time) 