; Fibonacci sequence program 
START:
    MOVEI 0 R0      ; Initialize the first Fibonacci number
    MOVEI 1 R1      ; Initialize the second Fibonacci number
    MOVEI 10 R2     ; Counter set to calculate first 10 Fibonacci numbers
LOOP:
    ADD R0 R1 R2    ; R3 = R0 + R1
    MOVE R1 R0      ; Move the second number to the first register
    MOVE R3 R1      ; Move the new Fibonacci number to the second register
    SUB R2 1 R2     ; Decrement the Counter
    BRAZ END        ; If the counter is zero, end the loop
    BRA LOOP        ; Otherwise, continue the loop
END:
    HALT            ; End of the program