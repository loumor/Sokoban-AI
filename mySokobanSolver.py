
'''

    2019 CAB320 Sokoban assignment

The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

You are not allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and triggers to a fail for the test of your code.
 
# by default does not allow push of boxes on taboo cells
SokobanPuzzle.allow_taboo_push = False 

# use elementary actions if self.macro == False
SokobanPuzzle.macro = False 

'''

# you have to use the 'search.py' file provided
# as your code will be tested with this specific file
import search
import math
import sokoban
from search import astar_graph_search, breadth_first_graph_search
from sokoban import find_2D_iterator



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (9510761, 'Morgan', 'Frearson') ] # GUYS PUT YOUR NAME AND NUMBER IN

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def move_coords(item, action):
        '''
        From the current x, y direction of the object move it towards the 
        action. Return the updated x, y coords 
        '''    
        x2 = item[0]
        y2 = item[1]
        if (action is 'Up'):
            y2 -= 1
        elif (action is 'Down'):
            y2 += 1
        elif (action is 'Left'):
            x2 -= 1
        elif (action is 'Right'):
            x2 += 1
        return (x2, y2)

def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo' if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable.  
    When determining the taboo cells, you must ignore all the existing boxes, 
    simply consider the walls and the target cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner inside the warehouse and not a target, 
             then it is a taboo cell.
     Rule 2: all the cells between two corners inside the warehouse along a 
             wall are taboo if none of these cells is a target.
    
    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with 
       an '#' and the taboo cells marked with an 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    '''
    A corner cell will have 1 wall above or below it and 1 wall on the
    left or right of it.
    
    '''
    # Identifiers 
    taboo_cell = 'X'
    wall_cell = '#'
    remove_worker_boxes = ['@', '$']
    target_cells = ['!','*', '.']
    space = ' '
    
    
    def inside_warehouse(warehouse_array, x, y):
        '''
        Check to see if we are inside the warehouse on this iteration
        '''
        if warehouse_array[x][y] == wall_cell:
            return True
        else: 
            return False
        
    def outside_warehouse(warehouse_array, x, y):
        '''
        Check to see if we are outside the warehouse on this iteration
        by seeing if there is empty space untill the end of the column
        '''
        not_outside = 0
        
        for cell in warehouse_array[x][y:]:
            if cell != ' ':
                not_outside += 1
                
        if not_outside == 0:
            return True 
        else: 
            return False 

    
    def check_corner(warehouse_array, x, y):
        '''
        Check to see if the current cell is a corner, this needs to have
        1 wall above or below and 1 wall to the left or right 
        '''
        above_below = 0 
        left_right = 0 
         
        if warehouse_array[x][y+1] == wall_cell: 
            above_below += 1
            
        if warehouse_array[x][y-1] == wall_cell:
            above_below += 1
    
        if warehouse_array[x+1][y] == wall_cell:
            left_right += 1
            
        if warehouse_array[x-1][y] == wall_cell:
            left_right += 1
            
        if left_right >= 1 and above_below >= 1: 
            return True 
        else:
            return False 
    
    def check_wall_LR(warehouse_array, x, y):
        '''
        Check to see if there is a wall above or below the current cell
        this computes the taboo cells for the left to right search 
        '''
        above_below = 0 
        
        if warehouse_array[x+1][y] == wall_cell: 
            above_below += 1
            
        if warehouse_array[x-1][y] == wall_cell:
            above_below += 1
            
        if above_below >= 1: 
            return True 
        else:
            return False 
        
    def check_wall_UD(warehouse_array, x, y):
        '''
        Check to see if there is a wall above or below the current cell
        this computes the taboo cells for the left to right search 
        '''
        left_right = 0 
        
        if warehouse_array[x][y+1] == wall_cell: 
            left_right += 1
            
        if warehouse_array[x][y-1] == wall_cell:
            left_right += 1
            
        if left_right >= 1: 
            return True 
        else:
            return False 
    
    # Convert map into single string 
    warehouse_string = str(warehouse)
    
    # Swap the player and box with space  
    # Keep target cells so we can check for corners later
    for item in remove_worker_boxes :
        warehouse_string = warehouse_string.replace(item, space)
    
    # Turn the warehouse back into an array allowing for corner cell finding 
    warehouse_array = [list(line) for line in warehouse_string.split('\n')]
    
    # Iterate through the array to check for corners that arent targets
    for x in range(len(warehouse_array)): 
        moved_inside = False
        for y in range(len(warehouse_array[0])-1):
            # Check we are inside the warehouse
            if not moved_inside: 
                if inside_warehouse(warehouse_array, x, y):
                    moved_inside = True
            else: 
                # Check to see we haven't left the warehouse
                if outside_warehouse(warehouse_array, x, y):
                    break 
                if warehouse_array[x][y] != wall_cell:
                    if warehouse_array[x][y] not in target_cells:
                        if check_corner(warehouse_array, x, y):
                            warehouse_array[x][y] = taboo_cell
                    
    # Make cells between two corners left to right taboo 
    for x in range(len(warehouse_array)):
        for y in range(len(warehouse_array[0])-1):
            # Find a taboo_cell 
            if warehouse_array[x][y] == taboo_cell:
                # Check it is a corner 
                if check_corner(warehouse_array, x, y): 
                    current_row = x
                    current_col = y
                    # Fill in taboo_cells from left to right 
                    for y2 in range(current_col, len(warehouse_array[0])-1):
                        # Check if we are outside the warehouse
                        if outside_warehouse(warehouse_array,x, y2):
                            break 
                        # Check that it isnt a wall cell
                        if warehouse_array[x][y2] == wall_cell:
                            break
                        safe_lf = True
                        # Check there is no target cells in this row
                        for y3 in range(current_col, len(warehouse_array[0])-1):
                            if warehouse_array[x][y3] in target_cells:
                                safe_lf = False
                        if safe_lf:
                            if check_wall_LR(warehouse_array, x, y2):
                                warehouse_array[x][y2] = taboo_cell
                                
                                                
                    # Fill in taboo_cells from up to down 
                    for x2 in range(current_row, len(warehouse_array)):
                        if outside_warehouse(warehouse_array,x2, y):
                            break 
                        if warehouse_array[x2][y] == wall_cell:
                            break 
                        safe_ud = True
                        for x3 in range(current_row, len(warehouse_array)):
                            if warehouse_array[x3][y] in target_cells:
                                safe_ud = False
                        if safe_ud:
                                if check_wall_UD(warehouse_array, x2, y):
                                    warehouse_array[x2][y] = taboo_cell
                                
                        
    # Turn the warehouse back into a string 
    final_warehouse = '\n'.join([''.join(line) for line in warehouse_array])
    
    # Remove the target cells 
    for item in target_cells :
        final_warehouse = final_warehouse.replace(item, ' ')
    
    return final_warehouse  

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    Each instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.
    
    
    '''
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.

    
    def __init__(self, warehouse, macro, allow_taboo_push):
        self.warehouse = warehouse # Grab the warehouse
        self.goalString = self.getGoalState() # Grab a string of the desired results
        self.walls = tuple(warehouse.walls) # Get the warehouse walls in a tuple      
       
        
        # Set the initial to a list of the boxes 
        initial = list(warehouse.boxes)
        # Place the worker in tuple position 0
        initial.insert(0, warehouse.worker)
        # Set the initial to tuple for use in action and results 
        self.initial = tuple(initial)
        
        
        self.worker = warehouse.worker
        self.boxes = list(warehouse.boxes) # Grab a list of the boxes 
        self.goal = warehouse.targets # Grab the goal state which is the targets
        
        # Get the taboo cells locations using the 2D iterator in sokoban class
        self.taboo = list(sokoban.find_2D_iterator(taboo_cells(warehouse).split(sep='\n'), "X"))
       
        self.targets = tuple(warehouse.targets) # Grab a tuple of the targets 
        self.boxesOriginal = list(warehouse.boxes) # Grab the original box positions
        self.allow_taboo_push = allow_taboo_push  # Set the taboo_push
        self.macro = macro # Set the macro search 

                            
    def actions(self, state): 
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
                
        actions = []
        direction = ["Up", "Down", "Left", "Right"]
        invert_moves = ["Down", "Up", "Right", "Left"]
        
        # Grab the worker and boxes 
        state = list(state)
        worker = state.pop(0)
        boxes = state
        
        # Make a copy of the current warehouse to check against 
        temp_warehouse = self.warehouse.copy(worker, boxes)
        tabooCells = self.taboo
        wallsCells = self.walls
#       accessible = []
        
##################################################################################   
        # FOR UNDERSTANDING PURPOSES #
        # Macro moves are just the position to worker needs to be in 
        # to push a box, and then the direction of pushing that box.
        # Elementry moves is every move made by the worker (going left, going down, blah blahh blahhh)
#################################################################################        
        
        if (self.allow_taboo_push == True): # Allowed to move box on taboo cells
            for box in boxes:
                accessible = []
                # Check each direction the box can be pushed 
                for i in range(len(direction)):
                    # Move the worker to the position one less than
                    # where the box would be 
                    update_worker = move_coords(box, invert_moves[i])
                    # Check if the worker can be moved to that location 
                    # The worker will be next to the box location 
                    if update_worker not in wallsCells:
                        if can_go_there(temp_warehouse, update_worker):
                            accessible.append((update_worker, direction[i]))
            
                # Check the box can be pushed into that location 
                for moves in accessible:
                    coords = moves[0]
                    direct = moves[1]
                    # Update the boxes position after the worker has pushed it 
                    worker_box = move_coords(coords, direct)
                    update_box = move_coords(worker_box, direct)
                    # Check the box doesnt violate any constraints 
                    if update_box not in wallsCells:
                        if update_box not in boxes: 
                            # Append the box that is being acted on 
                            actions.append((worker_box, direct))
                            #print("Action: ", actions)
            return actions
                            

        else: # Not allowed to move box on taboo cells
            for box in boxes:
                accessible = []
                # Check each direction the box can be pushed 
                for i in range(len(direction)):
                    # Move the worker to the position one less than
                    # where the box would be 
                    update_worker = move_coords(box, invert_moves[i])
                    # Check if the worker can be moved to that location 
                    # The worker will be next to the box location 
                    if update_worker not in wallsCells:
                        if can_go_there(temp_warehouse, update_worker):
                            accessible.append((update_worker, direction[i]))
            
                # Check the box can be pushed into that location 
                for moves in accessible:
                    coords = moves[0]
                    direct = moves[1]
                    # Update the boxes position after the worker has pushed it 
                    worker_box = move_coords(coords, direct)
                    update_box = move_coords(worker_box, direct)
                    # Check the box doesnt violate any constraints 
                    if update_box not in tabooCells:
                        if update_box not in wallsCells:
                            if update_box not in boxes: 
                                # Append the box that is being acted on 
                                actions.append((worker_box, direct))
                                #print("Action: ", actions)
            return actions

     
# NOT SURE WHAT THIS DOES COPIED FROM AN EXAMPLE ONLINE ###
#        if len(accessible) < 0:            
#            # Iterate throguh the moves and make sure they satify constraints
#            for move in direction:
#                if (move_coords(worker, move) not in tabooCells):
#                    if (move_coords(worker, move) not in wallsCells):
#                        if (move_coords(worker, move) in boxes):
#                            if move_coords(move_coords(worker, move), move) not in boxes:
#                                actions.append((move_coords(worker, move), move))                            
#                            else:
#                                actions.append((move_coords(worker, move), move))
#                
        
    def result(self, state, action):
        '''
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        '''        
        assert action in self.actions(state)
        newState = list(state) # Copy the state 
        remove = newState.pop(0) # Remove the worker from the copied states
        
        worker = state[0] # Grab the current worker 
#       boxes = state[1:]
        box = action[0] # Grab the current box being acted on 
        newBoxes = [] # For debugging 
        
        if (self.macro == True):
            # Return the macro actions 
            new_worker = box 
            # Move the box 
            newBox = move_coords(box, action[1])
            newBoxes.append(newBox)
            # Update the worker and box 
            newState[newState.index(box)] = newBox
            newState.insert(0, new_worker)
        else: 
            # Return the elementary actions 
            new_worker = move_coords(worker, action[1])
            # If new worker is in the box position it has moved the box
            if new_worker == box:
                newBox = move_coords(box, action[1])
                newBoxes.append(newBox)
                newState[newState.index(box)] = newBox
            else:
                newBoxes.append(box)
                newState[newState.index(box)] = box
            
            newState.insert(0, new_worker)
            
        
        return tuple(newState)
    

######## THIS STUFF COMMENTED OUT WORKS BUT NOT FOR MULTIPLE BOXES ######### 
    
#        assert action in self.actions(state)
##        action = list(action)
#        state = list(state)
#        action = list(action)
#        # Grab the workers (x,y)
#        (worker_x, worker_y) = state.pop(0)
#        actionType = action.pop(1)
#        box_type = action.pop(0)
#        
#        if (self.macro == True):
#            # Return Macro Actions 
#            
#            if actionType == 'Left':
#                # The worker is now where the box previously was
#                update_worker_x = box_type[0]
#                update_worker_y = box_type[1]
#                # Move the box to its new position 
#                (box_x, box_y) = (update_worker_x, update_worker_y)
#                state[state.index((box_x, box_y))] = (box_x - 1, box_y)
#                print(self.warehouse.boxes) # DEBUGGING
#                # Update the original box as its been pushed
#                self.warehouse.boxes.remove((box_x, box_y))
#                self.warehouse.boxes.append((box_x - 1, box_y))
#                print(self.warehouse.boxes) # DEBUGGING                 
#                # Update the worker to the state
#                state.insert(0, (update_worker_x, update_worker_y))
#                # Update the original warehouse worker
#                self.warehouse.worker = (update_worker_x, update_worker_y)
#            
#            if actionType == 'Right':
#                # The worker is now where the box previously was
#                update_worker_x = box_type[0]
#                update_worker_y = box_type[1]
#                # Move the box to its new position 
#                (box_x, box_y) = (update_worker_x, update_worker_y)
#                state[state.index((box_x, box_y))] = (box_x + 1, box_y)
#                print(self.warehouse.boxes) # DEBUGGING
#                # Update the original box as its been pushed
#                self.warehouse.boxes.remove((box_x, box_y))
#                self.warehouse.boxes.append((box_x + 1, box_y))
#                print(self.warehouse.boxes) # DEBUGGING                 
#                # Update the worker to the state
#                state.insert(0, (update_worker_x, update_worker_y))
#                # Update the original warehouse worker
#                self.warehouse.worker = (update_worker_x, update_worker_y)
#            
#            if actionType == 'Up':
#                # The worker is now where the box previously was
#                update_worker_x = box_type[0]
#                update_worker_y = box_type[1]
#                # Move the box to its new position 
#                (box_x, box_y) = (update_worker_x, update_worker_y)
#                state[state.index((box_x, box_y))] = (box_x, box_y - 1)
#                print(self.warehouse.boxes) # DEBUGGING
#                # Update the original box as its been pushed
#                self.warehouse.boxes.remove((box_x, box_y))
#                self.warehouse.boxes.append((box_x, box_y - 1))
#                print(self.warehouse.boxes) # DEBUGGING                 
#                # Update the worker to the state
#                state.insert(0, (update_worker_x, update_worker_y))
#                # Update the original warehouse worker
#                self.warehouse.worker = (update_worker_x, update_worker_y)
#            
#            if actionType == 'Down':
#                # The worker is now where the box previously was
#                update_worker_x = box_type[0]
#                update_worker_y = box_type[1]
#                # Move the box to its new position 
#                (box_x, box_y) = (update_worker_x, update_worker_y)
#                state[state.index((box_x, box_y))] = (box_x, box_y+1)
#                print(self.warehouse.boxes) # DEBUGGING
#                # Update the original box as its been pushed
#                self.warehouse.boxes.remove((box_x, box_y))
#                self.warehouse.boxes.append((box_x, box_y + 1))
#                print(self.warehouse.boxes) # DEBUGGING                 
#                # Update the worker to the state
#                state.insert(0, (update_worker_x, update_worker_y))
#                # Update the original warehouse worker
#                self.warehouse.worker = (update_worker_x, update_worker_y)
#            
#            return tuple(state)
#
#
#        else:
#            # Return Elementry Actions (All the moves for the worker and each box push) 
#                        
#            if actionType == 'Left':
#                update_worker_x = worker_x - 1
#                # See if the worker pushed a box 
#                if (update_worker_x, worker_y) in state:
#                    # Move box to workers new position 
#                    (box_x, box_y) = (update_worker_x, worker_y)
#                    state[state.index((box_x, box_y))] = (box_x - 1, box_y)
#                    print(self.warehouse.boxes) # DEBUGGING
#                    # Update the original box if its been pushed 
#                    self.warehouse.boxes.remove((box_x, box_y))
#                    self.warehouse.boxes.append((box_x - 1, box_y))
#                    print(self.warehouse.boxes) # DEBUGGING  
#                state.insert(0, (update_worker_x, worker_y))
#                # Update the original warehouse worker
#                self.warehouse.worker = (update_worker_x, worker_y)
#        
#            if actionType == 'Right':
#                update_worker_x = worker_x+1
#                # See if the worker pushed a box 
#                if (update_worker_x, worker_y) in state:
#                    # Move box to workers new position 
#                    (box_x, box_y) = (update_worker_x, worker_y)
#                    state[state.index((box_x, box_y))] = (box_x + 1, box_y)
#                    print(self.warehouse.boxes) # DEBUGGING
#                    # Update the original box if its been pushed 
#                    self.warehouse.boxes.remove((box_x, box_y))
#                    self.warehouse.boxes.append((box_x + 1, box_y))
#                    print(self.warehouse.boxes) # DEBUGGING                 
#                state.insert(0, (update_worker_x, worker_y))
#                # Update the original warehouse worker
#                self.warehouse.worker = (update_worker_x, worker_y)
#            
#            if actionType == 'Up':
#                update_worker_y = worker_y-1
#                # See if the worker pushed a box 
#                if (worker_x, update_worker_y) in state:
#                    # Move box to workers new position 
#                    (box_x, box_y) = (worker_x, update_worker_y)
#                    state[state.index((box_x, box_y))] = (box_x, box_y - 1)
#                    print(self.warehouse.boxes) # DEBUGGING
#                    # Update the original box if its been pushed 
#                    self.warehouse.boxes.remove((box_x, box_y))
#                    self.warehouse.boxes.append((box_x, box_y - 1))
#                    print(self.warehouse.boxes) # DEBUGGING  
#                state.insert(0, (worker_x, update_worker_y))
#                # Update the original warehouse worker
#                self.warehouse.worker = (worker_x, update_worker_y)
#                
#            if actionType == 'Down':
#                update_worker_y = worker_y + 1
#                # See if the worker pushed a box 
#                if (worker_x, update_worker_y) in state:
#                    # Move box to workers new position 
#                    (box_x, box_y) = (worker_x, update_worker_y)
#                    state[state.index((box_x, box_y))] = (box_x, box_y + 1)
#                    print(self.warehouse.boxes) # DEBUGGING
#                    # Update the original box if its been pushed 
#                    self.warehouse.boxes.remove((box_x, box_y))
#                    self.warehouse.boxes.append((box_x, box_y + 1))
#                    print(self.warehouse.boxes) # DEBUGGING  
#                state.insert(0, (worker_x, update_worker_y))
#                # Update the original warehouse worker
#                self.warehouse.worker = (worker_x, update_worker_y)
#            
#            return tuple(state)
#        
        
        
    def goal_test(self, state):
        '''
        Check the state of the warehouse
        Return True if the boxes are on the targets
        '''
        result = list(state)
        # Remove the worker from the state s
        worker = result.pop(0)
        if result == self.goal:
            return True 
        else:
            #print(self.goal)
            return False
        
    def getGoalState(self):
        '''
        Get the goal state of the warehouse
        Return a string representation of the goal state
        '''
        goal_state = self.warehouse
        # Convert map into single string 
        goal_state_string = str(goal_state)
        
        # Set goal state
        goal_state_string = goal_state_string.replace("$", " ").replace(".", "*").replace("@", " ")
        
        return goal_state_string
    
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    
 ###################### HEURISTICS FOR MACRO AND ELEMENTRY MOVES ##################   

    def hM(self, node):
        '''
        Get the heuristic for the self.Macro == True 
        This will solve the h(n) for solve_sokoban_macro. 
        Heuristic is the straight line distance from the box
        to a target. 
        Return heuristic distance. 
        ''' 
        
        distance = 0
        heuristic = 0 
        #print(node.state) # Debugging 
        boxes = node.state[1:]
        
        for box in boxes:
            # Find the closest target to the current box 
            closet_target = find_closest(box, self.targets)
            # Add the manhattan distance of the box to the closest target 
            distance += manhattan_distance(box, closet_target)
        
        # Grab the final distance 
        heuristic += distance
        
        return heuristic
            
            
    def hE(self,node):
        '''
        Get the heuristic for the self.Macro == False 
        This will solve the h(n) for solve_elementary. 
        Heuristic is the straight line distance from the box
        to a target. The worker will have to be added to the heuristic 
        to account for when the worker is not at the box/boxes yet. 
        Return heuristic distance. 
        ''' 
        distance = 0
        heuristic = 0 
        #print(node.state) # Debugging 
        worker = node.state[0]
        boxes = node.state[1:]
        
        for box in boxes:
            # Find the closest target to the current box 
            closet_target = find_closest(box, self.targets)
            # Add the manhattan distance of the box to the closest target 
            distance += manhattan_distance(box, closet_target)
        
        # Grab the current actions 
        nodeActions = self.actions(node.state)
        
        for action in nodeActions:
            # Add the distance of the worker to the box for each action 
            distance += manhattan_distance(action[0], worker)
        
        # Grab the final distance 
        heuristic += distance
        
        return heuristic
    

def find_closest(box, targets):
    '''
    Find the closest target to the given box 
    Return the target
    '''
    # Must make the distance number large so the first variable can be assigned 
    target_variables = ((0,0),100000000000000) 
    target_holder = targets
    # Check through all possible targets 
    for i in range(len(target_holder)):
        # How far is the box from the target. Cost is of 1 for each move. 
        # Calculate moves away in straight line distance the box is from the target        
        target_distance = abs(target_holder[i][0] - box[0]) + abs(target_holder[i][1] - box[1])
        
        # Check each target in the list
        # Overwrite the current target if the next target is closer 
        if target_distance <= target_variables[1]:
            target_variables = (target_holder[i], target_distance)
            
    return target_variables[0] # Return the target position 

        
def manhattan_distance(tup, tup2):
    '''
    Return the manhattan distance for the heuristic 
    '''
    return abs(tup[0] - tup2[0])+ abs(tup[1]-tup2[1])

def flip_tuple(a):
    '''
    Flip the provided tuple. This helps for switch row, col and x,y
    Return the flipped tuple
    '''
    return a[1], a[0]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    failure = 'Failure' 
    
    # Obtain the workers location 
    x_worker, y_worker = warehouse.worker 
    
    # Obtain the boxes location 
    x_boxes, y_boxes = warehouse.boxes
    
    # Check if each move in the sequence is vaild 
    for move in action_seq :
        # Check UP action
        if move == 'Up' :
            print('Debugging UP')
            next_x = x_worker
            next_y = y_worker - 1
            if (next_x, next_y) in warehouse.walls:
                return failure # Can't move into a wall
            if (next_x , next_y) in warehouse.boxes:
                # Move the boxes position 
                if (next_x, next_y - 1) not in warehouse.walls: 
                    # Remove the current box 
                    warehouse.boxes.remove((next_x, next_y))
                    # Append (MOVE) the box to new positon 
                    warehouse.boxes.append((next_x, next_y - 1))
                    # Move the worker 
                    y_worker = next_y
                else : 
                    return failure # Box was blocked by walls 
            else: 
                y_worker = next_y # Worker can be moved to new position
        
        # Check Down action
        if move == 'Down' :
            print('Debugging Down')
            next_x = x_worker
            next_y = y_worker + 1
            if (next_x, next_y) in warehouse.walls:
                return failure # Can't move into a wall
            if (next_x , next_y) in warehouse.boxes:
                # Move the boxes position 
                if (next_x, next_y + 1) not in warehouse.walls: 
                    # Remove the current box 
                    warehouse.boxes.remove((next_x, next_y))
                    # Append (MOVE) the box to new positon 
                    warehouse.boxes.append((next_x, next_y + 1))
                    # Move the worker 
                    y_worker = next_y
                else : 
                    return failure # Box was blocked by walls 
            else: 
                y_worker = next_y # Worker can be moved to new position
        
        # Check Left action
        if move == 'Left' :
            print('Debugging Left')
            next_x = x_worker - 1
            next_y = y_worker
            if (next_x, next_y) in warehouse.walls:
                return failure # Can't move into a wall
            if (next_x , next_y) in warehouse.boxes:
                # Move the boxes position 
                if (next_x - 1, next_y) not in warehouse.walls: 
                    # Remove the current box 
                    warehouse.boxes.remove((next_x, next_y))
                    # Append (MOVE) the box to new positon 
                    warehouse.boxes.append((next_x - 1, next_y))
                    # Move the worker 
                    x_worker = next_x
                else : 
                    return failure # Box was blocked by walls 
            else: 
                x_worker = next_x # Worker can be moved to new position
            
        # Check Right action
        if move == 'Right' :
            print('Debugging Right')
            next_x = x_worker + 1
            next_y = y_worker
            if (next_x, next_y) in warehouse.walls:
                return failure # Can't move into a wall
            if (next_x , next_y) in warehouse.boxes:
                # Move the boxes position 
                if (next_x + 1, next_y) not in warehouse.walls: 
                    # Remove the current box 
                    warehouse.boxes.remove((next_x, next_y))
                    # Append (MOVE) the box to new positon 
                    warehouse.boxes.append((next_x + 1, next_y))
                    # Move the worker 
                    x_worker = next_x
                else : 
                    return failure # Box was blocked by walls 
            else: 
                x_worker = next_x # Worker can be moved to new position
        
    # Update the workers position 
    warehouse.worker = x_worker, y_worker 
    
    '''
    Return a string representation of the warehouse. This is from sokoban.py 
    '''
    X,Y = zip(*warehouse.walls) # pythonic version of the above
    x_size, y_size = 1+max(X), 1+max(Y)
    
    vis = [[" "] * x_size for y in range(y_size)]
    for (x,y) in warehouse.walls:
        vis[y][x] = "#"
    for (x,y) in warehouse.targets:
        vis[y][x] = "."
    # if worker is on a target display a "!", otherwise a "@"
    # exploit the fact that Targets has been already processed
    # Note y is worker[1], x is worker[0]
    if vis[warehouse.worker[1]][warehouse.worker[0]] == ".": 
        vis[warehouse.worker[1]][warehouse.worker[0]] = "!"
    else:
        vis[warehouse.worker[1]][warehouse.worker[0]] = "@"
    # if a box is on a target display a "*"
    # exploit the fact that Targets has been already processed
    for (x,y) in warehouse.boxes:
        if vis[y][x] == ".": # if on target
            vis[y][x] = "*"
        else:
            vis[y][x] = "$"
    #print(str(warehouse))       
    return "\n".join(["".join(line) for line in vis])


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using elementary actions 
    the puzzle defined in a file.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    # Set Macro to False so that the SokobanPuzzle sets self.macro     
    macro = False 
    # Set Taboo push to True so that the SokobanPuzzle sets self.allow_taboo_push
    allow_taboo_push = False 
    
    elem_solve = SokobanPuzzle(warehouse, macro, allow_taboo_push) # Set up the warehouse objects
    
#    final_path = breadth_first_graph_search(elem_solve) 
    final_path = astar_graph_search(elem_solve, elem_solve.hE) # Run the graph search
       
    if final_path == None:
        return ['Impossible'] 
    else:
        # Grab the solution path 
        path_list = final_path.solution()
        # Store the elementary moves 
        move_list = list()
        # Grab the elementary movesfrom example M = [ ((3,4),'Left') ]
        for direction in range(len(path_list)):
            move = path_list[direction]
            move_list.append(move[1])
        return move_list # Return elementary moves in form 'Right' 'Left'.....

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - 

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''

    # Turn the warehouse into a string 
    warehouse_cells = str(warehouse).split('\n')    
    
    # Convert the warehouse cells into a list of strings to 
    index = 0
    for strings in warehouse_cells:
        warehouse_cells[index] = list(strings)
        # Increment the index
        index = index +1
    # Grab the x and y size of the array shape 
    x_size = len(warehouse_cells[0])
    y_size = len(warehouse_cells)
    
    # Set worker's x and y coordinates
    worker_x = warehouse.worker[0]
    worker_y = warehouse.worker[1]
    
    # Set destination's x and y coordinates
    dstx = dst[0]
    dsty = dst[1]
    
    # Set boxes' x and y coordinates
    for box in warehouse.boxes:
        box_x = box[0]
        box_y = box[1]
        
        # The box is on the goal the worker will not be able to move to this place
        if box == dst: 
            return False 
        
        # If the box y location is within the worker y and goal y 
        if box_y in range(worker_y, dsty) :
            # If the box is in the same row it will colide 
            if box_x == worker_x:
                return False 
        
        # If the box x location is within the worker x and goal x 
        if box_x in range(worker_x, dstx) :
            # If the box is in the same column it will colide 
            if box_y == worker_y: 
                return False     
        
        # If the goal is out of the x bounds of the warehouse 
        if dstx <= 0 or dstx > x_size:
            return False
       
        # If the goal is out of the y bounds of the warehouse 
        if dsty <= 0 or dsty > y_size:
            return False
    
    return True
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    # Set Macro to True so that the SokobanPuzzle sets self.macro     
    macro = True 
    # Set Taboo push to True so that the SokobanPuzzle sets self.allow_taboo_push
    allow_taboo_push = False 
    
    if warehouse.targets == warehouse.boxes:
        return [] # Return nothing becuase we are in the goal state
    
    macro_solve = SokobanPuzzle(warehouse, macro, allow_taboo_push) # Set up the warehouse objects
    
    #final_path = breadth_first_graph_search(macro_solve)
    final_path = astar_graph_search(macro_solve, macro_solve.hM) # Run the graph search
    
    if final_path == None:
        return ['Impossible'] 
    else:
        # Grab the solution path 
        path_list = final_path.solution()

        # Need to flip the (x,y) position so its in (row, col)
        for direction in range(len(path_list)):
            move = list() # Create an empty 
            move = path_list.pop(direction) # Grab the ((3,1), 'Right')
            move = list(move) # Convert to a list
            flip = move.pop(0) # Grab the tuple of (x, y)
            flipped = flip_tuple(flip) # Flip the tuple
            move.insert(0, flipped) # Insert the tuple back into the list
            move = tuple(move) # Turn the list into a tuple 
            path_list.insert(direction, move) # Insert the tuple into the original path list
        
        return path_list

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
        
