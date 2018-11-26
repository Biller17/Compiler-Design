from semantica import *

''' Adrian Biller A01018940
codigo basado en tutoriales de MIPS https://www.youtube.com/watch?v=0aexcR9CNcE'''


fileCode = []
registry = {'$zero': None, '$v0': None, '$v1': None, '$a0':None, '$a1': None, '$a2': None, '$a3': None, '$t0': None, '$t1': None, '$t2':None,'$t3':None,'$t4':None,'$t5':None,'$t6':None,'$t7':None}
def codeGen(tree, file, level):
    global fileCode
    # print((level*3)*'__', tree.type, " # ", tree.value)
    if tree.type == 'program':
        print('.text')
        print('.globl main')
        codeGen(tree.childNodes[0], file, level +1)

    elif tree.type == "fun-declaration":
        print(tree.childNodes[1].value, ":")
        print('     move $fp $sp')
        print('     sw $ra 0($sp)')
        print('     addiu $sp $sp ‐4')
        codeGen(tree.childNodes[2][1], file, level +1)


    elif tree.type == "call":
        if tree.childNodes[0].value == 'input':
            input()
        elif tree.childNodes[0].value == 'output':
            output()
        else:
            print('     sw $fp 0($sp)')
            print('     addiu $sp $sp ‐4')
            n = len(tree.childNodes[1].childNodes)-1
            for i in range(n):
                codeGen(tree.childNodes[1].childNodes[n-i], file, level+1)
                print('     sw $fp 0($sp)')
                print('     addiu $sp $sp ‐4')
            print("     jal ", tree.childNodes[0].value)
            # print(len(tree.childNodes[1].childNodes))


    elif tree.type == 'additive-expression' and len(tree.childNodes) == 2:
        if tree.childNodes[1].childNodes[0].type == '-':
            # print(tree.childNodes[0].type)
            codeGen(tree.childNodes[0], file, level+1)
            print('	sw $a0 0($sp)')
            print('	addiu $sp $sp ‐4')
            codeGen(tree.childNodes[1].childNodes[1], file, level +1)
            print('	lw $t1 4($sp)')
            print('	sub $a0 $t1 $a0')
            print('	addiu $sp $sp 4')
        elif tree.childNodes[1].childNodes[0].type == '+':
            codeGen(tree.childNodes[0], file, level+1)
            print('	sw $a0 0($sp)')
            print('	addiu $sp $sp ‐4')
            codeGen(tree.childNodes[1].childNodes[1], file, level +1)
            print('	lw $t1 4($sp)')
            print('	add $a0 $t1 $a0')
            print('	addiu $sp $sp 4')

    elif tree.type == 'term':
        print('multiplication')

    elif tree.type == 'expression':
        if tree.childNodes[1].type == '=':
            codeGen(tree.childNodes[2], file, level)
            print('     la ', getAvailableVar(), '($v1)')



    elif tree.type == 'iteration-stmt':
            print('     while:')
            codeGen(tree.childNodes[1], file, level +1)
            #todavia no se como poner el condicional
            codeGen(tree.childNodes[2], file, level +1)
            print('     j while')
            print('     exit:')

    elif(tree.type == 'selection-stmt'):
        if tree.childNodes[1].childNodes[1].childNodes[1].type  == '==':
            print('     beq $t0, $t1, true_branch')
        elif tree.childNodes[1].childNodes[1].childNodes[1].type  == '<':
            print('     slt $t3,$t1,$t0') #s0 > s1
            print('     beq $t3, 1 true_branch')
        elif tree.childNodes[1].childNodes[1].childNodes[1].type == '>':
            print('     slt $t3,$t1,$t0') #s0 < s1
            print('     beq $t3, 0 true_branch')
        elif tree.childNodes[1].childNodes[1].childNodes[1].type  == '=<':
            print('     beq $t0, $t1, true_branch')
            print('     slt $t3,$t1,$t0') #s0 > s1
            print('     beq $t3, 1 true_branch')
        elif tree.childNodes[1].childNodes[1].childNodes[1].type == '=>':
            print('     beq $t0, $t1, true_branch')
            print('     slt $t3,$t1,$t0') #s0 < s1
            print('     beq $t3, 0 true_branch')
        elif tree.childNodes[1].childNodes[1].childNodes[1].type == '!=':
            print('     beq $t0, $t1, false_branch')

        if tree.childNodes[3].type == 'else':
            print('false_branch:')
            codeGen(tree.childNodes[4], file, level+1)
            print('     b end_if')
        print("true_branch:")
        codeGen(tree.childNodes[2], file, level +1)
        print("end_if:")


    elif(tree.type == 'return-stmt'):
        codeGen(tree.childNodes[1][0].childNodes[1], file, level +1)
        print('     la $v0, $t3')
        print('     lw $fp 0($sp)')
        print('     jr $ra')
        # codeGen(tree.childNodes[0].type)

    elif type(tree.childNodes) == list:
        for i in range(len(tree.childNodes)):
            if(type(tree.childNodes[i]) == list):
                for j in range(len(tree.childNodes[i])):
                    codeGen(tree.childNodes[i][j],file, level+1)
            # if type(ast.childNodes[i]) == list:
            #     generateST(ast.childNodes[i] , currentScope)
            else:
                codeGen(tree.childNodes[i],file, level +1)
    if tree.type == 'endfile':
        print('     li $v0, 10')
        print('     syscall')



def input():
    print('     li $v0, 5')
    print('     syscall')
    print('     move $t0, $v0')
    # print('     jr $ra')
    return

def output():
    print('     li $v0, 1')
    print('     move $a0, $t0')
    print('     syscall')
    # print('     jr $ra')



def getAvailableVar():
    for i in range(7):
        index = '$t' + str(7 - i)
        if(registry[index] == None):
            return index


def codeGenREF(tree, file):
	if tree:
		# print('Nodo: {}. Tipo: {}'.format(tree.type, tree.tokenType))

		# Init of the code
		if tree.type == 'program':
			print('	.text')
			print('	.align 2')
			print('	.globl main')
			print('main:')

		if tree.type in opKind:
			if tree.type == 'PLUS':
				codeGen(tree.children[0], file)
				print('	sw $a0 0($sp)')
				print('	addiu $sp $sp ‐4')
				codeGen(tree.children[1], file)
				print('	lw $t1 4($sp)')
				print('	add $a0 $t1 $a0')
				print('	addiu $sp $sp 4')

			elif tree.type == 'MINUS':
				codeGen(tree.children[0], file)
				print('	sw $a0 0($sp)')
				print('	addiu $sp $sp ‐4')
				codeGen(tree.children[1], file)
				print('	lw $t1 4($sp)')
				print('	sub $a0 $t1 $a0')
				print('	addiu $sp $sp 4')

			elif tree.type == 'TIMES':
				codeGen(tree.children[0], file)
				print('	sw $a0 0($sp)')
				print('	addiu $sp $sp ‐4')
				codeGen(tree.children[1], file)
				print('	lw $t1 4($sp)')
				print('	mult $a0 $t1 $a0')
				print('	addiu $sp $sp 4')

			elif tree.type == 'OVER':
				codeGen(tree.children[0], file)
				print('	sw $a0 0($sp)')
				print('	addiu $sp $sp ‐4')
				codeGen(tree.children[1], file)
				print('	lw $t1 4($sp)')
				print('	div $a0 $t1 $a0')
				print('	addiu $sp $sp 4')

			# ASSIGN


		elif tree.type in compareKind:
			if tree.type == 'EQ':
				print('	beq $a0 $t1 true_branch')

			elif tree.type == 'DF':
				print('	bne $a0 $t1 true_branch')

			elif tree.type == 'GET':
				print('	bge $a0 $t1 true_branch')

			elif tree.type == 'LET':
				print('	ble $a0 $t1 true_branch')

			elif tree.type == 'GT':
				print('	bgt $a0 $t1 true_branch')

			elif tree.type == 'LT':
				print('	blt $a0 $t1 true_branch')

		elif tree.type == 'statement':
			if tree.children[0]:
				actualNode = tree
				if tree.children[0] and tree.children[0].tokenType == 'IF':
					# Move to the compare instruction
					tree = tree.children[1]
					codeGen(tree.children[0], file)
					print('	sw $a0 0($sp)')
					print('	addiu $sp $sp -4')
					codeGen(tree.children[1], file)
					print('	lw $t1 4($sp)')
					print('	addiu $sp $sp 4')
					codeGen(tree, file)
					print('false_brach:')

					# If there is an ELSE
					try:
						codeGen(actualNode.children[4],file)
					except IndexError:
						pass
					finally:
						print('	b end_if')

					print('true_brach:')
					codeGen(actualNode.children[2], file)
					print('end_if:')

				elif tree.children[0].tokenType == 'WHILE':
					# Move to the compare instruction
					tree = tree.children[1]
					print('begin_while:')
					codeGen(tree.children[0], file)
					print('	sw $a0 0($sp)')
					print('	addiu $sp $sp -4')
					codeGen(tree.children[1], file)
					print('	lw $t1 4($sp)')
					print('	addiu $sp $sp 4')
					codeGen(tree, file)
					print('	b end_while:')
					print('true_branch:')
					codeGen(actualNode.children[2], file)
					print('	b begin_while')
					print('end_while:')


		elif tree.tokenType == 'ID':
			pass

		elif tree.tokenType == 'NUM':
			print('	li $a0 {}'.format(tree.type))


		for child in tree.children:
			codeGen(child, file)



if __name__ == '__main__':
    print("Generador de codigo Adrian Biller A01018940")

    AST = sem()
    codeGen(AST, "codeGenerated.s", 0)
    print(registry)
    f= open("codeGenerated.s","w+")
    f.write("MIPS generated code")

    f.close()
