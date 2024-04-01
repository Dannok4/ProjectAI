from Board import pygame

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