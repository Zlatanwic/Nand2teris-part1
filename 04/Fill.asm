// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
(LOOP)
    @KBD
    D=M
    @FILL
    D;JNE        // 有输入时跳转FILL

    // 清除屏幕（CLEAR）
    @i
    M=0          // i=0
(CLEAR_LOOP)
    @i
    D=M
    @8192        // 关键修正：检查8192次循环
    D=D-A
    @LOOP
    D;JEQ        // 当i==8192时结束循环

    @SCREEN
    D=A
    @i
    A=D+M        // 计算SCREEN + i
    M=0          // 清除当前字

    @i
    M=M+1        // i++
    @CLEAR_LOOP
    0;JMP

(FILL)
    @i
    M=0          // i=0
(FILL_LOOP)
    @i
    D=M
    @8192        // 关键修正：检查8192次循环
    D=D-A
    @LOOP
    D;JEQ        // 当i==8192时结束循环

    @SCREEN
    D=A
    @i
    A=D+M        // 计算SCREEN + i
    M=-1         // 填充当前字为黑色

    @i
    M=M+1        // i++
    @FILL_LOOP
    0;JMP