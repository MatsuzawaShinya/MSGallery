@echo off

@set USER_INPUT_GUINAME=
@set /P USER_INPUT_GUINAME="‹N“®‚·‚éUI‚Ì–¼‘O: "

pushd %~dp0
@set BAT_DIR_PATH=%CD%
popd
@call :get_python_version %BAT_DIR_PATH%

pushd %~dp0..\..
@set STANDALONE_PATH=%CD%
popd
@call %STANDALONE_PATH%\entrance.bat %USER_INPUT_GUINAME% %PYTHON_VERSION%

if "%MS_DEBUG_FLAG%" == "1" (
    pause
)
exit /b

:get_python_version
@set PYTHON_VERSION=%~n1
exit /b 1