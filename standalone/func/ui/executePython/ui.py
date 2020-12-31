#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    指定したパスのpythonファイルを実行するGUI
"""
###############################################################################
## base lib

import os
import re
import sys
import json
import traceback
import subprocess

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from . import func as fc
from ... import settings as st
from msAppTools.settingFiles import systemGeneral as sg

QtWidgets,QtCore,QtGui = sg.QtWidgets,sg.QtCore,sg.QtGui
_SPSL               = fc._SPSL
_defaultText        = fc._defaultText
_dragText           = fc._dragText
_subprocessValue    = fc._subprocessValue
_subprocessTextList = fc._subprocessTextList
_DROPPATH           = fc._DROPPATH

###############################################################################

class DragTextLabel(QtWidgets.QWidget):
    r"""
        ドラッグした際のテキスト変更がされるラベルウィジェット
    """
    def __init__(self,parent=None):
        r"""
        """
        super(DragTextLabel,self).__init__(parent)
        
        self.__self = parent
        
        self.setAcceptDrops(True)
        self._fontSize        = 48
        self._subprocessText  = _subprocessTextList[0]
        self.__dropPathData   = ''
        self.__processNowFlag = False
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setContentsMargins(0,0,0,0)
        self._TL = QtWidgets.QLabel('')
        self._TL.setIndent(2)
        self._TL.setMargin(2)
        self._TL.setText(_defaultText)
        self._TL.setContentsMargins(2,2,2,2)
        self._TL.setAlignment(QtCore.Qt.AlignJustify) #QtCore.Qt.AlignCenter
        layout.addWidget(self._TL)
        
        self.paintEventPreSetting()
    
    ## ------------------------------------------------------------------------
    ## setting
    
    def paintEventPreSetting(self):
        r"""
            paintEvent関係のプリセッティング
        """
        self._animOffset = 0
        
        self._colDict = {
            'default' : [QtGui.QColor(12,12,20),QtGui.QColor(55,55,120)],
            'drag'    : [QtGui.QColor(20,12,12),QtGui.QColor(120,55,55)],
            'drop'    : [QtGui.QColor(12,20,12),QtGui.QColor(55,120,55)],
            'noFile'  : [QtGui.QColor(12,20,12),QtGui.QColor(120,55,120)],
        }
        self._lineAlpha     = 255
        self._bgStartColor  = self._colDict['default'][0]
        self._bgEndColor    = self._colDict['default'][1]
        
        self._gradient      = QtGui.QLinearGradient()
        self.setBgColor('default')
        
        self._startTimeline = sg.TimeLine(100)
        self._startTimeline.valueChanged.connect(self.dragAnimation)
        
        self._endTimeline   = sg.TimeLine(160)
        self._endTimeline.valueChanged.connect(self.leaveAnimation)
        
        self._bgTimeline    = sg.TimeLine(1,1)
        self._bgTimeline.stateChanged.connect(self.dragState)
        
        self._textAlpha     = 0
        self._processAlpha  = sg.TimeLine(400,10)
        self._processAlpha.valueChanged.connect(self.processAlpha)
    
    def setBgColor(self,type):
        r"""
            BGカラー設定
        """
        self._bgStartColor = self._colDict[type][0]
        self._bgEndColor   = self._colDict[type][1]
        self._gradient.setColorAt(0.0,self._bgStartColor)
        self._gradient.setColorAt(1.0,self._bgEndColor)
    
    def frameLineSetting(self,value):
        r"""
            フレームラインのアルファ設定
        """
        try:
            self._lineAlpha = value
        except:
            self._lineAlpha = 255
    
    def setSubprocessText(self,text,size=48):
        r"""
            toggle変更時のホップアップ表示テキスト
        """
        self._subprocessText = text
        self.setFontSize(size)
        self.update()
    
    def setFontSize(self,size=48):
        r"""
            フォントサイズ設定
        """
        self._fontSize = size
        self.update()
    
    ## ------------------------------------------------------------------------
    ## func
    
    def clear(self):
        r"""
            設定情報のクリア(親実行コマンド)
        """
        self._TL.setText(_defaultText)
        self._TL.setAlignment(QtCore.Qt.AlignJustify)
        self.clearDropPathData()
        self.frameLineSetting(255)
        self.setBgColor('default')
        self.update()
        
    def setProcessNowFlag(self,v):
        r"""
            プロセス状態フラグの設定
        """
        self.__processNowFlag = v
        
    def getProcessNowFlag(self):
        r"""
            プロセス状態フラグの取得
        """
        return self.__processNowFlag
    
    def setDropPathData(self,p):
        r"""
            ドロップパスのグローバルセット
        """
        self.__dropPathData = p
        
    def getDropPathData(self):
        r"""
            ドロップパスの取得
        """
        return self.__dropPathData
    
    def getDropPathDataBool(self):
        r"""
            ドロップパスのpy情報を取得しboolで返す
        """
        try:
            return True if re.search('[.]py$',self.getDropPathData()) else False
        except:
            return False
    
    def clearDropPathData(self):
        r"""
            ドロップパス初期化
        """
        self.__dropPathData = ''
    
    def startDragTimeLine(self):
        r"""
            ドラッグした際のタイムラインスタート開始イベント
        """
        self._startTimeline.start()
    
    def endDragTimeLine(self):
        r"""
            ドラッグして離れた際のタイムラインエンド開始イベント
        """
        self._endTimeline.start()
    
    def bgDragTimeLine(self):
        r"""
            ドラッグした際のタイムラインBGカラースタート始イベント
        """
        self._bgTimeline.start()
    
    def processAlphaTimeLine(self):
        r"""
            subprocess変更時のアニメーション開始イベント
        """
        self._processAlpha.start()
    
    def dragAnimation(self,value):
        r"""
            ドラッグ時アニメーションの実行メソッド
        """
        self._animOffset = (120*value)
        
        # dropデータが有りかつアルファラインが0じゃない(描画されている)場合実行
        if not self.getDropPathDataBool() and not self._lineAlpha==0.0:
            self.frameLineSetting((255*(1.0-value)))
        self.update()
    
    def dragState(self,state):
        r"""
            ドラック時のシングル実行メソッド
        """
        self.setBgColor('drag')
        self.update()
        # タイムライン秒数以内にアイテムがアイテムがドロップした場合
        # dropEventの描画処理の後にタイムラインの描画処理が走り結果背景色が
        # drag色(赤)になるかつ背景色を変える処理は一度でいいためストップさせる。
        self._bgTimeline.stop()
    
    def leaveAnimation(self,value):
        r"""
            カーソルリーブ時アニメーションの実行メソッド
        """
        if not self.getDropPathDataBool():
            self.frameLineSetting(255*value)
            self.setBgColor('default')
        else:
            self.setBgColor('drop')
        self.update()
    
    def processAlpha(self,value):
        r"""
            subprocess変更時の確認ホップアップテキストアルファ設定
        """
        self.setProcessNowFlag(True if not value==1.0 else False)
        self._textAlpha = int((255*(1.0-(value*value*value))))
        self.update()
    
    def updateText(self,path):
        r"""
            テキストのアップデート用関数
        """
        def fileAnalysis(f):
            r"""
                ファイルデータの解析
            """
            if not os.path.isfile(f):
                return fc.getStyleWord('!! Not file !!',4)
            p = os.path.dirname(f)
            d = os.path.basename(f)
            if not re.search('[.]py$',d):
                return fc.getStyleWord('!! Not py file !!',4)
            
            data = sg.getLastUpdateTime(f)
            last =  '{} {}'.format(data['ymd'][3],data['hms'][1])
            templateText = ('\n'
                'File name :\n\t{}\n'
                'File path :\n\t{}\n'
                'File size :\n\t{} bytes\n'
                'File line :\n\t{} line\n'
                'Update date :\n\t{}\n'
            ).format(d,p,sg.getFileSize(f),sg.getFileLine(f),last)
            return (templateText)
            
        if not path:
            return False
            
        text = sg.toDecode(fileAnalysis(path))
        res  = re.search('!!',text)
        self._TL.setText(text)
        self._TL.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignJustify|
            (QtCore.Qt.AlignCenter if res else QtCore.Qt.AlignLeft))
        self.setDropPathData(path)
        self.frameLineSetting(255 if res else 0)
        self.setBgColor('noFile' if res else 'drop')
        self.update()
        
        return True
    
    ## ------------------------------------------------------------------------
    ## event
    
    def dragEnterEvent(self,event):
        r"""
            ドラッグのイベント
        """
        mime = event.mimeData()
        event.accept() if mime.hasUrls() else event.ignore()
        
        self.startDragTimeLine()
        self.bgDragTimeLine()
        
    def dragLeaveEvent(self,event):
        r"""
            ドラッグが離れた時のイベント
        """
        self.endDragTimeLine()
    
    def dropEvent(self,event):
        r"""
            ドロップのイベント
        """
        mime = event.mimeData()
        path = mime.urls()
        for p in path:
            self.updateText(p.toLocalFile())
    
    def paintEvent(self,event):
        r"""
            イベント描画イベント
        """
        
        paint  = QtGui.QPainter(self)
        rect   = self.rect()
        center = rect.center()
        
        _frameBorder = 20
        
        self._gradient.setFinalStop(0,rect.height())
        brush = QtGui.QBrush(self._gradient)
        
        paint.setBrush(brush)
        paint.drawRect(rect)
        
        # 点線
        pen = QtGui.QPen(QtGui.QColor(180,180,180,self._lineAlpha),1)
        pen.setStyle(QtCore.Qt.DashLine)
        paint.setPen(pen)
        paint.setBrush(QtCore.Qt.NoBrush)
        
        # 枠の大きさ
        rect.setHeight(rect.height()-(_frameBorder*1.0)-_frameBorder)
        rect.setWidth(rect.width()*0.85)
        rect.moveCenter(center)
        rect.moveTop(_frameBorder)
        paint.drawRoundedRect(rect,4,4)
        
        # subprocess文字表示
        pen = QtGui.QPen(QtGui.QColor(222,222,222,self._textAlpha),1)
        paint.setFont(QtGui.QFont('arial black',self._fontSize))
        paint.setOpacity(1.0)
        paint.setPen(pen)
        
        # 親UIのサイズを元に文字位置を確定する()
        offset = 20
        _r = self.__self.rect()
        # _r.setRect(r.x(),r.y(),r.width()-offset,r.height()-offset)
        _r.setWidth(_r.width()-offset)
        _r.setHeight(_r.height()-offset)
        paint.drawText(_r,QtCore.Qt.AlignCenter,self._subprocessText)
        
###############################################################################
    
class ExecutePython(sg.ScrolledWidget):
    r"""
        zip作成gui
    """
    _layout = None
    
    def __init__(self,parent=None,masterDict=None):
        r"""
            初期設定
        """
        super(ExecutePython,self).__init__(parent)
        
        self.debugFlag = False
        
        self.__processList   = [subprocess.Popen,subprocess.call]
        self.__processToggle = _subprocessValue
        
        self._dict = masterDict
        self.uiSetting()
    
    ## ------------------------------------------------------------------------
    ## common parent event setting
    
    ## ------------------------------------------------------------------------
    ## ui
    
    def buildUI(self,parent=None):
        r"""
            enter description
        """
        self.preSetting()
        self._layout = QtWidgets.QVBoxLayout(parent)
        
    def uiSetting(self):
        r"""
            UI全体セッティング
        """
        self._TL = DragTextLabel(self)
        self._layout.addWidget(self._TL)
        self.setting()
    
    ## ------------------------------------------------------------------------
    ## event
        
    def keyPressEvent(self,event):
        r"""
            キープレスイベント(オーバーライド)
        """
        # 親keyPressEvent(Esc,windowClose等)をオーバーライドしてしてしまうので
        # superしてイベント情報を継承する
        super(ExecutePython,self).keyPressEvent(event)
        
        key   = self.getKeyType(event)
        mask  = self.getKeyMask()
        mask2 = self.getKeyMask2()
        
        # 削除
        if key['press'] in ('Del','Backspace'):
            self.refreshText()
        # 実行
        elif key['mod1']==mask['ctrl'] and key['press'] in ('Enter','Return'):
            self.execute()
        # 実行タイプ変更
        elif key['mod1']==mask['ctrl'] and key['press'] in ('Tab',):
            self.processToggle()
        # 再読込
        elif key['mod1']==mask['ctrl'] and key['press'] in ('R',):
            self.reload()
        # フォルダを開く
        elif key['mod1']==mask['ctrl'] and key['press'] in ('O',):
            self.openDir()
        # フォルダ/ファイルパスをクリップボードへコピー
        elif key['mod1']==mask['ctrl'] and key['press'] in ('C',):
            self.textCopyClipbord()
        # ドロップパス情報保存
        elif key['mod1']==mask2(['ctrl','shift']) and key['press'] in ('S',):
            self.savePath()
        # ドロップパス情報削除
        elif key['mod1']==mask2(['ctrl','shift']) and key['press'] in ('D',):
            self.deletePath()
        # ドロップパス情報整理
        elif key['mod1']==mask2(['ctrl','shift']) and key['press'] in ('A',):
            self.resetPath()
        # ドロップパスアップ
        elif (key['mod1']==mask2(['ctrl','shift']) and
                key['press'] in ('Up','Left')):
            self.changePath(-1)
        # ドロップパスダウン
        elif (key['mod1']==mask2(['ctrl','shift']) and
                key['press'] in ('Down','Right')):
            self.changePath(1)
        
    def mouseDoubleClickEvent(self,event):
        r"""
            ダブルクリックのイベント
        """
        self.execute()
        
    ## ------------------------------------------------------------------------
    ## setting
    
    def preSetting(self):
        r"""
            __init__設定時の動作をbuildUIで先行して行うための関数
        """
        # AppData/Roaming/msAppTools/<FILENAME>までのパスを設定
        _SPSL.setSeriesPath(_SPSL.getSaveEachUiPrefPath())
    
    def setting(self):
        r"""
            初期設定の窓口関数
        """
        self.styleSheetSet()
    
    def styleSheetSet(self):
        r"""
            スタイルシート一括設定
        """
        reflect = 'QLabel{color:#FFF;}'
        self._TL.setStyleSheet(reflect)
    
    ## ------------------------------------------------------------------------
    ## key func
    
    def savePath(self):
        r"""
            ドロップパスデータを外部保存
        """
        _p = sg.toBasePath(self._TL.getDropPathData())
        if not _p:
            print('+ Not drop path data.')
            return
        jsonPath = _SPSL.getPath()
        if not os.path.isfile(jsonPath):
            print('+ Not json path. "{}"'.format(jsonPath))
            return
        
        _d = _SPSL.getJsonFile()
        _saveDict = _d.get(_DROPPATH)
        _saveBuf  = _saveDict[:] if _saveDict else []
        
        if _p in _saveBuf:
            return
        _saveBuf.append(_p)
        _saveBuf.sort()
        _d[_DROPPATH] = _saveBuf
        _SPSL.setDict(_d)
        _SPSL.setBackup(True)
        _SPSL.setJsonFile()
        print(u'+ Save path. "{}"'.format(_p))
        
        if self._TL.getProcessNowFlag():
            return
            
        self._TL.setSubprocessText('Save')
        self._TL.processAlphaTimeLine()
    
    def deletePath(self):
        r"""
            外部ドロップパスデータを削除
        """
        _p = sg.toBasePath(self._TL.getDropPathData())
        if not _p:
            print('+ Not drop path data.')
            return
        jsonPath = _SPSL.getPath()
        if not os.path.isfile(jsonPath):
            print('+ Not json path. {}'.format(jsonPath))
            return
        _d = _SPSL.getJsonFile()
        _saveDict = _d.get(_DROPPATH)
        _saveBuf  = _saveDict[:] if _saveDict else []
        if not _p in _saveDict:
            return
            
        _saveBuf.remove(_p)
        _d[_DROPPATH] = _saveBuf
        _SPSL.setDict(_d)
        _SPSL.setBackup(True)
        _SPSL.setJsonFile()
        print(u'+ Remove path. "{}"'.format(_p))
        
        if self._TL.getProcessNowFlag():
            return            
        self._TL.setSubprocessText('Delete')
        self._TL.processAlphaTimeLine()
    
    def changePath(self,moveValue):
        r"""
            キー移動でのパス変化
        """
        _p = sg.toBasePath(self._TL.getDropPathData())
        jsonPath = _SPSL.getPath()
        if not os.path.isfile(jsonPath):
            print('+ Not json path. {}'.format(jsonPath))
            return
        _d = _SPSL.getJsonFile()
        _saveDict = _d.get(_DROPPATH)
        if not _saveDict:
            return
        _saveBuf  = _saveDict[:] if _saveDict else []
        
        try:
            index = 0 if not _p else (_saveBuf.index(_p)+moveValue)
            index = 0 if index>=len(_saveBuf) else index
            self._TL.updateText(_saveBuf[index])
        except ValueError:
            self._TL.updateText(_saveBuf[0])
    
    def resetPath(self):
        r"""
            保存されたドロップパスの表示とセット
        """
        jsonPath = _SPSL.getPath()
        if not os.path.isfile(jsonPath):
            print('+ Not json path. {}'.format(jsonPath))
            return
        _d = _SPSL.getJsonFile()
        _saveDict = _d.get(_DROPPATH)
        if not _saveDict:
            return
        _saveBuf  = _saveDict[:] if _saveDict else []
        
        for path in _saveBuf:
            if not os.path.isfile(path):
                _saveBuf.remove(path)
                print(u'+ Removed path. "{}"'.format(path))
        
        _d[_DROPPATH] = _saveBuf
        _SPSL.setDict(_d)
        _SPSL.setBackup(True)
        _SPSL.setJsonFile()
        print(u'+ Organize path.')
        
        if self._TL.getProcessNowFlag():
            return            
        self._TL.setSubprocessText('Organize',28)
        self._TL.processAlphaTimeLine()
    
    ## ------------------------------------------------------------------------
    ## func
    
    def textCopyClipbord(self):
        r"""
            今ドロップされているファイルパスをクリップボードへコピー
        """
        _t = self._TL.getDropPathData()
        if _t:
            sg.textCopy(_t)
            print(u'+ Copy to clipboard = "{}"'.format(_t))
        
    def openDir(self):
        r"""
            今ドロップされているフォルダを開く
        """
        _p = self._TL.getDropPathData()
        if _p:
            sg.openExplorer(_p)
    
    def refreshText(self):
        r"""
            テキストリフレッシュ
        """
        self._TL.clear()
    
    def changeToggleValue(self):
        r"""
            toggle(1->0/0->1)値変化
        """
        self.__processToggle = 0 if self.__processToggle else 1
        if self.debugFlag:
            print('+ Process type = ({}) {}'.format(
                self.__processToggle,self.__processList[self.__processToggle]))
        return self.__processToggle
        
    def processToggle(self):
        r"""
            プロセスタイプのtoggle設定
        """
        if self._TL.getProcessNowFlag():
            return
            
        self._TL.setSubprocessText(
            _subprocessTextList[self.changeToggleValue()])
        self._TL.processAlphaTimeLine()
    
    def reload(self):
        r"""
            リロード時の実行関数
        """
        if self._TL.getProcessNowFlag():
            return
            
        # ドロップされているpyデータを再読み込み
        if self._TL.updateText(self._TL.getDropPathData()):
            # paintEventでReloadを表示
            self._TL.setSubprocessText('Reload')
            self._TL.processAlphaTimeLine()

    def execute(self):
        r"""
            実行
        """
        if not self._TL.getDropPathDataBool():
            return
        try:
            _p = self._TL.getDropPathData()
            self.__processList[self.__processToggle]('python {}'.format(_p))
            STI = sg.SystemTrayIcon(6000)
            STI.setTitle('Running.')
            STI.setMsg(os.path.basename(_p))
            STI.setIcon(1)
            STI.showMsg()
        except:    
            traceback.print_exc()

    ## ------------------------------------------------------------------------
    ## common
    
    def setDebugFlag(self,value=True):
        r"""
            デバックフラグのスイッチ(オーバーライド)
        """
        self.debugFlag = value
    
    def getAboutData(self):
        r"""
            about情報の取得
        """
        return fc.getAboutInfo()
    
###############################################################################
## memo
"""
    QtCore.Qt.AlignCenter
    QtCore.Qt.AlignLeft
    QtCore.Qt.AlignRignt
    QtCore.Qt.AlignJustify
    
    QtCore.Qt.AlignHCenter
    QtCore.Qt.AlignVCenter
    QtCore.Qt.AlignTop
    QtCore.Qt.AlignBottom
   
    QtCore.Qt.TextDontClip
    QtCore.Qt.TextSingleLine
    QtCore.Qt.TextExpandTabs
    QtCore.Qt.TextShowMnemonic
    QtCore.Qt.TextWordWrap
    QtCore.Qt.TextIncludeTrailingSpaces
"""
###############################################################################
## END
