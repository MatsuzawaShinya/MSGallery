#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    ウインドウ設定をまとめたpyファイル
"""
###############################################################################
## base lib

import os
import sys
import json
import time
import traceback

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from msAppTools.settingFiles import systemGeneral as sg

###############################################################################
## setting

###############################################################################
## class

class WidgetSettingInfo(object):
    r"""
        ウィジェット情報を格納したクラス
    """
    def __init__(self):
        r"""
            初期設定
        """
        pass
    
    ## ----------------------------------------------------
    ## path info
    
    def getNowFolderPath(self):
        r"""
            現在のファイルパスを相対的に返す
        """
        return os.path.dirname(__file__)
    
    def getEachPythonFile(self,uiname,filetype):
        r"""
            UI名とpythonファイルタイプを指定してファイルパス情報を取得
            ファイルパス先のデータが無い場合はNoneを返す
        """
        path = os.path.join(self.getNowFolderPath(),uiname,
            filetype if '.py' in filetype else '{}.py'.format(filetype))
        return sg.toBasePath(path) if os.path.isfile(path) else None
    
    ## ----------------------------------------------------
    ## window info
    
    def getNowDirJsonPath(self):
        r"""
            ウィジェット情報が書かれたJsonのフルパスを相対的に取得
        """
        return os.path.join(os.path.dirname(__file__),'widgetinfo.json')
    
    def getJsonDate(self):
        r"""
            jsonの辞書データを取得
        """
        with open(self.getNowDirJsonPath(),'r') as f:
            d = json.load(f)
        return d
    
    def getSettingInfo(self):
        r"""
            設定情報を取得
        """
        return self.settings()
    
    def settings(self):
        r"""
            UIの基礎情報設定/情報元は同改装の.jsonにて管理
            order  : ウィジェット作成時の順番の順位（低いほど最初に作られる）
            start  : Mastema起動時にアイコンを作るかどうかのフラグ
            name   : ウィジェットタイトルネーム指定
            size   : 起動時のウィジェットのサイズ（2回目以降はサイズは保持される）
            drop   : setAcceptDropsの指定
        """
        return self.getJsonDate()

###############################################################################
## END
