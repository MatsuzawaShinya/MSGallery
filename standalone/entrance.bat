@echo off
@set ENTRANCE_CURRENT_PATH=%~dp0
@echo �ȉ��̖��O��UI���N�����܂� : %1
@echo;

if "%MS_DEBUG_FLAG%" == "1" (
    @echo Entrance path  = "%0"
    @echo Start gui name = "%1"
    @echo Python version = "%2"
    @echo;
)

if "%2" == "" (
    @echo Python�o�[�W�������w�肳��Ă��܂���B37��ݒ肵�܂��B
    @set PYTHON_START_VERSION=37
) else (
    @echo �w�肳�ꂽPython�o�[�W������ݒ肵�܂��B
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
    @echo ���̃o�b�`�t�@�C�������ڎ��s����܂����B
    pause
) else (
    %STARTUP_PYTHON_PATH%python.exe %ENTRANCE_CURRENT_PATH%entrance.py %1
)
exit /b