

global input
global position



#Adrian Biller A01018940 segundo examen parcial

def nextToken():
    global position
    position += 1
    return input[position]


def parseString(string):
    global input
    global position
    position = -1
    input = string

    print(parseA())


def parseA():
    if(nextToken() == "3"):
        return True
    elif(nextToken() == "c"):
        return True
    elif(nextToken() == "("):
        if(parseB()):
            if(nextToken() ==")"):
                return True
    return False

def parseB():
    if(parseA()):
        if(parseD()):
            return True
    return False

def parseD():
    while(nextToken() == ","):
        if(parseA()):
            if(parseD()):
                return True
    return False


if __name__ == '__main__':
    print("Codigo examen parcial 2 Adrián Biller")
    #ejemplos dados para correr el parser
    print("Parseando string: (c,(c,(3)),(c))")
    parseString("(c,(c,(3)),(c))")
    print("Parseando string: (3,c,(c)")
    parseString("(3,c,(c)")
