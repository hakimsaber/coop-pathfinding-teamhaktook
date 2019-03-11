# -*- coding: utf-8 -*-
# 3415762, 2018-03-10
import heapq
import sys

class Board:
    def __init__(self, lig, col, nbPlayers, nbItems):
        self.n = lig
        self.m = col
        self.tab = [[0 for i in range(col)] for j in range(lig)]
        self.players = [(0, 0)] * nbPlayers
        self.items = [(0, 0)] * nbItems
        self.overlapPlayersAndItems = [[True for j in range(nbItems)] for i in range(nbPlayers)]
        
    def setWalls(self, walls):
        for (l, c) in walls:
            self.tab[l][c] = -1

    def updateOverlap(self):
        nbItems = len(self.items)
        nbPlayers = len(self.players)
        for i in range(nbPlayers):
            for j in range(nbItems):
                self.overlapPlayersAndItems[i][j] = (self.players[i] == self.items[j])

    def isOverlaping(self, player):
        for b in self.overlapPlayersAndItems[player-1]:
            if b:
                return b
        return False

    def whatOverlap(self, player):
        item = None
        for i,b in enumerate(self.overlapPlayersAndItems[player-1]):
            if b:
                return i+1
        return None
    
    def setPlayers(self, playersPos):
        for i in range(len(self.players)):
            self.players[i] = playersPos[i]
            (l, c) = playersPos[i]
            self.tab[l][c] = i+1
        self.updateOverlap()
        
    def setItems(self, itemsPos):
        for i in range(len(self.items)):
            self.items[i] = itemsPos[i]
            (l, c) = itemsPos[i]
            self.tab[l][c] = -2 - i
        self.updateOverlap()
    
                
    def inTab(self, pos):
        (l, c) = pos
        return 0 <= l < self.n and 0 <= c < self.m

    def isWall(self, pos):
        (l, c) = pos
        return self.tab[l][c] == -1

    def isPlayer(self, pos):
        (l, c) = pos
        return self.tab[l][c] > 0

    def isItem(self, pos):
        (l, c) = pos
        return self.tab[l][c] < -1

    def isEmpty(self, pos):
        (l, c) = pos
        return self.tab[l][c] == 0
    
    def get(self, pos):
        (l, c) = pos
        return self.tab[l][c]
    
    def getPlayer(self, player):
        return self.players[player-1]
    
    def setPlayer(self, player, pos):
        if self.inTab(pos) and (self.isEmpty(pos) or self.isItem(pos)):
            (oldL, oldC) = self.players[player-1]
            self.tab[oldL][oldC] = 0
            self.players[player-1] = pos
            (l, c) = pos
            self.tab[l][c] = player
            self.updateOverlap()
            return True
        return False
    
    def getItem(self, item):
        return self.items[item-1]
    
    def setItem(self, item, pos):
        if self.inTab(pos) and self.isEmpty(pos):
            self.items[item-1] = pos
            (l, c) = pos
            self.tab[l][c] = -item - 1
            self.updateOverlap()
            return True
        return False

    def posTo(self, pos):
        i = self.get(pos)
        if i == 0:
            return 0
        elif i == -1:
            return -1
        elif i > 0:
            return i
        elif i < -1:
            return -i - 1
        
    def isGoal(self, player, pos):
        return self.items[player-1] == pos
    
    def getId(self, pos):
        return pos[0] * self.n + pos[1]

    def getCasesVidesAlontour(self, pos):
        return [(pos[0] + l, pos[1] + c) for (l, c) in [(-1, 0), (1, 0), (0, -1), (0, 1)] if self.inTab((pos[0] + l, pos[1] + c)) and not self.isWall((pos[0] + l, pos[1] + c)) and not self.isPlayer((pos[0] + l, pos[1] + c))]

    def show(self):
        s = "".join(['-' for i in range(self.m * 2 + 1)]) + '\n'
        for i in range(self.n):
            s += "|"
            for j in range(self.m):
                c = " "
                if self.tab[i][j] == -1:
                    c = "#"
                elif self.tab[i][j] < -1:
                    c = "o"
                elif self.tab[i][j] > 0:
                    c = str(self.tab[i][j])
                s += c
                if (not j == (self.m - 1)):
                    s += " "
                else:
                    s += "|"
            s += "\n"
        s += "".join(['-' for i in range(self.m * 2 + 1)])
        print(s)
        
    def deepCopy(self):
        copy = Board(self.n, self.m, len(self.players), len(self.nbItems))
        copy.setPlayers(self.players)
        copy.setItems(self.items)
        for i in range(self.n):
            for j in range(self.m):
                if (self.tab[i][j] == -1):
                    copy.tab[i][j] == -1
        return copy

class Player:
    def __init__(self, board, player):
        self.player = player

    def play(self, board):
        pos = board.getPlayer(self.player)
        goal = board.getItem(self.player)
        l = Astar(board, self.player, pos, goal, 1000)
##        print("mon chemin", l)
        if len(l) > 1:
            return l[1]
        else:
            return l[0]
        
class Node:
    def __init__(self, pos):
        self.pere = None
        self.fils = []
        self.g = 0
        self.pos = pos
        
    def getFils(self, board):
        self.fils = [Node(pos) for pos in board.getCasesVidesAlontour(self.pos)]
        for node in self.fils:
            node.pere = self
            node.g = self.g + 1
        return self.fils

    def h(self, finalPos):
        return heuristique_manhattan(self.pos, finalPos)

    def immatriculation(self, board):
        return board.getId(self.pos)
    
    def equal(self, node):
        return self.pos == node.pos
    
    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.g < other.g
        return NotImplemented

def heuristique_manhattan(currentPos, finalPos):
    (x, y) = currentPos
    (fx, fy) = finalPos
    return abs(fy - y) + abs(fx - x)

def Astar(board, player, posInit, goal, iteration=1000):
    """
        Probleme -> List[pos]
        retourne le chemin allant de l'etat initila à l'etat final
    """
    #print(player, posInit, "cherche", goal)
    n = 0
    nodeInit = Node(posInit)
    frontiere = [(nodeInit.g + nodeInit.h(goal), nodeInit)]
    reserve = dict()
    bestNode = nodeInit
    # Exploration
    while frontiere != [] and not board.isGoal(player, bestNode.pos) and n < iteration:
        #print("    ", bestNode.pos)
        #print("    ",frontiere)
        #print("    ", reserve)
        (min_f,bestNode) = heapq.heappop(frontiere)
        if bestNode.immatriculation(board) not in reserve:
            reserve[bestNode.immatriculation(board)] = bestNode.g
            nodes = bestNode.getFils(board)
            for node in nodes:
                f = node.g + node.h(goal)
                heapq.heappush(frontiere, (f, node))
        n += 1
##    print("n :", n)
##    print("reste :", len(frontiere))
##    print("evalué :", len(reserve))
    # The path
    l = []
    node = bestNode
    while node != None:
        l.append(node.pos)
        node = node.pere
    l.reverse()
    return l
