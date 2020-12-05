@echo off

REM コマンドプロンプトを隠す
if not "%MS_DEBUG_FLAG%" == "1" (
    if not "%~0" == "%~dp0.\%~nx0" (
        start /min cmd /c, "%~dp0.\%~nx0" %*
        exit
    )
)

REM ファイル名を取得
@call :get_file_name %~0

REM Pythonバージョンをパスから取得
pushd %~dp0
@set BAT_DIR_PATH=%CD%
popd
@call :get_python_version %BAT_DIR_PATH%

REM ウインドウを起動
pushd %~dp0..\..
@set STANDALONE_PATH=%CD%
popd
@call %STANDALONE_PATH%\entrance.bat %FILE_NAME% %PYTHON_VERSION%

if "%MS_DEBUG_FLAG%" == "1" (
    pause
)
exit /b

REM ---------------------------------------------------------------------------
REM ラベル

:get_python_version
@set PYTHON_VERSION=%~n1
exit /b 1

:get_file_name
@set FILE_NAME=%~n1
exit /b 1