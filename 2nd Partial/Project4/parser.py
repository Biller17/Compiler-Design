from globalTypes import *
from lexer import *

tokenList = []
tokenListValues = []
currentToken = -1

class Node:
    def __init__(self, type, childNodes = None, value =None):
        self.type = type
        self.value = value
        if childNodes :
            self.childNodes = childNodes
        else:
            self.childNodes = []

    def printTree(self, level = 0):
        print((level*3)*'__', self.type)
        # print(self.childNodes)
        if(self.childNodes != []):
            if(type(self.childNodes) == Node):
                self.childNodes.printTree(level+1)
            else:
                for i in range(len(self.childNodes)):
                    if(type(self.childNodes[i]) == list):
                        for j in range(len(self.childNodes[i])):
                            self.childNodes[i][j].printTree(level+1)
                    else:
                        self.childNodes[i].printTree(level+1)


def nextToken():
    global currentToken
    currentToken += 1
    return tokenList[currentToken]

    # global currentToken
    # currentToken = getToken()[0]
    # return currentToken

def getLastToken():
    return tokenList[currentToken]

def parser(imprime = True):
    # print(tokenList)
    initialConf()
    AST = parseProgram()
    if(imprime == True):
        AST.printTree(0)
    return AST


def parseProgram():
    return Node("program", [parseDeclarationList()])


def parseDeclarationList():
    # if(tokenList[currentToken + 1] == TokenType.ENDFILE):
    #     return []
    # for i in range(len(tokenList)):
    #     print(tokenList[i])
    childNodes = []
    while(True):
        if(tokenList[currentToken + 1] == TokenType.ENDFILE):
            childNodes.append(Node("endfile"))
            break
        else:
            dc =  parseDeclaration()
            if(dc):
                childNodes.append(dc)

    return(Node("declaration-list", childNodes))
    # return([parseDeclaration()].append(parseDeclarationList()))


def parseDeclaration():
    #assign int or void
    type = parseTypeSpecifier()
    childNodes = []
    if(type):
        childNodes.append(type)
        if(nextToken() == TokenType.ID):
            childNodes.append(Node("ID", [], tokenListValues[currentToken]))
            if(nextToken() == TokenType.OPEN_PARENTHESIS):
                fun = parseFunDeclaration()
                if(fun):
                    childNodes.append(fun)
                    return (Node("fun-declaration", childNodes))
            else:
                var = parseVarDeclaration()
                if(var):
                    childNodes.append(var)
                    return(Node("var-declaration", childNodes))

    return None


def parseVarDeclaration():
    childNodes = []
    if(nextToken() == TokenType.SEMICOLON):
        childNodes.append(Node(";"))
        return childNodes
    elif(nextToken() == TokenType.OPEN_BRACKETS):
        childNodes.append(Node("["))
        if(nextToken() == TokenType.NUM):
            childNodes.append(Node("NUM",[], tokenListValues[currentToken]))
            if(nextToken() == TokenType.CLOSE_BRACKETS):
                childNodes.append(Node("]"))
                if(nextToken() == TokenType.SEMICOLON):
                    childNodes.append(Node(";"))
                    return childNodes
    return None


def parseTypeSpecifier():
    token = nextToken()
    if(token == TokenType.INT):
        return(Node("int"))
    elif(token == TokenType.VOID):
        return(Node("void"))
    return None


def parseFunDeclaration():
    # print("función", currentToken)
    # childNodes = [Node("(")]
    childNodes = []
    params = parseParams()
    # print("_________",currentToken,"__________", tokenList[currentToken+1])
    if(params):
        childNodes.append(params)
        # childNodes.append(Node(")"))
        compoundStmt = parseCompoundStmt()
        if(compoundStmt):
            childNodes.append(compoundStmt)
            return childNodes
    return None




def parseParams():
    childNodes = [parseParam()]
    if(childNodes[0] == None):
        return None
    while(True):
        if(getLastToken() == TokenType.COMMA):
            # childNodes.append(Node(","))
            # print("_________",currentToken,"__________", tokenList[currentToken])
            param = parseParam()
            if(param):
                childNodes.append(param)
        if(getLastToken() == TokenType.CLOSE_PARENTHESIS):
            return(Node("params", childNodes))



def parseParam():
    childNodes = []
    typeSpecifier = parseTypeSpecifier()
    if(typeSpecifier):
        if(typeSpecifier.type == "void"):
            # childNodes.append(typeSpecifier)
            if(nextToken() == TokenType.CLOSE_PARENTHESIS):
                return(Node("void"))
        childNodes.append(typeSpecifier)
        if(nextToken() == TokenType.ID):
            childNodes.append(Node("ID", [], tokenListValues[currentToken]))
            if(nextToken() == TokenType.OPEN_BRACKETS):
                childNodes.append(Node("["))
                if(nextToken() == TokenType.CLOSE_BRACKETS):
                    childNodes.append(Node("]"))
                    return(Node("param", childNodes))
            elif(getLastToken() == TokenType.COMMA):
                return(Node("param", childNodes))
            elif(getLastToken() == TokenType.CLOSE_PARENTHESIS):
                return(Node("param", childNodes))
    return None



def parseCompoundStmt():
    childNodes = []
    if(nextToken() == TokenType.OPEN_KEYS):
        childNodes.append(Node("{"))
        local = parseLocalDeclarations()
        if(local):
            childNodes.append(local)
            statement = parseStatementList()

            if(statement):
                childNodes.append(statement)
                if(nextToken() == TokenType.CLOSE_KEYS):
                    childNodes.append(Node("}"))
                    return(Node("compound-stmt", childNodes))
    return None

def parseLocalDeclarations():
    global currentToken
    currentPos = currentToken
    childNodes = []
    while(True):
        tmp = parseLocalVarDeclaration()
        if(tmp):
            childNodes.append(tmp)
            currentPos = currentToken
        else:
            currentToken = currentPos
            break
    if(len(childNodes) > 0):
        return(Node("localDeclarations", childNodes))
    else:
        return(Node("empty"))

def parseLocalVarDeclaration():
    childNodes =[]
    type = parseTypeSpecifier()
    if(type):
        childNodes.append(type)
        if(nextToken() == TokenType.ID):
            childNodes.append(Node("ID", [], tokenListValues[currentToken]))
            tmp = parseVarDeclaration()
            if(tmp):
                childNodes.append(tmp)
                return(Node("var-declaration", childNodes))

def parseStatementList():
    global currentToken
    stmt = []
    tmp = parseStatement()
    while(tmp):
        stmt.append(tmp)
        tmp = parseStatement()

    # currentToken -= 1
    if(len(stmt) > 0):
        return(Node("statement-list", stmt))
    else:
        return(Node("empty"))



def parseStatement():
    global currentToken
    currentPos = currentToken
    childNodes = []
    exp = parseExpressionStmt()
    if(exp):
        return (Node("statement", exp))
    currentToken = currentPos
    exp = parseCompoundStmt()
    if(exp):
        return(Node("statement", exp))
    currentToken = currentPos
    exp = parseSelectionStmt()
    if(exp):
        return(Node("statement", exp))
    currentToken = currentPos
    exp = parseIterationStmt()
    if(exp):
        return(Node("statement", exp))
    currentToken = currentPos
    exp = parseReturnStmt()
    if(exp):
        childNodes.append(exp)
        return(Node("statement", childNodes))
    currentToken = currentPos

    return None




def parseExpressionStmt():
    global currentToken
    childNodes = []
    if(nextToken() == TokenType.SEMICOLON):
        return([Node(";")])
    else:
        currentToken -= 1
        exp = parseExpression()
        if(exp):
            childNodes.append([exp, Node(";")])
            return([Node("expression-stmt", childNodes)])
    return None

def parseSelectionStmt():
    global currentToken
    childNodes = []
    if(nextToken() == TokenType.IF):
        childNodes.append(Node("if"))
        if(nextToken() == TokenType.OPEN_PARENTHESIS):
            # childNodes.append(Node("("))
            exp = parseExpression()
            if(exp):
                childNodes.append(exp)
                if(nextToken() == TokenType.CLOSE_PARENTHESIS):
                    # childNodes.append(Node(")"))
                    stmt = parseStatement()
                    if(stmt):
                        childNodes.append(stmt)
                        if(nextToken() == TokenType.ELSE):
                            childNodes.append(Node("else"))
                            stmt = parseStatement()
                            if(stmt):
                                childNodes.append(stmt)
                                return([Node("selection-stmt", childNodes)])
                        else:

                            currentToken -= 1
                            return([Node("selection-stmt", childNodes)])
    return None


def parseIterationStmt():
    childNodes = []
    if(nextToken() == TokenType.WHILE):
        childNodes.append(Node("while"))
        if(nextToken() == TokenType.OPEN_PARENTHESIS):
            # childNodes.append(Node("("))
            exp = parseExpression()
            if(exp):
                childNodes.append(exp)
                if(nextToken() == TokenType.CLOSE_PARENTHESIS):
                    # childNodes.append(Node(")"))
                    stmt = parseStatement()
                    if(stmt):
                        childNodes.append(stmt)
                        return(Node("iteration-stmt", childNodes))
    return None

def parseReturnStmt():
    global currentToken
    childNodes = []
    if(nextToken() == TokenType.RETURN):
        childNodes.append(Node("return"))
        if(nextToken() ==  TokenType.SEMICOLON):
            childNodes.append(Node(";"))
            return(Node("return-stmt", childNodes))
        else:

            currentToken -= 1
            exp = parseExpression()

            if(exp):
                if(nextToken() == TokenType.SEMICOLON):
                    childNodes.append([exp, Node(";")])
                    return(Node("return-stmt", childNodes))
    return None

def parseExpression():
    childNodes = []
    global currentToken
    currentPos = currentToken
    var = parseVar()
    if(var):
        childNodes.append(var)
        if(nextToken() == TokenType.ASSIGNMENT):
            childNodes.append(Node("="))
            exp = parseExpression()
            if(exp):
                childNodes.append(exp)
                return(Node("expression", childNodes))

    currentToken = currentPos
    exp = parseSimpleExpression()
    if(exp):
        childNodes.append(exp)
        return(Node("expression", childNodes))
    return None

def parseVar():
    global currentToken
    childNodes = []
    if(nextToken() == TokenType.ID):
        childNodes.append(Node("ID", [], tokenListValues[currentToken]))
        if(nextToken() == TokenType.OPEN_BRACKETS):
            childNodes.append(Node("["))
            exp = parseExpression()
            if(exp):
                childNodes.append(exp)
                if(nextToken() == TokenType.CLOSE_BRACKETS):
                    childNodes.append(Node("]"))
                    return(Node("var", childNodes))
        else:
            currentToken -= 1
            return(Node("var", childNodes))
    return None

def parseSimpleExpression():
    childNodes = []
    global currentToken
    currentPos = currentToken
    add = parseAdditiveExp()
    if(add):
        childNodes.append(add)
        currentPos = currentToken
        relop = parseRelop()
        if(relop):
            childNodes.append(relop)
            add = parseAdditiveExp()
            if(add):
                childNodes.append(add)
                return(Node("simple-expression", childNodes))
        else:
            currentToken = currentPos
            return(Node("simple-expression", childNodes))

    return None


def parseRelop():
    global currentToken
    if(nextToken() == TokenType.LESS_THAN_EQUAL_TO):
        return(Node("<="))
    elif(getLastToken() == TokenType.LESS_THAN):
        return(Node("<"))
    elif(getLastToken() == TokenType.GREATER_THAN):
        return(Node(">"))
    elif(getLastToken() == TokenType.GREATER_THAN_EQUAL_TO):
        return(Node(">="))
    elif(getLastToken() == TokenType.EQUAL):
        return(Node("=="))
    elif(getLastToken() == TokenType.DIFFERENT):
        return(Node("!="))
    currentToken -= 1
    return None

def parseAdditiveExp():
    global currentToken
    currentPos = currentToken
    childNodes = []
    term = parseTerm()
    if(term):
        currentPos = currentToken
        childNodes.append(term)
        add = parseAdditiveExpP()
        if(add):
            childNodes.append(add)
            return(Node("additive-expression", childNodes))
        else:
            currentToken = currentPos
            return(Node("additive-expression", childNodes))
    return None


def parseAdditiveExpP():
    global currentToken
    childNodes = []
    addop = parseAddOp()
    if(addop):
        childNodes.append(addop)
        term = parseTerm()
        if(term):
            childNodes.append(term)
            currentPos = currentToken
            add = parseAdditiveExpP()
            if(add):
                childNodes.append(add)
                return(Node("additive-expression",childNodes))
            else:
                currentToken = currentPos
                return(Node("additive-expression",childNodes))
    else:
        return None


def parseAddOp():
    if(nextToken() == TokenType.PLUS):
        return(Node("+"))
    elif(getLastToken() == TokenType.MINUS):
        return(Node("-"))
    return None

def parseTerm():
    global currentToken
    currentPos = currentToken
    childNodes = []
    factor = parseFactor()
    if(factor):
        childNodes.append(factor)
        return(Node("term", childNodes))
    currentToken = currentPos
    term = parseTermP()
    if(term):
        childNodes.append(term)
        return(Node("term", childNodes))
    return None

def parseTermP():
    global currentToken
    childNodes = []
    mulop = parseMulop()
    if(mulop):
        childNodes.append(mulop)

        factor = parseFactor()
        if(factor):
            childNodes.append(factor)
            currentPos = currentToken
            term =  parseTermP()
            if(term):
                childNodes.append(term)
                return(Node("term-p", childNodes))
            currentToken = currentPos
            return(Node("term-p", childNodes))
    return None


def parseMulop():
    if(nextToken() == TokenType.ASTERISK):
        return(Node("*"))

    elif(tokenList[currentToken] == TokenType.SLASH):
        return(Node("/"))
    return None

def parseFactor():
    global currentToken
    childNodes = []
    currentPos = currentToken
    if(nextToken() == TokenType.OPEN_PARENTHESIS):
        # childNodes.append(Node("("))
        exp = parseExpression()
        if(exp):
            childNodes.append(exp)
            if(nextToken() == TokenType.CLOSE_PARENTHESIS):
                # childNodes.append(Node(")"))
                return(Node("factor", childNodes))
    elif(getLastToken() == TokenType.NUM):
        childNodes.append(Node("num", [], tokenListValues[currentToken]))
        return(Node("factor", childNodes))

    currentToken = currentPos
    call = parseCall()
    if(call):
        # print(currentToken)#--------------------------------------------------------------------------------
        childNodes.append(call)
        return(Node("factor", childNodes))

    currentToken = currentPos
    var = parseVar()
    if(var):
        childNodes.append(var)
        return(Node("factor", childNodes))

    return None

def parseCall():
    childNodes = []
    if(nextToken() == TokenType.ID):
        childNodes.append(Node("ID", [], tokenListValues[currentToken]))
        if(nextToken() == TokenType.OPEN_PARENTHESIS):
            # childNodes.append(Node("("))
            args = parseArgs()
            childNodes.append(args)
            if(args):
                # childNodes.append(Node(")"))
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


def parseArgs():
    global currentToken
    if(nextToken() == TokenType.CLOSE_PARENTHESIS):
        return(Node("empty"))

    currentToken -= 1
    arglist = parseArgList()
    if(arglist):
        return(Node("args", arglist))




def parseArgList():
    childNodes = [parseExpression()]
    while(True):
        if(nextToken() == TokenType.COMMA):
            # childNodes.append(Node(","))
            childNodes.append(parseExpression())
        elif(getLastToken() == TokenType.CLOSE_PARENTHESIS):
            return childNodes




def initialConf():
    print("starting parser")
    f = open('sample.txt', 'r')
    programa = f.read()     # lee todo el archivo a compilar
    progLong = len(programa)   # longitud original del programa
    programa = programa + '$'   # agregar un caracter $ que represente EOF
    posicion = 0 # posición del caracter actual del string
    # función para pasar los valores iniciales de las variables globales
    globales(programa, posicion, progLong)
    token = None
    while (True):
        token = getToken()
        tokenList.append(token[0])
        tokenListValues.append(token[1])
        if(token[0] == TokenType.ENDFILE):
            break



if __name__ == '__main__':
    AST = parser(True)
