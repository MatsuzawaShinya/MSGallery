#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    クリップボードに保存されているデータを
    入力されているラインパスに書き出すツール
"""
###############################################################################
## base lib

import os
import re
import sys
import json
import time
import base64
import traceback

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from . import func as fc
from ... import settings as st
from msAppTools.settingFiles import systemGeneral as sg

QtWidgets,QtCore,QtGui = sg.QtWidgets,sg.QtCore,sg.QtGui
_ck               = fc._ck
_startColumn      = fc._startColumn
_menuMaxLimit     = fc._menuMaxLimit
_path             = fc._path
_estimation       = fc._estimation
_startupPath      = fc._startupPath
_optionWidget     = fc._optionWidget
_startupLimitTime = fc._startupLimitTime
_epd              = fc._epd
_SPSL             = fc._SPSL

###############################################################################
## sub func

###############################################################################
## sub class

class OptionInfoData(sg.sgwidget.OptionInfoMasterdataClass):
    r"""
        オプションデータ総括クラス
    """
    def __init__(self,parentWidget=None,masterObject=None):
        r"""
            変数の初期設定
        """
        super(OptionInfoData,self).__init__(parentWidget,masterObject)
        
    def setDict(self):
        r"""
            オプションウィジェットベースデータ（オーバーライド）
        """
        self.data = {
            '010,lineNums':{
                'widget':{
                    'name':'QSpinBox',
                },
                'attribute':{
                    'setValue':3,
                    'setRange':(1,99),
                },
                'attribute1':{
                    'setToolTip':u'作成されるラインカラムの数',
                },
            },
            '020,extension':{
                'widget':{
                    'name':'QComboBox',
                },
                'attribute':{
                    'addItems':['jpg','png'],
                },
                'attribute1':{
                    'setCurrentIndex':1,
                    'setToolTip':'出力拡張子の初期設定',
                },
            },
        }
        
###############################################################################

class MenuListView(sg.ListView):
    r"""
        専用リストビューカスタマイズ
    """
    def __init__(self,parent=None):
        r"""
            初期設定
        """
        super(MenuListView,self).__init__(parent)
        self.setAlternatingRowColors(False)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.selfObj        = None
        self._saveSuggest   =  ''
        self._saveStartTime = 0.0
        self._saveEndTime   = 0.0
        
    ## ------------------------------------------------------------------------
    ## setting
    
    def setSelfObj(self,obj):
        r"""
            親オブジェクト格納
        """
        self.selfObj = obj
        
    def getSelfObj(self):
        r"""
            親オブジェクト取得
        """
        return self.selfObj
        
    ## ------------------------------------------------------------------------
    ## event
    
    def mousePressEvent(self,event):
        r"""
            メニュー項目をマウスで押したときのイベント
        """
        super(MenuListView,self).mousePressEvent(event)
        # self.setSpinboxFocus()
    
    def keyPressEvent(self,event):
        r"""
            キープレスイベント
        """
        super(MenuListView,self).keyPressEvent(event)
        
        key   = self.getKeyType(event)
        mask  = self.getKeyMask()
        mask2 = self.getKeyMask2()
        if key['press'] in ['Del','Backspace']:
            self.removeMenuItem()
        elif key['press'] in ['Up','Down']:
            self.moveCurrentIndexUpdate()
        elif key['press'] in ['Right']:
            self.setSpinboxFocus()
            
    ## ------------------------------------------------------------------------
    ## func
        
    def nowSelect(self):
        r"""
            選択しているアイテムインデックスのリターン
        """
        try:
            return self.selectionModel().selectedIndexes()
        except:
            return []
    
    def nowSelectItem(self):
        r"""
            選択しているアイテムリストのリターン
            
            Returns:
                any:
        """
        return [x.data() for x in self.nowSelect()]
    
    def removeItem(self,index=0):
        r"""
            アイテムの削除
        """
        model = self.model()
        model.removeRow(index,QtCore.QModelIndex())
    
    def getSelectItemRow(self,sorted=True):
        r"""
            選択アイテムのリターン(row)
        """
        _L = [s for s in self.selectedIndexes()]
        _L = list(set(_L))
        _L.sort(reverse=sorted)
        return _L
    
    def removeMenuItem(self):
        r"""
            選択アイテムの削除
        """
        for x in self.getSelectItemRow():
            obj  = self.getSelfObj()
            dict = obj.getNowData()[0]
            list = obj.getNowData()[1]
            self.removeItem(x.row())
            try:
                del dict[list[x.row()][0]]
            except:
                pass
            finally:
                obj.setNowData(dict)
    
    def moveCurrentIndexUpdate(self):
        r"""
            ↑↓キーを押した際のリストアップデート
        """
        self.getSelfObj().menuValueReflect()
    
    def connectFocusWidget(self,widget):
        r"""
            メニューと連携してフォーカスを当てるウィジェットをセット
        """
        self.__focuswidget = widget
    
    def setSpinboxFocus(self):
        r"""
            メニューを選択された際に実行されるフォーカスセットメソッド
        """
        self.__focuswidget.setFocus()
    
class SpinBox(QtWidgets.QSpinBox):
    r"""
        QSpinBox拡張クラス
    """
    KEYMETHOD = sg.KeyMethod()
    
    def __init__(self,parent=None):
        r"""
        """
        super(SpinBox,self).__init__(parent)
    
    ## ------------------------------------------------------------------------
    ## event
    
    def keyPressEvent(self,event):
        r"""
           ←→キーでウィジェットを行き来するキーイベント設定
        """
        super(SpinBox,self).keyPressEvent(event)
        
        _key   = self.KEYMETHOD._keyType(event)
        _mask  = self.KEYMETHOD._keyMask()
        _mask2 = self.KEYMETHOD._keyMask2()
        
        if _key['press'] in ('Left'):
            self.setListMenuFocus()
    
    ## ------------------------------------------------------------------------
    ## func
    
    def connectFocusWidget(self,widget):
        r"""
            メニューと連携してフォーカスを当てるウィジェットをセット
        """
        self.__focuswidget = widget
    
    def setListMenuFocus(self):
        r"""
            メニューを選択された際に実行されるフォーカスセットメソッド
        """
        self.__focuswidget.setFocus()
        
###############################################################################
    
class PrefSettingWidgetMain(sg.ScrolledWidget):
    r"""
        prefセッティング構成メイン部分
    """
    def __init__(self,parent=None):
        r"""
        """
        self.saveDict = None
        self.sortList = None
        self.__nowSelectMenuItem  = None
        self.__separator          = ':'
        self.__updateJsonDataDict = {}
        
        # buildUI/実行
        super(PrefSettingWidgetMain,self).__init__(parent)
        
        # _SPSL.getJsonEstimationData('ui')で取得し
        # setUpdateJsonData('ui')とsetNowDataにセットする際は別々に関数を
        # 実行しセットする。(変数に代入すると同一の扱いで数値が同期してしまう
        _SPSL.setBeforeEstimationInfo()
        self.setNowData(_SPSL.getJsonEstimationData('ui'))
        self.menuUpdate()
        
    def buildUI(self,parent=None):
        r"""
            レイアウトのオーバーライド用関数
        """
        self.setStyleSheet(
            '*{background-color:#333;}'
            'QLabel{color:#EEE;}'
            'QSpinBox,QPushButton{color:#EEE;background-color:#666;}'
            'QListView{color:#EEE;background-color:#444;}'
        )
        self.layout  = QtWidgets.QVBoxLayout(parent)
        two_layout   = QtWidgets.QHBoxLayout()
        left_layout  = QtWidgets.QVBoxLayout()
        right_layout = QtWidgets.QVBoxLayout()
        
        # left
        self.menuList = MenuListView()
        self.menuList.pressed.connect(self.menuValueReflect)
        self.menuList.setSelfObj(self)
        left_layout.addWidget(self.menuList)
        
        # right
        self.menuName  = QtWidgets.QLabel('')
        self.menuName.setStyleSheet('QLabel{background-color:#181818;}')
        self.menuName.setContentsMargins(2,2,2,2)
        self.menuValue = SpinBox()
        self.menuValue.setMaximum(99999)
        self.menuValue.valueChanged.connect(self.spinBoxChanged)
        refresh_btn    = QtWidgets.QPushButton('refresh')
        remove_btn     = QtWidgets.QPushButton('remove')
        update_btn     = QtWidgets.QPushButton('update')
        update_btn.setStyleSheet('QPushButton{background-color:#393;}')
        right_layout.addWidget(QtWidgets.QLabel('Menu name :'))
        right_layout.addWidget(self.menuName)
        right_layout.addWidget(QtWidgets.QLabel('Menu count :'))
        right_layout.addWidget(self.menuValue)
        right_layout.addStretch()
        right_layout.addWidget(refresh_btn)
        right_layout.addWidget(remove_btn)
        right_layout.addWidget(update_btn)

        two_layout.addLayout(left_layout ,5)
        two_layout.addLayout(right_layout,4)
        self.layout.addLayout(two_layout)
        
        refresh_btn.clicked.connect(self.menuUpdate_fromBtn)
        remove_btn.clicked.connect (self.removeMenuItem)
        update_btn.clicked.connect (self.updateJsonData)
        
        # add
        self.menuList.connectFocusWidget(self.menuValue)
        self.menuValue.connectFocusWidget(self.menuList)
    
    ## ------------------------------------------------------------------------
    ## setting func
    
    def setNowData(self,dict):
        r"""
            辞書データを正規化しセット
        """
        self.saveDict = dict
        self.sortList = sorted(
            self.saveDict.items(),reverse=True,key=(lambda x:x[1]))

    def getNowData(self):
        r"""
            辞書データを取得
        """
        return [self.saveDict,self.sortList]
    
    def updateJsonData(self):
        r"""
            辞書内容を反映保存
        """
        savedict_master = _SPSL.getJsonEstimationData('master')
        savedict_ui     = _SPSL.getJsonEstimationData('ui')
        first_d = _SPSL.getUpdateJsonData().get('before').get('ui')
        end_d   = self.getNowData()[0]
        
        # 重複/削除キーを取得
        intersection_keys         = first_d.keys() & end_d.keys()
        symmetric_difference_keys = first_d.keys() ^ end_d.keys()
        
        for key in first_d.keys():
            f_value = first_d.get(key)
            e_value = end_d.get(key)
            
            # 削除されたキーアイテムの処理
            if key in symmetric_difference_keys:
                e_value = 0
                del savedict_ui[key]
            # 重複(値が変更された場合)の処理
            elif key in intersection_keys:
                savedict_ui.update({key:e_value})
            else:
                raise RuntimeError(
                    u'!! Abnormal key detected <{}> !!'.format(key))
            
            cal_result = (e_value - f_value)
            
            # 数値に変動がなければスキップ
            if f_value == e_value:
                continue
            m_value = savedict_master.get(key)
            if not m_value or not isinstance(m_value, int):
                continue
            
            cal_val = (m_value + cal_result)
            savedict_master.update({key:cal_val})
            
            print(u'<{}> Difference value ({})'.format(key,cal_result))
            print(u'\tMaster {} -> {}'.format(m_value,cal_val))
            print(u'\tUI     {} -> {}'.format(f_value,e_value))
            print()
        
        _SPSL.setJsonEstimationData(savedict_master,savedict_ui)
        
        # 実行したら初期に格納した辞書データを更新
        _SPSL.setBeforeEstimationInfo()
    
    def menuUpdate_fromBtn(self):
        r"""
            ボタンからのメニューアップデート
        """
        self.setNowData(_SPSL.getJsonEstimationData('ui'))
        self.menuUpdate()
    
    def menuUpdate(self):
        r"""
            Listのアップデート
        """
        model = self.menuList.model()
        model.removeRows(0,model.rowCount())
        rootItem = model.invisibleRootItem()
        
        for s in self.getNowData()[1]:
            item = QtGui.QStandardItem('{}{}{}'.format(
                s[0],self.__separator,s[1]))
            rootItem.setChild(rootItem.rowCount(),0,item)
        
    def menuValueReflect(self):
        r"""
            選択リストの初期設定数をボックスに反映
        """
        nowmenu = self.menuList.nowSelect()
        nowstr  = self.menuList.nowSelectItem()
        if not nowstr or not nowmenu or nowstr[0] is None:
            return
        sp = nowstr[0].split(self.__separator)
        self.menuName.setText(str(sp[0]))
        self.menuValue.setValue(int(sp[1]))
        self.menuList.setCurrentIndex(nowmenu[0])
    
    def removeMenuItem(self):
        r"""
            選択リストアイテムの削除
        """
        self.menuList.removeMenuItem()
    
    def spinBoxChanged(self,value):
        r"""
            スピンボックスからの変更関数
        """
        # 選択アイテムの取得
        data = self.menuList.nowSelectItem()
        if not data:
            return
        
        # data[0] = None だった場合,マスター変数から値を取得し
        # それ以外(初回起動時など)はマスター変数に格納されている情報を代入
        if not data[0]:
            data = self.__nowSelectMenuItem
        else:
            self.__nowSelectMenuItem = data
        
        menudict    = self.getNowData()[0]
        # 選択位置の取得(※このタイミングで実行すること！)
        nowmenu     = self.menuList.nowSelect()
        newDataName = (data[0].split(self.__separator)[0]
            if data and not data[0] is None else '')
        
        # 変更した値で辞書を更新
        if newDataName:
            menudict.update({newDataName:value})
            self.setNowData(menudict)
        menuList = self.getNowData()[1]
        self.menuUpdate()
        
        # 変更した後リストが移動する可能性があるので
        # 選択のインデックス位置を合わせる
        if not nowmenu:
            return
        nowindex = nowmenu[0].row()
        setIndex = nowindex
        for i,m in enumerate(menuList):
            if newDataName==m[0]:
                if not i==nowindex:
                    setIndex = i
                    break
                break
        self.menuList.setCurrentIndex(
            self.menuList.model().createIndex(setIndex,0))
    
###############################################################################
    
class PrefSettingWidget(sg.EventBaseWidget):
    r"""
        prefセッティングウィジェット
    """
    def __init__(self,parent=None):
        r"""
            メインウィジェット全体設定
        """
        super(PrefSettingWidget,self).__init__(parent)
        
        c_pos = QtGui.QCursor().pos()
        w,h,offset    = 280,240,10
        self.wincolor = [48,32,64,232]
        self.setGeometry((c_pos.x()-(offset*4)),(c_pos.y()-(offset*2)),w,h)
        self.setAcceptDrops(False)
        self.setWindowFlags(sg._setWindowFlagsDict['tophint=True'])
        
        main = PrefSettingWidgetMain()
        
        we = sg.WidgetEventAction()
        we.setTitle(self.__class__.__name__)
        we.setHide(['-m','-o'])
        we.setWidget()
        we.setSelf(self)
        we.t.setStyleSheet(
            'QLabel{font-family:GEORGIA;font-size:13px;color:#FFF;}'
        )
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(we.getWidget())
        self.layout.addWidget(main)
    
    def keyPressEvent(self,event):
        r"""
            キープレスイベント
        """
        super(PrefSettingWidget,self).keyPressEvent(event)
        
###############################################################################
        
class EditNameWidget(sg.EventBaseWidget):
    r"""
        書き出すイメージファイルネームの編集用ウィジェット
    """   
    def __init__(self,object=None,parent=None):
        r"""
            メインウィジェット
        """
        super(EditNameWidget,self).__init__(parent)
        
        self._PSW = None
        
        self.line_num    = -1
        self.saveKeyInfo = []
        self.saveEndInfo = ['F12','F12','F12']
        self.saveStartTime = 0.0
        
        c_pos = QtGui.QCursor().pos()
        w,h,offset = 200,120,40
        self.setObject(object)
        self._fe = object._feDict
        self._ext,self._name  = '',''
        self.wincolor = [32,64,64,232]
        self.setGeometry((c_pos.x()-offset),(c_pos.y()-offset),w,h)
        self.setAcceptDrops(False)
        self.setWindowFlags(sg._setWindowFlagsDict['tophint=True'])
        self.baseRect = (self.rect().width(),self.rect().height())
        
        self.we = sg.WidgetEventAction()
        self.we.setTitle('Edit name')
        self.we.setCloseTime(100)
        self.we.setHide('minimize')
        self.we.setHide('-o')
        self.we.setWidget()
        self.we.setSelf(self)
        self.we.t.setStyleSheet(
            'QLabel{font-family:GEORGIA;font-size:13px;color:#FFF;}')
        
        self.__layoutList = []
        self.__cbList = []
        self.__leList = []
        for i,nea in enumerate(object._nameEditAttr):
            L_BUF = QtWidgets.QHBoxLayout()
            C = QtWidgets.QCheckBox('')
            C.address = (i,nea[0])
            C.setChecked(self._fe['{}{}'.format(nea[0],_ck)])
            L = QtWidgets.QLabel(nea[0])
            L.setStyleSheet('QLabel{color:#FFF;}')
            E = QtWidgets.QLineEdit(self._fe[nea[0]])
            E.address = (i,nea[0])
            E.textEdited.connect(self.textChange) # Old → E.textChanged.connect
            E.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            E.customContextMenuRequested.connect(self.estimationAllMenu)
            L_BUF.addWidget(C,1)
            L_BUF.addWidget(L,3)
            L_BUF.addWidget(E,6)
            self.__cbList.append(C)
            self.__leList.append(E)
            self.__layoutList.append(L_BUF)
            
        filePrefixLayout = QtWidgets.QHBoxLayout()
        self.prefixCB = QtWidgets.QCheckBox(' Prefix number files')
        self.prefixCB.setStyleSheet('QCheckBox{color:#FFF;}')
        self.prefixCB.toggled.connect(self.paddingChange)
        self.prefixPadding = QtWidgets.QLineEdit('4')
        self.prefixPadding.setValidator(QtGui.QIntValidator())
        filePrefixLayout.addWidget(self.prefixCB)
        filePrefixLayout.addWidget(self.prefixPadding)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.we.getWidget())
        ([self.layout.addLayout(x) for x in self.__layoutList])
        self.layout.addLayout(filePrefixLayout)
        
        self.setting()
        self._SV = sg.SuggestView()
        self._SV.exeHide()
        self._SV.setSuggestInsert(self.suggestInsert)
        
        # 指定キー判定用クラスを呼び出し
        self._SKLJ = sg.SpecifiedKeyLimitJudgment(
            self.saveEndInfo,_startupLimitTime)
        
    ## ------------------------------------------------------------------------
    ## setting
    
    def setting(self):
        r"""
            初期設定
        """
        obj = self.getObject()
        fd  = obj._feDict
        for i,n in enumerate(obj._nameEditAttr):
            self.__leList[i].setText(fd[n[0]])
            self.__cbList[i].setChecked(fd['{}{}'.format(n[0],_ck)])
        pa  = obj._paddingAttr
        self.prefixPadding.setText(str(fd[pa[0]]))
        self.prefixCB.setChecked(fd['{}{}'.format(pa[0],_ck)])
        
    def setObject(self,object):
        r"""
            オブジェクト格納変数
        """
        self._object = object
        
    def getObject(self):
        r"""
            オブジェクト変数のリターン
        """
        return self._object
    
    ## ------------------------------------------------------------------------
    ## event
    
    def mouseDoubleClickEvent(self,event):
        r"""
            ダブルクリックのイベント
        """
        self.inputInitialize()
        self.allReflect()
    
    def keyPressEvent(self,event):
        r"""
            キープレス時のイベント情報
        """
        _key  = self.getKeyType(event)
        _mask = self.getKeyMask()
        
        if _key['press'] in ['Esc']:
            self.we.setCloseTimeElapsed()
            self._SKLJ.resetSaveKey()
        elif _key['mod1'] == _mask['ctrl,shift']:
            if _key['press'] in ('F12',):
                if len(self._SKLJ.getSaveKey())==0:
                    self._SKLJ.setStartTime()
                self._SKLJ.addSaveKey(_key['press'])
        elif _key['press'] in ['Up','Down','Left','Right']:
            if not self._SV.isHidden():
                self._SV.keyPressEvent(event)
        elif _key['press'] in ['Enter','Return']:
            self.suggestInsert()
        else:
            self._SKLJ.resetSaveKey()
            
        if self._SKLJ.judgmentSaveKey():
            if self._SKLJ.judgmentLimitTime():
                if self._PSW:
                    fc.closedGui(self._PSW)
                self._PSW = PrefSettingWidget()
                self._PSW.show()
            self._SKLJ.resetSaveKey()
            
    def closeEvent(self,event):
        r"""
            ウィジェットを閉じた際の動作（オーバーライド）
        """
        fc.closedGui(self._SV)
        fc.closedGui(self._PSW)
        
    def mouseMoveEvent(self,event):
        r"""
            移動時のイベント動作
        """
        super(EditNameWidget,self).mouseMoveEvent(event)

        # Edit nameを移動時にサジェストも一緒についてくる設定
        self.moveGui(self.__leList[self.line_num])

    ## ------------------------------------------------------------------------
    ## get
    
    def getValueCB(self,index):
        r"""
        """
        try:
            return self.__cbList[index].isChecked()
        except:
            return None
            
    def getValueLE(self,index):
        r"""
        """
        try:
            return self.__leList[index].text()
        except:
            return None
    
    def getWidgetPositionInfo(self,widget):
        r"""
            ウィジェット／カーソル情報を返す
        """
        cursor_pos    = self.mapToGlobal(widget.cursorRect().bottomRight())
        lineedit_post = self.mapToGlobal(widget.pos())
        return [cursor_pos,lineedit_post]
    
    ## ------------------------------------------------------------------------
    ## func
    
    def allReflect(self):
        r"""
            反映メソッドの集約
        """
        self.nameReflect()
        self.textReflect()
    
    def textReflect(self):
        r"""
            エディットラインテキストの設定を文字として反映する
        """
        obj = self.getObject()
        fd  = obj._feDict
        
        _during = []
        for i,x in enumerate(obj._nameEditAttr):
            _t = self.getValueLE(i)
            _during.append(_t)
            fd.update({x[0]:_t})
            fd.update({'{}{}'.format(x[0],_ck):self.getValueCB(i)})
        pa = obj._paddingAttr
        pp = self.prefixPadding
        
        if pp.text():
            _t = pp.text()
            fd.update({pa[0]:int(9 if int(_t) > 9 else _t)})
            _during.append(_t)
        else:
            n = obj._paddingAttr[1]
            fd.update({pa[0]:n})
            pp.setText(str(n))
            
        fd.update({'{}{}'.format(pa[0],_ck):self.prefixCB.isChecked()})
        txt = ('"{}"'.format('/'.join(_during))
            if len([True for x in self.__cbList if x.isChecked()]) else '')
        obj.putLabel.setText(txt)
    
    def nameReflect(self):
        r"""
            エディットラインの設定を更新し反映する
        """
        obj = self.getObject()
        obj.nameEditReflect()
    
    def textChange(self,text='',line=-1,menuFlag=True,suggestFlag=True):
        r"""
            テキスト変更時の動作
        """
        try:
            self.line_num = self.sender().address[0]
        except:
            if line<0:
                self.line_num = line
        
        SC = self.__cbList[self.line_num].setChecked
        SC(True if len(self.__leList[self.line_num].text()) else False)
        
        c = len(self.__leList[1].text())
        p = len(self.__leList[2].text())
        s = len(self.__leList[3].text())
        
        # prefix/suffix設定時の動作
        if not p and not s:
            self.__cbList[1].setChecked(False)
        if p or s:
            self.__cbList[1].setChecked(True)
            
        # connect設定時の動作
        # self.__cbList[1].setChecked(True if c else False)
        
        self.allReflect()
        
        if menuFlag:
            self.estimationMenu(self.sender())
        if suggestFlag:
            self._SV.setTextLineWidget(self.__leList[self.line_num])
            self._SV.setSuggestItemList(sorted(
                _SPSL.getJsonEstimationData('sum').items(),
                reverse=True,key=(lambda x:x[1])))
            self._SV.eachMovePositioning(self.moveGui)
            self._SV.suggestSetting()
    
    def suggestInsert(self):
        r"""
            サジェスト(Enter/Return)時の動作
        """
        self._SV.suggestInsert()
        # 入力されたテキスト情報をメインUIへ更新する
        self.allReflect()
            
    def estimationAllMenu(self):
        r"""
            予測変換の標準右クリックメニュー：一覧
        """
        saveDict = _SPSL.getJsonEstimationData('sum')
        sortList = sorted(saveDict.items(),reverse=True,key=(lambda x:x[1]))

        menu = QtWidgets.QMenu()
        for i,s in enumerate(sortList):
            if i>=_menuMaxLimit:
                break
            m = menu.addAction(s[0],self.estimationAllExecute)
            m.nodename = s[0]
            m.address  = self.sender().address
        menu.exec_(QtGui.QCursor.pos())
    
    def estimationAllExecute(self):
        r"""
            予測変換の標準右クリックメニュー：実行
        """
        s = self.sender()
        self.__leList[s.address[0]].setText(s.nodename)
        self.textChange(suggestFlag=False)
    
    def estimationMenu(self,selfobj):
        r"""
            予測変換の標準右クリックメニュータイプ式：一覧(現在隠しコマンドに)
        """
        saveDict = _SPSL.getJsonEstimationData('sum')
        sortList = (sorted(saveDict.items(),reverse=True,key=(lambda x:x[1]))
            if saveDict else [])
        
        if (QtWidgets.QApplication.keyboardModifiers()==QtCore.Qt.AltModifier):
            menu = QtWidgets.QMenu()
            for s in sortList:
                if not re.search('^%s'%(
                        self.getValueLE(selfobj.address[0])),s[0]):
                    continue
                m = menu.addAction(s[0],self.estimationExecute)
                m.nodename = s[0]
                m.selfobj  = selfobj
            menu.exec_(QtGui.QCursor.pos())
    
    def estimationExecute(self):
        r"""
            予測変換の標準右クリックメニュータイプ式：実行
        """
        s = self.sender()
        s.address = s.selfobj.address
        self.__leList[s.selfobj.address[0]].setText(s.nodename)
    
    def paddingChange(self):
        r"""
            padding変更時の動作
        """
        ck = self.prefixCB.isChecked()
        if (ck == False and
            (self.__cbList[2].isChecked() or self.__cbList[3].isChecked())
        ): return
        self.__cbList[1].setChecked(ck)
        self.allReflect()
            
    def inputInitialize(self):
        r"""
            入力情報の初期化
        """
        obj = self.getObject()
        fd  = obj._feDict
        for i,nea in enumerate(obj._nameEditAttr):
            self.__leList[i].setText(nea[1])
            self.__cbList[i].setChecked(nea[2])
        pa = obj._paddingAttr
        self.prefixPadding.setText(str(pa[1]))
        self.prefixCB.setChecked(pa[2])
        
        # connect checkは全てを初期化した後に再設定
        self.__cbList[1].setChecked(obj._nameEditAttr[1][2])
    
    def moveGui(self,lines):
        r"""
            ウィジェット位置調整(SuggestViewでも実行)
        """
        cursor_pos,lineedit_post = self.getWidgetPositionInfo(lines)
        print(lines,cursor_pos,lineedit_post)
        self._SV.move(
            # 横位置調整
            (cursor_pos.x()-(cursor_pos.x()-lineedit_post.x()+(-110))+
                # ウィジェット横位置サイズに合わせた微調整
                ((self.rect().width()-self.baseRect[0])*0.6)),
            # 縦位置調整
            (cursor_pos.y()-(cursor_pos.y()-lineedit_post.y()+(+0)))
        )
        
###############################################################################
    
class ExportLineWidget(QtWidgets.QWidget):
    r"""
        エクスポートパーツ収納クラス
    """
    KEYMETHOD = sg.KeyMethod()
    _KEYMOVEPATHLIST = []
    
    def __init__(self,object=None,parent=None):
        r"""
            メインレイアウトクラス
        """
        super(ExportLineWidget,self).__init__(parent)
            
        self.setObject(object)
        self.bw_size   = 24
        self.exportExt = 'jpg'
        self.buttonGrpList   = []
        self._nameEditAttr   = []
        self._paddingAttr    = []
        self.__firstDropSave = ''
        self.__nameEditInfo  = {}
        self.setAttribute(QtCore.Qt.WA_StyledBackground,True)
        self.setAcceptDrops(True)
        
        h_layout         = QtWidgets.QHBoxLayout()
        self.pathLine    = QtWidgets.QLineEdit('')
        self.resultText  = QtWidgets.QLabel('')
        self.resultText.setStyleSheet('QLabel{color:#FFF;}')
        
        self.resetButton = QtWidgets.QPushButton('R')
        self.resetButton.setMaximumWidth(self.bw_size)
        self.resetButton.clicked.connect(self.resetPath)
        self.buttonGrpList.append(self.resetButton)
        
        self.upButton    = QtWidgets.QPushButton('U')
        self.upButton.setMaximumWidth(self.bw_size)
        self.upButton.clicked.connect(self.dirnamePath)
        self.buttonGrpList.append(self.upButton)
        
        self.expButton   = QtWidgets.QPushButton('exp')
        self.expButton.setMaximumWidth(self.bw_size*2)
        self.expButton.clicked.connect(self.exportImage)
        self.expButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.expButton.customContextMenuRequested.connect(
            self.exportImageSubMenu
        )
        self.buttonGrpList.append(self.expButton)
        
        h_layout.addWidget(self.pathLine)
        h_layout.addWidget(self.resultText)
        h_layout.addWidget(self.resetButton)
        h_layout.addWidget(self.upButton)
        h_layout.addWidget(self.expButton)
    
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(h_layout)
        
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
        mime = event.mimeData()
        path = mime.urls()
        for p in path:
            text = _fc(p.toLocalFile())
            self.pathLine.setText(text)
            self.__firstDropSave = text
            
    def keyPressEvent(self,event):
        r"""
            キープレス時のイベント情報
        """
        _key   = self.KEYMETHOD._keyType(event)
        _mask  = self.KEYMETHOD._keyMask()
        _mask2 = self.KEYMETHOD._keyMask2()
        
        if   _key['press'] in ('F1','F2'):
            self.keyMoveSetPath(_key['press'])
        elif _key['press'] in ('Up','Down'):
            self.keyMoveChangePath(_key['press'])
        elif _key['press'] in ('Return','Enter'):
            self.exportImage()
        elif _key['mod1']==_mask2(['ctrl']) and _key['press'] in ['O']:
            self.openDir()
        
    ## ------------------------------------------------------------------------
    ## setting
    
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
        
    def setNameEdit(self,d):
        r"""
            nameEdit情報の格納
        """
        self.__nameEditInfo = d
    
    def getNameEdit(self):
        r"""
            nameEdit情報のリターン
        """
        return self.__nameEditInfo
    
    def setKeyMovePath(self,list):
        r"""
            keyPathが変更されたら更新する用の関数
        """
        self._KEYMOVEPATHLIST = list
        try:
            obj._KEYMOVEPATHLIST.sort()
        except:
            pass
    
    ## ------------------------------------------------------------------------
    ## func
    
    def setFirstPath(self,p):
        r"""
            ファーストパスセット
        """
        self.__firstDropSave = p
        
    def getFirstPath(self):
        r"""
            ファーストパス取得
        """
        return self.__firstDropSave
    
    def resetPath(self):
        r"""
            ドロップ時のパスを再セットする
        """
        self.pathLine.setText(self.getFirstPath())
    
    def dirnamePath(self):
        r"""
            パスを一つ階層を上がった階層にセットする
        """
        self.pathLine.setText(os.path.dirname(self.pathLine.text()))
    
    def openDir(self):
        r"""
            セットされているパスをエクスプローラーで開く
        """
        p = sg.toBasePath(self.pathLine.text())
        if os.path.isdir(p):
            sg.openExplorer(p)
    
    def setKeyPath(self):
        r"""
            起動時にkeyを読み込んでセットする
        """
        jsonPath = _SPSL.getPath()
        if not os.path.isfile(jsonPath):
            print('+ Not json path. {}'.format(jsonPath))
            return
        d = _SPSL.getJsonFile()
        saveDict = d.get(_path)
        
        obj = self.getObject()
        obj._KEYMOVEPATHLIST = saveDict[:] if saveDict else []
        obj._KEYMOVEPATHLIST.sort()
    
    def keyMoveSetPath(self,keyType=None):
        r"""
            現在セットされているパスをjsonに保存/削除する
        """
        def _putPrint():
            r"""
                save,remove時にラベルとして可視表示する
            """
            self.resultText.setText('save' if keyType == 'F1' else 'remove')
            QtCore.QTimer.singleShot(1000,(lambda:self.resultText.setText('')))
        
        d = _SPSL.getJsonFile()
        saveDict = d.get(_path)
        _saveBuf = saveDict[:] if saveDict else []
        txt_path = sg.toBasePath(self.pathLine.text())
        # save
        if keyType in ('F1',):
            if not txt_path in _saveBuf and not txt_path == '':
                _saveBuf.extend([txt_path])
                print('+ Save path.')
                print('  -> {}'.format(sg.toEncode(txt_path,'cp932')))
                _putPrint()
        # remove
        elif keyType in ('F2',):
            if txt_path in _saveBuf and txt_path:
                try:
                    _saveBuf.remove(txt_path)
                    print('+ Remove path.')
                    print('  -> {}'.format(txt_path))
                    _putPrint()
                except:
                    pass
        else:
            pass
        d[_path] = _saveBuf
        _SPSL.setDict(d)
        _SPSL.setJsonFile()
        obj = self.getObject()
        obj._KEYMOVEPATHLIST = _saveBuf[:]
        obj._KEYMOVEPATHLIST.sort()
        obj.keyReflect()
        self.setKeyPath()
        
    def keyMoveChangePath(self,keyType=None):
        r"""
            ↑↓キーを押した際に保存されているパスにスライドして切り替える
        """
        obj = self.getObject()
        jsonPath = _SPSL.getPath()
        if not os.path.isfile(jsonPath):
            print('+ Not found save json file.')
            print('  -> {}'.format(jsonPath))
            return
        if not obj._KEYMOVEPATHLIST:
            print('+ Nothing is saved.')
            return
        txt_path = sg.toBasePath(self.pathLine.text())
        try:
            if keyType == 'Up':
                limit = 0
                initi = (len(obj._KEYMOVEPATHLIST)-1)
                step  = -1
            else:
                limit = (len(obj._KEYMOVEPATHLIST)-1)
                initi = 0
                step  = 1
            INDEX = obj._KEYMOVEPATHLIST.index(txt_path)
            NEXT  = (obj._KEYMOVEPATHLIST[initi]
                        if limit == INDEX else
                    obj._KEYMOVEPATHLIST[INDEX+step])
        except:
            NEXT  = obj._KEYMOVEPATHLIST[0]
        self.pathLine.setText(str(NEXT))
        
    def exportImage(self,open=False):
        r"""
            イメージエクスポート関数
        """
        _updateExclusion = {}
        _d  = {}
        _nd = self.getNameEdit()
        _pa = self._paddingAttr

        for nea in self._nameEditAttr:
            _d[nea[0]] = _nd[nea[0]]  if _nd['{}{}'.format(nea[0],_ck)] else ''
            _updateExclusion[nea[0]] = nea[3]
        _d[_pa[0]] = str(_nd[_pa[0]]) if _nd['{}{}'.format(_pa[0],_ck)] else ''
        
        # image export
        path = sg.exportClipboradImage(
            path    = self.pathLine.text(),
            ext     = self.exportExt,
            opendir = open,
            **_d
        )
        
        rt_st = self.resultText.setText
        rt_st(st._resultText[0 if path  else 1])
        QtCore.QTimer.singleShot(st._vanishTime,(lambda:rt_st('')))
        
        # save名の回数をアップデート
        saveDict_master = _SPSL.getJsonEstimationData('master')
        saveDict_ui     = _SPSL.getJsonEstimationData('ui')
        
        printmsg = []
        for d in _d:
            # savedictフラグが0以下なら処理を回避
            exc  = _updateExclusion.get(d)
            if not exc or exc<1:
                continue
            word = _d[d]
            if word=='' or word=='_':
                continue
            
            # master,ui/それぞれの辞書に更新情報を反映
            printmsg.append(u'>> {}'.format(word))
            for type in ['master','ui']:
                targetdict = eval('saveDict_{}'.format(type))
                # 取得情報が空（初期状態）の場合は数値を初期値に設定する
                nownum  = targetdict.get(word) if targetdict else 0
                nextnum = (nownum + 1) if nownum else 1
                if targetdict:
                    targetdict.update({
                        word:(nextnum if word in targetdict else 1)})
                else:
                    targetdict = {word:nextnum}
                exec('saveDict_{}.update(targetdict)'.format(type))
                printmsg.append(
                            u'{}: {} -> {}'.format('  {: <7}'.format(type),
                            nownum,nextnum))
        print('\n'.join(printmsg))
                
        _SPSL.setJsonEstimationData(saveDict_master,saveDict_ui)
        
        STI = sg.SystemTrayIcon(1)
        STI.setTitle('Executed.')
        STI.setMsg(path if path else 'No export.')
        STI.setIcon(1)
        STI.showMsg()
    
    def exportImageSubMenu(self):
        r"""
            右クリックホップアップ用サブコマンド関数
            
            Returns:
                any:
        """
        sg.openExplorer(self.pathLine.text())
    
###############################################################################
    
class ImageExporter(sg.ScrolledWidget):
    r"""
        イメージエクスポートのメインUI
    """
    _addLineList  = {}
    # 0 : パーツ名
    # 1 : 初期設定文字
    # 2 : チェックボックスの初期フラグ
    # 3 : export時にsavedictするかどうか(1以上で設定)
    _nameEditAttr = (
        ['specify','' ,False,2],
        ['connect','_',False,0],
        ['prefix' ,'' ,False,1],
        ['suffix' ,'' ,False,1],
    )
    _paddingAttr = ['padding',4,False]
    _feDict = {}
    for nea in _nameEditAttr:
        _feDict[nea[0]] = nea[1]
        _feDict['{}{}'.format(nea[0],_ck)] = nea[2]
    _feDict[_paddingAttr[0]] = _paddingAttr[1]
    _feDict['{}{}'.format(_paddingAttr[0],_ck)] = _paddingAttr[2]
    
    _KEYMOVEPATHLIST = []
    
    def __init__(self,parent=None,masterDict=None):
        r"""
            初期設定
        """
        self.preSetting()
        super(ImageExporter,self).__init__(parent)
        self._dict = masterDict
        self._ENW  = None
        self._WEA  = None
        
    ## ------------------------------------------------------------------------
    ## common parent event setting
    
    def setEventPackage(self,packaging):
        r"""
            子と関連性をためのメソッドパッケージを親から引き継いで設定する
        """
        super(ImageExporter,self).setEventPackage(packaging)
        
        # 親eventと連動
        if packaging:
            packaging()['set']('closeEvent',self.exeCloseEventFunc)
    
    ## ------------------------------------------------------------------------
    ## build
    
    def buildUI(self,parent=None):
        r"""
            レイアウトのオーバーライド用関数
        """
        commandLayout = QtWidgets.QHBoxLayout()
        self.putLabel = QtWidgets.QLabel('')
        self.putLabel.setStyleSheet('QLabel{color:#FFF;}')
        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(st._imageExportExt)
        self.combo.setFixedWidth(60)
        self.combo.currentIndexChanged.connect(self.changedExt)
        addButton  = QtWidgets.QPushButton('+ add')
        addButton.clicked.connect(self.addLineWidget)
        addButton.setFixedWidth(60)
        addButton.setEnabled(True)
        commandLayout.addSpacing(2)
        commandLayout.addWidget(self.putLabel)
        commandLayout.addStretch()
        commandLayout.addWidget(self.combo)
        commandLayout.addWidget(addButton)
        
        self.layout = QtWidgets.QVBoxLayout(parent)
        self.layout.addLayout(commandLayout)
        ([self.addLineWidget() for i in range(0,_startColumn)])
        
    ## ------------------------------------------------------------------------
    ## setting
    
    def preSetting(self):
        r"""
            __init__設定時の動作をbuildUIで先行して行うための関数
        """
        # AppData/Roaming/msAppTools/<FILENAME>までのパスを設定
        _SPSL.setSeriesPath(_SPSL.getSaveEachUiPrefPath())

    ## ------------------------------------------------------------------------
    ## event
    
    def mouseDoubleClickEvent(self,event):
        r"""
            ダブルクリックのイベント
        """
        enw = EditNameWidget(self)
        if self._ENW:
            fc.closedGui(self._ENW)
        enw.show()
        self._ENW = enw
    
    ## ------------------------------------------------------------------------
    ## func
    
    def nameEditReflect(self):
        r"""
            nameEdit情報を各ウィジェットに反映する
        """
        for s in self._addLineList:
            self._addLineList[s].setNameEdit(self._feDict)
    
    def changedExt(self):
        r"""
            作られたウィジェット群に対し現在の設定拡張子をセットする
        """
        for s in self._addLineList:
            self._addLineList[s].exportExt = self.combo.currentText()
    
    def keyReflect(self):
        r"""
            キーパス情報を各ウィジェットに反映する
        """
        for s in self._addLineList:
            self._addLineList[s].setKeyMovePath(self._KEYMOVEPATHLIST)
        
    def exeCloseEventFunc(self):
        r"""
            close時に実行するメソッドのクッション関数（親のcloseEventで実行）
        """
        _D = _SPSL.getJsonFile()
        saveDict = _D.get(_startupPath)
        bufDict  = {}
        
        # 情報なし（初回起動）の場合は保存辞書を生成
        if not saveDict:
            _D[_startupPath] = {}
        for i in self._addLineList:
            index = str(i) 
            t = self._addLineList[i].pathLine.text()
            # 起動時のエラーを防ぐため日本語が混じっている場合は空文字を代入
            t = ('' if sg.threeByteWordCheck(t) else t)
            # t = '' if sg.threeByteWordCheck(t) else sg.toEncode(t)
            if not saveDict:
                bufDict[index] = t
            else:
                if not saveDict.get(index):
                    bufDict[index] = t
                else:
                    bufDict.update({index:t})
        _D[_startupPath] = bufDict
        _SPSL.setDict(_D)
        _SPSL.setBackup(True)
        _SPSL.setJsonFile()
        
        # msatema経由時は辞書情報が残るので初期化する
        self._addLineList.clear()
        fc.closedGui(self._ENW)
    
    def addLineWidget(self):
        r"""
            lineWidgetの作成関数
        """
        num = len(self._addLineList)
        
        c   = st._colorIndexList[self.layout.count()%2]
        new = ExportLineWidget(self)
        new._nameEditAttr = self._nameEditAttr
        new._paddingAttr  = self._paddingAttr
        new.setNameEdit(self._feDict)
        new.setKeyPath()
        new.setStyleSheet(
            'QWidget{background-color:%s;}'%(c[0])
        )
        new.pathLine.setStyleSheet(
            'QLineEdit{color:%s;background-color:%s;}'%(c[1],c[2])
        )
        ([b.setStyleSheet('QPushButton{color:%s;}'%(c[3]))
            for b in new.buttonGrpList])
        self.layout.addWidget(new)
        self._addLineList.update({len(self._addLineList):new})
        
        # saveされている[STARTUPPATH]のライン入力情報をセット
        D = _SPSL.getJsonFile()
        savedata = D.get(_startupPath)
        if savedata:
            # savedata = savedata.get(str(num))
            savedata = savedata.get(str(num))
            _s = (savedata if savedata else '')
            self._addLineList[num].pathLine.setText(_s)
            new.setFirstPath(_s)
    
    def setWeaOptionWidgetFromParent(self,wea):
        r"""
            親ウィジェットから送られてきたWidgetEventActionを
            格納するためのクッション関数で、更に自身のオブジェクト情報を
            親(__init__)を経由してWidgetEventActionに送り込む。
        """
        self._WEA = wea
        self._WEA.setWidgetChildrenObject(self)
    
    def setOptionWidgetChildrenData(self):
        r"""
            オプションウィジェットを取得しレイアウトウィジェットをセットする
        """
        wg = self._WEA.getOptionWidget()
        wg.setStyleSheet('QLabel{color:#FFF;}')
        wg.setPaintEventColor(64,64,128,222)
        w,h,p = 250,200,QtGui.QCursor().pos()
        wg.setGeometry((p.x()-(w*0.5)),(p.y()-20),w,h)
        
        # <OPTIONWIDGE>が無いor空の場合は辞書データを作成
        if not fc.getJsonOptionWidget():
            masterDict = _SPSL.getJsonFile()
            masterDict.update({_optionWidget:{}})
            _SPSL.setDict(masterDict)
            _SPSL.setJsonFile()
            print(u'+ Create <OPTIONWIDGET> json tag data.')
        
        OID = OptionInfoData(wg,self)
        OID.execute()
    
    def reflectWidgetDataToVariable(self,dictInfo):
        r"""
            OptionWidget/closeFuncでボタン実行される際に実行する
            おおもとの関数
        """
        masterDict = _SPSL.getJsonFile()
        masterDict.update({_optionWidget:dictInfo})
        _SPSL.setDict(masterDict)
        _SPSL.setJsonFile()
    
    ## ------------------------------------------------------------------------
    ## about
    
    def getAboutData(self):
        r"""
            about情報の取得
        """
        return fc.getAboutInfo()
        
###############################################################################
## END
