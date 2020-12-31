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
        'version' : '2.0.1',
        'author'  : st._author,
        'release' : '2019/11/22',
        'update'  : '2020/07/14',
    }
    
###############################################################################
## base settings

_SPSL        = st.StandalonePathStoreList(getModuleName())
_defaultText = 'Drop here.'
_dragText    = 'Drag now...'
_subprocessValue    = 0
_subprocessTextList = ('Popen','call')
_DROPPATH = 'DROP_PATH'

###############################################################################
## sub func

def getStyleWord(w,i=4):
    r"""
        文字を見出し付でリターン
    """
    return '<h{1}>{0}</h{1}>'.format(w,i)

###############################################################################
## main func
    
###############################################################################
## END
