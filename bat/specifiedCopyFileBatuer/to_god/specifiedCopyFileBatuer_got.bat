@echo off
REM ===========================================================================
REM
REM ドロップしたファイルを所定の場所へ強制的に上書きしてコピーするバッチ
REM
REM ===========================================================================

REM 遅延環境変数の設定
setlocal enabledelayedexpansion

REM ファイルパス情報を元にファイルコピー
set TXTFILE=%~dp0%~n0.txt
echo 以下の設定.txtファイルを読み込みました
echo   : !TXTFILE!
echo;

if "%*" EQU "" (
    echo ドロップデータの変数がNULLのため処理を終了します。
    echo;
    endlocal && pause && exit /b 1
)

set USER_INPUT=
set /P USER_INPUT="指定した先にコピーを実行しますか？ (y/n) : "
echo;

if not !USER_INPUT!==y (
    if !USER_INPUT!==n (
        echo "n"が入力されたため処理を終了します。
    ) else (
        echo "y/n"以外の文字が入力されたため処理を終了します。
    )
    echo;
    endlocal && pause && exit /b 1
)

for /f "delims=; tokens=1" %%a in (!TXTFILE!) do (
    set COPYTOPATH=%%a
    if exist !COPYTOPATH!\ (
        echo Copy to path : !COPYTOPATH!
        echo;
        call :RUN_FILE_COPY %*
        echo;
    )
)

echo コピーが完了しました。
echo;
endlocal && pause && exit /b 0

REM ===========================================================================
REM
REM サブルーチンリスト
REM
REM ===========================================================================

:RUN_FILE_COPY
REM ---------------------------------------------------------------------------
REM ドロップされたファイルごとにコピーを実行
for %%f in (%*) do (
    set SRCFILEPATH=%%f
    call :EXE_BASENAME !SRCFILEPATH!
    set DSTFILEPATH=!COPYTOPATH!\!BASE_NAME!
    REM echo - src path : !SRCFILEPATH!
    REM echo - dst path : !DSTFILEPATH!
    echo Copy file : !BASE_NAME!
    copy !SRCFILEPATH! !DSTFILEPATH! /Y
)
exit /b

:EXE_BASENAME
REM ---------------------------------------------------------------------------
REM 送られてきたパラメータのファイル名だけを取得
set BASE_NAME=%~nx1
exit /b

:EOF
exit /b

REM ===========================================================================
REM END