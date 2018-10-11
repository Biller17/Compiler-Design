from globalTypes import *
from lexer import *


currentToken = None

class Node:
    def __init__(self, type, childNodes, value):
        self.type = type
        self.value = value
        if childNodes :
            self.childNodes = childNodes
        else:
            self.childNodes = []




def nextToken():
    currentToken = getToken()
    return currentToken

def parser(imprime = True):
    AST = parseProgram()
    # AST.printTree()
    return AST


def parseProgram():
    getToken()
    return Node("program", parseDeclarationList())


def parseDeclarationList():
    if(currentToken == TokenType.ENDFILE):
        return []

    return([parseDeclaration()].append(parseDeclarationList()))


def parseDeclaration():
    if(parseTypeSpecifier()):
        
# def parseFactor():
#     childNodes = []
#     if(getToken() == TokenType.OPEN_PARENTHESIS):
#

def parseTypeSpecifier():
    if(nextToken() == TokenType.INT):
        return(Node("int"))
    elif(nextToken() == TokenType.VOID):
        return(Node("void"))
    else:
        return None

def parseCall():
    childNodes = []
    if(nextToken() == TokenType.ID):
        childNodes.append(Node("ID"))
        if(nextToken() == TokenType.OPEN_PARENTHESIS):
            childNodes.append(Node("("))
            args = parseArgs()
            childNodes.append(args)
            if(args):
                childNodes.append(Node(")"))
                return(Node("call", childNodes))
    return None


# def parseArgs():
#     if(nextToken() == TokenType.CLOSE_PARENTHESIS):
#         return(Node("empty"))
#     else:
#         #checking list
#         while()
#
# def parseArgList():
#



if __name__ == '__main__':
    print("starting parser")
    f = open('sample.txt', 'r')
    programa = f.read()     # lee todo el archivo a compilar
    progLong = len(programa)   # longitud original del programa
    programa = programa + '$'   # agregar un caracter $ que represente EOF
    posicion = 0 # posición del caracter actual del string
    # función para pasar los valores iniciales de las variables globales
    globales(programa, posicion, progLong)
    AST = parser(True)
