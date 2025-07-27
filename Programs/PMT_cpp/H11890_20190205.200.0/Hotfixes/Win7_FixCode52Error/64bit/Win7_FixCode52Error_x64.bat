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
if %OS%==32BIT goto warnthenexit

echo ***************************
echo ** Installing root digital signatures
echo ***************************
..\..\rootsupd\AMD64-all-rootsupd.exe

dism /online /get-packages | findstr KB2921916 > %TEMP%\KB2921916.txt
FOR /F "usebackq delims=: tokens=2" %%i IN (%TEMP%\KB2921916.txt) DO set kb2921916=%%i
echo %kb2921916% | find "2921916" > nul
if %ERRORLEVEL% == 0 goto skip_kb2921916
echo ***************************
echo ** Installing KB2921916. **
echo ***************************
%windir%\System32\wusa.exe ..\..\\KB2921916\Windows6.1-KB2921916-x64.msu /quiet /norestart
set restartwin=1
:skip_kb2921916

dism /online /get-packages | findstr KB3033929 > %TEMP%\KB3033929.txt
FOR /F "usebackq delims=: tokens=2" %%i IN (%TEMP%\KB3033929.txt) DO set kb3033929=%%i
echo %kb3033929% | find "3033929" > nul
if %ERRORLEVEL% == 0 goto skip_kb3033929
echo ***************************
echo ** Installing KB3033929. **
echo ***************************
%windir%\System32\wusa.exe ..\..\\KB3033929\Windows6.1-KB3033929-x64.msu /quiet /norestart
set restartwin=1
:skip_kb3033929

if %restartwin% == 0 goto exit
echo **************************************
echo ** Please restart Windows manually. **
echo **************************************
goto exit

:warnthenexit
echo ********************
echo ** Not supported. **
echo ********************

:exit
del /q  %TEMP%\osname.txt
del /q  %TEMP%\KB2921916.txt
del /q  %TEMP%\KB3033929.txt
pause
popd
