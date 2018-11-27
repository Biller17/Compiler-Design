.text
.align 2
.globl main
gcd:
     move $fp $sp
     sw $ra 0($sp)
     addiu $sp $sp ‐4
     beq $t0, $t1, true_branch
false_branch:
     sw $fp 0($sp)
     addiu $sp $sp ‐4
     sw $fp 0($sp)
     addiu $sp $sp ‐4
     jal gcd
     la $v0, $t3
     lw $fp 0($sp)
     jr $ra
     b end_if
true_branch:
     la $v0, $t3
     lw $fp 0($sp)
     jr $ra
end_if:
     lw $ra 4($sp)
     addiu $sp $sp z
     lw $fp 0($sp)
     jr $ra
main:
     move $fp $sp
     sw $ra 0($sp)
     addiu $sp $sp ‐4
     ori $s0, 0
     ori $s1, 0
     la $t7($v1)
     la $t6($v1)
     lw $ra 4($sp)
     addiu $sp $sp z
     lw $fp 0($sp)
     jr $ra
     li $v0, 10
     syscall
