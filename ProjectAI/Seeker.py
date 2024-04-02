import sys
import pygame
import heapq
class Seeker:
    def __init__(self, position, vision_radius, bound, map, score=0):
        self.position = position
        self.vision_radius = vision_radius
        self.score = score
        self.bound = bound
        self.map = map

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
        
# def manhattan_distance(a, b):
#     return abs(a[0] - b[0]) + abs(a[1] - b[1])
#     return sqrt

# def neighbors(node):
#     x, y = node
#     return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]  # Assuming 4-connected neighbors

# def a_star_search(start, goal, heuristic, neighbors_fn):
#     open_set = []
#     closed_set = set()
#     heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, []))

#     while open_set:
#         _, g, current, path = heapq.heappop(open_set)

#         if current == goal:
#             return path + [current]
#         if current in closed_set:
#             continue
#         closed_set.add(current)
#         for neighbor in neighbors_fn(current):
#             if neighbor in closed_set:
#                 continue
#             new_g = g + 1
#             heapq.heappush(open_set, (new_g + heuristic(neighbor, goal), new_g, neighbor, path + [current]))

#     return None
def count_inversions(state):
    inv_count = 0
    flattened_board = [val for sublist in state for val in sublist]
    for i in range(len(flattened_board)):
        for j in range(i + 1, len(flattened_board)):
            if flattened_board[i] > flattened_board[j] and flattened_board[i] != 0 and flattened_board[j] != 0:
                inv_count += 1
    return inv_count

def inversion_distance(state):
    n = len(state)
    inv_count = count_inversions(state)
    vertical = inv_count // 3 + inv_count % 3

    horizontal = 0
    for i in range(n):
        for j in range(n):
            if state[i][j] == 0:
                continue
            for k in range(j + 1, n):
                if state[i][k] == 0:
                    continue
                if (state[i][j] - 1) // n == (state[i][k] - 1) // n:
                    if state[i][j] > state[i][k]:
                        horizontal += 1

    return vertical + horizontal

def a_star_inversion_distance(initial_state, goal_state):
    frontier = PriorityQueue()
    initial_state_cost = inversion_distance(initial_state.board)
    initial_state.cost = initial_state_cost
    frontier.put((initial_state_cost, initial_state))
    explored = {}

    max_memory_usage = 0
    while not frontier.empty():
        memory_usage = get_memory_usage()
        max_memory_usage = max(max_memory_usage, memory_usage)
        current_f_score, current_state = frontier.get()

        if current_state.board == goal_state:
            return get_solution(current_state), max_memory_usage

        explored[tuple(map(tuple, current_state.board))] = current_state.cost

        for successor in current_state.successors():
            if tuple(map(tuple, successor.board)) not in explored or explored[tuple(map(tuple, successor.board))] > successor.cost:
                g_score = current_state.cost + 1
                h_score = inversion_distance(successor.board)
                f_score = g_score + h_score
                successor.cost = g_score
                frontier.put((f_score, successor))
                explored[tuple(map(tuple, successor.board))] = successor.cost

    return None, max_memory_usage

# Example usage:
start = (0, 0)
goal = (5, 5)
map = [[0, 0, 0, 0, 0, 0],
       [0, 1, 1, 1, 1, 0],
       [0, 1, 0, 0, 1, 0],
       [0, 1, 0, 1, 1, 0],
       [0, 0, 0, 0, 0, 0]]

seeker = Seeker(start, 1, (len(map), len(map[0])), map)
path = a_star_search(start, goal, manhattan_distance, neighbors)

if path:
    print("Path found:", path)
else:
    print("No path found.")
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
