@echo off
REM ===========================================================================
REM
REM 指定したディレクトリ内のファイル／ドロップファイルに
REM 日付(YYYYMMDD_)を付与してリネームするバッチ
REM
REM ===========================================================================

REM 遅延環境変数の設定
setlocal enabledelayedexpansion

if "%*" EQU "" (
    echo;
    echo バッチが直接実行されたため終了します。
    echo;
    endlocal && pause && exit /b 1
)

echo ディレクトリ内ファイル／ドロップファイルの先頭に日付を付与してリネームします。
echo 日付(YYYYMMDD_)が付与されている場合は処理をスキップします。
echo;
echo ( 1 ) : 今日の日付を付与してリネームします。
echo ( 2 ) : ファイルの更新日時を付与してリネームします。
echo ( 0 ) : 処理を中断します。
echo;

set USER_INPUT=
@set /P USER_INPUT="実行したいタイプの数字を入力してください。 (1/2/0) : "
echo;

if not "!USER_INPUT!"=="0" (
    if "!USER_INPUT!"=="1" (
        set INPUT_TYPE=!USER_INPUT!
    ) else if "!USER_INPUT!"=="2" (
        set INPUT_TYPE=!USER_INPUT!
    ) else (
        echo "1" "2" 以外が入力されたため処理を終了します。
        echo;
        call :EXE_EXET
    )
) else (
    echo "0"が入力されたため処理を終了します。
    echo;
    call :EXE_EXET
)

REM ディレクトリ判定をif existで行う場合、
REM ネットワークドライブにマウント(要確認)されている場合フォルダ判断が
REM 上手くいかないため、指定されたファイルアイテムのサイズで
REM ディレクトリ(0バイト)／ファイル(1バイト以上)で判断する。
for %%f in (%*) do (
    set SRCDATA=%%f
	set SIZE=%%~zf
    REM ディレクトリの処理
	if "!SIZE!"=="0" (
		for %%a in (!SRCDATA!\*) do (
            call :RENAME_FILE %%a
        )
    REM ファイルの処理
	) else (
		if exist !SRCDATA! (
			call :RENAME_FILE %%f
		)
	)
)

echo 全てのファイルのリネームが完了しました。
echo;
call :EXE_EXET

REM ===========================================================================
REM
REM サブルーチンリスト
REM
REM ===========================================================================

:RENAME_FILE
REM ---------------------------------------------------------------------------
REM 送られてきたファイルの先頭に今日の日付を付与してリネーム
for %%f in (%*) do (
    set SRCPATH=%%f
    call :EXE_DIRNAME !SRCPATH!
    call :EXE_BASENAME !SRCPATH!	
    
    if "!INPUT_TYPE!"=="1" (
        call :EXE_NOWDATE_INFO !SRCPATH!
    ) else (
        call :EXE_LASTUPDATE_INFO !SRCPATH!
    )
    
    set SRCNAME=!BASE_NAME!
    set DSTNAME=!NOW_DATE!!BASE_NAME!
    
    echo SRC PATH : !SRCPATH!
    REM 指定された日付フォーマットではない場合日付を付与しリネームする
    echo "!SRCNAME!" | findstr /R "[2][0][0-9][0-9][0-1][0-9][0-3][0-9]_">NUL
    if not "!ERRORLEVEL!"=="0" (
        REM リネーム先が同一の場合リネーム末尾に
        ren !SRCPATH! !DSTNAME!
        if not "!ERRORLEVEL!"=="0" (
            echo Rename "error".
            echo;
        ) else (
            set EXETYPE=finished
            call :FINISH_ECHO 1
        )
    ) else (
        set EXETYPE=skipped
        call :FINISH_ECHO 0
    )
)
exit /b

REM ---------------------------------------------------------------------------
REM 今日の日時から8桁(YYYYMMDD)のDATEを設定
:EXE_NOWDATE_INFO
set DATE_YEAR=!date:~0,4!
set DATE_MONTH=!date:~5,2!
set DATE_DAY=!date:~8,2!
set NOW_DATE=!DATE_YEAR!!DATE_MONTH!!DATE_DAY!_
exit /b

REM ---------------------------------------------------------------------------
REM ファイルの更新日時から8桁(YYYYMMDD)のDATEを設定
:EXE_LASTUPDATE_INFO
set LAST_UPDATE=%~t1
set LAST_YEAR=!LAST_UPDATE:~0,4!
set LAST_MONTH=!LAST_UPDATE:~5,2!
set LAST_DAY=!LAST_UPDATE:~8,2!
set NOW_DATE=!LAST_YEAR!!LAST_MONTH!!LAST_DAY!_
exit /b

REM ---------------------------------------------------------------------------
REM 送られてきたパラメータのパス名だけ取得
:EXE_DIRNAME
set DIR_NAME=%~dp1
exit /b

REM ---------------------------------------------------------------------------
REM 送られてきたパラメータのファイル名だけを取得
:EXE_BASENAME
set BASE_NAME=%~nx1
exit /b

REM ---------------------------------------------------------------------------
REM 送られてきたパラメータのファイル名だけを取得
:FINISH_ECHO
echo Rename "!EXETYPE!".
if not "%1"=="0" (
    echo   : SRC !SRCNAME!
    echo   : DST !DSTNAME!
)
echo;
exit /b

REM ---------------------------------------------------------------------------
REM 終了処理
:EXE_EXET
endlocal && pause && exit

:EOF
exit /b

REM ===========================================================================
REM END