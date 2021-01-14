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

_SPSL = fc._SPSL

## ----------------------------------------------------------------------------

_setResizeMode = ('setResizeMode'
    if sg.getPythonVersion()=='27' else 'setSectionResizeMode')

_PREFIX = 'prefix'
_SUFFIX = 'suffix'

###############################################################################
## sub func

_SV = sg.SuggestView()
_SV.exeHide()

_VM_ = sg.VariableManagement()

###############################################################################
## sub class

class InputLine(QtWidgets.QLineEdit):
    r"""
        入力ラインカスタマイズクラス
    """
    def __init__(self,text='',editText=True,parent=None):
        r"""
        """
        super(InputLine,self).__init__(text,parent)
        self.parentWidget  = parent if parent else None
        self.executeMethod = self.__temp
        
        self.setTextEnableFlag = editText
        self.cursorPositionChanged.connect(self.textChange)
    
    ## ----------------------------------------------------
    ## temp    
    
    def __temp(self):
        r"""
            テンプレートメソッド
        """
        print(u'>>> テンプレート用のメソッドを表示しています。')
    
    ## ----------------------------------------------------
    ## setting
    
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
    
    ## ----------------------------------------------------
    ## event
        
    def keyPressEvent(self,event):
        r"""
            キープレスイベント設定
        """
        super(InputLine,self).keyPressEvent(event)
        key   = keymethod._keyType(event)
        mask  = keymethod._keyMask()
        mask2 = keymethod._keyMask2()
        
        if key['press'] in ['Enter','Return']:
            if not _SV.isHidden():
                self.suggestInsert()
            else:
                self.exeExecuteMethod()
        elif key['press'] in ['Up','Down','Left','Right']:
            if not _SV.isHidden():
                _SV.keyPressEvent(event)
        
    ## ----------------------------------------------------
    ## func
    
    def clearText(self):
        r"""
            テキストクリア
        """
        self.clear()
    
    def textChange(self,oldpos,newpos):
        r"""
            テキストラインが変更された時の挙動
        """
        _VM_.setVariable('nowFocusLineEdit',self)
        
        if not self.setTextEnableFlag:
            return
        _SV.setTextLineWidget(self)
        _SV.setSuggestItemList(sorted(
            _SPSL.getJsonEstimationData('sum').items(),
            reverse=True,key=(lambda x:x[1])))
        _SV.eachMovePositioning(self.moveGui)
        _SV.suggestSetting()

    def moveGui(self,lines=None,fit=True,resizeFlag=False):
        r"""
            ウィジェット位置調整(SuggestViewでも実行)
        """
        line   = lines if lines else self
        c_pos  = self.mapToGlobal(self.cursorRect().bottomRight())
        l_post = self.mapToGlobal(self.pos())
        ## fit=True /サジェスト表示位置をライン左部にフィット固定
        ## fit=False/サジェスト表示位置を入力カーソルライン位置に流動指定
        baseX = self.parentWidget.pos().x()
        putx  = (int(baseX-(_SV.rect().width()*0.5))
                    if fit else (c_pos.x()+(-14)))
        puty  = (c_pos.y()+(+2))
        putw  = _SV.rect().width()
        puth  = _SV.rect().height()
        
        # ディスプレイサイズに合わせたリミット数値調整
        _off  = -3
        _DI   = sg.DesktopInfo()
        drect = _DI.getWidgetDesktopSize(self.parentWidget)
        
        # 左側の調整
        if putx < _off:
            putw += putx
            putx  = 0
        else:
            putw = _SV.winsize[0]
        
        # 下側の調整
        blimit = drect.height()-(_SV.rect().height())
        if puty > blimit:
            puth += (blimit-puty)
            puty = blimit
        else:
            puth = _SV.winsize[1]
        
        _SV.move(putx,puty)
        if resizeFlag:
            _SV.resize(putw,puth)
        
    def suggestInsert(self):
        r"""
            サジェスト(Enter/Return)時の動作
        """
        _SV.suggestInsert()
    
## ----------------------------------------------------------------------------

class AdditionInputLine(QtWidgets.QWidget):
    r"""
        チェックボックスで切り替え可能な入力ラインの作成
    """
    def __init__(self,text='',editText=True,parent=None):
        r"""
        """
        self._parent = parent
        super(AdditionInputLine,self).__init__(self._parent)
        
        self.setWidgetStateInfo()
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(2,0,2,0)
        self.hlayout = QtWidgets.QHBoxLayout()

        ## ------------------------------------------------        
        ## tabで移動する際の順番はウィジェットの宣言順になる
        
        self.mainline  = InputLine(text,editText,self._parent)
        prefix = self.getCheckBoxLayout(_PREFIX,True)
        suffix = self.getCheckBoxLayout(_SUFFIX,False)
        self.setWidgetStateInfo('mainline',self.mainline)
        
        ## ------------------------------------------------        
        
        self.hlayout.addLayout(prefix,alignment=QtCore.Qt.AlignLeft)
        self.hlayout.addWidget(self.mainline,stretch=10)
        self.hlayout.addLayout(suffix,alignment=QtCore.Qt.AlignRight)
        self.layout.addLayout(self.hlayout)

    ## ----------------------------------------------------
    ## sub method
    
    def getCheckBoxLayout(self,named,pos=True):
        r"""
            チェックボックスの入力ラインを返す
        """
        ## ------------------------------------------------
        ## main layout
        
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        cb = QtWidgets.QCheckBox('')
        cb.setToolTip(u'チェックオンで入力文字を接続文字として付与')
        cb.setChecked(True)
        le = InputLine('',True,self._parent)
        le.setFixedWidth(50)
        cb.connectLineEdit = le
        cb.stateChanged.connect(self.checkBoxToggleState)
        
        wlist = [cb,le]
        [layout.addWidget(w) for w in (wlist[:] if pos else wlist[::-1])]
        
        self.setWidgetStateInfo('{}_layout'.format(named)  ,layout)
        self.setWidgetStateInfo('{}_checkbox'.format(named),cb)
        self.setWidgetStateInfo('{}_lineedit'.format(named),le)
        
        return layout
    
    ## ----------------------------------------------------
    ## setting
    
    def getMainEditLine(self):
        r"""
            メインのEditLineを取得する
        """
        return self.mainline if hasattr(self,'mainline') else None
    
    def setWidgetStateInfo(self,key=None,value=None):
        r"""
            ウィジェット内主要パーツ情報を辞書形式で保存
            key,value未定義で実行した場合は辞書を初期化
        """
        if key==None and value==None:
            self._widgetStateInfo = {}
            return
        self._widgetStateInfo.update({key:value})
        
    def getWidgetStateInfo(self,key=''):
        r"""
            ウィジェット内主要パーツ情報を返す
            key指定がある場合は辞書内容を取得
        """
        return (self._widgetStateInfo
            if not key else self._widgetStateInfo.get(key))
    
    ## ----------------------------------------------------
    ## widget method
            
    def checkBoxToggleState(self,state):
        r"""
            チェックボックス状態によってラインエディットの
            可視化を操作するメソッド
            checkState: [0]Unchecked, [1]PartiallyChecked, [2]Checked
                https://doc.qt.io/qt-5/qt.html#CheckState-enum
        """
        sender = self.sender()
        if not hasattr(sender,'connectLineEdit'):
            return
        sle = sender.connectLineEdit
        sle.show() if state==2 else sle.hide()

## ----------------------------------------------------------------------------
    
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
        
        self.__parentWidget = parent if parent else None
        
        self.refrectEstimationData(False)
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
        _P = _PREFIX
        _S = _SUFFIX
        _JO = '_'.join
        
        _d  = self._changeTextDict
        _bn = _d['basename'] if _d.get('basename') else ''
        _st = _d['start']    if _d.get('start')    else None
        _pd = _d['padding']  if _d.get('padding')  else None
        _sp = _d['step']     if _d.get('step')     else None
        _sc = _d['search']   if _d.get('search')   else ''
        _re = _d['replace']  if _d.get('replace')  else ''
        _pr = _d[_PREFIX]    if _d.get(_PREFIX)    else ''
        _su = _d[_SUFFIX]    if _d.get(_SUFFIX)    else ''
        
        __cb = self.getCheckboxWidgetDict()
        __cb_bn = __cb.get('basename').isChecked()
        __cb_rp = __cb.get('replace').isChecked()
        __cb_re = __cb.get('regularExpression').isChecked()
        __cb_ps = __cb.get('prefixSuffix').isChecked()

        _pr_pr = (_d[_JO([_P,_P])] if _d.get(_JO([_P,_P])) and
            __cb.get(_JO([_P,_P])).isChecked() else '')
        _pr_su = (_d[_JO([_P,_S])] if _d.get(_JO([_P,_S])) and
            __cb.get(_JO([_P,_S])).isChecked() else '')
        _su_pr = (_d[_JO([_S,_P])] if _d.get(_JO([_S,_P])) and
            __cb.get(_JO([_S,_P])).isChecked() else '')
        _su_su = (_d[_JO([_S,_S])] if _d.get(_JO([_S,_S])) and
            __cb.get(_JO([_S,_S])).isChecked() else '')
        
        estimationUpdataInfo = {
            'basename' : {
                'variable' : _bn,
                'enable'   : __cb_bn,
            },
            'search' : {
                'variable' : _sc,
                'enable'   : __cb_rp,
                'regexp'   : __cb_re
            },
            'replace' : {
                'variable' : _re,
                'enable'   : __cb_rp,
                'regexp'   : __cb_re,
            },
            _PREFIX : {
                'variable' : _pr,
                'enable'   : __cb_ps,
            },
            _SUFFIX : {
                'variable' : _su,
                'enable'   : __cb_ps,
            },
        }
        
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
                    _bef = _D('{}{}{}'.format(
                        _E('{}{}{}'.format(_pr_pr,_pr,_pr_su)),
                        _E(_bef),
                        _E('{}{}{}'.format(_su_pr,_su,_su_su)))
                    )
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
        
        ## estimation情報の更新
        if self.refrectEstimationData():
            printmsg = []
            saveDict_master = _SPSL.getJsonEstimationData('master')
            saveDict_ui     = _SPSL.getJsonEstimationData('ui')
            for key,item in estimationUpdataInfo.items():
                word = _d.get(key)
                # 各ラインのテキスト情報がない場合はスキップ
                if not word:
                    continue
                # enable=OFFの場合は処理しない
                if not item.get('enable'):
                    continue
                # replace/RegularExpressionが有効の場合は処理をしない
                if item.get('regexp'):
                    continue
                
                for word in [x for x in word.split('_')]:
                    if not word or word == '':
                        continue
                    printmsg.append(u'>> {}'.format(word))
                    for type in ['master','ui']:
                        targetdict = eval('saveDict_{}'.format(type))
                        nownum  = targetdict.get(word) if targetdict else 0
                        nextnum = (nownum if nownum else 0) + 1
                        if targetdict:
                            targetdict.update({word:nextnum})
                        else:
                            targetdict = {word:nextnum}
                        exec('saveDict_{}.update(targetdict)'.format(type))
                        printmsg.append(
                            u'{}: {} -> {}'.format('  {: <7}'.format(type),
                            nownum,nextnum))
            print('\n'.join(printmsg))

            _SPSL.setJsonEstimationData(saveDict_master,saveDict_ui)
            _SPSL.setBeforeEstimationInfo()
        
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
    
    def refrectEstimationData(self,flag=None):
        r"""
            estimationに書き込む際の有効フラグ設定
        """
        if isinstance(flag,bool):
            self.__estimationFlag = flag if isinstance(flag,bool) else False
        else:
            return self.__estimationFlag
    
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
                print(u'+ Renamed.\n  src = {}\n  dst = {}'.format(src,dst))
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
        
        self.refrectEstimationData(True)
        _renameLoop()
        self.refrectEstimationData(False)
        
        # Ctrlの押下情報があればテキストラインを初期化
        _key   = keymethod._keyType(None)
        _mask  = keymethod._keyMask()
        _mask2 = keymethod._keyMask2()
        if _key['mod2']==_mask2(['ctrl']):
            self.__parentWidget.setLineEditInfo()
        
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
        self.preSetting()
        self._dict   = masterDict
        self._parent = parent
        
        self._addressInfo = {
            'type'       : 'type',
            'initialize' : 'initialize',
        }
        
        super(Renamer,self).__init__(parent)
    
        # set/estimation
        _SPSL.setBeforeEstimationInfo()
        
        # set/suggestViwe setWindowFlags
        _SV.setParentWindowFlags(parent)
        
    ## ------------------------------------------------------------------------
    ## common parent event setting
    
    def setEventPackage(self,packaging):
        r"""
            子と関連性をためのメソッドパッケージを親から引き継いで設定する
        """
        super(Renamer,self).setEventPackage(packaging)
        
        # 親eventと連動
        if packaging:
            packaging()['set']('closeEvent',self.exeCloseEventFunc)
    
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
        
        ad_t = self._addressInfo.get('type')
        ad_i = self._addressInfo.get('initialize')
        
        
        self.__textWidgetList      = []
        self.__checkboxWidgetDict  = {}
        self.__labelWidgetList     = []
        self.__checkBoxWidgetList  = []
        
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
        self.__checkboxWidgetDict['basename'] = self.bn_enableCheck
        bn_checkLayout.addStretch()
        bn_checkLayout.addWidget(self.bn_enableCheck)
        
        bn_editLayout = QtWidgets.QHBoxLayout()
        bn_nameLabel = Q_LABEL('Input name : ')
        self.__labelWidgetList.append(bn_nameLabel)
        self.bn_basenameLine = InputLine(parent=self._parent)
        self.bn_basenameLine.address = {ad_t:'basename',ad_i:''}
        self.__textWidgetList.append(self.bn_basenameLine)
        bn_editLayout.addWidget(bn_nameLabel)
        bn_editLayout.addWidget(self.bn_basenameLine)
        
        bn_numberingLayout = QtWidgets.QHBoxLayout()
        self.startNumLine  = InputLine(editText=False,parent=self._parent)
        self.paddingLine   = InputLine(editText=False,parent=self._parent)
        self.stepLine      = InputLine(editText=False,parent=self._parent)
        self.startNumLine.address = {ad_t:'start'  ,ad_i:'1'}
        self.paddingLine.address  = {ad_t:'padding',ad_i:'1'}
        self.stepLine.address     = {ad_t:'step'   ,ad_i:'1'}
        self.__textWidgetList.append(self.startNumLine)
        self.__textWidgetList.append(self.paddingLine)
        self.__textWidgetList.append(self.stepLine)
        for x in (self.paddingLine,self.stepLine):
            x.setValidator(QtGui.QIntValidator())
        qlabelbuf = Q_LABEL('Start number')
        self.__labelWidgetList.append(qlabelbuf)
        bn_numberingLayout.addWidget(qlabelbuf,2)
        bn_numberingLayout.addWidget(self.startNumLine,1)
        bn_numberingLayout.addSpacing(6)
        qlabelbuf = Q_LABEL('Padding')
        self.__labelWidgetList.append(qlabelbuf)
        bn_numberingLayout.addWidget(qlabelbuf,2)
        bn_numberingLayout.addWidget(self.paddingLine,1)
        bn_numberingLayout.addSpacing(6)
        qlabelbuf = Q_LABEL('Step')
        self.__labelWidgetList.append(qlabelbuf)
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
        self.__checkboxWidgetDict['regularExpression'] = self.rep_regexpCheck
        self.rep_enableCheck = QtWidgets.QCheckBox('Enable')
        self.rep_enableCheck.setChecked(True)
        self.__checkboxWidgetDict['replace'] = self.rep_enableCheck
        rep_checkLayout.addStretch()
        rep_checkLayout.addWidget(self.rep_regexpCheck)
        rep_checkLayout.addWidget(self.rep_enableCheck)
        
        rep_formLayout       = QtWidgets.QFormLayout()
        self.rep_searchLine  = InputLine(parent=self._parent)
        self.rep_replaceLine = InputLine(parent=self._parent)
        self.rep_searchLine.address  = {ad_t:'search' ,ad_i:''}
        self.rep_replaceLine.address = {ad_t:'replace',ad_i:''}
        self.__textWidgetList.append(self.rep_searchLine)
        self.__textWidgetList.append(self.rep_replaceLine)
        qlabelbuf = Q_LABEL('Search  :')
        self.__labelWidgetList.append(qlabelbuf)
        rep_formLayout.addRow(qlabelbuf,self.rep_searchLine)
        qlabelbuf = Q_LABEL('Replace :')
        self.__labelWidgetList.append(qlabelbuf)
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
        self.__checkboxWidgetDict['prefixSuffix'] = self.ps_enableCheck

        ps_formLayout = QtWidgets.QFormLayout()
        _PSLIST       = [_PREFIX,_SUFFIX]
        for ps in _PSLIST:
            bufline = AdditionInputLine(parent=self._parent)
            
            # mainline
            buf = eval("bufline.getWidgetStateInfo('mainline')")
            buf.address = {ad_t:ps,ad_i:''}
            self.__textWidgetList.append(buf)
            
            # prefix & suffix line
            for ps2 in _PSLIST:
                # lineedit
                buf = eval(
                    "bufline.getWidgetStateInfo('{}_lineedit')".format(ps2))
                buf.address = {ad_t:'{}_{}'.format(ps,ps2),ad_i:None}
                self.__textWidgetList.append(buf)
                # checkbox
                buf = eval(
                    "bufline.getWidgetStateInfo('{}_checkbox')".format(ps2))
                self.__checkboxWidgetDict['{}_{}'.format(ps,ps2)] = buf
            
            labelbuf = Q_LABEL('{}{} :'.format(ps[0].upper(),ps[1:]))
            self.__labelWidgetList.append(labelbuf)
            ps_formLayout.addRow(labelbuf,bufline)
            
            # 可視化ラインの初期設定
            eval('bufline.getWidgetStateInfo("{}_checkbox")'
                    '.setChecked({})'.format(ps,False))
        
        presufLayout.addWidget(ps_title)
        presufLayout.addWidget(
            self.ps_enableCheck,alignment=QtCore.Qt.AlignRight)
        presufLayout.addLayout(ps_formLayout)
        
        ## --------------------------------------------------------------------
        ## view
        
        self._view = TreeView(self)
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
        ## all layout setting
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setContentsMargins(8,8,8,8)
        layout.addWidget(basenameFrame)
        layout.addWidget(replaceFrame)
        layout.addWidget(presufFrame)
        layout.addWidget(self._view)
        layout.addWidget(self.exeButton,alignment=QtCore.Qt.AlignCenter)
    
        ## --------------------------------------------------------------------
        ## post setting
        
        # lineEditの入力情報を初期化
        self.setLineEditInfo()
        
        # label
        [__labelStyle(x) for x in self.__labelWidgetList]
        
        # lineEdit
        for _t in self.__textWidgetList:
            _t.self = _t  
            _type   = _t.address['type']
            self._view.dictUpdate(_type,_t.text())
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
                print(u'>> InputLine/setExecuteMethodを実行できませんでした。')
                print
        
        # checkBox
        self._view.setCheckboxWidgetDict(self.__checkboxWidgetDict)
        for _c in self.__checkboxWidgetDict:
            self.__checkboxWidgetDict[_c].toggled.connect(
                self._view.cbListUpdate)
            __checkBoxStyle(self.__checkboxWidgetDict[_c])       
        
        self._view.headerResize()
        
    ## --------------------------------------------------------------------
    ## event
    
    def resizeEvent(self,event):
        r"""
            リサイズされた際のイベント
        """
        super(Renamer,self).resizeEvent(event)
        self.buttonResized(event)
    
    def exeCloseEventFunc(self):
        r"""
            close時に実行するメソッドのクッション関数（親のcloseEventで実行）
        """
        # 入力時メインGUIを閉じた際suggestViwを終了する
        _SV.exeHide()
        
    def mouseMoveEvent(self,event):
        r"""
            移動時のイベント動作
        """
        super(Renamer,self).mouseMoveEvent(event)
        _VM_.getVariable('nowFocusLineEdit').moveGui()
        
    ## --------------------------------------------------------------------
    ## setting
    
    def preSetting(self):
        r"""
            __init__設定時の動作をbuildUIで先行して行うための関数
        """
        # AppData/Roaming/msAppTools/<FILENAME>までのパスを設定
        _SPSL.setSeriesPath(_SPSL.getSaveEachUiPrefPath())
    
    def setLineEditInfo(self):
        r"""
            ラインエディットの入力情報をセット
            外部のウィジェットでも実行するため関数化
        """
        ([_t.setText(_t.text() if _t.address['initialize']==None
            else _t.address['initialize']) for _t in self.__textWidgetList])
    
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
        
    ## --------------------------------------------------------------------
    ## func

###############################################################################
## END
