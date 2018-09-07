from globalTypes import *
from lexer import *



f = open('sample.txt', 'r')
programa = f.read()     # lee todo el archivo a compilar
progLong = len(programa)   # longitud original del programa
programa = programa + '$'   # agregar un caracter $ que represente EOF
posicion = 0       # posición del caracter actual del string
# función para pasar los valores iniciales de las variables globales
globales(programa, posicion, progLong)
token, tokenString = getToken(True)
while (token != TokenType.ENDFILE):
    token, tokenString = getToken(True)
