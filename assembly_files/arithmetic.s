.text
# test addi, add, sub instructions

#addi, add
addi $r1, $r0, 16
addi $r2, $r0, 31
add $r3, $r2, $r1

#sub
addi $r1, $r0, -16
addi $r2, $r0, 16
sub $r3, $r2, $r1

halt

.data
