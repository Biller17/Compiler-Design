from semantica import *

opKind =  [ 'PLUS', 'MINUS', 'TIMES', 'OVER', 'ASSIGN' ]
compareKind = [ 'EQ', 'DF', 'GET', ',LET', 'GT', 'LT' ]
evaluationKind = ['IF', 'WHILE']


def codeGen(tree, file, level):
    print((level*3)*'__', tree.type, " # ", tree.value)
    if type(tree.childNodes) == list:
        for i in range(len(tree.childNodes)):
            if(type(tree.childNodes[i]) == list):
                for j in range(len(tree.childNodes[i])):
                    codeGen(tree.childNodes[i][j],file, level+1)
            # if type(ast.childNodes[i]) == list:
            #     generateST(ast.childNodes[i] , currentScope)
            else:
                codeGen(tree.childNodes[i],file, level +1)



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
    codeGen(AST, "codeGenerated.txt", 0)
