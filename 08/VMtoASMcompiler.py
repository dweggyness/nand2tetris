import sys
import os

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


def writeCallASMInstruction(funcName, argsCount):
  label = 'LABEL' + str(curVMLine)
  asmInstruction = ''

  asmInstruction += f'@{label} \n' # push return address into stack
  asmInstruction += 'D=A \n'
  asmInstruction += '@SP \n'
  asmInstruction += 'A=M \n'
  asmInstruction += 'M=D \n'
  asmInstruction += '@SP \n' # inc *@SP
  asmInstruction += 'M=M+1 \n'
  # push *@LCL onto stack
  for curAddress in ['@LCL','@ARG','@THIS','@THAT']:
    asmInstruction += f'{curAddress} \n'
    asmInstruction += 'D=M \n'
    asmInstruction += '@SP \n'
    asmInstruction += 'A=M \n'
    asmInstruction += 'M=D \n'
    asmInstruction += '@SP \n' # inc *@SP
    asmInstruction += 'M=M+1 \n'

  # reposition *@ARG to (@SP - 5 - argsCount)
  asmInstruction += '@SP \n'
  asmInstruction += 'D=M \n'
  asmInstruction += '@5 \n' # @SP - 5
  asmInstruction += 'D=D-A \n'
  asmInstruction += f'@{argsCount} \n' # @SP - 5 - argsCount
  asmInstruction += 'D=D-A \n' 
  asmInstruction += '@ARG \n'
  asmInstruction += 'M=D \n'
  # reposition *@LCL to @SP
  asmInstruction += '@SP \n'
  asmInstruction += 'D=M \n'
  asmInstruction += '@LCL \n' # @SP - 5
  asmInstruction += 'M=D \n'

  # goto function
  asmInstruction += f'@{funcName} \n'
  asmInstruction += '0;JMP \n'
  asmInstruction += f'({label}) \n'

  return asmInstruction

def writeFunctionASMInstruction(funcName, argsCount):
  asmInstruction = ''
  asmInstruction += f'({funcName}) \n'
  for x in range(int(argsCount)):
    asmInstruction += parseVMInstruction('push constant 0')

  return asmInstruction

def writeReturnASMInstruction():
  asmInstruction = '@LCL \n'
  asmInstruction += 'D=M \n'
  asmInstruction += '@R15 \n'
  asmInstruction += 'M=D \n' # store @LCL address in @R15, temp var
  asmInstruction += '@5 \n'
  asmInstruction += 'A=D-A \n' # set pointer to *(@LCL - 5)
  asmInstruction += 'D=M \n' # return address
  asmInstruction += '@R14 \n'  # store @RET address at @R14 ( @LCL - 5 )
  asmInstruction += 'M=D \n' 

  # pop the stack, and place it at *@ARG
  asmInstruction += '@SP \n'
  asmInstruction += 'A=M-1 \n'
  asmInstruction += 'D=M \n' # top value in the stack
  asmInstruction += '@ARG \n'
  asmInstruction += 'A=M \n'
  asmInstruction += 'M=D \n' # set @ARG to popped value
  asmInstruction += 'D=A \n' # store pointer of @ARG
  asmInstruction += '@SP \n'
  asmInstruction += 'M=D+1 \n' # set @SP to @ARG + 1

  # restore @addresses to caller's
  # iterate through endFrame backwards
  for curAddress in ['@THAT','@THIS','@ARG','@LCL']:
    asmInstruction += '@R15 \n'
    asmInstruction += 'M=M-1 \n' # set endFrame to *(endFrame - 1)
    asmInstruction += 'A=M \n'
    asmInstruction += 'D=M \n'
    asmInstruction += f'{curAddress} \n'
    asmInstruction += 'M=D \n'

  # goto Return address
  asmInstruction += '@R14 \n'
  asmInstruction += 'A=M \n' # return address
  asmInstruction += '0;JMP \n' # goto return address

  return asmInstruction
  

def writeBranchingAsmInstruction(conditional, label):
  asmInstruction = ''
  if (conditional == 'label'):
    asmInstruction += f'({label}) \n'
  elif (conditional == 'goto'):
    asmInstruction += f'@{label} \n' # set address to destination label
    asmInstruction += '0;JMP \n' # jump
  elif (conditional == 'if-goto'):
    asmInstruction += '@SP \n'
    asmInstruction += 'M=M-1 \n' # deduct stack pointer by 1 as we consume it
    asmInstruction += 'A=M \n'
    asmInstruction += 'D=M \n' # top value in the stack
    asmInstruction += f'@{label} \n' # set address to destination label
    asmInstruction += 'D;JNE \n' # jump
  else:
    raise Exception('Error in Branch instruction! Invalid conditional - ', conditional)

  return asmInstruction

def parseVMInstruction(line):
  line = line.split('//')[0] # remove comments, if any
  line = line.strip() # remove left and right whitespace

  if (len(line) == 0 or line.isspace()): # empty line, skip
    return 0
  
  asmInstruction = ''

  vmInstruction = line.split(' ')
  if (vmInstruction[0] == 'push'): # push instruction
    # vmInstruction example = ['push', 'constant', '2']
    # example2 = ['goto', 'LABEL']
    asmInstruction = writePushASMInstruction(vmInstruction[1], vmInstruction[2])
  elif (vmInstruction[0] == 'pop'): #pop instruction
    asmInstruction = writePopASMInstruction(vmInstruction[1], vmInstruction[2])
  elif (vmInstruction[0] in ['label', 'goto', 'if-goto']):
    asmInstruction = writeBranchingAsmInstruction(vmInstruction[0], vmInstruction[1])
  elif (vmInstruction[0] == 'function'):
    asmInstruction = writeFunctionASMInstruction(vmInstruction[1], vmInstruction[2])
  elif (vmInstruction[0] == 'call'):
    asmInstruction = writeCallASMInstruction(vmInstruction[1], vmInstruction[2])
  elif (vmInstruction[0] == 'return'):
    asmInstruction = writeReturnASMInstruction()
  else: # else its a arithmetic op
    asmInstruction = writeArithmeticASMInstruction(vmInstruction[0])
  
  return asmInstruction

def main():
  outputName = os.path.join(dirName, os.path.basename(dirName)) 
  with open(f'{outputName}.asm', 'w') as outputFile:
     # bootstrap code, set @SP to 256, call Sys.init
    outputFile.write('@256 \n')
    outputFile.write('D=A \n')
    outputFile.write('@SP \n')
    outputFile.write('M=D \n')
    outputFile.write(parseVMInstruction('call Sys.init 0'))
    outputFile.write('\n')
    for fileName in os.listdir(dirName):
      if fileName.endswith('.vm'): # only operate on .VM files
        curVMFile = os.path.join(dirName, fileName) 
        with open(f'{curVMFile}', 'r') as inputFile:
          outputFile.write(f'// cur file: {fileName} \n')
          for line in inputFile:
            asmInstruction = parseVMInstruction(line)

            if asmInstruction:
              global curVMLine
              curVMLine += 1
              outputFile.write(asmInstruction)
              outputFile.write('\n')

try:
  dirName = 'FunctionCalls/StaticsTest' #sys.argv[1]
except:

  print('Please provide a filename as a command line argument')

main()