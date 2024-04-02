import pygame
from Board import *

def main():
    pygame.init()
    game_map = Board('map1_1.txt')  

    # Calculate the size of the game window based on the size of the game board and the cell size
    screen_width = game_map.m * (game_map.CELL_SIZE + MARGIN) + MARGIN * 2
    screen_height = game_map.n * (game_map.CELL_SIZE + MARGIN) + MARGIN * 2
    screen_size = (screen_width, screen_height)

    # Create the game window
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Map Representation")

    seeker = Seeker(game_map)

    done = False
    clock = pygame.time.Clock()

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

        # Draw the game map
        game_map.draw_map(screen, game_map.CELL_SIZE)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
