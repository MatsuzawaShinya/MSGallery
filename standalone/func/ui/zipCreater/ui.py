#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    指定したフォルダ内にあるすべてのファイルをzip化するGUI
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

from . import func as fc
from ... import settings as st
from msAppTools.settingFiles import systemGeneral as sg

QtWidgets,QtCore,QtGui = sg.QtWidgets,sg.QtCore,sg.QtGui

###############################################################################

class FilterWidget(sg.EventBaseWidget):
    r"""
        フィルターを設定するウィジェット
    """
    _st = {'label':'#FFF','text':'#000','bg':'#FFF'}
    
    def __init__(self,object=None,parent=None):
        r"""
            メインレイアウト
        """
        super(FilterWidget,self).__init__(parent)
        c_pos  = QtGui.QCursor().pos()
        w,h,offset = 256,256,40
        self._ext,self._name  = '',''
        self.setObject(object)
        self.wincolor = [32,64,64,192]
        self.setGeometry((c_pos.x()-offset),(c_pos.y()-offset),w,h)
        self.setAcceptDrops(False)
        self.setWindowFlags(sg._setWindowFlagsDict['tophint=True'])
        
        radioLayout = QtWidgets.QHBoxLayout()
        self.rb_filter  = QtWidgets.QRadioButton('Filter mode')
        self.rb_exclude = QtWidgets.QRadioButton('Exclude mode')
        ([rb.setStyleSheet('QRadioButton{color:%s;}'%(self._st['label']))
            for rb in (self.rb_filter,self.rb_exclude)])
        (self.rb_filter.setChecked(True)
                if self.getObject()._saveRB == 1 else
            self.rb_exclude.setChecked(True))
        
        radioLayout.addStretch()
        radioLayout.addWidget(self.rb_filter)
        radioLayout.addWidget(self.rb_exclude)
        
        extLabel  = QtWidgets.QLabel('Ext :')
        nameLabel = QtWidgets.QLabel('Name :')
        ([l.setStyleSheet('QLabel{color:%s;}'%(self._st['label']))
            for l in (extLabel,nameLabel)])
        self.extTextFilter  = QtWidgets.QTextEdit('')
        self.extTextFilter.textChanged.connect(self.extWriteChanged)
        self.nameTextFilter = QtWidgets.QTextEdit('')
        self.nameTextFilter.textChanged.connect(self.nameWriteChanged)
        for t in (self.extTextFilter,self.nameTextFilter):
            t.setStyleSheet(
                'QTextEdit{color:%s;background-color:%s;}'%(
                    self._st['text'],self._st['bg']))
            t.setTabChangesFocus(True)
        
        self.we = sg.WidgetEventAction()
        self.we.setTitle('Filter setting')
        self.we.setCloseTime(100)
        self.we.setHide('close')
        self.we.setHide('minimize')
        self.we.setWidget()
        self.we.setSelf(self)
        self.we.t.setStyleSheet(
            'QLabel{font-family:GEORGIA;font-size:13px;color:#FFF;}')
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.we.getWidget())
        self.layout.addLayout(radioLayout)
        self.layout.addWidget(extLabel)
        self.layout.addWidget(self.extTextFilter)
        self.layout.addWidget(nameLabel)
        self.layout.addWidget(self.nameTextFilter)
        
        self.setting()
    
    ## ------------------------------------------------------------------------
    ## event
    
    def leaveEvent(self,event):
        r"""
            カーソルが出たときのイベントアクション
        """
        _stringToList = (lambda w:
            (w.split('\n') if '\n' in w else [] if w == '' else [w]))
        obj = self.getObject()
        fd  = obj._feDict
        fd.update({'ext' :self.getExt()})
        fd.update({'name':self.getName()})
        if self.rb_filter.isChecked():
            fd.update({'ext_f' :_stringToList(self.getExt())})
            fd.update({'name_f':_stringToList(self.getName())})
            fd.update({'ext_e' :[]})
            fd.update({'name_e':[]})
            obj._saveRB = 1
        else:
            fd.update({'ext_f' :[]})
            fd.update({'name_f':[]})
            fd.update({'ext_e' :_stringToList(self.getExt())})
            fd.update({'name_e':_stringToList(self.getName())})
            obj._saveRB = 2
        self.we.setCloseTimeElapsed()
    
    ## ------------------------------------------------------------------------
    ## func
    
    def setting(self):
        r"""
            初期設定関数
        """
        fd = self.getObject()._feDict
        if fd['ext']:
            self.setExt(fd['ext'])
            self.extTextFilter.setPlainText(fd['ext'])
        if fd['name']:
            self.setName(fd['name'])
            self.nameTextFilter.setPlainText(fd['name'])

    def setObject(self,obj):
        r"""
            オブジェクト格納関数
        """
        self._object = obj
        
    def getObject(self):
        r"""
            オブジェクト変数を返す
        """
        return self._object
        
    def setExt(self,word):
        r"""
            extのフィルター設定関数
        """
        self._ext = word
        
    def getExt(self):
        r"""
            ext設定変数を返す
        """
        return self._ext
        
    def setName(self,word):
        r"""
            nameのフィルター設定関数
        """
        self._name = word
        
    def getName(self):
        r"""
            name設定変数を返す
        """
        return self._name
        
    def extWriteChanged(self):
        r"""
            extフィールドが変更された時に文字列を変数に保存する関数
        """
        self.setExt(self.extTextFilter.toPlainText())
        
    def nameWriteChanged(self):
        r"""
            nameフィールドが変更された時に文字列を変数に保存する関数
        """
        self.setName(self.nameTextFilter.toPlainText())
        
###############################################################################
        
class PathLineWidget(QtWidgets.QWidget):
    r"""
        パスライン設定のウィジェット
    """
    def __init__(self,parent=None):
        r"""
            ウィジェットライン
            
            Args:
                parent (any):enter description
                
            Returns:
                any:
        """
        super(PathLineWidget,self).__init__(parent)
        self.setAcceptDrops(True)
        
        self.title    = QtWidgets.QLabel('DEFAULT')
        self.pathLine = QtWidgets.QLineEdit('')
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.title,alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.pathLine)
        self.layout.addStretch()
    
    ## ------------------------------------------------------------------------
    ## event
    
    def dragEnterEvent(self,event):
        r"""
            ドラッグのイベント
        """
        mime = event.mimeData()
        event.accept() if mime.hasUrls() else event.ignore()
    
    def dropEvent(self,event):
        r"""
            ドロップのイベント
        """
        _fc = (lambda p: os.path.dirname(p) if os.path.isfile(p) else p)
        ([self.pathLine.setText(_fc(p.toLocalFile()))
            for p in event.mimeData().urls()])
    
###############################################################################
    
class ZipCreater(sg.ScrolledWidget):
    r"""
        zip作成gui
    """
    _STYLESHEET = {
        'QLineEdit':'QLineEdit{color:#000;background-color:#FFF;}',
        'QLabel'   :'QLabel{color:#FFF;}',
    }
    _feDict = {
        'ext' :'','ext_f' :[],'ext_e' :[],
        'name':'','name_f':[],'name_e':[],
    }
    _saveRB = 1
    
    def __init__(self,parent=None,masterDict=None):
        r"""
            初期設定
        """
        super(ZipCreater,self).__init__(parent)
        self._dict = masterDict
    
    ## ------------------------------------------------------------------------
    ## common parent event setting
    
    ## ------------------------------------------------------------------------
    ## build
    
    def buildUI(self,parent=None):
        r"""
            enter description
        """
        self._LAYOUTDICT = {}
        __LINEEDIT,__LABEL = [],[]
        
        self.SP = PathLineWidget()
        self.SP.title.setText('Original data')
        __LABEL.append(self.SP.title)
        __LINEEDIT.append(self.SP.pathLine)
        
        self.DP = PathLineWidget()
        self.DP.title.setText('Export to path')
        __LABEL.append(self.DP.title)
        __LINEEDIT.append(self.DP.pathLine)
        
        nameLayout = QtWidgets.QHBoxLayout()
        nameLayout.setContentsMargins(10,8,10,0)
        nameLabel = QtWidgets.QLabel('Name : ')
        __LABEL.append(nameLabel)
        self.nameLine = QtWidgets.QLineEdit('')
        __LINEEDIT.append(self.nameLine)
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameLine)
        
        exeLayout = QtWidgets.QHBoxLayout()
        self.exeLabel = QtWidgets.QLabel('')
        self.exeLabel.setStyleSheet('QLabel{color:#111;}')
        __LABEL.append(self.exeLabel)
        exeButton = QtWidgets.QPushButton('Execute')
        exeButton.clicked.connect(self.execute)
        exeLayout.addWidget(self.exeLabel,2,alignment=QtCore.Qt.AlignCenter)
        exeLayout.addWidget(exeButton,3)
        
        self.layout = QtWidgets.QVBoxLayout(parent)
        self.layout.addWidget(self.SP)
        self.layout.addWidget(self.DP)
        self.layout.addLayout(nameLayout)
        self.layout.addStretch()
        self.layout.addLayout(exeLayout)

        self._LAYOUTDICT.update({'QLineEdit':__LINEEDIT})
        self._LAYOUTDICT.update({'QLabel'   :__LABEL})
        self.setting()
    
    ## ------------------------------------------------------------------------
    ## event
    
    def mouseDoubleClickEvent(self,event):
        r"""
            ダブルクリックのイベント
        """
        fw = FilterWidget(self)
        fw.show()
    
    ## ------------------------------------------------------------------------
    ## setting
    
    def setting(self):
        r"""
            初期設定の窓口関数
        """
        self.setFirstName()
        self.styleSheetSet()
        
    def setFirstName(self):
        r"""
            書き出しzip名の名前にデフォルトのランダム文字を入れる
        """
        self.nameLine.setText(
            '{}_{}'.format(
                sg.getDateTime()['ymd'][0],sg.returnRandomString(length=8)
            )
        )
    
    def styleSheetSet(self):
        r"""
            スタイルシート一括設定
        """
        ([w.setStyleSheet(self._STYLESHEET[a])
            for a in self._LAYOUTDICT for w in self._LAYOUTDICT[a]])
    
    def getAboutData(self):
        r"""
            about情報の取得
        """
        return fc.getAboutInfo()
    
    ## ------------------------------------------------------------------------
    ## func
        
    def execute(self):
        r"""
            実行
        """
        STIE = sg.SystemTrayIcon(2000)
        STIE.setTitle('+ Error.')
        STIE.setMsg('')
        
        src  = self.SP.pathLine.text()
        dst  = self.DP.pathLine.text()
        name = self.nameLine.text()
        if not src:
            msg = '>> Not set src path.'
            STIE.setMsg(msg)
            STIE.showMsg()
            raise RuntimeError(msg)
        elif not dst:
            msg = '>> Not set dst path.'
            STIE.setMsg(msg)
            STIE.showMsg()
            raise RuntimeError(msg)
        elif not name:
            msg = '>> Not set export zip name.'
            STIE.setMsg(msg)
            STIE.showMsg()
            raise RuntimeError(msg)
        STIE.setTitle('+ Create start.')
        STIE.showMsg()
        
        res  = sg.createZipFile(src,dst,name,createMode=1,
            extFilter   = self._feDict['ext_f'] ,
            nameFilter  = self._feDict['name_f'],
            extExclude  = self._feDict['ext_e'] ,
            nameExclude = self._feDict['name_e'],
        )
        _S = {
            'setText'   :self.exeLabel.setText,
            'styleSheet':self.exeLabel.setStyleSheet,
        }
        if res:
            _S['setText']('Exrport!!')
        else:
            _S['styleSheet']('QLabel{color:#F00;}')
            _S['setText']('Error!!')
            _S['styleSheet']('QLabel{color:#111;}')
        
        QtCore.QTimer.singleShot(st._vanishTime,(lambda:_S['setText']('')))
        self.setFirstName()
        
        STIE = sg.SystemTrayIcon(9999)
        STIE.setTitle('Executed.')
        STIE.setMsg('Src:\n{}\nDst:\n{}\nName:\n{}'.format(src,dst,name))
        STIE.setIcon(1)
        STIE.showMsg()

###############################################################################
## END
