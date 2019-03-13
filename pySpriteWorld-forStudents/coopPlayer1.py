# -*- coding: utf-8 -*-
# 3415762, 2018-03-10
import heapq
import random
class Board:
    """
    classe Board stocke un plateau de N lignes, M colonnes.
    Elle enregistre la position actuelle des joueurs et des objets.
    pour chaque case est représenté par un entier relatif tel que :
        -  0 : case vide
        - -1 : Mur, obstacle i.e case inaccessible.
        - [1, ..., nbPlayers[ : joueurs.
        - [-nbItems, ..., -2] : item, tel que item i à pour valeur -i-1 sur le
        plateau.
    Chaque joueur n° i à pour objectif l'item n° j, tel que 0 < i = j
    """
    def __init__(self, lig, col, nbPlayers, nbItems, goals=[]):
        self.n = lig
        self.m = col
        self.tab = [[0 for i in range(col)] for j in range(lig)]
        self.players = [(0, 0)] * nbPlayers
        self.goals = goals if len(goals) == nbPlayers else [i+1 if i < nbItems else random.randint(1,nbItems) for i in range(nbPlayers)]
        self.items = [(0, 0)] * nbItems
        self.overlapPlayersAndItems = [[True for j in range(nbItems)] for i in range(nbPlayers)]
        
    def setWalls(self, walls):
        """
        List[pos] -> void
        pour chaque position devient un mur dans le plateau
        """
        for (l, c) in walls:
            self.tab[l][c] = -1

    def updateOverlap(self):
        """
        void -> void
        met à jour la liste de liste boolean indiquant si un joueur est sur la 
        meme case qu'un objet.
        """
        nbItems = len(self.items)
        nbPlayers = len(self.players)
        for i in range(nbPlayers):
            for j in range(nbItems):
                self.overlapPlayersAndItems[i][j] = (self.players[i] == self.items[j])

    def isOverlaping(self, player):
        """
        player -> boolean
        Retourne True le joueur est sur un item
        """
        for b in self.overlapPlayersAndItems[player-1]:
            if b:
                return b
        return False

    def whatOverlap(self, player):
        """
        player -> item or None
        Retourne l'item sur le lequel le joueur est sinon None
        """
        for i,b in enumerate(self.overlapPlayersAndItems[player-1]):
            if b:
                return i+1
        return None
    
    def setPlayers(self, playersPos):
        """
        List[pos] -> void
        Met à jour sur le plateau et la liste des players leur position
        * met à jour l'overlapping
        """
        for i in range(len(self.players)):
            self.players[i] = playersPos[i]
            (l, c) = playersPos[i]
            self.tab[l][c] = i+1
        self.updateOverlap()
        
    def setItems(self, itemsPos):
        """
        List[pos] -> void
        Met à jour sur le plateau et la liste des items leur position
        * met à jour l'overlapping
        """
        for i in range(len(self.items)):
            self.items[i] = itemsPos[i]
            (l, c) = itemsPos[i]
            self.tab[l][c] = -2 - i
        self.updateOverlap()
                
    def inTab(self, pos):
        """
        pos -> boolean
        retourne True si la position est sur le plateau
        """
        (l, c) = pos
        return 0 <= l < self.n and 0 <= c < self.m

    def isWall(self, pos):
        """
        pos -> boolean
        retourne True si la position est un mur
        """
        (l, c) = pos
        return self.tab[l][c] == -1

    def isPlayer(self, pos):
        """
        pos -> boolean
        retourne True si la position est un player
        """
        (l, c) = pos
        return self.tab[l][c] > 0 or pos in self.players

    def isItem(self, pos):
        """
        pos -> boolean
        retourne True si la position est un objet
        """
        (l, c) = pos
        return self.tab[l][c] < -1 or pos in self.items

    def isEmpty(self, pos):
        """
        pos -> boolean
        retourne True si la position est vide
        """
        (l, c) = pos
        return self.tab[l][c] == 0
    
    def get(self, pos):
        """
        pos -> int
        retourne la valeur sur le plateau
        """
        (l, c) = pos
        return self.tab[l][c]
    
    def getPlayer(self, player):
        """
        player -> pos
        retourne la position du joueur
        """
        return self.players[player-1]
    
    def setPlayer(self, player, pos):
        """
        player * pos -> boolean
        retourne True si le changement de position du joueur spécifié à pu 
        se faire, sinon False
        * contrainte, la position indiqué :
            - sur le plateau
            - ne doit pas un être un mur
        * met à jour l'overlapping
        """
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
        """
        item -> pos
        retourne la position de l'item demandé
        """
        return self.items[item-1]
    
    def setItem(self, item, pos):
        """
        item * pos -> boolean
        retourne True si le changement de position de l'item spécifié à pu 
        se faire, sinon False
        * contrainte, la position indiqué :
            - sur le plateau
            - doit être vide
        * met à jour l'overlapping
        """
        if self.inTab(pos) and self.isEmpty(pos):
            self.items[item-1] = pos
            (l, c) = pos
            self.tab[l][c] = -item - 1
            self.updateOverlap()
            return True
        return False
    
    def getGoal(self, player):
        """
        player -> item
        Retourne l'item recherché par le joueur
        """
        return self.goals[player-1]
    
    def isGoal(self, player, pos):
        """
        player * pos -> boolean
        Retourne True si le player se trouve à la même position que l'item
        recherché.
        """
        return self.items[self.goals[player-1]-1] == pos
    
    def getId(self, pos):
        """
        pos -> int
        Retourne un numéro unique pour chaque case du plateau
        """
        return pos[0] * self.n + pos[1]

    def getCasesVidesAlontour(self, pos):
        """
        pos -> list[pos]
        Retourne la liste des position accessible par un joueur.
        Respecte les affrimations suivantes : 
            - dans le plateau
            - n'est pas un mur
            - un joueur n'est pas déjà dessus
        """
        return [(pos[0] + l, pos[1] + c) for (l, c) in [(-1, 0), (1, 0), (0, -1), (0, 1)] if self.inTab((pos[0] + l, pos[1] + c)) and not self.isWall((pos[0] + l, pos[1] + c)) and not self.isPlayer((pos[0] + l, pos[1] + c))]

    def show(self):
        """
        void -> void
        Affiche le plateau sur la sortie standart
        """
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
        """
        void -> Board
        Retourne une copie de cette instance Board.
        c'est une copie en profondeur.
        """
        copy = Board(self.n, self.m, len(self.players), len(self.nbItems))
        copy.setPlayers(self.players)
        copy.setItems(self.items)
        for i in range(self.n):
            for j in range(self.m):
                if (self.tab[i][j] == -1):
                    copy.tab[i][j] == -1
        return copy

class Player:
    """
    classe Player, désigne un joueur coopéaratif
    Il cherche à obtenir l'objet dont la position est indiqué dans board
    """
    def __init__(self, board, player, o, algo="A*"):
        self.player = player
        self.algo = algo
        self.o = o

    def play(self, board):
        """
        Board -> pos
        Retourne un coup i.e la prochaine case où il souhaite se rendre.
        dans el but de parvenir à la case qui détient son objectif
        """
        pos = board.getPlayer(self.player)
        goal = board.getItem(board.getGoal(self.player))
        if self.algo == "A*":
            l = Astar(board, self.player, pos, goal, 1000)
    ##        print("mon chemin", l)
            if len(l) > 1:
                return l[1]
            else:
                return l[0]
        return pos
    
    def wantPickup(self, board):
        """
        void -> boolean
        Retourne True si le joueur désire rammassé la fiole, false sinon
        * Dans le cadre de la coopéaration, le joueur ne souhaite que 
        rammassé sa fiole
        """
        pos = board.getPlayer(self.player)
        goal = board.getItem(board.getGoal(self.player))
        return pos == goal
    
    def pickUp(self, board, layers):
        """
        Board * Layers -> Rammassable
        Hypothèse on suppose qu'il existe un objet a rammassé
        Retourne l'objet Rammasé
        """
        return self.o.ramasse(layers)
    
class Node:
    """
    Classe Node, désigne un noeud ou une feuille d'un arbre, elle represente 
    le parcours dans une Board.
    chaque noeud possède:
        - un père
        - liste de ses fils i.e les positions aux alontour accessible
        - position dans la Board
        - g, le coût pour arriver de la racine de l'arbre à ce noeud.
    """
    def __init__(self, pos):
        self.pere = None
        self.fils = []
        self.g = 0
        self.pos = pos
        
    def getFils(self, board):
        """
        Board -> void
        Remplis le la liste des fils du Noeud par l'etat de la board donné.
        * chaque fils à pour g, le g du père plus un.
        """
        self.fils = [Node(pos) for pos in board.getCasesVidesAlontour(self.pos)]
        for node in self.fils:
            node.pere = self
            node.g = self.g + 1
        return self.fils

    def h(self, finalPos):
        """
        pos -> int
        Retourne l'heuristique de manhattan du Noeud par rapport à la position 
        donné.
        """
        return heuristique_manhattan(self.pos, finalPos)

    def immatriculation(self, board):
        """
        Board -> int
        Retourne un entier unique à chaque Noeud
        * Utilise la méthode id de la board pour donné un entier unique en 
        fonction de la position que représente le noeud.
        """
        return board.getId(self.pos)
    
    def equal(self, node):
        """
        Node -> boolean
        Retourne True si les noeuds sont les mêmes
        """
        return self.pos == node.pos
    
    def __lt__(self, other):
        """
        other -> boolean Or NotImplemented
        retourne True si le coût du noeud actuelle est inférieur au noeud 
        spécifié.
        """
        if isinstance(other, self.__class__):
            return self.g < other.g
        return NotImplemented

def heuristique_manhattan(currentPos, finalPos):
    """
    pos * pos -> int
    Retourne le nombre de case maximum séparant les deux positions.
    * heuristique
    """
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
