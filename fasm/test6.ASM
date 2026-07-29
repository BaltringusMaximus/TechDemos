format pe64 console
entry start
section '.text' code readable executable
start:
org 100h
; Message 1
mov ah,09
mov dx,msg
int 21h
; Message 2
; LOL
mov ah,09
mov dx,msg2
int 21h
mov ah,08
int 21h
; ENd
int 20h
msg db "hello world!$", 0Dh, 0Ah, 0
msg2 db "made by Josh!$", 0Dh, 0Ah, 0