from parser import *


#programa analizador de semantica Adrian Biller A01018940


class Scope:
    def __init__(self, level):
        self.level = level
        self.symbolTable = {}
        self.childScopes = []





def generateST(ast, table, currentScope, scopeLevel = 0):
    '''Checking if node is
    variable definition
    variable definition (array)
    function definition'''
    # print((scopeLevel*3)*'__', ast.type, ast.value)
    if(ast.childNodes != []):
        for i in range(len(ast.childNodes)):
            if(type(ast.childNodes[i]) == list):
                for j in range(len(ast.childNodes[i])):
                    generateST(ast.childNodes[i][j], table,currentScope, scopeLevel +1)
            else:
                if(ast.childNodes[i].type == "fun-declaration"):
                    print("******************************************            fun")
                    #get function type id and params into symbolTable
                    getFunctionProps(ast.childNodes[i])
                    #create new scope and add function type, id and params
                    #use function recursively and check in new scope

                elif(ast.childNodes[i].type == "var-declaration"):
                    print("ñññññññññññññññññññññññññññññññññññññññññ             var")
                    #get all variables declared and put them in the current scope
                generateST(ast.childNodes[i],table,currentScope, scopeLevel+1)



def getFunctionProps(node):
    #function type
    print("function type", node.childNodes[0].type)
    #function id
    print("function id", node.childNodes[1].type)


    #getting params
    print("param", node.childNodes[2][1].childNodes[0].type)




def tabla( AST, imprime = True):
    initialScope = Scope(0)
    dict = {}
    generateST(AST, dict, initialScope)
    return 0




def semantica(AST, imprime = True):
    return 0

if __name__ == '__main__':
    print("Analizador semantico Adrian Biller A01018940")
    AST = parser(False)
    tabla = tabla(AST)
