format pe64 console
entry start

STD_OUTPUT_HANDLE       = -11

section '.text' code readable executable

start:
;        int3
        call test_function
;        push 0FF
        sub     rsp,8
;        int3
        lea     rcx, [memory_slot]
        mov     [rsp],rcx
        mov     rax, 123456789ABCDEFh
;        mov     [rsp], rax
        mov     qword [memory_slot],rax
        sub     rsp, 16
        lea     rcx, [memory_slot]
        add     rcx, 8
        mov     [rsp+8], rcx
        mov     qword [rsp], 08h
        mov     rcx, [rsp+8]
;        lea     [rsp],qword [memory_slot]
        mov     rax, 0FEDCBA9876543210h
        mov     [rcx], rax

        mov     [float],rax
        mov     [memory_slot],al
        mov     rax,[float+1]
        mov     [memory_slot+1],al
        mov     rax,[float+2]
        mov     [memory_slot+2],al
        mov     rax,[float+3]
        mov     [memory_slot+3],al
        mov     [integer],ax
        mov     ax,[integer]
        mov     [memory_slot],al
        mov     ax,[integer+1]
        mov     [memory_slot+1],al
;        movsx   ax,al
;        lea     rax,[memory_slot]
        mov     [memory_slot+1],ah
;        shl     al,1
        mov     [memory_slot+2],al
        push    rax
        movsx   ax,al
;        mov     [memory_slot+2],db [rsi]
        add     al, 1
        add     al, 1
        add     al, 1
        mov     [memory_slot], 0
;        mov     al, 1
        mov     [memory_slot], ah
        shl     al,1
        mov     [memory_slot], al
        shl     al,1
        mov     [memory_slot], al
        shl     al,1
        mov     [memory_slot], al
        sub     rsp,8*7         ; reserve stack for API use and make stack dqword aligned
        mov     rcx,STD_OUTPUT_HANDLE
        call    [GetStdHandle]
        mov     rcx,rax
;        int3
        lea     rdx,[message]
        mov     r8d,message_length
        lea     r9,[rsp+4*8]
        mov     qword[rsp+4*8],0
        call    [WriteFile]
        mov     rcx,STD_OUTPUT_HANDLE
        call    [GetStdHandle]
        mov     rcx,rax
        lea     rdx,[message2]
        mov     r8d,message2_length
        lea     r9,[rsp+4*8]
        mov     qword[rsp+4*8],0
        call    [WriteFile]
        mov     rcx,STD_OUTPUT_HANDLE
        call    [GetStdHandle]
        mov     rcx,rax
        lea     rdx,[memory_slot+1]
        mov     r8d,1
        lea     r9,[rsp+4*8]
        mov     qword[rsp+4*8],0
        call    [WriteFile]
        mov     rcx,20000
        call    [Sleep]
        mov     ecx,eax
        call    [ExitProcess]

test_function:
        push    rbp
        mov     rbp,rsp
        pop     rbp
        ret

section '.heap' data readable writeable

memory_slot db 16384 dup(0FFh)

section '.types' data readable writeable

char    db 0AAh
integer dw 0AAh,0AAh
float   dq 0AAh,0AAh,0AAh,0AAh

section '.data' data readable writeable

message         db 'Hello World!',0Dh, 0Ah, "test again"
message2        db '\\n test',0
message_length  = $ - message
message2_length = $ - message2

section '.idata' import data readable writeable

        dd      RVA kernel_table,0,0,RVA kernel_name,RVA kernel_table
        dd      0,0,0,0,0

kernel_table:
        ExitProcess     dq RVA _ExitProcess
        GetStdHandle    dq RVA _GetStdHandle
        WriteFile       dq RVA _WriteFile
        Sleep           dq RVA _Sleep
                        dq 0

kernel_name     db 'KERNEL32.DLL',0
user_name       db 'USER32.DLL',0

_ExitProcess    db 0,0,'ExitProcess',0
_GetStdHandle   db 0,0,'GetStdHandle',0
_WriteFile      db 0,0,'WriteFile',0
_Sleep          db 0,0,'Sleep',0