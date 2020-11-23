import numpy as np
import random
import copy

def consecutif(arr, x):
    i = 0
    j = 0
    rec = 0
    while j<len(arr):
        if arr[j] == x:
            i += 1
        else:
            if i>rec:
                rec = i
            i=0
        j+=1
    if arr[-1] == x:
        return i
    else:
        return rec


class Minimax():
    def __init__(self):
        self.init_board()

    def init_board(self):
        self.player = "j1"
        self.winner = ""
        self.board = np.tile(' ', (7,7))
        print(self.board)
        self.colonne = {1:0,2:0,3:0,4:0,5:0,6:0,7:0}

    def move(self, player, col):
        if player == "p1":
            self.board[-self.colonne[col]-1,col-1] = "X"
        if player == "p2":
            self.board[-self.colonne[col]-1,col-1] = "0"
        self.colonne[col]+=1
        #print(self.board)

    def partie(self):
        pos = [10,10]
        joueur = ["j1", "ordi"]
        ind = 0
        self.player = joueur[ind]
        CW = 0
        while CW != 1:
            print("Au tour de : ", self.player)
            if self.player == "j1":
                print(self.board)
                coup = int(input())
                self.move("p1",coup)
                pos = (-self.colonne[coup], coup-1)
            if self.player == "ordi":
                coup = self.MinMax()
                self.move("p2",coup)
                pos = (-self.colonne[coup], coup-1)
            ind += 1
            self.player = joueur[ind%2]
            CW = self.condWin(pos)

    def condWin(self, pos):
        if pos == [10,10]:
            return 0
        pos=[pos[0]+7, pos[1]]
        val = self.board[pos[0], pos[1]]
        if list(self.colonne.values()) == [7,7,7,7,7,7,7]:
            print("Tie!")
            self.winner = "Tie"
            return 1
        else:
            hor = list(self.board[pos[0],:])
            ver = list(self.board[:,pos[1]])
            diag1, diag2 = self.makeDiagonale(pos)
            if consecutif(hor,val) >=4 or consecutif(ver, val)>=4 or consecutif(diag1, val)>=4 or consecutif(diag2, val) >=4:
                print("Win!!!")
                self.winner = self.player
                return 1

    def MinMax(self):
        print("Minmax")
        self.board2 = copy.deepcopy(self.board)
        self.colonne2 = copy.deepcopy(self.colonne)
        L=[]
        for i in range(1,8):
            for j in range(1,8):
                for k in range(1,8):
                    try:

                        self.move("p2",i)
                        pos = (-self.colonne[i], i-1)

                        self.move("p1",j)
                        pos = (-self.colonne[j], j-1)

                        self.move("p2",k)
                        pos = (-self.colonne[k], k-1)
                        L.append(self.score("0",pos))

                        self.board = copy.deepcopy(self.board2)
                        self.colonne = copy.deepcopy(self.colonne2)
                    except IndexError as e:
                        L.append(0)
        maxx = [max(i) for i in self.paquet(L)]
        minn = [min(i) for i in self.paquet(maxx)]
        maxx = np.argmax(minn)
        self.board = self.board2
        self.colonne =  self.colonne2
        print("fin minmax")
        return maxx+1

    def paquet(self, L):
        Lis = []
        souslis = []
        j = 1
        for i in L:
            souslis.append(i)
            if j%7==0:
                Lis.append(souslis)
                souslis = []
            j+=1
        return Lis

    def makeDiagonale(self, pos):
        if pos[1]>=pos[0]:
            ptref = [0,pos[1]-pos[0]]
            diag1 = [self.board[ptref[0]+i,ptref[1]+i] for i in range(pos[0]+7-pos[1])]
            extra = list(np.repeat(' ', ptref[1]))
            diag1 = extra + diag1
        else:
            ptref = [pos[0]-pos[1],0]
            diag1 = [self.board[ptref[0]+i,ptref[1]+i] for i in range(pos[1]+7-pos[0])]
            extra = list(np.repeat(' ', ptref[0]))
            diag1 = diag1 + extra
        if pos[1]+pos[0]<=6:
            ptref = [pos[1]+pos[0],0]
            diag2 = [self.board[ptref[0]-i,ptref[1]+i] for i in range(pos[0]+pos[1]+1)]
            extra = list(np.repeat(' ', 6-ptref[0]))
            diag2 = diag2 + extra
        else:
            ptref = [6,pos[1]-(6-pos[0])]
            diag2 = [self.board[ptref[0]-i,ptref[1]+i] for i in range(7-(pos[1]-(6-pos[0])))]
            extra = list(np.repeat(' ', ptref[1]))
            diag2 = extra + diag2
        return diag1, diag2

    def trancheLine(self, line):
        Lines = {}
        j = 0
        i = 1
        while i < len(line):
            if line[i]-1 != line[i-1]:
                i+=1
                j+=1
            else:
                if j not in Lines.keys():
                    Lines[j] = [line[i-1], line[i]]
                else:
                    Lines[j].append(line[i])
                i+=1
        return Lines

    def sous_score(self, line, pat, pos, val):
        transH = [i for i in range(len(line)) if line[i] == pat]
        trancheH = self.trancheLine(transH)
        for i in trancheH.keys():
            if val in trancheH[i]:
                if len(trancheH[i]) == 2:
                    return 2
                if len(trancheH[i]) == 3:
                    return 5
                if len(trancheH[i]) == 4:
                    return 1000
        return 0

    def score(self, pat, pos):
        pos=[pos[0]+7, pos[1]]
        score = 0
        val = self.board[pos[0], pos[1]]
        if pos[1] == 3: score += 4
        score += self.sous_score(list(self.board[pos[0],:]), pat, pos, pos[1])
        score += self.sous_score(list(self.board[:,pos[1]]), pat, pos, pos[0])
        score += self.sous_score(self.makeDiagonale(pos)[0], pat, pos, pos[1])
        score += self.sous_score(self.makeDiagonale(pos)[1], pat, pos, pos[1])
        return score

    def sous_score_adv(self, line, pat, pos, val, hvd):
        transH = [i for i in range(len(line)) if line[i] == pat]
        trancheH = self.trancheLine(transH)
        #print("pos", pos)
        #print(hvd, trancheH, transH)
        for i in trancheH.keys():
            if val in trancheH[i]:
                if len(trancheH[i]) == 2:
                    return -2
                if len(trancheH[i]) == 3:
                    tr = trancheH[i]
                    if hvd == "vertical":
                        return -100
                    if hvd == "horizontal":
                        if tr[-1] == 6 and self.board[pos[0],3] == " " and self.colonne[tr[0]-1] == 6 - pos[0]:
                            return -100
                        elif tr[-1] == 6:
                            return 0
                        if tr[0] == 0 and self.board[pos[0],3] == " " and self.colonne[tr[1]+2] == 6 - pos[0]:
                            return -100
                        elif tr[0] == 0:
                            return 0
                        if self.board[pos[0],tr[0]-1] == " " and self.colonne[tr[0]] == 6 - pos[0]: return -100
                        if self.board[pos[0],tr[-1]+1] == " " and self.colonne[tr[-1]+2] == 6 - pos[0]: return -100

                    if hvd == "diag1":
                        if pos[1] == tr[-1]:
                            pd = pos
                            pg = [pos[0]+2,pos[1]-2]
                        if pos[1] == tr[1]:
                            pd = [pos[0]-1,pos[1]+1]
                            pg = [pos[0]+1,pos[1]-1]
                        if pos[1] == tr[0]:
                            pd = [pos[0]-2,pos[1]+2]
                            pg = pos
                        if pg == [2,0] or pg == [6,4]:
                            return 0
                        if tr[-1] == 6 and self.board[pg[0]+1,pg[1]-1] == " " and self.colonne[tr[0]] == 5 - pg[0]:
                            return -100
                        elif tr[-1] == 6:
                            return 0
                        if tr[0] == 0 and self.board[pd[0]-1,pd[1]+1] == " " and self.colonne[tr[-1]+2] == 7 - pd[0]:
                            return -100
                        elif tr[0] == 0:
                            return 0
                        if pg[0] == 6 and self.board[pd[0]-1,pd[1]+1] == " " and self.colonne[tr[-1]+2] == 7 - pd[0]:
                            return -100
                        elif pg[0] == 6:
                            return 0
                        if pd[0] == 0 and self.board[pg[0]+1,pg[1]-1] == " " and self.colonne[tr[0]] == 5 - pg[0]:
                            return -100
                        elif pd[0] == 0:
                            return 0
                        if self.board[pg[0]+1,pg[1]-1] == " " and self.colonne[pg[1]] == 5 - pg[0]: return -100
                        if self.board[pd[0]-1,pd[1]+1] == " " and self.colonne[pd[1]+2] == 7 - pd[0]: return -100
                    if hvd == "diag2":
                        if pos[1] == tr[-1]:
                            pd = pos
                            pg = [pos[0]-2,pos[1]-2]
                        if pos[1] == tr[1]:
                            pd = [pos[0]+1,pos[1]+1]
                            pg = [pos[0]-1,pos[1]-1]
                        if pos[1] == tr[0]:
                            pd = [pos[0]+2,pos[1]+2]
                            pg = pos
                        #print("tr", tr)
                        #print("pd", pd)
                        #print("pg", pg)
                        if pg == [4,0] or pg == [0,4]:
                            return 0
                        if tr[-1] == 6 and self.board[pg[0]-1,pg[1]-1] == " " and self.colonne[tr[-1]] == 7 - pg[0]:
                            return -100
                        elif tr[-1] == 6:
                            return 0
                        if tr[0] == 0 and self.board[pd[0]+1,pd[1]+1] == " " and self.colonne[tr[-1]+2] == 5 - pd[0]:
                            return -100
                        elif tr[0] == 0:
                            return 0
                        if pg[0] == 0 and self.board[pd[0]+1,pd[1]+1] == " " and self.colonne[tr[-1]+2] == 5 - pd[0]:
                            return -100
                        elif pg[0] == 0:
                            return 0
                        if pd[0] == 6 and self.board[pg[0]-1,pg[1]-1] == " " and self.colonne[tr[0]] == 7 - pg[0]:
                            return -100
                        elif pd[0] == 6:
                            return 0
                        if self.board[pg[0]-1,pg[1]-1] == " " and self.colonne[pg[1]] == 7 - pg[0]: return -100
                        if self.board[pd[0]+1,pd[1]+1] == " " and self.colonne[pd[1]+2] == 5 - pd[0]: return -100
        return 0

    def scoreadv(self, pat, pos):
        pos=[pos[0]+7, pos[1]]
        score = 0
        val = self.board[pos[0], pos[1]]
        score += self.sous_score_adv(list(self.board[pos[0],:]), pat, pos, pos[1], "horizontal")
        score += self.sous_score_adv(list(self.board[:,pos[1]]), pat, pos, pos[0], "vertical")
        score += self.sous_score_adv(self.makeDiagonale(pos)[0], pat, pos, pos[1], "diag2")
        score += self.sous_score_adv(self.makeDiagonale(pos)[1], pat, pos, pos[1], "diag1")
        #print(pat, score)
        return score

MM = Minimax()
