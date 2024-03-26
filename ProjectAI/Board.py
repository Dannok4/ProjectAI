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

def create_map(file_name):
    # Read the input file
    with open(file_name, 'r') as file:
        # Read the size of the map
        n, m = map(int, file.readline().split())
        
        # Initialize the map
        map_matrix = [[' ' for _ in range(m)] for _ in range(n)]

        # Read the map matrix
        for i in range(n):
            row = list(map(int, file.readline().split()))
            for j in range(m):
                if row[j] == 2:
                    map_matrix[i][j] = 'H'  # Hider
                elif row[j] == 3:
                    map_matrix[i][j] = 'S'  # Seeker
                elif row[j] == 1:
                    map_matrix[i][j] = '#'  # Wall
        
        # Read obstacle coordinates
        obstacles = []
        for _ in range(4):
            obstacle_line = file.readline().split()
            if obstacle_line:
                obstacles.append(list(map(int, obstacle_line)))       

        # Create the map
        m += 2
        n += 2
        map_with_objects = [[' ' for _ in range(m)] for _ in range(n)]
        
        # Mark borders as walls
        for i in range(n):
            map_with_objects[i][0] = '#'
            map_with_objects[i][m - 1] = '#'
        for j in range(m):
            map_with_objects[0][j] = '#'
            map_with_objects[n - 1][j] = '#'

        for i in range(0, n - 2):
            for j in range(0, m - 2):
                map_with_objects[i + 1][j + 1] = map_matrix[i][j]

        # Mark obstacles
        for obstacle in obstacles:
            if len(obstacle) == 4:
                top, left, bottom, right = obstacle
                for i in range(top, bottom + 1):
                    for j in range(left, right + 1):
                        map_with_objects[i + 1][j + 1] = 'X'  # Obstacle
            else:
                print("Invalid obstacle format:", obstacle)
        
        return map_with_objects, n, m, obstacles


def draw_map(map_with_objects, obstacles, n, m):
    # Initialize Pygame
    pygame.init()
    seeker_pos = None

    # Tìm vị trí ban đầu của Seeker
    for row in range(0, n):
        for col in range(0, m):
            if map_with_objects[row][col] == 'S':
                seeker_pos = (row, col)
                break
        if seeker_pos:
            break
    
     # Tính toán kích thước màn hình
    screen_width = m * (CELL_SIZE + MARGIN) + MARGIN * 2
    screen_height = n * (CELL_SIZE + MARGIN) + MARGIN * 2

    # Set the width and height of the screen [width, height]
    screen_size = (screen_width, screen_height)
    screen = pygame.display.set_mode(screen_size)
    
    pygame.display.set_caption("Map Representation")
    
    # Loop until the user clicks the close button
    done = False
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    # -------- Main Program Loop -----------
    while not done:
        moved_this_loop = False
        # --- Main event loop
        # Kiểm tra và xử lý sự kiện nhấn phím
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if not moved_this_loop:
                    if event.key == pygame.K_a:
                        map_with_objects, obstacles, seeker_pos = move_seeker(map_with_objects, obstacles, seeker_pos, 'left')
                        moved_this_loop = True
                    elif event.key == pygame.K_d:
                        map_with_objects, obstacles, seeker_pos = move_seeker(map_with_objects, obstacles, seeker_pos, 'right')
                        moved_this_loop = True
                    elif event.key == pygame.K_w:
                        map_with_objects, obstacles, seeker_pos = move_seeker(map_with_objects, obstacles, seeker_pos, 'up')
                        moved_this_loop = True
                    elif event.key == pygame.K_s:
                        map_with_objects, obstacles, seeker_pos = move_seeker(map_with_objects, obstacles, seeker_pos, 'down')
                        moved_this_loop = True                    
        
        # --- Drawing code should go here
        # Clear the screen
        screen.fill(WHITE)

         # Vẽ khung viền chữ nhật bao quanh không gian trò chơi
        pygame.draw.rect(screen, GRAY, (MARGIN, MARGIN, screen_width - MARGIN * 2, screen_height - MARGIN * 2))
        
        # Draw the mađ
        for row in range(n):
            for col in range(m):
                color = WHITE
                if map_with_objects[row][col] == '#':
                    color = BLACK
                elif map_with_objects[row][col] == 'H':
                    color = GREEN
                elif map_with_objects[row][col] == 'S':
                    color = RED
                elif map_with_objects[row][col] == 'X':
                    color = BLUE
                pygame.draw.rect(screen, color,
                                 [(MARGIN + CELL_SIZE) * col + MARGIN,
                                  (MARGIN + CELL_SIZE) * row + MARGIN,
                                  CELL_SIZE, CELL_SIZE])
        
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        # --- Limit frames per second
        clock.tick(60)
    
    # Close the window and quit.
    pygame.quit()


def move_seeker(map_with_objects, obstacles, seeker_pos, direction):
    # Lấy vị trí hiện tại của Seeker
    row, col = seeker_pos

    # Xác định vị trí mục tiêu dựa trên hướng di chuyển
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
    
    # Kiểm tra xem vị trí mục tiêu có nằm trong giới hạn của bản đồ không
    if 0 < target_row < len(map_with_objects) - 1 and 0 < target_col < len(map_with_objects[0]) - 1:
        # Kiểm tra nếu vị trí mục tiêu không phải là tường ('#') hoặc obstacle ('X')
        if map_with_objects[target_row][target_col] not in ['#', 'X']:
            # Di chuyển Seeker đến vị trí mục tiêu
            map_with_objects[row][col] = ' '
            map_with_objects[target_row][target_col] = 'S'
            seeker_pos = (target_row, target_col)
            # Di chuyển hình chữ nhật chứa 'X' theo hướng di chuyển của seeker
        elif map_with_objects[target_row][target_col] == 'X':   
            map_with_objects, obstacles, success = move_obstacle(map_with_objects, obstacles, direction, target_row, target_col)
            if success:
                map_with_objects[row][col] = ' '
                map_with_objects[target_row][target_col] = 'S'
                seeker_pos = (target_row, target_col)

    return map_with_objects, obstacles, seeker_pos

def move_obstacle(map_with_objects, obstacles, direction, target_row, target_col):
    # Xác định vị trí obstacle
    obstacle_site = None
    for i, obstacle in enumerate(obstacles):
        if len(obstacle) == 4:
            top, left, bottom, right = obstacle
            if (target_col == left + 1 or target_col == right + 1) and (target_row >= top + 1 and target_row <= bottom + 1):
                obstacle_site = i
                break
            if (target_row == top + 1 or target_row == bottom + 1) and (target_col >= left + 1 and target_col <= right + 1):
                obstacle_site = i
                break

    if obstacle_site is not None:
        top, left, bottom, right = obstacles[obstacle_site]
        top += 1
        left += 1
        right += 1
        bottom += 1

    if direction == 'up':
        for i in range(left, right + 1):
            if(top < 1 or map_with_objects[top - 1][i] in ['#', 'X']):
                return map_with_objects, obstacles, False   
        map_with_objects[top - 1][left:right + 1] = ['X'] * (right - left + 1)
        map_with_objects[bottom][left:right + 1] = [' '] * (right - left + 1)
        obstacles[obstacle_site] = (top - 2, left - 1, bottom - 2, right - 1)
    elif direction == 'down':
        for i in range(left, right + 1):
            if(bottom > n - 3 or map_with_objects[bottom + 1][i] in ['#', 'X']):
                return map_with_objects, obstacles, False
        map_with_objects[bottom + 1][left:right + 1] = ['X'] * (right - left + 1)
        map_with_objects[top][left:right + 1] = [' '] * (right - left + 1)
        obstacles[obstacle_site] = (top, left - 1, bottom, right - 1)
    elif direction == 'left':
        for i in range(top, bottom + 1):
            if(left < 1 or map_with_objects[i][left - 1] in ['#', 'X']):
                return map_with_objects, obstacles, False
        for i in range(top, bottom + 1):
            map_with_objects[i][left - 1] = 'X'
            map_with_objects[i][right] = ' '
        obstacles[obstacle_site] = (top - 1, left - 2, bottom - 1, right - 2)
    elif direction == 'right':
        for i in range(top, bottom + 1):
            if(right > m - 3 or map_with_objects[i][right + 1] in ['#', 'X']):
                return map_with_objects, obstacles, False 
        for i in range(top, bottom + 1):
                map_with_objects[i][right + 1] = 'X'
                map_with_objects[i][left] = ' '          
        obstacles[obstacle_site] = (top - 1, left, bottom - 1, right)
    
    return map_with_objects, obstacles, True


# Example usage:
map_with_objects, n, m, obstacles = create_map('map1_1.txt')
draw_map(map_with_objects, obstacles, n, m)
