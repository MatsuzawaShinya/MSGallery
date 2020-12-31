#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    systemGeneral/widget関係の処理をまとめたファイル
"""
###############################################################################
## base lib

import os
import re
import json
import time
import traceback
from .. import stylesheet as ss

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from . import (func as sgfunc, info as sginfo)
MSINFO = sginfo.MsAppToolsBaseInfo()

## ----------------------------------------------------------------------------
## local lib / ローカル環境に合わせたインポート

print(u'systemGeneral / ローカルインポートを開始します。')

try:
    from PySide2 import QtWidgets,QtGui,QtCore
    print('>> Import "PySide2".')
except:
    from .. import pyside2
    QtWidgets,QtCore,QtGui = pyside2.QtWidgets,pyside2.QtCore,pyside2.QtGui
    print('>> Import my package "pyside2" conversion.')
try:
    from msAppTools import msAppIcons
    iconFlag = True
    print('>> Flag state of msAppTools "True"')
except:
    iconFlag = False
    print('>> Flag state of msAppTools "False"')
try:
    import shiboken2
    from maya import OpenMayaUI
    MainWindow = shiboken2.wrapInstance(
        long(OpenMayaUI.MQtUtil.mainWindow()),QtWidgets.QWidget
    )
    shibokenFlag = True
    print('>> Flag state of shiboken2 "True"')
except:
    shibokenFlag = False
    print('>> Flag state of shiboken2 "False"')

###############################################################################
## - Setting

def path():
    r"""
        ファイルパスのリターン
    """
    return (__file__)

## maApppName
msAppToolsName = MSINFO.getMsAppToolsName()

## work company
NOW_COMPANY    = 'GOONEYS'

## setWindowFlags state
_defaultFrame = (QtCore.Qt.Window|QtCore.Qt.FramelessWindowHint)
_setWindowFlagsDict = {
    ''              : _defaultFrame,
    'default'       : _defaultFrame,
    'tophint=True'  : (_defaultFrame|QtCore.Qt.WindowStaysOnTopHint),
    'tophint=False' : (_defaultFrame|QtCore.Qt.WindowFlags()),
}

_ESTIMATION = MSINFO.getEstimationName()

###############################################################################
## Global common func

## ----------------------------------------------------------------------------
## key mask

"""
# ?
# event.modifiers() == QtCore.Qt.MetaModifierで判定ができない。バグ？
# -> QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.MetaModifier でいける

event.key()
    winKey : QtCore.Qt.Key_Meta
    Shift  : QtCore.Qt.Key_Shift
    Ctrl   : QtCore.Qt.Key_Control
    Alt    : QtCore.Qt.Key_Alt
    <-     : QtCore.Qt.Key_Left
    ->     : QtCore.Qt.Key_Right
event.modifiers()
    winKey : QtCore.Qt.MetaModifier
    Shift  : QtCore.Qt.ShiftModifier
    Ctrl   : QtCore.Qt.ControlModifier
    Alt    : QtCore.Qt.AltModifier
"""

class KeyMethod(object):
    r"""
        キーメソッド内包/取得クラス
    """
    def __init__(self):
        r"""
        """
        pass
    
    def _mouseType(self,pos):
        r"""
            キーマスクのリターン/複数回使用
        """
        return (
            1 if pos.button() == QtCore.Qt.MouseButton.LeftButton  else
            2 if pos.button() == QtCore.Qt.MouseButton.MidButton   else
            3 if pos.button() == QtCore.Qt.MouseButton.RightButton else
            0
        )
    
    def _keyMask(self):
        r"""
            キーマスクのリターン/複数回使用
        """
        return {
            'ctrl'           : (QtCore.Qt.ControlModifier),
            'shift'          : (QtCore.Qt.ShiftModifier),
            'alt'            : (QtCore.Qt.AltModifier),
            'ctrl,shift'     : (QtCore.Qt.ControlModifier|
                                QtCore.Qt.ShiftModifier),
            'ctrl,alt'       : (QtCore.Qt.ControlModifier|
                                QtCore.Qt.AltModifier),
            'shift,alt'      : (QtCore.Qt.ShiftModifier|
                                QtCore.Qt.AltModifier),
            'ctrl,shift,alt' : (QtCore.Qt.ControlModifier|
                                QtCore.Qt.ShiftModifier|
                                QtCore.Qt.AltModifier)
        }
        
    def _keyMask2core(self,typeList=[]):
        r"""
            キーマスクのリターン(指定タイプ)/複数回使用
        """
        _R = []
        _D = {
            'ctrl'  : 'QtCore.Qt.ControlModifier',
            'shift' : 'QtCore.Qt.ShiftModifier',
            'alt'   : 'QtCore.Qt.AltModifier',
        }
        for t in typeList:
            r = _D.get(t)
            if r:
                _R.append(r)
        try:
            return eval('|'.join(_R)) if _R else False
        except:
            return None
            
    def _keyMask2(self):
        r"""
            キーマスクのリターン/メソッドで取得
        """
        return self._keyMask2core
        
    def _keyType(self,event):
        r"""
            キータイプのリターン/複数回使用
        """
        try:
            key   = event.key()
        except:
            key   = None
        try:
            mod1  = event.modifiers()
        except:
            mod1  = None
        try:
            mod2  = QtWidgets.QApplication.keyboardModifiers()
        except:
            mod2  = None
        try:
            press = QtGui.QKeySequence(event.key()).toString(
                        QtGui.QKeySequence.NativeText)
        except:
            press = None
        return {'key':key,'mod1':mod1,'mod2':mod2,'press':press}

def _getWidgetReturnTypeValue(widgetComanndName=''):
    r"""
        QtWidgetsの各コマンド別の取得アトリビュート文字を返す関数
    """
    dictInfo = {
        # QWidget Class
        'QAbstractButton'  : 'text',
        'QAbstractSlider'  : 'value',
        'QAbstractSpinBox' : 'text',
        'QCalendarWidget'  : 'yearShown,monthShown',
        'QComboBox'        : 'currentText',
        'QDesignerActionEditorInterface'    : '',
        'QDesignerFormWindowInterface'      : '',
        'QDesignerObjectInspectorInterface' : '',
        'QDesignerPropertyEditorInterface'  : '',
        'QDesignerWidgetBoxInterface'       : '',
        'QDesktopWidget'   : '',
        'QDialog'          : 'result',
        'QDialogButtonBox' : '',
        'QDockWidget'      : 'widget',
        'QFocusFrame'      : 'widget',
        'QFrame'           : '',
        'QGroupBox'        : 'title',
        'QKeySequenceEdit' : '',
        'QLineEdit'        : 'text',
        'QMacCocoaViewContainer' : '',
        'QMacNativeWidget'       : '',
        'QMainWindow'      : '',
        'QMdiSubWindow'    : 'widget',
        'QMenu'            : 'title',
        'QMenuBar'         : '',
        'QOpenGLWidget'    : '',
        'QProgressBar'     : 'value',
        'QQuickWidget'     : '',
        'QRubberBand'      : '',
        'QSizeGrip'        : '',
        'QSplashScreen'    : '',
        'QSplitterHandle'  : '',
        'QStatusBar'       : '',
        'QSvgWidget'       : '',
        'QTabBar'          : 'tabText',
        'QTabWidget'       : 'tabText',
        'QToolBar'         : '',
        'QWizardPage'      : 'title',
        
        'QLabel'           : 'text',
        'QTextEdit'        : 'toPlainText',
        'QCheckBox'        : 'value',
        
        # QAbstractSpinBox Class
        'QSpinBox'         : 'value',
        'QDoubleSpinBox'   : 'value',
        'QDateTimeEdit'    : 'value',
        
        # other
        '' : None,
        
    }
    
    return dictInfo[widgetComanndName]

###############################################################################
## - Widget

class EventBaseWidget(QtWidgets.QWidget):
    r"""
        イベントとメニュー付きのウィジェットクラス
        GUIで共通して使用される標準ウィジェットとなる
    """
    KEYMETHOD = KeyMethod()
    
    def __init__(self,parent=None):
        r"""
        """
        super(EventBaseWidget,self).__init__(parent)
        
        self.debugFlag = False
        self.title     = self.__class__.__name__
        self.version   = '0.0a'
        self.author    = 'Matsuzawa Shinya'
        self.release   = '9999/99/99'
        self.update    = '9999/99/99'
        self.wincolor  = []
        self.mc        = QtCore.QPoint(0,0)
        self.mouseType = None
        
        self.setAcceptDrops(True)
        self.setWindowFlags(_setWindowFlagsDict[''])
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.exePopMenu)
        
        self.setPaintEventColor(8,8,8,192)
        self.PSL = PathStoreList('EventBaseWidget')
    
    ## ------------------------------------------------------------------------
    ## Event
    
    def getMouseType(self,pos):
        r"""
            マウスクリックのパターン返し
        """
        return self.KEYMETHOD._mouseType(pos)
    
    def getKeyMask(self):
        r"""
            キーマスクのリターン
        """
        return self.KEYMETHOD._keyMask()
    
    def getKeyMask2(self,typeList=[]):
        r"""
            キーマスクのリターン(指定タイプ)
        """
        return self.KEYMETHOD._keyMask2()
    
    def getKeyType(self,event=None):
        r"""
        """
        return self.KEYMETHOD._keyType(event)
        
    def keyPressEvent(self,event):
        r"""
            キープレス時のイベント情報
        """
        super(EventBaseWidget,self).keyPressEvent(event)
        
        key,mask = self.getKeyType(event),self.getKeyMask()
        # print(2222,QtCore.Qt.Key_Meta==key['key'])
        
        if (key['press'] == 'F1'):
            pass
        elif (key['mod1'] == mask['ctrl,shift'] and key['press'] == 'F10'):
            self.printRect()
        elif (key['mod1'] == mask['ctrl']  and key['press'] == 'F11'):
            self.frontmostSwitch(True)
        elif (key['mod1'] == mask['shift'] and key['press'] == 'F11'):
            self.frontmostSwitch(False)
        elif (key['mod1'] == mask['ctrl']  and key['press'] == 'F12'):
            self.setDebugFlag(True)
        elif (key['mod1'] == mask['shift'] and key['press'] == 'F12'):
            self.setDebugFlag(False)
        elif (key['mod1'] == mask['ctrl']  and key['press'] == 'F5'):
            print(1111)
        elif (key['press'] == 'Esc'):
            self._WEA = WidgetEventAction()
            self._WEA.setSelf(self)
            self._WEA.setCloseTime(150)
            self._WEA.setCloseTimeElapsed()
        else:
            None
        
    def mousePressEvent(self,event):
        r"""
            マウスのクリックが押された時の動作
        """
        self.mouseType          = self.getMouseType(event)
        self.mc                 = event.pos()
        self.o_posX,self.o_posY = None,None
        self.pressFlag          = True
    
    def mouseDoubleClickEvent(self,event):
        r"""
            ダブルクリックのイベント
        """
        pass
    
    def mouseReleaseEvent(self, event):
        r"""
            マウスのクリックが離された時の動作
        """
        self.mouseType          = self.getMouseType(event)
        self.o_posX,self.o_posY = None,None
        self.pressFlag          = False

    def mouseMoveEvent(self,event):
        r"""
            マウスが動いた時の動作
        """
        e_x ,e_y  = event.x(),event.y()
        eg_x,eg_y = event.globalX(),event.globalY()
        if self.mouseType == 1:
            if self.pressFlag:
                self.move(self.mapToParent(event.pos()-self.mc))
            if self.debugFlag:
                w = 'W:{}-{}={}'.format(eg_x,e_x,(eg_x-e_x))
                h = 'H:{}-{}={}'.format(eg_y,e_y,(eg_y-e_y))
                print('\t{},{}'.format(w.ljust(16,' '),h))
        elif self.mouseType == 2:
            pass
        elif self.mouseType == 3:
            if self.o_posX and self.o_posY:
                s_posX,s_posY = (e_x-self.o_posX),(e_y-self.o_posY)
                self.resize(
                    self.rect().width() +s_posX,
                    self.rect().height()+s_posY
                )
                if self.debugFlag:
                    w = 'W:{}-{}={}'.format(e_x,self.o_posX,s_posX)
                    h = 'H:{}-{}={}'.format(e_y,self.o_posY,s_posY)
                    print('\t{},{}'.format(w.ljust(16,' '),h))
        else:
            pass
        self.o_posX,self.o_posY = e_x,e_y
    
    def paintEvent(self, event):
        r"""
            描画のイベント
        """
        c = self.wincolor
        p = QtGui.QPainter(self)
        p.setRenderHints(QtGui.QPainter.Antialiasing)
        p.setBrush(QtGui.QColor(c[0],c[1],c[2],c[3]))
        p.drawRoundedRect(self.rect(),16,16)
        
    def enterEvent(self,event):
        r"""
            カーソルが入ったときのイベントアクション
        """
        pass
    
    def leaveEvent(self,event):
        r"""
            カーソルが出たときのイベントアクション
        """
        pass
    
    def closeEvent(self, event):
        r"""
            閉じたときのイベント
        """
        pass
    
    def dragEnterEvent(self, event):
        r"""
            ドラッグのイベント
        """
        mime = event.mimeData()
        event.accept() if mime.hasUrls() else event.ignore()
    
    def dropEvent(self, event):
        r"""
            ドロップのイベント
        """
        mime = event.mimeData()
        path = mime.urls()
        for p in path:
            if self.debugFlag:
                print('.path()       ={}'.format(p.path()))        # ゴミ
                print('.toLocalFile()={}'.format(p.toLocalFile())) # 神
                print('.toString()   ={}'.format(p.toString()))
    
    ## ------------------------------------------------------------------------
    ## Func
    
    def setPaintEventColor(self,r,g,b,a):
        r"""
            ウィジェットバックグラウンドカラーの設定
        """
        self.wincolor = [r,g,b,a]
    
    ## ------------------------------------------------------------------------
    ## Func
    
    def setDebugFlag(self,value=True):
        r"""
            デバックフラグのスイッチ
        """
        self.debugFlag = value
        print(u'Debug mode = %s'%(value))
    
    def getWidgetSize(self):
        r"""
            ウィジェットサイズのリターン
        """
        return (self.rect().width(),self.rect().height())
    
    def getGeometryPosition(self):
        r"""
            widget位置のリターン
        """
        return (self.geometry().x(),self.geometry().y())
    
    def printRect(self):
        r"""
            guiサイズをプリント
        """
        print('W:{}\nH:{}'.format(self.rect().width(),self.rect().height()))
    
    def frontmostSwitch(self,switch=True):
        r"""
            最前面を保持するかどうかの切り替え関数
        """
        self.setWindowFlags(
            _setWindowFlagsDict['tophint={}'.format(
                'True' if switch else 'False')]
        )
        self.show() # 再描画しないと反映されない
        print(u'+ WindowStaysOnTopHint = {}'.format(switch))
    
    def setOpenWidgetInfo(self,titleName):
        r"""
            window起動時の位置・サイズ調整の設定関数
        """
        self.PSL.setPath(self.PSL.windowPrefPath())
        try:
            _d  ,_t   = self.PSL.getJsonFile(),titleName
            _ow ,_oh  = self.getWidgetSize()
            _ows,_ohs = int(_ow*0.4),int(_oh*0.4)
            try:
                desktopSize = QtWidgets.QApplication.desktop()
                _dw,_dh = desktopSize.width(),desktopSize.height()
                # 条件に満たしていればその位置に移動,そうでない場合は初期位置に
                if ((0-_ows) < _d[_t]['pos'][0] < (_dw-_ow) and
                    (0)      < _d[_t]['pos'][1] < (_dh-_ohs)
                ): 
                    self.move(_d[_t]['pos'][0], _d[_t]['pos'][1])
            except:
                pass
            self.resize(_d[_t]['size'][0],_d[_t]['size'][1])
            return _d[_t]
        except:
            self.PSL.checkPathFile()
    
    def setCloseWidgetInfo(self,titleName):
        r"""
            window終了時の位置・サイズ調整の設定関数
        """
        _x,_y = self.getGeometryPosition()
        _w,_h = self.getWidgetSize()
        _d,_t = self.PSL.getJsonFile(),titleName
        if not _d.get(_t):
            _d[_t] = {'pos':[_x,_y],'size':[_w,_h]}
        else:
            if _d[_t].get('pos') and _d[_t].get('size'):                
                if (_d[_t]['pos'][0]  != _x or _d[_t]['pos'][1]  != _y or
                    _d[_t]['size'][0] != _w or _d[_t]['size'][1] != _h
                ):
                    _d[_t] = {'pos':[_x,_y],'size':[_w,_h]}
        self.PSL.setDict(_d)
        self.PSL.setJsonFile()
    
    ## ------------------------------------------------------------------------
    ## menu func
    
    def toSettings(self,obj,title,author,version,update,release):
        r"""
            メインレイアウトの部分で文字設定を送るための関数
        """
        obj.main.title.setText(title)
        obj.main.author.setText ('Author : {}'.format(author))
        obj.main.version.setText('Version : {}'.format(version))
        obj.main.update.setText ('Last update : {}'.format(update))
        obj.main.release.setText('Release : {}'.format(release))
        
    def exeAbout(self):
        r"""
            aboutの情報設定(テンプレート)
        """
        c_pos = QtGui.QCursor().pos()
        _x,_y = c_pos.x(),c_pos.y()
        if shibokenFlag:
            about = showWindow(AboutUI,wfFlag=False)
            about.setGeometryPosition(_x,_y)
        else:
            about = AboutUI()
            about.show()
            about.setGeometryPosition(_x,_y)
        self.toSettings(
            obj     = about,
            title   = self.title,
            author  = self.author,
            version = self.version,
            release = self.release,
            update  = self.update,
        )
    
    def exePopMenu(self):
        r"""
            ポップメニュー窓口(Ctrl+Shit+Alt)
        """
        if self.getKeyType()['mod2'] == self.getKeyMask()['ctrl,shift,alt']:
            menu = QtWidgets.QMenu()
            menu.addAction('About', self.exeAbout)
            menu.exec_(QtGui.QCursor.pos())
    
## ----------------------------------------------------------------------------
    
class WidgetEventAction(EventBaseWidget):
    r"""
        ウィジェット外部の共有パーツクラス
        タイトル/オプション/クローズボタンなど
    """
    def __init__(self,parent=None):
        r"""
            __init__
        """
        super(WidgetEventAction,self).__init__(parent)
        
        self.title  = ''
        self.layout = None
        self.selfClass = None
        self._hide = []
        self._time = 250
        
        self._childrenObj  = None
        self._optionWidget = None
    
    def newOptionWidget(self):
        r"""
            オプションウィジェットをセット
        """
        self._optionWidget = OptionWidget()
        
    def setOptionWidget(self,widget):
        r"""
            オプションウィジェットをセット
        """
        self._optionWidget = widget
    
    def getOptionWidget(self):
        r"""
            オプションウィジェットを取得
        """
        return self._optionWidget
    
    def showOptionWidget(self):
        r"""
            オプションウィジェットを取得
        """
        w = self.getOptionWidget()
        w.setWindowFlags(_setWindowFlagsDict['tophint=True'])
        w.show()
    
    def setTitle(self,name):
        r"""
            タイトルのセット
        """
        self.title = name
    
    def setSelf(self,s):
        r"""
            クラスのセット
        """
        self.selfClass = s
    
    def getSelf(self):
        r"""
            クラスのリターン
        """
        return self.selfClass
    
    def getTitle(self):
        r"""
            タイトルのリターン
            
            Returns:
                any:
        """
        return self.title
    
    def setCloseTime(self,time):
        r"""
            クローズするタイムを設定
        """
        self._time = time
    
    def getCloseTime(self):
        r"""
            クローズタイムのリターン
        """
        return self._time
    
    def setHide(self,hide):
        r"""
            レイアウトハイド変数を設定
                str(str) :lower変換しリスト追加
                list(tuple):forで回しlower変換しリスト追加
        """
        if isinstance(hide,bytes):
            self._hide.append(hide.lower())
        elif isinstance(hide,list) or isinstance(hide,tuple):
            for h in hide:
                self._hide.append(h.lower())
        else:
            self._hide.append(hide.lower())
            
    def getHide(self):
        r"""
            レイアウトハイド変数を返す
        """
        return self._hide
    
    def setWidget(self):
        r"""
            ウィジェットのセットレイアウト
        """
        self.t  = QtWidgets.QLabel(self.getTitle())
        self.t.setStyleSheet(ss.LABEL_STYLE)
        self.o  = QtWidgets.QPushButton('')
        self.c  = QtWidgets.QPushButton('')
        self.mi = QtWidgets.QPushButton('')
        if iconFlag:
            self.o.setStyleSheet(ss.BORDER_STYLE_2)
            self.o.setIcon(msAppIcons.iconPath('ui_option_white'))
            self.o.setIconSize(QtCore.QSize(16,16))
            self.c.setStyleSheet(ss.BORDER_STYLE_2)
            self.c.setIcon(msAppIcons.iconPath('ui_close_white'))
            self.c.setIconSize(QtCore.QSize(16,16))
            self.mi.setStyleSheet(ss.BORDER_STYLE_2)
            self.mi.setIcon(msAppIcons.iconPath('ui_minimize_white'))
            self.mi.setIconSize(QtCore.QSize(16,16))
        else:
            self.o.setText('o')
            self.o.setMaximumWidth(32)
            self.c.setText('x')
            self.c.setMaximumWidth(32)
            self.mi.setText('x')
            self.mi.setMaximumWidth(32)
        self.o.clicked.connect(lambda:self.openOptionWidget())
        self.c.clicked.connect(lambda:self.setCloseTimeElapsed())
        self.mi.clicked.connect(lambda:self.setMinimized())
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.t ,alignment=QtCore.Qt.AlignLeft)
        h_layout.addStretch()
        h_layout.addWidget(self.o ,alignment=QtCore.Qt.AlignRight)
        h_layout.addWidget(self.mi,alignment=QtCore.Qt.AlignRight)
        h_layout.addWidget(self.c ,alignment=QtCore.Qt.AlignRight)
        self.layout = h_layout
        
        self.hideSetting()
        
    def getWidget(self):
        r"""
            レイアウトをリターン
        """
        return self.layout
    
    def setCloseTimeElapsed(self):
        r"""
            フェードアウトする動作を追加
        """
        s = self.getSelf()
        t = self.getCloseTime()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(t)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(s.close)
        self.timer.start()
        # Python3.7 対応
        self.pa = QtCore.QPropertyAnimation(s,('windowOpacity'.encode()))
        self.pa.setStartValue(1.0)
        self.pa.setEndValue(0.0)
        for i in range(0,10,1):
            _i = ((i+1)*0.1)
            self.pa.setKeyValueAt(_i,(1.0-(_i*_i)))
        # self.pa.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self.pa.setDuration(t)
        self.pa.start(QtCore.QAbstractAnimation.DeleteWhenStopped)
        
        '''
        setEasingCurveの種類(https://doc.qt.io/qt-5/qeasingcurve.html)
        QtCore.QEasingCurve:
            .Linear
            .InQuad    .OutQuad    .InOutQuad    .OutInQuad
            .InCubic   .OutCubic   .InOutCubic   .OutInCubic
            .InQuart   .OutQuart   .InOutQuart   .OutInQuart
            .InQuint   .OutQuint   .InOutQuint   .OutInQuint
            .InSine    .OutSine    .InOutSine    .OutInSine
            .InExpo    .OutExpo    .InOutExpo    .OutInExpo
            .InCirc    .OutCirc    .InOutCirc    .OutInCirc
            .InElastic .OutElastic .InOutElastic .OutInElastic
            .InBack    .OutBack    .InOutBack    .OutInBack
            .InBounce  .OutBounce  .InOutBounce  .OutInBounce
        '''
    
    ## ------------------------------------------------------------------------
    ## button commands
    
    def setWidgetChildrenObject(self,obj):
        r"""
        """
        self._childrenObj = obj
    
    def getWidgetChildrenObject(self):
        r"""
        """
        return self._childrenObj
    
    def openOptionWidget(self):
        r"""
            オプションウィジェット表示
        """
        func = 'setOptionWidgetChildrenData'
        gwho = self.getWidgetChildrenObject()
        if hasattr(gwho,func):
            self.newOptionWidget()
            exec('gwho.{}()'.format(func))
            self.showOptionWidget()
    
    def setMinimized(self):
        r"""
            最小化設定
        """
        self.getSelf().showMinimized()
    
    def hideSetting(self):
        r"""
            ハイドオブジェクト変数がが設定されていたら実行
        """
        ho = self.getHide()
        if '-t' in ho or 'title' in ho:
            self.t.hide()
        if '-o' in ho or 'option' in ho:
            self.o.hide()
        if '-c' in ho or 'close' in ho:
            self.c.hide()
        if '-m' in ho or 'minimize' in  ho:
            self.mi.hide()
    
    ## ------------------------------------------------------------------------
    ## Event
    
    def mousePressEvent(self, pos):
        r"""
            このクラスでは不要なのでオーバーライドで初期化
        """
        pass
    
    def mouseReleaseEvent(self, pos):
        r"""
            このクラスでは不要なのでオーバーライドで初期化
        """
        pass

    def mouseMoveEvent(self, pos):
        r"""
            このクラスでは不要なのでオーバーライドで初期化
        """
        pass

## ----------------------------------------------------------------------------

class OptionWidget(EventBaseWidget):
    r"""
        オプションウィジェット用のカスタマイズクラス
    """
    def __init__(self,parent=None):
        r"""
            初期化設定
        """
        super(OptionWidget,self).__init__(parent)
        
        self.guiObj         = None
        # self._dictData      = {}
        self._setWidgetDict = {}
        
    def __repr__(self):
        r"""
        """
        return '+ Func <<{}>>'.format(self.__class__.__name__)
    
    def setWidgetDict(self,d):
        r"""
            ウィジェット作成の辞書セット
        """
        self._setWidgetDict = d
        
    def getWidgetDict(self):
        r"""
            ウィジェット作成の辞書取得
        """
        return self._setWidgetDict
    
    def createWidgetParts(self):
        r"""
            セットされている辞書データを元にGUIレイアウトを作成しそれを返す
        """
        def dictOrder(d):
            r"""
                辞書の先頭のkey情報を昇順ソート
            """
            order = []
            for k,v in d.items():
                order.append(k)
            order.sort()
            return order   
            
        _createLayout = QtWidgets.QVBoxLayout()
        
        _d = self.getWidgetDict()
        for _o in dictOrder(_d):
            _index,_label = _o.split(',')
            _hLayout = QtWidgets.QHBoxLayout()
            _wid     = _d[_o]['widget']
            _widget  = eval('QtWidgets.{}()'.format(_wid['name']))
            # widgetObjectのウィジェット設定をアップデート
            _d[_o]['widgetObject'] = _widget
            for i in range(999):
                _attr = _d[_o].get((
                    'attribute{}'.format('' if i==0 else i)))
                if not _attr:
                    break
                for _a in _attr:
                    at,av,execmd = _a,_attr[_a],''
                    if isinstance(av,bytes):
                        execmd = ("_widget.{}('{}')".format(at,av))
                    elif isinstance(av,int):
                        execmd = ("_widget.{}({})".format(at,av))
                    elif isinstance(av,float):
                        execmd = ("_widget.{}({})".format(at,av))
                    elif isinstance(av,list):
                        execmd = ("_widget.{}({})".format(at,av))
                    elif isinstance(av,tuple):
                        execmd = ("_widget.{}(*{})".format(at,av))
                    else:
                        continue
                    try:
                        exec(execmd)
                    except:
                        pass
            _hLayout.addWidget(QtWidgets.QLabel(_label),5)
            _hLayout.addWidget(_widget,5)
            _createLayout.addLayout(_hLayout)
        
        # self.setAfterUpdateDict(_d)
        
        w = QtWidgets.QWidget()
        w.setLayout(_createLayout)
        return w
    
    # def setAfterUpdateDict(self,d):
        # r"""
            # 更新後の辞書データを保存
        # """
        # self._dictData = d
    
    # def getAfterUpdateDict(self):
        # r"""
            # 更新後の辞書データを取得
        # """
        # return self._dictData
    
    def setGuiObject(self,w):
        r"""
            各guiのOptionInfoDataから送られてきたguiオブジェクトを格納する関数
        """
        self.guiObj = w
    
    def mouseDoubleClickEvent(self,event):
        r"""
            ダブルクリックのイベント
        """
        self.WEA = WidgetEventAction()
        self.WEA.setSelf(self)
        self.WEA.setCloseTime(150)
        self.WEA.setCloseTimeElapsed()
    
    def closeEvent(self,event):
        r"""
            閉じた際の設定されているウィジェット項目の内容を
            各ウィジェットに反映する
        """
        super(OptionWidget,self).closeEvent(event)
        
        print(888,self.guiObj)
        
## ----------------------------------------------------------------------------

class ImageWidget(QtWidgets.QWidget):
    r"""
        イメージをラベル化する
    """
    def __init__(self, parent=None):
        r"""
            メインUI
        """
        super(ImageWidget, self).__init__(parent)
        
        self.__widget     = None
        self.__w,self.__h = 1.0,1.0
        self.__imageLabel = QtWidgets.QLabel()
        self.__lineEdit   = QtWidgets.QLineEdit()
    
    ## ------------------------------------------------------------------------
    
    def newLabel(self):
        r"""
            新しいウィジェットを作成する
        """
        self.__imageLabel = QtWidgets.QLabel()
    
    def setScaled(self,w,h):
        r"""
            画像スケールサイズを設定
        """
        self.__w = w
        self.__h = h
    
    def getScaled(self):
        r"""
            スケールサイズのリターン
        """
        return (self.__w,self.__h)
   
    def setSendLabel(self,label):
        r"""
            送られてきたlabelをアサインする
        """
        self.__imageLabel = label
    
    def setImage(self,path):
        r"""
            イメージパスをQLabelにpixmap化
        """
        pixmap = QtGui.QPixmap(QtGui.QImage(path))
        newmap = pixmap.scaled(
            int(self.rect().width() *self.__w),
            int(self.rect().height()*self.__h),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        self.__imageLabel.setPixmap(newmap)
    
    def getImage(self):
        r"""
            イメージウィジェットのリターン
        """
        return self.__imageLabel
    
    ## ------------------------------------------------------------------------
    
    def newLineEdit(self):
        r"""
            新しいウィジェットを作成する
        """
        self.__lineEdit = QtWidgets.QLineEdit()
    
    def setSendLineEdit(self,le):
        r"""
            送られてきたlineEditをアサインする
        """
        self.__lineEdit = le

    def setText(self,word):
        r"""
            文字列をlineEdit化
        """
        self.__lineEdit.setText(word)
    
    def getText(self):
        r"""
            lineEditのウィジェットをリターン
        """
        return self.__lineEdit

## ----------------------------------------------------------------------------

class ScrolledWidget(QtWidgets.QScrollArea):
    r"""
        UIをスクロールを行うための設定
    """
    KEYMETHOD = KeyMethod()
    
    def __init__(self,parent=None):
        r"""
            スクロールエリアをウィジットにセットする
        """
        super(ScrolledWidget, self).__init__(parent)
        
        self.setWidgetResizable(True) # 横幅にフィットさせる記述
        self.setStyleSheet(self.getStyleSheet())        
        
        # スクロールされた際の実行コマンド紐付け
        self.verticalScrollBar().valueChanged.connect(self.scrolledMoveValue)
        self.horizontalScrollBar().valueChanged.connect(self.scrolledMoveValue)
        
        buf = 'msToolScrollWidget'
        widget = QtWidgets.QWidget()
        widget.setObjectName(buf)
        widget.setStyleSheet('QWidget#%s{background:transparent;}'%(buf))
        self.buildUI(widget)
        self.setWidget(widget)
        
        self._epc = EventPackageChildren()
    
    ## ------------------------------------------------------------------------
    ## Layout build func
    
    def buildUI(self,panret):
        r"""
            継承した先で実行するオーバーライド用関数
        """
        pass
    
    def getStyleSheet(self):
        r"""
            スタイルシートの設定文字列取得
        """
        _tbc     = ss.MAINUIBGC_C
        reflect  = ''
        
        # QLabelカラーを白色に
        reflect += ('QLabel{color: #EEE;}')
        
        # QScrollArea全体設定
        reflect += ('QScrollArea{background-color:%s;}'%(_tbc))
        
        # QScrollBar個別設定
        _style   = 'border:1px solid #BBB;background-color:%s;'%(_tbc)
        for vh in ('vertical','horizontal'):
            QSB  = 'QScrollBar'
            reflect += ('%s:%s{%s;}'%(QSB,vh,_style))
            reflect += ('%s::sub-line:%s{%s}'%(QSB,vh,_style))
            reflect += ('%s::add-line:%s{%s}'%(QSB,vh,_style))
        
        return reflect
    
    def getKeyMask(self):
        r"""
            キーマスクのリターン
        """
        return self.KEYMETHOD._keyMask()
    
    def getKeyMask2(self,typeList=[]):
        r"""
            キーマスクのリターン(指定タイプ)
        """
        return self.KEYMETHOD._keyMask2()
    
    def getKeyType(self,event=None):
        r"""
            キータイプのリターン
        """
        return self.KEYMETHOD._keyType(event)
    
    def scrolledMoveValue(self,a):
        r"""
            スクロールした際の動作
        """
        pass
        
    ## ------------------------------------------------------------------------
    ## common parent event setting
    
    def setEventPackage(self,packaging):
        r"""
            子と関連性をためのメソッドパッケージを親から引き継いで設定する
            オーバーライド用メソッド
        """
        self._epc.setEventPackageMethod(packaging)

    def getEventPackage(self):
        r"""
            子と関連性をためのメソッドパッケージを取得
        """
        return self._epc.getEventPackageMethod()
        
    ## ------------------------------------------------------------------------
    ## Pre process
    
    def exePreProcess(self):
        r"""
        """
        print('>>> Execute pre process, "{}".'.format(self.__class__.__name__))
    
    ## ------------------------------------------------------------------------
    ## Post process
    
    def exePostProcess(self):
        r"""
        """
        print('>>> Execute post process, "{}".'.format(self.__class__.__name__))
    
###############################################################################
## - Sub widget parts

class ListView(QtWidgets.QListView):
    r"""
        カテゴリ毎のアイテムを作るリストビュー
    """
    KEYMETHOD = KeyMethod()

    def __init__(self, parent=None):
        r"""
            メインUI
        """
        super(ListView, self).__init__(parent)
        
        self.rootPath  = ''
        self.childData = []
        self.itemMask  = []
        
        self.setMinimumSize(1, 1)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        
        model = QtGui.QStandardItemModel(0, 1)
        
        self.setModel(model)
        self.selModel = QtCore.QItemSelectionModel(model)
        self.setSelectionModel(self.selModel)
        self.selModel.selectionChanged.connect(self.update)
    
    def getKeyMask(self):
        r"""
            キーマスクのリターン
        """
        return self.KEYMETHOD._keyMask()
    
    def getKeyMask2(self,typeList=[]):
        r"""
            キーマスクのリターン(指定タイプ)
        """
        return self.KEYMETHOD._keyMask2()
    
    def getKeyType(self,event=None):
        r"""
            キータイプのリターン
        """
        return self.KEYMETHOD._keyType(event)
    
    def clear(self):
        r"""
            リストのクリア
        """
        model = self.model()
        model.removeRows(0, model.rowCount())
    
    def allClear(self):
        r"""
            選択リストのクリア
        """
        for i,cl in enumerate(self.clearList):
            if i == 0:
                continue
            [cl2.clear() for cl2 in cl]
    
    def setPath(self, path):
        r"""
            パスをアイテムをセットする
        """
        self.rootPath = path
        self.clear()
        
        model = self.model()
        for file in os.listdir(path):
            if not os.path.isdir(os.path.join(path,file)):
                print('+ Not dir name = [%s]' % (file))
                continue
            if self.itemMask:
                if file in self.itemMask:
                    item = QtGui.QStandardItem(file)
                    model.setItem(model.rowCount(), 0, item)
            else:
                item = QtGui.QStandardItem(file)
                model.setItem(model.rowCount(), 0, item)
    
    def update(self, selected, deselected):
        r"""
            こどものデータをアップデートする
        """
        if not self.childData or not selected:
            return
        
        path = os.path.join(self.rootPath, self.nowSelectItem())
        
        ([cd.setPath(path) if os.path.isdir(path) else
            cd.clear() for cd in self.childData])
        
    def nowSelectItem(self):
        r"""
            選択しているアイテムリストのリターン
        """
        return self.selectionModel().currentIndex().data()
    
    def selectedFile(self):
        r"""
            選択データのリターン
        """
        data = self.nowSelectItem()
        if not data:
            return
        return os.path.join(self.rootPath, data)

## ----------------------------------------------------------------------------

class PushButton(QtWidgets.QPushButton):
    r"""
        QPushButton/カスタムクラス
    """
    def __init__(self,buttontext='',parent=None):
        r"""
        """
        super(PushButton,self).__init__(buttontext,parent)
        
        self.resetStyleWord()
        self.addStyleWord(resetflag=True)
        self.setDefaultStyle()
    
    ## ------------------------------------------------------------------------
    ## base setting
    
    def getDefaultWord(self):
        r"""
            デフォルトのスタイル書式の取得
        """
        return 'QPushButton{%(addStyle)s}'
        
    def resetStyleWord(self):
        r"""
            スタイルシート書式のリセット
        """
        self.__styleword = self.getDefaultWord();
            
    ## ------------------------------------------------------------------------
    ## edit
            
    def addStyleWord(self,setword=None,resetflag=False):
        r"""
            スタイル書式を設定/初期化、内部のスタイルワードを連結
        """
        if resetflag:
            self.__addWord = ''
        elif setword!=None:
            if isinstance(setword,str):
                self.__addWord += setword
            elif isinstance(setword,list):
                self.__addWord += (''.join(setword))
            else:
                pass
    
    def getStyleWord(self):
        r"""
            スタイル書式を設定する内部のスタイルワードを連結
        """
        return self.__addWord
    
    def setStyleSheetWord(self,setword='',returnflag=False):
        r"""
            スタイル書式をセットするメソッド
            setwordが指定されていればそちらを優先し、指定が無ければ
            既にセットされている書式を適用する。
        """
        self.__styleword = self.getDefaultWord() % {
            'addStyle' : setword if setword else self.getStyleWord()
        }
        if returnflag:
            return self.__styleword
    
    def getStyleSheetWord(self):
        r"""
            スタイル書式をリターン
        """
        return self.__styleword
        
    def setBaseStyle(self):
        r"""
            起動時の基本スタイルを設定
        """
        self.resetStyleWord()
        self.setStyleSheetWord('color:111;')
        self.applyStyleSheet()
    
    def setDefaultStyle(self):
        r"""
            ボタンレイアウトスタイルをデフォルト設定にするメソッド
        """
        self.setBaseStyle()
    
    ## ------------------------------------------------------------------------
    ## color edit
    
    def getGradientColor(self,direction=1,col1='#111',col2='#EEE',col3='#E11'):
        r"""
            グラデーションカラーを取得
            col1 : 開始色
            col2 : 終了色
            col3 : 中間色
            direction : グラデーション方向
                1  = 縦2色(デフォルト)
                12 = 縦2色, 13 = 縦3色
                22 = 横2色, 23 = 縦3色
                32 = 対角線2色, 33 = 対角線3色
        """
        CSM = ss.ColorStyleManagement()
        gradientDict = {
            1  : CSM.baseDefaultGradationColor(),
            12 : CSM.baseVerticalGradationColor2(),
            13 : CSM.baseVerticalGradationColor3(),
            22 : CSM.baseHorizonGradationColor2(),
            23 : CSM.baseHorizonGradationColor3(),
            32 : CSM.baseDiagonalGradationColor2(),
            33 : CSM.baseDiagonalGradationColor3(),
        }
        varticalstyle = gradientDict.get(direction)
        if not varticalstyle:
            return None
        return (varticalstyle%(col1,col2,col3)
            if int(str(direction)[-1])==3 else varticalstyle%(col1,col2))
    
    ## ------------------------------------------------------------------------
    ## execute
    
    def applyStyleSheet(self,logflag=False):
        r"""
            セットされているスタイル書式で当PushButtonにsetStyleSheetする
        """
        styleword = self.getStyleSheetWord()
        self.setStyleSheet(styleword)
        if logflag:
            print('>> Set stylesheet word,\n\t{}'.format(styleword))
        
## ----------------------------------------------------------------------------

class SuggestView(EventBaseWidget):
    r"""
        予測変換サジェストウィジェット
    """
    _listViewStyleSheetDict= {
        'default':{
            'color':'#DDD',
            'background-color':'#383838',
        },
        'selected':{
            'color':'#FFF',
            'background-color':'#27A',
        },
        'hover':{
            'color':'#FFF',
            'background-color':'#08D',
        },
    }
    
    def __init__(self,parent=None):
        r"""
            初期設定
        """
        super(SuggestView,self).__init__(parent)
        
        self.setTextLineWidget()
        self.setSuggestItemList()
        self.eachMovePositioning(self.emptyFunc)
        
        self.parentSuggestFunc = self.suggestInsert
        self.wincolor = [8,8,32,192]
        self.resize(200,240)
        self.setWindowFlags(_setWindowFlagsDict['tophint=True'])
        
        self.setListView(ListView())
        __view = self.getListView()
        self.setLietViewStyleSheet()
        __view.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        __view.setFocusPolicy(QtCore.Qt.NoFocus)
        __view.setAlternatingRowColors(False)
        __view.doubleClicked.connect(self.exeSuggestInsert)
        
        model = QtGui.QStandardItemModel()
        __view.setModel(model)
        selection_model = QtCore.QItemSelectionModel(model)
        __view.setSelectionModel(selection_model)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(__view)
    
    ## ------------------------------------------------------------------------
    ## event
    
    def paintEvent(self,event):
        r"""
            描画のイベント（オーバーライド）
        """
        c = self.wincolor
        p = QtGui.QPainter(self)
        p.setRenderHints(QtGui.QPainter.Antialiasing)
        p.setBrush(QtGui.QColor(c[0],c[1],c[2],c[3]))
        p.drawRoundedRect(self.rect(),2,2)
    
    def keyPressEvent(self,event):
        r"""
            キーイベント（オーバーライド）
        """
        super(SuggestView,self).keyPressEvent(event)

        sgview  = self.getListView()
        model   = sgview.model()
        listNum = model.rowCount()
        _key    = self.getKeyType(event)
        _mask   = self.getKeyMask()
        _mask2  = self.getKeyMask2()
        _press  = _key['press']
        
        if _press in ['Up','Down']:
            now     = self.getQModelIndexList()
            index   = now.row()
            if _key['press']=='Up':
                index -= 1
                # アイテムのトップに来たら最下層のアイテムにインデックスをセット
                if index<0:
                    index = listNum-1
            else:
                index += 1
                # アイテムの最下層に来たらトップのアイテムにインデックスをセット
                if index>=listNum:
                    index = 0
            sgview.setCurrentIndex(model.createIndex(index,0))
        elif _press in ['Left','Right'] and _key['mod1']==_mask2(['ctrl']):
            self.exeHide()
        elif _press in ['Return','Enter']:
            self.exeSuggestInsert()
        else:
            pass
    
    ## ------------------------------------------------------------------------
    ## setting
    
    def setLietViewStyleSheet(self):
        r"""
            リストビュースタイルシート設定
        """
        _KD = self.getListViewStyleSheetDict()
        reflect = '''
            QListView{background-color:%s;color:%s;}
            QListView::item:selected:!active{background-color:%s;color:%s;}
            QListView::item:!selected:hover{background-color:%s;color:%s;}
        '''%(
            _KD['default']['background-color'] ,_KD['default']['color'],
            _KD['selected']['background-color'],_KD['selected']['color'],
            _KD['hover']['background-color']   ,_KD['hover']['color'],
        )
        self.getListView().setStyleSheet(reflect)
    
    def setListViewStyleSheetDict(self,d):
        r"""
            スタイルシート親リスト更新
        """
        self._listViewStyleSheetDict = d
        
    def getListViewStyleSheetDict(self):
        r"""
            スタイルシート親リスト取得
        """
        return self._listViewStyleSheetDict
    
    def createListItem(self,addlist=[]):
        r"""
            送られてきたリストを元にリストアイテム列を生成
        """
        model = self.getListView().model()
        model.removeRows(0,model.rowCount())
        for i,item in enumerate(addlist):
            model.setItem(i,0,QtGui.QStandardItem(item))
            
        selmodel  = self.getListView().selectionModel()
        itemindex = model.indexFromItem(model.item(0,0))
        selmodel.select(
            itemindex,QtCore.QItemSelectionModel.ClearAndSelect
        )
        selmodel.setCurrentIndex(
            itemindex,QtCore.QItemSelectionModel.ClearAndSelect
        )
    
    ## ------------------------------------------------------------------------
    ## common func
    
    def getQModelIndexList(self):
        r"""
        """
        return ([x for x in
            self.getListView().selectionModel().selectedIndexes()])[0]
    
    def emptyFunc(self):
        r"""
            空の関数
        """
        pass
    
    def exeShow(self):
        r"""
            表示
        """
        self.show()
        
    def exeHide(self):
        r"""
            非表示
        """
        self.hide()
    
    def setListView(self,view):
        r"""
            ListViewのウィジェットを取得
        """
        self._suggestView = view
        
    def getListView(self):
        r"""
            ListViewのウィジェットを取得
        """
        return self._suggestView
    
    ## ------------------------------------------------------------------------
    ## suggest func
    
    def setTextLineWidget(self,widget=None):
        r"""
            テキストラインウィジェット情報をセット
        """
        self.__baseTextLineWidget = widget
        
    def getTextLineWidget(self):
        r"""
            テキストラインウィジェット情報を取得
        """
        return self.__baseTextLineWidget
        
    def setSuggestItemList(self,list=[]):
        r"""
            サジェストリストに登録するアイテムをセット
        """
        self.__suggestItemList = list
        
    def getSuggestItemList(self):
        r"""
            サジェストリストに登録するアイテムを取得
        """
        return self.__suggestItemList
    
    def setSuggestInsert(self,f):
        r"""
            親のサジェストメソッドをセット
        """
        self.parentSuggestFunc = f
    
    def getSuggestInsert(self):
        r"""
            親のサジェストメソッドを取得
        """
        return self.parentSuggestFunc
    
    def exeSuggestInsert(self):
        r"""
            サジェストアイテム選択の実行メソッド
        """
        try:
            self.getSuggestInsert()()
        except:
            traceback.print_exc()
            return False
        return True

    def eachMovePositioning(self,func=None):
        r"""
            移動調整用の関数を指定or実行
            func変数に指定がある場合はセット、指定がなければ取得
        """
        if func:
            self.__moveFunction = (
                func if ('method' in str(type(func))) else self.emptyFunc)
        else:
            return self.__moveFunction if self.__moveFunction else None

    def suggestSetting(self):
        r"""
            設定されている情報を収集しサジェストリスト項目を作成
        """
        textwidget = self.getTextLineWidget()
        if not textwidget:
            raise RuntimeError(
                u'!! QLineEdit is not set. "setTextLineWidget(QLineEdit)" !!')
        itemlist   = self.getSuggestItemList()
        if not itemlist:
            raise RuntimeError(
                u'!! Item list is not set. "setSuggestItemList(list)" !!')
        
        pickList = []
        for item in itemlist:
            input = textwidget.text()
            if not input:
                continue
            word  = item[0]
            # 1文字の場合は正規表現固有の文字に引っかからないように処理を加える
            re_input = (input if len(input)>=2 else '[{}]'.format(input))
            if re.search(re_input,word):
                pickList.append(word)
                continue
                
        # 何も入力されていない/ピックリストがないなら非表示に
        if not textwidget.text() or not pickList:
            self.exeHide()
            return
        
        self.createListItem(pickList)
        self.eachMovePositioning()(textwidget)
        self.exeShow()
        # ウィンドウフォーカスは常にテキストラインに固定
        textwidget.setFocus()
        textwidget.activateWindow()
        
    def suggestInsert(self):
        r"""
            サジェスト(Enter/Return)時の動作
        """
        listAll = self.getQModelIndexList()
        if not listAll or self.isHidden():
            return
            
        # ↓↑キーで移動した際はmodelIndexが正常に取得できないため
        # selectionModel.model()経由でインデックス位置を探知しネームを取得する
        #   ※ クリック選択は問題なく取得される
        now = listAll.data()
        if not now:
            _model = self.getListView().selectionModel().model()
            now    = str(_model.item(listAll.row(),0).data(0))

        now_textLine = self.getTextLineWidget()
        if not now_textLine:
            return
        now_textLine.setText(now)
        self.exeHide()

## ----------------------------------------------------------------------------

class SystemTrayIcon(QtWidgets.QWidget):
    r"""
        システムトレイアイコンの設定
    """
    def __init__(self,showTime=10000,parent=None):
        r"""
            ベース設定
        """
        super(SystemTrayIcon,self).__init__(parent)
        
        self._showTime    = showTime
        self._showTitle   = 'TITLE'
        self._showMessage = 'MSG'
        self._showIcon    = QtWidgets.QSystemTrayIcon.Information
        self._method      = self.tempPrint
        
        exit_act = QtWidgets.QAction('+ Exit(&X)',self,triggered=self.close)
        menu = QtWidgets.QMenu(self)
        menu.addAction(exit_act)
        
        self.trayIcon = QtWidgets.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.setIcon(msAppIcons.iconPath('systemTrayIcon_icon'))
        self.trayIcon.messageClicked.connect(self.activated)
        # self.trayIcon.activated.connect(self.activated)
        self.trayIcon.show()
    
    ## ------------------------------------------------------------------------
    ## set command
    
    def tempPrint(self):
        r"""
        """
        print('---- TEMPLATE ----')
    
    def setTitle(self,t):
        r"""
            タイトルセット
        """
        self._showTitle = t
    
    def setMsg(self,m):
        r"""
            メッセージセット
        """
        self._showMessage = m
        
    def setIcon(self,i):
        r"""
            アイコンセット
        """
        DICT = {
            0 : QtWidgets.QSystemTrayIcon.NoIcon,
            1 : QtWidgets.QSystemTrayIcon.Information,
            2 : QtWidgets.QSystemTrayIcon.Warning,
            3 : QtWidgets.QSystemTrayIcon.Critical,
        }
        d = DICT.get(i)
        self._showIcon = d if d else DICT[0]
    
    def setActivedMethod(self,method):
        r"""
            activated実行時に処理されるメソッドをセット
        """
        self._method = method
        
    def getActivedMethod(self):
        r"""
            activated実行時に処理されるメソッドを取得
        """
        return self._method
    
    ## ------------------------------------------------------------------------
    ## check command
    
    def getSystemTrayAvailable(self):
        r"""
            isSystemTrayAvailableチェック
        """
        if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
            return False
        else:
            return True
    
    def checkSystemTrayAvailable(self):
        r"""
            isSystemTrayAvailableエラー出力
        """
        if not self.getSystemTrayAvailable():
            raise OSError('Can not use system tray on this system !')
    
    ## ------------------------------------------------------------------------
    ## execute command
    
    def started(self):
        r"""
            メッセージ起動
        """
        QtCore.QTimer.singleShot(self._showTime,(lambda:self))
    
    def showMsg(self):
        r"""
            メッセージ設定
        """
        if self.getSystemTrayAvailable():
            self.trayIcon.showMessage(
                self._showTitle,self._showMessage,self._showIcon,
                millisecondsTimeoutHint=self._showTime
            )
    
    def exeHide(self):
        r"""
            メッセージをハイド
        """
        self.trayIcon.hide()
    
    def activated(self,reason=True):
        r"""
            アクティブコマンド
        """
        # if reason==QtWidgets.QSystemTrayIcon.Trigger:
        print('>>> Actived command start.')            
        try:
            self.getActivedMethod()()
        except:
            pass

## ----------------------------------------------------------------------------

class TimeLine(QtCore.QTimeLine):
    r"""
        タイムライン設定のクラス
    """
    ## ------------------------------------------------------------------------
    ## info
    
    r"""
        QTimeLine::EaseInCurve    (0)
            The value starts growing slowly, then increases in speed.
        QTimeLine::EaseOutCurve   (1)
            The value starts growing steadily, then ends slowly.
        QTimeLine::EaseInOutCurve (2)
            The value starts growing slowly, then runs steadily,
            then grows slowly again.
        QTimeLine::LinearCurve    (3)
            The value grows linearly (e.g., if the duration is 1000 ms, -
            the value at time 500 ms is 0.5).
        QTimeLine::SineCurve      (4)
            The value grows sinusoidally.
        QTimeLine::CosineCurve    (5)
    """
    _curveShapeList = {
        0 : QtCore.QTimeLine.EaseInCurve,
        1 : QtCore.QTimeLine.EaseOutCurve,
        2 : QtCore.QTimeLine.EaseInOutCurve,
        3 : QtCore.QTimeLine.LinearCurve,
        4 : QtCore.QTimeLine.SineCurve,
        5 : QtCore.QTimeLine.CosineCurve,
        'easeInCurve'    : QtCore.QTimeLine.EaseInCurve,
        'easeOutCurve'   : QtCore.QTimeLine.EaseOutCurve,
        'easeInOutCurve' : QtCore.QTimeLine.EaseInOutCurve,
        'linearCurve'    : QtCore.QTimeLine.LinearCurve,
        'sineCurve'      : QtCore.QTimeLine.SineCurve,
        'cosineCurve'    : QtCore.QTimeLine.CosineCurve,
    }
    
    def __init__(self,timeout=100,interval=10,curveShape='linearCurve'):
        r"""
            初期設定
        """
        super(TimeLine,self).__init__(timeout)
        self.setUpdateInterval(interval)
        self.setCurveShape(self._curveShapeList[curveShape])
        
    def setTimeout(self,t):
        r"""
            タイムアウト感覚時間をセッティング
        """
        self.setDuration(t)
        
    def setInterval(self,i):
        r"""
            インターバルの時間をセッティング
        """
        self.setUpdateInterval(i)
    
    def setFrameRangeFunc(self,s,e):
        r"""
            スタート,エンドフレーム設定
        """
        self.setFrameRange(s,e)
    
    def setStartFrameFunc(self,t):
        r"""
            スタートフレーム設定
        """
        self.setStartFrame(t)
        
    def setEndFrameFunc(self,t):
        r"""
            エンドフレーム設定
        """
        self.setEndFrame(t)
    
    def setCurveShapeFunc(self,c):
        r"""
            カーブシェイプタイムの設定
        """
        try:
            n = self._curveShapeList.get(c)
            if n:
                self.setCurveShape(self._curveShapeList[n])
        except:
            self.setCurveShape(self._curveShapeList['linearCurve'])
        
    def getTimeline(self):
        r"""
            タイムラインを取得する
        """
        return self._timeline

## ----------------------------------------------------------------------------

class HorizonFrame(QtWidgets.QFrame):
    r"""
        横線を入れるクラス
    """
    def __init__(self,bold=1,color='#EEE',parent=None):
        r"""
            横線記述
        """
        super(HorizonFrame,self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(bold)
        self.setColor(color)
    
    def setColor(self,color):
        r"""
            ラインカラーを設定
        """
        pal = self.palette()
        pal.setColor(QtGui.QPalette.WindowText,color)
        self.setPalette(pal)
    
## ----------------------------------------------------------------------------

class SliderField(QtWidgets.QWidget):
    
    r"""
        スライダーフィールド親元コード
    """
    def __init__(self, parent=None):
        r"""
            メインUI
            
            Args:
                parent (any):[edit]
                
            Returns:
                any:None
        """
        super(SliderField, self).__init__(parent)
        
        self.factor = 0.01
        
        HBox = QtWidgets.QHBoxLayout(self)
        self.spinBox = QtWidgets.QDoubleSpinBox()
        self.spinBox.setSingleStep(0.01)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.sliderMoved.connect(self.convToSpinBox)
        self.spinBox.valueChanged.connect(self.convToSlider)
                
        HBox.addWidget(self.spinBox)
        HBox.addWidget(self.slider)
        
        self.setDecimals = self.spinBox.setDecimals
        self.setSingleStep = self.spinBox.setSingleStep
    
    def setRange(self, min, max):
        r"""
            レンジの設定
        """
        self.spinBox.setRange(min, max)
        self.slider.setRange(min//self.factor, max//self.factor)
    
    def setValue(self, value):
        r"""
            数値の設定
        """
        self.spinBox.setValue(value)
        self.convToSlider(value)
    
    def value(self):
        r"""
            スピンボックスの値を返す
        """
        return self.spinBox.value()
    
    def convToSpinBox(self, value):
        r"""
            スピンボックスに値を設定する際に変換する関数
        """
        val = value * self.factor
        self.spinBox.setValue(val)
        
    def convToSlider(self, d):
        r"""
            スライダーに値を設定する際に変換する関数
        """
        self.slider.setValue(d//self.factor)
    
    def setFactor(self, factor):
        r"""
            ファクター（小数値、割る数）の変換値
        """
        self.factor = factor
    
###############################################################################
## - About info widget

class AboutMainUI(ScrolledWidget):
    r"""
        aboutUI内部部分
    """
    def buildUI(self, parent=None):
        r"""
            レイアウトコマンド記述
        """
        reflect  = ''
        reflect += 'QScrollArea{color:#FFF;background-color:#444;}'
        reflect += 'QLabel{color:#FFF;qproperty-alignment:AlignCenter;}'
        _style   = 'border:1px solid #BBB;background-color:%s;'%(ss.MAINUIBGC_C)
        for vh in ('vertical','horizontal'):
            QSB  = 'QScrollBar'
            reflect += ('%s:%s{%s;}'%(QSB,vh,_style))
            reflect += ('%s::sub-line:%s{%s}'%(QSB,vh,_style))
            reflect += ('%s::add-line:%s{%s}'%(QSB,vh,_style))
        self.setStyleSheet(reflect)
        self.title = QtWidgets.QLabel('TITLE')
        self.title.setStyleSheet(
            'QLabel{font-size:20px;font-family:Cambria;background-color:#000;}')
        self.author  = QtWidgets.QLabel('AUTHOR')
        self.version = QtWidgets.QLabel('VERSION')
        self.release = QtWidgets.QLabel('RELEASE')
        self.update  = QtWidgets.QLabel('UPDATE')
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setSpacing(7)
        layout.addWidget(self.title)
        layout.addWidget(self.author)
        layout.addWidget(self.version)
        layout.addWidget(self.release)
        layout.addWidget(self.update)

## ----------------------------------------------------------------------------

class AboutUI(EventBaseWidget):
    r"""
        aboutUI
    """
    def __init__(self,parent=None):
        r"""
            メイン部分
        """
        super(AboutUI,self).__init__(parent)
        
        self.debugFlag = False
        
        # windowの枠を削除
        self.setWindowFlags(_setWindowFlagsDict['tophint=True'])
        # 透明化
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # aboutにも使用↓テンプレ用
        self.title   = self.__class__.__name__
        self.version = '2.0a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/03/19'
        self.update  = '2018/07/13'
        
        self.setWindowTitle(self.title)
        self._w,self._h = 300,150
        self.resize(self._w,self._h)
        
        self.main = AboutMainUI(self)
        
        uiName = 'ms%s'%(self.title)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}'%(uiName,ss.MAINUIBGC))
        
        self.closeAction = WidgetEventAction()
        self.closeAction.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.main)
    
    def mouseDoubleClickEvent(self,event):
        r"""
            ダブルクリックのイベント
        """
        self.closeAction.setCloseTimeElapsed()
    
    def setGeometryPosition(self,x,y):
        r"""
            gui位置の設定
        """
        self.move(x-(self._w//2),y-(self._h//2))

###############################################################################

class BusyBar(EventBaseWidget):
    r"""
        ビジー状態のウィジェットバーを表示するクラス
    """
    def __init__(self,iconName='bar-1',parent=None):
        r"""
            初期設定
        """
        super(BusyBar,self).__init__(parent)
        
        if not iconFlag:
            raise RuntimeError('+ msAppIconがimportされていません。')
        
        iconType = iconName
        offset   = 20
        self.debugFlag = False
        self.setWindowFlags(_setWindowFlagsDict['tophint=True'])
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.title = self.__class__.__name__
        self.setWindowTitle(self.title)
        self.wincolor = [64,64,64,192]
        w,h = getImageSize(msAppIcons.filePath(iconType))
        self.resize(w+offset,h+offset)
        
        uiName = 'ms{}'.format(self.title)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}'%(uiName,ss.MAINUIBGC))
        
        self.we = WidgetEventAction()
        self.we.setTitle('Busy...')
        self.we.setWidget()
        self.we.setSelf(self)
        self.we.t.setStyleSheet('QLabel{color:#FFF;font-family:GEORGIA;}')
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.we.getWidget())
        self.layout.addWidget(
            msAppIcons.moveIconPath(iconType),alignment=QtCore.Qt.AlignCenter)

    ## ------------------------------------------------------------------------
    ## event
    
    def mouseDoubleClickEvent(self,event):
        r"""
            ダブルクリックのイベント
        """
        self.we.setCloseTimeElapsed()
    
    ## ------------------------------------------------------------------------
    ## func
        
    def getIconName(self):
        r"""
            使用可能なgifアイコンネームをリターン
        """
        return msAppIcons.getProgressIconName()
    
## ----------------------------------------------------------------------------
    
class ProgressBar(EventBaseWidget):
    r"""
        プログレスバーウィジェット
    """
    def __init__(self,parent=None):
        r"""
            メインレイアウト
        """
        super(ProgressBar,self).__init__(parent)
        
        self.debugFlag = False
        self.setWindowFlags(QtCore.Qt.Window|QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.title  = self.__class__.__name__
        self.setWindowTitle(self.title)
        self.resize(300,40)
        self.wincolor = [0,16,32,192]
        
        uiName = 'ms{}'.format(self.title)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}'%(uiName,ss.MAINUIBGC))
        
        titleWidget = WidgetEventAction()
        titleWidget.setTitle(self.title)
        titleWidget.setWidget()
        titleWidget.setSelf(self)
        
        self.__progress = QtWidgets.QProgressBar()
        self.__progress.setFormat('%v / %m')
        self.__progress.setAlignment(QtCore.Qt.AlignBottom)
        self.__progress.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.__log = QtWidgets.QTextEdit()
        self.__log.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.__log.setEnabled(False)
        self.__default_color = QtGui.QColor(200, 200, 200)
        self.__log.setTextColor(self.__default_color)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(titleWidget.getWidget())
        self.layout.addWidget(self.__log)
        self.layout.addWidget(self.__progress)
        
        self.closeAction = WidgetEventAction()
        self.closeAction.setSelf(self)
        
        # self.setCount(100)
        # for i in range(100):
            # self.next()
        # self.finish()
        
    def addMessage(self, message, color=None):
        r"""
            結果表示フィールドにメッセージを追加する。
        """
        self.__log.moveCursor(QtGui.QTextCursor.End)
        if not color:
            color = self.__default_color
        self.__log.setTextColor(color)
        self.__log.insertPlainText(message+'\n')
        print(message)

    def setBusy(self, message):
        r"""
            プログレスバーをビジー状態にする。
        """
        self.__progress.setRange(0, 0)
        self.__log.setText(message + '\n')
        self.__default_color = self.__log.textColor()

    def setCount(self, count):
        r"""
            プログレスバーのカウンタの上限値を設定する。
        """
        self.__progress.setRange(0, count-1)
        self.__progress.setTextVisible(True)

    def next(self, message=None):
        r"""
            プログレスバーの進捗を一つアップする。
        """
        self.__progress.setValue(self.__progress.value() + 1)
        if message:
            self.addMessage('\n'+message)

    def finish(self):
        r"""
            終了を告げる表示に設定する。
        """
        self.__progress.setValue(0)
        self.__progress.setRange(0,1)
        self.__progress.setTextVisible(False)
        self.addMessage('Organizing files were finished.')
    
    ## ------------------------------------------------------------------------
    ## Event
        
    def mousePressEvent(self,event):
        r"""
            マウスのクリックが押された時の動作
        """
        self.mouseType          = self.getMouseType(event)
        self.mc                 = event.pos()
        self.o_posX,self.o_posY = None,None
        self.pressFlag          = True
        if self.mouseType == 2:
            self.closeAction.setCloseTimeElapsed()
            
    def mouseDoubleClickEvent(self,event):
        r"""
            ダブルクリックのイベント
        """
        self.closeAction.setCloseTimeElapsed()

###############################################################################

class TimeEvent(object):
    r"""
        タイムイベントの設定
    """
    def __init__(self,parent=None):
        r"""
            基本設定
        """
        self.__time   = None
        self.__s_time = None
        self.__e_time = None
        self.__round  = 2
    
    def setDecimal(self,rou):
        r"""
            小数点の切り捨て数設定
        """
        self.__round = rou
    
    def getDecimal(self):
        r"""
            切り捨て小数点数のリターン
        """
        return self.__round
    
    def nowTime(self):
        r"""
            今の時間をリターン
        """
        return time.time()
    
    def setTime(self):
        r"""
            時間のセット
        """
        self.__time = self.nowTime()
        
    def getTime(self):
        r"""
            時間のリターン
        """
        return round(self.__time,self.getDecimal())
    
    def setStartTime(self):
        r"""
            スタートタイムのセット
        """
        self.__s_time = round(self.nowTime(),self.getDecimal())
        
    def getStartTime(self):
        r"""
            スタートタイムのリターン
        """
        return self.__s_time
        
    def printStartTime(self):
        r"""
            スタートタイムのプリント
        """
        print(self.__s_time)
    
    def setEndTime(self):
        r"""
            エンドタイムのセット
        """
        self.__e_time = (
            round((self.nowTime()-self.__s_time),self.getDecimal())
                if self.__s_time else None
        )
    
    def getEndTime(self):
        r"""
            エンドタイムのリターン
        """
        return self.__e_time
    
    def printEndTime(self):
        r"""
            エンドタイムのプリント
        """
        print(self.__e_time)
    
    def flowProcessStartTime(self):
        r"""
            スタートタイムの流れ処理を実行
        """
        self.setStartTime()
        return self.getStartTime()
        
    def flowProcessEndTime(self):
        r"""
            エンドタイムの流れ処理を実行
        """
        self.setEndTime()
        return self.getEndTime()

## ----------------------------------------------------------------------------

class SpecifiedKeyLimitJudgment(object):
    r"""
        決められた秒数内で指定されたリストのキー情報を取得し
        判定を返すメソッドを集約した専用クラス
    """
    def __init__(self,conditionKeyList=[],limitKeyTime=1.0):
        r"""
        """
        self.resetSaveKey()
        self.readdConditionKeyList(conditionKeyList,True)
        self.reLimitKeyTime(limitKeyTime)
        
    def getTime(self):
        r"""
            現在時間を取得
        """
        return time.time()
    
    def resetSaveKey(self):
        r"""
            保存用の変数をリセットするメソッド
        """
        self.__inputKeyInfo  = []
        self.__startTime     = 0.0
    
    def addSaveKey(self,key):
        r"""
            押下されたキー情報を保存リストに追加
        """
        self.__inputKeyInfo.append(key)
    
    def getSaveKey(self):
        r"""
            保存されている入力キーリストを取得
        """
        return self.__inputKeyInfo
    
    def setStartTime(self,starttime=None):
        r"""
            最初にキーが押された時間を記録
            スタートタイムが指定されていなければ現在の時間を設定
        """
        self.__startTime = starttime if starttime else self.getTime()
        
    def getStartTime(self):
        r"""
            最初にキーが押された時間を取得
        """
        return self.__startTime
    
    def readdConditionKeyList(self,key,new=False):
        r"""
            条件キーリスト追加or新規に指定する
        """
        if new:
            self.__conditionKeyList = key
        else:
            self.__conditionKeyList.append(key)
    
    def getConditionKeyList(self):
        r"""
            条件キーリストを取得
        """
        return self.__conditionKeyList
    
    def reLimitKeyTime(self,limittime=1.0):
        r"""
            条件キーリスト追加or新規に指定する
        """
        self.__limitKeyTime = limittime
        
    def getLimitKeyTime(self):
        r"""
            条件キーリスト追加or新規に指定する
        """
        return self.__limitKeyTime
    
    def judgmentSaveKey(self):
        r"""
            保存されたキー、指定されたキーの条件比較
        """
        return (True
            if self.getSaveKey() == self.getConditionKeyList() else False)
        
    def judgmentLimitTime(self):
        r"""
            キー押下時間が指定された秒数以内で押されているか判定
        """
        return (True
            if(self.getTime()-self.getStartTime() <= self.getLimitKeyTime())
            else False)
    
## ----------------------------------------------------------------------------

class VariableManagement(object):
    r"""
        ウィジェット作成された情報をまとめ管理/運用するクラス
    """
    def __init__(self):
        r"""
        """
        pass
    
    def getVariableAllList(self):
        r"""
            クラス内に設定されている変数の一覧を取得
        """
        return self.__dict__
    
    def setVariable(self,valname,param):
        r"""
            setattrを使用しウィジェット方法を変数に格納する
        """
        flag = param
        try:
            setattr(self,valname,param)
        except:
            flag = None
        return flag
    
    def getVariable(self,valname,type=False):
        r"""
            getattrを使用しウィジェット情報を取得する
            取得に失敗した（設定されたデータが無い）場合はNoneを返す
        """
        try:
            param = getattr(self,valname)
            return ([param,type(param)] if type else param)
        except:
            return None

## ----------------------------------------------------------------------------

class PathStoreList(sgfunc.PathClass):
    r"""
        msAppTools系ファイルの根幹ファイルパスへのアクセスメソッドを
        集約したまとめクラス
    """
    def __init__(self,uiname='',parent=None):
        r"""
            初期設定
        """
        super(PathStoreList,self).__init__()
        
        self._path = ''
        self._dict = {}
        self._buflag = False
        
        self.setBaseUiName(uiname)
        
        self.suffixPrefName = '.{}.json'
        self.estimationBase = '%s{}'%(MSINFO.getEstimationBaseJsonName())
        
        self.estimationName = self.getEstimationName()
        self.windowPrefFile = 'window{}'.format(
            self.getSuffixName('pref'))
            
        self.msAppToolsPath = self.toBasePath(
            os.path.join(self.getRoamingPath(),msAppToolsName))
    
    ## ----------------------------------------------------
    ## base name setting
    
    def setBaseUiName(self,uiname):
        r"""
            ベースUI名を記録
        """
        self.__uiname = uiname
        
    def getBaseUiName(self):
        r"""
            ベースUI名を取得
        """
        # if not self.__uiname:
            # raise RuntimeError(u'!! Not specified <<__uiname>> !!')
        return self.__uiname if self.__uiname else 'master'
    
    def getSuffixName(self,suf=''):
        r"""
            ベースsuffix変数に指定文字を付与して取得
        """
        return self.suffixPrefName.format(suf)
    
    def getPrefJsonName(self):
        r"""
            ui名を指定してuiname.pref.jsonをリターン
        """
        return ('{}{}'.format(self.getBaseUiName(),self.getSuffixName('pref')))
    
    ## ----------------------------------------------------
    ## estimation setting
    
    def getEstimationName(self,uiname=''):
        r"""
            ベースestimation名を取得
        """
        return self.estimationBase.format(
            self.getSuffixName(uiname if uiname else self.getBaseUiName()))
    
    def getEstimationMasterPath(self):
        r"""
            msAppTools直下のマスターestimationパスを取得
        """
        return ('/'.join([
            self.getMasterPath(),self.getEstimationName('master')]))
    
    def getEstimationEachuiPath(self,uiname=''):
        r"""
            ui名を指定してestimation.XXXX.jsonのフルパスを取得
        """
        return self.toBasePath(os.path.join(
            self.getMasterPath(),self.getBaseUiName(),
            self.getEstimationName(self.getBaseUiName())))
    
    def getSaveEachUiPrefPath(self,uiname=''):
        r"""
            ui名を指定してXXXX.pref.jsonのフルパスを取得
        """
        return self.toBasePath(os.path.join(self.getMasterPath(),
            self.getBaseUiName(),self.getPrefJsonName()))
    
    ## ----------------------------------------------------
    ## path setting
    
    def getMasterPath(self):
        r"""
            msAppToolsまでのベースパスを取得
        """
        return self.msAppToolsPath
    
    def windowPrefPath(self):
        r"""
            window設定のprefファイルのパスリターン
        """
        return self.toBasePath(os.path.join(
            self.getRoamingPath(),msAppToolsName,self.windowPrefFile))
    
    ## ----------------------------------------------------
    ## other setting
    
    def setPath(self,p):
        r"""
            呼び出しjsonパスの設定
        """
        self._path = p
    
    def getPath(self):
        r"""
            呼び出しパスの取得
        """
        return self._path
        
    def setDict(self,d):
        r"""
            辞書データのセット
        """
        self._dict = d
        
    def getDict(self):
        r"""
            辞書データの取得
        """
        return self._dict
    
    def setBackup(self,value=False):
        r"""
        """
        self._buflag = value
        
    def getBackup(self):
        r"""
        """
        return self._buflag
        
    def getJsonFile(self):
        r"""
            jsonデータの情報をリターン
        """
        p = self.getPath()
        self.checkTempJsonFile(p)
        f = open(p,'r')
        d = json.load(f)
        f.close()
        return d
    
    ## ----------------------------------------------------
    ## action func
    
    def setJsonFile(self):
        r"""
            辞書データをjsonにセット
        """
        def _backup(path):
            r"""
            """
            f = open(path,'w')
            json.dump(self.getDict(),f,
                indent=4,sort_keys=True,ensure_ascii=False)
            f.close()
            
        if not self._path or not self._dict:
            return
        
        # BU
        if self.getBackup():
            _backup('{}.bu'.format(self.getPath()))
        
        # default
        _backup(self.getPath())
    
    def createMsAppToolsDir(self):
        r"""
            msAppToolsのディレクトリ作成
        """
        if not os.path.isdir(self.msAppToolsPath):
            os.mkdir(self.msAppToolsPath)
            print('+ Create Roaming msAppTools dir.')
    
    def checkTempJsonFile(self,path):
        r"""
            指定されたjsonファイルパスがなければ作成する
        """
        addinfo  = {'DEFAULT':[]}
        jsonfile = os.path.basename(path)
        
        if not os.path.isfile(path) and jsonfile.endswith('.json'):
            # estimationKeyInfo.XXX.jsonの場合_ESTIMATIONの空辞書情報を追加
            if jsonfile.startswith(MSINFO.getEstimationBaseJsonName()):
                addinfo.update({_ESTIMATION:{}})
                print(u'+ Add info <estimation>.')
            f    = open(path,'w')
            dict = addinfo
            json.dump(dict,f,indent=4,sort_keys=True)
            f.close()
            print(u'>>> Create json file / {}'.format(path))
    
    def checkPathFile(self):
        r"""
            対象ファイルの確認。無ければデフォルトデータを作成
        """
        path = self.getPath()

        # ディレクトリ確認
        dirnamedir = os.path.dirname(path)
        if not os.path.isdir(dirnamedir):
            os.makedirs(dirnamedir)
            print('>>> Create dirs / {}'.format(dirnamedir))
        
        # jsonファイル確認
        self.checkTempJsonFile(path)
    
    def setSeriesPath(self,filepath):
        r"""
            パスセットの一連の流れをまとめて実行する
        """
        self.setPath(filepath)
        self.createMsAppToolsDir()
        self.checkPathFile()
    
## ----------------------------------------------------------------------------

class EventPackageChildren(object):
    r"""
        親(ui/func)からのeventFuncPackagingを操作するクラス
    """
    def __init__(self):
        r"""
        """
        self._eventPackage = None
        
    def setEventPackageMethod(self,packaging):
        r"""
            親(ui/func)からのeventFuncPackagingを格納する関数
        """
        self._eventPackage = packaging
        
    def getEventPackageMethod(self):
        r"""
            親(ui/func)からのeventFuncPackagingを取得する関数
        """
        return self._eventPackage

## ----------------------------------------------------------------------------

class OptionInfoMasterdataClass(object):
    r"""
        子クラス用/オプションウィジェット用データ総括クラス
    """
    def __init__(self,parentWidget=None,masterObject=None):
        r"""
            変数の初期設定
        """
        self.widget = parentWidget
        self.object = masterObject
        self.data   = None
        
        self.connectionObject()
        self.setDict()
        
    def __repr__(self):
        r"""
            クラス情報の取得
        """
        return (u'+ Class <<{}>>'.format(self.__class__.__name__))
    
    def createWidgetLayout(self):
        r"""
            ウィジェット作成
        """
        _d = self.getDict()
        if not _d:
            print(u'+ No setting dict data.')
            return
        _wg = self.getWidget()
        if not _wg:
            print(u'+ Widget not set.')
            return
        
        _mw = [4,4,4,4]
        _wg.setContentsMargins(*_mw)
        
        layout = QtWidgets.QVBoxLayout(_wg)
        
        title = QtWidgets.QLabel('+ Option widget')
        title.setStyleSheet(ss.LABEL_STYLE)
        layout.addWidget(title)
        
        frame = QtWidgets.QFrame()
        fName = 'bn_{}'.format(returnRandomString(length=12))
        frame.setObjectName(fName)
        frame.setStyleSheet('#%s{border:1px solid #FFF;}'%(fName))
        layout.addWidget(frame)
        
        borderLayout = QtWidgets.QVBoxLayout(frame)
        borderLayout.setContentsMargins(*_mw)
        
        _wg.setWidgetDict(_d)
        borderLayout.addWidget(_wg.createWidgetParts())
        borderLayout.addStretch()
        
        exeButton = QtWidgets.QPushButton('Update refrect')
        exeButton.clicked.connect(lambda:self.executeButtonCommand())
        layout.addWidget(exeButton)
        
    def setDict(self):
        r"""
            オーバーライド用オプションウィジェットベースデータ。
            ここにウィジェット作成用の元となる辞書データを記述していく。
        """
        self.data = {
            '099,tempLine':{
                'widget':{
                    'name':'QLineEdit', # QtWidgets.XXX の XXXに相当する名称を指定
                },
                'attribute':{
                    'setValue':'Default',
                },
                'attribute1':{
                    'setToolTip':'(TEMP)QLineEdit',
                },
            },
            '050,tempSpinBox':{
                'widget':{
                    'name':'QSpinBox',
                },
                'attribute':{
                    'setValue':4,
                    'setRange':(1,20), # range設定のようにint/str形式の物を
                                       # カンマ(,)綴りで指定する場合はtuple形式
                },
                'attribute1':{
                    'setToolTip':'(TEMP)QSpinBox',
                },
            },
            '020,extension':{
                'widget':{
                    'name':'QComboBox',
                },
                'attribute':{
                    'addItems':['jpg','png'], # 配列で設定するものはlist形式
                },
                'attribute1':{
                    'setCurrentIndex':1,
                    'setToolTip':'bbbb',
                },
            },
        }
        
    def getDict(self):
        r"""
            辞書データ取得
        """
        return self.data
        
    def setWidget(self,w):
        r"""
            経由されてきたWidgetEventActionを設定するクッション関数
        """
        self.widget = w
        
    def getWidget(self):
        r"""
            格納されたWidgetEventActionの取得関数
        """
        return self.widget
    
    def connectionObject(self):
        r"""
            OptionWidgetにguiオブジェクトを引き渡す関数
        """
        self.widget.setGuiObject(self.object)
    
    def executeButtonCommand(self):
        r"""
            Executeボタン実行関数
        """
        print(2211,self.object)
        # print('hasattr:setAfterUpdateDict',hasattr(self.widget,'setAfterUpdateDict'))
        # print('hasattr:getAfterUpdateDict',hasattr(self.widget,'getAfterUpdateDict'))
        
        # ウィジェットの設定されているデータを取得し子クラスに設定し外部保存する
        saveDictInfo = {}
        nowDict = self.getDict()
        for _d in nowDict:
            _wn  = nowDict[_d]['widget']['name']
            _wvt = _getWidgetReturnTypeValue(_wn)
            # exec('_r = nowDict[_d]["widgetObject"].{}()'.format(_wvt))
            _val = eval('nowDict[_d]["widgetObject"].{}()'.format(_wvt))
            saveDictInfo.update({_d:_val})
        
        if hasattr(self.object,'reflectWidgetDataToVariable'):
            self.object.reflectWidgetDataToVariable(saveDictInfo)
    
    def execute(self):
        r"""
            ウィジェットの作成等の実行
        """
        print('>> Start function <{}>'.format(self.__class__.__name__))
        self.createWidgetLayout()

## ----------------------------------------------------------------------------

class ConstructionUiFunction(object):
    r"""
        共通のクラスUIを作成しオブジェクト変数をリターンするクラス
    """
    def __init__(self):
        r"""
            __init__
        """
        self.__schemaList   = None
        self.__returnList   = []
        self.__GROUPLIST    = []
        self.__BUTTONLIST   = []
        
        self.__menu         = None
        self.__popMenuClass = []
        self.__modifierFlag = None
        
    def setSchema(self,schema):
        r"""
            スキーマーをセット
        """
        self.__schemaList = schema
    
    def getSchema(self):
        r"""
            セットされたスキーマーを返す
        """
        return self.__schemaList
    
    def setMenu(self,menu):
        r"""
            メニューアイテムのセット
        """
        self.__menu = menu
    
    def getMenu(self):
        r"""
            メニューアイテムのリターン
        """
        return self.__menu
    
    def clearList(self):
        r"""
            セットされるスキーマー変数を初期化
        """
        self.__returnList  = []
        self.__GROUPLIST   = []
        self.__BUTTONLIST  = []
    
    def setReturnList(self,group,button,uiParts=None):
        r"""
            リターンされるパーツをセット
        """
        self.__returnList = [group,button]
        if uiParts:
            self.__returnList.append(uiParts)
        
    def getReturnList(self):
        r"""
            セットされたパーツをリターン
        """
        return self.__returnList
        
    def setModifierFlag(self,modifier=[]):
        r"""
            モディファイアーリストの該当条件の検索とセット
        """
        ctrl,shift,alf = False,False,False
        for m in modifier:
            mr = m.lower()
            ctrl  = True if mr == 'ctrl'  else False
            shift = True if mr == 'shift' else False
            alt   = True if mr == 'alt'   else False
        if ctrl:
            self.__modifierFlag = (QtCore.Qt.ControlModifier)
        elif shift:
            self.__modifierFlag = (QtCore.Qt.ShiftModifier)
        elif alt:
            self.__modifierFlag = (QtCore.Qt.AltModifier)
        elif ctrl and shift:
            self.__modifierFlag = (QtCore.Qt.ControlModifier|
                                   QtCore.Qt.ShiftModifier)
        elif ctrl and alt:
            self.__modifierFlag = (QtCore.Qt.ControlModifier|
                                   QtCore.Qt.AltModifier)
        elif shift and alt:
            self.__modifierFlag = (QtCore.Qt.ShiftModifier|
                                   QtCore.Qt.AltModifier)
        elif ctrl and shift and alt:
            self.__modifierFlag = (QtCore.Qt.ControlModifier|
                                   QtCore.Qt.ShiftModifier  |
                                   QtCore.Qt.AltModifier)
        else:
            self.__modifierFlag = []
    
    def getModifierFlag(self):
        r"""
            enter description
        """
        return self.__modifierFlag
        
    ## ------------------------------------------------------------------------
    
    def basicUI(self):
        r"""
            ベーシックなUIの作成関数
        """
        self.clearList()
        for i,u in enumerate(self.__schemaList):
            vl = QtWidgets.QVBoxLayout()
            vl.setContentsMargins(8,4,8,4)
            for i2,u2 in enumerate(u):
                if i2 == 0:
                    group = QtWidgets.QGroupBox(u2)
                    group.setStyleSheet('QGroupBox{%s}'%(ss.GROUPFONT))
                    group.setLayout(vl)
                    self.__GROUPLIST.append(group)
                else:
                    hl = QtWidgets.QHBoxLayout()
                    __item = []
                    for i3,u3 in enumerate(u2):
                        if not len(u2) == 1 and i3 == 0:
                            hl.addStretch(1)
                        if u3[0] == 'label':
                            parts = QtWidgets.QLabel(u3[1])
                        elif u3[0] == 'lineEdit':
                            parts = QtWidgets.QLineEdit(u3[1])
                            __item.append(parts)
                        elif u3[0] == 'spinBox':
                            parts = QtWidgets.QSpinBox()
                            parts.setRange(u3[1][0],u3[1][1])
                            parts.setValue(u3[2])
                            parts.setSingleStep(u3[3])
                            __item.append(parts)
                        elif u3[0] == 'combobox':
                            parts = QtWidgets.QComboBox()
                            parts.addItems(u3[1])
                            __item.append(parts)
                        elif u3[0] == 'radioButton':
                            parts = QtWidgets.QRadioButton(u3[1])
                            parts.setChecked(u3[2])
                            __item.append(parts)
                        elif u3[0] == 'button':
                            parts = QtWidgets.QPushButton(u3[1])
                            parts.address = u3[2]
                            parts.item = __item
                            parts.setStyleSheet(u3[3])
                            self.__BUTTONLIST.append(parts)
                        elif u3[0] == 'border':
                            parts = HorizonFrame()
                        parts.setToolTip(u3[-1])
                        hl.addWidget(parts,u3[-2])
                    vl.addLayout(hl)
        self.setReturnList(self.__GROUPLIST,self.__BUTTONLIST)
    
    def groupDictUI(self):
        r"""
            ベーシックなUIの作成関数（辞書版）
        """
        self.clearList()
        __POPMENUDICT = {}
        for i,u in enumerate(self.__schemaList):
            vl = QtWidgets.QVBoxLayout()
            vl.setContentsMargins(8,4,8,4)
            for i2,u2 in enumerate(u):
                hl = QtWidgets.QHBoxLayout()
                __item = []
                for i3,u3 in enumerate(u2):
                    if not i2 == 0 and u3['setStretch']:
                        hl.addStretch(1)
                    if i2 == 0:
                        group = QtWidgets.QGroupBox(u3['groupWidget'])
                        group.setStyleSheet('QGroupBox{%s}'%(ss.GROUPFONT))
                        group.setLayout(vl)
                        self.__GROUPLIST.append(group)
                    else:
                        parts = None
                        wd    = u3['widget']
                        if wd == 'label':
                            parts = QtWidgets.QLabel(u3['labelName'])
                        elif wd == 'lineEdit':
                            parts = QtWidgets.QLineEdit(u3['lineName'])
                            __item.append(parts)
                        elif wd == 'comboBox':
                            parts = QtWidgets.QComboBox()
                            parts.addItems(u3['addItem'])
                            __item.append(parts)
                        elif wd == 'spinBox':
                            parts = QtWidgets.QSpinBox()
                            parts.setRange(u3['range'][0],u3['range'][1])
                            parts.setValue(u3['value'])
                            parts.setSingleStep(u3['step'])
                            __item.append(parts)
                        elif wd == 'doubleSpinBox':
                            parts = QtWidgets.QSpinBox()
                            parts.setRange(u3['range'][0],u3['range'][1])
                            parts.setValue(u3['value'])
                            parts.setSingleStep(u3['step'])
                            __item.append(parts)
                        elif wd == 'radioButton':
                            parts = QtWidgets.QRadioButton(u3['radioName'])
                            parts.setChecked(u3['isChecked'])
                            __item.append(parts)
                        elif wd == 'button':
                            parts = QtWidgets.QPushButton(u3['buttonName'])
                            parts.setStyleSheet(u3['styleSheet'])
                            parts.item = __item
                            self.__BUTTONLIST.append(parts)
                        elif wd == 'border':
                            parts = HorizonFrame()
                        if u3['popFlag']:
                            __POPMENUDICT[u3['address']] = [parts,u3['popItem']]
                        parts.address = u3['address']
                        parts.setToolTip(u3['toolTip'])
                        hl.addWidget(parts,u3['widgetLength'])
                vl.addLayout(hl)
        self.setReturnList(self.__GROUPLIST,self.__BUTTONLIST,__POPMENUDICT)
        
        # popMenuの表示設定
        [self.popMenuImAction(__POPMENUDICT[name]) for name in __POPMENUDICT]
        
    def menuUI(self):
        r"""
            メニューUIの作成関数
        """
        for u in self.__schemaList:
            menuList = []
            menuList.append([self.__menu,99])
            parentFlag = True
            for u2 in u:
                for x in range(5,-1,-1):
                    if not u2[0] == x:
                        continue
                    if u2[0] == 0:
                        mm = menuList[-1][0].addAction(u2[1])
                        mm.address = u2[1]
                        mm.triggered.connect(u2[2])
                    else:
                        for mi,ml in enumerate(menuList):
                            if ml[1] == 99 and parentFlag:
                                mb = menuList[-1][0].addMenu(u2[1].center(8,' '))
                                menuList.append([mb,u2[0],u2[1]])
                                parentFlag = False
                            elif ml[1] == (u2[0]+1):
                                mb = ml[0].addMenu(u2[1])
                                menuList.append([mb,u2[0],u2[1]])
    
    def popMenuImAction(self,uiparts):
        r"""
            個々にpopMenuを表示させるための中間関数
        """
        uiparts[0].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        uiparts[0].customContextMenuRequested.connect(
            lambda: self.exeLaunchMenu(uiparts[1])
        )

    def exeLaunchMenu(self,mParts):
        r"""
            メニュー表示関数
        """
        for m in mParts:
            self.setModifierFlag(m['modifier'])
            keyModifier = self.getModifierFlag()
            if (isinstance(keyModifier, list) or
                QtWidgets.QApplication.keyboardModifiers() == keyModifier
            ):
                menu = QtWidgets.QMenu()
                m = menu.addAction(m['menuName'],m['funcName'])
                menu.exec_(QtGui.QCursor.pos())

###############################################################################
## END