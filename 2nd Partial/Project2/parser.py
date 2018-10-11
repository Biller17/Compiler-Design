from globalTypes import *
from lexer import *




class Node:
    def __init__(self, type, childNodes, value):
        self.type = type
        self.value = value
        if childNodes :
            self.childNodes = childNodes
        else:
            self.childNodes = []




def parser(imprime = True):
    AST = parseProgram()
    # AST.printTree()
    return AST


    # while (token != TokenType.ENDFILE):
    #     token, tokenString = getToken(True)



def parseProgram():
    return Node("program","", parseDeclarationList())


def parseDeclarationList():


def parseFactor():
    childNodes = []
    if(getToken() == TokenType.OPEN_PARENTHESIS):


def parseCall():
    childNodes = []
    if(getToken() == TokenType.ID):
        childNodes.append(Node("ID"))
        if(getToken() == TokenType.OPEN_PARENTHESIS):
            childNodes.append(Node("("))
            args = parseArgs()
            childNodes.append(args)
            if(args):
                childNodes.append(Node(")"))
                return(Node("call", childNodes))
    return None


def parseArgs():
    if(getToken() == TokenType.CLOSE_PARENTHESIS):
        return(Node("empty"))
    args = parseArgList()
    if(args):
        return(Node("arg-list"))

def parseArgList():




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
