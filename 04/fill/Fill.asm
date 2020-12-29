// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)

@8191
D=A
@i // 8000 blocs of memory belong to the screen
M=D

@24576 // keyboard memory address
D=M
@BLACKENLOOP
D;JNE // keyboard != 0, is pressed, blacken screen

(WHITENLOOP) // set @SCREEN + 8000 to 0, @SCREEN + 7999 to 0, ... ,@SCREEN + 0 to 0
@i
D=M
@LOOP // if i is < 0, done with setting screen to white
D;JLT

@SCREEN // screen base address
A=A+D // new address to current location @SCREEN + i
M=0 // current pixel to white

@i // decrement counter by 1
M=M-1

@WHITENLOOP
0;JMP

(BLACKENLOOP) // set @SCREEN + 8000 to -1, @SCREEN + 7999 to -1, ... ,@SCREEN + 0 to -1
@i
D=M
@LOOP // if i is < 0, done with setting screen to black
D;JLT

@SCREEN // screen base address
A=A+D // new address to current location @SCREEN + i
M=-1 // current pixel to black

@i // decrement counter by 1
M=M-1

@BLACKENLOOP
0;JMP


@LOOP
0;JMP