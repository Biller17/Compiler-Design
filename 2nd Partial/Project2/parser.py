from globalTypes import *
from lexer import *


currentToken = None

class Node:
    def __init__(self, type, childNodes = None, value =None):
        self.type = type
        self.value = value
        if childNodes :
            self.childNodes = childNodes
        else:
            self.childNodes = []




def nextToken():

    global currentToken
    currentToken = getToken()[0]
    return currentToken

def parser(imprime = True):
    AST = parseProgram()
    # AST.printTree()
    return AST


def parseProgram():
    return Node("program", parseDeclarationList())


def parseDeclarationList():
    if(currentToken == TokenType.ENDFILE):
        return []


    return([parseDeclaration()].append(parseDeclarationList()))


def parseDeclaration():
    print("declaration")
    #assign int or void
    childNodes = [parseTypeSpecifier()]
    if(nextToken() == TokenType.ID):
        childNodes.append(Node("ID"))
        if(nextToken() == TokenType.OPEN_PARENTHESIS):
            childNodes.append(parseFunDeclaration())
            return (Node("fun-declaration", childNodes))
        else:
            childNodes.append(parseVarDeclaration())
            return(Node("var-declaration", childNodes))

    return None


def parseFunDeclaration():
    childNodes = [Node("(")]
    params = parseParams()
    if(params):
        childNodes.append(params)
        global currentToken
        if(currentToken == TokenType.CLOSE_PARENTHESIS):
            childNodes.append(Node(")"))
            compoundStmt = parseCompountStmt()
            if(compoundStmt):
                childNodes.append(compoundStmt)
                return childNodes
    return None

def parseVarDeclaration():
    childNodes = []
    if(nextToken() == TokenType.SEMICOLON):
        childNodes.append(Node(";"))
        return childNodes
    elif(nextToken() == TokenType.OPEN_BRACKETS):
        childNodes.append(Node("["))
        if(nextToken() == TokenType.NUM):
            childNodes.append(Node("NUM"))
            if(nextToken() == TokenType.CLOSE_BRACKETS):
                childNodes.append(Node("]"))
                if(nextToken() == TokenType.SEMICOLON):
                    childNodes.append(Node(";"))
                    return childNodes
    return None


def parseParams():
    if(nextToken() == TokenType.CLOSE_PARENTHESIS):
        return(Node("void"))
    else:
        






# def parseFactor():
#     childNodes = []
#     if(getToken() == TokenType.OPEN_PARENTHESIS):
#

def parseTypeSpecifier():
    token = nextToken()
    if(token == TokenType.INT):
        return(Node("int"))
    elif(token == TokenType.VOID):
        return(Node("void"))
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
