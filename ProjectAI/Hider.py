﻿import random
from Board import Board

class Hider:
    def __init__(self, x, y):
        self.position = (x, y)  # Starting position
        self.announce_position = (-1, 0)
        
    def check_valid_move(self, board, x, y, direction):       
        # check valid movement for hider
        if 0 <= x < board.m and 0 <= y < board.n:
            if board.map_with_objects[y][x] == 0:
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
            self.position = (x, y) # if valid, save position
            
        return self.position

    def announce(self, board): # Make an announcement
        pre_announce_x, pre_announce_y = self.announce_position
        
        if pre_announce_x != -1: # already announce previously
            board.map_with_objects[pre_announce_y][pre_announce_x] = 0 # delete previous announcement
        
        rand_announce = random.randint(1, 49) # random position
        
        x_hider, y_hider = self.position
        
        dem = 1;
        for i in range(max(y_hider - 3, 0), min(y_hider + 3, board.n - 1)):
            for j in range(max(x_hider - 3, 0), min(x_hider + 3, board.m - 1)):
                if dem == rand_announce: # correct position to announce
                    board.map_with_objects[i][j] = 5 # signal for an announcement
                    return
                else: dem += 1 # not correct, find another
           
    def look_around(self, board): # return position of seeker
        x_hider, y_hider = self.position
        x_seeker, y_seeker = -1, 0
        
        for i in range(max(y_hider - 2, 0), min(y_hider + 2, board.n - 1)):
            for j in range(max(x_hider - 2, 0), min(x_hider + 2, board.m - 1)):
                if board.map_with_objects[i][j] == 3:
                    x_seeker = j
                    y_seeker = i
                    j = board.m, i = board.n # end loop when fought
                    
        if x_seeker != -1: # saw seeker
            x_vector, y_vector = x_seeker - x_hider, y_seeker - y_hider # cal vector to have direction
            
            if (abs(x_vector) == 1 and y_vector == 0) or (x_vector == 0 and abs(y_vector) == 1): # side-by-side in straight
                return (x_seeker, y_seeker) # accepted sight
            
            if abs(x_vector) == 1 and abs(y_vector) == 1: # side-by-side in diagonal
                if (board[y_seeker][x_hider] != 0 and board[y_seeker][x_hider] != 2) and (board[y_hider][x_seeker] != 0 and board[y_hider][x_seeker] != 2): # blocked sight
                    return (-1, 0) # not see
                else: return (x_seeker, y_seeker) # accepted sight
            
            if (abs(x_vector) == 2 and y_vector == 0) or (x_vector == 0 and abs(y_vector) == 2): # in straight
                if (board[y_hider + y_vector/2][x_hider + x_vector/2] != 0 and board[y_hider + y_vector/2][x_hider + x_vector/2] != 2): # blocked sight
                    return (-1, 0) # not see
                else: return (x_seeker, y_seeker) # accepted sight
        
            if abs(x_vector) == 2 and abs(y_vector) == 2: # in diagonal
                if (board[y_hider + y_vector/2][x_hider] != 0 and board[y_hider + y_vector/2][x_hider] != 2) and (board[y_hider][x_hider + x_vector/2] != 0 and board[y_hider][x_hider + x_vector/2] != 2): # blocked sight (near hider)
                    return (-1, 0) # not see
                elif (board[y_seeker - y_vector/2][x_seeker] != 0 and board[y_seeker - y_vector/2][x_seeker] != 2) and (board[y_seeker][x_seeker - x_vector/2] != 0 and board[y_seeker][x_seeker - x_vector/2] != 2): # blocked sight (near seeker)
                    return (-1, 0) # not see
                elif board[y_hider + y_vector/2][x_hider + x_vector/2] != 0 and board[y_hider + y_vector/2][x_hider + x_vector/2] != 2: # blocked sight (in diagonal)
                    return (-1, 0) # not see
                else: return (x_seeker, y_seeker) # accepted sight
             
            # in other positions (8 others)
            if (board[y_hider + y_vector/2][x_hider + x_vector/2] != 0 and board[y_hider + y_vector/2][x_hider + x_vector/2] != 2) and (board[y_seeker - y_vector/2][x_seeker - x_vector/2] != 0 and board[y_seeker - y_vector/2][x_seeker - x_vector/2] != 2): # blocked sight
                return (-1, 0) # not see
            else: return (x_seeker, y_seeker) # accepted sight

        return (-1, 0) # not see