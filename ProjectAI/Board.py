import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define cell size and margin
CELL_SIZE = 30
MARGIN = 2

class Board:
    def __init__(self, file_name):
        self.map_with_objects, self.n, self.m, self.obstacles = self.create_map(file_name)
        self.seeker_pos = None

    # Đọc file và tạo map bằng ký tự
    def create_map(self, file_name):
        with open(file_name, 'r') as file:
            n, m = map(int, file.readline().split())
            map_matrix = [[' ' for _ in range(m)] for _ in range(n)]

            for i in range(n):
                row = list(map(int, file.readline().split()))
                for j in range(m):
                    if row[j] == 2:
                        map_matrix[i][j] = 'H' # Hider
                    elif row[j] == 3:
                        map_matrix[i][j] = 'S' # Seeker
                    elif row[j] == 1:
                        map_matrix[i][j] = '#' # Wall
        
            obstacles = []
            for _ in range(4):
                obstacle_line = file.readline().split()
                if obstacle_line:
                    obstacles.append(list(map(int, obstacle_line)))       

            m += 2
            n += 2
            map_with_objects = [[' ' for _ in range(m)] for _ in range(n)]
            
            for i in range(n):
                map_with_objects[i][0] = '#'
                map_with_objects[i][m - 1] = '#'
            for j in range(m):
                map_with_objects[0][j] = '#'
                map_with_objects[n - 1][j] = '#'

            for i in range(0, n - 2):
                for j in range(0, m - 2):
                    map_with_objects[i + 1][j + 1] = map_matrix[i][j]

            for obstacle in obstacles:
                if len(obstacle) == 4:
                    top, left, bottom, right = obstacle
                    for i in range(top, bottom + 1):
                        for j in range(left, right + 1):
                            map_with_objects[i + 1][j + 1] = 'X' # Obstacle
                else:
                    print("Invalid obstacle format:", obstacle)
            
            return map_with_objects, n, m, obstacles

    # Vẽ map bằng đồ họa
    def draw_map(self, screen):
        screen_width = self.m * (CELL_SIZE + MARGIN) + MARGIN * 2
        screen_height = self.n * (CELL_SIZE + MARGIN) + MARGIN * 2

        screen.fill(WHITE)
        pygame.draw.rect(screen, GRAY, (MARGIN, MARGIN, screen_width - MARGIN * 2, screen_height - MARGIN * 2))
        
        for row in range(self.n):
            for col in range(self.m):
                color = WHITE
                if self.map_with_objects[row][col] == '#':
                    color = BLACK
                elif self.map_with_objects[row][col] == 'H':
                    color = GREEN
                elif self.map_with_objects[row][col] == 'S':
                    color = RED
                elif self.map_with_objects[row][col] == 'X':
                    color = BLUE
                pygame.draw.rect(screen, color,
                                [(MARGIN + CELL_SIZE) * col + MARGIN,
                                (MARGIN + CELL_SIZE) * row + MARGIN,
                                CELL_SIZE, CELL_SIZE])

class Seeker:
    def __init__(self, board):
        self.board = board
        self.seeker_pos = self.find_seeker_pos()

    # Tìm vị trí seeker trong map
    def find_seeker_pos(self):
        for row in range(self.board.n):
            for col in range(self.board.m):
                if self.board.map_with_objects[row][col] == 'S':
                    return (row, col)
        return None

    # Di chuyển Seeker bằng phím
    def move(self, direction):
        row, col = self.seeker_pos
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
        
        if 0 < target_row < len(self.board.map_with_objects) - 1 and 0 < target_col < len(self.board.map_with_objects[0]) - 1:
            if self.board.map_with_objects[target_row][target_col] not in ['#', 'X']:
                self.board.map_with_objects[row][col] = ' '
                self.board.map_with_objects[target_row][target_col] = 'S'
                self.seeker_pos = (target_row, target_col)
            elif self.board.map_with_objects[target_row][target_col] == 'X':   
                self.move_obstacle(direction, target_row, target_col)

    # Di chuyển khối vật cản  
    def move_obstacle(self, direction, target_row, target_col):
        obstacle_site = None
        for i, obstacle in enumerate(self.board.obstacles):
            if len(obstacle) == 4:
                top, left, bottom, right = obstacle
                if (target_col == left + 1 or target_col == right + 1) and (target_row >= top + 1 and target_row <= bottom + 1):
                    obstacle_site = i
                    break
                if (target_row == top + 1 or target_row == bottom + 1) and (target_col >= left + 1 and target_col <= right + 1):
                    obstacle_site = i
                    break
        
        if obstacle_site is not None:
            top, left, bottom, right = self.board.obstacles[obstacle_site]
            top += 1
            left += 1
            right += 1
            bottom += 1

        if direction == 'up':
            for i in range(left, right + 1):
                if(top < 1 or self.board.map_with_objects[top - 1][i] in ['#', 'X']):
                    return 
            self.board.map_with_objects[top - 1][left:right + 1] = ['X'] * (right - left + 1)
            self.board.map_with_objects[bottom][left:right + 1] = [' '] * (right - left + 1)
            self.board.obstacles[obstacle_site] = (top - 2, left - 1, bottom - 2, right - 1)
        elif direction == 'down':
            for i in range(left, right + 1):
                if(bottom > self.board.n - 3 or self.board.map_with_objects[bottom + 1][i] in ['#', 'X']):
                    return
            self.board.map_with_objects[bottom + 1][left:right + 1] = ['X'] * (right - left + 1)
            self.board.map_with_objects[top][left:right + 1] = [' '] * (right - left + 1)
            self.board.obstacles[obstacle_site] = (top, left - 1, bottom, right - 1)
        elif direction == 'left':
            for i in range(top, bottom + 1):
                if(left < 1 or self.board.map_with_objects[i][left - 1] in ['#', 'X']):
                    return
            for i in range(top, bottom + 1):
                self.board.map_with_objects[i][left - 1] = 'X'
                self.board.map_with_objects[i][right] = ' '
            self.board.obstacles[obstacle_site] = (top - 1, left - 2, bottom - 1, right - 2)
        elif direction == 'right':
            for i in range(top, bottom + 1):
                if(right > self.board.m - 3 or self.board.map_with_objects[i][right + 1] in ['#', 'X']):
                    return 
            for i in range(top, bottom + 1):
                    self.board.map_with_objects[i][right + 1] = 'X'
                    self.board.map_with_objects[i][left] = ' '          
            self.board.obstacles[obstacle_site] = (top - 1, left, bottom - 1, right)

def main():
    pygame.init()
    # Tạo map
    game_map = Board('map1_1.txt')  
    screen_width = (CELL_SIZE + MARGIN) * game_map.m + MARGIN
    screen_height = (CELL_SIZE + MARGIN) * game_map.n + MARGIN
    screen_size = (screen_width, screen_height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Map Representation")

    seeker = Seeker(game_map)

    done = False
    clock = pygame.time.Clock()

    # Kiểm tra sự kiện nhấn phím
    while not done:
        moved_this_loop = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if not moved_this_loop:
                    if event.key == pygame.K_a:
                        seeker.move('left')
                        moved_this_loop = True
                    elif event.key == pygame.K_d:
                        seeker.move('right')
                        moved_this_loop = True
                    elif event.key == pygame.K_w:
                        seeker.move('up')
                        moved_this_loop = True
                    elif event.key == pygame.K_s:
                        seeker.move('down')
                        moved_this_loop = True                    
        # Cập nhật lại map sau khi di chuyển
        game_map.draw_map(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
