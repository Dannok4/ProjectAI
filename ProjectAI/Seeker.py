import sys
import pygame
import heapq
import math
class Seeker:
    def __init__(self, x, y):
        self.position = (x, y) # Starting position
        # self.score = score
        self.seeker_pos = self.find_seeker_pos()

    # Tìm vị trí seeker trong map
    def find_seeker_pos(self):
        for row in range(self.board.n):
            for col in range(self.board.m):
                if self.board.map_with_objects[row][col] == '3':
                    return (row, col)
        return None    
    def setVision(self):
        startX = max(0, self.position[0] - self.vision_radius)
        startY = max(0, self.position[1] - self.vision_radius)
        endX = min(self.bound[0] - 1, self.position[0] + self.vision_radius)
        endY = min(self.bound[1] - 1, self.position[1] + self.vision_radius)
        print(f"X({startX}->{endX}); Y({startY}->{endY})")

        if startX < 0: 
            startX = 0
        if endX >= self.bound[0]: 
            endX = self.bound[0] - 1
        if startY < 0: 
            startY = 0 
        if endY >= self.bound[1]: 
            endY = self.bound[1] - 1

        self.vision = []  
        for i in range(startX, endX + 1):
            row = []
            for j in range(startY, endY + 1):
                row.append(self.game_map[i][j])
            self.vision.append(row)

        seekerInVisionX = self.position[0] - startX
        seekerInVisionY = self.position[1] - startY

        if 0 <= seekerInVisionX < len(self.vision) and 0 <= seekerInVisionY < len(self.vision[0]):
            self.vision[seekerInVisionX][seekerInVisionY] = 8

        self.vision = self.processVision(self.vision, seekerInVisionX, seekerInVisionY)
        return self.vision

        self.direction = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1 , 1), (-1, -1)] # go right, left, down, up, down_right, down_left, up_right, up_left 

        self.valid_vision_left = []
        self.valid_vision_right = []
        self.valid_vision_up = []
        self.valid_vision_down = []

        self.valid_vision_up_left = []
        self.invalid_vision_up_left = []

        self.valid_vision_up_right = []
        self.invalid_vision_up_right = []

        self.valid_vision_down_left = []
        self.invalid_vision_down_left = []

        self.valid_vision_down_right = []
        self.invalid_vision_down_right = []

        self.valid_movement = []
    
    def check_diagonal_up_left(self, row, col):
        for i in range(1, self.vision_radius + 1):
            if ( row == self.position[0] - i and col == self.position[1] - i):
                return True
        return False

    def check_diagonal_up_right(self, row, col):
        for i in range(1, self.vision_radius + 1):
            if (row == self.position[0] - i and col == self.position[1] + i):
                return True
        return False

    def check_diagonal_down_left(self, row, col):
        for i in range(1, self.vision_radius + 1):
            if ( row == self.position[0] + i and col == self.position[1] - i):
                return True
        return False
    
    def check_diagonal_down_right(self, row, col):
        for i in range(1, self.vision_radius + 1):
            if ( row == self.position[0] + i and col == self.position[1] + i):
                return True
        return False
    
    
    def check_diagonal_down_of_up_left(self, row, col):
        for _ in range(1, self.vision_radius + 1):
            if (abs(row - col) > abs (self.position[0] - self.position[1])):
                return True
        return False
    
    def check_diagonal_down_of_up_right(self, row, col):
        for _ in range(1, self.vision_radius + 1):
            if (abs(row - col) < abs (self.position[0] - self.position[1])):
                return True
        return False
    
    def check_diagonal_down_of_down_left(self, row, col):
        for _ in range(1, self.vision_radius + 1):
            if (abs(row + col) > abs (self.position[0] + self.position[1])):
                return True
        return False
    
    def check_diagonal_down_of_down_right(self, row, col):
        for _ in range(1, self.vision_radius + 1):
            if (abs(row + col) < abs (self.position[0] + self.position[1])):
                return True
        return False
    
    def check_invalid_vision_up_left(self, row, col):
        if len(self.invalid_vision_up_left) == 0:
            return True

        for tpl in self.invalid_vision_up_left:
            if not self.check_diagonal_up_left(row, col) and self.check_diagonal_down_of_up_left(row, col) and ( col == tpl[1] - 1 and ( row == tpl[0] or row == tpl[0] - 1)):
                return False
            elif not self.check_diagonal_up_left(row, col) and not self.check_diagonal_down_of_up_left(row, col) and ( row == tpl[0] - 1 and ( col == tpl[1] or col == tpl[1] - 1)):
                return False
            elif self.check_diagonal_up_left(tpl[0], tpl[1]) and (row == tpl[0] or col == tpl[1]):
                return False
            elif self.check_diagonal_up_left(tpl[0], tpl[1]) and self.check_diagonal_up_left(row, col):
                return False
        return True
    
    def check_invalid_vision_up_right(self, row, col):
        if len(self.invalid_vision_up_right) == 0:
            return True

        for tpl in self.invalid_vision_up_right:
            if not self.check_diagonal_up_right(row, col) and not self.check_diagonal_down_of_up_right(row, col) and ( col == tpl[1] + 1 and ( row == tpl[0] or row == tpl[0] - 1)):
                return False
            elif not self.check_diagonal_up_right(row, col) and self.check_diagonal_down_of_up_right(row, col) and ( row == tpl[0] - 1 and ( col == tpl[1] or col == tpl[1] + 1)):
                return False
            elif self.check_diagonal_up_right(tpl[0], tpl[1]) and (row == tpl[0] or col == tpl[1]):
                return False
            elif self.check_diagonal_up_right(tpl[0], tpl[1]) and self.check_diagonal_up_right(row, col):
                return False
        return True
    
    def check_invalid_vision_down_left(self, row, col):
        if len(self.invalid_vision_down_left) == 0:
            return True

        for tpl in self.invalid_vision_down_left:
            if not self.check_diagonal_down_left(row, col) and not self.check_diagonal_down_of_down_left(row, col) and ( col == tpl[1] - 1 and ( row == tpl[0] or row == tpl[0] + 1)):
                return False
            elif not self.check_diagonal_down_left(row, col) and self.check_diagonal_down_of_down_left(row, col) and ( row == tpl[0] + 1 and ( col == tpl[1] or col == tpl[1] - 1)):
                return False
            elif self.check_diagonal_down_left(tpl[0], tpl[1]) and (row == tpl[0] or col == tpl[1]):
                return False
            elif self.check_diagonal_down_left(tpl[0], tpl[1]) and self.check_diagonal_down_left(row, col):
                return False
        return True
    
    def check_invalid_vision_down_right(self, row, col):
        if len(self.invalid_vision_down_right) == 0:
            return True

        for tpl in self.invalid_vision_down_right:
            if not self.check_diagonal_down_right(row, col) and self.check_diagonal_down_of_down_right(row, col) and ( col == tpl[1] + 1 and ( row == tpl[0] or row == tpl[0] + 1)):
                return False
            elif not self.check_diagonal_down_right(row, col) and not self.check_diagonal_down_of_down_right(row, col) and ( row == tpl[0] + 1 and ( col == tpl[1] or col == tpl[1] + 1)):
                return False
            elif self.check_diagonal_down_right(tpl[0], tpl[1]) and (row == tpl[0] or col == tpl[1]):
                return False
            elif self.check_diagonal_down_right(tpl[0], tpl[1]) and self.check_diagonal_down_right(row, col):
                return False
        return True

    def check_vision_left(self):
        for i in range(1, self.vision_radius + 1):
            if self.position[1] - i >= 0 and self.map[self.position[0]][self.position[1] - i] == 0:
                self.valid_vision_left.append((self.position[0], self.position[1] - i))
            else:
                return
    
    def check_vision_right(self):
        for i in range (1, self.vision_radius + 1):
            if self.position[1] + i < self.bound[1] and self.map[self.position[0]][self.position[1] + i] == 0:
                self.valid_vision_right.append((self.position[0], self.position[1] + i))
            else:
                return

    def check_vision_up(self):
        for i in range(1, self.vision_radius + 1):
            if self.position[0] - i >= 0 and self.map[self.position[0] - i][self.position[1]] == 0:
                self.valid_vision_up.append((self.position[0] - i, self.position[1]))
            else:
                return
    
    def check_vision_down(self):
        for i in range (1, self.vision_radius + 1):
            if self.position[0] + i < self.bound[0] and self.map[self.position[0] + i][self.position[1]] == 0:
                self.valid_vision_down.append((self.position[0] + i, self.position[1]))
            else:
                return
    
    def check_vision_up_left(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] - row >= 0 and self.position[1] - col >= 0 and self.check_invalid_vision_up_left(self.position[0] - row, self.position[1] - col) and self.map[self.position[0] - row][self.position[1] - col] == 0:
                    self.valid_vision_up_left.append((self.position[0] - row, self.position[1] - col))
                elif self.position[0] - row >= 0 and self.position[1] - col >= 0:
                    self.invalid_vision_up_left.append((self.position[0] - row, self.position[1] - col))

    def check_vision_up_right(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] - row >= 0 and self.position[1] + col < self.bound[1] and self.check_invalid_vision_up_right(self.position[0] - row, self.position[1] + col) and self.map[self.position[0] - row][self.position[1] + col] == 0:
                    self.valid_vision_up_right.append((self.position[0] - row, self.position[1] + col))
                elif self.position[0] - row >= 0 and self.position[1] + col < self.bound[1]:
                    self.invalid_vision_up_right.append((self.position[0] - row, self.position[1] + col))

    def check_vision_down_left(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] + row < self.bound[0] and self.position[1] - col >= 0 and self.check_invalid_vision_down_left(self.position[0] + row, self.position[1] - col) and self.map[self.position[0] + row][self.position[1] - col] == 0:
                    self.valid_vision_down_left.append((self.position[0] + row, self.position[1] - col))
                elif self.position[0] + row < self.bound[0] and self.position[1] - col >= 0:
                    self.invalid_vision_down_left.append((self.position[0] + row, self.position[1] - col))

    def check_vision_down_right(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1] and self.check_invalid_vision_down_right(self.position[0] + row, self.position[1] + col) and self.map[self.position[0] + row][self.position[1] + col] == 0:
                    self.valid_vision_down_right.append((self.position[0] + row, self.position[1] + col))
                elif self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1]:
                    self.invalid_vision_down_right.append((self.position[0] + row, self.position[1] + col))

    def seeker_valid_vision(self):
        self.check_vision_left()
        self.check_vision_right()
        self.check_vision_up()
        self.check_vision_down()
        self.check_vision_up_left()
        self.check_vision_up_right()
        self.check_vision_down_left()
        self.check_vision_down_right()

    def seeker_go_right(self):
        self.position = tuple(map(sum, zip(self.position, self.direction[0])))
    
    def seeker_go_left(self):
        self.position = tuple(map(sum, zip(self.position, self.direction[1])))

    def seeker_go_down(self):
        self.position = tuple(map(sum, zip(self.position, self.direction[2])))

    def seeker_go_up(self):
        self.position = tuple(map(sum, zip(self.position, self.direction[3])))
    
    def seeker_go_down_right(self):
        self.position = tuple(map(sum, zip(self.position, self.direction[4])))

    def seeker_go_down_left(self):
        self.position = tuple(map(sum, zip(self.position, self.direction[5])))

    def seeker_go_up_right(self):
        self.position = tuple(map(sum, zip(self.position, self.direction[6])))

    def seeker_go_up_left(self):
        self.position = tuple(map(sum, zip(self.position, self.direction[7])))

     #def seeker_can_see_hider(self, hider_position):
    # Kiểm tra xem vị trí của hider có nằm trong tầm nhìn của seeker hay không
    def seeker_can_see_hider(self):
        hider_position = None

        # Tìm vị trí của hider trong tầm nhìn của seeker
        for i in range(len(self.vision)):
            for j in range(len(self.vision[0])):
                if self.vision[i][j] == 2:
                    hider_position = (i, j)
                    break
        # Nếu không tìm thấy vị trí của hider, không thể nhìn thấy
        if hider_position is None:
            return False
        # Kiểm tra xem vị trí của hider có nằm trong tầm nhìn của seeker hay không
        row, col = hider_position
        # Kiểm tra tầm nhìn theo các hướng
        if (row, col) in self.valid_vision_left:
            return True
        if (row, col) in self.valid_vision_right:
            return True
        if (row, col) in self.valid_vision_up:
            return True
        if (row, col) in self.valid_vision_down:
            return True
        if (row, col) in self.valid_vision_up_left:
            return True
        if (row, col) in self.valid_vision_up_right:
            return True
        if (row, col) in self.valid_vision_down_left:
            return True
        if (row, col) in self.valid_vision_down_right:
            return True
        return False
    def manhattan_distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(node):
        x, y = node
        return [
            (x+1, y), (x-1, y), (x, y+1), (x, y-1),  # Four primary directions
            (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)  # Diagonal directions
        ]

    def a_star_search_with_path_update(start, goal, heuristic, neighbors_fn):
        open_set = []
        heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, []))
    
        while open_set:
            _, g, current, path = heapq.heappop(open_set)
        
            if current == goal:
                return path + [current]
        
            successors = neighbors_fn(current)
            for neighbor in successors:
                new_g = g + 1
                new_path = path + [current]
            
                # Thực hiện tìm kiếm lại nếu có successors mới
                if neighbor not in new_path:
                    heapq.heappush(open_set, (new_g + heuristic(neighbor, goal), new_g, neighbor, new_path))

        return None
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

    def successors(node, center, map):
    x, y = node
    cx, cy = center
    successors_list = []

    # Di chuyển đến trung tâm
    if x != cx: 
        x_direction = (cx - x) // abs(cx - x)
        successors_list.append((x + x_direction, y))
    if y != cy:
        y_direction = (cy - y) // abs(cy - y)
        successors_list.append((x, y + y_direction))
    
    # Di chuyển theo 8 hướng
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(map) and 0 <= new_y < len(map[0]) and map[new_x][new_y] != '#':
                successors_list.append((new_x, new_y))

    return successors_list
