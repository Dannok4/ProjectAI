from Board import Board

class Hider:
    def __init__(self, name, x, y):
        self.name = name
        self.position = (x, y)  # Starting position
        self.steps = 0
        self.announce_position = (-1, 0)
        
    def check_valid_move(self, Board, direction):
        x, y = self.position
        
        # check valid movement for hider
        if 0 <= x < Board.m and 0 <= y < Board.n:
            if Board[y][x] == 0:
                if direction == "left" or direction == "right" or direction == "up" or direction == "down":
                    return True
                else:
                    if direction == "up_left":
                        if Board[y-1][x] != 0 or Board[y][x-1] != 0: return True
                        else: return False
                        
                    if direction == "up_right":
                        if Board[y][x+1] != 0 or Board[y-1][x] != 0: return True
                        else: return False
                        
                    if direction == "down_left":
                        if Board[y][x-1] != 0 or Board[y+1][x] != 0: return True
                        else: return False
                        
                    if direction == "up_left":
                        if Board[y+1][x] != 0 or Board[y][x+1] != 0: return True
                        else: return False 
                        
            else: return False
        else: return False

    def move(self, direction, map_with_objects):
        # Check if movement is valid
        if self.check_valid_move(map_with_objects, direction):
            return 0
        
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

        self.position = (x, y)
        self.steps += 1
        
        if self.steps % 5 == 0:  # make a signal each 5 steps
            self.signal()

    def announce(self, full_map):
        # Make an announcement
        pre_announce_x, pre_announce_y = self.announce_position
        
        if pre_announce_x != -1: # already announce previously
            full_map[pre_announce_y][pre_announce_x] = 0 # delete previous announcement
        
        self.announce_position = self.position
        x, y = self.announce_position
        full_map[y][x] = 5 # signal for announcement
        

           
    def look_around(self, board):
        x, y = self.position
        
        for i in range(max(y-2, 0), min(y+2, board.n)):
            for j in range(max(x-2, 0), min(x+2, board.m)):
                if (board[i][j] == )