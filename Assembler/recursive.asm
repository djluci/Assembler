; Sum from 1 to N recursively
; Input: N in R0
; Ouput: Sum in R0

sum_recurisve:
    CMP R0, 1           ; Compare N to 1
    BEQ base_case       ; If N is 1, go to base case
    PUSH R0             ; Save N on the stack
    SUB R0, R0, 1       ; N = N - 1
    CALL sum_recurisve  ; Recursive call 
    POP R1              ; Pop old N into R1
    ADD R0, R0, R1      ; Add old N to result
    RETURN              ; Return to caller

base_case:
    MOVE R1, 1          ; Base case: return 1
    RETURN              ; Return from base case