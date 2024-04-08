# Template by Bruce A. Maxwell, 2015
#
# implements a simple assembler for the following assembly language
# 
# - One instruction or label per line.
#
# - Blank lines are ignored.
#
# - Comments start with a # as the first character and all subsequent
# - characters on the line are ignored.
#
# - Spaces delimit instruction elements.
#
# - A label ends with a colon and must be a single symbol on its own line.
#
# - A label can be any single continuous sequence of printable
# - characters; a colon or space terminates the symbol.
#
# - All immediate and address values are given in decimal.
#
# - Address values must be positive
#
# - Negative immediate values must have a preceeding '-' with no space
# - between it and the number.
#

# Language definition:
#
# LOAD D A   - load from address A to destination D
# LOADA D A  - load using the address register from address A + RE to destination D
# STORE S A  - store value in S to address A
# STOREA S A - store using the address register the value in S to address A + RE
# BRA L      - branch to label A
# BRAZ L     - branch to label A if the CR zero flag is set
# BRAN L     - branch to label L if the CR negative flag is set
# BRAO L     - branch to label L if the CR overflow flag is set
# BRAC L     - branch to label L if the CR carry flag is set
# CALL L     - call the routine at label L
# RETURN     - return from a routine
# HALT       - execute the halt/exit instruction
# PUSH S     - push source value S to the stack
# POP D      - pop form the stack and put in destination D
# OPORT S    - output to the global port from source S
# IPORT D    - input from the global port to destination D
# ADD A B C  - execute C <= A + B
# SUB A B C  - execute C <= A - B
# AND A B C  - execute C <= A and B  bitwise
# OR  A B C  - execute C <= A or B   bitwise
# XOR A B C  - execute C <= A xor B  bitwise
# SHIFTL A C - execute C <= A shift left by 1
# SHIFTR A C - execute C <= A shift right by 1
# ROTL A C   - execute C <= A rotate left by 1
# ROTR A C   - execute C <= A rotate right by 1
# MOVE A C   - execute C <= A where A is a source register
# MOVEI V C  - execute C <= value V
#

# 2-pass assembler
# pass 1: read through the instructions and put numbers on each instruction location
#         calculate the label values
#
# pass 2: read through the instructions and build the machine instructions
#

import sys

# converts d to an 8-bit 2-s complement binary value
def dec2comp8( d, linenum ):
    if d >= 0:
        return format(d if d < 128 else d - 256, '08b')
    else:
        return format((1 << 8) + d, '08b')

# converts d to an 8-bit unsigned binary value
def dec2bin8( d, linenum ):
    if d < 0 or d >= 256:
        print(f'Invalid address on line {linenum}: value is negative or too large')
        sys.exit()
    return format(d, '08b')


# Tokenizes the input data, discarding white space and comments
# returns the tokens as a list of lists, one list for each line.
#
# The tokenizer also converts each character to lower case.
def tokenize( fp ):
    tokens = []
    fp.seek(0) # start of the file
    lines = fp.readlines()
    # strip white space and comments from each line
    for line in lines:
        comment_index = line.find('#')
        if comment_index != -1:
            line = line[:comment_index]
        line = line.strip().lower()
        if line:
            tokens.append(line.split())
    return tokens


# reads through the file and returns a dictionary of all location
# labels with their line numbers
def pass1( tokens ):
    labels = {}
    instructions = []
    linenum = 0
    
    for token_line in tokens:
        if len(token_line) == 1 and token_line[0].endswith(':'):
            label = token_line[0][:-1]
            if label in labels:
                print(f'Duplicate label "{label}" found on line {linenum}')
                sys.exit()
            labels[label] = linenum
        else:
            instructions.append(token_line)
            linenum += 1
    return labels, instructions

def pass2( tokens, labels ):
    machine_instructions = []
    opcode_map = {'movei': '11111'}
    register_map = {'ra': '000', 're': '100', 'rd': '010', 'rb': '001', 'rc': '101'}
    for token_line in tokens:
        opcode = opcode_map.get(token_line[0], '0' * 5)
        if token_line[0] == 'movei':
            immediate_value = format(int(token_line[1]), '08b')
            register_code = register_map.get(token_line[2], '0' * 3)
            machine_instruction = opcode + immediate_value + register_code
        else:
            machine_instruction = '0' * 16
        machine_instructions.append(machine_instruction)
    return machine_instructions

def main( file_path ):
    try:
        with open(file_path, 'r') as file:
            tokens = tokenize(file)
    except FileNotFoundError:
        print(f'Error: File {file_path} not found.')
        return
    
    labels, instruction_tokens = pass1(tokens)
    machine_instructions = pass2(instruction_tokens, labels)
    
    print("-- program memory file for" + file_path)
    print("Depth = 256;")
    print("Width = 16;")
    print("ADDRESS_RADIX = HEX;")
    print("DATA_RADIX = BIN;")
    print("CONTENT")
    print("BEGIN")
    
    for line, instr in enumerate(machine_instructions):
        print(f"{line:02X} : {instr};")
        
    for line in range(len(machine_instructions), 256):
        print(f"{line:02X} : {'1' * 16};")
        
    print("END")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python assembler.py <filename>')
        sys.exit()
        
    main(sys.argv[1])
    