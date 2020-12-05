#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    共通セットデータの格納init
"""
###############################################################################
## base lib

import os
import sys
import json
import traceback

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from msAppTools.settingFiles import systemGeneral as sg

###############################################################################

_author = 'Matsuzawa Shinya'
_imageExportExt = ['jpg','png']
_colorIndexList = {
    0 : ('#434371','#000','#FFF','#FEE'),
    1 : ('#547AA5','#000','#FFF','#EFE'),
}
_resultText = ('OK','NG')
_vanishTime = 1500

_eventPackageDict = {
    'set':'setEvent',
    'get':'getEvent',
    'exe':'exeEvent',
    'ep' :'eventPackage',
}

###############################################################################

class StandalonePathStoreList(sg.sgwidget.PathStoreList):
    r"""
        スタンドアロンパス継承用クラス
    """
    def __init__(self,parent=None):
        r"""
            初期設定
        """
        super(StandalonePathStoreList,self).__init__(parent)
    
    def getPrefJsonName(self,uiname):
        r"""
            ui名を指定してuiname.pref.jsonをリターン
        """
        try:
            return ('{}{}'.format(uiname,self.getSuffixName('pref')))
        except:
            return '' 
    
    def getSavePath(self,uiname):
        r"""
            ui名を指定してXXXX.pref.jsonを取得
        """
        _path = sg.toBasePath(os.path.join(self.getRoamingPath(),
            sg.msAppToolsName,uiname,self.getPrefJsonName(uiname)))
        return _path

###############################################################################