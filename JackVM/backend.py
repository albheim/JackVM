from Tkinter import Tk
from tkFileDialog import askopenfilename
import os

'''
Created on 2 mar 2013

@author: Albin Heimerson
'''
class Parser(object):
    
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3 
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6 
    C_RETURN = 7
    C_CALL = 8
    
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
            
        while line.find("  ") + 1:
            line = line.replace("  ", " ")
            
        while len(line) > 0 and line[0] == " ":
            line = line[1:]
            
        while len(line) > 0 and line[-1] == " ":
            line = line[0:-1]
        return line

    def hasMoreCommands(self):
        while self.i < len(self.lines):
            self.lines[self.i] = self.trim(self.lines[self.i])
            if len(self.lines[self.i]) > 1:
                return True
            self.lines.pop(self.i)
        return False

    def advance(self):
        print self.lines[self.i]
        tmp = self.lines[self.i].split(" ")
        self.vcommand = tmp[0]
        if len(tmp) > 1:
            self.varg1 = tmp[1]
        if len(tmp) > 2:
            self.varg2 = tmp[2]
        self.i += 1

    def commandType(self):
        if self.vcommand == "pop":
            return self.C_POP
        if self.vcommand == "push":
            return self.C_PUSH
        if self.vcommand == "label":
            return self.C_LABEL
        if self.vcommand == "goto":
            return self.C_GOTO
        if self.vcommand == "if-goto":
            return self.C_IF
        if self.vcommand == "function":
            return self.C_FUNCTION
        if self.vcommand == "return":
            return self.C_RETURN
        if self.vcommand == "call":
            return self.C_CALL
        
        return self.C_ARITHMETIC
    
    def command(self):
        return self.vcommand
    
    def arg1(self):
        return self.varg1
    
    def arg2(self):
        return self.varg2


class CodeWriter(object):
        
    def __init__(self, f):
        self.savename = f
        self.buffer = ""
        self.funcname = ""
        self.retaddcnt = 0
        
    def setFileName(self, filename):
        self.filename = filename.split("/")[-1].split(".")[0]
        self.varcount = 0
        self.retaddcnt = 0

    
    def writeInit(self):
        self.buffer += "@256 \n D=A \n @SP \n M=D \n @Sys.init \n 0;JMP\n\n"
    
    def writeLabel(self, label):
        self.buffer += "(" + self.funcname + "$" + label + ") \n\n"
    
    def writeGoto(self, label):
        self.buffer += "@" + self.funcname + "$" + label + " \n 0;JMP \n\n"
    
    def writeIf(self, label):
        self.buffer += "@SP \n AM=M-1 \n D=M \n @" + self.funcname + "$" + label + " \n D;JNE \n\n"
    
    def writeCall(self, functionName, numArgs):#problem med return address
        self.retaddcnt += 1
        self.buffer += "@" + self.funcname + "$return_" + str(self.retaddcnt) + " \n D=A  \n @SP \n A=M  \n M=D \n @LCL \n"
        self.buffer += " D=M  \n @SP  \n AM=M+1 \n M=D \n  @ARG  \n D=M  \n @SP \n AM=M+1 \n M=D \n @THIS  \n D=M  \n @SP  \n "
        self.buffer += "AM=M+1 \n M=D \n @THAT  \n D=M  \n @SP  \n AM=M+1 \n M=D \n @SP \n M=M+1 \n D=M  \n @5  \n D=D-A  \n @"
        self.buffer += numArgs + " \n D=D-A  \n @ARG  \n M=D \n @SP  \n D=M  \n @LCL  \n M=D \n @"
        self.buffer += functionName + " \n 0;JMP  \n (" + self.funcname + "$return_" + str(self.retaddcnt) + ")  \n\n"
    
    def writeReturn(self):
        self.buffer += "@LCL  \n D=M  \n @R13  \n M=D  \n @5  \n A=D-A  \n D=M  \n @R14  \n M=D  \n @SP  \n"
        self.buffer += " AM=M-1  \n D=M  \n @ARG  \n A=M  \n M=D \n D=A+1  \n @SP  \n M=D  \n @R13  \n AM=M-1  \n"
        self.buffer += " D=M  \n @THAT  \n M=D \n @R13  \n AM=M-1  \n D=M  \n @THIS  \n M=D  \n @R13  \n AM=M-1  \n"
        self.buffer += " D=M  \n @ARG  \n M=D \n @R13  \n AM=M-1  \n D=M  \n @LCL  \n M=D   \n @R14  \n A=M  \n 0;JMP \n\n"
    
    def writeFunction(self, functionName, numLocals):
        self.funcname = functionName
        self.buffer += "(" + self.funcname + ") \n"
        for i in range(int(numLocals)):
            self.buffer += " @SP \n AM=M+1 \n A=A-1 \n M=0 \n"
        self.buffer += "\n"
            
    
    def writeArithmetic(self, command):
        if command == "add":
            self.buffer += "@SP \n AM=M-1 \n D=M \n A=A-1 \n M=M+D"
        elif command == "sub":
            self.buffer += "@SP \n AM=M-1 \n D=M \n A=A-1 \n M=M-D"
        elif command == "neg":
            self.buffer += "@SP \n A=M-1 \n M=-M"
        elif command == "eq":
            self.buffer += "@SP \n AM=M-1 \n D=M \n @SP \n AM=M-1 \n D=M-D \n @"
            self.buffer += self.filename + "_" + str(self.varcount) + " \n D;JNE \n"
            self.buffer += "D=-1 \n @" + self.filename + "_" + str(self.varcount + 1) + "\n 0;JMP \n"
            self.buffer += "(" + self.filename + "_" + str(self.varcount) + ") \n"
            self.buffer += "D=0 \n"
            self.buffer += "(" + self.filename + "_" + str(self.varcount + 1) + ") \n"
            self.buffer += "@SP \n AM=M+1 \n A=A-1 \n M=D"
            self.varcount += 2
        elif command == "gt":
            self.buffer += "@SP \n AM=M-1 \n D=M \n @SP \n AM=M-1 \n D=M-D \n @"
            self.buffer += self.filename + "_" + str(self.varcount) + " \n D;JLE \n"
            self.buffer += "D=-1 \n @" + self.filename + "_" + str(self.varcount + 1) + "\n 0;JMP \n"
            self.buffer += "(" + self.filename + "_" + str(self.varcount) + ") \n"
            self.buffer += "D=0 \n"
            self.buffer += "(" + self.filename + "_" + str(self.varcount + 1) + ") \n"
            self.buffer += "@SP \n AM=M+1 \n A=A-1 \n M=D"
            self.varcount += 2
        elif command == "lt":
            self.buffer += "@SP \n AM=M-1 \n D=M \n @SP \n AM=M-1 \n D=M-D \n @"
            self.buffer += self.filename + "_" + str(self.varcount) + " \n D;JGE \n"
            self.buffer += "D=-1 \n @" + self.filename + "_" + str(self.varcount + 1) + "\n 0;JMP \n"
            self.buffer += "(" + self.filename + "_" + str(self.varcount) + ") \n"
            self.buffer += "D=0 \n"
            self.buffer += "(" + self.filename + "_" + str(self.varcount + 1) + ") \n"
            self.buffer += "@SP \n AM=M+1 \n A=A-1 \n M=D"
            self.varcount += 2
        elif command == "and":
            self.buffer += "@SP \n AM=M-1 \n D=M \n A=A-1 \n M=M&D"
        elif command == "or":
            self.buffer += "@SP \n AM=M-1 \n D=M \n A=A-1 \n M=M|D"
        elif command == "not":
            self.buffer += "@SP \n A=M-1 \n M=!M"
            
        self.buffer += "\n\n"
    
    def writePushPop(self, command, segment, index):
        if segment == "constant":
            self.buffer += "@" + index + " \n D=A \n @SP \n A=M \n M=D \n @SP \n M=M+1"
        elif segment == "local":
            if command == "push":
                self.buffer += "@" + index + " \n D=A \n @LCL \n A=M+D \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1"
            else:
                self.buffer += "@" + index + " \n D=A \n @LCL \n M=M+D \n @SP \n AM=M-1 \n D=M \n @LCL \n A=M \n M=D \n @"
                self.buffer += index + " \n D=A \n @LCL \n M=M-D"
        elif segment == "argument":
            if command == "push":
                self.buffer += "@" + index + " \n D=A \n @ARG \n A=M+D \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1"
            else:
                self.buffer += "@" + index + " \n D=A \n @ARG \n M=M+D \n @SP \n AM=M-1 \n D=M \n @ARG \n A=M \n M=D \n @"
                self.buffer += index + " \n D=A \n @ARG \n M=M-D"
        elif segment == "this":
            if command == "push":
                self.buffer += "@" + index + " \n D=A \n @THIS \n A=M+D \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1"
            else:
                self.buffer += "@" + index + " \n D=A \n @THIS \n M=M+D \n @SP \n AM=M-1 \n D=M \n @THIS \n A=M \n M=D \n @"
                self.buffer += index + " \n D=A \n @THIS \n M=M-D"
        elif segment == "that":
            if command == "push":
                self.buffer += "@" + index + " \n D=A \n @THAT \n A=M+D \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1"
            else:
                self.buffer += "@" + index + " \n D=A \n @THAT \n M=M+D \n @SP \n AM=M-1 \n D=M \n @THAT \n A=M \n M=D \n @"
                self.buffer += index + " \n D=A \n @THAT \n M=M-D"
        elif segment == "static":
            if command == "push":
                self.buffer += "@" + self.filename + "." + index + " \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1"
            else:
                self.buffer += "@SP \n AM=M-1 \n D=M \n @" + self.filename + "." + index + " \n M=D"
        elif segment == "pointer":
            if command == "push":
                if index == "0":
                    self.buffer += "@THIS \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1"
                else:
                    self.buffer += "@THAT \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1"
            else:
                if index == "0":
                    self.buffer += "@SP \n AM=M-1 \n D=M \n @THIS \n M=D"
                else:
                    self.buffer += "@SP \n AM=M-1 \n D=M \n @THAT \n M=D"
        elif segment == "temp":
            k = str(int(index) + 5)
            if command == "push":
                self.buffer += "@" + k + " \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1"
            else:
                self.buffer += "@SP \n AM=M-1 \n D=M \n @" + k + " \n M=D"
                          
        self.buffer += "\n\n"

    def close(self):
        f = open(self.savename, 'w')
        f.write(self.buffer)
        f.close()




def getFiles(path):
    f = list()
    if not os.path.isdir(path):
        f.append(path)
        return f
    l = os.listdir(path)
    for e in l:
        if os.path.isdir(path + "/" + e):
            f = f + getFiles(path + "/" + e)
        else:
            f.append(path + "/" + e)
    return f

def translate(path):
    fname = ""
    if os.path.isdir(path):
        fname = path + "/" + path.split("/")[-1] + ".asm"
    else:
        fname = path[:-3] + ".asm"
        
    c = CodeWriter(fname)
    c.writeInit()
    
    for filename in getFiles(path):
        if filename[-3:] == ".vm":
            p = Parser(filename)
            c.setFileName(filename)
            while p.hasMoreCommands():
                p.advance()
                command = p.commandType()
                if command == Parser.C_POP or command == Parser.C_PUSH:
                    c.writePushPop(p.command(), p.arg1(), p.arg2())
                elif command == Parser.C_ARITHMETIC:
                    c.writeArithmetic(p.command())
                elif command == Parser.C_LABEL:
                    c.writeLabel(p.arg1())
                elif command == Parser.C_CALL:
                    c.writeCall(p.arg1(), p.arg2())
                elif command == Parser.C_FUNCTION:
                    c.writeFunction(p.arg1(), p.arg2())
                elif command == Parser.C_GOTO:
                    c.writeGoto(p.arg1())
                elif command == Parser.C_IF:
                    c.writeIf(p.arg1())
                elif command == Parser.C_RETURN:
                    c.writeReturn()
                
    print "\n*****\nDone!\n*****\n"
    print c.buffer
    c.close()


if __name__ == "__main__":
    Tk().withdraw()
    translate(askopenfilename())
