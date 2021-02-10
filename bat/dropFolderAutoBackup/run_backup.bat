@echo off
REM ===========================================================================
REM
REM ドロップしたディレクトリを所定の場所へナンバリングして
REM バックアップを行うバッチ処理
REM
REM ===========================================================================

REM 遅延環境変数の設定
setlocal enabledelayedexpansion

REM pref.iniから情報の取得
set INIFILE=%~dp0pref.ini
echo 以下の.iniファイルを読み込みました
echo   : !INIFILE!
echo;

call :GET_INIFILE_INFO "BACKUP" "outputpath" OUTPUTPATH !INIFILE!
set BACKUP_INPUTPATH=%1
set BACKUP_INPUTNAME=%~nx1
set BACKUP_OUTPUTPATH=!OUTPUTPATH!
set BACKUP_OUTPUTTOPPATH=!OUTPUTPATH!\!BACKUP_INPUTNAME!

REM NULLの場合"1"を返す
if not defined BACKUP_INPUTPATH (
    echo ドロップデータの変数がNULLのため処理を終了します。
    endlocal && pause && exit /b 1
)
REM 何もドロップされて居ない場合"1"を返す
if "!BACKUP_INPUTPATH!"=="" (
    echo ドロップデータが確認出来ないため処理を終了します。
    endlocal && pause && exit /b 1
)
REM フォルダが存在しない場合"1"を返す
if not exist !BACKUP_INPUTPATH!\ (
    echo インプットしたフォルダが見つからないため処理を終了します。
    endlocal && pause && exit /b 1
)

REM バックアップ先のフォルダ内アイテムネームを調査し
REM 同一ネームフォルダが合った場合インデックスを付与する
set NOW_DATE=%date:~0,4%%date:~5,2%%date:~8,2%
set INDEX_COUNT=1
for /f "usebackq" %%f in (`dir /b !BACKUP_OUTPUTTOPPATH!`) do (
    echo "%%f" | findstr "!BACKUP_INPUTNAME!_!NOW_DATE!">NUL
    if not ERRORLEVEL 1 (
        set /a INDEX_COUNT+=1
    )
)
REM 0埋めでインデックス文字を確定
set ZERO_INDEX=0000!INDEX_COUNT!
REM 書き出し後のフォルダ名を確定
set file_name=!BACKUP_INPUTNAME!_!NOW_DATE!_!ZERO_INDEX:~-2!
set BACKUP_OUTPUTFOLDERPATH=!OUTPUTPATH!\!BACKUP_INPUTNAME!\!file_name!

echo バックアップ元フォルダパス
echo   : !BACKUP_INPUTPATH!
echo;
echo バックアップ先フォルダパス
echo   : !BACKUP_OUTPUTFOLDERPATH!
echo;

@set USER_INPUT=
@set /P USER_INPUT="上記の設定でバックアップを実行しますか？ (y/n) : "

if not !USER_INPUT!==y (
    if !USER_INPUT!==n (
        echo "n"が入力されたため処理を終了します。
    ) else (
        echo "y/n"以外の文字が入力されたため処理を終了します。
    )
    echo;
    endlocal && pause && exit /b 1
)

call :RUN_BACKUP_COPY !BACKUP_INPUTPATH! !BACKUP_OUTPUTFOLDERPATH!

echo バックアップが終了しました。
echo;
endlocal && pause && exit /b 0

REM ===========================================================================
REM サブルーチンリスト

:GET_INIFILE_INFO
REM ---------------------------------------------------------------------------
REM INIファイルから項目を読み取り返す
REM   %0 : このバッチ名
REM   %1 : セクション名
REM   %2 : キー名
REM   %3 : 取得変数名
REM   %4 : INIファイルパス名
REM   ※キーを取得できない場合は、取得変数に「ERR」を返す
set RESULT_NAME=
set SECTION_NAME=
REM -------------------------------------------------------
REM for文の/Fコマンド詳細
REM     (http://www.atmarkit.co.jp/ait/articles/0106/23/news004_2.html)
REM eol=;
REM     行末コメント開始文字をcにする。この文字以降は注釈として無視される
REM skip=n
REM     ファイルの先頭からn行を無視する
REM delims=xxx
REM     デリミタをxxxとする。複数文字の指定が可能。デフォルトはタブとスペース
REM         ↓のforは.iniで<変数名=パラメータ>を<=>で指定してるため
REM         delims="="と言った書き方になる。
REM tokens=x,y
REM     デリミタで区切られたパートを変数に代入してコマンド側に渡すかを指定する
REM         区切られた変数はその後に記述される「%%変数」に代入される。
REM         複数の区切りがある場合はその英文字から次の文字が自動的に使用される。
REM         「tokens=1,2」/ %%aの場合 %%a,%%b
REM         「tokens=1-4」/ %%aの場合 %%a,%%b,%%c,%%d
REM usebackq
REM     バッククォート（“`”、逆引用符）で囲まれた文字列をコマンドとして実行する
for /F "usebackq eol=; delims== tokens=1,2" %%x in (%4) do (
    set V=%%x
    set P=!V:~0,1!!V:~-1,1!
    set S=!V:~1,-1!
    if "!P!"=="[]" set SECTION_NAME=!S!
    if "!SECTION_NAME!"=="%~1" if "!V!"=="%~2" (
        set RESULT_NAME=%%y
        goto GET_INIFILE_EXIT
    )
)
set RESULT_NAME=ERR

:GET_INIFILE_EXIT
REM ---------------------------------------------------------------------------
REM INIファイルから項目を読み取り返す
set %3=!RESULT_NAME!
exit /b

:RUN_BACKUP_COPY
REM ---------------------------------------------------------------------------
REM バックアップ処理を開始
xcopy %1 %2 /S/E/I/Y
exit /b

:EOF
exit /b

REM ===========================================================================
REM END