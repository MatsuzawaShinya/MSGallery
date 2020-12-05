#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    ウインドウ関数をまとめたファイル
"""
###############################################################################
## base lib

import os
import sys
import json
import time
import traceback
from distutils.util import strtobool

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from . import lib
from .. import settings as st
from msAppTools.settingFiles import systemGeneral as sg

EPD = st._eventPackageDict
WSI = lib.WidgetSettingInfo()
QtWidgets,QtCore,QtGui = sg.QtWidgets,sg.QtCore,sg.QtGui

###############################################################################

class MainWindow(sg.EventBaseWidget):
    r"""
        メインウィンドウクラス
    """
    def __init__(self,guiName,parent=None):
        r"""
            初期設定
        """
        super(MainWindow,self).__init__(parent)
        
        self._dict = WSI.getSettingInfo()
        
        ## --------------------------------------------------------------------
        ## pre process
        
        # 指定モジュールのインポート
        r"""
            ！！注意！！
            importの名前が変数で指定されているためexecを使用しているが、
            できれば避けたほうがいい。（参照：https://teratail.com/questions/148237）
            execを関数内で使用するとglobal,localとの区別で面倒な事が発生するため
            使用するのであれば場所に関しては十分に注意するべし。
        """
        # self.importModule(guiName) # self.importModule(self._dict)
        exec('from . import {}'.format(guiName))
        
        ## --------------------------------------------------------------------
        ## base setting
        
        self.PSL = sg.PathStoreList()
        self.aboutData  = []
        self._eventFunc = {}
        
        if self._dict[guiName]:
            _d = self._dict[guiName]
            self.startupFlag = False
        else:
            _d = self._dict['default']
            self.startupFlag = True
            
        self.setWindowFlags(sg._setWindowFlagsDict[_d['windowFlag']])
        
        self.__titleName = _d['name']
        self.__guiObject = eval('{}.openWindow(self)'.format(guiName))
        self.resize(_d['size'][0],_d['size'][1])
        self.setAcceptDrops(True if strtobool(str(_d['drop'])) else False)
        
        self._nowGui = _d.get('name')
        
        # 各ウィジェットの位置・大きさを設定
        self.setOpenWidgetInfo(self.__titleName)
        # 各ウィジェットごとの設定
        self.individualSetting()
        # aboutデータを起動guiのパターンでsetattr設定
        self.aboutData = self.__guiObject.getAboutData()
        ([setattr(self,x,self.aboutData[x]) for x in self.aboutData])
        
        self.we = sg.WidgetEventAction()
        self.we.setTitle(self.__titleName)
        self.we.setWidget()
        self.we.setSelf(self)
        self.we.t.setStyleSheet(
            'QLabel{font-family:GEORGIA;font-size:13px;color:#FFF;}'
        )

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.we.getWidget())
        self.layout.addWidget(self.__guiObject)
        
        self.setWeaOptionWidgetToChildren()
        
        # 各ScrolledWidgetのpostProcessを実行
        self.__guiObject.exePostProcess()
        
    ## --------------------------------------------------------------------
    ## Settings
    
    def individualSetting(self):
        r"""
            それぞれのウィジェット毎の詳細設定
        """
        # eventPackageを子へ送る
        self.__guiObject.setEventPackage(self.eventFuncPackaging)
        
        # Mastema/GUI情報を送信追記記述
        if self._nowGui in ['Mastema','Mastema2']:
            self.__guiObject.startup(
                self._dict,self.rect().width(),self.rect().height())
    
    ## --------------------------------------------------------------------
    ## Func
    
    def importModule(self,val):
        r"""
            mainGuiの親のUI基礎情報設定を元にモジュールのインポートを実行
            execが関数内でグローバルスコープされる問題があるので、
            このメソッドは使用を控える。
            （execにglobals()をあたえ処理は動くようにして対応はした）
        """
        def _import(name):
            r"""
            """
            try:
                exec('from . import {}'.format(name),globals())
                print('>>> Successful completion, "{}"'.format(name))
            except:
                print('>>> Import failed. "{}"'.format(name))
        
        # 辞書で入ってきた場合全てを処理
        if isinstance(val,dict):
            print('+ Import type = dict')
            [_import(d) for d in val]
        # 文字列(GUI名)で入ってきた場合はそのGUIを読み込み
        elif isinstance(val,str):
            print('+ Import type = str')
            _import(val)
    
    def setWeaOptionWidgetToChildren(self):
        r"""
            こどものウィジェットにWidgetEventActionのウィジェットを送る
            実行の順番は以下の通り。
            1)GUI起動時
                MainWindow(__init__):
                    -> こどもにWidgetEventActionのオブジェクトを送る
                こどものGUIウィジェット(setWeaOptionWidgetFromParent):
                    -> 親から送られれきたWidgetEventActionを子でセットし管理
            2)オプションボタン実行時
                systemGeneral(openOptionWidget):
                    新しいウィジェットを作成しこどものウィジェット作成関数
                    (setOptionWidgetChildrenData)にアクセスしウィジェットを
                    作成する。その後オプションウィジェットを表示（show）
        """
        if hasattr(self.__guiObject,'setWeaOptionWidgetFromParent'):
            self.__guiObject.setWeaOptionWidgetFromParent(self.we)
    
    def setDebugFlag(self,value=True):
        r"""
            デバックフラグのスイッチ(オーバーライド)
        """
        _f = sys._getframe().f_code.co_name
        
        self.debugFlag = value
        print(u'Debug mode = %s'%(str(value)))
        
        # こどもにsetDebugFlagメソッドがある場合は関連付ける
        if hasattr(self.__guiObject,_f):
            eval('"self.__guiObject.{}(value)"'.format(_f))
            print(u'  + Associate with children ')

    ## --------------------------------------------------------------------
    ## Event package setting
    
    def setEvent(self,eventName,eventFunc):
        r"""
            イベントを設定
        """
        self._eventFunc[eventName] = eventFunc
        
    def getEvent(self,eventName):
        r"""
            イベントを取得
        """
        return self._eventFunc.get(eventName)
        
    def exeEvent(self,eventName):
        r"""
            イベントを実行
        """
        ev = self.getEvent(eventName)
        if ev:
           ev()

    def eventFuncPackaging(self):
        r"""
            イベント系メソッドをパッケージして返す
        """
        # return (self.setEvent,self.getEvent,self.exeEvent)
        return {
            'set' : self.setEvent,
            'get' : self.getEvent,
            'exe' : self.exeEvent,
        }
    
    ## --------------------------------------------------------------------
    ## Event
    
    def keyPressEvent(self,event):
        r"""
            キープレス時のイベント情報(オーバーライド)
        """
        super(MainWindow,self).keyPressEvent(event)
        
        key,mask = self.getKeyType(event),self.getKeyMask()
        if (key['press'] == 'F1') and self.debugFlag:
            sg.openExplorer(self.PSL.msAppToolsPath)
        else:
            pass
    
    def mouseMoveEvent(self,event):
        r"""
            マウスが動いた時の動作
        """
        super(MainWindow,self).mouseMoveEvent(event)
        
        if self.mouseType == 3 and self._nowGui == 'Mastema':
            self.__guiObject.iconResize(
                w=self.rect().width(),h=self.rect().height())
        
    def closeEvent(self,event):
        r"""
            閉じたときのイベント(オーバーライド)
        """
        # 閉じる際のイベント実行を連動（メインメソッドは子で保有）
        self.exeEvent(sys._getframe().f_code.co_name)
        self.setCloseWidgetInfo(self.__titleName)
        if self.debugFlag:
            print('>>> Debug mode on, Run sleep.')
            time.sleep(2)

    def dropEvent(self,event):
        r"""
            ドロップ時のイベント(オーバーライド)
        """
        # ドロップ時のイベントを実行（メインメソッドは子で保有し設定）
        self.exeEvent(sys._getframe().f_code.co_name)

###############################################################################
## END
