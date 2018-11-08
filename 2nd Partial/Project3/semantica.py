from parser import *


#programa analizador de semantica Adrian Biller A01018940


class ScopeNode:
    def __init__(self, level):
        self.level = level
        self.symbolTable = []
        self.childScope = []


    def generateSymbolTable():
        

    def printTree(self, level = 0):
        print((level*3)*'__', self.type)
        # print(self.childNodes)
        if(self.childNodes != []):
            if(type(self.childNodes) == Node):
                self.childNodes.printTree()
            else:
                for i in range(len(self.childNodes)):
                    if(type(self.childNodes[i]) == list):
                        for j in range(len(self.childNodes[i])):
                            self.childNodes[i][j].printTree()
                    else:
                        self.childNodes[i].printTree(level+1)



def tabla( AST, imprime = True):
    return 0



def semantica(AST, imprime = True):
    return 0

if __name__ == '__main__':
    print("Analizador semantico Adrian Biller A01018940")
    AST = parser(False)
    tabla = tabla(AST)
