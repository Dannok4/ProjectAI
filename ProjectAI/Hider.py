import random
from Board import *

class Hider:
    def __init__(self, x, y):
        self.position = (x, y) # Starting position
        self.old_position = self.position
        self.announce_position = (-1, 0)
        
    def check_valid_move(self, board, x, y, direction): # return true if valid movement     
        if 0 <= x < board.m and 0 <= y < board.n: # if position is in range of map
            if board.map_with_objects[y][x] == 0: # if next position is empty
                if direction == "left" or direction == "right" or direction == "up" or direction == "down":
                    return True
                else:
                    if direction == "up_left":
                        if (board.map_with_objects[y+1][x] == 1 or board.map_with_objects[y+1][x] == 4) and (board.map_with_objects[y][x+1] == 1 or board.map_with_objects[y][x+1] == 4): return False
                        else: return True
                        
                    if direction == "up_right":
                        if (board.map_with_objects[y+1][x] == 1 or board.map_with_objects[y+1][x] == 4) and (board.map_with_objects[y][x-1] == 1 or board.map_with_objects[y][x-1] == 4): return False
                        else: return True
                        
                    if direction == "down_left":
                        if (board.map_with_objects[y-1][x] == 1 or board.map_with_objects[y-1][x] == 4) and (board.map_with_objects[y][x+1] == 1 or board.map_with_objects[y][x+1] == 4): return False
                        else: return True
                        
                    if direction == "down_right":
                        if (board.map_with_objects[y-1][x] == 1 or board.map_with_objects[y-1][x] == 4) and (board.map_with_objects[y][x-1] == 1 or board.map_with_objects[y][x-1] == 4): return False
                        else: return True 
                        
            else: return False
        else: return False

    def move(self, direction, board): # return next position or current position if move is invalid
        # Move function for hider          
        x, y = self.position
                    
        if direction == "left":
            x -= 1
        if direction == "right":
            x += 1
        if direction == "up":
            y -= 1
        if direction == "down":
            y += 1
        if direction == "up_left":
            x -= 1
            y -= 1
        if direction == "up_right":
            x += 1
            y -= 1
        if direction == "down_left":
            x -= 1
            y += 1
        if direction == "down_right":
            x += 1
            y += 1
            
        # Check if movement is valid
        if self.check_valid_move(board, x, y, direction):
            return (x, y) # if valid, return position   
        else: return self.position # else, return current position (no move)

    def announce(self, board): # return position of announcement     
        rand_announce = random.randint(1, 49) # random position
        x_hider, y_hider = self.position
        
        dem = 1
        for i in range(max(y_hider - 3, 0), min(y_hider + 3, board.n - 1) + 1):
            for j in range(max(x_hider - 3, 0), min(x_hider + 3, board.m - 1) + 1):
                if (i, j) != (y_hider, x_hider) and board.map_with_objects[i][j] != 1: # Avoid hider's position and walls
                    if dem == rand_announce: # correct position to announce
                        self.announce_position = j, i # save announce position
                        return (j, i)
                    else: 
                        dem += 1 # not correct, find another
           
    def look_around(self, board): # return position of seeker
        x_hider, y_hider = self.position
        x_seeker, y_seeker = -1, 0
        
        for i in range(max(y_hider - 2, 0), min(y_hider + 2, board.n - 1) + 1):
            for j in range(max(x_hider - 2, 0), min(x_hider + 2, board.m - 1) + 1):
                if board.map_with_objects[i][j] == 3:
                    x_seeker = j
                    y_seeker = i
                    # end loop when fought
                    j = board.m + 1
                    i = board.n + 1 
                    
        if x_seeker != -1: # saw seeker
            x_vector, y_vector = x_seeker - x_hider, y_seeker - y_hider # cal vector to have direction
            
            if (abs(x_vector) == 1 and y_vector == 0) or (x_vector == 0 and abs(y_vector) == 1): # side-by-side in straight
                return (x_seeker, y_seeker) # accepted sight
            
            if abs(x_vector) == 1 and abs(y_vector) == 1: # side-by-side in diagonal
                if (board.map_with_objects[y_seeker][x_hider] != 0 and board.map_with_objects[y_seeker][x_hider] != 2) and (board.map_with_objects[y_hider][x_seeker] != 0 and board.map_with_objects[y_hider][x_seeker] != 2): # blocked sight
                    return (-1, 0) # not see
                else: return (x_seeker, y_seeker) # accepted sight
            
            if (abs(x_vector) == 2 and y_vector == 0) or (x_vector == 0 and abs(y_vector) == 2): # in straight
                if (board.map_with_objects[y_hider + y_vector/2][x_hider + x_vector/2] != 0 and board.map_with_objects[y_hider + y_vector/2][x_hider + x_vector/2] != 2): # blocked sight
                    return (-1, 0) # not see
                else: return (x_seeker, y_seeker) # accepted sight
        
            if abs(x_vector) == 2 and abs(y_vector) == 2: # in diagonal
                if (board.map_with_objects[y_hider + y_vector/2][x_hider] != 0 and board.map_with_objects[y_hider + y_vector/2][x_hider] != 2) and (board.map_with_objects[y_hider][x_hider + x_vector/2] != 0 and board.map_with_objects[y_hider][x_hider + x_vector/2] != 2): # blocked sight (near hider)
                    return (-1, 0) # not see
                elif (board.map_with_objects[y_seeker - y_vector/2][x_seeker] != 0 and board.map_with_objects[y_seeker - y_vector/2][x_seeker] != 2) and (board.map_with_objects[y_seeker][x_seeker - x_vector/2] != 0 and board.map_with_objects[y_seeker][x_seeker - x_vector/2] != 2): # blocked sight (near seeker)
                    return (-1, 0) # not see
                elif board.map_with_objects[y_hider + y_vector/2][x_hider + x_vector/2] != 0 and board.map_with_objects[y_hider + y_vector/2][x_hider + x_vector/2] != 2: # blocked sight (in diagonal)
                    return (-1, 0) # not see
                else: return (x_seeker, y_seeker) # accepted sight
             
            # in other positions (8 others)
            if (board.map_with_objects[y_hider + y_vector/2][x_hider + x_vector/2] != 0 and board.map_with_objects[y_hider + y_vector/2][x_hider + x_vector/2] != 2) and (board.map_with_objects[y_seeker - y_vector/2][x_seeker - x_vector/2] != 0 and board.map_with_objects[y_seeker - y_vector/2][x_seeker - x_vector/2] != 2): # blocked sight
                return (-1, 0) # not see
            else: return (x_seeker, y_seeker) # accepted sight

        return (-1, 0) # not see
    
    def movement_strategy(self, board): # function to move, no return
        x_seeker, y_seeker = self.look_around(board) # look around before moving
        x_moved, y_moved = self.position
        all_directions = ["up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right"]
        
        if x_seeker == -1: # not fought seeker
            # move randomly
            selected_directions = []

            while (x_moved, y_moved) == self.position and len(selected_directions) < len(all_directions): # choose a direction which not similar to all previous one
                remaining_directions = [d for d in all_directions if d not in selected_directions]
                direction = random.choice(remaining_directions)
    
                selected_directions.append(direction)
                    
                x_moved, y_moved = self.move(direction, board) # move test, if fail, return current position
                
            self.position = (x_moved, y_moved) # modify position (if cannot move, standing)

        else: # seeker fought
            distance_to_seeker = (self.position[0] - x_seeker) ** 2 + (self.position[1] - y_seeker) ** 2
            valid_position = []
                
            for direction in all_directions: # find all possible way
                (xi, yi) = self.move(direction, board)
                    
                if (xi, yi) != self.position and (xi - x_seeker) ** 2 + (xi - y_seeker) ** 2 >= distance_to_seeker: # if movable and increase or keep distance
                    valid_position.append((xi, yi))
                        
            if len(valid_position) > 0: # if there is any possible position, move based on max distance
                max_distance_position = max(valid_position, key=lambda pos: (pos[0] - x_seeker) ** 2 + (pos[1] - y_seeker) ** 2)
                self.position = max_distance_position
            # else, no move, just standing