# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18
# 3415762, 2018-03-10

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys

from coopPlayer1 import *

# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----

def estCoupValide(board, pos, nextPos):
    return heuristique_manhattan(pos, nextPos) <= 1 and not board.isWall(nextPos) and not board.isPlayer(nextPos)

# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()
board = None

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'pathfindingWorld_MultiPlayer4'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 100  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():
    global board
    #for arg in sys.argv:
    iterations = 1000 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    
    #-------------------------------
    # Initialisation
    #-------------------------------
       
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    nbItems = len(goalStates)
    print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    
    (lig, col) = (20, 20)
    board = Board(lig, col, nbPlayers, nbItems)
    board.setWalls(wallStates)
    board.setItems(goalStates)
    board.setPlayers(initStates)
    pPlayer = [Player(board, i+1, players[i]) for i in range(nbPlayers)]
    
    #-------------------------------
    # Placement aleatoire des fioles 
    #-------------------------------
    
    
    # on donne a chaque joueur une fiole a ramasser
    # en essayant de faire correspondre les couleurs pour que ce soit plus simple à suivre
    
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
    for i in range(iterations):
##        board.show()
        for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
            p = pPlayer[j]
            (row,col) = board.getPlayer(p.player)
            (next_row, next_col) = p.play(board)
            #print((next_row, next_col))
            if estCoupValide(board, (row, col), (next_row, next_col)):
                board.setPlayer(p.player,(next_row, next_col))
                players[j].set_rowcol(next_row,next_col)
                #print ("pos :", p.player, next_row,next_col)
                game.mainiteration()
                col=next_col
                row=next_row
                
                
            # si on a  trouvé un objet on le ramasse
            if board.isOverlaping(p.player): # Si le joueur est sur un item
                if (p.wantPickup(board)):
                    o = p.pickUp(board, game.layers)
                    game.mainiteration()
                    print ("Objet trouvé par le joueur ", p.player)
                    item = board.whatOverlap(p.player)
                    score[j]+=1
                    
            
                    # et on remet un même objet à un autre endroit
                    x = random.randint(1,board.n-1)
                    y = random.randint(1,board.m-1)
                    while not board.isEmpty((x,y)):
                        x = random.randint(1,19)
                        y = random.randint(1,19)
                    o.set_rowcol(x,y)
                    board.setItem(item, (x, y))
                    print("Nouvelle objet se trouve :", (x, y))
                    game.layers['ramassable'].add(o)
                    game.mainiteration()                
                
                
                    break
        
    
    print ("scores:", score)
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


