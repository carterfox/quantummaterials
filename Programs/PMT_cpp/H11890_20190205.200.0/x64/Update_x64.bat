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
        echo.
        if not exist %windir%\system32\difxapi.dll (
             if "%1"=="" robocopy .\ %windir%\system32 difxapi.dll /XC /XN /XO >NUL
        )
        ..\UPDATE_x64.exe oem usedriverstore -i:h11890.inf %1
        echo.
        echo Done.
        echo.
    ) else (
        echo.
        echo ********************
        echo ** Not supported. **
        echo ********************
        echo.
    )
) else (
    echo.
    echo *********************************
    echo ** Please Run as administrator **
    echo *********************************
    echo.
)
pause
popd