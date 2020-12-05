#!/usr/b    in/python
# -*- coding: utf-8 -*-
r"""
    webImageDownloder/関数設定ファイル
"""
###############################################################################
## base lib

import os
import re
import sys

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from ... import settings as st
from msAppTools.settingFiles import systemGeneral as sg

###############################################################################
## base settings

_ck               = '_check'
_startColumn      = 3
_menuMaxLimit     = 12
_path             = 'PATH'
_estimation       = 'ESTIMATION'
_startupPath      = 'STARTUPPATH'
_optionWidget     = 'OPTIONWIDGET'
_startupLimitTime = 0.98
_epd              = st._eventPackageDict
_SPSL             = st.StandalonePathStoreList()

###############################################################################
## common func

def getModuleName():
    r"""
        パスからモジュールネームを相対的に取得
    """
    return (os.path.basename(os.path.dirname(__file__)))
    
def getAboutInfo():
    r"""
        aboutベースデータ取得
    """
    return {
        'title'   : getModuleName(),
        'version' : '3.0.1',
        'author'  : st._author,
        'release' : '2019/04/22',
        'update'  : '2020/07/14',
    }
    
###############################################################################
## sub func

def getJsonEstimationData():
    r"""
        pref.jsonデータのESTIMATIONを取得
    """
    d = _SPSL.getJsonFile()
    return d.get(_estimation)

def getJsonOptionWidget():
    r"""
        pref.jsonデータのOPTIONWIDGETを取得
    """
    d = _SPSL.getJsonFile()
    return d.get(_optionWidget)

def closedGui(gui):
    r"""
        guiをチェックしてクローズ
    """
    try:
        gui.close()
    except:
        pass

###############################################################################
## main func
    
###############################################################################
## END
