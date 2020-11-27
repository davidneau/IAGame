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
        if player == "Player":
            self.board[-self.colonne[col]-1,col-1] = "X"
        if player == "ordi":
            self.board[-self.colonne[col]-1,col-1] = "0"
        self.colonne[col]+=1
        #print(self.board)

    def partie(self):
        pos = [10,10]
        joueur = ["Player", "ordi"]
        ind = 0
        self.player = joueur[ind]
        CW = 0
        i = 0
        while CW != 1:
            print("Au tour de : ", self.player)
            if self.player == "Player":
                print(self.board)
                coup = int(input())
                self.move("Player",coup)
                pos = (-self.colonne[coup], coup-1)
            if self.player == "ordi":
                coup = self.MinMax()+1
                self.move("ordi",coup)
                pos = (-self.colonne[coup], coup-1)
            i+=1
            ind += 1
            print(self.board)
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
                        sum = 0

                        self.move("ordi",i)
                        pos = (-self.colonne[i], i-1)
                        sum += self.score("ordi","0",pos)

                        self.move("Player",j)
                        pos = (-self.colonne[j], j-1)
                        sum += self.score("Player","X",pos)

                        self.move("ordi",k)
                        pos = (-self.colonne[k], k-1)
                        sum += self.score("ordi","0",pos)

                        L.append(sum)

                        self.board = copy.deepcopy(self.board2)
                        self.colonne = copy.deepcopy(self.colonne2)
                    except:
                        L.append(0)
                        self.board = copy.deepcopy(self.board2)
                        self.colonne = copy.deepcopy(self.colonne2)
        maxx = [max(i) for i in self.paquet(L)]
        print(maxx)
        minn = [min(i) for i in self.paquet(maxx)]
        print(minn)
        if len(np.unique(maxx)) == 1:
            maxx = random.randint(1,7)
        else:
            maxx = np.argmax(minn)
        self.board = copy.deepcopy(self.board2)
        self.colonne = copy.deepcopy(self.colonne2)
        print("fin minmax")
        return maxx

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
            diag1 = [self.board[ptref[0]+i, ptref[1]+i] for i in range(pos[0]+7-pos[1])]
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

    def relu(self,x):
        if x<0:
            return 0
        else:
            return x

    def threeinarow(self, L, pt, pat, vert):
        #return the position of the gap if there a 3 pieces in a row
        if vert:
            p = pt[0]
        else:
            p = pt[1]
        maxAlign = 0
        numberOfWindows = 4-abs(p-3)
        for wind in range(numberOfWindows):
            w = L[self.relu(p-3)+wind : self.relu(p-3)+wind+4]
            if w.count(pat) == 3 and w.count(' ') == 1:
                if maxAlign < 3:
                    maxAlign = 3
                a = wind
                b = w
            elif w.count(pat) == 4:
                maxAlign = 4
        if maxAlign == 3:
            return self.relu(p - 3) + a + b.index(' ') + 1
        elif maxAlign == 4:
            return "win"

    def get_heuristic(self, player, line, pat,  pos, vert):
        score = self.threeinarow(line, pos, pat, vert)
        if score != None: print(score)
        if score == "win" and player == "Player": return -100000
        if score == "win" and player == "ordi": return 10000000
        if score != None:
            newpos=[6-self.colonne[score], score-1]
            self.move(player, score)
            CW2 = self.condWin([newpos[0]-7,newpos[1]])
            print(CW2)
            if CW2 == 1:
                if player == "Player":
                    self.board[newpos[0], newpos[1]] = ''
                    self.colonne[score] -= 1
                    return -100
                if player == "ordi":
                    self.board[newpos[0], newpos[1]] = ''
                    self.colonne[score] -= 1
                    return 1
        return 0

    def score(self, player, pat, pos):
        pos=[pos[0]+7, pos[1]]
        score = 0
        val = self.board[pos[0], pos[1]]
        score += self.get_heuristic(player, list(self.board[pos[0],:]), pat, pos, False)
        score += self.get_heuristic(player, list(self.board[:,pos[1]]), pat, pos, True)
        score += self.get_heuristic(player, self.makeDiagonale(pos)[0], pat, pos, False)
        score += self.get_heuristic(player, self.makeDiagonale(pos)[1], pat, pos, False)
        return score
