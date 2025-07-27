@echo off
setlocal
pushd %~dp0
set restartwin=0
if not exist %SystemRoot%\system32\systeminfo.exe goto warnthenexit
systeminfo | find "Microsoft Windows" > %TEMP%\osname.txt
FOR /F "usebackq delims=: tokens=2" %%i IN (%TEMP%\osname.txt) DO set vers=%%i
echo %vers% | find "Windows 7" > nul
if %ERRORLEVEL% == 0 goto ver_7
goto warnthenexit

:ver_7
reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT
if %OS%==32BIT call 32bit\Win7_FixCode52Error_x86
if %OS%==64BIT call 64bit\Win7_FixCode52Error_x64
goto exit

:warnthenexit
echo ********************
echo ** Not supported. **
echo ********************
pause

:exit
del /q  %TEMP%\osname.txt
del /q  %TEMP%\KB2921916.txt
del /q  %TEMP%\KB3033929.txt
popd
