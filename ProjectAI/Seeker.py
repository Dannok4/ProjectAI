import sys
import pygame
import heapq
import math
class Seeker:
    def __init__(self, position, vision_radius, bound, map):
        self.position = position
        self.vision_radius = vision_radius
       # self.score = score
        self.bound = bound
        self.map = map
        #self.seeker_pos = self.find_seeker_pos()
   def is_valid_position(self, row, col):
        return 0 <= row < self.bound[0] and 0 <= col < self.bound[1] and self.game_map[row][col] == 0
   def processVision(self, vision, seekerRow, seekerColumn):
        width = len(vision)
        length = len(vision[0])

        # Xử lý từng ô riêng lẻ
        for row in range(width):    
            for col in range(length):
                if vision[row][col] == 1:
                    # Ô đang xét lệch theo chiều dọc nhiều so với Seeker
                    if abs(row - seekerRow) > abs(col - seekerColumn): 
                        i = row
                        if row < seekerRow: # Ô ở phía trên Seeker
                            while i >= 0:
                                vision[i][col] = 1
                                i -= 1    
                        
                            # Nếu ô ở ngay trên Seeker
                            if row > 0  and row == seekerRow - 1 and col == seekerColumn:
                                if col > 0: vision[row-1][col-1] = 1
                                if col < length - 1: vision[row-1][col+1] = 1

                        elif row > seekerRow:   # Ô ở dưới Seeker
                            while i < width:
                                vision[i][col] = 1
                                i += 1

                            # Nếu ô ở ngay dưới Seeker
                            if row < width - 1 and row == seekerRow + 1 and col == seekerColumn:
                                if col > 0: vision[row+1][col-1] = 1
                                if col < length - 1: vision[row+1][col+1] = 1


                    # Ô đang xét lệch theo chiều ngang nhiều so với Seeker
                    elif abs(row - seekerRow) < abs(col - seekerColumn):
                        j = col
                        if col < seekerColumn:  # Ô bên trái Seeker
                            while j >= 0:
                                vision[row][j] = 1
                                j -= 1

                            # Nếu ô ngay trái Seeker
                            if col > 0 and col == seekerColumn - 1 and row == seekerRow:
                                if row > 0: vision[row-1][col-1] = 1
                                if row < width - 1: vision[row+1][col-1] = 1

                        elif col > seekerColumn:  # Ô bên phải Seeker
                            while j < length:
                                vision[row][j] = 1
                                j += 1

                            # Nếu ô ngay phải Seeker
                            if col < length - 1 and col == seekerColumn + 1 and row == seekerRow:
                                if row > 0: vision[row-1][col+1] = 1
                                if row < width - 1: vision[row+1][col+1] = 1
                        

                    # Ô đang xét nằm trên đường chéo với Seeker
                    else:
                        i, j = row, col
                        if row < seekerRow and col < seekerColumn:  # Đường chéo góc trên-trái
                            while(i >= 0 and j >= 0):
                                vision[i][j] = 1

                                if i != row and i > 0: vision[i-1][j] = 1
                                if j != col and j > 0: vision[i][j-1] = 1

                                i -= 1
                                j -= 1

                        elif row < seekerRow and col > seekerColumn:  # Đường chéo góc trên-phải
                            while(i >= 0 and j < length):
                                vision[i][j] = 1

                                if i != row and i > 0: vision[i-1][j] = 1
                                if j != col and j < length - 1: vision[i][j+1] = 1

                                i -= 1
                                j += 1

                        elif row > seekerRow and col > seekerColumn:   # Đường chéo góc dưới-phải
                            while(i < width and j < length):
                                vision[i][j] = 1

                                if i != row and i < width - 1: vision[i+1][j] = 1
                                if j != col and j < length - 1: vision[i][j+1] = 1

                                i += 1
                                j += 1

                        elif row > seekerRow and col < seekerColumn:    # Đường chéo góc dưới-trái
                            while(i < width and j >= 0):
                                vision[i][j] = 1

                                if i != row and i < width - 1: vision[i+1][j] = 1
                                if j != col and j > 0: vision[i][j-1] = 1

                                i += 1
                                j -= 1


        # Xử lý các ô bị che bởi 2 ô kề nhau
        for i in range(width//2):
            for row in range(width):
                for col in range(length):
                    if vision[row][col] == 1:
                        if row > 0 and row < seekerRow: # 2 ô đang xét nằm trên Seeker
                            if col <= seekerColumn and col < length-1:  # 2 ô nằm bên trái so với Seeker
                                if vision[row][col+1] == 1: # 2 ô đang xét nằm ngang
                                    vision[row-1][col] = 1

                                if col > 0 and vision[row-1][col] == 1: # 2 ô đang xét nằm dọc
                                    vision[row-1][col-1] = 1

                                if col > 0 and vision[row+1][col] == 1:
                                    vision[row][col-1] = 1

                            if col >= seekerColumn and col < length-1: # 2 ô nằm bên phải Seeker
                                if vision[row][col+1] == 1: # 2 ô nằm ngang
                                    vision[row-1][col+1] = 1

                                if vision[row-1][col] == 1: # 2 ô nằm dọc
                                    vision[row-1][col+1] = 1

                                if vision[row+1][col] == 1:
                                    vision[row][col+1] = 1
                                
                        
                        elif row > seekerRow and row < width - 1:   # 2 ô đang xét nằm dưới Seeker
                            if col <= seekerColumn and col < length-1:
                                if vision[row][col+1] == 1:
                                    vision[row+1][col] = 1

                                if col > 0 and vision[row+1][col] == 1:
                                    vision[row+1][col-1] = 1

                                if col > 0 and vision[row-1][col] == 1:
                                    vision[row][col-1] = 1

                            elif col >= seekerColumn and col < length-1:
                                if vision[row][col+1] == 1:
                                    vision[row+1][col+1] = 1

                                if vision[row+1][col] == 1:
                                    vision[row+1][col+1] = 1

                                if vision[row-1][col] == 1:
                                    vision[row][col+1] = 1
                    
        return vision

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
        
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(node):
    x, y = node
    return [
        (x+1, y), (x-1, y), (x, y+1), (x, y-1),  # Four primary directions
        (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)  # Diagonal directions
    ]

def a_star_search(start, goal, heuristic, neighbors_fn):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, []))

    while open_set:
        _, g, current, path = heapq.heappop(open_set)

        if current == goal:
            return path + [current]
        
        if current in closed_set:
            continue
        
        closed_set.add(current)
        
        for neighbor in neighbors_fn(current):
            if neighbor in closed_set:
                continue
            
            new_g = g + 1
            heapq.heappush(open_set, (new_g + heuristic(neighbor, goal), new_g, neighbor, path + [current]))

    return None



# Example usage:
start = (0, 0)
goal = (5, 5)
map = [[0, 1, 1, 0, 0, 0],
       [0, 1, 1, 1, 1, 0],
       [0, 1, 1, 0, 1, 0],
       [0, 1, 1, 0, 1, 0],
       [0, 1, 1, 0, 0, 0],
       [0, 1, 1, 0, 0, 0]]

seeker = Seeker(start, 1, (len(map), len(map[0])), map)
path = a_star_search(start, goal, manhattan_distance, neighbors)

if path:
    print("Path found:", path)
else:
    print("No path found.")

# def test_setVision():
#     game_map = [[0, 0, 0, 0, 0, 0],
#                 [0, 1, 1, 1, 1, 0],
#                 [0, 1, 0, 0, 1, 0],
#                 [0, 1, 0, 1, 1, 0],
#                 [0, 0, 0, 0, 0, 0]]
    
#     position = (0, 0)
#     vision_radius = 3
#     bound = (len(game_map), len(game_map[0]))
    
#     # Tạo một đối tượng Seeker với đủ các đối số
#     seeker = Seeker(position, vision_radius, bound, game_map)
    
#     # Thực hiện test cho hàm setVision
#     vision = seeker.setVision()
#     print(vision)

# # Gọi hàm test_setVision để kiểm tra
# test_setVision()
# def test_setVision():
#     game_map = [[0, 0, 0, 0, 0, 0],
#                 [0, 1, 1, 1, 1, 0],
#                 [0, 1, 0, 0, 1, 0],
#                 [0, 1, 0, 1, 1, 0],
#                 [0, 0, 0, 0, 0, 0]]
    
#     position = (0, 0)
#     vision_radius = 3
#     bound = (len(game_map), len(game_map[0]))
    
#     # Tạo một đối tượng Seeker với đủ các đối số
#     seeker = Seeker(position, vision_radius, bound, game_map)
    
#     # Thực hiện test cho hàm setVision
#     vision = seeker.setVision()
#     print(vision)

# # Gọi hàm test_setVision để kiểm tra
# test_setVision()
