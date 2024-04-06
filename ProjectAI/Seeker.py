import sys
import pygame
import heapq
import math
class Seeker:
    def __init__(self, x, y, bound, board):
        self.position = (x, y) # Starting position x: hàng, y: cột
        # self.score = score
        # self.seeker_pos = self.find_seeker_pos()
        self.vision_radius = 3
        self.vision=self.setVision()
        self.valid_vision = []
        self.bound = bound
        self.map = board

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

    # Tìm vị trí seeker trong map
    def find_seeker_pos(self):
        for row in range(self.board.n):
            for col in range(self.board.m):
                if self.board.map_with_objects[row][col] == '3':
                    return (row, col)
        return None    
    
    def setVision(self):
        vision = []
        for i in range(-self.vision_radius, self.vision_radius + 1):
            row = []
            for j in range(-self.vision_radius, self.vision_radius + 1):
                new_x = self.position[0] + i
                new_y = self.position[1] + j
                # Không cần kiểm tra game_map nữa vì không sử dụng game_map
                row.append((new_x, new_y))  # Tạo vision dựa trên self.position
            vision.append(row)
        return vision
    
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
            if self.position[1] - i >= 0 and self.map.map_with_objects[self.position[0]][self.position[1] - i] == 0:
                self.valid_vision_left.append((self.position[0], self.position[1] - i))
            else:
                return
    
    def check_vision_right(self):
        for i in range (1, self.vision_radius + 1):
            if self.position[1] + i < self.bound[1] and self.map.map_with_objects[self.position[0]][self.position[1] + i] == 0:
                self.valid_vision_right.append((self.position[0], self.position[1] + i))
            else:
                return

    def check_vision_up(self):
        for i in range(1, self.vision_radius + 1):
            if self.position[0] - i >= 0 and self.map.map_with_objects[self.position[0] - i][self.position[1]] == 0:
                self.valid_vision_up.append((self.position[0] - i, self.position[1]))
            else:
                return
    
    def check_vision_down(self):
        for i in range (1, self.vision_radius + 1):
            if self.position[0] + i < self.bound[0] and self.map.map_with_objects[self.position[0] + i][self.position[1]] == 0:
                self.valid_vision_down.append((self.position[0] + i, self.position[1]))
            else:
                return
    
    def check_vision_up_left(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] - row >= 0 and self.position[1] - col >= 0 and self.check_invalid_vision_up_left(self.position[0] - row, self.position[1] - col) and self.map.map_with_objects[self.position[0] - row][self.position[1] - col] == 0:
                    self.valid_vision_up_left.append((self.position[0] - row, self.position[1] - col))
                elif self.position[0] - row >= 0 and self.position[1] - col >= 0:
                    self.invalid_vision_up_left.append((self.position[0] - row, self.position[1] - col))

    def check_vision_up_right(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] - row >= 0 and self.position[1] + col < self.bound[1] and self.check_invalid_vision_up_right(self.position[0] - row, self.position[1] + col) and self.map.map_with_objects[self.position[0] - row][self.position[1] + col] == 0:
                    self.valid_vision_up_right.append((self.position[0] - row, self.position[1] + col))
                elif self.position[0] - row >= 0 and self.position[1] + col < self.bound[1]:
                    self.invalid_vision_up_right.append((self.position[0] - row, self.position[1] + col))

    def check_vision_down_left(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] + row < self.bound[0] and self.position[1] - col >= 0 and self.check_invalid_vision_down_left(self.position[0] + row, self.position[1] - col) and self.map.map_with_objects[self.position[0] + row][self.position[1] - col] == 0:
                    self.valid_vision_down_left.append((self.position[0] + row, self.position[1] - col))
                elif self.position[0] + row < self.bound[0] and self.position[1] - col >= 0:
                    self.invalid_vision_down_left.append((self.position[0] + row, self.position[1] - col))

    def check_vision_down_right(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1] and self.check_invalid_vision_down_right(self.position[0] + row, self.position[1] + col) and self.map.map_with_objects[self.position[0] + row][self.position[1] + col] == 0:
                    self.valid_vision_down_right.append((self.position[0] + row, self.position[1] + col))
                elif self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1]:
                    self.invalid_vision_down_right.append((self.position[0] + row, self.position[1] + col))


    def seeker_valid_vision(self):
        self.vision
        self.check_vision_left()
        self.check_vision_right()
        self.check_vision_up()
        self.check_vision_down()
        self.check_vision_up_left()
        self.check_vision_up_right()
        self.check_vision_down_left()
        self.check_vision_down_right()
        self.valid_vision = self.valid_vision_left + self.valid_vision_right + self.valid_vision_up + \
                            self.valid_vision_down + self.valid_vision_up_left + self.valid_vision_up_right + \
                            self.valid_vision_down_left + self.valid_vision_down_right

    # di chuyển bằng phím
    def move(self, direction):
         row, col = self.position[0], self.position[1]
         target_row = row
         target_col = col
         if direction == 'up':
             target_row -= 1
         elif direction == 'down':
             target_row += 1
         elif direction == 'left':
             target_col -= 1
         elif direction == 'right':
             target_col += 1
        
         if 0 < target_row < len(self.map.map_with_objects) - 1 and 0 < target_col < len(self.map.map_with_objects[0]) - 1:
             if self.map.map_with_objects[target_row][target_col] not in [1, 4]:
                 self.map.map_with_objects[row][col] = 0
                 self.map.map_with_objects[target_row][target_col] = 3
                 self.seeker_pos = (target_row, target_col)
             elif self.map.map_with_objects[target_row][target_col] == 4:   
                 success = self.move_obstacle(direction, target_row, target_col)
                 if success:
                     self.map.map_with_objects[row][col] = 0
                     self.map.map_with_objects[target_row][target_col] = 3
                     self.seeker_pos = (target_row, target_col)
    
    # # Kiểm tra xem vị trí của hider có nằm trong tầm nhìn của seeker hay không
    # def seeker_can_see_hider(self):
    #     hider_position = None

    #     # Tìm vị trí của hider trong tầm nhìn của seeker
    #     for i in range(len(self.vision)):
    #         for j in range(len(self.vision[0])):
    #             if self.vision[i][j] == 2:
    #                 hider_position = (i, j)
    #                 break
    #     # Nếu không tìm thấy vị trí của hider, không thể nhìn thấy
    #     if hider_position is None:
    #         return False
    #     # Kiểm tra xem vị trí của hider có nằm trong tầm nhìn của seeker hay không
    #     row, col = hider_position
    #     # Kiểm tra tầm nhìn theo các hướng
    #     if (row, col) in self.valid_vision_left:
    #         return True
    #     if (row, col) in self.valid_vision_right:
    #         return True
    #     if (row, col) in self.valid_vision_up:
    #         return True
    #     if (row, col) in self.valid_vision_down:
    #         return True
    #     if (row, col) in self.valid_vision_up_left:
    #         return True
    #     if (row, col) in self.valid_vision_up_right:
    #         return True
    #     if (row, col) in self.valid_vision_down_left:
    #         return True
    #     if (row, col) in self.valid_vision_down_right:
    #         return True
    #     return False
    
    def seeker_can_see_hider(self):
    # Cập nhật tầm nhìn hợp lệ của Seeker trước khi kiểm tra
        self.seeker_valid_vision()

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

        # Kiểm tra xem vị trí của hider có trong tầm nhìn hợp lệ của seeker không
        return hider_position in set(self.valid_vision_left +
                                     self.valid_vision_right +
                                     self.valid_vision_up +
                                     self.valid_vision_down +
                                     self.valid_vision_up_left +
                                     self.valid_vision_up_right +
                                     self.valid_vision_down_left +
                                     self.valid_vision_down_right)
    

    # def check_announce_in_listening_radius(seeker_position, hider_announce, listening_radius):
    #     x_seeker, y_seeker = seeker_position
    #     x_announce, y_announce = hider_announce

    #     # Tính khoảng cách Manhattan giữa seeker và tín hiệu thông báo từ hider
    #     distance = abs(x_seeker - x_announce) + abs(y_seeker - y_announce)

    #     # Nếu khoảng cách nhỏ hơn hoặc bằng bán kính lắng nghe, trả về True và vị trí của thông báo
    #     if distance <= listening_radius:
    #         return True, hider_announce
    #     else:
    #         return False, None 

    def check_announce_in_listening_radius(seeker_position, hider_announce, radius_Vision):
        x_seeker, y_seeker = seeker_position
        x_announce, y_announce = hider_announce

        # Tính khoảng cách Manhattan giữa seeker và tín hiệu thông báo từ hider
        distance = abs(x_seeker - x_announce) + abs(y_seeker - y_announce)

        # Nếu khoảng cách nhỏ hơn hoặc bằng bán kính lắng nghe (radius_Vision), trả về True và vị trí của thông báo
        if distance <= radius_Vision:
            return True, hider_announce
        else:
            return False, None
        
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


    def successors(node, board_instance, map):
        x, y = node
        cx, cy = board_instance.n, board_instance.m  # Lấy giá trị cx, cy từ thể hiện của lớp Board
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
    

    def Seeker_move(self, board_instance, hider_position, announce_position):
    # Kiểm tra xem Hider có trong tầm nhìn của Seeker hay không
        if self.seeker_can_see_hider():
            # Nếu Hider nằm trong tầm nhìn của Seeker:
            path = self.a_star_search_with_path_update(self.position, hider_position, self.manhattan_distance, self.neighbors)
            if path:
                next_position = path[1]  # Vị trí tiếp theo trong đường đi đến hider
                self.position = next_position
        else:
            # Nếu Hider không có trong tầm nhìn, kiểm tra xem có thông báo từ Hider không
            announce_exists, announcePosition = self.check_announce_in_listening_radius(self.position,  announce_position, listening_radius=3)
            if announce_exists:
                # Nếu có thông báo từ Hider và nằm trong bán kính lắng nghe, di chuyển theo thông báo
                path = self.a_star_search_with_path_update(self.position, announcePosition, self.manhattan_distance, self.neighbors)
                if path:
                    next_position = path[1]  # Vị trí tiếp theo trong đường đi đến vị trí thông báo
                    self.position = next_position
            else:
                # Nếu không có thông báo từ Hider, di chuyển theo các hướng có thể
                successors_list = self.successors(self.position, board_instance, board_instance.map_with_objects)
                if successors_list:
                    next_position = successors_list[0] # Chọn bước di chuyển đầu tiên
                    self.position = next_position
        return self.position


