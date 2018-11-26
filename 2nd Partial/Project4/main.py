

from globalTypes import *
from parser import *
from semantica import *
from cgen import *


f = open('sample.txt', 'r')
programa = f.read()
progLong = len(programa)
programa = programa + '$'
posicion  = 0

globales(programa, posicion, progLong)
print("Entrega final Adrian Biller A01018940 C- compiler")
AST =  parser(True)
semantica(AST, True)
codeGen(AST, 'codeGenerated.s')
