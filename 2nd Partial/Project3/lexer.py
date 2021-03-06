from globalTypes import *

#Proyecto 1 lexer Adrian Biller A01018940


def globales(prog, pos, long):
    #string del programa entero
    global programa
    #posicion del cursor en el programa que se esta analizando
    global posicion
    #longitud del programa analizando
    global progLong
    programa = prog
    posicion = pos
    progLong = long


#function that returns the tuple value and prints token depending on parameters
#if it receives an error then calls print error function
def printToken(TokenType, TokenVal, imprime, tokenLen, errorMSG = "", errorpos = 0):
    global posicion
    posicion += tokenLen
    if(TokenVal == 'error'):
        printError(errorpos, errorMSG)
    if(imprime):
        print("(", TokenType, ",", TokenVal, ")")
    return(TokenType, TokenVal)


#function that receives a token value and determines if it's a reserved word or a normal id
def checkIfKeyWord(token, imprime, idsize):
    if(token == 'else'):
        return (printToken(TokenType.ELSE, token, imprime, idsize))
    elif(token == 'if'):
        return (printToken(TokenType.IF, token, imprime, idsize))
    elif(token == 'int'):
        return (printToken(TokenType.INT, token, imprime, idsize))
    elif(token == 'return'):
        return (printToken(TokenType.RETURN, token, imprime, idsize))
    elif(token == 'void'):
        return (printToken(TokenType.VOID, token, imprime, idsize))
    elif(token == 'while'):
        return (printToken(TokenType.WHILE, token, imprime, idsize))
    else:
        return(printToken(TokenType.ID, token, imprime, idsize))

#receives message and position to print error message
def printError(posicion, errorMSG):
    linePos = posicion
    print("Linea : ", errorMSG )
    while(True):
        linePos -= 1
        if(programa[linePos] == '\n'):
            break
    pointer = linePos
    while(True):
        linePos += 1
        if(programa[linePos] == '\n'):
            break
        print(programa[linePos], end= "")
    print("\n")
    while(True):
        if(pointer == posicion-1):
            print("^")
            break
        else:
            print(" ", end="")
        pointer +=1





#this function reads the whole program to
def getToken(imprime = False):
    global posicion
    #ignoring any space newline or tab character
    while(programa[posicion] == ' ' or programa[posicion] == '\n' or programa[posicion]== '\t'):
        posicion += 1


    #ignoring comments
    if(programa[posicion] == '/'):
        if(programa[posicion+1] == '*'):
            while(True):
                posicion += 1
                if(programa[posicion] == '*'):
                    if(programa[posicion+1] == '/'):
                        posicion+= 2
                        break

    while(programa[posicion] == ' ' or programa[posicion] == '\n' or programa[posicion]== '\t'):
        posicion += 1

    if(programa[posicion] == '$'):
        return (printToken(TokenType.ENDFILE, '$', imprime, 1))
    #special symbols
    elif(programa[posicion] == '+'):
        return (printToken(TokenType.PLUS, '+', imprime, 1))
    elif(programa[posicion] == '-'):
        return (printToken(TokenType.MINUS, '-', imprime, 1))
    elif(programa[posicion] == ';'):
        return (printToken(TokenType.SEMICOLON, ';', imprime, 1))
    elif(programa[posicion] == ','):
        return (printToken(TokenType.COMMA, ',', imprime, 1))
    elif(programa[posicion] == '('):
        return (printToken(TokenType.OPEN_PARENTHESIS, '(', imprime, 1))
    elif(programa[posicion] == ')'):
        return (printToken(TokenType.CLOSE_PARENTHESIS, ')', imprime,1 ))
    elif(programa[posicion] == '['):
        return (printToken(TokenType.OPEN_BRACKETS, '[', imprime, 1))
    elif(programa[posicion] == ']'):
        return (printToken(TokenType.CLOSE_BRACKETS, ']', imprime, 1))
    elif(programa[posicion] == '{'):
        return (printToken(TokenType.OPEN_KEYS, '{', imprime, 1))
    elif(programa[posicion] == '}'):
        return (printToken(TokenType.CLOSE_KEYS, '}', imprime, 1))

    elif(programa[posicion] == '<'):
        if(programa[posicion+1] == '='):
            return (printToken(TokenType.LESS_THAN_EQUAL_TO, '<=', imprime, 2))
        return (printToken(TokenType.LESS_THAN, '<', imprime, 1))

    elif(programa[posicion] == '>'):
        if(programa[posicion+1] == '='):
            return (printToken(TokenType.GREATER_THAN_EQUAL_TO, '>=', imprime, 2))
        return (printToken(TokenType.GREATER_THAN, '>', imprime, 1))

    elif(programa[posicion] == '*'):
        # if(programa[posicion+1] == '/'):
        #     return (printToken(TokenType.CLOSE_COMMENT, '*/', imprime, 2))
        return (printToken(TokenType.ASTERISK, '*', imprime, 1))

    elif(programa[posicion] == '/'):
        # if(programa[posicion+1] == '*'):
        #
        #     return (printToken(TokenType.OPEN_COMMENT, '/*', imprime, 2))
        return (printToken(TokenType.SLASH, '/', imprime, 1))

    elif(programa[posicion] == '='):
        if(programa[posicion+1] == '='):
            return (printToken(TokenType.EQUAL, '==', imprime, 2))
        return (printToken(TokenType.ASSIGNMENT, '=', imprime, 1))

    elif(programa[posicion] == '!'):
        if(programa[posicion+1] == '='):
            return (printToken(TokenType.DIFFERENT, '!=', imprime, 2))
        else:
            return(printToken(TokenType.ERROR, 'error', imprime, 2, "Error en la formacion de expresion", posicion))
            # return(printToken(TokenType.ERROR, 'error', imprime, 1))

    #checking if its id
    elif(programa[posicion].isalpha()):
        idsize = 1
        token = programa[posicion]
        while(True):
            if(programa[posicion+idsize].isalnum()):
                token += programa[posicion + idsize]
                idsize +=1
            else:
                break
        return (checkIfKeyWord(token, imprime, idsize))
        # return(printToken(TokenType.ID, token, imprime, idsize))

#checking if its number
    elif(programa[posicion].isdigit()):
        idsize = 1
        token = programa[posicion]
        while(True):
            if(programa[posicion+idsize].isdigit()):
                token += programa[posicion + idsize]
                idsize +=1
            elif(programa[posicion + idsize].isalpha()):
                pos = posicion + idsize
                errorpos = posicion + idsize
                while(True):
                    if(programa[posicion+idsize] == ' ' or programa[posicion+idsize] == '\n' or programa[posicion+idsize] == '\t'):
                        return(printToken(TokenType.ERROR, 'error', imprime, idsize, "Error en la formacion de un entero", errorpos))
                    else:
                        idsize += 1
            else:
                break



        return(printToken(TokenType.NUM, token, imprime, idsize))




    else:
        return(printToken(TokenType.ERROR, 'error', imprime, 1))
