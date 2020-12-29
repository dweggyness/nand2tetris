import sys

# .asm to .hack assembler
# To use, call this py file and enter the file name as an argument
# Example usage: 'python3 assembler.py pong/Pong.asm'
# Creates a .hack file in the same directory as the source file.
# Example output: 'python3 assembler.py pong/Pong.hack'

destDict = {
  '0': '000',
  'M': '001',
  'D': '010',
  'MD': '011',
  'A': '100',
  'AM': '101',
  'AD': '110',
  'AMD': '111'
}
jumpDict = {
  'null': '000',
  'JGT': '001',
  'JEQ': '010',
  'JGE': '011',
  'JLT': '100',
  'JNE': '101',
  'JLE': '110',
  'JMP': '111'
}
compDict = {
  '0': '0101010',
  '1': '0111111',
  '-1': '0111010',
  'D': '0001100',
  'A': '0110000',
  'M': '1110000',
  '!D': '0001101',
  '!A': '0110001',
  '!M': '1110001',
  '-D': '0001111',
  '-A': '0110011',
  '-M': '1110011',
  'D+1': '0011111',
  'A+1': '0110111',
  'M+1': '1110111',
  'D-1': '0001110',
  'A-1': '0110010',
  'M-1': '1110010',
  'D+A': '0000010',
  'D+M': '1000010',
  'D-A': '0010011',
  'D-M': '1010011',
  'A-D': '0000111',
  'M-D': '1000111',
  'D&A': '0000000',
  'D&M': '1000000',
  'D|A': '0010101',
  'D|M': '1010101'
}

def to15BitBinaryStr(number):
  binaryValue = bin(int(number))
  binaryValue = binaryValue[2:] # remove leading '0b' in binary value, e.g 0b101 -> 101 
  binaryStr = str(binaryValue).zfill(15)

  return binaryStr

def main():
  outputName = fileName.split('.')[0]
  with open(f'{outputName}.hack', 'w') as outputFile:
    with open(f'{fileName}', 'r') as inputFile:
      lineNumber = 0
      variableFreePointer = 16
      pointerDict = {
        'SP': '0',
        'LCL': '1',
        'ARG': '2',
        'THIS': '3',
        'THAT': '4',
        'R0': '0', 'R1': '1', 'R2': '2', 'R3': '3', 'R4': '4', 'R5': '5', 'R6': '6', 'R7': 7, 'R8': 8, 'R9': 9,
        'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
        'SCREEN': 16384,
        'KBD': 24576
      }
      
      # first pass, assign label values
      for line in inputFile:
        line = line.split('//')[0] # remove comments, if any
        line = line.strip() # remove left and right whitespace

        if (len(line) == 0 or line.isspace()): # empty line, skip
          continue
        elif line[0] == '(': # LABEL
          labelName = line[1:-1] # get everything between the brackets
          pointerDict[labelName] = lineNumber
        else:
          lineNumber += 1
      
      inputFile.seek(0) # move read cursor back to start
      lineNumber = 0
      for line in inputFile:
        line = line.split('//')[0] # remove comments, if any
        line = line.strip() # remove left and right whitespace
        if (len(line) == 0 or line.isspace()): # empty line, skip
          continue
        elif line[0] == '(': # label line, skip
          continue
        elif line[0] == '@': # A-Instruction
          address = line[1:].strip()
          decAddress = ''
          if address.isdigit(): # @17, not a varialbe
            decAddress = address
          else: # @sum, is a variable, check pointerDict
            if address in pointerDict: # already in dict
              decAddress = pointerDict[address]
            else: # not in dict yet, add to it
              decAddress = variableFreePointer
              pointerDict[address] = decAddress
              variableFreePointer += 1 # increment to next pointer
          machineInstruction = '0' + to15BitBinaryStr(decAddress)
          lineNumber += 1
        else: # C-Instruction
          compField = ''
          destField = '0'
          jumpField = 'null'
          if ';' in line: # has jump statement, e.g: D=A;JMP
            jumpField = line.split(';')[1].strip()
            remainingField = line.split(';')[0]
            if '=' in remainingField: # has both dest and comp, e.g: D=A;JMP
              destAndCompSplit = remainingField.split('=')
              destField = destAndCompSplit[0].strip()
              compField = destAndCompSplit[1].strip()
            else: # only has comp, e.g: 0;JMP
              compField = remainingField[0].strip()
          else: # no jump statement, e.g: D=A+1
            if '=' in line: # has both dest and comp, e.g: D=A;JMP
              destAndCompSplit = line.split('=')
              destField = destAndCompSplit[0].strip()
              compField = destAndCompSplit[1].strip()
            else: # only has comp, e.g: 0;JMP
              compField = line.strip()
          try:
            comp = compDict[compField]
            dest = destDict[destField]
            jump = jumpDict[jumpField]
            lineNumber += 1
          except:
            print(f'Error on line {lineNumber}: {line}, error with one or more of these fields:')
            print("Unexpected error:", sys.exc_info()[0])
            print('Result Comp: ' + comp + ' Original field: ' + compField)
            print('Result Dest: ' + dest + ' Original field: ' + destField)
            print('Result Jump: ' + jump + ' Original field: ' + jumpField)

          machineInstruction = '111' + comp + dest + jump
        outputFile.write(machineInstruction)
        outputFile.write('\n')

try:
  fileName = sys.argv[1]
except:
  print('Please provide a filename as a command line argument')
main()