from Tkinter import Tk
from tkFileDialog import askopenfilename
import re

A_COMMAND = 1
C_COMMAND = 2
L_COMMAND = 3

class Parser:
    def __init__(self, fname):
        f = open(fname)
        self.lines = list()
        self.i = 0
        for l in f.readlines():
            self.lines.append(l)
        f.close()

    def trim(self, line):
        line = line[:-1]
        commentpos = line.find("//")
        if commentpos + 1:
            line = line[0 : commentpos]
        line = re.sub('\s+', '', line)
        return line

    def hasMoreCommands(self):
        while self.i < len(self.lines):
            self.lines[self.i] = self.trim(self.lines[self.i])
            if self.lines[self.i] > 1:
                return True
            self.lines.pop(self.i)
        return False

    def advance(self):
        self.command = self.lines[self.i]
        print "@" + self.command + "@"
        self.i += 1

    def commandType(self):
        if self.command[0] == "@":
            return A_COMMAND
        elif self.command[0] == "(":
            return L_COMMAND
        else:
            return C_COMMAND

    def symbol(self):
        if self.commandType() == A_COMMAND:
            tmp = self.command[1:]
            if re.match("\A[a-zA-Z\._\$:][a-zA-Z0-9\._\$:]*\Z", tmp):
                return tmp
            else:
                return int(tmp)
        else:
            return self.command[1:-1]

    def dest(self):
        return self.command.split("=")[0]

    def comp(self):
        t1 = self.command.split(";")
        t2 = t1[0].split("=")
        if len(t2) > 1:
            return t2[1]
        return t2[0]

    def jump(self):
        return self.command.split(";")[1]

    def reset(self):
        self.i = 0


class Code:
    def __init__(self):
        self.jmpval = {}
        self.jmpval["JMP"] = "111"
        self.jmpval["JLE"] = "110"
        self.jmpval["JNE"] = "101"
        self.jmpval["JGE"] = "011"
        self.jmpval["JLT"] = "100"
        self.jmpval["JGT"] = "001"
        self.jmpval["JEQ"] = "010"
        self.jmpval[""] = "000"

        self.dval = {}
        self.dval["AMD"] = "111"
        self.dval["AD"] = "110"
        self.dval["AM"] = "101"
        self.dval["MD"] = "011"
        self.dval["A"] = "100"
        self.dval["M"] = "001"
        self.dval["D"] = "010"
        self.dval[""] = "000"

        self.cinstrval = {}
        self.cinstrval["0"] = "0101010"
        self.cinstrval["1"] = "0111111"
        self.cinstrval["-1"] = "0111010"
        self.cinstrval["D"] = "0001100"
        self.cinstrval["A"] = "0110000"
        self.cinstrval["!D"] = "0001101"
        self.cinstrval["!A"] = "0110001"
        self.cinstrval["-D"] = "0001111"
        self.cinstrval["-A"] = "0110011"
        self.cinstrval["D+1"] = "0011111"
        self.cinstrval["A+1"] = "0110111"
        self.cinstrval["D-1"] = "0001110"
        self.cinstrval["A-1"] = "0110010"
        self.cinstrval["D+A"] = "0000010"
        self.cinstrval["D-A"] = "0010011"
        self.cinstrval["A-D"] = "0000111"
        self.cinstrval["D&A"] = "0000000"
        self.cinstrval["D|A"] = "0010101"
        self.cinstrval["M"] = "1110000"
        self.cinstrval["!M"] = "1110001"
        self.cinstrval["-M"] = "1110011"
        self.cinstrval["M+1"] = "1110111"
        self.cinstrval["M-1"] = "1110010"
        self.cinstrval["D+M"] = "1000010"
        self.cinstrval["D-M"] = "1010011"
        self.cinstrval["M-D"] = "1000111"
        self.cinstrval["D&M"] = "1000000"
        self.cinstrval["D|M"] = "1010101"

    def dest(self, s):
        return self.dval[s]
    
    def comp(self, s):
        return self.cinstrval[s]
    
    def jump(self, s):
        return self.jmpval[s]



Tk().withdraw()
filename = askopenfilename()
fnew = filename.replace(".asm", ".hack")

bintext = ""

p = Parser(filename)
c = Code()

while p.hasMoreCommands():
    p.advance()
    if p.commandType() == A_COMMAND:
        tmp = str(bin(p.symbol()))[2:]
        bintext += "0" * (16 - len(tmp)) + tmp + "\n"
    elif p.commandType() == C_COMMAND:
        bintext += "111" + c.comp(p.comp()) + c.dest(p.dest()) + c.jump(p.jump())
        
f = open(fnew, 'w')
f.write(bintext)
f.close()
