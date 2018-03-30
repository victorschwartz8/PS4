.text
# test bgt, beqz, jal, j, jr instructions
addi $r3, $r0, 0
addi $r1, $r0, 15
addi $r2, $r0, 16

bgt $r2, $r1, greater_than #branch is taken
halt #shouldn't be executed

greater_than:
jal my_func #procedure call
beqz $r1, equal #branch is taken
addi $r1, $r2, 1 #shouldn't be executed
halt #shouldn't be executed

my_func:
addi $r1, $r1, -15 #make $r1 equal to 0
jr $r7 #return
addi $r1, $r2, 1 #shouldn't be executed
halt #shouldn't be executed

equal:
j end #jump to end
add $r1, $r2, $r2 #shouldn't be executed

end:
halt

.data
