@echo off
REM ===========================================================================
REM
REM �h���b�v�����f�B���N�g��������̏ꏊ�փi���o�����O����
REM �o�b�N�A�b�v���s���o�b�`����
REM
REM ===========================================================================

REM �x�����ϐ��̐ݒ�
setlocal enabledelayedexpansion

REM pref.ini������̎擾
set INIFILE=%~dp0pref.ini
echo �ȉ���.ini�t�@�C����ǂݍ��݂܂���
echo   : !INIFILE!
echo;

call :GET_INIFILE_INFO "BACKUP" "outputpath" OUTPUTPATH !INIFILE!
set BACKUP_INPUTPATH=%1
set BACKUP_INPUTNAME=%~nx1
set BACKUP_OUTPUTPATH=!OUTPUTPATH!
set BACKUP_OUTPUTTOPPATH=!OUTPUTPATH!\!BACKUP_INPUTNAME!

REM NULL�̏ꍇ"1"��Ԃ�
if not defined BACKUP_INPUTPATH (
    echo �h���b�v�f�[�^�̕ϐ���NULL�̂��ߏ������I�����܂��B
    endlocal && pause && exit /b 1
)
REM �����h���b�v����ċ��Ȃ��ꍇ"1"��Ԃ�
if "!BACKUP_INPUTPATH!"=="" (
    echo �h���b�v�f�[�^���m�F�o���Ȃ����ߏ������I�����܂��B
    endlocal && pause && exit /b 1
)
REM �t�H���_�����݂��Ȃ��ꍇ"1"��Ԃ�
if not exist !BACKUP_INPUTPATH!\ (
    echo �C���v�b�g�����t�H���_��������Ȃ����ߏ������I�����܂��B
    endlocal && pause && exit /b 1
)

REM �o�b�N�A�b�v��̃t�H���_���A�C�e���l�[���𒲍���
REM ����l�[���t�H���_���������ꍇ�C���f�b�N�X��t�^����
set NOW_DATE=%date:~0,4%%date:~5,2%%date:~8,2%
set INDEX_COUNT=1
for /f "usebackq" %%f in (`dir /b !BACKUP_OUTPUTTOPPATH!`) do (
    echo "%%f" | findstr "!BACKUP_INPUTNAME!_!NOW_DATE!">NUL
    if not ERRORLEVEL 1 (
        set /a INDEX_COUNT+=1
    )
)
REM 0���߂ŃC���f�b�N�X�������m��
set ZERO_INDEX=0000!INDEX_COUNT!
REM �����o����̃t�H���_�����m��
set file_name=!BACKUP_INPUTNAME!_!NOW_DATE!_!ZERO_INDEX:~-2!
set BACKUP_OUTPUTFOLDERPATH=!OUTPUTPATH!\!BACKUP_INPUTNAME!\!file_name!

echo �o�b�N�A�b�v���t�H���_�p�X
echo   : !BACKUP_INPUTPATH!
echo;
echo �o�b�N�A�b�v��t�H���_�p�X
echo   : !BACKUP_OUTPUTFOLDERPATH!
echo;

@set USER_INPUT=
@set /P USER_INPUT="��L�̐ݒ�Ńo�b�N�A�b�v�����s���܂����H (y/n) : "

if not !USER_INPUT!==y (
    if !USER_INPUT!==n (
        echo "n"�����͂��ꂽ���ߏ������I�����܂��B
    ) else (
        echo "y/n"�ȊO�̕��������͂��ꂽ���ߏ������I�����܂��B
    )
    echo;
    endlocal && pause && exit /b 1
)

call :RUN_BACKUP_COPY !BACKUP_INPUTPATH! !BACKUP_OUTPUTFOLDERPATH!

echo �o�b�N�A�b�v���I�����܂����B
echo;
endlocal && pause && exit /b 0

REM ===========================================================================
REM �T�u���[�`�����X�g

:GET_INIFILE_INFO
REM ---------------------------------------------------------------------------
REM INI�t�@�C�����獀�ڂ�ǂݎ��Ԃ�
REM   %0 : ���̃o�b�`��
REM   %1 : �Z�N�V������
REM   %2 : �L�[��
REM   %3 : �擾�ϐ���
REM   %4 : INI�t�@�C���p�X��
REM   ���L�[���擾�ł��Ȃ��ꍇ�́A�擾�ϐ��ɁuERR�v��Ԃ�
set RESULT_NAME=
set SECTION_NAME=
REM -------------------------------------------------------
REM for����/F�R�}���h�ڍ�
REM     (http://www.atmarkit.co.jp/ait/articles/0106/23/news004_2.html)
REM eol=;
REM     �s���R�����g�J�n������c�ɂ���B���̕����ȍ~�͒��߂Ƃ��Ė��������
REM skip=n
REM     �t�@�C���̐擪����n�s�𖳎�����
REM delims=xxx
REM     �f���~�^��xxx�Ƃ���B���������̎w�肪�\�B�f�t�H���g�̓^�u�ƃX�y�[�X
REM         ����for��.ini��<�ϐ���=�p�����[�^>��<=>�Ŏw�肵�Ă邽��
REM         delims="="�ƌ������������ɂȂ�B
REM tokens=x,y
REM     �f���~�^�ŋ�؂�ꂽ�p�[�g��ϐ��ɑ�����ăR�}���h���ɓn�������w�肷��
REM         ��؂�ꂽ�ϐ��͂��̌�ɋL�q�����u%%�ϐ��v�ɑ�������B
REM         �����̋�؂肪����ꍇ�͂��̉p�������玟�̕����������I�Ɏg�p�����B
REM         �utokens=1,2�v/ %%a�̏ꍇ %%a,%%b
REM         �utokens=1-4�v/ %%a�̏ꍇ %%a,%%b,%%c,%%d
REM usebackq
REM     �o�b�N�N�H�[�g�i�g`�h�A�t���p���j�ň͂܂ꂽ��������R�}���h�Ƃ��Ď��s����
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
REM INI�t�@�C�����獀�ڂ�ǂݎ��Ԃ�
set %3=!RESULT_NAME!
exit /b

:RUN_BACKUP_COPY
REM ---------------------------------------------------------------------------
REM �o�b�N�A�b�v�������J�n
xcopy %1 %2 /S/E/I/Y
exit /b

:EOF
exit /b

REM ===========================================================================
REM END