import pygame
from Seeker import *
from Hider import *
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PINK = (255, 182, 193)
MARGIN = 1


class Board:    
    def __init__(self, is_lv4, file_name):
        self.map_with_objects, self.n, self.m, self.obstacles, self.CELL_SIZE, self.pos_seeker, self.pos_hiders = self.create_map(is_lv4, file_name)
        self.steps = 0

    # Đọc file và tạo map bằng ký tự
    def create_map(self, is_lv4, file_name):
        pos_seeker = (-1, 0)
        pos_hiders = []
        map_with_objects = []
        obstacles = []

        with open(file_name, 'r') as file:
            n, m = map(int, file.readline().split())
            map_matrix = [[0 for _ in range(m)] for _ in range(n)]
            #Xác định kích thước mỗi ô vuông trong bảng
            if max(m, n) <= 50:
                CELL_SIZE = 15
            elif max(m, n) <= 100:
                CELL_SIZE = 6
            elif max(m, n) <= 150:
                CELL_SIZE = 4
            else:
                CELL_SIZE = 3

            for i in range(n):
                row = list(map(int, file.readline().split()))
                for j in range(m):
                    if row[j] == 2:
                        map_matrix[i][j] = 2 # Hider
                        pos_hiders.append((j + 1, i + 1)) # lấy vị trí các hiders
                    elif row[j] == 3:
                        map_matrix[i][j] = 3 # Seeker
                        pos_seeker = (i + 1, j + 1) # lấy vị trí seeker
                    elif row[j] == 1:
                        map_matrix[i][j] = 1 # Wall    

            m += 2
            n += 2
            map_with_objects = [[0 for _ in range(m)] for _ in range(n)]
        
            for i in range(n):
                map_with_objects[i][0] = 1
                map_with_objects[i][m - 1] = 1
            for j in range(m):
                map_with_objects[0][j] = 1
                map_with_objects[n - 1][j] = 1

            for i in range(0, n - 2):
                for j in range(0, m - 2):
                    map_with_objects[i + 1][j + 1] = map_matrix[i][j]

            if is_lv4 == True: # if level 4, read obstacle, else, no need to
                obstacles = []
                for _ in range(4):
                    obstacle_line = file.readline().split()
                    if obstacle_line:
                        obstacles.append(list(map(int, obstacle_line)))

                for obstacle in obstacles:
                    if len(obstacle) == 4:
                        top, left, bottom, right = obstacle
                        for i in range(top, bottom + 1):
                            for j in range(left, right + 1):
                                map_with_objects[i + 1][j + 1] = 4 # Obstacle
                    else:
                        print("Invalid obstacle format:", obstacle)
            
            return map_with_objects, n, m, obstacles, CELL_SIZE, pos_seeker, pos_hiders

    def draw_map(self, screen, seeker, all_hiders, countdown, score):
        # Kích thước của màn hình với một cột bổ sung cho đồng hồ và điểm số
        screen_width = self.m * (self.CELL_SIZE + MARGIN) + MARGIN * 3 + 200  # Thêm 200 pixel cho cột đồng hồ và điểm số
        screen_height = self.n * (self.CELL_SIZE + MARGIN) + MARGIN * 2

        # Vẽ background màu trắng
        screen.fill(WHITE)

        # Vẽ bản đồ
        pygame.draw.rect(screen, GRAY, (MARGIN, MARGIN, screen_width - MARGIN * 3 - 200, screen_height - MARGIN * 2))  # Giảm đi 200 pixel cho cột đồng hồ và điểm số

        #Vẽ đường đi và tường
        for row in range(self.n):
            for col in range(self.m):
                if self.map_with_objects[row][col] == 1:
                    pygame.draw.rect(screen, BLACK,
                                [(MARGIN + self.CELL_SIZE) * col + MARGIN,
                                (MARGIN + self.CELL_SIZE) * row + MARGIN,
                                self.CELL_SIZE, self.CELL_SIZE])

        # Vẽ tầm nhìn của seeker
        self.draw_vision(screen, seeker)
    
        #Vẽ Hider                        
        for hider in all_hiders:
            hider_col, hider_row = hider.position
            pygame.draw.rect(screen, GREEN,
                                [(MARGIN + self.CELL_SIZE) * hider_col + MARGIN,
                                (MARGIN + self.CELL_SIZE) * hider_row + MARGIN,
                                self.CELL_SIZE, self.CELL_SIZE])
            
        # Lấy tọa độ của Seeker
        seeker_row, seeker_col = seeker.position

        # Vẽ Seeker
        pygame.draw.rect(screen, RED,
                        [(MARGIN + self.CELL_SIZE) * seeker_col + MARGIN,
                        (MARGIN + self.CELL_SIZE) * seeker_row + MARGIN,
                        self.CELL_SIZE, self.CELL_SIZE])

        # Vẽ cột bên phải chứa đồng hồ đếm ngược và điểm số
        pygame.draw.rect(screen, GRAY, (screen_width - 200, MARGIN, 200, screen_height - MARGIN * 2))
        font = pygame.font.SysFont(None, 30)

        # Vẽ đồng hồ đếm ngược
        #countdown_text = font.render("Time: " + str(countdown), True, BLACK)
        #screen.blit(countdown_text, (screen_width - 190, 120))  # Đặt đồng hồ đếm ngược ở bên phải trên của màn hình

        # Vẽ điểm số
        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (screen_width - 190, 80))  # Đặt điểm số ở bên phải dưới của màn hình

        # Vẽ số lượng hider còn lại
        hider_text = font.render("Hider: " + str(len(all_hiders)), True, BLACK)
        screen.blit(hider_text, (screen_width - 190, 40))  # Đặt điểm số ở bên phải dưới của màn hình
                
    def draw_vision(self, screen, seeker):                
        # Xóa tất cả các ô tầm nhìn cũ (trừ các tường hoặc hider)
        for pos in seeker.valid_vision:
            row, col = pos
            # Kiểm tra xem ô có phải là đường đi không
            if self.map_with_objects[row][col] == 0:
                pygame.draw.rect(screen, GRAY,  # Chọn màu nền của bản đồ
                                [(MARGIN + self.CELL_SIZE) * col + MARGIN,
                                (MARGIN + self.CELL_SIZE) * row + MARGIN,
                                self.CELL_SIZE, self.CELL_SIZE])
                
        seeker.seeker_valid_vision()       
        
        # Vẽ tầm nhìn của seeker
        for (row, col) in seeker.valid_vision:
            pygame.draw.rect(screen, ORANGE,  # Choose color for valid vision (e.g., ORANGE)
                            [(MARGIN + self.CELL_SIZE) * col + MARGIN,
                            (MARGIN + self.CELL_SIZE) * row + MARGIN,
                            self.CELL_SIZE, self.CELL_SIZE])
            
    def draw_announce(self, screen, all_hiders, hider_announce):
        hider_announce.clear()
        for hider in all_hiders:
            announce_pos = hider.announce(self) 
            if announce_pos is not None:
                hider_announce.append(announce_pos)
                pygame.draw.rect(screen, PINK,
                                [(MARGIN + self.CELL_SIZE) * announce_pos[0] + MARGIN,
                                (MARGIN + self.CELL_SIZE) * announce_pos[1] + MARGIN,
                                self.CELL_SIZE, self.CELL_SIZE])
        return hider_announce


    # Hàm chuyển đổi danh sách các phần tử thành danh sách các tọa độ tương ứng
    def convert_to_coordinates(self, sections):
        coordinates = []
        for section in sections:
            if section == 'center':
                coordinates.append(self.get_center_pos())

            elif section == 'top_left':
                coordinates.append((1, 1))
            elif section == 'top_right':
                coordinates.append((1, (self.m - 2)))
            elif section == 'bottom_left':
                coordinates.append(((self.n - 2), 1))
            elif section == 'bottom_right':
                coordinates.append(((self.n - 2), (self.m - 2)))

            elif section == 'top':
                coordinates.append((1, ((self.m - 2) // 2)))
            elif section == 'left-top':
                coordinates.append((1, ((self.m - 2) // 4)))
            elif section == 'right-top':
                coordinates.append((1, (3 * (self.m - 2) // 4)))

            elif section == 'bottom':
                coordinates.append(((self.n - 2), ((self.m - 2) // 2)))
            elif section == 'left-bottom':
                coordinates.append(((self.n - 2), ((self.m - 2) // 4)))
            elif section == 'right-bottom':
                coordinates.append(((self.n - 2), (3 * (self.m - 2) // 4)))

            elif section == 'left':
                coordinates.append(((self.n - 2) // 2, 1))
            elif section == 'top-left':
                coordinates.append(((self.n - 2) // 4, 1))
            elif section == 'bottom-left':
                coordinates.append(((3 * (self.n - 2) // 4), 1))      

            elif section == 'right':
                coordinates.append(((self.n - 2) // 2, self.m - 2))
            elif section == 'top-right':
                coordinates.append(((self.n - 2) // 4, self.m - 2))
            elif section == 'bottom-right':
                coordinates.append(((3 * (self.n - 2) // 4), self.m - 2))
                
        return coordinates

    def get_priority_direction(self):
        # Lấy kích thước của bản đồ
        n_rows, n_cols = self.n, self.m

        # Chia map thành 4 phần
        center_row, center_col = n_rows // 2, n_cols // 2
        top_left = [(r, c) for r in range(center_row) for c in range(center_col)]
        top_right = [(r, c) for r in range(center_row) for c in range(center_col, n_cols)]
        bottom_left = [(r, c) for r in range(center_row, n_rows) for c in range(center_col)]
        bottom_right = [(r, c) for r in range(center_row, n_rows) for c in range(center_col, n_cols)]

        
        # Đếm số lượng tường trong từng phần
        walls_count = {
            'top_left': sum(1 for r, c in top_left if self.map_with_objects[r][c] in [1, 4]),
            'top_right': sum(1 for r, c in top_right if self.map_with_objects[r][c] in [1, 4]),
            'bottom_left': sum(1 for r, c in bottom_left if self.map_with_objects[r][c] in [1, 4]),
            'bottom_right': sum(1 for r, c in bottom_right if self.map_with_objects[r][c] in [1, 4])
        }

        # Sắp xếp các phần theo số lượng tường giảm dần
        sorted_sections = sorted(walls_count.items(), key=lambda x: x[1], reverse=True)

        # Lấy vị trí của Seeker
        seeker_row, seeker_col = self.pos_seeker

        # Kiểm tra vị trí của Seeker thuộc phần nào
        if seeker_row < center_row:
            if seeker_col < center_col:
                seeker_section = 'top_left'
            else:
                seeker_section = 'top_right'
        else:
            if seeker_col < center_col:
                seeker_section = 'bottom_left'
            else:
                seeker_section = 'bottom_right'

        # Tạo danh sách các phần được sắp xếp theo số lượng tường giảm dần, bắt đầu với 'center'
        priority_directions = ['center']

        # Biến đếm vị trí trong danh sách các phần
        position = 1

        # Loại bỏ phần chứa Seeker khỏi danh sách các phần và chèn nó vào cuối mảng
        for section, _ in sorted_sections:
            if section != seeker_section:
                position += 1
                if position % 2 == 1:
                    priority_directions.append('center')
                else:
                    priority_directions.append(section)
                

        # Chèn "center" vào cuối danh sách
        priority_directions.append('center')   
        priority_directions.append(seeker_section)
        priority_directions.append('center')

        # Chèn thêm các vị trí giữa mỗi cạnh
        priority_directions.append('top')
        priority_directions.append('bottom')
        priority_directions.append('left')
        priority_directions.append('right')
        priority_directions.append('center')

        # Chèn thêm các vị trí 1/4 mỗi cạnh
        priority_directions.append('left-top')
        priority_directions.append('left-bottom')
        priority_directions.append('right-top')    
        priority_directions.append('right-bottom')
        priority_directions.append('top-left')
        priority_directions.append('top-right')
        priority_directions.append('bottom-left')    
        priority_directions.append('bottom-right')
        
        # Chuyển đổi danh sách các phần tử thành danh sách các tọa độ tương ứng
        priority_coordinates = self.convert_to_coordinates(priority_directions)

        # Trả về danh sách các phần được sắp xếp theo số lượng tường giảm dần
        return priority_coordinates

    # Xác định vị trí trung tâm map
    def get_center_pos(self):
        cx, cy = self.n // 2, self.m // 2
        dx, dy = 0, 0
        if self.map_with_objects[cx][cy] not in [1, 4]:
            return (cx, cy)
        else:  
            direction = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]      
            while self.map_with_objects[cx + dx][cy + dy] not in [1, 4]:   
                for dx, dy in direction:
                    if self.map_with_objects[cx + dx][cy + dy] not in [1, 4]:
                        return (cx + dx, cy + dy)
                direction *= 2
