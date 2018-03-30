.text
# test shl, shra instructions

#shl
addi $r1, $r0, 1
shl $r2, $r1, 7

#shra
shra $r3, $r2, 7

halt

.data
