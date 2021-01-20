import re

keywordList = ['class','constructor','function' ,
'method','field','static','var' ,
'int','char','boolean','void','true' ,
'false','null','this','let','do' ,
'if','else','while','return']
symbolList = ['{','}','(',')','[',']','.' ,
',',';', '+' , '-','*','/','&' ,
'|','<','>','=','~']
specialSymbolMapping = {
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  '&': '&amp;',
}

class JackTokenizer:
  def __init__(self, fileName):
    self.hasMoreTokens = True
    self.curTokenIndex = 0
    self.curToken = ""
    self.curTokenType = ""
    self.nextTokenType = ""

    self.tokenList = []
    
    with open(fileName, 'r') as file:
      tokens = self.tokenizeFile(file)
      if tokens:
        with open(f'{fileName[:-5]}Tokens.xml', 'w') as outputFile:
          outputFile.write('<tokens> \n')
          for token in tokens:
            self.tokenList.append(token)
            outputFile.write(f'{token} \n')
          outputFile.write('</tokens> \n')

          

  def tokenizeFile(self, file):
    tokenList = []
    isInComment = False 
    clearIsInComment = False
    for line in file: # tokenize line-by-line
      line = line.split('//')[0] # remove single line comments, if any

      if '/**' in line: # has a multiline comment
        isInComment = True
      if '*/' in line: # end of multiline comment
        clearIsInComment = True

      if isInComment: # dont parse tokenize line if still in multiline comment
        pass
      else:
        line = line.strip() # remove left and right whitespace

        if (len(line) == 0 or line.isspace()): # empty line, skip
          continue

        # try:
        tokens = self.tokenizeString(line)
        if tokens:
          for token in tokens:
            tokenList.append(token)
        # except:
         #  print(f'Error in line {line} in file {file}')
        
      if clearIsInComment:
        isInComment = False
        clearIsInComment = False

    return tokenList

  def tokenizeString(self, line): # tokenizes a whitespaceless string, returns an Array of token strings
    tokenList = []
    if not line: # empty?
      return None
    else: 
      curString = ""
      isStringConstant = False
      for char in line:
        if char == ' ' and not isStringConstant: # reach a whitespace, and its not a string constant
          if curString:
            if curString in keywordList:
              tokenList.append(f'<keyword> {curString} </keyword>')
            elif curString[0].isnumeric(): # its an int constant
              tokenList.append(f'<integerConstant> {curString} </integerConstant>')
            else:
              tokenList.append(f'<identifier> {curString} </identifier>') # previous string is identifier
          curString = ''
        elif char not in symbolList: # count_Of_3Dogs
          curString += char
          if char in ['"', "'"]: # dont stop at whitespace if its a str constant
            if isStringConstant: # end of string constant, second double quotation
              curString = curString.strip('"').strip("'")
              tokenList.append(f'<stringConstant> {curString} </stringConstant>')
              isStringConstant = False
              curString = ""
            else:
              isStringConstant = True
        else: # else in symbol list
          if curString:
            if curString in keywordList:
              tokenList.append(f'<keyword> {curString} </keyword>')
            elif curString[0].isnumeric(): # its an int constant
              tokenList.append(f'<integerConstant> {curString} </integerConstant>')
            else:
              tokenList.append(f'<identifier> {curString} </identifier>') # previous string is identifier
          if char in specialSymbolMapping:
            tokenList.append(f'<symbol> {specialSymbolMapping[char]} </symbol>') # current symbol
          else:
            tokenList.append(f'<symbol> {char} </symbol>') # current symbol
          curString = ""
      if curString:
        tokenList.append(f'<identifier> {curString} </identifier>') # previous string is identifier
    return tokenList

  def advance(self): # returns the next token while advancing the input
    nextItem = self.tokenList[self.curTokenIndex]
    nextItemSplit = re.split('[<>]', nextItem)
    # ['', 'keyword', 'return', '/keyword', '']
    self.curTokenType = nextItemSplit[1]
    self.curToken = nextItemSplit[2].strip()
    nextToken = self.curToken

    self.curTokenIndex += 1
    if (self.curTokenIndex == len(self.tokenList)):
      self.hasMoreTokens = False

    return nextToken

  def peekAhead(self, num = 1): # gets the n-th next token without advancing the input
    nextItem = self.tokenList[self.curTokenIndex + num - 1]
    nextItemSplit = re.split('[<>]', nextItem)
    # ['', 'keyword', 'return', '/keyword', '']
    self.nextTokenType = nextItemSplit[1]
    nextToken = nextItemSplit[2].strip()

    return nextToken


  def tokenType(self):
    return self.curTokenType
