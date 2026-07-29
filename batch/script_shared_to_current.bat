@echo off
echo 1: misaki nakahara
echo 1: enma ai
echo 1: akame
echo 1: lain
echo 1: rei ayanami
echo 1: flandre scarlett
echo 1: raimu hakurei
echo 1: nue hujuu
echo 1: hachikuji
echo 1: shuvi 
cd /d E:\sys
set YYYYMMDD=%date:~6,4%%date:~3,2%%date:~0,2%
echo %YYYYMMDD%
mkdir %YYYYMMDD%
cd %YYYYMMDD%
set dailyfolder=%cd%
cd /d S:\PNG
echo %YYYYMMDD%
cd %YYYYMMDD%
set shared=%cd%
cd /d I:\sys
echo %YYYYMMDD%
mkdir %YYYYMMDD%
cd %YYYYMMDD%
set activefolder=%cd%
@echo on
echo activefolder=%activefolder%
echo shared=%shared%
echo dailyfolder=%dailyfolder%
@echo off
timeout 1 > NUL
:a
echo %time%
ROBOCOPY %shared% %activefolder%
ROBOCOPY %shared% %dailyfolder% /mov
timeout 60 > NUL
goto :a
pause
@exit
