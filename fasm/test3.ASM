format pe64 console
entry start

STD_OUTPUT_HANDLE       = -11

section '.text' code readable executable

start:
        sub     rsp,8*7         ; reserve stack for API use and make stack dqword aligned
        mov     rcx,STD_OUTPUT_HANDLE
        call    [GetStdHandle]
        mov     rcx,rax
        lea     rdx,[message]
        mov     r8d,message_length
        lea     r9,[rsp+4*8]
        mov     qword[rsp+4*8],0
        call    [WriteFile]
        mov     ecx,eax
        call    [ExitProcess]

section '.data' data readable writeable

message         db 'Hello World!',0
message_length  = $ - message

section '.idata' import data readable writeable

        dd      0,0,0,RVA kernel_name,RVA kernel_table
        dd      0,0,0,0,0

kernel_table:
        ExitProcess     dq RVA _ExitProcess
        GetStdHandle    dq RVA _GetStdHandle
        WriteFile       dq RVA _WriteFile
                        dq 0

kernel_name     db 'KERNEL32.DLL',0
user_name       db 'USER32.DLL',0

_ExitProcess    db 0,0,'ExitProcess',0
_GetStdHandle   db 0,0,'GetStdHandle',0
_WriteFile      db 0,0,'WriteFile',0