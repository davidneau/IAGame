from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from minimax  import Minimax
import random

class Connect4(Minimax):

    def __init__(self):
        Minimax.__init__(self)
        self.fen = Tk()
        self.COTE = 350
        self.case = 50
        self.isMinMax = False
        self.can=Canvas(self.fen,bg="white", height=self.COTE, width=self.COTE)
        self.can.pack()
        self.var = IntVar()
        def get_int(coup):
            self.var.set(random.randint(1,9999))
            print(self.var.get())
            self.coup = coup
        canvButton = Canvas(self.fen,bg="white", height=self.case, width=self.COTE)
        canvButton.pack()
        self.bout1 = Button(canvButton, text='1',width=5, command = lambda:get_int(1))
        self.bout1.grid(row=0)
        self.bout2 = Button(canvButton, text='2',width=5, command = lambda:get_int(2)).grid(row=0, column=1)
        self.bout2 = Button(canvButton, text='3',width=5, command = lambda:get_int(3)).grid(row=0, column=2)
        self.bout2 = Button(canvButton, text='4',width=5, command = lambda:get_int(4)).grid(row=0, column=3)
        self.bout2 = Button(canvButton, text='5',width=5, command = lambda:get_int(5)).grid(row=0, column=4)
        self.bout2 = Button(canvButton, text='6',width=5, command = lambda:get_int(6)).grid(row=0, column=5)
        self.bout2 = Button(canvButton, text='7',width=5, command = lambda:get_int(7)).grid(row=0, column=7)
        self.init_board_GUI()
        self.partie()
        self.fen.mainloop()




    def init_board_GUI(self):
        self.can.create_rectangle(0,0,self.COTE, self.COTE, fill = "blue")
        NB_DE_CASES = 7
        MARGE=0
        PAS=50
        COTE = self.COTE
        x=0
        while (x<=NB_DE_CASES):
            self.can.create_line(MARGE,MARGE+PAS*x,MARGE+COTE,MARGE+PAS*x,fill='black')
            x=x+1
        x=0
        while (x<=NB_DE_CASES):
            self.can.create_line(MARGE+PAS*x,MARGE,MARGE+PAS*x,MARGE+COTE,fill='black')
            x=x+1

    def move(self, player, col):
        if player == "p1":
            self.board[-self.colonne[col]-1,col-1] = "X"
            posi = [-self.colonne[col]-1,col-1]
            if self.isMinMax == False:
                print(posi)
                posi[0] = posi[0] + 7
                self.can.create_oval((posi[1]*50)+5,(posi[0]*50)+5,(posi[1]*50+50)-5, (posi[0]*50+50)-5, fill = "red")
        if player == "p2":
            self.board[-self.colonne[col]-1,col-1] = "0"
            posi = [-self.colonne[col]-1,col-1]
            if self.isMinMax == False:
                print(posi)
                posi[0] = posi[0] + 7
                self.can.create_oval((posi[1]*50)+5,(posi[0]*50)+5,(posi[1]*50+50)-5, (posi[0]*50+50)-5, fill = "yellow")
        self.colonne[col]+=1

    def partie(self):
        self.init_board()
        pos = [10,10]
        joueur = ["j1", "ordi"]
        ind = 0
        self.player = joueur[ind]
        CW = 0
        while CW != 1:
            print("Au tour de : ", self.player)
            if self.player == "j1":
                print(self.board)
                print(self.var.get())
                self.bout1.wait_variable(self.var)
                print("coup de j1 :", self.coup)
                self.move("p1",self.coup)
                pos = (-self.colonne[self.coup], self.coup-1)
            if self.player == "ordi":
                self.isMinMax = True
                coup = self.MinMax()
                self.isMinMax = False
                self.move("p2",coup)
                pos = (-self.colonne[coup], coup-1)
            ind += 1
            self.player = joueur[ind%2]
            CW = self.condWin(pos)


C4 = Connect4()
