
keywordList = ['class','constructor','function' ,
'method','field','static','var' ,
'int','char','boolean','void','true' ,
'false','null','this','let','do' ,
'if','else','while','return']
symbolList = ['{','}','(',')','[',']','.' ,
',',';', '+' , '-','*','/','&' ,
'|','<','>','=','~']

opList = ['+','-','*','/','&','|','<','>','=', '&lt;','&gt;','&quot;','&amp;']

unaryOpList = ['-','~']
keywordConstantList = ['true','false','null','this']

class CompilationEngine:
  def __init__(self, tokenizer, fileName):
    self.tokenizer = tokenizer
    self.fileName = fileName
    self.file = open(f'{fileName[:-5]}Parsed.xml', "w")

    self.compileClass()

    self.file.close()

  def eat(self, *expectedToken):
    curToken = self.tokenizer.advance()

    if (curToken in expectedToken or '^' in expectedToken): # '^' for identifiers, e.g classnames
      if curToken in keywordList:
        self.output(f'<keyword> {curToken} </keyword>')
      elif curToken in symbolList:
        self.output(f'<symbol> {curToken} </symbol>')
      else:
        self.output(f'<identifier> {curToken} </identifier>')
      return True
    else:
      return False

  def output(self, outputStr):
    self.file.write(f'{outputStr} \n')

  def compileClass(self):
    self.output('<class>')
    self.eat('class')
    self.eat('^') # classname
    self.eat('{')
    while self.tokenizer.peekAhead() in ['static', 'field']:
      self.compileClassVarDec()
    while self.tokenizer.peekAhead() in ['constructor', 'function', 'method']:
      self.compileSubroutine()
    self.eat('}')
    self.output('</class>')

  def compileClassVarDec(self):
    self.output('<classVarDec>')
    self.eat('static', 'field')
    self.eat('^') # type
    self.eat('^') # varname
    while self.tokenizer.peekAhead() == ',': # there are more variables
      self.eat(',')
      self.eat('^')
    self.eat(';')
    self.output('</classVarDec>')

  def compileSubroutine(self):
    self.output('<subroutineDec>')
    self.eat('constructor', 'function', 'method')
    self.eat('void', '^')
    self.eat('^')
    self.eat('(')
    self.compileParameterList()
    self.eat(')')
    self.compileSubroutineBody()
    self.output('</subroutineDec>')

  def compileParameterList(self):
    self.output('<parameterList>')
    if (self.tokenizer.peekAhead() != ')'): # there are parameters
      self.eat('^') # type
      self.eat('^') # varname
      while self.tokenizer.peekAhead() == ',': # there are more variables
        self.eat(',')
        self.eat('^') # type
        self.eat('^') # varname
    self.output('</parameterList>')

  def compileSubroutineBody(self):
    self.output('<subroutineBody>')
    self.eat('{')
    while (self.tokenizer.peekAhead() == 'var'): # there are var decs
      self.compileVarDec()
    self.compileStatements()
    self.eat('}')
    self.output('</subroutineBody>')

  def compileVarDec(self):
    self.output('<varDec>')
    self.eat('var')
    self.eat('^') # type
    self.eat('^') # varname
    while self.tokenizer.peekAhead() == ',': # there are more variables
        self.eat(',')
        self.eat('^') # varname
    self.eat(';')
    self.output('</varDec>')

  def compileStatements(self):
    self.output('<statements>')
    while(self.tokenizer.peekAhead() in ['let','if','while','do','return']):
      if self.tokenizer.peekAhead() == 'let':
        self.compileLet()
      if self.tokenizer.peekAhead() == 'if':
        self.compileIf()
      if self.tokenizer.peekAhead() == 'while':
        self.compileWhile()
      if self.tokenizer.peekAhead() == 'do':
        self.compileDo()
      if self.tokenizer.peekAhead() == 'return':
        self.compileReturn()
    self.output('</statements>')

  def compileLet(self):
    self.output('<letStatement>')
    self.eat('let')
    self.eat('^') # varname
    if self.tokenizer.peekAhead() == '[': # its an array entry!
      self.eat('[')
      self.compileExpression()
      self.eat(']')
    self.eat('=')
    self.compileExpression()
    self.eat(';')
    self.output('</letStatement>')

  def compileIf(self):
    self.output('<ifStatement>')
    self.eat('if')
    self.eat('(')
    self.compileExpression()
    self.eat(')')
    self.eat('{')
    self.compileStatements()
    self.eat('}')
    if self.tokenizer.peekAhead() == 'else': # else statement
      self.eat('else')
      self.eat('{')
      self.compileStatements()
      self.eat('}')
    self.output('</ifStatement>')

  def compileWhile(self):
    self.output('<whileStatement>')
    self.eat('while')
    self.eat('(')
    self.compileExpression()
    self.eat(')')
    self.eat('{')
    self.compileStatements()
    self.eat('}')
    self.output('</whileStatement>')

  def compileDo(self):
    self.output('<doStatement>')
    self.eat('do')
    self.compileSubroutineCall()
    self.eat(';')
    self.output('</doStatement>')

  def compileReturn(self):
    self.output('<returnStatement>')
    self.eat('return')
    if self.tokenizer.peekAhead() != ';': # there is an expression
      self.compileExpression()
    self.eat(';')
    self.output('</returnStatement>')

  def compileExpression(self):
    self.output('<expression>')
    self.compileTerm()
    while self.tokenizer.peekAhead() in opList: # op
      self.output(f'<symbol> {self.tokenizer.advance()} </symbol>')
      self.compileTerm()
    self.output('</expression>')

  def compileTerm(self):
    self.output('<term>')
    self.tokenizer.peekAhead()
    if self.tokenizer.nextTokenType == 'integerConstant':
      self.output(f'<integerConstant> {self.tokenizer.advance()} </integerConstant>')
    elif self.tokenizer.nextTokenType == 'stringConstant':
      self.output(f'<stringConstant> {self.tokenizer.advance()} </stringConstant>')
    elif self.tokenizer.peekAhead() in keywordConstantList:
      self.output(f'<keyword> {self.tokenizer.advance()} </keyword>')
    else: # varname
      nextNextToken = self.tokenizer.peekAhead(2)
      if (self.tokenizer.peekAhead() in unaryOpList):
        self.output(f'<symbol> {self.tokenizer.advance()} </symbol>')
        self.compileTerm() # term
      elif (self.tokenizer.peekAhead() == '('):
        self.eat('(')
        self.compileExpression()
        self.eat(')')
      elif (nextNextToken == '['):
        self.eat('^') #varname
        self.eat('[')
        self.compileExpression()
        self.eat(']') #varname
      elif (nextNextToken in ['[', '.']): #subroutine call
        self.compileSubroutineCall()
      else: # just a varname
        self.eat('^')
    self.output('</term>')
    pass

  def compileSubroutineCall(self):
    self.eat('^')
    if self.tokenizer.peekAhead() == '(':
      self.eat('(')
      self.compileExpressionList()
      self.eat(')')
    elif self.tokenizer.peekAhead() == '.':
      self.eat('.')
      self.eat('^')
      self.eat('(')
      self.compileExpressionList()
      self.eat(')')

  def compileExpressionList(self):
    self.output('<expressionList>')
    if self.tokenizer.peekAhead() != ')': # there are expressions
      self.compileExpression()
    while self.tokenizer.peekAhead() == ',': # more expressions
      self.eat(',')
      self.compileExpression()
    self.output('</expressionList>')
  


