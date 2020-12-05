@echo off
@set ENTRANCE_CURRENT_PATH=%~dp0
@echo 以下の名前のUIを起動します : %1
@echo;

if "%MS_DEBUG_FLAG%" == "1" (
    @echo Entrance path  = "%0"
    @echo Start gui name = "%1"
    @echo Python version = "%2"
    @echo;
)

if "%2" == "" (
    @echo Pythonバージョンが指定されていません。37を設定します。
    @set PYTHON_START_VERSION=37
) else (
    @echo 指定されたPythonバージョンを設定します。
    @echo Version : "%2"
    @set PYTHON_START_VERSION=%2
)
@echo;

if "%COMPANY%" == "StudioGOONEYS,Inc." (
    @set STARTUP_PYTHON_PATH=%PROGRAMDATA%\gooneys\soft\python\
    @set PYTHONPATH=%GN_PYTHON_DEFLINK%;%GN_COMPANY_LOCAL_PATH%\soft\python2.7\Lib\site-packages
) else (
    @set STARTUP_PYTHON_PATH=C:\Python%PYTHON_START_VERSION%\
)

@echo Entrance path : "%ENTRANCE_CURRENT_PATH%"
@echo Python path   : "%STARTUP_PYTHON_PATH%"
@echo;

if "%*" EQU "" (
    @echo このバッチファイルが直接実行されました。
    pause
) else (
    %STARTUP_PYTHON_PATH%python.exe %ENTRANCE_CURRENT_PATH%entrance.py %1
)
exit /b