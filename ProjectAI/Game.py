from Board import *
from Hider import *
from Seeker import *
import pygame

def level1():
# create level
    pos_seeker =  (-1, 0)
    pos_all_hiders = [] # list of all hiders position
    all_announce_position = []
    filename = ""
    board = Board(pos_seeker, pos_all_hiders, False, filename)
    seeker = Seeker(pos_seeker)
    
    hiders = [] # create multi-hider
    for i in range(len(pos_all_hiders)):
        hider_i = Hider(pos_all_hiders[i])
        hiders.append(hider_i)
     
    while len(pos_all_hiders) != 0: # còn hider còn dí
        if board.steps != 0 and board.steps % 5 == 0: # neu la luot thu 5 moi vong -> announce
            for i in range(len(hiders)):
                all_announce_position.append(hiders[i].announce(board))
            
        pos_seeker = seeker.Seeker_move
       
        
        
        pos_seeker = seeker.position
        board.steps += 1

def level2():
    # create level
    pos_seeker =  (-1, 0)
    pos_all_hiders = [] # list of all hiders position
    all_announce_position = []
    filename = ""
    board = Board(pos_seeker, pos_all_hiders, False, filename)
    seeker = Seeker(pos_seeker)
    
    hiders = [] # create multi-hider
    for i in range(len(pos_all_hiders)):
        hider_i = Hider(pos_all_hiders[i])
        hiders.append(hider_i)
     
    while len(pos_all_hiders) != 0: # còn hider còn dí
        if board.steps != 0 and board.steps % 5 == 0: # neu la luot thu 5 moi vong -> announce
            for i in range(len(hiders)):
                all_announce_position.append(hiders[i].announce(board))
            
        #----------them vao dong nay ham nhin xung quanh / nghe xung quanh
        #----------neu thay hider / announce thi sao, khong thay thi sao
        
        pos_seeker = seeker.position
        board.steps += 1

#def level3():