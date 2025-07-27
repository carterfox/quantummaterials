@echo off
setlocal
pushd %~dp0
set _os_bitness=64
if %PROCESSOR_ARCHITECTURE%==x86 (
    if not defined PROCESSOR_ARCHITEW6432 set _os_bitness=32
)   
net session >nul 2>&1
if %errorLevel% == 0 (
    if %_os_bitness%==64 (
        call x64\Update_x64
    ) else (
        call x86\Update_x86
    )
) else (
    echo.
    echo *********************************
    echo ** Please Run as administrator **
    echo *********************************
    echo.
    pause
)
popd