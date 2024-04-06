from Board import *
from Hider import *
from Seeker import *
import pygame

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

def level3(board):
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
                
        for i in range(all_hiders):
            all_hiders[i].movement_strategy(board) # di chuyển các hiders
            
        board.pos_seeker = seeker.Seeker_move # di chuyển seeker tìm hider(s)
        seeker.point -= 1
        board.steps += 1
        
        for j in range(len(all_hiders)):
            if all_hiders[j].position == seeker.position:
                all_hiders.pop(j)
                seeker.point += 20
        
        # hàm vẽ map
        
    # in ra điểm
    
def run_game():
    print("Select a level:") # chọn level
    print("1. Level 1")
    print("2. Level 2")
    print("3. Level 3")
    print("4. Level 4")
    choice = input("Enter your choice (1-4): ")

    # if choice == 1 or choice == 2:
    #     # Bắt đầu trò chơi với màn chơi 1, 2
    #     pass
    # elif choice == 3:
    #     # Bắt đầu trò chơi với màn chơi 3
    #     pass
    # elif choice == 4:
    #     # Bắt đầu trò chơi với màn chơi 4
    #     pass
    # else:
    #     print("Invalid choice.")
    #     sys.exit()
    
    if choice == '1':
        pygame.init()
        filename = r"c:\Users\HO TIEN PHAT\Documents\GitHub\ProjectAI\ProjectAI\map1_1.txt"
        board = Board(False, filename)

        seeker = Seeker(board.pos_seeker[0], board.pos_seeker[1], (board.n, board.m), board)
        all_hiders = [Hider(pos[0], pos[1]) for pos in board.pos_hiders]
        num_hiders = len(all_hiders)
        finded_hider = 0

        # Calculate the size of the game window based on the size of the game board and the cell size
        screen_width = board.m * (board.CELL_SIZE + MARGIN) + MARGIN * 2
        screen_height = board.n * (board.CELL_SIZE + MARGIN) + MARGIN * 2
        screen_size = (screen_width, screen_height)

        # Create the game window
        screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Map Representation")

        # Draw the initial game map
        screen.fill(WHITE)
        seeker = Seeker(board.pos_seeker[0], board.pos_seeker[1], (board.n, board.m), board)
        board.draw_map(screen, board.CELL_SIZE)
        pygame.display.flip()

        done = False
        clock = pygame.time.Clock()
        while not done and finded_hider < num_hiders:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True    

                hider_announce = []
                # Move seeker using the algorithm
                board.pos_seeker, finded_hider = seeker.Seeker_move(hider_announce)                                     
                board.steps += 1 


                screen.fill(WHITE)
                seeker = Seeker(board.pos_seeker[0], board.pos_seeker[1], (board.n, board.m), board)
                 
                # Draw the game map
                board.draw_map(screen, board.CELL_SIZE)
                board.draw_vision(screen, board.CELL_SIZE)

                #screen.fill(WHITE)
                #seeker = Seeker(board.pos_seeker[0], board.pos_seeker[1], (board.n, board.m), board)
                #board.draw_map(screen, board.CELL_SIZE)

                
                # Draw announcements for hiders
                if board.steps % 5 == 0 and board.steps > 0:
                    hider_announce.clear()
                    for hider_pos in board.pos_hiders:
                        hider = Hider(hider_pos[0], hider_pos[1])
                        announce_pos = hider.announce(board)
                        hider_announce.append(announce_pos)
                        if announce_pos is not None:
                            pygame.draw.rect(screen, PINK,
                                            [(MARGIN + board.CELL_SIZE) * announce_pos[0] + MARGIN,
                                            (MARGIN + board.CELL_SIZE) * announce_pos[1] + MARGIN,
                                            board.CELL_SIZE, board.CELL_SIZE])
                        
                pygame.display.flip()
                clock.tick(1)
        

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    pygame.quit()
                    quit()  # Thoát khỏi chương trình hoàn toàn
        
