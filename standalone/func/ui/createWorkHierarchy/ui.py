#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    createWorkHierarchy/Explanation,ui
"""
###############################################################################
## base lib

import os
import re
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
_VM_  = sg.VariableManagement()
_COL_ = sg.ss.ColorStyleManagement()
SM    = fc.SubMethod()
SPSL  = st.StandalonePathStoreList(fc.getModuleName())

###############################################################################
## layout class

class WidgetPartsClass(QtWidgets.QWidget):
    r"""
        キャプションとウィジェットパーツをまとめて設定するクラス
    """
    def __init__(self,parent=None):
        r"""
        """
        super(WidgetPartsClass,self).__init__(parent)
        
        self.clearWidgetInfo()
        self.clearKeyListManagemnet()
        
    ## ------------------------------------------------------------------------
    ## setting func
    
    def clearWidgetInfo(self):
        r"""
            ウィジェット情報をすべてクリア
        """
        self.buildLayout = QtWidgets.QVBoxLayout()
        self.buildLayout.setSpacing(10)
        self.buildLayout.setContentsMargins(2,4,2,4)
        self.partsLayout = QtWidgets.QHBoxLayout()
        self.captionMsg  = ''

    def setCaption(self,msg='',padding=True):
        r"""
            キャプションを設定
        """
        self.captionMsg = '{}{}'.format((u'+ ' if msg and padding else ''),msg)
        
    def getCaption(self):
        r"""
            キャプションを取得
        """
        return self.captionMsg
    
    def setParamLayout(self,lay):
        r"""
            キャプション下のウィジェットを設定
        """
        try:
            self.partsLayout.addLayout(lay,lay.stretchValue)
        except:
            self.partsLayout.addLayout(lay)
        
    def getParamLayout(self):
        r"""
            キャプション下のウィジェットをレイアウトで取得
        """
        return self.partsLayout
    
    def clearKeyListManagemnet(self):
        r"""
            パラメータをキー指定で管理する変数の初期化
        """
        self.managementIndexList = {}
        
    def setKeyListManagemnet(self,key,param):
        r"""
            パラメータをキー指定でリスト管理する
        """
        list = self.managementIndexList.get(key)
        if not list:
            self.managementIndexList[key] = []
        self.managementIndexList[key].append(param)
    
    def getKeyListManagemnet(self,key):
        r"""
            インデックスを指定して情報を取得する
        """
        list = self.managementIndexList.get(key)
        return list if list else []
    
    ## ------------------------------------------------------------------------
    ## layout func
    
    def getBoxLayout(self,V=True):
        r"""
            True/QVBoxLayout,False/HBoxLayoutを返す
        """
        return QtWidgets.QVBoxLayout() if V else QtWidgets.QHBoxLayout()
    
    def setListToLayout(self,widgetList=[]):
        r"""
            レイアウトを格納したリストをHBoxLayoutに格納する
        """
        [self.setParamLayout(v) for v in widgetList]
    
    ## ------------------------------------------------------------------------
    ## execute func
    
    def exeBuildLayout(self):
        r"""
            設定したレイアウト情報を元にウィジェットを作成しレイアウトを取得
        """
        # label
        cap = self.getCaption()
        if cap:
            captionLabel = QtWidgets.QLabel(cap)
            self.buildLayout.addWidget(captionLabel)
        # widget
        self.buildLayout.addLayout(self.getParamLayout())

        return self.buildLayout

###############################################################################
## create tab

class CreateTabWidget(sg.ScrolledWidget):
    r"""
        createタブウィジェット
    """
    def __init__(self,parent=None):
        r"""
        """
        super(CreateTabWidget,self).__init__(parent)

    ## ------------------------------------------------------------------------
    ## build
    
    def buildUI(self,parent=None):
        r"""
            enter description
        """
        self.layout = QtWidgets.QVBoxLayout(parent)
        WPC = WidgetPartsClass()
        
        ## ------------------------------------------------
        ## ウィジェット/クラスの名前
        
        bufkey = 'createName'
        WPC.setCaption('Create widget/class name.')
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        VLAY.addWidget(QtWidgets.QLabel('Set name : '))
        VLAY.stretchValue = 3
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        bnl  = _VM_.setVariable('baseNameLine',QtWidgets.QLineEdit(''))
        bnl.textChanged.connect(self.refrectLineName)
        VLAY.addWidget(bnl)
        VLAY.stretchValue = 7
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.layout.addLayout(WPC.exeBuildLayout())
        self.addHorizonLine(self.layout)
        WPC.clearWidgetInfo()
        
        ## ------------------------------------------------
        ## Class name
        
        bufkey = 'writeClassName'
        WPC.setCaption('Write json data.')
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        VLAY.addWidget(QtWidgets.QLabel('Class name (NoEdit) : '))
        VLAY.stretchValue = 3
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        wln  = _VM_.setVariable('writeClassName',QtWidgets.QLineEdit(''))
        wln.setReadOnly(True)
        VLAY.addWidget(wln)
        VLAY.stretchValue = 7
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.layout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        ## ------------------------------------------------
        ## Order
        
        bufkey = 'orderParam'
        WPC.setCaption()
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        VLAY.addWidget(QtWidgets.QLabel('Order number : '))
        VLAY.stretchValue = 3
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        oln  = _VM_.setVariable('orderParam',QtWidgets.QLineEdit(''))
        oln.setValidator(QtGui.QIntValidator())
        oln.textChanged.connect(self.orderNumberCheck)
        oln.setText('100')
        VLAY.addWidget(oln)
        VLAY.stretchValue = 7
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.layout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        ## ------------------------------------------------
        ## Width/Height
        
        bufkey = 'widthHeight'
        WPC.setCaption()
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        VLAY.addWidget(QtWidgets.QLabel('Width size :'))
        VLAY.stretchValue = 2
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        wcb  = _VM_.setVariable('widthSize',QtWidgets.QLineEdit(''))
        wcb.setValidator(QtGui.QIntValidator())
        wcb.setText('400')
        VLAY.addWidget(wcb)
        VLAY.stretchValue = 3
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        VLAY.addWidget(QtWidgets.QLabel('Hieght size :'))
        VLAY.stretchValue = 2
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        hcb  = _VM_.setVariable('heightSize',QtWidgets.QLineEdit(''))
        hcb.setValidator(QtGui.QIntValidator())
        hcb.setText('400')
        VLAY.addWidget(hcb)
        VLAY.stretchValue = 3
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.layout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        ## ------------------------------------------------
        ## Drop
        
        self.setStyleSheet('QRadioButton{color:#EEE;}')
        bufkey = 'dropParam'
        dropParamGroup = QtWidgets.QButtonGroup(self)
        WPC.setCaption()
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        VLAY.addWidget(QtWidgets.QLabel('"setAcceptDrops" flag :'))
        VLAY.stretchValue = 4
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        drbt = _VM_.setVariable('dropTrue' ,QtWidgets.QRadioButton('True'))
        drbt.setChecked(True)
        dropParamGroup.addButton(drbt,0)
        VLAY.addWidget(drbt)
        VLAY.stretchValue = 1
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        drbf = _VM_.setVariable('dropFalse',QtWidgets.QRadioButton('False'))
        dropParamGroup.addButton(drbf,1)
        VLAY.addWidget(drbf)
        VLAY.stretchValue = 1
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        VLAY.addWidget(QtWidgets.QLabel(''))
        VLAY.stretchValue = 5
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.layout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        
        ## ------------------------------------------------
        ## Start
        
        bufkey = 'startParam'
        startParamGroup = QtWidgets.QButtonGroup(self)
        WPC.setCaption()
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        VLAY.addWidget(QtWidgets.QLabel('Mastema startup flag :'))
        VLAY.stretchValue = 4
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        srbt = _VM_.setVariable('showTrue' ,QtWidgets.QRadioButton('True'))
        srbt.setChecked(True)
        startParamGroup.addButton(srbt,0)
        VLAY.addWidget(srbt)
        VLAY.stretchValue = 1
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        srbf = _VM_.setVariable('showFalse',QtWidgets.QRadioButton('False'))
        startParamGroup.addButton(srbf,1)
        VLAY.addWidget(srbf)
        VLAY.stretchValue = 1
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        VLAY.addWidget(QtWidgets.QLabel(''))
        VLAY.stretchValue = 5
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.layout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        ## ------------------------------------------------
        ## Window flag
        
        bufkey = 'windowFlagParam'
        WPC.setCaption()
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        VLAY.addWidget(QtWidgets.QLabel('Set window flag :'))
        VLAY.stretchValue = 3
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        wfcb = _VM_.setVariable('windowFlagBox',QtWidgets.QComboBox())
        wfcb.addItems(fc.WINDOWFLAG)
        VLAY.addWidget(wfcb)
        VLAY.stretchValue = 7
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.layout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        self.layout.addStretch()
        self.addHorizonLine(self.layout)
        self.layout.addStretch()
        
        ## ------------------------------------------------
        ## PushButton
        
        pb = _VM_.setVariable('createButton',sg.PushButton('Create'))
        pb.addStyleWord('color:#FFF;')
        pb.addStyleWord(pb.getGradientColor(12,'#888','#222'))
        pb.setStyleSheetWord()
        pb.applyStyleSheet()
        pb.setFixedHeight(32)
        pb.clicked.connect(self.executeCreate)
        self.layout.addWidget(pb)
        
        ## ------------------------------------------------
        ## Post process
        
        self.exePostProcess()
        
    ## ------------------------------------------------------------------------
    ## Pre/Post process
    
    def exePostProcess(self):
        r"""
            Post process
        """
        bnl = _VM_.getVariable('baseNameLine')
        bnl.setText('zzzzTestTempData')
    
    ## ------------------------------------------------------------------------
    ## widget
    
    def addHorizonLine(self,layout):
        r"""
        """
        layout.addWidget(sg.HorizonFrame())
    
    ## ------------------------------------------------------------------------
    ## func
    
    def refrectLineName(self):
        r"""
            メインのLineEditネームが変更されたらテキスト情報を反映する
        """
        wcn = _VM_.getVariable('writeClassName')
        wcn.setText(SM.capitalizeFirstLetter(
            str(_VM_.getVariable('baseNameLine').text())))
    
    def orderNumberCheck(self):
        r"""
            入力されているorder数が重複していないかチェック
            重複していた場合は入力文字を赤し、それ以外なら黒カラーに設定
        """
        prefdata = SM.getWindowPrefInfo()
        if not prefdata:
            return
        orderlist = sorted(
            [v['order'] for v in prefdata.values() if v.get('order')])
        op     = _VM_.getVariable('orderParam')
        result = (int(op.text()) in orderlist) if op.text() else None
        op.setStyleSheet('QLineEdit{color:%s;}'%(
            '#E00' if result else '#E0E' if result is None else '#111'))
        return result
    
    ## ------------------------------------------------------------------------
    ## execute
    
    def executeCreate(self):
        r"""
            処理実行
        """        
        ## --------------------------------------------------------------------
        ## pre process
        
        bnl = _VM_.getVariable('baseNameLine')
        if not bnl.text():
            print(u'!! "baseNameLine"に何も入力されていないので'
                  u'処理を中断します!!')
            return
        if self.orderNumberCheck():
            print(u'!! "order"の重複が確認されたので処理を中断します !!')
            return
        
        ## --------------------------------------------------------------------
        ## main
        
        BN = os.path.basename
        
        libTempDictInfo = SM.getLibTempPath()
        batPath = libTempDictInfo.get('bat').get('path')
        batFile = batPath.get('bat')
        dirPath     = libTempDictInfo.get('dir').get('path')
        baseDirFile = dirPath.get('base')
        initFile    = dirPath.get('init')
        funcFile    = dirPath.get('func')
        uiFile      = dirPath.get('ui')
        
        # Python2系でunicodeで返ってくるので
        # write処理でerrorを回避するためstrに変換
        basename = str(_VM_.getVariable('baseNameLine').text())
        Basename = SM.capitalizeFirstLetter(basename)
        SM.setBasename(basename)
        
        rw        = ('r','w')
        pver      = int(sg.getPythonVersion()[0])
        paramDict = {
            rw[0]   :{'mode':rw[0],'encoding':None},
            rw[1]   :{'mode':rw[1],'encoding':None},
            'option':{'path':''},
        }
        if pver==2:
            paramDict['option'].update({'path':'name'})
            [paramDict[x].pop('encoding') for x in rw]
        elif pver==3:
            paramDict['option'].update({'path':'file'})
            [paramDict[x].update({'encoding':'utf-8'}) for x in rw]
        else:
            raise RuntimeError(u'!! 不明なPythonVersion "{}" !!'.format(pver))
        
        ## --------------------------------------------------------------------
        ## ui/funcディレクトリコピー
        
        uiPath = SM.getFuncUiPath()
        outDir = SM.pathJoin([uiPath,basename])
        SM.copydir(baseDirFile,outDir)        
        
        def __exeEdit(type,target):
            r"""
            """
            bufpath = SM.pathJoin([outDir,BN(target)])
            param   = paramDict
            ([param[x].update({param['option']['path']:bufpath}) for x in rw])
        
            with open(**param[rw[0]]) as f:
                writetext = f.read()
            
            if type in ['func']:
                # date
                writetext = re.sub(
                    fc.TEMPDATE,sg.getDateTime()['ymd'][2],writetext)
            elif type in ['ui']:
                pass
            else:
                pass
            # name
            writetext = re.sub(fc.TEMPNAME,Basename,writetext)
            
            with open(**param[rw[1]]) as f:
                f.write(writetext)
        
        ## __init__/edit
                
        ## func/edit
        __exeEdit('func',funcFile)
        
        ## ui/edit
        __exeEdit('ui',uiFile)
        
        ## json/edit
        windowPrefInfo = SM.getWindowPrefInfo()
        
        # 新しく書き込む情報を辞書型で整理
        newWriteInfo   = {
            basename : {
                'drop'       : ('True' if
                    _VM_.getVariable('dropTrue').isChecked() else 'False'),
                'name'       : Basename,
                'order'      : int(_VM_.getVariable('orderParam').text()),
                'size'       : [int(_VM_.getVariable('widthSize').text()),
                    int(_VM_.getVariable('heightSize').text())],
                'start'      : ('True' if
                    _VM_.getVariable('showTrue').isChecked() else 'False'),
                'windowFlag' : str(
                    _VM_.getVariable('windowFlagBox').currentText()),
            }
        }
        margePrefInfo = {**windowPrefInfo,**newWriteInfo}
        
        # dump
        SM.dumpJsonFile(SM.getWidgetJsonPath(),margePrefInfo)
        
        ## --------------------------------------------------------------------
        ## batコピー（メタデータを保持しないcopyを採用）
        
        batPathList = SM.getBatPath()
        [SM.copy(batFile,x) for x in batPathList]
        
        ## --------------------------------------------------------------------
        ## Post process
        
        self.orderNumberCheck()

###############################################################################
## Edit tab

class EditLayoutBox(sg.ScrolledWidget):
    r"""
        編集用のウィジェットレイアウトボックス
    """
    def __init__(self,typename,parent=None):
        r"""
        """
        self.setCategoryName(typename)
        super(EditLayoutBox,self).__init__(parent)
        
    ## ------------------------------------------------------------------------
    ## setting method
    
    def setCategoryName(self,cat):
        r"""
            共通のカテゴリー名を変数にセット
        """
        self.__category = cat
        
    def getCategoryName(self):
        r"""
            共通のカテゴリー名を取得
        """
        return self.__category
    
    def mergeCategoryName(self,name):
        r"""
            共通のカテゴリー名を取得
        """
        return '{}_{}'.format(name,self.__category)
    
    ## ------------------------------------------------------------------------
    ## build
    
    def buildUI(self,parent=None):
        r"""
        """
        self.hlayout = QtWidgets.QHBoxLayout(parent)
        self.vlayout = QtWidgets.QVBoxLayout()
        
        orgtext  = SM.capitalizeFirstLetter(self.getCategoryName())
        toptext  = ('{} area'.format(orgtext))
        toplabel = _VM_.setVariable(
            self.getCategoryWidgetName('topLabelWidget'),
            QtWidgets.QLabel(toptext))
        toplabel.setContentsMargins(0,2,0,2)
        toplabel.setStyleSheet(
            'QLabel{color:#EEE;qproperty-alignment:AlignCenter;'
            'font-size:16px;font-family:Cambria;background-color:#111;}')
        self.vlayout.addWidget(toplabel)
        self.setStyleSheet('QRadioButton{color:#EEE;}')
        
        _contentsMarginsSize = {
            'default'     : [8,0,2,0],
            'radioButton' : [32,0,2,0],
        }
        
        WPC = WidgetPartsClass()
        ADD = self.mergeCategoryName
        
        ## ------------------------------------------------
        ## Class name
        
        bufkey = ADD('widgetClassName')
        WPC.setCaption('Class name.')
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        bnl  = _VM_.setVariable(
            ADD('editBaseNameLine'),QtWidgets.QLineEdit(''))
        bnl.setContentsMargins(*_contentsMarginsSize['default'])
        bnl.textChanged.connect(self.refrectLineName)
        VLAY.addWidget(bnl)
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.vlayout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()        
        
        ## ------------------------------------------------
        ## Class name
        
        bufkey = ADD('widgetClassNameMirror')
        WPC.setCaption()
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        bnl  = _VM_.setVariable(
            ADD('editBaseNameLineMirror'),QtWidgets.QLineEdit(''))
        bnl.setContentsMargins(*_contentsMarginsSize['default'])
        bnl.setReadOnly(True)
        VLAY.addWidget(bnl)
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.vlayout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        ## ------------------------------------------------
        ## Order
        
        bufkey = ADD('widgetOrderParam')
        WPC.setCaption('Widget order.')
        ## ------------------------------------------------
        VLAY = WPC.getBoxLayout(True)
        oln  = _VM_.setVariable(ADD('editOrderParam'),QtWidgets.QLineEdit(''))
        oln.setContentsMargins(*_contentsMarginsSize['default'])
        oln.setValidator(QtGui.QIntValidator())
        oln.textChanged.connect(self.orderNumberCheck)
        VLAY.addWidget(oln)
        WPC.setKeyListManagemnet(bufkey,VLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.vlayout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        ## ------------------------------------------------
        ## Width/Height
        
        bufkey = ADD('widgetWidthHeight')
        WPC.setCaption('Widget width/height.')
        ## ------------------------------------------------
        HLAY = WPC.getBoxLayout(False)
        wln  = _VM_.setVariable(ADD('editWidth'),QtWidgets.QLineEdit('200'))
        wln.setValidator(QtGui.QIntValidator())
        HLAY.addWidget(QtWidgets.QLabel('Width'))
        HLAY.addWidget(wln)
        WPC.setKeyListManagemnet(bufkey,HLAY)
        ## ------------------------------------------------
        HLAY = WPC.getBoxLayout(False)
        hln  = _VM_.setVariable(ADD('editHeight'),QtWidgets.QLineEdit('200'))
        hln.setValidator(QtGui.QIntValidator())
        HLAY.addWidget(QtWidgets.QLabel('Height'))
        HLAY.addWidget(hln)
        WPC.setKeyListManagemnet(bufkey,HLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.vlayout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        ## ------------------------------------------------
        ## setAcceptDrops
        
        bufkey = ADD('widgetAcceptDrops')
        WPC.setCaption('setAcceptDrops flag.')
        dropParamGroup = QtWidgets.QButtonGroup(self)
        ## ------------------------------------------------
        HLAY = WPC.getBoxLayout(False)
        HLAY.setContentsMargins(*_contentsMarginsSize['radioButton'])
        adrbt = _VM_.setVariable(
            ADD('editAcceptDropsTrue') ,QtWidgets.QRadioButton('True'))
        adrbf = _VM_.setVariable(
            ADD('editAcceptDropsFalse'),QtWidgets.QRadioButton('False'))
        dropParamGroup.addButton(adrbt,0)
        dropParamGroup.addButton(adrbf,1)
        adrbt.setChecked(True)
        HLAY.addStretch()
        HLAY.addWidget(adrbt)
        HLAY.addWidget(adrbf)
        WPC.setKeyListManagemnet(bufkey,HLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.vlayout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        ## ------------------------------------------------
        ## mastema startup
        
        bufkey = ADD('widgetMastemaStartup')
        WPC.setCaption('Mastema startup flag.')
        startParamGroup = QtWidgets.QButtonGroup(self)
        ## ------------------------------------------------
        HLAY = WPC.getBoxLayout(False)
        HLAY.setContentsMargins(*_contentsMarginsSize['radioButton'])
        msrbt = _VM_.setVariable(
            ADD('editMastemaStartupTrue') ,QtWidgets.QRadioButton('True'))
        msrbf = _VM_.setVariable(
            ADD('editMastemaStartupFalse'),QtWidgets.QRadioButton('False'))
        startParamGroup.addButton(msrbt,0)
        startParamGroup.addButton(msrbf,1)
        msrbt.setChecked(True)
        HLAY.addStretch()
        HLAY.addWidget(msrbt)
        HLAY.addWidget(msrbf)
        WPC.setKeyListManagemnet(bufkey,HLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.vlayout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        ## ------------------------------------------------
        ## setWindowFlag
        
        bufkey = ADD('widgetWindowFlagParam')
        WPC.setCaption('Window flag.')
        ## ------------------------------------------------
        HLAY = WPC.getBoxLayout(False)
        wfcb = _VM_.setVariable(ADD('editWindowFlagBox'),QtWidgets.QComboBox())
        wfcb.addItems(fc.WINDOWFLAG)
        HLAY.addStretch(1)
        HLAY.addWidget(wfcb,12)
        WPC.setKeyListManagemnet(bufkey,HLAY)
        ## ------------------------------------------------
        WPC.setListToLayout(WPC.getKeyListManagemnet(bufkey))
        self.vlayout.addLayout(WPC.exeBuildLayout())
        WPC.clearWidgetInfo()
        
        ## ------------------------------------------------
        ## Merge layout
        
        self.vlayout.addStretch()
        self.hlayout.addLayout(self.vlayout)
        
        ## ------------------------------------------------
        ## Post process
        
        self.refrectJsonDate()
        
    ## ------------------------------------------------------------------------
    ## setting
    
    def refrectJsonDate(self):
        r"""
            jsonの初期データをウィジェットに反映
        """
        pass
    
    ## ------------------------------------------------------------------------
    ## widget method
    
    def getCategoryWidget(self,prefixname=''):
        r"""
            指定したクラスワードからwidgetを取得
        """
        return _VM_.getVariable(self.getCategoryWidgetName(prefixname))
        
    def getCategoryWidgetName(self,prefixname=''):
        r"""
            指定したクラスワードからwidget共通ネームを取得
        """
        if not prefixname:
            return None
        orgtext = SM.capitalizeFirstLetter(self.getCategoryName())
        return '{}{}'.format(prefixname,orgtext)
    
    ## ------------------------------------------------------------------------
    ## func
    
    def refrectLineName(self):
        r"""
            メインのLineEditネームが変更されたらテキスト情報を反映する
        """
        ADD = self.mergeCategoryName
        buf = _VM_.getVariable(ADD('editBaseNameLineMirror'))
        buf.setText(SM.capitalizeFirstLetter(str(
            _VM_.getVariable(ADD('editBaseNameLine')).text())))
    
    def orderNumberCheck(self):
        r"""
            入力されているorder数が重複していないかチェック
            重複していた場合は入力文字を赤し、それ以外なら黒カラーに設定
        """
        op = _VM_.getVariable(self.mergeCategoryName('editOrderParam'))
        if not op.text():
            return
            
        prefdata = SM.getWindowPrefInfo()
        if not prefdata:
            return
        orderlist = sorted(
            [v['order'] for v in prefdata.values() if v.get('order')])
        
        # current/order値を取得
        current  = _VM_.getVariable('widgetTypeName').currentText()
        noworder = prefdata.get(current).get('order')
        opvalue  = int(op.text())

        # 現在値=Green(#080),重複=Red(#E00),それ以外Black(#111)
        setcolor = ('#080' if noworder==opvalue else '#E00'
            if opvalue in orderlist else '#111')
        op.setStyleSheet('QLineEdit{color:%s;}'%(setcolor))
    
class EditTabWidget(sg.ScrolledWidget):
    r"""
        editタブウィジェット
    """
    def __init__(self,parent=None):
        r"""
        """
        super(EditTabWidget,self).__init__(parent)
    
    ## ------------------------------------------------------------------------
    ## build
    
    def buildUI(self,parent=None):
        r"""
        """
        self.layout = QtWidgets.QVBoxLayout(parent)
        
        ## --------------------------------------------------------------------
        ## Pulldown menu
        
        hlayout   = QtWidgets.QHBoxLayout()
        pullmenu  = _VM_.setVariable(
            'widgetTypeName',QtWidgets.QComboBox())
        pullmenu.currentTextChanged.connect(self.toggleComboBox)
        updatebtn = _VM_.setVariable(
            'widgetTypeUpdate',QtWidgets.QPushButton('Update'))
        updatebtn.clicked.connect(self.executeUpdate)
        hlayout.addWidget(QtWidgets.QLabel('Target name :'),2)
        hlayout.addStretch()
        hlayout.addWidget(pullmenu,8)
        hlayout.addWidget(updatebtn)
        self.layout.addLayout(hlayout)
        
        ## --------------------------------------------------------------------
        ## Read/Write Area
        
        hlayout = QtWidgets.QHBoxLayout()
        for area in fc.READWRITE:
            buf = _VM_.setVariable(
                self.getAreaName(area),EditLayoutBox(area))
            hlayout.addWidget(buf)
        self.layout.addLayout(hlayout,9)
        self.layout.addStretch()
        
        ## --------------------------------------------------------------------
        ## PushButton
        
        pb = _VM_.setVariable(
            'editExecuteButton',QtWidgets.QPushButton('Execute Edit'))
        pb.setStyleSheet('QPushButton{color:#FFF;%s}'%(
            _COL_.GRD_C_VERTICAL%('#888','#222')))
        pb.setFixedHeight(32)
        pb.clicked.connect(self.editExecute)
        self.layout.addWidget(pb,1)
        
        ## --------------------------------------------------------------------
        ## Post process
        
        self.postSetting()
    
    ## --------------------------------------------------------------------
    ## Setting
    
    def postSetting(self):
        r"""
            レイアウト構築最後に実行するメソッド
        """
        self.addItemList()
    
    def getAreaName(self,area):
        r"""
            エリア情報をフルネームウィジェット形式で返す
        """
        return '{}AreaWidget'.format(area)
    
    def dataUpdate(self,text):
        r"""
            シーン内のjsonデータをアップデート
        """
        windowPrefInfo = SM.getWindowPrefInfo()
        if not windowPrefInfo:
            return
        infolist = windowPrefInfo.get(text)
        if not infolist:
            return
            
        for area in fc.READWRITE:
            AW  = _VM_.getVariable(self.getAreaName(area))
            ADD = AW.mergeCategoryName
            
            # class name
            _VM_.getVariable(ADD('editBaseNameLine')).setText(text)
            
            # class name mirror
            _VM_.getVariable(ADD('editBaseNameLineMirror')).setText(
                infolist.get('name'))
            
            # order
            _VM_.getVariable(ADD('editOrderParam')).setText(
                str(infolist.get('order')))
            
            # widget width/height
            for i,wh in enumerate(['Width','Height']):
                bufwidget = _VM_.getVariable(ADD('edit{}'.format(wh)))
                bufwidget.setText(str(infolist.get('size')[i]))
            
            # setAcceptDrops
            _VM_.getVariable(ADD('editAcceptDrops{}'.format(
                str(infolist.get('drop'))))).setChecked(True)
            
            # mastema startup
            _VM_.getVariable(ADD('editMastemaStartup{}'.format(
                str(infolist.get('drop'))))).setChecked(True)
            
            # window flags
            _VM_.getVariable(ADD('editWindowFlagBox')).setCurrentText(
                str(infolist.get('windowFlag')))
    
    ## --------------------------------------------------------------------
    ## Widget
    
    def addItemList(self):
        r"""
            json辞書を参照してコンボボックスのリストアイテムをセット
        """
        windowPrefInfo = SM.getWindowPrefInfo()
        if not windowPrefInfo:
            return
        self.addComboBoxItem(
            sorted([key for key in windowPrefInfo.keys()],reverse=False))
    
    def addComboBoxItem(self,addlist=[]):
        r"""
            ボックス内を初期化しつつアイテムを新規に追加する
        """
        pullmenu = _VM_.getVariable('widgetTypeName')
        pullmenu.clear()
        pullmenu.addItems(addlist)
        
    def toggleComboBox(self,text):
        r"""
            ボックス内に変更があったら実行するメソッド
        """
        self.dataUpdate(text)
        
    def executeUpdate(self):
        r"""
            ボタン押下のアップデートメソッド
        """
        self.dataUpdate(_VM_.getVariable('widgetTypeName').currentText())
    
    ## ------------------------------------------------------------------------
    ## Execute
    
    def editExecute(self):
        r"""
            実行メソッド
        """
        ## --------------------------------------------------------------------
        ## local method
        
        def boolCheck(widget):
            r"""
            """
            try:
                return str(True if widget.isChecked() else False)
            except:
                raise RuntimeError(
                    u'!! 取得できないウィジェットbool : {}'.format(widget))
        
        AWR = _VM_.getVariable(self.getAreaName(fc.READWRITE[0]))
        AWW = _VM_.getVariable(self.getAreaName(fc.READWRITE[1]))
        ADD = AWW.mergeCategoryName
        
        ## --------------------------------------------------------------------
        ## 入力されている情報チェック
        checklist = ['editBaseNameLine','editBaseNameLineMirror',
            'editOrderParam','editWidth','editHeight']
        for x in checklist:
            buf = ADD(x)
            if not _VM_.getVariable(buf).text():
                raise RuntimeError(
                    u'!! 入力されていないテキスト : {}'.format(buf))
        
        ## --------------------------------------------------------------------
        ## データの書き換え
        
        # json
        windowPrefInfo = SM.getWindowPrefInfo()

        # 新しく書き込む情報を辞書型で整理
        basename = str(_VM_.getVariable(ADD('editBaseNameLine')).text())
        Basename = str(_VM_.getVariable(ADD('editBaseNameLineMirror')).text())
        order = int(_VM_.getVariable(ADD('editOrderParam')).text())
        sizew = int(_VM_.getVariable(ADD('editWidth')).text())
        sizeh = int(_VM_.getVariable(ADD('editHeight')).text())
        drop  = boolCheck(_VM_.getVariable(ADD('editAcceptDropsTrue')))
        start = boolCheck(_VM_.getVariable(ADD('editMastemaStartupTrue')))
        wflag = str(_VM_.getVariable(ADD('editWindowFlagBox')).currentText())
        
        newWriteInfo = {
            basename : {
                'name'       : Basename,
                'order'      : order,
                'size'       : [sizew,sizeh],
                'drop'       : drop,
                'start'      : start,
                'windowFlag' : wflag,
            }
        }
        
        # 既存の辞書から情報修正する辞書データを削除する
        sortingPrefInfo = windowPrefInfo
        del sortingPrefInfo[_VM_.getVariable(
            AWR.mergeCategoryName('editBaseNameLine')).text()]
        
        margePrefInfo = {**sortingPrefInfo,**newWriteInfo}
        
        ## --------------------------------------------------------------------
        ## confirme
        
        msg  = (u'以下の内容で実行します。よろしいですか？\n\n')
        msg += (u'Widget basename : \n\t{}\n'.format(basename))
        msg += (u'Class basename : \n\t{}\n'.format(Basename))
        msg += (u'Order number : \n\t{}\n'.format(order))
        msg += (u'Widget size : \n\t{}x{}\n'.format(sizew,sizeh))
        msg += (u'AcceptDrops flag : \n\t{}\n'.format(drop))
        msg += (u'Mastema startup flag : \n\t{}\n'.format(start))
        msg += (u'Window flag : \n\t{}\n'.format(wflag))
        msgdialog = QtWidgets.QMessageBox(self)
        msgdialog.setStyleSheet('QLabel{color:#111;}')
        msgdialog.setWindowTitle('Confirme')
        msgdialog.setText(msg)
        msgdialog.setIcon(QtWidgets.QMessageBox.Question)
        msgdialog.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        result = msgdialog.exec_()
        if result==QtWidgets.QMessageBox.Cancel:
            return
        
        # json/dump
        SM.dumpJsonFile(SM.getWidgetJsonPath(),margePrefInfo)
        
        # bat/copy
        SM.setBasename(basename)
        bpath = SM.getBatPath()
        for p in bpath:
            basepath = os.path.dirname(p)
            readname = _VM_.getVariable(
                AWR.mergeCategoryName('editBaseNameLine')).text()
            
            ## !! 重要 !!
            ## readとwriteのネームが一致していたら処理をスキップ
            if basename == readname:
                continue
                
            srcpath  = ('/'.join([basepath,('.'.join([readname,'bat']))]))
            dstpath  = ('/'.join([basepath,('.'.join([basename,'bat']))]))
            SM.copy2(srcpath,dstpath)
            SM.remove(srcpath)
        
        # post process
        self.addItemList()
        wtn = _VM_.getVariable('widgetTypeName')
        wtn.setCurrentText(basename)
        
        STIE = sg.SystemTrayIcon(5000)
        STIE.setTitle('Edit finished.')
        STIE.setMsg('')
        STIE.showMsg()
        
###############################################################################
## main class

class CreateWorkHierarchy(sg.ScrolledWidget):
    r"""
        ウィジェットメインレイアウト
    """
    def __init__(self,parent=None,masterDict=None):
        r"""
            初期設定
        """
        # 一番トップの親"EventBaseWidget"を格納
        self.masterWidget = parent
        
        super(CreateWorkHierarchy,self).__init__(parent)
        self._dict = masterDict
    
    ## ------------------------------------------------------------------------
    ## common parent event setting
    
    def setEventPackage(self,packaging):
        r"""
            子と関連性を保つためのメソッドパッケージを親から引き継いで設定する
        """
        super(CreateWorkHierarchy,self).setEventPackage(packaging)
        
        # 親eventと連動
        if packaging:
            packaging()['set']('closeEvent',self.exeCloseEventFunc)
    
    ## ------------------------------------------------------------------------
    ## build
    
    def buildUI(self,parent=None):
        r"""
            enter description
        """
        self.preSetting()
        self.layout = QtWidgets.QVBoxLayout(parent)
        
        # tab
        tab  = _VM_.setVariable('tabWidget',QtWidgets.QTabWidget())
        ctab = _VM_.setVariable('createTabWidget',CreateTabWidget())
        etab = _VM_.setVariable('editTabWidget',EditTabWidget())
        tab.addTab(ctab,'Create')
        tab.addTab(etab,'Edit')
        tab.tabBarClicked.connect(self.resizeWidget)
        self.layout.addWidget(tab)
        
        self.setTabStyleSheet()
        self.buildSetting()
    
    def resizeWidget(self,index):
        r"""
            選択タブによってウィジェットを適切なサイズに変更する
        """
        tab  = _VM_.getVariable('tabWidget')
        
        def __checkIndex(specifyindex):
            r"""
                インデックスをチェックして他タブから変更があった場合Trueを返す
            """
            return (True if index == specifyindex
                and tab.currentIndex() != specifyindex else False)
        
        # Create
        if __checkIndex(0):
            self.masterWidget.resize(475,475)
        # Edit
        elif __checkIndex(1):
            self.masterWidget.resize(570,600)
        else:
            pass
    
    ## ------------------------------------------------------------------------
    ## event
    
    ## ------------------------------------------------------------------------
    ## setting
    
    def preSetting(self):
        r"""
            __init__設定時の動作をbuildUIで先行して行うための関数
        """
        # AppData/Roaming/msAppTools/<FILENAME>までのパスを設定
        SPSL.setSeriesPath(SPSL.getSaveEachUiPrefPath())
    
    def buildSetting(self):
        r"""
            build時に設定されるセッティングメソッド
        """
        _D = SPSL.getJsonFile()
        
        # タブ位置を再帰
        tabindex = _D.get(fc.PREFDATA['TAB'])
        if tabindex:
            tab = _VM_.getVariable('tabWidget')
            tab.setCurrentIndex(tabindex.get('INDEX'))
    
    def setTabStyleSheet(self):
        r"""
            タブのスタイルシートをセット
        """
        _VM_.getVariable('tabWidget').setStyleSheet(_COL_.getCommonTabColor())
    
    def getAboutData(self):
        r"""
            about情報の取得
        """
        return fc.getAboutInfo()
    
    ## ------------------------------------------------------------------------
    ## func
    
    def exeCloseEventFunc(self):
        r"""
            close時に実行するメソッドのクッション関数（親のcloseEventで実行）
        """
        _D = SPSL.getJsonFile()

        # タブ位置を記録
        bufDict = {}
        tab = _VM_.getVariable('tabWidget')
        bufDict['INDEX'] = tab.currentIndex()
        _D[fc.PREFDATA['TAB']] = bufDict
        
        SPSL.setDict(_D)
        SPSL.setBackup(True)
        SPSL.setJsonFile()

###############################################################################
## END
'''
    ## func edit
    >> 関数組み込み型
    if pver==2:
        _openfunc_ = open(bufpath,'r')
    elif pver==3:
        _openfunc_ = open(bufpath,'r',encoding='utf-8')
    else:
        return
    with _openfunc_ as f:
        textall = f.read()
        
    >> 辞書代入型
    if pver==2:
        param_r = {'name':bufpath,'mode':'r'}
    elif pver==3:
        param_r = {'file':bufpath,'mode':'r','encoding':'utf-8'}
    else:
        return
    with open(**param_r) as f:
        textall = f.read()
'''