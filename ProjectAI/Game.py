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
    choice = int(input("Enter your choice (1-4): "))

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
    
    if choice == 1 or choice == 2 or choice == 3 or choice == 4:
        pygame.init()
        filename = "map1_1.txt"
        board = Board(False, filename)
    
        # Calculate the size of the game window based on the size of the game board and the cell size
        screen_width = board.m * (board.CELL_SIZE + MARGIN) + MARGIN * 2
        screen_height = board.n * (board.CELL_SIZE + MARGIN) + MARGIN * 2
        screen_size = (screen_width, screen_height)

        # Create the game window
        screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Map Representation")


        done = False
        clock = pygame.time.Clock()
        while not done:
            moved_this_loop = False
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                 
            # Draw the game map
            board.draw_map(screen, board.CELL_SIZE)

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
