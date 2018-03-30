.text
# test nand, xor instrctions

#nand
addi $r1, $r0, 15
addi $r2, $r0, 12
nand $r3, $r2, $r1

#xor
xor $r4, $r3, $r2

halt

.data
