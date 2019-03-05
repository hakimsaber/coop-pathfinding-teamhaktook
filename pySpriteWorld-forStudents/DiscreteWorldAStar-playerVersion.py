# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18
# 3415762, 2019-02-26

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

import heapq

# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----

class Probleme():
    def __init__(self, n, m, posInit,posFin):
        self.n = n
        self.m = m
        self.posInit = posInit
        self.posFin = posFin
        self.tab = [[0 for i in range(n)] for j in range(m)]
        
    def setWall(self, listePos):
        """
        List[2-uplet] -> void
        initialise les murs
        """
        for pos in listePos:
            self.tab[pos[0]][pos[1]] = -1
            
    def h(self, node):
        return hm(node.pos, self.posFin)
    
    def getPosInit(self):
        return self.posInit
    
    def getPosFin(self):
        return self.posFin
    
    def getCase(self, i, j):
        return self.tab[i][j]
    
    def estBut(self, pos):
        return pos == self.posFin
    
    def estMur(self, i, j):
        return self.tab[i][j] == -1
    
    def inTab(self, i, j):
        return 0 <= i < self.n and 0 <= j < self.m
    
    def immatriculation(self, node):
        """
        Node -> int
        """
        return node.pos[0] * self.n + node.pos[1]
    
    def getCasesAlontour(self, i, j):
        """
        int * int -> List[2-uplet[int]]
        ne regarde que la 4 directions
        Retourne la liste des cases au alontour dans le tableau, uniquement les cases possible
        """
        direction = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        return [(i+x, j+y) for x, y in direction if self.inTab(i+x, j+y) and not self.estMur(i+x, j+y)]
        
class Node:
    def __init__(self, pos):
        self.pos = pos
        self.pere = None
        self.fils = []
        self.g = 0
        
    def getFils(self,p):
        self.fils = [Node(pos) for pos in p.getCasesAlontour(self.pos[0], self.pos[1])]
        for node in self.fils:
            node.pere = self
            node.g = self.g + 1
        return self.fils
    
    def equal(self, node):
        return self.pos == node.pos
    
    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.g < other.g
        return NotImplemented
    
def hm(pos, posFinal):
    """
    2-uplet[int] * 2-uplet[int] -> int
    retourne l'heuristique de manhanttan
    """
    return abs(posFinal[1] - pos[0]) + abs(posFinal[1] - pos[1])

    
def Astar(p):
    """
        Probleme -> List[Noeud]
        retourne le chemin allant de l'etat initila à l'etat final
    """
    nodeInit = Node(p.getPosInit())
    frontiere = [(nodeInit.g + p.h(nodeInit), nodeInit)]
    reserve = dict()
    bestNode = nodeInit
    while frontiere != [] and not p.estBut(bestNode.pos):
        (min_f,bestNode) = heapq.heappop(frontiere)
        if p.immatriculation(bestNode) not in reserve:
            reserve[p.immatriculation(bestNode)] = bestNode.g
            nodes = bestNode.getFils(p)
            for node in nodes:
                f = node.g + p.h(node)
                heapq.heappush(frontiere, (f, node))
    return bestNode


# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Building the matrix
    #-------------------------------
       
           
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    print ("Wall states:", wallStates)
        
    
    #-------------------------------
    # Building the best path with A*
    #-------------------------------
    
    p = Probleme(21, 21, initStates[0], goalStates[0])
    p.setWall(wallStates)
    n = Astar(p)
    print(n.pos)
    l = []
    while n != None:
        l.append(n.pos)
        n = n.pere
    l.reverse()
        
    #-------------------------------
    # Moving along the path
    #-------------------------------
        
    # bon ici on fait juste un random walker pour exemple...
    

    row,col = initStates[0]
    #row2,col2 = (5,5)
    j = 0
    for i in range(iterations):
    
#        
#        x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
#        next_row = row+x_inc
#        next_col = col+y_inc
        if j < len(l):
            next_row, next_col = l[j]
            j += 1
            
        if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=20 and next_col>=0 and next_col<=20:
            player.set_rowcol(next_row,next_col)
            print ("pos 1:",next_row,next_col)
            game.mainiteration()

            col=next_col
            row=next_row

        
        
            
        # si on a  trouvé l'objet on le ramasse
        if (row,col)==goalStates[0]:
            o = game.player.ramasse(game.layers)
            game.mainiteration()
            print ("Objet trouvé!", o)
            break
        '''
        #x,y = game.player.get_pos()
    
        '''

    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()