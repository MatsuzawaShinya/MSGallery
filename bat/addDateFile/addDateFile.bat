@echo off
REM ===========================================================================
REM
REM �w�肵���f�B���N�g�����̃t�@�C���^�h���b�v�t�@�C����
REM ���t(YYYYMMDD_)��t�^���ă��l�[������o�b�`
REM
REM ===========================================================================

REM �x�����ϐ��̐ݒ�
setlocal enabledelayedexpansion

if "%*" EQU "" (
    echo;
    echo �o�b�`�����ڎ��s���ꂽ���ߏI�����܂��B
    echo;
    endlocal && pause && exit /b 1
)

echo �f�B���N�g�����t�@�C���^�h���b�v�t�@�C���̐擪�ɓ��t��t�^���ă��l�[�����܂��B
echo ���t(YYYYMMDD_)���t�^����Ă���ꍇ�͏������X�L�b�v���܂��B
echo;
echo ( 1 ) : �����̓��t��t�^���ă��l�[�����܂��B
echo ( 2 ) : �t�@�C���̍X�V������t�^���ă��l�[�����܂��B
echo ( 0 ) : �����𒆒f���܂��B
echo;

set USER_INPUT=
@set /P USER_INPUT="���s�������^�C�v�̐�������͂��Ă��������B (1/2/0) : "
echo;

if not "!USER_INPUT!"=="0" (
    if "!USER_INPUT!"=="1" (
        set INPUT_TYPE=!USER_INPUT!
    ) else if "!USER_INPUT!"=="2" (
        set INPUT_TYPE=!USER_INPUT!
    ) else (
        echo "1" "2" �ȊO�����͂��ꂽ���ߏ������I�����܂��B
        echo;
        call :EXE_EXET
    )
) else (
    echo "0"�����͂��ꂽ���ߏ������I�����܂��B
    echo;
    call :EXE_EXET
)

REM �f�B���N�g�������if exist�ōs���ꍇ�A
REM �l�b�g���[�N�h���C�u�Ƀ}�E���g(�v�m�F)����Ă���ꍇ�t�H���_���f��
REM ��肭�����Ȃ����߁A�w�肳�ꂽ�t�@�C���A�C�e���̃T�C�Y��
REM �f�B���N�g��(0�o�C�g)�^�t�@�C��(1�o�C�g�ȏ�)�Ŕ��f����B
for %%f in (%*) do (
    set SRCDATA=%%f
	set SIZE=%%~zf
    REM �f�B���N�g���̏���
	if "!SIZE!"=="0" (
		for %%a in (!SRCDATA!\*) do (
            call :RENAME_FILE %%a
        )
    REM �t�@�C���̏���
	) else (
		if exist !SRCDATA! (
			call :RENAME_FILE %%f
		)
	)
)

echo �S�Ẵt�@�C���̃��l�[�����������܂����B
echo;
call :EXE_EXET

REM ===========================================================================
REM
REM �T�u���[�`�����X�g
REM
REM ===========================================================================

:RENAME_FILE
REM ---------------------------------------------------------------------------
REM �����Ă����t�@�C���̐擪�ɍ����̓��t��t�^���ă��l�[��
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
    REM �w�肳�ꂽ���t�t�H�[�}�b�g�ł͂Ȃ��ꍇ���t��t�^�����l�[������
    echo "!SRCNAME!" | findstr /R "[2][0][0-9][0-9][0-1][0-9][0-3][0-9]_">NUL
    if not "!ERRORLEVEL!"=="0" (
        REM ���l�[���悪����̏ꍇ���l�[��������
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
REM �����̓�������8��(YYYYMMDD)��DATE��ݒ�
:EXE_NOWDATE_INFO
set DATE_YEAR=!date:~0,4!
set DATE_MONTH=!date:~5,2!
set DATE_DAY=!date:~8,2!
set NOW_DATE=!DATE_YEAR!!DATE_MONTH!!DATE_DAY!_
exit /b

REM ---------------------------------------------------------------------------
REM �t�@�C���̍X�V��������8��(YYYYMMDD)��DATE��ݒ�
:EXE_LASTUPDATE_INFO
set LAST_UPDATE=%~t1
set LAST_YEAR=!LAST_UPDATE:~0,4!
set LAST_MONTH=!LAST_UPDATE:~5,2!
set LAST_DAY=!LAST_UPDATE:~8,2!
set NOW_DATE=!LAST_YEAR!!LAST_MONTH!!LAST_DAY!_
exit /b

REM ---------------------------------------------------------------------------
REM �����Ă����p�����[�^�̃p�X�������擾
:EXE_DIRNAME
set DIR_NAME=%~dp1
exit /b

REM ---------------------------------------------------------------------------
REM �����Ă����p�����[�^�̃t�@�C�����������擾
:EXE_BASENAME
set BASE_NAME=%~nx1
exit /b

REM ---------------------------------------------------------------------------
REM �����Ă����p�����[�^�̃t�@�C�����������擾
:FINISH_ECHO
echo Rename "!EXETYPE!".
if not "%1"=="0" (
    echo   : SRC !SRCNAME!
    echo   : DST !DSTNAME!
)
echo;
exit /b

REM ---------------------------------------------------------------------------
REM �I������
:EXE_EXET
endlocal && pause && exit

:EOF
exit /b

REM ===========================================================================
REM END