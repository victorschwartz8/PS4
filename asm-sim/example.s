.text
# Example program for the Duke 250/16 computer.
# Developed for ECE/COMPSCI 250, Spring 2017.

    # load address of string and run the print string function
    la $r1, hello            # r1 = address of hello
    #   (because of the real instructions emitted for the 'la' pseudo instruction, the next instruction is at PC 0x0007)
    jal puts                 # call puts function, r7=PC+1 (0x0008)
    #halt
    # read a byte and the word kappa and subtract
    input $r5                # r5 = the key or 128 on fail
    output $r5               # print it
    la $r1, kappa            # r1 = address of kappa (7)
    lw $r2, 0($r1)           # r2 = kappa           (1000 or 0x03E8)
    sw $r5, 4($r1)           # mem[kappa + 4] = r5
    lw $r4, 4($r1)           # r4 = r5
    add $r4, $r4, $r1        # r4 = r4 + 3
    output $r4               # print it
    sub $r3, $r2, $r5        # r3 = kappa - key     (assuming read was a fail, it's 872 or 0x0368)

    # do some random instructions
    addi $r4, $r0, -1        # r4 = 0xFFFF
    xor $r5, $r2, $r4        # r4 = ~kappa          (-1001 or 0xFC17)
    nand $r5, $r2, $r5       # r5 = kappa | ~kappa  (logically, this must be 0xFFFF)
    shl $r6, $r2, 2          # r6 = kappa << 2      (4000 or 0x0FA0)
    shra $r6, $r2, 2         # r6 = kappa >> 2      (250 or 0x00FA)
    addi $r2, $r2, -2        # r2 -= 2              (998 or 0x03E6)
    shra $r2, $r4, 1         # r4 = r2 >> 1         (499 or 0x01F3)
    bgt $r2, $r0, done       # if (r2>0) goto done (branch is taken)
    add $r2, $r2, $r0        # (this instruction is skipped)
    
done:
    # end the program -- this will hang forever on the real thing, but the simulator detects it and simply exits gracefully
    halt
    
    # registers at end of program (assuming read was a fail): [0000 0007 01F3 0368 FC17 FFFF 00FA 0008]

puts:
loop:
    lw $r3, 0($r1)        # load this character (because we're in word-addressed memory, each character is a 16-bit word)
    beqz $r3, endloop # if at null char, break
    output $r3            # print it
    addi $r1, $r1, 1      # pointer++
    j loop                # loop
endloop:
    jr $r7                # return

.data
hello: .asciiz "Hello!"
kappa: .word 1000
