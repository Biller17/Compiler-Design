from parser import *


#programa analizador de semantica Adrian Biller A01018940


class Scope:
    def __init__(self, level, parent):
        self.level = level
        self.symbolTable = {}
        self.childScopes = []
        self.parent = parent

    def printTable(self):
        print("LEVEL ", self.level)
        print(self.symbolTable)
        if(self.childScopes != []):
            for i in range(len(self.childScopes)):
                self.childScopes[i].printTable()




def generateST(ast, currentScope):
    '''Checking if node is
    variable definition
    variable definition (array)
    function definition'''
    # print((scopeLevel*3)*'__', ast.type, ast.value)
    if type(ast.childNodes) == list:
        for i in range(len(ast.childNodes)):
            if(type(ast.childNodes[i]) == list):
                for j in range(len(ast.childNodes[i])):
                    generateST(ast.childNodes[i][j],currentScope)
            # if type(ast.childNodes[i]) == list:
            #     generateST(ast.childNodes[i] , currentScope)
            else:
                if(ast.childNodes[i].type == "localDeclarations"):
                    # print("ñññññññññññññññññññññññññññññññññññññññññ             var")
                    # print(ast.childNodes[i].childNodes[1].value)
                    #get all variables declared and put them in the current scope
                    currentScope.symbolTable = getVarDeclaration(ast.childNodes[i], currentScope.symbolTable)

                elif(ast.childNodes[i].type == "fun-declaration"):
                    # print("******************************************            fun")
                    #get function type id and params into symbolTable
                    currentScope.symbolTable = getFunctionProps(ast.childNodes[i], currentScope.symbolTable)
                    #create new scope and add function type, id and params
                    #use function recursively and check in new scope
                    # print(table)
                    #setting table in scope
                    newScope = Scope(currentScope.level + 1, currentScope)
                    currentScope.childScopes.append(newScope)
                    newScope.symbolTable = getFunctionProps(ast.childNodes[i], newScope.symbolTable)
                    generateST(ast.childNodes[i], newScope)

                generateST(ast.childNodes[i],currentScope)
    return currentScope






def getVarDeclaration(node, table):
    for i in range(len(node.childNodes)):
        table[(node.childNodes[i].childNodes[1].value)] = node.childNodes[i].childNodes[0].type

    return table





def getFunctionProps(node, table):
    # print("param", node.childNodes[2][1].childNodes)
    params = getParams(node.childNodes[2][1].childNodes)
    table[node.childNodes[1].value] = [node.childNodes[0].type, params]
    # print(table)
    #function type
    # print("function type", node.childNodes[0].type)
    # #function id
    # print("function id", node.childNodes[1].type)


    return table


def getParams(params):
    paramArr = []
    for i in range(len(params)):
        # print(params[i].type)
        if(params[i].type == "param"):
            # print(params[i].childNodes[0].type)
            paramArr.append(params[i].childNodes[0].type)
        elif(params[i].type =="void"):
            paramArr.append("void")
    return paramArr



def tabla( AST, imprime = True):
    initialScope = Scope(0, None)
    return generateST(AST, initialScope)



def semanticAnalizer(ast, scopes, scopeIndex):
    if type(ast.childNodes) == list:
        for i in range(len(ast.childNodes)):
            if type(ast.childNodes[i]) == list:
                for j in range(len(ast.childNodes[i])):
                    semanticAnalizer(ast.childNodes[i][j],scopes, scopeIndex)
            # if type(ast.childNodes[i]) == list:
            #     generateST(ast.childNodes[i] , currentScope)
            else:
                # print(ast.childNodes[i].type)
                if(ast.childNodes[i].type == "expression"):
                    # print(ast.childNodes[i].childNodes[1].value)
                    #get all variables declared and put them in the current scope
                    if not typeCheck(ast.childNodes[i], scopes[scopeIndex]):
                        print("error")
                        return 0
                elif(ast.childNodes[i].type == "fun-declaration"):
                    scopeIndex +=1
                semanticAnalizer(ast.childNodes[i],scopes, scopeIndex)
    return 0




def typeCheck(nodes, scope):
    #id de primer valor
    if nodes.childNodes[1].childNodes[0].type == 'additive-expression':
        if nodes.childNodes[1].childNodes[0].childNodes[0].childNodes[0].childNodes[0].type  == 'call':
            if nodes.childNodes[1].childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0].value != 'input' and nodes.childNodes[1].childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0].value!= 'output':
                try:
                    if scope.symbolTable[nodes.childNodes[1].childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0].value]:
                        return True
                except Exception as e:
                    return True
    # print(nodes.childNodes[0].childNodes[0].value)
    # print(nodes.childNodes[1].childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[0].value)
    return True

def semantica(AST, imprime = True):
    ST = tabla(AST)
    scopes = []
    if imprime:
        ST.printTable()
    scopes = getScopeArray(ST, [])
    semanticAnalizer(AST, scopes, 0)
    return 0

def getScopeArray(scope, scopearr):
    scopearr.append(scope)
    if len(scope.childScopes) > 0:
        for i in range(len(scope.childScopes)):
            getScopeArray(scope.childScopes[i], scopearr)
    return scopearr

def sem():
    print("Analizador semantico Adrian Biller A01018940")
    AST = parser(False)
    semantica(AST)
    return AST
