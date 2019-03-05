#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:40:58 2019

@author: 3415762
"""
import random

class Carte:
    grid = [[]]         # List[List[0 ou -1]
    items = dict()      # Dict[ItemName:(lig, col)]
    players = dict()    # Dict[JoueurI:(lig, col)]
    nbPlayer = 0        # int
    
    def __init__(self, lig, col, nbPlayer, walls, players, **items):
        self.nbPlayer = nbPlayer
        self.players = {"joueur%d"(i):players[i] for i in range(nbPlayer)}
        self.items = {name:pos for (pos, name) in enumerate(items)}
        self.grid = [[0 if not (i,j) in walls else -1 for j in range(col)] for i in range(lig)]
    
    def isIn(self, lig, col):
        return 0 <= lig < len(self.grid) and 0 <= col < len(self.grid[0]) 
    
    def isWall(self, lig, col):
        return -1 == self.grid[lig][col]
    
    def isPlayer(self, lig, col):
        for pos in range(self.players.keys()):
            if (lig, col) == pos:
                return True
        return False
    
    def isItem(self, lig, col):
        for pos in range(self.items.keys()):
            if (lig, col) == pos:
                return True
        return False
    
    def movePlayer(self, player, pos):
        if player not in self.players.keys():
            return False
        if (self.isWall(pos[0], pos[1])):
            return False
        self.players[player] = pos
        return True
    
    def popItem(self, item):
        if item not in self.items.keys():
            return False
        self.items.pop(item)
        return True
    

class Game:
    players = []
    items = []
    scoreItems = [[]]
    score = []
    moves = [[]]
    carte = None
    nbJoueur = 0
    
    def __init__(self, carte, items, nbJoueur, players):
        self.carte = carte
        self.nbJoueur = nbJoueur
        self.players = players
        self.items = items
    
    
    

def initGame(carte, nbJoueur, *args):
    """
    Carte * int * List[Player]
    """
    if (len(args) != nbJoueur):
        print ("Veuillez entrer", nbJoueur, "joueurs")
        return None
    return Game(carte, nbJoueur)