'''
Created on 2 mar 2013

@author: Albin Heimerson
'''

from Tkinter import Tk
from tkFileDialog import askopenfilename
import os, re

class Tokenizer:
    
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4
        
    def __init__(self, fname):
        f = open(fname)
        self.code = ""
        self.token = ""
        self.type = ""
        for l in f.readlines():
            self.code += self.trim(l)
        f.close()
        self.trim2()

    def trim(self, line):
        commentpos = line.find("//")
        if commentpos + 1:
            line = line[0 : commentpos]
        return line
    
    def trim2(self):
        i = self.code.find("/*")
        while i + 1:
            k = self.code.find("*/")
            self.code = self.code[0:i] + self.code[k+2:]
            i = self.code.find("/*")
        self.code = re.sub('\s+', ' ', self.code)
                
    def hasMoreTokens(self):
        while len(self.code) > 0 and self.code[0] == " ":
            self.code = self.code[1:]
        return not self.code == ""

    def advance(self):
        if not self.hasMoreTokens():
            print("NO MORE TOKENS!")
            return
        
        if self.code[:5] == "class":
            self.token = "class";
            self.code = self.code[5:]
            self.type = self.KEYWORD
        elif self.code[:11] == "constructor":
            self.token = "constructor";
            self.code = self.code[11:]
            self.type = self.KEYWORD
        elif self.code[:8] == "function":
            self.token = "function";
            self.code = self.code[8:]
            self.type = self.KEYWORD
        elif self.code[:6] == "method":
            self.token = "method";
            self.code = self.code[6:]
            self.type = self.KEYWORD
        elif self.code[:5] == "field":
            self.token = "field";
            self.code = self.code[5:]
            self.type = self.KEYWORD
        elif self.code[:6] == "static":
            self.token = "static";
            self.code = self.code[6:]
            self.type = self.KEYWORD
        elif self.code[:3] == "var":
            self.token = "var";
            self.code = self.code[3:]
            self.type = self.KEYWORD
        elif self.code[:3] == "int":
            self.token = "int";
            self.code = self.code[3:]
            self.type = self.KEYWORD
        elif self.code[:4] == "char":
            self.token = "char";
            self.code = self.code[4:]
            self.type = self.KEYWORD
        elif self.code[:7] == "boolean":
            self.token = "boolean";
            self.code = self.code[7:]
            self.type = self.KEYWORD
        elif self.code[:4] == "void":
            self.token = "void";
            self.code = self.code[4:]
            self.type = self.KEYWORD
        elif self.code[:4] == "true":
            self.token = "true";
            self.code = self.code[4:]
            self.type = self.KEYWORD
        elif self.code[:5] == "false":
            self.token = "false";
            self.code = self.code[5:]
            self.type = self.KEYWORD
        elif self.code[:4] == "this":
            self.token = "this";
            self.code = self.code[4:]
            self.type = self.KEYWORD   
        elif self.code[:4] == "null":
            self.token = "null";
            self.code = self.code[4:]
            self.type = self.KEYWORD
        elif self.code[:3] == "let":
            self.token = "let";
            self.code = self.code[3:]
            self.type = self.KEYWORD
        elif self.code[:2] == "do":
            self.token = "do";
            self.code = self.code[2:]
            self.type = self.KEYWORD
        elif self.code[:2] == "if":
            self.token = "if";
            self.code = self.code[2:]
            self.type = self.KEYWORD
        elif self.code[:4] == "else":
            self.token = "else";
            self.code = self.code[4:]
            self.type = self.KEYWORD
        elif self.code[:5] == "while":
            self.token = "while";
            self.code = self.code[5:]
            self.type = self.KEYWORD
        elif self.code[:6] == "return":
            self.token = "return";
            self.code = self.code[6:]
            self.type = self.KEYWORD
        elif self.code[0] == "{":
            self.token = "{";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "}":
            self.token = "}";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "[":
            self.token = "[";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "]":
            self.token = "]";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "(":
            self.token = "(";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == ")":
            self.token = ")";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == ".":
            self.token = ".";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == ",":
            self.token = ",";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == ";":
            self.token = ";";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "+":
            self.token = "+";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "-":
            self.token = "-";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "*":
            self.token = "*";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "/":
            self.token = "/";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "&":
            self.token = "&";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "|":
            self.token = "|";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "<":
            self.token = "<";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == ">":
            self.token = ">";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "=":
            self.token = "=";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "~":
            self.token = "~";
            self.code = self.code[1:]
            self.type = self.SYMBOL
        elif self.code[0] == "\"":
            self.code = self.code[1:]
            i = self.code.find("\"")
            self.token = self.code[:i]
            self.code = self.code[i+1:]
            self.type = self.STRING_CONST
        elif "0123456789".find(self.code[0]) + 1 or (self.code[0] == "-" and "0123456789".find(self.code[1]) + 1):
            t = self.code[0]
            self.code = self.code[1:]
            while "0123456789".find(self.code[0]) + 1:
                t += self.code[0]
                self.code = self.code[1:]
            self.token = int(t)
            self.type = self.INT_CONST
        elif re.match("[A-Za-z_]", self.code[0]):
            self.token = self.code[0]
            self.code = self.code[1:]
            while re.match("[A-Za-z_0123456789]", self.code[0]):
                self.token += self.code[0]
                self.code = self.code[1:]
            self.type = self.IDENTIFIER
        else:
            print("BUGBUGBUG!!")
        
    def tokenType(self):
        return self.type
    
    def keyWord(self):
        if self.tokenType() == self.KEYWORD:
            return "<keyword> " + self.token + " </keyword>\n"
        print "ERROR WHEN ASKING FOR KEYWORD " + self.token
    
    def symbol(self):
        if self.tokenType() == self.SYMBOL:
            return "<symbol> " + self.token + " </symbol>\n"
        print "ERROR WHEN ASKING FOR SYMBOL " + self.token
    
    def identifier(self):
        if self.tokenType() == self.IDENTIFIER:
            return "<identifier> " + self.token + " </identifier>\n"
        print "ERROR WHEN ASKING FOR IDENTIFIER " + self.token
    
    def intVal(self):
        if self.tokenType() == self.INT_CONST:
            return "<integerConstant> " + str(self.token) + " </integerConstant>\n"
        print "ERROR WHEN ASKING FOR INT_CONST " + self.token
    
    def stringVal(self):
        if self.tokenType() == self.STRING_CONST:
            return "<stringConstant> " + self.token + " </stringConstant>\n"
        print "ERROR WHEN ASKING FOR STRING_CONST " + self.token
    
    def printSelf(self):
        if self.type == self.KEYWORD:
            print self.keyWord()
        elif self.type == self.SYMBOL:
            print self.symbol()
        elif self.type == self.IDENTIFIER:
            print self.identifier()
        elif self.type == self.INT_CONST:
            print self.intVal()
        elif self.type == self.STRING_CONST:
            print self.stringVal()
        
        
        
class CompilationEngine:
    def __init__(self, filein, fileout):
        self.tokenizer = Tokenizer(filein)
        self.fout = fileout
        self.text = ""
        self.indent = 1
    
    def compileClass(self):
        self.text += "<class>\n"
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.keyWord()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.identifier()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        
        while self.tokenizer.tokenType() == Tokenizer.KEYWORD:
            if self.tokenizer.token == "field" or self.tokenizer.token == "static":
                self.compileClassVarDec()
            elif self.tokenizer.token == "function" or self.tokenizer.token == "method" or self.tokenizer.token == "constructor":
                self.compileSubroutine()
            self.tokenizer.advance()
        
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.text += "</class>"
        
        print self.text + "\n"*5
        
    def compileClassVarDec(self):
        self.text += "  " * self.indent + "<classVarDec>\n"
        self.indent += 1
        
        self.text += "  " * self.indent + self.tokenizer.keyWord()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.keyWord()
        
        while not str(self.tokenizer.token) == ";":
            self.tokenizer.advance()
            self.text += "  " * self.indent + self.tokenizer.identifier()
            self.tokenizer.advance()
            self.text += "  " * self.indent + self.tokenizer.symbol()

        self.indent -= 1
        self.text += "  " * self.indent + "</classVarDec>\n"

    def compileSubroutine(self):
        self.text += "  " * self.indent + "<subroutineDec>\n"
        self.indent += 1
        
        self.text += "  " * self.indent + self.tokenizer.keyWord()
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == Tokenizer.KEYWORD:
            self.text += "  " * self.indent + self.tokenizer.keyWord()
        else:
            self.text += "  " * self.indent + self.tokenizer.identifier()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.identifier()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        
        self.compileParameterList()
        
        self.text += "  " * self.indent + self.tokenizer.symbol()
        
        self.text += "  " * self.indent + "<subroutineBody>\n"
        self.indent += 1
        
        self.tokenizer.advance()#{
        self.text += "  " * self.indent + self.tokenizer.symbol()
        
        self.tokenizer.advance()
        while str(self.tokenizer.token) == "var":
            self.compileVarDec()
            self.tokenizer.advance()
        
        self.compileStatements()
        
        print "sub " + self.tokenizer.token
        print "sub " + self.text
        
        self.text += "  " * self.indent + self.tokenizer.symbol()
        
        self.indent -= 1
        self.text += "  " * self.indent + "</subroutineBody>\n"
        
        self.indent -= 1
        self.text += "  " * self.indent + "</subroutineDec>\n"
    
    def compileParameterList(self):
        self.text += "  " * self.indent + "<parameterList>\n"
        self.indent += 1
        
        if self.tokenizer.tokenType() == Tokenizer.SYMBOL:
            self.indent -= 1
            self.text += "  " * self.indent + "</parameterList>\n"
            return 
                
        self.text += "  " * self.indent + self.tokenizer.keyWord()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.identifier()
        self.tokenizer.advance()
        while self.tokenizer.token == ",":
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
            self.text += "  " * self.indent + self.tokenizer.keyWord()
            self.tokenizer.advance()
            self.text += "  " * self.indent + self.tokenizer.identifier()
            self.tokenizer.advance()
        self.indent -= 1
        self.text += "  " * self.indent + "</parameterList>\n"
    
    def compileVarDec(self):
        self.text += "  " * self.indent + "<varDec>\n"
        self.indent += 1
        
        self.text += "  " * self.indent + self.tokenizer.keyWord()
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == Tokenizer.KEYWORD:
            self.text += "  " * self.indent + self.tokenizer.keyWord()
        else:    
            self.text += "  " * self.indent + self.tokenizer.identifier()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.identifier()
        self.tokenizer.advance()
        while self.tokenizer.token == ",":
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
            self.text += "  " * self.indent + self.tokenizer.identifier()
            self.tokenizer.advance()
        
        self.text += "  " * self.indent + self.tokenizer.symbol()

        self.indent -= 1
        self.text += "  " * self.indent + "</varDec>\n"
    
    def compileStatements(self):
        self.text += "  " * self.indent + "<statements>\n"
        self.indent += 1
        
        while self.tokenizer.tokenType() == Tokenizer.KEYWORD:
            if self.tokenizer.token == "let":
                self.compileLet()
            elif self.tokenizer.token == "do":
                self.compileDo()
            elif self.tokenizer.token == "while":
                self.compileWhile()
            elif self.tokenizer.token == "return":
                self.compileReturn()
            elif self.tokenizer.token == "if":
                self.compileIf()
            
        self.indent -= 1
        self.text += "  " * self.indent + "</statements>\n"
    
    def compileDo(self):
        self.text += "  " * self.indent + "<doStatement>"
        self.indent += 1
        
        self.text += "  " * self.indent + self.tokenizer.keyWord()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.identifier()
        self.tokenizer.advance()
        
        if self.tokenizer.token == "(":
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
            
            self.text += "  " * self.indent + "<expressionList>"
            self.indent += 1
            
            self.compileExpression()
            self.tokenizer.advance()
            
            while self.tokenizer.token == ",":
                self.text += "  " * self.indent + self.tokenizer.symbol()
                self.tokenizer.advance()
                self.compileExpression()
                self.tokenizer.advance()
                
            self.indent -= 1
            self.text += "  " * self.indent + "</expressionList>"
            
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
        elif self.tokenizer.token == ".":
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
            self.text += "  " * self.indent + self.tokenizer.identifier()
            self.tokenizer.advance()
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
            
            self.text += "  " * self.indent + "<expressionList>"
            self.indent += 1
            
            self.compileExpression()
            self.tokenizer.advance()
            
            while self.tokenizer.token == ",":
                self.text += "  " * self.indent + self.tokenizer.symbol()
                self.tokenizer.advance()
                self.compileExpression()
                self.tokenizer.advance()
                
            self.indent -= 1
            self.text += "  " * self.indent + "</expressionList>"
            
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
                    
        self.indent -= 1
        self.text += "  " * self.indent + "</doStatement>"
    
    def compileLet(self):
        self.text += "  " * self.indent + "<letStatement>\n"
        self.indent += 1
        
        self.text += "  " * self.indent + self.tokenizer.keyWord()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.identifier()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        
        self.compileExpression()
                
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        
        self.indent -= 1
        self.text += "  " * self.indent + "</letStatement>\n"
    
    def compileWhile(self):
        self.text += "  " * self.indent + "<whileStatement>\n"
        self.indent += 1
        
        self.text += "  " * self.indent + self.tokenizer.keyWord()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        self.compileExpression()
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        
        self.compileStatements()
        
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        
        self.indent -= 1
        self.text += "  " * self.indent + "</whileStatement>\n"
    
    def compileReturn(self):
        self.text += "  " * self.indent + "<returnStatement>\n"
        self.indent += 1
        
        self.text += "  " * self.indent + self.tokenizer.keyWord()
        self.tokenizer.advance()
        
        self.compileExpression()
        
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        
        self.indent -= 1
        self.text += "  " * self.indent + "</returnStatement>\n"
    
    def compileIf(self):
        self.text += "  " * self.indent + "<ifStatement>\n"
        self.indent += 1
        
        self.text += "  " * self.indent + self.tokenizer.keyWord()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        self.compileExpression()
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        
        self.compileStatements()
        
        self.text += "  " * self.indent + self.tokenizer.symbol()
        self.tokenizer.advance()
        
        if self.tokenizer.token == "else":
            self.text += "  " * self.indent + self.tokenizer.keyWord()
            self.tokenizer.advance()
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compileStatements()
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
        
        self.indent -= 1
        self.text += "  " * self.indent + "</ifStatement>\n"
    
    def compileExpression(self):
        self.text += "  " * self.indent + "<expression>\n"
        self.indent += 1
        self.compileTerm()
        
        while self.tokenizer.token == "-" or self.tokenizer.token == "+" or self.tokenizer.token == "*" or self.tokenizer.token == "/" or self.tokenizer.token == "&" or self.tokenizer.token == "|" or self.tokenizer.token == "<" or self.tokenizer.token == ">" or self.tokenizer.token == "=": 
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compileTerm()
        
        
        self.indent -= 1
        self.text += "  " * self.indent + "</expression>\n"
    
    def compileTerm(self):
        self.text += "  " * self.indent + "<term>\n"
        self.indent += 1
        
        if self.tokenizer.tokenType() == Tokenizer.INT_CONST:
            self.text += "  " * self.indent + self.tokenizer.intVal()
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == Tokenizer.STRING_CONST:
            self.text += "  " * self.indent + self.tokenizer.stringVal()
            self.tokenizer.advance()
        elif self.tokenizer.token == "(":
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.compileExpression()
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
        elif self.tokenizer.token == "-" or self.tokenizer.token == "~":
            self.text += "  " * self.indent + self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compileTerm()
        elif self.tokenizer.token == "true" or self.tokenizer.token == "false" or  self.tokenizer.token == "null" or  self.tokenizer.token == "this":
            self.text += "  " * self.indent + self.tokenizer.keyWord()
        elif self.tokenizer.tokenType() == Tokenizer.IDENTIFIER:
            self.text += "  " * self.indent + self.tokenizer.identifier()
            self.tokenizer.advance()
            if self.tokenizer.token == "[":
                self.text += "  " * self.indent + self.tokenizer.symbol()
                self.tokenizer.advance()
                self.compileExpression()
                self.text += "  " * self.indent + self.tokenizer.symbol()
                self.tokenizer.advance()
            elif self.tokenizer.token == "(":
                self.text += "  " * self.indent + self.tokenizer.symbol()
                self.tokenizer.advance()
                
                self.text += "  " * self.indent + "<expressionList>\n"
                self.indent += 1
                
                self.compileExpression()
                self.tokenizer.advance()
                
                while self.tokenizer.token == ",":
                    self.text += "  " * self.indent + self.tokenizer.symbol()
                    self.tokenizer.advance()
                    self.compileExpression()
                    self.tokenizer.advance()
                    
                self.indent -= 1
                self.text += "  " * self.indent + "</expressionList>\n"
                
                self.text += "  " * self.indent + self.tokenizer.symbol()
                self.tokenizer.advance()
            elif self.tokenizer.token == ".":
                self.text += "  " * self.indent + self.tokenizer.symbol()
                self.tokenizer.advance()
                self.text += "  " * self.indent + self.tokenizer.identifier()
                self.tokenizer.advance()
                self.text += "  " * self.indent + self.tokenizer.symbol()
                self.tokenizer.advance()
                
                self.text += "  " * self.indent + "<expressionList>\n"
                self.indent += 1
                
                self.compileExpression()
                
                while self.tokenizer.token == ",":
                    self.text += "  " * self.indent + self.tokenizer.symbol() 
                    self.tokenizer.advance()
                    self.compileExpression()
                    self.tokenizer.advance()
                    
                self.indent -= 1
                self.text += "  " * self.indent + "</expressionList>\n"
                
                
                self.text += "  " * self.indent + self.tokenizer.symbol()
                self.tokenizer.advance()
            
        self.indent -= 1
        self.text += "  " * self.indent + "</term>\n"


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
    for filename in getFiles(path):
        if filename[-5:] == ".jack":
            c = CompilationEngine(filename, filename[-4:] + "vm")
            c.compileClass()

if __name__ == "__main__":
    Tk().withdraw()
    translate(askopenfilename())


        
    