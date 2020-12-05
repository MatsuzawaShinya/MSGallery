#!/usr/bin/python
# -*- coding: utf-8 -*-
# old_style:google style:google
r"""
    入力ファイルを規則に沿ってリネームするツール
"""
###############################################################################
## base lib

import os
import re
import sys
import json
import string
import traceback

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from . import func as fc
from ... import settings as st
from msAppTools.settingFiles import systemGeneral as sg

QtWidgets,QtCore,QtGui = sg.QtWidgets,sg.QtCore,sg.QtGui
keymethod = sg.KeyMethod()

## ----------------------------------------------------------------------------

_setResizeMode = ('setResizeMode'
    if sg.getPythonVersion()=='27' else 'setSectionResizeMode')

###############################################################################

class InputLine(QtWidgets.QLineEdit):
    r"""
        入力ラインのカスタマイズクラス
    """
    def __init__(self,text,parent=None):
        r"""
        """
        super(InputLine,self).__init__(text,parent)
        self.executeMethod = self.__temp
    
    def __temp(self):
        r"""
            テンプレートメソッド
        """
        print(u'>>> テンプレート用のメソッドを表示しています。')
    
    def setExecuteMethod(self,m):
        r"""
            実行メソッドをセット
        """
        self.executeMethod = m
    
    def getExecuteMethod(self):
        r"""
            実行メソッドを取得
        """
        return self.executeMethod
        
    def exeExecuteMethod(self):
        r"""
            メソッドを実行
        """
        try:
            self.getExecuteMethod()()
        except:
            print(u'>>> メソッドを実行出来ませんでした。')
            print(u'\nMethod = {}'.format(self.getExecuteMethod()))
            print
        
    def keyPressEvent(self,event):
        r"""
            キープレスイベント設定
        """
        super(InputLine,self).keyPressEvent(event)
        key   = keymethod._keyType(event)
        mask  = keymethod._keyMask()
        mask2 = keymethod._keyMask2()
        
        if key['press'] in ['Enter','Return']:
            self.exeExecuteMethod()
    
###############################################################################
    
class TreeView(QtWidgets.QTreeView):
    r"""
        ビュー作成のクラス
    """
    debugFlag = None
    
    def __init__(self,parent=None):
        r"""
            設定
        """
        super(TreeView,self).__init__(parent)
        
        self.listInitialize()
        
        self.__firstPathList  = []
        self.__basenameList   = []
        self.__changenameList = []
        
        self._changeTextDict     = {}
        self._checkboxWidgetDict = {}
        
        self.setAcceptDrops(True)
        self.setDragEnabled(False)
        self.setDropIndicatorShown(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.doubleClicked.connect(self.deleteDoubleClicked)
        
    ## ------------------------------------------------------------------------
    ## event
    
    def dragEnterEvent(self,event):
        r"""
            ドラッグ時のイベント
        """
        mime = event.mimeData()
        event.accept() if mime.hasUrls() else event.ignore()
    
    def dragMoveEvent(self,event):
        r"""
            ドラック中のイベント
        """
        mime = event.mimeData()
        event.accept() if mime.hasUrls() else event.ignore()
        
    def dropEvent(self,event):
        r"""
            ドロップ時のイベント
        """
        mine = event.mimeData()
        if mine.hasUrls():
            urls = mine.urls()
            for url in urls:
                filename = url.toLocalFile()
                self.__firstPathList.append(filename)
        else:
            event.ignore()
        self.addViewItem()
        self.listUpdate()
    
    def keyPressEvent(self,event):
        r"""
            キー押下時のイベント
        """
        key   = keymethod._keyType(event)
        mask  = keymethod._keyMask()
        mask2 = keymethod._keyMask2()
        
        self.getSelectItem()
        if key['press'] in ('Del','Backspace'):
            [self.removeItem(x) for x in self.getSelectItemRow()]
            
    ## ------------------------------------------------------------------------
    ## setting
    
    def listInitialize(self):
        r"""
            リストの初期化
        """
        self.__firstPathList  = []
        self.__basenameList   = []
        self.__changenameList = []
    
    def setCheckboxWidgetDict(self,d):
        r"""
            チェックボックスウィジェット辞書の格納
        """
        self._checkboxWidgetDict = d
        
    def getCheckboxWidgetDict(self):
        r"""
            チェックボックスウィジェット辞書のリターン
        """
        return self._checkboxWidgetDict
    
    def getSelectItem(self):
        r"""
            選択アイテムのリターン(オブジェクト)
        """
        return [s for s in self.selectedIndexes()]
    
    def getSelectItemData(self):
        r"""
            選択アイテムのリターン(アイテム名)
        """
        return [s.data() for s in self.selectedIndexes()]
    
    def getSelectItemRow(self,sorted=True):
        r"""
            選択アイテムのリターン(row)
        """
        _L = [s.row() for s in self.selectedIndexes()]
        _L = list(set(_L))
        _L.sort(reverse=sorted)
        return _L
        
    def setDebugFlag(self,value=True):
        r"""
            デバックフラグのスイッチ(オーバーライド)
        """
        self.debugFlag = value
    
    ## ------------------------------------------------------------------------
    ## local func
    
    def _setList(self,_L):
        r"""
            順番を維持しつつリストの重複を削除して返す
        """
        return sorted(set(_L),key=_L.index) if isinstance(_L,list) else []
    
    ## ------------------------------------------------------------------------
    ## func
    
    def addViewItem(self):
        r"""
            アイテムの初期追加関数
        """
        self.removeAllItem()
        model = self.model()
        row   = model.rowCount()
        for i,s in enumerate(self.__basenameList):
            model.setItem(i+row,0,QtGui.QStandardItem(s))
            model.setItem(i+row,1,QtGui.QStandardItem(s))
    
    def dictUpdate(self,k,a):
        r"""
            テキスト変更のアップデート関数
        """
        self._changeTextDict[k] = a
    
    def textLineCheck(self):
        r"""
            startLineの設定
        """
        # _tex = self.sender().self.text()
        self.organizeViewItem()
    
    def numberLineEdit(self):
        r"""
            数値系(start,padding,step)lineEditの上限下限設定
        """
        s = self.sender()
        _text = s.self.text()
        if _text and s.address['type'] in ('padding','step'):
            try:
                _num = int(_text)
                if _num < 1:
                    s.self.setText('1')
            except:
                pass
        self.organizeViewItem()
        
    def organizeViewItem(self):
        r"""
            編集された名前を生成しリストアップする
        """
        s = self.sender()
        try:
            self.dictUpdate(s.address['type'],s.self.text())
        except:
            pass
        self.listUpdate()
    
    def deleteDoubleClicked(self,index=None):
        r"""
            ダブルクリック時のアイテム削除関数
        """
        self.removeItem(self.selectedIndexes()[0].row())
    
    def removeItem(self,index=0):
        r"""
            アイテムの削除
        """
        model = self.model()
        model.removeRow(index,QtCore.QModelIndex())
        self.listOrganize(index)
    
    def removeAllItem(self):
        r"""
            全てのアイテムの削除
        """
        model = self.model()
        ([model.removeRow(0,QtCore.QModelIndex())
            for r in range(model.rowCount())])
    
    def reAddItem(self):
        r"""
            編集されたアイテムをビューにセット
        """
        self.removeAllItem()
        model = self.model()
        row   = model.rowCount()
        for i,x in enumerate(zip(self.__basenameList,self.__changenameList)):
            model.setItem(i+row,0,QtGui.QStandardItem(x[0]))
            model.setItem(i+row,1,QtGui.QStandardItem(x[1]))
    
    def beforeAfterTextChanged(self,_list):
        r"""
            入力されたテキスト情報を元に置き換える名前を作成する
        """
        _E = sg.toEncode
        _D = sg.toDecode 
        
        _d = self._changeTextDict
        _bn,_sc,_re,_pr,_su = '','','','',''
        _st,_pd,_sp = None,None,None
        if _d.get('basename'):
            _bn = _d['basename']
        if _d.get('start'):
            _st = _d['start']
        if _d.get('padding'):
            _pd = _d['padding']
        if _d.get('step'):
            _sp = _d['step']
        if _d.get('search'):
            _sc = _d['search']
        if _d.get('replace'):
            _re = _d['replace']
        if _d.get('prefix'):
            _pr = _d['prefix']
        if _d.get('suffix'):
            _su = _d['suffix']
        
        __cb = self.getCheckboxWidgetDict()
        __cb_bn = __cb.get('basename').isChecked()
        __cb_re = __cb.get('regularExpression').isChecked()
        __cb_rp = __cb.get('replace').isChecked()
        __cb_ps = __cb.get('prefixSuffix').isChecked()
        
        numberFlag  = True if (_st and _pd and _sp) else False
        try:
            _ck = int(_st)
            _stFlag = 1 if isinstance(_ck,int) else 2
        except:
            _stFlag = 2
        _LS = True
        if numberFlag:
            # ここで英数字(A-Z)を数値(0-25)に置き換え
            if _stFlag == 2:
                if re.search('[A-Za-z]+',_st):
                    _nums = (int(
                        sg.alphabeticNumberConversion(sg.toEncode(_st)))-1)
                    _LS = False if _st.islower() else True
                else:
                    _nums = 1
            else:
                _nums = int(_st)
        _returnList = []
        for _l in _list:
            _bef = os.path.splitext(_l)[0]
            _aft = os.path.splitext(_l)[1]
            # search/replace
            if __cb_rp:
                # regularExpression
                if __cb_re:
                    try:
                        _bef = re.sub(_sc,_re,_bef)
                    except:
                        _bef = _bef
                else:
                    if _sc:
                        _bef = _bef.replace(_sc,_re,1)
            # prefix/suffix
            if __cb_ps:
                try:
                    _bef = _D('{}{}{}'.format(_E(_pr),_E(_bef),_E(_su)))
                except:
                    _bef = _bef
            # basename
            if __cb_bn:
                if numberFlag:
                    _pad = ('{:0>%s}'%(_pd)).format(_nums)
                    _nums += int(_sp)
                    _bef = _D('{}{}'.format(_bn,_pad))
                    if _stFlag == 2:
                        _alp = sg.alphabeticNumberConversion(int(_pad)+1,_LS)
                        _bef = _D(('{}{:%s>%s}'%(
                            'A' if _LS else 'a',_pd)).format(_bn,_alp))
            res_tex = _D('{}{}'.format(_E(_bef),_E(_aft)))
            _returnList.append(res_tex)
            if self.debugFlag:
                print('res_tex =',res_tex)
        return _returnList
    
    def cbListUpdate(self,value=None):
        r"""
            checkboxのtoggledから実行されるアップデート関数
        """
        try:
            self.textLineCheck()
        except:
            pass
        self.listUpdate()
    
    def listOrganize(self,index=0):
        r"""
            インデックス番号の要素を削除その後更新する
        """
        del self.__firstPathList[index]
        self.listUpdate()
        
    def __listCheck(self):
        r"""
            リストの整合性のチェック
        """
        LOG = ''
        len_f = len(self.__firstPathList)
        len_b = len(self.__basenameList)
        len_c = len(self.__changenameList)
        if not len_f == len_b == len_c:
            LOG += (u'+ リスト変数の数の不一致\n')
            LOG += (u'    self.__firstPathList  = "{}"\n'.format(len_f))
            LOG += (u'    self.__basenameList   = "{}"\n'.format(len_b))
            LOG += (u'    self.__changenameList = "{}"\n'.format(len_c))
            print(LOG)
            raise
    
    def __getListNums(self):
        r"""
            リストサイズ（）をリターン
        """
        self.__listCheck()
        return len(self.__firstPathList)
    
    def listUpdate(self):
        r"""
            リストを整理して更新する
        """
        self.__firstPathList  = self._setList(self.__firstPathList)
        self.__basenameList   = self._setList(([os.path.basename(p)
                                        for p in self.__firstPathList]))
        self.__changenameList = self.beforeAfterTextChanged(self.__basenameList)
        
        self.__listCheck()
        self.reAddItem()
        self.headerResize()
    
    def headerResize(self):
        r"""
            ヘッダーのサイズをフィットさせる
        """
        # こちらで実行するコマンドは""でくくらない
        eval('self.header().{}(0,'
             'QtWidgets.QHeaderView.ResizeToContents)'.format(_setResizeMode))
        eval('self.header().{}(1,'
             'QtWidgets.QHeaderView.ResizeToContents)'.format(_setResizeMode))
    
    def executeRename(self):
        r"""
            リネームの実行
        """
        def _renameLoop():
            r"""
                リネーム処理の再帰関数
            """
            self.__listCheck()
            __forNums = 0
            numberExecutions = len(self.__firstPathList)
            # 逆順から処理することで昇順名前のリネーム被りを少しでも回避する
            for i in reversed(range(numberExecutions)):
                src = self.__firstPathList[i]
                dst = src.replace(
                    self.__basenameList[i],self.__changenameList[i])
                if os.path.exists(dst):
                    __forNums += 1
                    continue
                os.rename(src,dst)
                print(u'Renamed.\n  src = {}\n  dst = {}'.format(src,dst))
                self.removeItem(i)
            
            # 全てコンティニューの(リネーム先の名前があった)場合は処理を抜ける。
            # -> 上書き防止のため（os.renameすると強制的に上書きになる）
            if numberExecutions == __forNums:
                print(u'+ 全てのアイテムのリネーム先があるため処理を中断します。')
                return -2
            # アイテムを全て処理し終えたら抜ける
            elif self.__getListNums() == 0:
                self.listInitialize()
                return -1
            # それ以外はアイテムを再処理する
            else:
                _renameLoop()
        
        _renameLoop()
        
###############################################################################

class Renamer(sg.ScrolledWidget):
    r"""
        rename用gui
    """
    debugFlag = None
    
    def __init__(self,parent=None,masterDict=None):
        r"""
            初期設定
        """
        super(Renamer,self).__init__(parent)
        self._dict   = masterDict
        self._parent = parent
    
    ## ------------------------------------------------------------------------
    ## common parent event setting
    
    ## ------------------------------------------------------------------------
    ## build
    
    def buildUI(self,parent=None):
        r"""
            メインレイアウト作成関数（オーバーライド）
        """
        _fontColor = 'color:#FFF'
        __titleStyle    = (lambda x: x.setStyleSheet(
            'QLabel{font-size:16px;font-family:GEORGIA;%s;}'%(_fontColor)))
        __labelStyle    = (lambda x: x.setStyleSheet(
            'QLabel{%s;}'%(_fontColor)))
        __checkBoxStyle = (lambda x: x.setStyleSheet(
            'QCheckBox{%s;}'%(_fontColor)))
        
        _s =  ''
        _s += ('QLabel{%s;}'      %(_fontColor))
        _s += ('QCheckBox{%s;}'   %(_fontColor))
        _s += ('QRadioButton{%s;}'%(_fontColor))
        _s += self.getStyleSheet()
        self.setStyleSheet(_s)
        
        ## --------------------------------------------------------------------
        ## setting
        
        Q_LABEL = QtWidgets.QLabel
        
        __textWidgetList     = []
        __checkboxWidgetDict = {}
        __labelWidgetList    = []
        __checkBoxWidgetList = []
        
        ## --------------------------------------------------------------------
        ## local func
        
        def _getFrameWidget():
            r"""
                frameWidgetを作成しリターン
            """
            buf = QtWidgets.QFrame()
            objname = 'bn_{}'.format(sg.returnRandomString(length=12))
            buf.setObjectName(objname)
            buf.setStyleSheet(
                '#%s{border:2px solid #FFF;}'%(objname)
            )
            return buf
        
        ## --------------------------------------------------------------------# -------------------------------------------------
        ## basename
        
        basenameFrame  = _getFrameWidget()
        basenameLayout = QtWidgets.QVBoxLayout(basenameFrame)

        bn_title = Q_LABEL('+ Basename settings')
        __titleStyle(bn_title)
        bn_checkLayout = QtWidgets.QHBoxLayout()
        self.bn_enableCheck = QtWidgets.QCheckBox('Enable')
        __checkboxWidgetDict['basename'] = self.bn_enableCheck
        bn_checkLayout.addStretch()
        bn_checkLayout.addWidget(self.bn_enableCheck)
        
        bn_editLayout = QtWidgets.QHBoxLayout()
        bn_nameLabel = Q_LABEL('Input name : ')
        __labelWidgetList.append(bn_nameLabel)
        self.bn_basenameLine = InputLine('base')
        self.bn_basenameLine.address = {'type':'basename'}
        __textWidgetList.append(self.bn_basenameLine)
        bn_editLayout.addWidget(bn_nameLabel)
        bn_editLayout.addWidget(self.bn_basenameLine)
        
        bn_numberingLayout = QtWidgets.QHBoxLayout()
        self.startNumLine  = InputLine('1')
        self.paddingLine   = InputLine('1')
        self.stepLine      = InputLine('1')
        self.startNumLine.address = {'type':'start'  }
        self.paddingLine.address  = {'type':'padding'}
        self.stepLine.address     = {'type':'step'   }
        __textWidgetList.append(self.startNumLine)
        __textWidgetList.append(self.paddingLine)
        __textWidgetList.append(self.stepLine)
        for x in (self.paddingLine,self.stepLine):
            x.setValidator(QtGui.QIntValidator())
        qlabelbuf = Q_LABEL('Start number')
        __labelWidgetList.append(qlabelbuf)
        bn_numberingLayout.addWidget(qlabelbuf,2)
        bn_numberingLayout.addWidget(self.startNumLine,1)
        bn_numberingLayout.addSpacing(6)
        qlabelbuf = Q_LABEL('Padding')
        __labelWidgetList.append(qlabelbuf)
        bn_numberingLayout.addWidget(qlabelbuf,2)
        bn_numberingLayout.addWidget(self.paddingLine,1)
        bn_numberingLayout.addSpacing(6)
        qlabelbuf = Q_LABEL('Step')
        __labelWidgetList.append(qlabelbuf)
        bn_numberingLayout.addWidget(qlabelbuf,2)
        bn_numberingLayout.addWidget(self.stepLine,1)
        
        basenameLayout.addWidget(bn_title)
        basenameLayout.addLayout(bn_checkLayout)
        basenameLayout.addLayout(bn_editLayout)
        basenameLayout.addLayout(bn_numberingLayout)
                
        ## --------------------------------------------------------------------
        ## replace
        
        replaceFrame  = _getFrameWidget()
        replaceLayout = QtWidgets.QVBoxLayout(replaceFrame)
        
        rep_title = Q_LABEL('+ Replace')
        __titleStyle(rep_title)
        rep_checkLayout = QtWidgets.QHBoxLayout()
        self.rep_regexpCheck = QtWidgets.QCheckBox('Regular Expression')
        self.rep_regexpCheck.setChecked(False)
        __checkboxWidgetDict['regularExpression'] = self.rep_regexpCheck
        self.rep_enableCheck = QtWidgets.QCheckBox('Enable')
        self.rep_enableCheck.setChecked(True)
        __checkboxWidgetDict['replace'] = self.rep_enableCheck
        rep_checkLayout.addStretch()
        rep_checkLayout.addWidget(self.rep_regexpCheck)
        rep_checkLayout.addWidget(self.rep_enableCheck)
        
        rep_formLayout       = QtWidgets.QFormLayout()
        self.rep_searchLine  = InputLine('')
        self.rep_replaceLine = InputLine('')
        self.rep_searchLine.address  = {'type':'search'}
        self.rep_replaceLine.address = {'type':'replace'}
        __textWidgetList.append(self.rep_searchLine)
        __textWidgetList.append(self.rep_replaceLine)
        qlabelbuf = Q_LABEL('Search  :')
        __labelWidgetList.append(qlabelbuf)
        rep_formLayout.addRow(qlabelbuf,self.rep_searchLine)
        qlabelbuf = Q_LABEL('Replace :')
        __labelWidgetList.append(qlabelbuf)
        rep_formLayout.addRow(qlabelbuf,self.rep_replaceLine)
        
        replaceLayout.addWidget(rep_title)
        replaceLayout.addLayout(rep_checkLayout)
        replaceLayout.addLayout(rep_formLayout)
        
        ## --------------------------------------------------------------------
        ## prefix/suffix
        
        presufFrame  = _getFrameWidget()
        presufLayout = QtWidgets.QVBoxLayout(presufFrame)
        ps_title = Q_LABEL('+ Prefix / Suffix')
        __titleStyle(ps_title)
        self.ps_enableCheck = QtWidgets.QCheckBox('Enable')
        self.ps_enableCheck.setChecked(True)
        __checkboxWidgetDict['prefixSuffix'] = self.ps_enableCheck
        
        ps_formLayout      = QtWidgets.QFormLayout()
        self.ps_prefixLine = InputLine('')
        self.ps_suffixLine = InputLine('')
        self.ps_prefixLine.address = {'type':'prefix'}
        self.ps_suffixLine.address = {'type':'suffix'}
        __textWidgetList.append(self.ps_prefixLine)
        __textWidgetList.append(self.ps_suffixLine)
        qlabelbuf = Q_LABEL('Prefix :')
        __labelWidgetList.append(qlabelbuf)
        ps_formLayout.addRow(qlabelbuf,self.ps_prefixLine)
        qlabelbuf = Q_LABEL('Suffix :')
        __labelWidgetList.append(qlabelbuf)
        ps_formLayout.addRow(qlabelbuf,self.ps_suffixLine)
        
        presufLayout.addWidget(ps_title)
        presufLayout.addWidget(self.ps_enableCheck,alignment=QtCore.Qt.AlignRight)
        presufLayout.addLayout(ps_formLayout)
        
        ## --------------------------------------------------------------------
        ## view
        
        self._view = TreeView()
        model = QtGui.QStandardItemModel(0,2)
        model.setHeaderData(0,QtCore.Qt.Horizontal,'Before')
        model.setHeaderData(1,QtCore.Qt.Horizontal,'After')
        self._view.setModel(model)
        # こちらで実行するコマンドは""でくくる
        eval('"self._view.header().{}(0,'
             'QtWidgets.QHeaderView.ReasizeToContents)"'.format(_setResizeMode))
        
        ## --------------------------------------------------------------------
        ## execute
        
        self.exeButton = QtWidgets.QPushButton('Rename execute')
        self.exeButton.setFixedWidth(100)
        self.exeButton.setStyleSheet(
            'QPushButton{color:#FFF;%s}'%(sg.ss.GRD_C_VERTICAL%('#777','#111'))
        )
        self.exeButton.clicked.connect(self._view.executeRename)

        ## --------------------------------------------------------------------
        ## all
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setContentsMargins(8,8,8,8)
        layout.addWidget(basenameFrame)
        layout.addWidget(replaceFrame)
        layout.addWidget(presufFrame)
        layout.addWidget(self._view)
        layout.addWidget(self.exeButton,alignment=QtCore.Qt.AlignCenter)
    
        ## --------------------------------------------------------------------
        ## post setting
        
        # label
        [__labelStyle(x) for x in __labelWidgetList]
        
        # lineEdit
        for _t in __textWidgetList:
            _t.self     = _t  
            _type,_text = _t.address['type'],_t.text()
            self._view.dictUpdate(_type,_text)
            if _type in ('start',):
                _func = self._view.textLineCheck
            elif _type in ('padding','step'):
                _func = self._view.numberLineEdit
            else:
                _func = self._view.organizeViewItem
                if _type in ('basename',):
                    pass
            _t.textChanged.connect(_func)
            try:
                _t.setExecuteMethod(self._view.executeRename)
            except:
                print(u'>>> InputLine/setExecuteMethodを実行できませんでした。')
                print
        
        # checkBox
        self._view.setCheckboxWidgetDict(__checkboxWidgetDict)
        for _c in __checkboxWidgetDict:
            __checkboxWidgetDict[_c].toggled.connect(self._view.cbListUpdate)
            __checkBoxStyle(__checkboxWidgetDict[_c])
        
    ## --------------------------------------------------------------------
    ## event
    
    def resizeEvent(self,event):
        r"""
            リサイズされた際のイベント
        """
        super(Renamer,self).resizeEvent(event)
        self.buttonResized(event)
    
    ## --------------------------------------------------------------------
    ## setting
    
    def buttonResized(self,event=None,ratio=60):
        r"""
            renameボタン/リサイズ
        """
        # self._parent.rect().width(),self._parent.rect().height()
        # event.size().width(),event.size().height()
        self.exeButton.setFixedWidth(event.size().width()*(ratio*0.01))
    
    def setDebugFlag(self,value=True):
        r"""
            デバックフラグのスイッチ(オーバーライド)
        """
        self.debugFlag = value
        self._view.setDebugFlag(value)
    
    def getAboutData(self):
        r"""
            about情報の取得
        """
        return fc.getAboutInfo()

###############################################################################
## END
