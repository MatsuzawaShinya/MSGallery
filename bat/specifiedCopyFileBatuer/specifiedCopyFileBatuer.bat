@echo off
REM ===========================================================================
REM
REM �h���b�v�����t�@�C��������̏ꏊ�֋����I�ɏ㏑�����ăR�s�[����o�b�`
REM
REM ===========================================================================

REM �x�����ϐ��̐ݒ�
setlocal enabledelayedexpansion

REM �t�@�C���p�X�������Ƀt�@�C���R�s�[
set TXTFILE=%~dp0%~n0.txt
echo �ȉ��̐ݒ�.txt�t�@�C����ǂݍ��݂܂���
echo   : !TXTFILE!
echo;

set USER_INPUT=
set /P USER_INPUT="�w�肵����ɃR�s�[�����s���܂����H (y/n) : "
echo;

if not !USER_INPUT!==y (
    if !USER_INPUT!==n (
        echo "n"�����͂��ꂽ���ߏ������I�����܂��B
    ) else (
        echo "y/n"�ȊO�̕��������͂��ꂽ���ߏ������I�����܂��B
    )
    echo;
    endlocal && pause && exit /b 1
)

for /f "delims=; tokens=1" %%a in (!TXTFILE!) do (
    set COPYTOPATH=%%a
    if exist !COPYTOPATH!\ (
        echo [Copy path] !COPYTOPATH!
        call :RUN_FILE_COPY %*
        echo;
    )
)

echo �R�s�[���������܂����B
echo;
endlocal && pause && exit /b 0

REM ===========================================================================
REM
REM �T�u���[�`�����X�g
REM
REM ===========================================================================

:RUN_FILE_COPY
REM ---------------------------------------------------------------------------
REM �h���b�v���ꂽ�t�@�C�����ƂɃR�s�[�����s
for %%f in (%*) do (
    set SRCFILEPATH=%%f
    call :EXE_BASENAME !SRCFILEPATH!
    set DSTFILEPATH=!COPYTOPATH!\!BASE_NMAE!
    REM echo - src path : !SRCFILEPATH!
    REM echo - dst path : !DSTFILEPATH!
    echo Copy file : !BASE_NMAE!
    copy !SRCFILEPATH! !DSTFILEPATH! /Y
)
exit /b

:EXE_BASENAME
REM ---------------------------------------------------------------------------
REM �����Ă����p�����[�^�̃t�@�C�����������擾
set BASE_NMAE=%~nx1
exit /b

:EOF
exit /b

REM ===========================================================================
REM END