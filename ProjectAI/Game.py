from Board import *
from Hider import *
from Seeker import *
import pygame

'''
def level_1_2(board):
# create level
    all_announce_position = []

    seeker = Seeker(board.pos_seeker)
    
    all_hiders = [] # create all hiders
    for i in range(len(board.pos_hiders)):
        hider_i = Hider(board.pos_hiders[i]) # add all hiders
        all_hiders.append(hider_i)
        
    # hàm vẽ map
     
    while len(all_hiders) != 0: # còn hider còn dí
        if board.steps != 0 and board.steps % 5 == 0: # neu la luot thu 5 moi vong -> announce
            for i in range(len(all_hiders)):
                all_announce_position.append(all_hiders[i].announce(board))
            
        seeker.position = seeker.Seeker_move # di chuyển seeker tìm hider(s)
        seeker.point -= 1
        board.steps += 1
        
        for j in range(len(all_hiders)):
            if all_hiders[j].position == seeker.position:
                all_hiders.pop(j)
                seeker.point += 20
        
        # hàm vẽ map
        
    # in ra điểm
'''

# def level3(board):
# # create level
#     all_announce_position = []
    
#     seeker = Seeker(board.pos_seeker)
    
#     all_hiders = [] # create all hiders
#     for i in range(len(board.pos_hiders)):
#         hider_i = Hider(board.pos_hiders[i]) # add all hiders
#         all_hiders.append(hider_i)
     
#     # hàm vẽ map

#     while len(all_hiders) != 0: # còn hider còn dí
#         if board.steps != 0 and board.steps % 5 == 0: # neu la luot thu 5 moi vong -> announce
#             for i in range(len(all_hiders)):
#                 all_announce_position.append(all_hiders[i].announce(board))
                
#         for i in range(all_hiders):
#             all_hiders[i].movement_strategy(board) # di chuyển các hiders
            
#         board.pos_seeker = seeker.Seeker_move # di chuyển seeker tìm hider(s)
#         seeker.point -= 1
#         board.steps += 1
        
#         for j in range(len(all_hiders)):
#             if all_hiders[j].position == seeker.position:
#                 all_hiders.pop(j)
#                 seeker.point += 20
        
#         # hàm vẽ map
        
#     # in ra điểm


def level_1_2(board):
    # Khởi tạo seeker, hiders
    seeker = Seeker(board.pos_seeker[0], board.pos_seeker[1], (board.n, board.m), board)
    all_hiders = [Hider(pos[0], pos[1]) for pos in board.pos_hiders]

    # Khởi tạo các biến
    goal = board.get_priority_direction()
    successors_list = seeker.success(goal[0])
    index_goal = 0
    step_list = 0
    score = 0
    countdown = 300
    hider_announce = []

    # Tính kích thước màn hình
    screen_width = board.m * (board.CELL_SIZE + MARGIN) + MARGIN * 3 + 200
    screen_height = board.n * (board.CELL_SIZE + MARGIN) + MARGIN * 2
    screen_size = (screen_width, screen_height)

    # Tạo cửa sổ trò chơi
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Map Representation")

    # Vẽ map
    screen.fill(WHITE)
    board.draw_map(screen, seeker, all_hiders, countdown, score)
    pygame.display.flip()

    # Tìm kiếm
    done = False
    clock = pygame.time.Clock()
    while not done:
        if len(all_hiders) == 0:
            print("done, score is: ")
            print(score)
            return
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True    

            check_find_hider = False

            # Thuật toán tìm kiếm
            board.pos_seeker, check_find_hider = seeker.Seeker_move(board, hider_announce, successors_list, step_list, all_hiders)                                     
            board.steps += 1 
            score -= 1
            step_list += 1

            # Kiểm tra thay đổi hướng tìm kiếm
            if board.pos_seeker == successors_list[-1]:
                step_list = 0
                index_goal += 1
                successors_list = seeker.success(goal[index_goal])
            
            # Tìm thấy hider
            if check_find_hider:
                # Cập nhật lại hướng tìm kiếm
                step_list = 0   
                successors_list = seeker.success(goal[index_goal])

                # Cập nhật điểm, số lượng hiders
                for hider in all_hiders:
                    if hider.position[0] == seeker.position[1] and hider.position[1] == seeker.position[0]:
                        all_hiders.remove(hider)
                        score += 20

            # Cập nhật map
            board.draw_map(screen, seeker, all_hiders, countdown, score)           
            
            # Tạo annnounce 
            if board.steps % 5 == 0 and board.steps > 0:
                hider_announce = board.draw_announce(screen, all_hiders, hider_announce)
            elif board.steps > 5: # draw current announce
                for announce in hider_announce:
                    if announce not in all_hiders and announce != board.pos_seeker: 
                        pygame.draw.rect(screen, PINK,
                                        [(MARGIN + board.CELL_SIZE) * announce[0] + MARGIN,
                                        (MARGIN + board.CELL_SIZE) * announce[1] + MARGIN,
                                        board.CELL_SIZE, board.CELL_SIZE])                    

            pygame.display.flip()
            clock.tick(5)    

def level_3(board):
    # Khởi tạo seeker, hiders
    seeker = Seeker(board.pos_seeker[0], board.pos_seeker[1], (board.n, board.m), board)
    all_hiders = [Hider(pos[0], pos[1]) for pos in board.pos_hiders]

    # Khởi tạo các biến
    goal = board.get_priority_direction()
    successors_list = seeker.success(goal[0])
    index_goal = 0
    step_list = 0
    score = 0
    countdown = 300
    hider_announce = []

    # Tính kích thước màn hình
    screen_width = board.m * (board.CELL_SIZE + MARGIN) + MARGIN * 3 + 200
    screen_height = board.n * (board.CELL_SIZE + MARGIN) + MARGIN * 2
    screen_size = (screen_width, screen_height)

    # Tạo cửa sổ trò chơi
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Map Representation")

    # Vẽ map
    screen.fill(WHITE)
    board.draw_map(screen, seeker, all_hiders, countdown, score)
    pygame.display.flip()

    # Tìm kiếm
    done = False
    clock = pygame.time.Clock()
    while not done:
        if len(all_hiders) == 0:
            print("done, score is: ")
            print(score)
            return
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True    

            check_find_hider = False

            # Thuật toán tìm kiếm
            board.pos_seeker, check_find_hider = seeker.Seeker_move(board, hider_announce, successors_list, step_list, all_hiders)                                     
            board.steps += 1 
            score -= 1
            step_list += 1

            # Kiểm tra thay đổi hướng tìm kiếm
            if board.pos_seeker == successors_list[-1]:
                step_list = 0
                index_goal += 1
                successors_list = seeker.success(goal[index_goal])
            
            # Tìm thấy hider
            if check_find_hider:
                # Cập nhật lại hướng tìm kiếm
                step_list = 0   
                successors_list = seeker.success(goal[index_goal])

                # Cập nhật điểm, số lượng hiders
                for hider in all_hiders:
                    if hider.position[0] == seeker.position[1] and hider.position[1] == seeker.position[0]:
                        all_hiders.remove(hider)
                        score += 20

            for i in range (len(all_hiders)):
                all_hiders[i].movement_strategy(board) # move hiders

            # Cập nhật map
            board.draw_map(screen, seeker, all_hiders, countdown, score)           

            # Tạo annnounce 
            if board.steps % 5 == 0 and board.steps > 0:
                hider_announce = board.draw_announce(screen, all_hiders, hider_announce)
            elif board.steps > 5: # draw current announce
                for announce in hider_announce:
                    if announce not in all_hiders and announce != board.pos_seeker: 
                        pygame.draw.rect(screen, PINK,
                                        [(MARGIN + board.CELL_SIZE) * announce[0] + MARGIN,
                                        (MARGIN + board.CELL_SIZE) * announce[1] + MARGIN,
                                        board.CELL_SIZE, board.CELL_SIZE])  
                        
            pygame.display.flip()
            clock.tick(5)
    
    
def run_game():
    print("Select a level:") # chọn level
    print("1. Level 1")
    print("2. Level 2")
    print("3. Level 3")
    print("")
    print("** Please notice that you should move mouse non-stop until done to make it run **")
    print("** We are very sorry for this inconvenience **")
    print("")
    choice = input("Enter your choice (1-3): ")

    if choice == '1' or choice == '2':
        pygame.init()
        filename = r"map1_1.txt"
        board = Board(False, filename)

        level_1_2(board)

        while True:    
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    pygame.quit()
                    quit()  # Thoát khỏi chương trình hoàn toàn
                    
    if choice == '3':
        pygame.init()
        filename = r"map1_1.txt"
        board = Board(False, filename)

        level_3(board)

        while True:    
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    pygame.quit()
                    quit()  # Thoát khỏi chương trình hoàn toàn
        
