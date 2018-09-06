
##Examen parcial Adrian Biller a01018940


def lexer3(s):
    print("Examen parcial Adrian Biller A01018940")
    strings = s.split(' ')
    lexerStrings = []
    accepted = 1
    decimal = 0
    for i in range(len(strings)):
        if(strings[i] != ''):
            if(strings[i] == '\n'):
                continue
            for j in range(len(strings[i])):
                if(strings[i][j] == '.'):
                    if(j <= 0):
                        accepted = 0
                    if(decimal == 1):
                        accepted = 0
                    decimal = 1
                else:
                    try:
                        num = int(strings[i][j])
                    except:
                        accepted = 0
                    if(num > 2):
                        accepted = 0
            decimal = 0
            if(accepted == 1):
                lexerStrings.append(strings[i])
                # print("accepted")
            else:
                print(lexerStrings)
                return

    print(lexerStrings)




if __name__ == '__main__':
    lexer3("2110.011    11.  \n 112021   \n  13.12    21.11A \n   .211  .234124234    jsdhlskdfjsldkfjsldkf A ADrian Biller Alcantara         sdjsdlkfjsa   1212212112.211212.1212")
