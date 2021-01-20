import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

dirName = 'ArrayTest'

def main():
  for fileName in os.listdir(dirName):
    if fileName.endswith('.jack'): # only operate on .jack files
      curJackFile = os.path.join(dirName, fileName) 
      tokenizer = JackTokenizer(curJackFile)
      CompilationEngine(tokenizer, curJackFile)

main()

