from Tkinter import Tk
from tkFileDialog import askopenfilename
import re


jmpval = {}
jmpval["JMP"] = "111"
jmpval["JLE"] = "110"
jmpval["JNE"] = "101"
jmpval["JGE"] = "011"
jmpval["JLT"] = "100"
jmpval["JGT"] = "001"
jmpval["JEQ"] = "010"

cinstrval = {}
cinstrval["0"] = "101010"
cinstrval["1"] = "111111"
cinstrval["-1"] = "111010"
cinstrval["D"] = "001100"
cinstrval["A"] = "110000"
cinstrval["!D"] = "001101"
cinstrval["!A"] = "110001"
cinstrval["-D"] = "001111"
cinstrval["-A"] = "110011"
cinstrval["D+1"] = "011111"
cinstrval["A+1"] = "110111"
cinstrval["D-1"] = "001110"
cinstrval["A-1"] = "110010"
cinstrval["D+A"] = "000010"
cinstrval["D-A"] = "010011"
cinstrval["A-D"] = "000111"
cinstrval["D&A"] = "000000"
cinstrval["D|A"] = "010101"
cinstrval["M"] = "110000"
cinstrval["!M"] = "110001"
cinstrval["-M"] = "110011"
cinstrval["M+1"] = "110111"
cinstrval["M-1"] = "110010"
cinstrval["D+M"] = "000010"
cinstrval["D-M"] = "010011"
cinstrval["M-D"] = "000111"
cinstrval["D&M"] = "000000"
cinstrval["D|M"] = "010101"

labels = {}
labels["SP"] = labels["R0"] = 0
labels["LCL"] = labels["R1"] = 1
labels["ARG"] = labels["R2"] = 2
labels["THIS"] = labels["R3"] = 3
labels["THAT"] = labels["R4"] = 4
labels["R5"] = 5
labels["R6"] = 6
labels["R7"] = 7
labels["R8"] = 8
labels["R9"] = 9
labels["R10"] = 10
labels["R11"] = 11
labels["R12"] = 12
labels["R13"] = 13
labels["R14"] = 14
labels["R15"] = 15
labels["SCREEN"] = 16384
labels["KBD"] = 24576

rcount = 16

def trim(line):
    line = line[:-1]
    commentpos = line.find("//")
    if commentpos + 1:
        line = line[0 : commentpos]
    line = re.sub('\s+', ' ', line)
    return line


def labelcheck(line, num):
    line = trim(line)
    
    if len(line) < 2:
        return 0

    if line[0] == "(":
        labels[line[1:-1]] = num
        return 0
    
    return 1

def translate(line):
    line = trim(line)
    
    if len(line) < 2:
        return ""
    
    if line[0] == "@":
        astr = line[1:]
        num = 0
        if astr in labels:
            num = str(bin(labels[astr]))[2:]
        elif re.match("\A[a-zA-Z\._\$:][a-zA-Z0-9\._\$:]*\Z", astr):
            global rcount
            labels[astr] = rcount
            num = str(bin(rcount))[2:]
            rcount += 1
        else:
            num = str(bin(int(astr)))[2:]
        return "0" * (16 - len(num)) + num + "\n"

    if line[0] == "(":
        return ""

    jmp=dest=cinstr=""
    instr = "111"

    t1 = line.split(";")
    t2 = t1[0].split("=")
    cinstr = t2[0]
    if len(t2) > 1:
        cinstr = t2[1]
        dest = t2[0]

    if cinstr.find("M") + 1:
        instr = instr + "1"
    else:
        instr = instr + "0"

    instr = instr + cinstrval[cinstr]
    if dest.find("A") + 1:
        instr += "1"
    else:
        instr += "0"            
    if dest.find("D") + 1:
        instr += "1"
    else:
        instr += "0"
    if dest.find("M") + 1:
        instr += "1"
    else:
        instr += "0"
    if len(t1) > 1:
        instr = instr + jmpval[t1[1]]
    else:
        instr = instr + "000"
    return instr + "\n"


Tk().withdraw()
filename = askopenfilename()

fnew = filename.replace(".asm", ".hack")

f = open(filename)

bintext = ""

k = list()
num = 0

for line in f.readlines():
    k.append(line)
    num += labelcheck(line, num)

for line in k:
    bintext += translate(line)

f = open(fnew, 'w')
f.write(bintext)
f.close()


