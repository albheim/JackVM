'''
Created on 2 mar 2013

@author: Albin Heimerson
'''

import backend, frontend#, assembler
from Tkinter import Tk
from tkFileDialog import askdirectory

def main():
    Tk().withdraw()
    frontend.translate("C:/Users/Albin Heimerson/Desktop/nand2tetris/projects/10/Square/SquareGame.jack")#askdirectory())
    #backend.translate("C:/Users/Albin Heimerson/Desktop/nand2tetris/projects/08/FunctionCalls/StaticsTest")

if __name__ == "__main__":
    main()