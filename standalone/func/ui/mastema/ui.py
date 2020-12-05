#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    Mastema/ウィジェットファイル
"""
###############################################################################
## base lib

import os
import sys
import json
import time
import traceback
import subprocess
from distutils.util import strtobool

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from .   import func as fc
from ..  import func as up2_func
from ... import icon
from ... import settings as st
from msAppTools.settingFiles import systemGeneral as sg

MainWindow = up2_func.MainWindow
QtWidgets,QtCore,QtGui = sg.QtWidgets,sg.QtCore,sg.QtGui
_epd = st._eventPackageDict
_iconResizeFlag = fc._iconResizeFlag

###############################################################################

class Mastema(sg.ScrolledWidget):
    r"""
        gui総合起動窓口
    """
    _dict   = {}
    _layout = None
    
    def __init__(self,parent=None,masterDict=None):
        r"""
            初期設定
        """
        super(Mastema,self).__init__(parent)
        
        self._dict = masterDict
        self.setDict(masterDict)
        
        self.COLUMN = 4
        self._w,self._h      = None,None
        self._iconResizeFlag = _iconResizeFlag
        self._childGuiList   = []
        
    ## ------------------------------------------------------------------------
    ## common parent event setting
    
    def setEventPackage(self,packaging,setup=True):
        r"""
            子と関連性をためのメソッドパッケージを親から引き継いで設定する
        """
        super(Mastema,self).setEventPackage(packaging)
        
        # 親eventと連動
        if setup:
            packaging()['set']('closeEvent',self.exeCloseInterlock)
    
    ## ------------------------------------------------------------------------
    ## event
    
    def exeCloseInterlock(self,log=False):
        r"""
            mastema終了時に子UIも一緒に閉じる親メソッド
        """
        for C in self._childGuiList:
            for c in C:
                try:
                    C[c].close()
                except:
                    if log:
                        print(u'Already gui closed. "{}"'.format(c))
    
    ## ------------------------------------------------------------------------
    ## ui
    
    def buildUI(self,parent=None):
        r"""
            buildUIはMastema実行時に先に実行されるので
            予めレイアウトの受け皿に設定しておく
        """
        self._layout = QtWidgets.QVBoxLayout(parent)
        
    def guiSetting(self):
        r"""
            guiレイアウトの作成
            
            Returns:
                any:
        """
        INDEX    = (lambda x,y:((x//y),(x%y)))
        NUM      = 0
        iconsize = 40
        self.widgetList = []
        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(2,2,2,2)
        grid.setSpacing(4)
        grid.setAlignment(QtCore.Qt.AlignCenter)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)
        
        for d in self.getDict():
            gui = self._dict[d]
            if not isinstance(gui,dict):
                print('>> Skip not dictionary type. "{}"'.format(d))
                continue
            startbool = gui.get('start')
            if not startbool:
                print('>> Start not setting value. "{}"'.format(d))
                continue
            if not strtobool(str(startbool)):
                print('>> Start flag is off. "{}"'.format(d))
                continue
            pb = QtWidgets.QPushButton('')
            pb.setStyleSheet(sg.ss.BORDER_STYLE_2)
            pb.setIcon(icon.iconPath(icon=d))
            pb.setIconSize(QtCore.QSize(iconsize,iconsize))
            pb.setToolTip(gui['name'])
            self.widgetList.append([gui['order'],pb,d])
        
        # orderの順番に並び替え
        self.widgetList.sort()
        for w in self.widgetList:
            ind = INDEX(NUM,self.COLUMN)
            grid.addWidget(w[1],ind[0],ind[1])
            NUM += 1
            
        self._layout.addLayout(grid)
        self.iconResize(self.getGuiSize()[0],self.getGuiSize()[1])
        
    ## ------------------------------------------------------------------------
    ## func
    
    def startup(self,d,w,h):
        r"""
            起動時のセットアップメソッド
        """
        self.setDict(d)
        self.setGuiSize(w,h)
        self.guiSetting()
        self.connectFunc()
        
    def setDict(self,d):
        r"""
            辞書データのセット
        """
        self._dict = d
        
    def getDict(self):
        r"""
            辞書データの返し
        """
        return self._dict
        
    def setGuiSize(self,w,h):
        r"""
            guiサイズの保存
        """
        self._w,self._h = w,h
    
    def getGuiSize(self):
        r"""
            guiサイズのリターン
        """
        return (self._w,self._h)
    
    def connectFunc(self):
        r"""
            各アイコンボタンに関数を紐づけ
        """
        for x in self.widgetList:
            x[1].name = x[2]
            x[1].clicked.connect(self.openGui)
        
    def openGui(self):
        r"""
            GUI起動メソッド
            起動したウィジェットの情報を格納しクローズ時の自動終了へと紐付ける
        """
        name = self.sender().name
        
        kmb = sg.KeyMethod()
        km2 = kmb._keyMask2()
        kt  = kmb._keyType(None)
        
        if km2(['ctrl']) == kt['mod2']:
            self.getBatPath(name)
        else:
            MW = MainWindow(name)
            MW.show()
            self._childGuiList.append({name:MW})
            
    def iconResize(self,w=None,h=None):
        r"""
            アイコンリサイズ
        """
        if self._iconResizeFlag:
            _RS = (lambda s:int(s//self.COLUMN))
            _w = w if w else self.rect().width()
            _h = h if h else self.rect().height()
            ([b[1].setIconSize(QtCore.QSize(_RS(_w),_RS(_h)))
                for b in self.widgetList])
            
    ## ------------------------------------------------------------------------
    ## path
    
    def getBatPath(self,name=''):
        r"""
            バッチ実行パスを相対的に取得
        """
        _dn_ = os.path.dirname
        
        standalonepath = _dn_(_dn_(_dn_(_dn_(__file__))))
        batpath = os.path.join(
            standalonepath,'bat',sg.getPythonVersion(),'{}.bat'.format(name))
        
        if not os.path.isfile(batpath):
            return
        
        ## 最初に実行したbat下にある状態でsubprocess実行すると
        ## 同一のPythonプロセスで開始されるため別プロセスとして起動が出来ない。
        # subprocess.Popen(batpath,shell=True,close_fds=True)
    
    ## ------------------------------------------------------------------------
    ## common
            
    def getAboutData(self):
        r"""
            about情報の取得
        """
        return fc.getAboutInfo()
        
###############################################################################
## End

