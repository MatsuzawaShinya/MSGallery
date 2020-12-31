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

_ESTIMATION = sg._ESTIMATION

###############################################################################

class StandalonePathStoreList(sg.sgwidget.PathStoreList):
    r"""
        スタンドアロンパス継承用クラス
        2020/12/23
            estimationへアクセスするメソッドを当クラスに移動
    """
    def __init__(self,uiname='StandalonePathStoreList',parent=None):
        r"""
            初期設定
        """
        super(StandalonePathStoreList,self).__init__(uiname,parent)
        
        self.__keyEstimationPath = None
        self.__beforePath = None
        self.__updateJsonDataDict = {}
        
    ## ----------------------------------------------------
    ## settings
        
    def setEstimationPath(self,path):
        r"""
            estimationパスを設定
        """
        self.__keyEstimationPath = path
        
    def getEstimationPath(self):
        r"""
            estimationパスを取得
        """
        return self.__keyEstimationPath
        
    def getEstimationModuleNameFullPath(self,type=''):
        r"""
            モジュールネームに対応したEstimationのフルパスを返す
        """
        infodata = {
            'master' : self.getEstimationMasterPath(),
            'ui'     : self.getEstimationEachuiPath(),
            ''       : '',
        }
        return infodata[type]
        
    def setBeforePath(self,path=''):
        r"""
            ベースパスをグローバス変数にセット
            path = True  : self.getPath()のパスを__beforePathセットし
                    新しいパスを_SPSLにセット
                    getPath()で取得できなかった場合は処理しない
            path = False : __beforePathにセットされているパスを_SPSLに再セット
                    パスが__beforePathに指定されていない場合は処理しない
        """
        if path:
            gp = self.getPath()
            self.__beforePath = gp if gp else None
            self.setPath(path)
        else:
            if not self.__beforePath:
                return
            self.setPath(self.__beforePath)
        
    ## ----------------------------------------------------
    ## json action
    
    def getJsonEstimationData(self,keyTarget=None):
        r"""
            sum,master,各ui毎のESTIMATION値を辞書形式に変換し送る
        """
        # masterとui毎のestimation情報を取得
        self.setBeforePath(self.getEstimationModuleNameFullPath('master'))
        d1 = self.getJsonFile()
        self.setBeforePath()
        self.setBeforePath(self.getEstimationModuleNameFullPath('ui'))
        d2 = self.getJsonFile()
        self.setBeforePath()
        est_d1 = d1.get(_ESTIMATION)
        est_d2 = d2.get(_ESTIMATION)
        
        returndict = {
            'sum'   :{},
            'master':{},
            'ui'    :{},
        }
        
        # 取得辞書情報を確認
        # masterに情報がない（初回起動時）は空辞書情報を返す
        if not est_d1:
            return returndict
        
        # 各uiの重複key情報を取得
        intersection_keys = (est_d1.keys() & est_d2.keys()
            if est_d1 and est_d2 else [])

        # キー情報を取得し一つの辞書にまとめる
        sumdict = {}
        for k,v in est_d1.items():
            value = ((v + est_d2.get(k)) if k in intersection_keys else v)
            sumdict.update({k:value})
        returndict.update({'sum'   :sumdict})
        returndict.update({'master':est_d1})
        returndict.update({'ui'    :est_d2})

        return returndict.get(keyTarget) if keyTarget else returndict
        
    def setJsonEstimationData(self,masterdict={},uidict={}):
        r"""
            master,各ui専用のestimation.jsonにデータを書き込む
        """
        # _estimationが付与されてない辞書の場合は付け足す
        _ADDEST = (lambda d: d if d.get(_ESTIMATION) else {_ESTIMATION:d})
        
        # estimation.master.json/更新
        self.setBeforePath(self.getEstimationModuleNameFullPath('master'))
        self.setDict(_ADDEST(masterdict))
        self.setJsonFile()
        self.setBeforePath()
        
        # estimation.ui.json/更新
        self.setBeforePath(self.getEstimationModuleNameFullPath('ui'))
        self.setDict(_ADDEST(uidict))
        self.setJsonFile()
        self.setBeforePath()
        
    ## ----------------------------------------------------
    ## json infomation
    
    def setUpdateJsonData(self,when='before',type='master',d={}):
        r"""
            ui起動時に、estimation.jsonのui辞書情報を格納
        """
        insertdict = self.__updateJsonDataDict.get(when)
        if not insertdict:
            insertdict = {type:d}
        else:
            insertdict.update({type:d})
        self.__updateJsonDataDict.update({when:insertdict})
        
    def getUpdateJsonData(self):
        r"""
            更新前,後の辞書データを取得
        """
        return self.__updateJsonDataDict
    
    def setBeforeEstimationInfo(self):
        r"""
            起動時/update時に参照されるベース辞書情報をセットする
        """
        self.setUpdateJsonData(
            'before','master',self.getJsonEstimationData('master'))
        self.setUpdateJsonData(
            'before','ui'    ,self.getJsonEstimationData('ui'))
    
    ## ----------------------------------------------------
    ## other
        
    def _print(self,addmsg=''):
        r"""
        """
        print(9999,str(addmsg),self.getPath())
        
###############################################################################