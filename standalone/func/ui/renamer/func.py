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
        'version' : '2.2.1',
        'author'  : st._author,
        'release' : '2019/04/26',
        'update'  : '2021/01/13',
    }

###############################################################################
## base settings

_SPSL = st.StandalonePathStoreList(getModuleName())

###############################################################################
## sub func

###############################################################################
## main func
    
###############################################################################
## END