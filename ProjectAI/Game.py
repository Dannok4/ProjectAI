from Board import *
from Hider import *
from Seeker import *
import pygame

def level_1_2():
# create level
    pos_seeker =  (-1, 0)
    pos_all_hiders = [] # list of all hiders position
    all_announce_position = []
    filename = ""
    board = Board(pos_seeker, pos_all_hiders, False, filename)
    seeker = Seeker(-1, 0)
    
    all_hiders = [] # create all hiders
    for i in range(len(pos_all_hiders)):
        hider_i = Hider(pos_all_hiders[i]) # add all hiders
        all_hiders.append(hider_i)
        
    # hàm vẽ map
     
    while len(all_hiders) != 0: # còn hider còn dí
        if board.steps != 0 and board.steps % 5 == 0: # neu la luot thu 5 moi vong -> announce
            for i in range(len(all_hiders)):
                all_announce_position.append(all_hiders[i].announce(board))
            
        pos_seeker = seeker.Seeker_move # di chuyển seeker tìm hider(s)
        seeker.point -= 1
        board.steps += 1
        
        for j in range(len(all_hiders)):
            if all_hiders[j].position == seeker.position:
                all_hiders.pop(j)
                seeker.point += 20
        
        # hàm vẽ map
        
    # in ra điểm

def level3():
   # create level
    pos_seeker =  (-1, 0)
    pos_all_hiders = [] # list of all hiders position
    all_announce_position = []
    filename = ""
    board = Board(pos_seeker, pos_all_hiders, False, filename)
    seeker = Seeker(-1, 0)
    
    all_hiders = [] # create all hiders
    for i in range(len(pos_all_hiders)):
        hider_i = Hider(pos_all_hiders[i]) # add all hiders
        all_hiders.append(hider_i)
     
    # hàm vẽ map

    while len(all_hiders) != 0: # còn hider còn dí
        if board.steps != 0 and board.steps % 5 == 0: # neu la luot thu 5 moi vong -> announce
            for i in range(len(all_hiders)):
                all_announce_position.append(all_hiders[i].announce(board))
                
        for i in range(all_hiders):
            all_hiders[i].movement_strategy(board) # di chuyển các hiders
            
        pos_seeker = seeker.Seeker_move # di chuyển seeker tìm hider(s)
        seeker.point -= 1
        board.steps += 1
        
        for j in range(len(all_hiders)):
            if all_hiders[j].position == seeker.position:
                all_hiders.pop(j)
                seeker.point += 20
        
        # hàm vẽ map
        
    # in ra điểm 