@256 
D=A 
@SP 
M=D 
@LABEL0 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@LCL 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@ARG 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@THIS 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@THAT 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@SP 
D=M 
@5 
D=D-A 
@0 
D=D-A 
@ARG 
M=D 
@SP 
D=M 
@LCL 
M=D 
@Sys.init 
0;JMP 
(LABEL0) 

// cur file: Class1.vm 
(Class1.set) 

@0 
D=A 
@ARG 
A=D+M 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@SP 
A=M-1 
D=M 
@var.0 
M=D 
@SP 
M=M-1 

@1 
D=A 
@ARG 
A=D+M 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@SP 
A=M-1 
D=M 
@var.1 
M=D 
@SP 
M=M-1 

@0 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@LCL 
D=M 
@R15 
M=D 
@5 
A=D-A 
D=M 
@R14 
M=D 
@SP 
A=M-1 
D=M 
@ARG 
A=M 
M=D 
D=A 
@SP 
M=D+1 
@R15 
M=M-1 
A=M 
D=M 
@THAT 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@THIS 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@ARG 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@LCL 
M=D 
@R14 
A=M 
0;JMP 

(Class1.get) 

@var.0 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@var.1 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@SP 
A=M-1 
D=M 
A=A-1 
M=M-D 
@SP 
M=M-1 

@LCL 
D=M 
@R15 
M=D 
@5 
A=D-A 
D=M 
@R14 
M=D 
@SP 
A=M-1 
D=M 
@ARG 
A=M 
M=D 
D=A 
@SP 
M=D+1 
@R15 
M=M-1 
A=M 
D=M 
@THAT 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@THIS 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@ARG 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@LCL 
M=D 
@R14 
A=M 
0;JMP 

// cur file: Class2.vm 
(Class2.set) 

@0 
D=A 
@ARG 
A=D+M 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@SP 
A=M-1 
D=M 
@var.0 
M=D 
@SP 
M=M-1 

@1 
D=A 
@ARG 
A=D+M 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@SP 
A=M-1 
D=M 
@var.1 
M=D 
@SP 
M=M-1 

@0 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@LCL 
D=M 
@R15 
M=D 
@5 
A=D-A 
D=M 
@R14 
M=D 
@SP 
A=M-1 
D=M 
@ARG 
A=M 
M=D 
D=A 
@SP 
M=D+1 
@R15 
M=M-1 
A=M 
D=M 
@THAT 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@THIS 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@ARG 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@LCL 
M=D 
@R14 
A=M 
0;JMP 

(Class2.get) 

@var.0 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@var.1 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@SP 
A=M-1 
D=M 
A=A-1 
M=M-D 
@SP 
M=M-1 

@LCL 
D=M 
@R15 
M=D 
@5 
A=D-A 
D=M 
@R14 
M=D 
@SP 
A=M-1 
D=M 
@ARG 
A=M 
M=D 
D=A 
@SP 
M=D+1 
@R15 
M=M-1 
A=M 
D=M 
@THAT 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@THIS 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@ARG 
M=D 
@R15 
M=M-1 
A=M 
D=M 
@LCL 
M=D 
@R14 
A=M 
0;JMP 

// cur file: Sys.vm 
(Sys.init) 

@6 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@8 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@LABEL27 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@LCL 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@ARG 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@THIS 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@THAT 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@SP 
D=M 
@5 
D=D-A 
@2 
D=D-A 
@ARG 
M=D 
@SP 
D=M 
@LCL 
M=D 
@Class1.set 
0;JMP 
(LABEL27) 

@SP 
A=M-1 
D=M 
@0 
D=A 
@5 
D=D+A 
@R13 
M=D 
@SP 
A=M-1 
D=M 
@R13 
A=M 
M=D 
@SP 
M=M-1 

@LABEL29 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@LCL 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@ARG 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@THIS 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@THAT 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@SP 
D=M 
@5 
D=D-A 
@0 
D=D-A 
@ARG 
M=D 
@SP 
D=M 
@LCL 
M=D 
@Class1.get 
0;JMP 
(LABEL29) 

@23 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@15 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1 

@LABEL32 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@LCL 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@ARG 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@THIS 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@THAT 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@SP 
D=M 
@5 
D=D-A 
@2 
D=D-A 
@ARG 
M=D 
@SP 
D=M 
@LCL 
M=D 
@Class2.set 
0;JMP 
(LABEL32) 

@SP 
A=M-1 
D=M 
@0 
D=A 
@5 
D=D+A 
@R13 
M=D 
@SP 
A=M-1 
D=M 
@R13 
A=M 
M=D 
@SP 
M=M-1 

@LABEL34 
D=A 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@LCL 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@ARG 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@THIS 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@THAT 
D=M 
@SP 
A=M 
M=D 
@SP 
M=M+1 
@SP 
D=M 
@5 
D=D-A 
@0 
D=D-A 
@ARG 
M=D 
@SP 
D=M 
@LCL 
M=D 
@Class2.get 
0;JMP 
(LABEL34) 

(WHILE) 

@WHILE 
0;JMP 

