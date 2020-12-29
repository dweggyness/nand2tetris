// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@R0
D=M
@R2 // initialize R2 to 0
M=0
@i // set counter variable to RAM[0]
M=D

(LOOP) // add RAM[1] to RAM[2], RAM[0] times
@i
D=M
@END // if J is <= 0, end program
D;JLE

@i // else reduce count of additions left
M=M-1

@R1
D=M
@R2 // add RAM[1] to RAM[2]
M=D+M

@LOOP // repeat
0;JMP

(END)
@END
0;JMP