import sys

# .vm to .asm assembler
# To use, call this py file and enter the file name as an argument
# Example usage: 'python3 VMtoASMcompiler.py MemoryAccess/BasicTest/BasicTest.vm'
# Creates a .asm file in the same directory as the source file.
# Example output: 'MemoryAccess/BasicTest/BasicTest.asm'

memSegmentDict = {
  'local': '@LCL',
  'argument': '@ARG',
  'this': '@THIS',
  'that': '@THAT',
  'temp': '@5'
}

# where arg (cmd) -> add, sub, neg, eq, gt, lt, and, or, not
# operate on top 2 values in stack
def writeArithmeticASMInstruction(cmd):
  asmInstruction = '@SP \n'
  asmInstruction += 'A=M-1 \n' # @(SP-1)
  asmInstruction += 'D=M \n'
  # D contains value of @(SP-1), current pointer *(SP-1)
  if (cmd == 'add'):
    asmInstruction += 'A=A-1 \n' # @(SP - 2)
    asmInstruction += 'M=M+D \n' # @(SP-2) + @(SP-1)
  elif (cmd == 'sub'):
    asmInstruction += 'A=A-1 \n' # @(SP - 2)
    asmInstruction += 'M=M-D \n'
  elif (cmd == 'and'):
    asmInstruction += 'A=A-1 \n' # @(SP - 2)
    asmInstruction += 'M=D&M \n'
  elif (cmd == 'or'):
    asmInstruction += 'A=A-1 \n' # @(SP - 2)
    asmInstruction += 'M=D|M \n'
  elif (cmd == 'neg'):
    asmInstruction += 'M=-M \n'
    asmInstruction += '@SP \n' # to counter the @SP M=M-1 at the end of each VM instruction write
    asmInstruction += 'M=M+1 \n' # it was added as most other cmds ( 6/8 ) uses the top2 in the stack instead of top1 
  elif (cmd == 'not'):
    asmInstruction += 'M=!M \n'
    asmInstruction += '@SP \n' # to counter the @SP M=M-1 at the end of each VM instruction write
    asmInstruction += 'M=M+1 \n' # it was added as most other cmds ( 6/8 ) uses the top2 in the stack instead of top1 
  elif (cmd in ['eq', 'gt', 'lt']):
    asmInstruction += 'A=A-1 \n' # @(SP - 2)
    asmInstruction += 'D=M-D \n'
    asmInstruction += f'@TRUE.{curVMLine} \n' 
    if (cmd == 'eq'):    
      asmInstruction += 'D;JEQ \n' # if D-M (@SP-1 - @SP-2) = 0, they are equal
    elif (cmd == 'gt'):
      asmInstruction += 'D;JGT \n'
    elif (cmd == 'lt'):
      asmInstruction += 'D;JLT \n'
    # instructions specific to 'eq,gt,lt' instructions
    asmInstruction += f'@INSERT_VALUE.{curVMLine} \n'
    asmInstruction += 'D=0 \n' # else they are not equal, set D=0
    asmInstruction += '0;JMP \n'
    asmInstruction += f'(TRUE.{curVMLine}) \n' # set D=1 if they are equal
    asmInstruction += 'D=-1 \n'
    asmInstruction += f'(INSERT_VALUE.{curVMLine}) \n'
    asmInstruction += '@SP \n'
    asmInstruction += 'A=M-1 \n'
    asmInstruction += 'A=A-1 \n'
    asmInstruction += 'M=D \n'
  else:
    raise Exception('Error! Invalid arithmetic instruction provided: ', cmd)

  asmInstruction += '@SP \n'
  asmInstruction += 'M=M-1 \n'
  return asmInstruction

curVMLine = 0

# push a value from address at memSegment into the stack
# possible memSegments -> local, argument, this, that, constant, static, pointer, temp
def writePushASMInstruction(memSegment, address):
  asmInstruction = ''
  if (memSegment == 'constant'):
    asmInstruction += f'@{address} \n' # set cur data value to address
    asmInstruction += 'D=A \n' 
    asmInstruction += '@SP \n'
    asmInstruction += 'A=M \n'
    asmInstruction += 'M=D \n'
  elif (memSegment == 'static'):
    asmInstruction += f'@var.{address} \n'
    asmInstruction += 'D=M \n' 
    asmInstruction += '@SP \n'
    asmInstruction += 'A=M \n'
    asmInstruction += 'M=D \n'
  elif (memSegment == 'pointer'):
    pointerDict = { '0': '@THIS', '1': '@THAT' }
    asmInstruction += f'{pointerDict[address]} \n'
    asmInstruction += 'D=M \n' 
    asmInstruction += '@SP \n'
    asmInstruction += 'A=M \n'
    asmInstruction += 'M=D \n'
  elif (memSegment in ['local', 'argument', 'this', 'that', 'temp']):
    asmInstruction += f'@{address} \n'
    asmInstruction += 'D=A \n' 
    asmInstruction += f'{memSegmentDict[memSegment]} \n'
    asmInstruction += 'A=D+M \n' 
    asmInstruction += 'D=M \n' 
    asmInstruction += '@SP \n'
    asmInstruction += 'A=M \n'
    asmInstruction += 'M=D \n'
  else: 
    raise Exception('Error in Push instruction! Invalid memSegment - address provided: ', memSegment, ' - ', address)

  asmInstruction += '@SP \n'
  asmInstruction += 'M=M+1 \n'
  return asmInstruction

  
def writePopASMInstruction(memSegment, address):
  asmInstruction = '@SP \n'
  asmInstruction += 'A=M-1 \n'
  asmInstruction += 'D=M \n' # top value in the stack
  if (memSegment == 'static'):
    asmInstruction += f'@var.{address} \n'
    asmInstruction += 'M=D \n'
  elif (memSegment == 'pointer'):
    pointerDict = { '0': '@THIS', '1': '@THAT' }
    asmInstruction += f'{pointerDict[address]} \n'
    asmInstruction += 'M=D \n'
  elif (memSegment in ['local', 'argument', 'this', 'that', 'temp']):
    asmInstruction += f'@{address} \n'
    asmInstruction += 'D=A \n' 
    asmInstruction += f'{memSegmentDict[memSegment]} \n'
    if (memSegment == 'temp'): # special case for temp as it has no 'base address' pointer
      asmInstruction += 'D=D+A \n' 
    else:
      asmInstruction += 'D=D+M \n'
    asmInstruction += '@R13 \n' # store address of where we want to pop the variable
    asmInstruction += 'M=D \n' 
    asmInstruction += '@SP \n'
    asmInstruction += 'A=M-1 \n'
    asmInstruction += 'D=M \n' # top value in the stack
    asmInstruction += '@R13 \n' # store address of where we want to pop the variable
    asmInstruction += 'A=M \n' 
    asmInstruction += 'M=D \n' # insert value from @R13 into desired location

  else: 
    raise Exception('Error in Pop Instruction! Invalid memSegment - address provided: ', memSegment, ' - ', address)

  asmInstruction += '@SP \n'
  asmInstruction += 'M=M-1 \n'
  return asmInstruction


def main():
  outputName = fileName.split('.')[0]
  with open(f'{outputName}.asm', 'w') as outputFile:
    with open(f'{fileName}', 'r') as inputFile:
      for line in inputFile:
        line = line.split('//')[0] # remove comments, if any
        line = line.strip() # remove left and right whitespace

        if (len(line) == 0 or line.isspace()): # empty line, skip
          continue
        
        asmInstruction = ''

        vmInstruction = line.split(' ')
        if (vmInstruction[0] == 'push'): # push instruction
          # vmInstruction example = ['push', 'constant', '2']
          asmInstruction = writePushASMInstruction(vmInstruction[1], vmInstruction[2])
        elif (vmInstruction[0] == 'pop'): #pop instruction
          asmInstruction = writePopASMInstruction(vmInstruction[1], vmInstruction[2])
        else: # else its a arithmetic op
          asmInstruction = writeArithmeticASMInstruction(vmInstruction[0])

        global curVMLine
        curVMLine += 1
        outputFile.write(asmInstruction)
        outputFile.write('\n')

try:
  fileName = sys.argv[1]
except:
  print('Please provide a filename as a command line argument')

main()