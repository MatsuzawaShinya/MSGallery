#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    libフォルダ内のファイルアイテムを扱う総合ファイル
"""
###############################################################################
## base lib

import os
import sys
import json
sys.dont_write_bytecode = True

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

###############################################################################
## common attribute

_twiiterjsonfile = 'TWITTER_API_INFO.json'

###############################################################################
## common func

def pathReplace(path,type=True):
    r"""
        スラッシュバックスラッシュの変換
    """ 
    L = ('\\','/')
    src,dst = (L[0],L[1]) if type else (L[1],L[0])
    return path.replace(src,dst)

REP = pathReplace

###############################################################################

class Twitter(object):
    r"""
        ツイッター情報を取得する総合クラス
    """
    def __init__(self):
        r"""
            初期設定
        """
        pass
        
    def __call__(self):
        r"""
            呼び出し設定
        """
        pass
    
    def getPath(self):
        r"""
            ファイルパスを取得
        """
        return REP(os.path.dirname(__file__))
    
    def getTwiiterJsonPath(self):
        r"""
            ファイル内のtwiter-jsonファイルのパスを返す
        """
        return REP(os.path.join(self.getPath(),_twiiterjsonfile))
    
    def getApiInfo(self):
        r"""
            ツイッターAPI情報の取得
        """
        f = open(self.getTwiiterJsonPath(),'r')
        d = json.load(f)
        f.close()
        return d

###############################################################################
## other

###############################################################################