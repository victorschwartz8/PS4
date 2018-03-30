.text


jal test

done:
    # end the program -- this will hang forever on the real thing, but the simulator detects it and simply exits gracefully
    halt

test:
addi $r2, $r0, 5
jr $r7
addi $r1, $r0, 10
