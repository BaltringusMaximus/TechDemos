@echo off
set YYYYMMDD=%date:~6,4%%date:~3,2%%date:~0,2%
set rejected=E:\sys\Rejected
echo %YYYYMMDD%
cd %YYYYMMDD%
set dailyfolder=%cd%
:a
echo %time%
ROBOCOPY %rejected% %dailyfolder% /mov
timeout 300 > NUL
goto :a
pause
@exit
