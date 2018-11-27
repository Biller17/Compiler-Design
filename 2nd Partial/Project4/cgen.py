from semantica import *

''' Adrian Biller A01018940
codigo basado en tutoriales de MIPS https://www.youtube.com/watch?v=0aexcR9CNcE'''


fileCode = []
registry = {'$zero': None, '$v0': None, '$v1': None, '$a0':None, '$a1': None, '$a2': None, '$a3': None, '$t0': None, '$t1': None, '$t2':None,'$t3':None,'$t4':None,'$t5':None,'$t6':None,'$t7':None, '$s0': None, '$s1': None,'$s1': None,'$s3': None,'$s4': None,'$s5': None,'$s6': None,'$s7': None}
def codeGen(tree, file, level = 0):
    global fileCode
    # fileCode.append((level*3)*'__', tree.type)
    if tree.type == 'program':
        fileCode.append('.text')
        fileCode.append('.align 2')
        fileCode.append('.globl main')
        codeGen(tree.childNodes[0], file, level +1)

    elif tree.type == "fun-declaration":
        fileCode.append(tree.childNodes[1].value + ":")
        fileCode.append('     move $fp $sp')
        fileCode.append('     sw $ra 0($sp)')
        fileCode.append('     addiu $sp $sp ‐4')
        codeGen(tree.childNodes[2][1], file, level +1)
        fileCode.append('     lw $ra 4($sp)')
        fileCode.append('     addiu $sp $sp z')
        fileCode.append('     lw $fp 0($sp)')
        fileCode.append('     jr $ra')


    elif tree.type == "call":
        # fileCode.append('                                                 ',tree.childNodes[0].value)
        if tree.childNodes[0].value == 'input':
            input()
        elif tree.childNodes[0].value == 'output':
            output()
        else:
            fileCode.append('     sw $fp 0($sp)')
            fileCode.append('     addiu $sp $sp ‐4')
            n = len(tree.childNodes[1].childNodes)-1
            for i in range(n):
                codeGen(tree.childNodes[1].childNodes[n-i], file, level+1)
                fileCode.append('     sw $fp 0($sp)')
                fileCode.append('     addiu $sp $sp ‐4')
            fileCode.append("     jal " + tree.childNodes[0].value)
            # fileCode.append(len(tree.childNodes[1].childNodes))


    elif tree.type == 'additive-expression' and len(tree.childNodes) == 2:
        if tree.childNodes[1].childNodes[0].type == '-':
            # fileCode.append(tree.childNodes[0].type)
            codeGen(tree.childNodes[0], file, level+1)
            fileCode.append('     sw $a0 0($sp)')
            fileCode.append('     addiu $sp $sp ‐4')
            codeGen(tree.childNodes[1].childNodes[1], file, level +1)
            fileCode.append('     lw $t1 4($sp)')
            fileCode.append('     sub $a0 $t1 $a0')
            fileCode.append('     addiu $sp $sp 4')
        elif tree.childNodes[1].childNodes[0].type == '+':
            codeGen(tree.childNodes[0], file, level+1)
            fileCode.append('     sw $a0 0($sp)')
            fileCode.append('     addiu $sp $sp ‐4')
            codeGen(tree.childNodes[1].childNodes[1], file, level +1)
            fileCode.append('     lw $t1 4($sp)')
            fileCode.append('     add $a0 $t1 $a0')
            fileCode.append('     addiu $sp $sp 4')

    elif tree.type == 'term' and len(tree.childNodes) > 1:
        if tree.childNodes[1].type =='term-p':
            if tree.childNodes[1].childNodes[0].type == '*':
                codeGen(tree.childNodes[0], file, level +1)
                fileCode.append('     sw $a0 0($sp)')
                fileCode.append('     addiu $sp $sp ‐4')
                codeGen(tree.childNodes[1].childNodes[1], file, level +1)
                fileCode.append('     lw $t1 4($sp)')
                fileCode.append('     mult $a0 $t1 $a0')
                fileCode.append('     addiu $sp $sp 4')
            elif tree.childNodes[1].childNodes[0].type == '/':
                codeGen(tree.childNodes[0], file)
                fileCode.append('      sw $a0 0($sp)')
                fileCode.append('      addiu $sp $sp ‐4')
                codeGen(tree.childNodes[1].childNodes[1], file, level +1)
                fileCode.append('      lw $t1 4($sp)')
                fileCode.append('      div $a0 $t1 $a0')
                fileCode.append('      addiu $sp $sp 4')

    elif tree.type == 'expression':
        if tree.childNodes[1].type == '=':
            codeGen(tree.childNodes[2], file, level)
            fileCode.append('     la ' + getAvailableTempVar() + '($v1)')

    elif tree.type == 'iteration-stmt':
            fileCode.append('     while:')
            codeGen(tree.childNodes[1], file, level +1)
            #todavia no se como poner el condicional
            fileCode.append('     exit')
            codeGen(tree.childNodes[2], file, level +1)
            fileCode.append('     j while')
            fileCode.append('     exit:')

    elif(tree.type == 'selection-stmt'):
        if tree.childNodes[1].childNodes[1].childNodes[1].type  == '==':
            fileCode.append('     beq $t0, $t1, true_branch')
        elif tree.childNodes[1].childNodes[1].childNodes[1].type  == '<':
            fileCode.append('     slt $t3,$t1,$t0') #s0 > s1
            fileCode.append('     beq $t3, 1 true_branch')
        elif tree.childNodes[1].childNodes[1].childNodes[1].type == '>':
            fileCode.append('     slt $t3,$t1,$t0') #s0 < s1
            fileCode.append('     beq $t3, 0 true_branch')
        elif tree.childNodes[1].childNodes[1].childNodes[1].type  == '=<':
            fileCode.append('     beq $t0, $t1, true_branch')
            fileCode.append('     slt $t3,$t1,$t0') #s0 > s1
            fileCode.append('     beq $t3, 1 true_branch')
        elif tree.childNodes[1].childNodes[1].childNodes[1].type == '=>':
            fileCode.append('     beq $t0, $t1, true_branch')
            fileCode.append('     slt $t3,$t1,$t0') #s0 < s1
            fileCode.append('     beq $t3, 0 true_branch')
        elif tree.childNodes[1].childNodes[1].childNodes[1].type == '!=':
            fileCode.append('     beq $t0, $t1, false_branch')

        if tree.childNodes[3].type == 'else':
            fileCode.append('false_branch:')
            codeGen(tree.childNodes[4], file, level+1)
            fileCode.append('     b end_if')
        fileCode.append("true_branch:")
        codeGen(tree.childNodes[2], file, level +1)
        fileCode.append("end_if:")


    elif(tree.type == 'return-stmt'):
        codeGen(tree.childNodes[1][0].childNodes[1], file, level +1)
        fileCode.append('     la $v0, $t3')
        fileCode.append('     lw $fp 0($sp)')
        fileCode.append('     jr $ra')
        # codeGen(tree.childNodes[0].type)

    elif tree.type == 'var-declaration':
        # fileCode.append(tree.childNodes[1].value)
        fileCode.append('     ori ' + getAvailableVar(tree.childNodes[1].value) + ', 0')


    elif type(tree.childNodes) == list:
        # fileCode.append('                                                                             ',tree.type)
        for i in range(len(tree.childNodes)):
            if(type(tree.childNodes[i]) == list):
                for j in range(len(tree.childNodes[i])):
                    codeGen(tree.childNodes[i][j],file, level+1)
            # if type(ast.childNodes[i]) == list:
            #     generateST(ast.childNodes[i] , currentScope)
            else:
                codeGen(tree.childNodes[i],file, level +1)
    if tree.type == 'endfile':
        fileCode.append('     li $v0, 10')
        fileCode.append('     syscall')
        generateFile(file)





def input():
    fileCode.append('     li $v0, 5')
    fileCode.append('     syscall')
    fileCode.append('     move $t0, $v0')
    return

def output():
    fileCode.append('     li $v0, 1')
    fileCode.append('     move $a0, $t0')
    fileCode.append('     syscall')
    return



def getAvailableTempVar():
    for i in range(7):
        index = '$t' + str(7 - i)
        if(registry[index] == None):
            registry[index] = "in use"
            return index

def getAvailableVar(var):
    for i in range(7):
        index = '$s' + str(i)
        if(registry[index] == None):
            registry[index] = "in use"
            return index

def generateFile(file):
    print("Generador de codigo Adrian Biller A01018940")
    open(file, 'w').close()
    f= open(file,"a")
    for i in range(len(fileCode)):
        temp = fileCode[i] + "\n"
        f.write(temp)

    f.close()


if __name__ == '__main__':


    AST = sem()
    codeGen(AST, "codeGenerated.s", 0)
    print(registry)
    f= open("codeGenerated.s","a")
    for i in range(len(fileCode)):
        temp = fileCode[i] + "\n"
        print(temp)
        f.write(temp)
    f.close()
