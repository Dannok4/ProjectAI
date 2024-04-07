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
            if self.position[1] - i > 0 and self.map.map_with_objects[self.position[0]][self.position[1] - i] != 1:
                self.valid_vision_left.append((self.position[0], self.position[1] - i))
            else:
                return
    
    def check_vision_right(self):
        for i in range (1, self.vision_radius + 1):
            if self.position[1] + i < self.bound[1] - 1 and self.map.map_with_objects[self.position[0]][self.position[1] + i] != 1:
                self.valid_vision_right.append((self.position[0], self.position[1] + i))
            else:
                return

    def check_vision_up(self):
        for i in range(1, self.vision_radius + 1):
            if self.position[0] - i > 0 and self.map.map_with_objects[self.position[0] - i][self.position[1]] != 1:
                self.valid_vision_up.append((self.position[0] - i, self.position[1]))
            else:
                return
    
    def check_vision_down(self):
        for i in range (1, self.vision_radius + 1):
            if self.position[0] + i < self.bound[0] - 1 and self.map.map_with_objects[self.position[0] + i][self.position[1]] != 1:
                self.valid_vision_down.append((self.position[0] + i, self.position[1]))
            else:
                return
    
    def check_vision_up_left(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] - row >= 0 and self.position[1] - col >= 0 and self.check_invalid_vision_up_left(self.position[0] - row, self.position[1] - col) and self.map.map_with_objects[self.position[0] - row][self.position[1] - col] != 1:
                    self.valid_vision_up_left.append((self.position[0] - row, self.position[1] - col))
                elif self.position[0] - row >= 0 and self.position[1] - col >= 0:
                    self.invalid_vision_up_left.append((self.position[0] - row, self.position[1] - col))

    def check_vision_up_right(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] - row >= 0 and self.position[1] + col < self.bound[1] and self.check_invalid_vision_up_right(self.position[0] - row, self.position[1] + col) and self.map.map_with_objects[self.position[0] - row][self.position[1] + col] != 1:
                    self.valid_vision_up_right.append((self.position[0] - row, self.position[1] + col))
                elif self.position[0] - row >= 0 and self.position[1] + col < self.bound[1]:
                    self.invalid_vision_up_right.append((self.position[0] - row, self.position[1] + col))

    def check_vision_down_left(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] + row < self.bound[0] and self.position[1] - col >= 0 and self.check_invalid_vision_down_left(self.position[0] + row, self.position[1] - col) and self.map.map_with_objects[self.position[0] + row][self.position[1] - col] != 1:
                    self.valid_vision_down_left.append((self.position[0] + row, self.position[1] - col))
                elif self.position[0] + row < self.bound[0] and self.position[1] - col >= 0:
                    self.invalid_vision_down_left.append((self.position[0] + row, self.position[1] - col))

    def check_vision_down_right(self):
        for row in range (1, self.vision_radius + 1):
            for col in range (1, self.vision_radius + 1):
                if self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1] and self.check_invalid_vision_down_right(self.position[0] + row, self.position[1] + col) and self.map.map_with_objects[self.position[0] + row][self.position[1] + col] != 1:
                    self.valid_vision_down_right.append((self.position[0] + row, self.position[1] + col))
                elif self.position[0] + row < self.bound[0] and self.position[1] + col < self.bound[1]:
                    self.invalid_vision_down_right.append((self.position[0] + row, self.position[1] + col))

    def seeker_valid_vision(self):   
        self.vision

        self.valid_vision_left.clear()
        self.valid_vision_right.clear()
        self.valid_vision_up.clear()
        self.valid_vision_down.clear()
        self.valid_vision_up_left.clear()
        self.valid_vision_up_right.clear()
        self.valid_vision_down_left.clear()
        self.valid_vision_down_right.clear()
        self.invalid_vision_down_left.clear()
        self.invalid_vision_down_right.clear()
        self.invalid_vision_up_left.clear()
        self.invalid_vision_up_right.clear()

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
    
    def seeker_can_see_hider(self, all_hiders):
    # Cập nhật tầm nhìn hợp lệ của Seeker trước khi kiểm tra
        self.seeker_valid_vision()

        hider_position = None

        # Tìm vị trí của hider trong tầm nhìn của seeker
        for (i, j) in self.valid_vision:
            for hider in all_hiders:
                if hider.position == (j, i):
                    hider_position = (i, j)
                    return hider_position
            
        return None

    def check_announce_in_listening_radius(self, seeker_position, hider_announce, radius_Vision):
        x_seeker, y_seeker = seeker_position
        for announce in hider_announce:
            if announce:
                x_announce, y_announce = announce

            # Tính khoảng cách Manhattan giữa seeker và tín hiệu thông báo từ hider
            distance = abs(x_seeker - x_announce) + abs(y_seeker - y_announce)

            # Nếu khoảng cách nhỏ hơn hoặc bằng bán kính lắng nghe (radius_Vision), trả về True và vị trí của thông báo
            if distance <= radius_Vision:
                return True, announce
                           
        return False, None
        
    def manhattan_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, node):
        x, y = node
        return [
            (x+1, y), (x-1, y), (x, y+1), (x, y-1),  # Four primary directions
            (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)  # Diagonal directions
        ]

    def a_star_search_with_path_update(self, start, goal, heuristic):
        open_set = []
        heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, []))
        closed_set = set()
    
        while open_set:
            _, g, current, path = heapq.heappop(open_set)
        
            if current == goal:
                return path + [current]
            
            if current in closed_set:
                continue

            closed_set.add(current)

            neighbors_fn = self.neighbors
            successors = neighbors_fn(current)
            for neighbor in successors:
                new_g = g + 1
                new_path = path + [current]
            
                 # Kiểm tra xem ô neighbor có nằm trong ranh giới của bản đồ không
                if 0 <= neighbor[0] < len(self.map.map_with_objects) and 0 <= neighbor[1] < len(self.map.map_with_objects[0]):
                    # Kiểm tra xem ô neighbor có là tường không
                    if self.map.map_with_objects[neighbor[0]][neighbor[1]] not in [1, 4]:
                        # Thực hiện tìm kiếm lại nếu có successors mới
                        if neighbor not in new_path:
                            heapq.heappush(open_set, (new_g + heuristic(neighbor, goal), new_g, neighbor, new_path))

        return None    

    def success(self, goal):
        return self.a_star_search_with_path_update(self.position, goal, self.manhattan_distance)

    def Seeker_move(self, announce_position, successors_list, step_list, all_hiders):
    # Kiểm tra xem Hider có trong tầm nhìn của Seeker hay không
        hider_position = self.seeker_can_see_hider(all_hiders)
        find_hider = False
        
        if hider_position:
            # Nếu Hider nằm trong tầm nhìn của Seeker:
            path = self.a_star_search_with_path_update(self.position, hider_position, self.manhattan_distance)
            if path:
                next_position = path[1]  # Vị trí tiếp theo trong đường đi đến hider
                self.position = next_position
                if self.position == hider_position:
                    find_hider = True
        else:
            # Nếu Hider không có trong tầm nhìn, kiểm tra xem có thông báo từ Hider không
            announce_exists, announcePosition = self.check_announce_in_listening_radius(self.position, announce_position, 3)
            if announce_exists:
                # Nếu có thông báo từ Hider và nằm trong bán kính lắng nghe, di chuyển theo thông báo
                path = self.a_star_search_with_path_update(self.position, announcePosition, self.manhattan_distance, self.neighbors)
                if path:
                    next_position = path[1]  # Vị trí tiếp theo trong đường đi đến vị trí thông báo
                    self.position = next_position
            else:
                # Nếu không có thông báo từ Hider, di chuyển theo các hướng có thể
                if successors_list:
                    next_position = successors_list[step_list] # Chọn bước di chuyển đầu tiên
                    self.position = next_position
            
        return self.position, find_hider

