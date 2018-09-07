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



def getToken(imprime = True):
    print(TokenType.IF)
    return TokenType.IF
