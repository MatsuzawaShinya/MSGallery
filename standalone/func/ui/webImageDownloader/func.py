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

REP              = sg.slashConversion
EPD              = st._eventPackageDict
SPSL             = st.StandalonePathStoreList()
KEYMETHOD        = sg.KeyMethod()
TWSIZE           = 'orig'
OUTPUTLINEPATH   = 'OUTPUTLINEPATH'
SLEEPTIMEINFO    = 'SLEEPTIMEINFO'
INPUTDAYLINE     = 'INPUTDAYLINE'
TABLEURLINFOLIST = 'TABLEURLINFOLIST'
DROPFILELOGLIST  = 'DROPFILELOGLIST'
GOBACKDAYS       = 'GOBACKDAYS'
GOBACKDAYSDEFVAL = 31
YMDLIST = ('yyyymmdd','yyyymm','yymmdd','mmdd','yyyy','yy','mm','dd')
TABLEHEADERLIST  = {
    0 : {
        'type'  :'checkbox',
        'header':'',
    },
    1 : {
        'type'  :'url',
        'header':'URL',
    },
    2 : {
        'type'  :'data',
        'header':'DATA',
    },
}

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
        'version' : '2.1.1',
        'author'  : st._author,
        'release' : '2020/05/14',
        'update'  : '2020/07/28',
    }
    
###############################################################################
## sub func

###############################################################################
## main func
    
###############################################################################
## END
