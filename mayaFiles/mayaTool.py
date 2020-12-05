#!/usr/bin/python
# -*- coding: utf-8 -*-
r'''
    @file     mayaTool.py
    @brief    UIを伴うツール類のまとめ
    @class    SelectPreservationWidget       : 横一列のレイアウト品をまとめたクラス
    @class    SelectPreservationMainUI       : 選択ノードを保存して選択したりするツールのレイアウト部分
    @class    SelectPreservationUI           : 選択ノードを保存して選択したりするツールのメイン部分
    @class    SliderParts                    : スライダーパーツ部分
    @class    CameraZoomerMainUI             : cameraZoomerメイン記述
    @class    CameraZoomerUI                 : cameraZoomerUI
    @class    AttributeSupportToolMainUI     : アトリビュートサポートツールコア部分
    @class    AttributeSupportToolUI         : アトリビュートサポートツールのUI
    @class    ImageOperationMainUI           : 画像操作UIレイアウト部分
    @class    ImageOperationUI               : 画像操作UI
    @class    ModelingSynthesisToolMainUI    : レイアウト作成処理
    @class    ModelingSynthesisToolUI        : モデリングコマンド総合ツール
    @class    PointMovedConfigurationMainUI  : PointMovedConfigurationメイン部分
    @class    PointMovedConfigurationUI      : 選択ノードの中心位置に対してアクションを行うUI
    @class    TemplateSettingMainUI          : テンプレート設定UIのレイアウト部分
    @class    TemplateSettingUI              : テンプレート設定のUI
    @class    ModelingPaperPatternMainUI     : ModelingPaperPatternUIメイン記述
    @class    ModelingPaperPatternUI         : ModelingPaperPatternUIクラス
    @class    colorButtonWidget              : カラーダイアログの入り口ボタンクラス
    @class    MaterialColorAssignmentMainUI  : MaterialColorAssignmentMainUIレイアウト部分
    @class    MaterialColorAssignmentUI      : 設定したカラーのマテリアルをオブジェクトにアサインするUI
    @class    PoseResetterMainUI             : 内部レイアウト設定
    @class    PoseResetterUI                 : gooneys仕様で作られたリグデータのポーズ設定UI
    @class    CreateGeometryCacheMainUI      : ジオメトリキャッシュ作成の中身部分
    @class    AlembicOptionToolsExportAttrUI : Exportアトリビュート領域のウィジェット
    @class    AlembicOptionToolsExportUI     : Exportメイン関数
    @class    AlembicOptionToolsImportUI     : Importメイン関数
    @class    AlembicOptionToolsUI           : アレンビック関係のコマンドをまとめたツールUI
    @class    CacheSettingMainUI             : CacheSettingMainUIのメインコード
    @class    CacheSettingUI                 : CacheSettingUIのメインコード
    @class    SimPlayblastMainUI             : SimPlayblastUIレイアウト部分
    @class    SimPlayblastUI                 : SimPlayblastUIのメインコード
    @class    TransferBlendShapeMainUI       : TransferBlendShapeのMainUI部分
    @class    TransferBlendShapeUI           : TransferBlendShapeのUI
    @class    SearchSkinClusterMainUI        : SearchSkinClusterUIレイアウト部分
    @class    SearchSkinClusterUI            : SearchSkinClusterのUI
    @class    FitToMeshMainUI                : FitToMeshUIメイン部分
    @class    FitToMeshUI                    : FitToMeshのUI
    @class    MoveVertexSameNodeMainUI       : レイアウト部分
    @class    MoveVertexSameNodeUI           : MoveVertexSameNodeのUI
    @class    NClothAttrValuesMainUI         : NClothAttrValuesUIメイン部分
    @class    NClothAttrValuesUI             : nClothのアトリビュートを書き出すUI
    @class    AlignPolyGridMainUI            : AlignPolyGridUIメイン部分
    @class    AlignPolyGridUI                : AlignPolyGridのUI
    @class    SetDropImageMainUI             : ドロップテストレイアウト構築ウィジェット
    @class    SetDropImageUI                 : ドロップテストUI
    @function uc                             : undoを一つにまとめる
    @function showWindow                     : ウィンドウの表示
    @date     2017/05/29 8:46[matsuzawa](matsuzawa@gooneys.co.jp)
    @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    このソースの版権は[StudioGOONEYS,Inc.]にあります
    無断転載、改ざん、無断使用は基本的に禁止しておりますので注意して下さい
    このソースを使用して不具合や不利益等が生じても[StudioGOONEYS,Inc.]
    は一切責任を負いませんのであらかじめご了承ください
'''
import os,re,sys,json,math,time,shutil,shiboken2
from . import mayaFunc
from ..settingFiles import stylesheet    as ss
from ..settingFiles import systemGeneral as sg
from maya import cmds,mel,OpenMayaUI
from PySide2 import QtWidgets,QtGui,QtCore
from msAppTools import msAppIcons
MainWindow = shiboken2.wrapInstance(
    long(OpenMayaUI.MQtUtil.mainWindow()),QtWidgets.QWidget
)

_TE = sg.TimeEvent()

# -----------------------------------------------------------------------------
# common func系

def uc(command, *args, **keywords):
    r'''
        @brief  undoを一つにまとめる
        @param  command(any)  : [関数]
        @param  args(any)     : enter description
        @param  keywords(any) : enter description
        @return (any):None
    '''
    cmds.undoInfo(ock=True)
    try:
        command(*args, **keywords)
    except Exception as e:
        raise e
    finally:
        cmds.undoInfo(cck=True)

# =============================================================================
# =============================================================================

# -----------------------------------------------------------------------------
# - common
# -----------------------------------------------------------------------------

class SelectPreservationWidget(QtWidgets.QWidget):
    r'''
        @brief    横一列のレイアウト品をまとめたクラス
        @inherit  QtWidgets.QWidget
        @function popupMenuSetup : メニューの準備
        @function save           : 選択ノードをセーブする時に実行される関数
        @function select         : 選択されているノードを選択する時に実行される関数
        @function nodePrint      : 入力されているエディット情報のプリント
        @function optionVarSet   : オプションバーのセット
        @function optionVarRead  : オプションバーの読み込み
        @function optionVarDel   : オプションバーの削除
        @date     2017/12/15 08:54[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self,num=0,length=2,parent=None):
        r'''
            @brief  メイン関数
            @param  num(any)    : カラムナンバー数
            @param  length(any) : enter description
            @param  parent(any) : enter description
            @return (any):
        '''
        super(SelectPreservationWidget, self).__init__(parent)
        
        self.label = ('{:0>%s}'%(str(length))).format(str(num))
        self.opvtn = 'selectPreservationOptionVarName_%s' % (self.label)
        
        columnAllLayout = QtWidgets.QHBoxLayout(self)
        columnAllLayout.setContentsMargins(0, 0, 0, 0)
        columnAllLayout.setSpacing(2)
        bufLabel = QtWidgets.QLabel('%s : ' % (self.label))
        bufButtonA = QtWidgets.QPushButton('Save')
        bufButtonA.clicked.connect(self.save)
        bufButtonB = QtWidgets.QPushButton('Select')
        bufButtonB.clicked.connect(self.select)
        self.bufText = QtWidgets.QLineEdit('')
        self.bufText.setReadOnly(True)
        self.bufText.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.bufText.customContextMenuRequested.connect(self.popupMenuSetup)
        columnAllLayout.addWidget(bufLabel)
        columnAllLayout.addWidget(bufButtonA)
        columnAllLayout.addWidget(bufButtonB)
        columnAllLayout.addWidget(self.bufText)
    
    def popupMenuSetup(self, point):
        r'''
            @brief  メニューの準備
            @param  point(any) : ポイントの座標<PySide.QtCore.QPoint(X,Y)>
            @return (any):
        '''
        exeMenu = QtWidgets.QMenu()
        exeMenu.addAction('%s : print' % (self.label), self.nodePrint)
        opv = exeMenu.addMenu('%s : optionVar' % (self.label))
        opv.addAction('set',  self.optionVarSet)
        opv.addAction('read', self.optionVarRead)
        opv.addAction('del',  self.optionVarDel)
        
        # window全体のポイント位置からホップアップ位置を指定
        exeMenu.exec_(QtGui.QCursor.pos())
        
        # ポイントを固定する場合
        # exeMenu.exec_(QtCore.QPoint(300, 300)) 
    
    def save(self):
        r'''
            @brief  選択ノードをセーブする時に実行される関数
            @return (any):
        '''
        buf = ''
        sep = ','
        ls  = cmds.ls(sl=True)
        m   = QtWidgets.QApplication.keyboardModifiers()
        # add
        if m == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
            buf = self.bufText.text()
            sel = filter(
                lambda _str:_str != '', buf.split(sep)
            )
            for l in ls:
                flag = False
                for s in sel:
                    if s == l:
                        flag = True
                if not flag:
                    buf += '%s%s' % (l, sep)
        # replace
        else:
            for l in ls:
                buf += '%s%s' % (l, sep)
        
        self.bufText.setText(buf)
    
    def select(self):
        r'''
            @brief  選択されているノードを選択する時に実行される関数
            @return (any):
        '''
        confSelList = []
        
        # ノードの有無の確認
        for s in filter(lambda _str:_str != '', self.bufText.text().split(',')):
            if cmds.objExists(s):
                confSelList.append(s)
        
        m = QtWidgets.QApplication.keyboardModifiers()
        if m == QtCore.Qt.ShiftModifier:
            cmds.select(confSelList, tgl=True)
        elif m == QtCore.Qt.ControlModifier:
            cmds.select(confSelList, d=True)
        elif m == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
            cmds.select(confSelList, add=True)
        else:
            cmds.select(confSelList, r=True)
    
    def nodePrint(self):
        r'''
            @brief  入力されているエディット情報のプリント
            @return (any):
        '''
        line = '# %s #' % ('+'*60)
        print(line)
        for s in filter(lambda _str:_str != '', self.bufText.text().split(',')):
            print(s)
        print(line)
        
    def optionVarSet(self):
        r'''
            @brief  オプションバーのセット
            @return (any):
        '''
        cmds.optionVar(sv=[self.opvtn, self.bufText.text()])
        print('optionVar set. [name:%s]' % (self.opvtn))
        
    def optionVarRead(self):
        r'''
            @brief  オプションバーの読み込み
            @return (any):
        '''
        # オプションバーがセットされてない場合はエラーになるのでそれを回避
        try:
            self.bufText.setText(cmds.optionVar(q=self.opvtn))
            print('optionVar read. [name:%s]' % (self.opvtn))
        except:
            print('optionVar read Failure. [name:%s]' % (self.opvtn))
        
    def optionVarDel(self):
        r'''
            @brief  オプションバーの削除
            @return (any):
        '''
        cmds.optionVar(rm=self.opvtn)
        print('optionVar delete. [name:%s]' % (self.opvtn))
    
class SelectPreservationMainUI(sg.ScrolledWidget):
    r'''
        @brief    選択ノードを保存して選択したりするツールのレイアウト部分
        @inherit  sg.ScrolledWidget
        @function buildUI   : 継承した関数内にUIを作成する
        @function addWidget : 横一列のウィジェットを作る親関数
        @date     2017/12/14 14:38[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    bc = {0:'#a2e4e5', 1:'#b2e59e'}
    
    def buildUI(self,parent=None):
        r'''
            @brief  継承した関数内にUIを作成する
            @param  parent(any) : enter description
            @return (any):
        '''
        addLayout = QtWidgets.QHBoxLayout()
        addlabel  = QtWidgets.QLabel(u'Add column : ')
        addButton = QtWidgets.QPushButton('+ add')
        addButton.setStyleSheet('QPushButton{background-color:#96570f}')
        addButton.clicked.connect(self.addWidget)
        addLayout.addStretch()
        addLayout.addWidget(addlabel)
        addLayout.addWidget(addButton)

        self.columnAllLayout = QtWidgets.QVBoxLayout()
        for i in range(0,4):
            self.addWidget()
            
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setSpacing(3)
        layout.addLayout(addLayout)
        layout.addLayout(self.columnAllLayout)
        layout.addStretch()
        
    def addWidget(self):
        r'''
            @brief  横一列のウィジェットを作る親関数
            @return (any):
        '''
        i = self.columnAllLayout.count()
        w = SelectPreservationWidget(num=str(i))
        w.setStyleSheet(
            'QPushButton{color:#111;background-color:%s}' % (self.bc[i%2])
        )
        self.columnAllLayout.addWidget(w)

class SelectPreservationUI(sg.EventBaseWidget):
    r'''
        @brief    選択ノードを保存して選択したりするツールのメイン部分
        @inherit  sg.EventBaseWidget
        @date     2017/12/14 14:38[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self,parent=None):
        r'''
            @brief  メインUI
            @param  parent(any) : enter description
            @return (any):
        '''
        super(SelectPreservationUI, self).__init__(parent)
        
        self.debugFlag = False        
        self.claName = self.__class__.__name__
        self.version = '1.2a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2017/12/14'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(300,200)
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        main = SelectPreservationMainUI()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)
    
# -----------------------------------------------------------------------------

class SliderParts(QtWidgets.QWidget):
    r'''
        @brief    スライダーパーツ部分
        @inherit  QtWidgets.QWidget
        @function popMenu            : ホップアップメニュー設定
        @function resetValue         : 入力数値のリセット
        @function buttonStep         : ボタン実行時の操作
        @function setLabel           : ラベルの設定
        @function setRange           : レンジの設定
        @function setValue           : 数値の設定
        @function setDafaultParam    : デフォルトの数値の設定
        @function setStep            : ステップ数
        @function value              : スピンボックスの値を返す
        @function moveSpinBoxCommand : スピンボックス変更時に実行される関数
        @function convToSpinBox      : スピンボックスに値を設定する際に変換する関数
        @function moveSliderCommand  : スライダー変更時に実行される関数
        @function convToSlider       : スライダーに値を設定する際に変換する関数
        @function setFactor          : ファクター（小数値、割る数）の変換値
        @function zoom               : 数値変更時にパースのアトリビュートを設定する関数
        @date     2018/02/09 14:33[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, camBox, parent=None):
        r'''
            @brief  enter description
            @param  camBox(any) : enter description
            @param  parent(any) : enter description
            @return (any):
        '''
        super(SliderParts, self).__init__(parent)
        
        self.factor = 0.01
        self.cam = camBox
        
        filmTransLayout = QtWidgets.QVBoxLayout()
        filmTransLayout.setSpacing(2)
        self.filmTransLabel = QtWidgets.QLabel('')
        filmTransSliderLayout = QtWidgets.QHBoxLayout()
        self.spinBox = QtWidgets.QDoubleSpinBox()
        self.spinBox.valueChanged.connect(self.moveSpinBoxCommand)
        self.spinBox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.spinBox.customContextMenuRequested.connect(self.popMenu)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.sliderMoved.connect(self.moveSliderCommand)
        self.slider.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.slider.customContextMenuRequested.connect(self.popMenu)
        buttonA = QtWidgets.QPushButton('<')
        buttonB = QtWidgets.QPushButton('>')
        buttonA.type = False
        buttonB.type = True
        buttonA.clicked.connect(self.buttonStep)
        buttonB.clicked.connect(self.buttonStep)
        filmTransSliderLayout.addWidget(self.spinBox)
        filmTransSliderLayout.addWidget(self.slider)
        filmTransSliderLayout.addWidget(buttonA)
        filmTransSliderLayout.addWidget(buttonB)
        filmTransLayout.addWidget(self.filmTransLabel)
        filmTransLayout.addLayout(filmTransSliderLayout)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(2)
        layout.addLayout(filmTransLayout)
        
    def popMenu(self):
        r'''
            @brief  ホップアップメニュー設定
            @return (any):
        '''
        menu = QtWidgets.QMenu()
        m = menu.addAction('reset', self.resetValue)
        menu.exec_(QtGui.QCursor.pos())

    def resetValue(self):
        r'''
            @brief  入力数値のリセット
            @return (any):
        '''
        self.setValue(self.defaultValue)
        
    def buttonStep(self):
        r'''
            @brief  ボタン実行時の操作
            @return (any):
        '''
        val  = self.spinBox.value()
        step = self.spinBox.singleStep()
        sum  = val + step if self.sender().type else val - step
        
        self.setValue(sum)
        self.zoom()
        
    def setLabel(self, label):
        r'''
            @brief  ラベルの設定
            @param  label(any) : ラベル名
            @return (any):
        '''
        self.filmTransLabel.setText(label)
        
    def setRange(self, min, max):
        r'''
            @brief  レンジの設定
            @param  min(any) : [int]最小値
            @param  max(any) : [int]最大値
            @return (any):None
        '''
        self.spinBox.setRange(min, max)
        self.slider.setRange(min/self.factor, max/self.factor)
    
    def setValue(self, value):
        r'''
            @brief  数値の設定
            @param  value(any) : [double]入力数値
            @return (any):None
        '''
        self.spinBox.setValue(value)
        self.convToSlider(value)
    
    def setDafaultParam(self, value, attr):
        r'''
            @brief  デフォルトの数値の設定
            @param  value(any) : デフォルト数値
            @param  attr(any)  : enter description
            @return (any):
        '''
        self.defaultValue = value
        self.attrType = attr
    
    def setStep(self, step):
        r'''
            @brief  ステップ数
            @param  step(any) : 0.1, 0.01など
            @return (any):
        '''
        self.spinBox.setSingleStep(step)
    
    def value(self):
        r'''
            @brief  スピンボックスの値を返す
            @return (any):スピンボックスの値
        '''
        return self.spinBox.value()

    def moveSpinBoxCommand(self, value):
        r'''
            @brief  スピンボックス変更時に実行される関数
            @param  value(any) : ボックス変更時に自動的に入力される数値
            @return (any):
        '''
        self.convToSlider(value)
        self.zoom()
        
    def convToSpinBox(self, value):
        r'''
            @brief  スピンボックスに値を設定する際に変換する関数
            @param  value(any) : [int]スライダーから代入される変数値
            @return (any):None
        '''
        val = value * self.factor
        self.spinBox.setValue(val)
    
    def moveSliderCommand(self, value):
        r'''
            @brief  スライダー変更時に実行される関数
            @param  value(any) : スライダー変更時に自動的に入力される数値
            @return (any):
        '''
        self.convToSpinBox(value)
        self.zoom()
    
    def convToSlider(self, d):
        r'''
            @brief  スライダーに値を設定する際に変換する関数
            @param  d(any) : [int]スピンボックスから代入される変数値
            @return (any):None
        '''
        val = d/self.factor
        self.slider.setValue(val)
    
    def setFactor(self, factor):
        r'''
            @brief  ファクター（小数値、割る数）の変換値
            @param  factor(any) : [double]割る少数点数
            @return (any):None
        '''
        self.factor = factor
        
    def zoom(self):
        r'''
            @brief  数値変更時にパースのアトリビュートを設定する関数
            @return (any):
        '''
        camName = self.cam.currentText()
        if not cmds.objExists(camName):
            print(u'+ Camera[%s]が存在しません。' % camName)
            return
        
        # slider,spinboxの初回起動時にはattrTypeの変数が設定されず
        # エラーになるのでtry文を使い回避する。
        try:
            attr = ''
            
            if self.attrType == 'H':
                attr = 'filmTranslateH'
            elif self.attrType == 'V':
                attr = 'filmTranslateV'
            elif self.attrType == 'S':
                attr = 'postScale'
            else:
                attr = None
            
            attrName = '%s.%s' % (camName, attr)
            
            if not cmds.objExists(attrName):
                print(u'+ アトリビュート[%s]が存在しません。' % attrName)
                return
            
            cmds.setAttr(attrName, self.spinBox.value())
        except:
            pass
        
class CameraZoomerMainUI(sg.ScrolledWidget):
    r'''
        @brief    cameraZoomerメイン記述
        @inherit  sg.ScrolledWidget
        @function buildUI          : UIなどの記述部分
        @function valueSet         : 設定されているカメラのアトリビュートの数値をセット
        @function comboBoxAddItems : comboBoxのアイテム追加関数
        @date     2018/02/09 11:21[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent=None):
        r'''
            @brief  UIなどの記述部分
            @param  parent(any) : enter description
            @return (any):
        '''
        
        selCameraHLayout = QtWidgets.QHBoxLayout()
        selCameraLabel = QtWidgets.QLabel(u'Select camera :')
        self.selCameraComBox = QtWidgets.QComboBox()
        self.comboBoxAddItems()
        selCameraHLayout.addWidget(selCameraLabel)
        selCameraHLayout.addWidget(self.selCameraComBox)
        
        self.filmTranslateH = SliderParts(self.selCameraComBox)
        self.filmTranslateH.setLabel('Film translate H')
        self.filmTranslateH.setRange(-1,1)
        self.filmTranslateH.setDafaultParam(0.0, 'H')
        self.filmTranslateH.setStep(0.01)
        self.filmTranslateV = SliderParts(self.selCameraComBox)
        self.filmTranslateV.setLabel('Film translate V')
        self.filmTranslateV.setRange(-1,1)
        self.filmTranslateV.setDafaultParam(0.0, 'V')
        self.filmTranslateV.setStep(0.01)
        self.postScale = SliderParts(self.selCameraComBox)
        self.postScale.setLabel('Post scale')
        self.postScale.setRange(0.01,20)
        self.postScale.setDafaultParam(1.0, 'S')
        self.postScale.setStep(0.01)
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setSpacing(2)
        layout.addLayout(selCameraHLayout)
        layout.addWidget(self.filmTranslateH)
        layout.addWidget(self.filmTranslateV)
        layout.addWidget(self.postScale)
        
        self.valueSet()
        
    def valueSet(self):
        r'''
            @brief  設定されているカメラのアトリビュートの数値をセット
            @return (any):
        '''
        for fc,at,dfv in (
            [self.filmTranslateH,'filmTranslateH',0.0],
            [self.filmTranslateV,'filmTranslateV',0.0],
            [self.postScale,'postScale',1.0],
        ):
            try:
                fc.setValue(
                    cmds.getAttr('%s.%s' % (
                        self.selCameraComBox.currentText(),at)
                    )
                )
            except:
                fc.setValue(dfv)

    def comboBoxAddItems(self):
        r'''
            @brief  comboBoxのアイテム追加関数
            @return (any):
        '''
        L = []
        mp = 'modelPanel'
        
        panel = cmds.getPanel(wf=True)
        if not panel.startswith(mp):
            panel = '%s4' % (mp)
        
        nc  = cmds.modelPanel(panel,q=True,camera=True)
        ncs = cmds.ls(nc, dag=True, shapes=True, ap=True)
        L.append(ncs[0])
        
        for cam in cmds.ls(ca=True):
            if cam == ncs[0]:
                continue
            L.append(cam)
        
        self.selCameraComBox.addItems(L)
        
class CameraZoomerUI(sg.EventBaseWidget):
    r'''
        @brief    cameraZoomerUI
        @inherit  sg.EventBaseWidget
        @date     2018/02/09 11:19[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  ガワ設定
            @param  parent(any) : enter description
            @return (any):
        '''
        super(CameraZoomerUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/02/09'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(370,270)
        
        main = CameraZoomerMainUI()
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)

# -----------------------------------------------------------------------------

class AttributeSupportToolMainUI(sg.ScrolledWidget):
    r'''
        @brief    アトリビュートサポートツールコア部分
        @inherit  sg.ScrolledWidget
        @function buildUI              : レイアウトメイン部分
        @function exeSetSelectNodeMenu : setSelectNode起動メニュー
        @function exeSetSelectNode     : 最初に選択したノードをセットする
        @function exeApply             : Apply時の実行関数
        @function exeSelect            : listviewを選択したときに実行されるコマンド
        @date     2018/05/29 15:05[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    attrList = (
        ['userDefined','read','write','array','keyable','extension','locked',
         'unlocked','visible','ramp','connectable','settable'],
        ['string'],
    )
    ss_lineBgc = 'QLineEdit{background-color:#000;}'
    
    def buildUI(self, parent=None):
        r'''
            @brief  レイアウトメイン部分
            @param  parent(any) : enter description
            @return (any):
        '''
        # -------------------------------------------------
        # node name
        
        nnLayout    = QtWidgets.QHBoxLayout()
        nnLabel     = QtWidgets.QLabel('Node name :')
        self.nnLine = QtWidgets.QLineEdit()
        self.nnLine.returnPressed.connect(self.exeApply)
        self.nnLine.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.nnLine.customContextMenuRequested.connect(self.exeSetSelectNodeMenu)
        nnButton    = QtWidgets.QPushButton('Apply')
        nnButton.clicked.connect(self.exeApply)
        nnLayout.addWidget(nnLabel)
        nnLayout.addWidget(self.nnLine)
        nnLayout.addWidget(nnButton)
        
        # -------------------------------------------------
        # attribute list (other string)
        
        attrLayoutA = QtWidgets.QGridLayout()
        num = 0
        self.cb_List = []
        for i1 in range(3):
            for i2 in range(4):
                buf = QtWidgets.QCheckBox(self.attrList[0][num])
                buf.clicked.connect(self.exeApply)
                attrLayoutA.addWidget(buf,i1,i2,1,1)
                self.cb_List.append(buf)
                num += 1
                
        # attribute list (string only)
        attrLayoutB      = QtWidgets.QHBoxLayout()
        self.cb_List_st  = QtWidgets.QCheckBox(self.attrList[1][0])
        self.cb_List_st.clicked.connect(self.exeApply)
        self.cb_List_ln  = QtWidgets.QLineEdit('*')
        self.cb_List_ln.returnPressed.connect(self.exeApply)
        self.priCheckBox = QtWidgets.QCheckBox('Print cmd')
        attrLayoutB.addWidget(self.cb_List_st)
        attrLayoutB.addWidget(self.cb_List_ln)
        attrLayoutB.addWidget(self.priCheckBox)
        
        # -------------------------------------------------
        # result line
        
        resultLayoutA     = QtWidgets.QHBoxLayout()
        self.fullNameLine = QtWidgets.QLineEdit('')
        self.fullNameLine.setEnabled(True)
        self.fullNameLine.setStyleSheet(self.ss_lineBgc)
        self.fullNameCB   = QtWidgets.QCheckBox('Short')
        self.fullNameCB.clicked.connect(self.exeSelect)
        resultLayoutA.addWidget(self.fullNameLine)
        resultLayoutA.addWidget(self.fullNameCB)
        
        resultLayoutB      = QtWidgets.QHBoxLayout()
        self.nodeNameLine  = QtWidgets.QLineEdit('')
        self.nodeNameLine.setEnabled(True)
        self.nodeNameLine.setStyleSheet(self.ss_lineBgc)
        self.shortNameLine = QtWidgets.QLineEdit('')
        self.shortNameLine.setEnabled(True)
        self.shortNameLine.setStyleSheet(self.ss_lineBgc)
        self.attrNumLine   = QtWidgets.QLineEdit('')
        self.attrNumLine.setEnabled(False)
        self.attrNumLine.setStyleSheet(self.ss_lineBgc)
        resultLayoutB.addWidget(self.nodeNameLine,4)
        resultLayoutB.addWidget(self.shortNameLine,2)
        resultLayoutB.addWidget(self.attrNumLine,1)
        
        # -------------------------------------------------
        # list line
        
        self.listWidget = QtWidgets.QListView()
        self.listWidget.setMinimumSize(1,1)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget.setAlternatingRowColors(True)
        model = QtGui.QStandardItemModel(0,1)
        self.listWidget.setModel(model)
        self.listWidget.selModel = QtCore.QItemSelectionModel(model)
        self.listWidget.setSelectionModel(self.listWidget.selModel)
        self.listWidget.selModel.selectionChanged.connect(self.exeSelect)
        
        # -------------------------------------------------
        # レイアウト総合
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addLayout(nnLayout)
        layout.addLayout(attrLayoutA)
        layout.addLayout(attrLayoutB)
        layout.addLayout(resultLayoutA)
        layout.addLayout(resultLayoutB)
        layout.addWidget(self.listWidget)
        layout.addStretch()
    
    def exeSetSelectNodeMenu(self):
        r'''
            @brief  setSelectNode起動メニュー
            @return (any):
        '''
        menu = QtWidgets.QMenu()
        m = menu.addAction('Set select node', self.exeSetSelectNode)
        menu.exec_(QtGui.QCursor.pos())
    
    def exeSetSelectNode(self):
        r'''
            @brief  最初に選択したノードをセットする
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            return
        self.nnLine.setText(sel[0])
    
    def exeApply(self):
        r'''
            @brief  Apply時の実行関数
            @return (any):
        '''
        def _listAttrPrifSetting(type):
            r'''
                @brief  アトリビュートをチェックしてcmdコマンド用のオプションフラグを追加する
                @param  type(any) : True=string以外, False=string
                @return (any):
            '''
            prifList = []
            list   = self.attrList[0] if type else self.attrList[1]
            atlist = self.cb_List     if type else [self.cb_List_st]
            for i,at in enumerate(list):
                if type == False:
                    if not atlist[i].isChecked():
                        prifList.append('*')
                    else:
                        prifList.append(self.cb_List_ln.text())
                else:
                    prifList.append(atlist[i].isChecked())
            return prifList
                
        node = self.nnLine.text()
        if not node:
            print(u'+ Nodeが記入されていません。')
            return
        if not cmds.objExists(node):
            print(u'+ Nodeがシーンに存在しません。')
            return
        
        prif = []
        prif += _listAttrPrifSetting(type=True)
        prif += _listAttrPrifSetting(type=False)
        
        if self.priCheckBox.isChecked():
            print(
                'cmds.listAttr("%s",userDefined=%s,read=%s,write=%s,array=%s,'
                'keyable=%s,extension=%s,locked=%s,unlocked=%s,visible=%s,'
                'ramp=%s,connectable=%s,settable=%s,string="%s")' % (
                    node,
                    prif[0],prif[1],prif[2],prif[3],prif[4],
                    prif[5],prif[6],prif[7],prif[8],prif[9],
                    prif[10],prif[11],prif[12],
                )
            )
            
        result = cmds.listAttr(
            node,
            userDefined = prif[0],
            read        = prif[1],
            write       = prif[2],
            array       = prif[3],
            keyable     = prif[4],
            extension   = prif[5],
            locked      = prif[6],
            unlocked    = prif[7],
            visible     = prif[8],
            ramp        = prif[9],
            connectable = prif[10],
            settable    = prif[11],
            string      = '%s' % (prif[12]),
        )
        
        # -------------------------------------------------
        # listviewに追加
        
        # 初期化
        model = self.listWidget.model()
        model.removeRows(0, model.rowCount())
        self.attrNumLine.setText('')
        self.fullNameLine.setText('')
        self.nodeNameLine.setText('')
        self.shortNameLine.setText('')
        
        if not result:
            return
        
        rootItem = model.invisibleRootItem()
        for r in result:
            item = QtGui.QStandardItem(r)
            rootItem.setChild(rootItem.rowCount(),0,item)
        
        self.attrNumLine.setText(str(len(result)))
    
    def exeSelect(self):
        r'''
            @brief  listviewを選択したときに実行されるコマンド
            @return (any):
        '''
        node   = self.nnLine.text()
        attr   = self.listWidget.selectionModel().currentIndex().data()
        lnName = '%s.%s' % (node,attr)
        if not cmds.objExists(lnName):
            return
        snAttr = cmds.ls(lnName,sn=True)[0].split('.')[1]
        snName = '%s.%s' % (node,snAttr)
        
        # write
        self.fullNameLine.setText(lnName)
        if self.fullNameCB.isChecked():
            self.fullNameLine.setText(snName)
        self.nodeNameLine.setText(attr)
        self.shortNameLine.setText(snAttr)
        
        
class AttributeSupportToolUI(sg.EventBaseWidget):
    r'''
        @brief    アトリビュートサポートツールのUI
        @inherit  sg.EventBaseWidget
        @date     2018/05/29 14:57[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  UIおおもと部分
            @param  parent(any) : enter description
            @return (any):
        '''
        super(AttributeSupportToolUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/05/29'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(400,400)
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        main  = AttributeSupportToolMainUI()
        close = QtWidgets.QPushButton('Close')
        close.clicked.connect(self.close)
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)
        layout.addWidget(close)

# -----------------------------------------------------------------------------

class ImageOperationMainUI(sg.ScrolledWidget):
    r'''
        @brief    画像操作UIレイアウト部分
        @inherit  sg.ScrolledWidget
        @function buildUI               : UI作成メイン関数
        @function keyPressEvent         : キープレス時のイベント情報
        @function setViewDefaultResize  : ウィンドウサイズのデフォルト設定
        @function exeUrlMenu            : メニュー窓口
        @function setImageSavePath      : イメージパスの保存
        @function getImageSavePath      : 保存したファイルパスのリターン
        @function setWindowSize         : ウィンドウサイズの保持関数
        @function getWindowSize         : ウィンドウサイズのリターン
        @function deleteImagePath       : 指定した先のファイルの削除
        @function exeSetImage           : imageのセット
        @function exeOpenDir            : ディレクトリのオープン
        @function exeOpenTempDir        : Tempディレクトリのオープン
        @function exeOpenSetPathDir     : 設定されているディレクトリパスのオープン
        @function exeSetPathDialog      : ダイアログからパスをセット
        @function exeClipboradToImage   : キャプチャされている画像をクリップボードに保存
        @function exeExportCaptureImage : 指定されている先のパスにキャプチャ画像を書き出し
        @function exeFitImage           : リサイズした際にimageLabelをスケールする
        @date     2018/10/09 10:39[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent=None):
        r'''
            @brief  UI作成メイン関数
            @param  parent(any) : enter description
            @return (any):
        '''
        self.class_st = None
        self.image    = None
        self.radioList = []
        self.radioItem = ('png','jpg')
        self.defaultLabelName     = 'No image data'
        self.defaultSaveImagePath = r'C:/_temp'
        self.imageMagni = 0.88
                
        self.labelLayout = QtWidgets.QVBoxLayout()
        self.imageLabel = QtWidgets.QLabel(self.defaultLabelName)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding
        )
        self.imageLabel.setToolTip(
            u'キャプチャされた画像が表示されます。\n'
            u'画像は不透過のjpg形式でデフォルトAppData\Local\Tempに仮保存されます。\n'
            u'コマンド:\n'
            u'[ Alt + Z ] 画像キャプチャ\n'
            u'[ Shift + Z ] UIサイズを初期化'
        )
        self.imageLabel.setStyleSheet(
            'QLabel{qproperty-alignment:AlignCenter;}QLabel{%s}'%(
                ss.GRD_C_VERTICAL%('#777','#111')
            )
        )
        capButton = QtWidgets.QPushButton('Capture')
        capButton.setToolTip(
            u'アクティブになっているMayaのビュー画像をキャプチャします。'
        )
        capButton.setStyleSheet(
            'QPushButton{background-color:rgb(12,128,196);height:24px;}'
        )
        capButton.clicked.connect(self.exeSetImage)
        capButton.menuAddress = 'openTempDir'
        capButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        capButton.customContextMenuRequested.connect(self.exeUrlMenu)
        self.labelLayout.addWidget(self.imageLabel)
        
        optionGroup   = QtWidgets.QGroupBox('Option')
        optionVLayout = QtWidgets.QVBoxLayout(optionGroup)
        pathLayout    = QtWidgets.QHBoxLayout()
        self.pathLine = QtWidgets.QLineEdit('')
        self.pathLine.setToolTip(
            u'イメージデータを書き出す先のパスを設定します。'
        )
        pathButton    = QtWidgets.QPushButton('SetPath')
        pathButton.setToolTip(
            u'ダイアログからパスを設定します。'
        )
        pathButton.clicked.connect(self.exeSetPathDialog)
        openButton    = QtWidgets.QPushButton('OpenDir')
        openButton.setToolTip(
            u'設定されているパスの先があればディレクトリを開きます。'
        )
        openButton.clicked.connect(self.exeOpenSetPathDir)
        pathLayout.addWidget(self.pathLine)
        pathLayout.addWidget(pathButton)
        pathLayout.addWidget(openButton)
        optionVLayout.addLayout(pathLayout)
        commandLayout = QtWidgets.QHBoxLayout()
        pasteButton   = QtWidgets.QPushButton('Paste to clipborad')
        pasteButton.setToolTip(
            u'設定されている拡張子のキャプチャ画像をクリップボードに保存します。'
        )
        pasteButton.clicked.connect(self.exeClipboradToImage)
        exportButton  = QtWidgets.QPushButton('Export to path')
        exportButton.setToolTip(
            u'指定されている先のパスにキャプチャ画像を書き出します。'
        )
        exportButton.clicked.connect(self.exeExportCaptureImage)
        
        self.radioTop  = QtWidgets.QButtonGroup()
        for i,rn in enumerate(self.radioItem):
            buf = QtWidgets.QRadioButton(rn)
            if i == 0:
                buf.setChecked(True)
            commandLayout.addWidget(buf,1)
            self.radioTop.addButton(buf,i)
            self.radioList.append(buf)
        commandLayout.addWidget(pasteButton,3)
        commandLayout.addWidget(exportButton,3)
        optionVLayout.addLayout(commandLayout)
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addLayout(self.labelLayout,6)
        layout.addWidget(capButton,3)
        layout.addWidget(optionGroup,1)
    
    def keyPressEvent(self, event):
        r'''
            @brief  キープレス時のイベント情報
            @param  event(any) : enter description
            @return (any):
        '''
        key  = self.getKeyType(event)
        mask = self.getKeyMask()
        
        if   (key['mod1'] == mask['alt'] and key['press'] == 'Z'):
            self.exeSetImage()
        elif (key['mod1'] == mask['shift'] and key['press'] == 'Z'):
            self.setViewDefaultResize()
    
    def setViewDefaultResize(self):
        r'''
            @brief  ウィンドウサイズのデフォルト設定
            @return (any):
        '''
        w,h = self.getWindowSize()
        self.class_st.resize(w,h)
    
    def exeUrlMenu(self):
        r'''
            @brief  メニュー窓口
            @return (any):
        '''
        m = self.sender()
        
        menu = QtWidgets.QMenu()
        if m.menuAddress == 'openTempDir':
            dir = menu.addAction('Open temp dir', self.exeOpenTempDir)
            menu.exec_(QtGui.QCursor.pos())
    
    def setImageSavePath(self,mainP,mainJ,tempJ):
        r'''
            @brief  イメージパスの保存
            @param  mainP(any) : main png
            @param  mainJ(any) : main jpg
            @param  tempJ(any) : temp jpg
            @return (any):
        '''
        self.mainP  = mainP
        self.mainJ  = mainJ
        self.thumbJ = tempJ
    
    def getImageSavePath(self):
        r'''
            @brief  保存したファイルパスのリターン
            @return (any):保存されてそのパス、無いならNone
        '''
        try: 
            return (self.mainP,self.mainJ,self.thumbJ)
        except AttributeError:
            return (None,None,None)
    
    def setWindowSize(self,w,h):
        r'''
            @brief  ウィンドウサイズの保持関数
            @param  w(any) : 横幅
            @param  h(any) : 縦幅
            @return (any):
        '''
        self.win_w = w
        self.win_h = h
    
    def getWindowSize(self):
        r'''
            @brief  ウィンドウサイズのリターン
            @return (any):
        '''
        try: 
            return (self.win_w,self.win_h)
        except AttributeError:
            return None
    
    def deleteImagePath(self, path):
        r'''
            @brief  指定した先のファイルの削除
            @param  path(any) : ファイルパス
            @return (any):
        '''
        if not path:
            return False
        if not os.path.isfile(path):
            return False
        try:
            os.remove(path)
            returnFlag = True
        except:
            returnFlag = False
        return returnFlag
        
    def exeSetImage(self):
        r'''
            @brief  imageのセット
            @return (any):
        '''
        [self.deleteImagePath(p) for p in self.getImageSavePath()]
        
        try:
            tempPath = os.path.join(
                os.path.dirname(os.environ['APPDATA']),'Local','Temp'
            )
        except KeyError:
            tempPath = defaultSaveImagePath
            if not os.path.isdir(tempPath):
                os.makedirs(tempPath)
                print(u'+ Create dir.')
                print(u'\t: %s'%(tempPath))
        
        epd = ('100png','100jpg','THUMBNAILjpg')
        day = cmds.about(cd=True).replace('/','')
        rsw = mayaFunc.returnRandomString(24)
        epn = ['%s_%s_%s'%(day,rsw,p) for p in epd]
        
        viewSize = mayaFunc.getViewSize()
        compsize = (
            [viewSize[0],viewSize[1],True]
                if viewSize[0] > viewSize[1] else
            [viewSize[1],viewSize[0],False]
        )
        rewhsize = (
            int(self.rect().width() *self.imageMagni)
                if compsize[2] else
            int(self.rect().height()*self.imageMagni)
        )
        magni = float(rewhsize)/float(compsize[0])
        wh    = (
            [rewhsize,int(compsize[1]*magni)]
                if compsize[2] else
            [int(compsize[1]*magni),rewhsize]
        )
        
        # メイン画像
        mainDataP = mayaFunc.viewCapture(
            path=tempPath,ext=epd[0][-3:],name=epn[0],logPring=False
        )
        mainDataJ = mayaFunc.viewCapture(
            path=tempPath,ext=epd[1][-3:],name=epn[1],logPring=False
        )
        # サムネ用
        capData = mayaFunc.viewCapture(
            path=tempPath,w=wh[0],h=wh[1],ext=epd[1][-3:],
            name=epn[2],logPring=True
        )
        self.image = QtGui.QImage(capData[0])
        pixmap = QtGui.QPixmap(self.image)
        self.imageLabel.setPixmap(pixmap)
        self.setImageSavePath(mainDataP[0],mainDataJ[0],capData[0])
    
    def exeOpenDir(self, path):
        r'''
            @brief  ディレクトリのオープン
            @param  path(any) : パス
            @return (any):
        '''
        if not path:
            return False
        sg.openExplorer(path)
    
    def exeOpenTempDir(self):
        r'''
            @brief  Tempディレクトリのオープン
            @return (any):
        '''       
        self.exeOpenDir(os.path.dirname(self.getImageSavePath()[0]))
    
    def exeOpenSetPathDir(self):
        r'''
            @brief  設定されているディレクトリパスのオープン
            @return (any):
        '''
        self.exeOpenDir(self.pathLine.text())
    
    def exeSetPathDialog(self):
        r'''
            @brief  ダイアログからパスをセット
            @return (any):
        '''
        dialog = QtWidgets.QFileDialog.getExistingDirectory(self)
        aft = self.pathLine.text() if not dialog else dialog
        self.pathLine.setText(aft)
    
    def exeClipboradToImage(self):
        r'''
            @brief  キャプチャされている画像をクリップボードに保存
            @return (any):
        '''
        pathData = self.getImageSavePath()
        item = pathData[0] if self.radioList[0].isChecked() else pathData[1]

        result = sg.imageCopy(item)
        if result:
            print(u'+ イメージをクリップボードに貼り付けました。')
        else:
            print(u'+ イメージをクリップボード貼り付けに失敗しました。')
    
    def exeExportCaptureImage(self):
        r'''
            @brief  指定されている先のパスにキャプチャ画像を書き出し
            @return (any):成功でTrue
        '''
        pathData = self.getImageSavePath()
        src = pathData[0] if self.radioList[0].isChecked() else pathData[1]
        dst = self.pathLine.text()
        
        if not os.path.isdir(dst):
            print(u'+ 書き出し先のディレクトリが見つかりません')
            print(u'\tPath : %s'%(dst))
            return False

        file,ext = os.path.splitext(src)
        file = os.path.basename(file).split('_') 
        dst  = os.path.join(dst,'%s_%s%s'%(file[0],file[1],ext))
        try:
            shutil.copy2(src,dst)
            print(u'+ Export to image data.')
            print(u'\tDst path : %s'%os.path.dirname(dst))
            print(u'\tDst name : %s'%os.path.basename(dst))
            return True
        except:
            print(u'+ 書き出しに失敗しました。')
            return False
    
    def exeFitImage(self):
        r'''
            @brief  リサイズした際にimageLabelをスケールする
            @return (any):
        '''
        if not self.image:
            return
        r = self.rect()
        pixmap = QtGui.QPixmap(self.image)
        newmap = pixmap.scaled(
            int(r.width()*self.imageMagni),int(r.height()*self.imageMagni),
            QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation
        )
        self.imageLabel.setPixmap(newmap)
            
class ImageOperationUI(sg.EventBaseWidget):
    r'''
        @brief    画像操作UI
        @inherit  sg.EventBaseWidget
        @function closeEvent     : 閉じるときのアクション
        @function resizeEvent    : 画面リサイズ時のアクション
        @function dragEnterEvent : ドラッグのイベント
        @function dropEvent      : ドロップのイベント
        @date     2018/10/09 10:36[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  UI作成のおおもと部分
            @param  parent(any) : enter description
            @return (any):
        '''
        super(ImageOperationUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/10/09'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(win_w,win_h)
        self.setAcceptDrops(True)
        
        win_w,win_h = 420,500
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        self.main = ImageOperationMainUI()
        self.main.setWindowSize(win_w,win_h)
        
        self.main.class_st = self
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(self.main)
        
    # Event ===================================================================
        
    def closeEvent(self, event):
        r'''
            @brief  閉じるときのアクション
            @param  event(any) : イベント格納変数
            @return (any):
        '''
        # tempに保存されたファイルの削除
        [self.main.deleteImagePath(p) for p in self.main.getImageSavePath()]
    
    def resizeEvent(self, event):
        r'''
            @brief  画面リサイズ時のアクション
            @param  event(any) : イベント格納変数
            @return (any):
        '''
        # imageLabelのフィット処理
        self.main.exeFitImage()
    
    def dragEnterEvent(self, event):
        r'''
            @brief  ドラッグのイベント
            @param  event(any) : イベントアクション
            @return (any):
        '''
        mime = event.mimeData()
        if mime.hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        r'''
            @brief  ドロップのイベント
            @param  event(any) : イベントアクション
            @return (any):
        '''
        mime = event.mimeData()
        path = mime.urls()
        for p in path:
            fp = p.toLocalFile()
            # ファイルパスの設定
            orgPath = os.path.dirname(fp) if os.path.isfile(fp) else fp
            self.main.pathLine.setText(orgPath)
    
    # func ====================================================================

# -----------------------------------------------------------------------------
# - modeling
# -----------------------------------------------------------------------------

class ModelingSynthesisToolMainUI(sg.ScrolledWidget):
    r'''
        @brief    レイアウト作成処理
        @inherit  sg.ScrolledWidget
        @function buildUI                : レイアウトコード
        @function exeImFunc              : 指定の起動関数へ渡すクッション関数
        @function exePopMenuCmd          : ホップメニュー窓口
        @function exeStartupSgt          : sculptGeometryToolの起動関数
        @function exeAverageVertex       : アベレージバーテックス適用
        @function exeAxisZeroMove        : axisZeroMoveの実行
        @function exeDuplicateReversal   : DuplicateMergeの実行
        @function exeOriginPositionCheck : originPositionCheckの実行
        @function exeFreeze              : setFreezeの実行
        @function exeNormalizedCv        : normalizedCvの実行
        @date     2018/11/12 09:33[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self,parent=None):
        r'''
            @brief  レイアウトコード
            @param  parent(any) : enter description
            @return (any):
        '''
        __SCHEMALIST = (
            [
                [
                    ['icon',1],[
                        'sgtButton','start sgt','modeling_sgt_v01',[24,24],
                        (u'sculptGeometryToolの起動')
                    ],
                ],
                [['stretch',1]],
            ],
            [
                [['spin',3],['aveVer',[1,10],1,1,(u'丸みのステップ数')]],
                [
                    ['button',1],['aveVer','ave',(u'averageVertexの実行')],
                    [False,[]],
                ],
            ],
            [
                [['combo',3],[
                    'axisZero',False,['x','y','z'],
                    (u'頂点エッジを指定の0位置に移動')]
                ],
                [
                    ['button',1],['axisZero','axis',(u'axisZeroMoveの実行')],
                    [False,[]],
                ],
            ],
            [
                [
                    ['button',1],['dupRev','dupRev',(
                        u'duplicateMergeの実行\n右クリックでメニューを表示')
                    ],
                    [True,['X','Y','Z','MergeX','MergeY','MergeZ']],
                ],
            ],
            [
                [['spin',3],['posChk',[1,50],10,1,(u'丸みのステップ数')]],
                [
                    ['button',1],['posChk','posChk',(
                        u'選択頂点のゼロ位置確認\n右クリックでメニューを表示')
                    ],
                    [True,['X','Y','Z']],
                ],
            ],
            [
                [
                    ['button',1],['freeze','freeze',(
                        u'freeze実行。\nデフォルトで全て右クリックで個別メニュー')
                    ],
                    [True,['translate','rotate','scale','joint']],
                ],
                [
                    ['button',1],['normalizeCv','norCv',(u'メッシュのCVの初期化')],
                    [True,['historyDelete']],
                ],
            ],
        )
        self.hLayout = []
        self.dict = {}
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setSpacing(4)
        
        for i,u in enumerate(__SCHEMALIST):
            hL = QtWidgets.QHBoxLayout()
            self.hLayout.append(hL)
            for i2,u2 in enumerate(u):
                if u2[0][0] == 'icon':
                    p = QtWidgets.QPushButton()
                    p.address = u2[1][0]
                    p.setStyleSheet(ss.BORDER_STYLE_2)
                    p.setToolTip(u2[1][-1])
                    p.setText(u2[1][1])
                    p.setIcon(msAppIcons.iconPath(icon=u2[1][2]))
                    p.setIconSize(QtCore.QSize(u2[1][3][0],u2[1][3][1]))
                    p.clicked.connect(self.exeImFunc)
                    hL.addWidget(p,u2[0][1])
                elif u2[0][0] == 'button':
                    p = QtWidgets.QPushButton(u2[1][1])
                    p.address = u2[1][0]
                    p.setToolTip(u2[1][-1])
                    p.clicked.connect(self.exeImFunc)
                    if u2[2][0]:
                        p.item    = u2[2][1] 
                        p.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                        p.customContextMenuRequested.connect(self.exePopMenuCmd)
                    hL.addWidget(p,u2[0][1])
                elif u2[0][0] == 'spin':
                    p = QtWidgets.QSpinBox()
                    p.setToolTip(u2[1][-1])
                    p.setRange(u2[1][1][0],u2[1][1][1])
                    p.setValue(u2[1][2])
                    p.setSingleStep(u2[1][3])
                    self.dict[u2[1][0]] = p
                    hL.addWidget(p,u2[0][1])
                elif u2[0][0] == 'combo':
                    p = QtWidgets.QComboBox()
                    p.address = u2[1][0]
                    p.setToolTip(u2[1][-1])
                    p.addItems(u2[1][2])
                    if u2[1][1]:
                        p.currentIndexChanged.connect(self.exeImFunc)
                    self.dict[u2[1][0]] = p
                    hL.addWidget(p,u2[0][1])
                else:
                    hL.addStretch(u2[0][1])
        
        [layout.addLayout(h) for h in self.hLayout]
        layout.addStretch()

    def exeImFunc(self):
        r'''
            @brief  指定の起動関数へ渡すクッション関数
            @return (any):
        '''
        s = self.sender()
        if s.address == 'sgtButton':
            self.exeStartupSgt()
        elif s.address == 'aveVer':
            self.exeAverageVertex(s.address)
        elif s.address == 'axisZero':
            self.exeAxisZeroMove(s.address)
        elif s.address == 'freeze':
            self.exeFreeze()
        elif s.address == 'normalizeCv':
            self.exeNormalizedCv()
    
    def exePopMenuCmd(self):
        r'''
            @brief  ホップメニュー窓口
            @return (any):
        '''
        s    = self.sender()
        menu = QtWidgets.QMenu()
        for i in s.item:
            if s.address == 'dupRev':
                mb = menu.addAction(i,self.exeDuplicateReversal)
                mb.menu = i
            elif s.address == 'posChk':
                mb = menu.addAction(i,self.exeOriginPositionCheck)
                mb.menu    = i
                mb.address = s.address
            elif s.address == 'freeze':
                mb = menu.addAction(i,self.exeFreeze)
                mb.menu = i
            elif s.address == 'normalizeCv':
                mb = menu.addAction(i,self.exeNormalizedCv)
                mb.menu = i
        menu.exec_(QtGui.QCursor.pos())
    
    def exeStartupSgt(self):
        r'''
            @brief  sculptGeometryToolの起動関数
            @return (any):
        '''
        try:
            mel.eval('artPuttyToolScript(4);ToolSettingsWindow();')
        except:
            print(u'scluptGeometryToolの起動に失敗')
    
    def exeAverageVertex(self,address):
        r'''
            @brief  アベレージバーテックス適用
            @param  address(any) : dictに保存された該当のウィジェットパーツのアドレス名
            @return (any):
        '''
        mayaFunc.applyAverageVertex(self.dict[address].value())
    
    def exeAxisZeroMove(self,address):
        r'''
            @brief  axisZeroMoveの実行
            @param  address(any) : dictに保存された該当のウィジェットパーツのアドレス名
            @return (any):
        '''
        mayaFunc.axisZeroMove(self.dict[address].currentText())
    
    def exeDuplicateReversal(self):
        r'''
            @brief  DuplicateMergeの実行
            @return (any):
        '''
        s = self.sender()
        axis   = s.menu[-1]
        m_flag = s.menu.lower().startswith('merge')
        mayaFunc.duplicateReversal(axis,merge=m_flag)
    
    def exeOriginPositionCheck(self):
        r'''
            @brief  originPositionCheckの実行
            @return (any):
        '''
        s = self.sender()
        mayaFunc.originPositionCheck(
            axis    =s.menu,
            accuracy=self.dict[s.address].value()
        )
    def exeFreeze(self):
        r'''
            @brief  setFreezeの実行
            @return (any):
        '''
        s = self.sender()
        tr,ro,sc,jo = False,False,False,False
        if isinstance(s.menu,bytes):
            if s.menu == 'translate':
                tr = True
            elif s.menu == 'rotate':
                ro = True
            elif s.menu == 'scale':
                sc = True
            elif s.menu == 'joint':
                jo = True
        else:
            tr,ro,sc = True,True,True
        mayaFunc.setFreeze(tr,ro,sc,jo)
    
    def exeNormalizedCv(self):
        r'''
            @brief  normalizedCvの実行
            @return (any):
        '''
        type = 2 if self.sender().menu == 'historyDelete' else 1
        mayaFunc.normalizedCv(type)
    
class ModelingSynthesisToolUI(sg.EventBaseWidget):
    r'''
        @brief    モデリングコマンド総合ツール
        @inherit  sg.EventBaseWidget
        @date     2018/11/12 09:30[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  ガワの設定
            @param  parent(any) : enter description
            @return (any):
        '''
        super(ModelingSynthesisToolUI,self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/11/12'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(140,400)
        
        main = ModelingSynthesisToolMainUI()
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}'%(uiName,ss.MAINUIBGC))
        
        we = sg.WidgetEventAction()
        we.setTitle('MST UI')
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)

# -----------------------------------------------------------------------------

class PointMovedConfigurationMainUI(sg.ScrolledWidget):
    r'''
        @brief    PointMovedConfigurationメイン部分
        @inherit  sg.ScrolledWidget
        @function buildUI           : 内部設定
        @function exePopMenuCmd     : ポップメニュー窓口
        @function setPivot          : ピポットの値から数値を代入
        @function exeClear          : 入力ラインの初期化
        @function exeMenuClear      : クリアーメニューの設定
        @function exeSetTranslate   : translate値のセット
        @function exeSetVertexPoint : vertexPoint値の中心点の値セット
        @function exeApply          : 実行
        @function exeMenu           : メニューからの実行
        @date     2018/02/05 14:06[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent=None):
        r'''
            @brief  内部設定
            @param  parent(any) : enter description
            @return (any):
        '''
        topPartsHLayout = QtWidgets.QHBoxLayout()
        
        buf = (u'のポイント位置です。')
        laftPartsVBoxLayout  = QtWidgets.QVBoxLayout()
        laftPartsVBoxLayout.setSpacing(8)
        xLayout = QtWidgets.QHBoxLayout()
        xLabel = QtWidgets.QLabel('X :')
        self.xLineEdit = QtWidgets.QLineEdit()
        self.xLineEdit.setToolTip(u'X%s' % (buf))
        self.xLineEdit.setStyleSheet('QLineEdit{background-color:#200;}')
        self.xLineEdit.menu = 'x'
        self.xLineEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.xLineEdit.customContextMenuRequested.connect(self.exeMenuClear)
        xLayout.addWidget(xLabel)
        xLayout.addWidget(self.xLineEdit)
        yLayout = QtWidgets.QHBoxLayout()
        yLabel = QtWidgets.QLabel('Y :')
        self.yLineEdit = QtWidgets.QLineEdit()
        self.yLineEdit.setToolTip(u'Y%s' % (buf))
        self.yLineEdit.setStyleSheet('QLineEdit{background-color:#020;}')
        self.yLineEdit.menu = 'y'
        self.yLineEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.yLineEdit.customContextMenuRequested.connect(self.exeMenuClear)
        yLayout.addWidget(yLabel)
        yLayout.addWidget(self.yLineEdit)
        zLayout = QtWidgets.QHBoxLayout()
        zLabel = QtWidgets.QLabel('Z :')
        self.zLineEdit = QtWidgets.QLineEdit()
        self.zLineEdit.setToolTip(u'Z%s' % (buf))
        self.zLineEdit.setStyleSheet('QLineEdit{background-color:#002;}')
        self.zLineEdit.menu = 'z'
        self.zLineEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.zLineEdit.customContextMenuRequested.connect(self.exeMenuClear)
        zLayout.addWidget(zLabel)
        zLayout.addWidget(self.zLineEdit)
            
        laftPartsVBoxLayout.addLayout(xLayout)
        laftPartsVBoxLayout.addLayout(yLayout)
        laftPartsVBoxLayout.addLayout(zLayout)
        laftPartsVBoxLayout.addStretch()
        
        rightPartsVBoxLayout = QtWidgets.QVBoxLayout()
        editHLayout = QtWidgets.QHBoxLayout()
        self.editCheckBox = QtWidgets.QCheckBox('Edit')
        self.editCheckBox.setToolTip(
            u'左記の入力の可不可を切り替えます。'
        )
        clearButton = QtWidgets.QPushButton('Clear')
        clearButton.setToolTip(
            u'入力ラインの数値を初期化します。'
        )
        clearButton.clicked.connect(self.exeClear)
        clearButton.type = 'all'
        editHLayout.addWidget(self.editCheckBox)
        editHLayout.addWidget(clearButton)
        translateButton = QtWidgets.QPushButton('Translate')
        translateButton.address = 'pivot'
        translateButton.setToolTip(
            u'ノードのtranslate情報を入力します。'
        )
        translateButton.clicked.connect(self.exeSetTranslate)
        translateButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        translateButton.customContextMenuRequested.connect(self.exePopMenuCmd)
        vertexPointButton = QtWidgets.QPushButton('VertexPoint')
        vertexPointButton.setToolTip(
            u'頂点情報の中心点の情報を入力します。'
        )
        vertexPointButton.clicked.connect(self.exeSetVertexPoint)
        rightPartsVBoxLayout.addLayout(editHLayout)
        rightPartsVBoxLayout.addWidget(translateButton)
        rightPartsVBoxLayout.addWidget(vertexPointButton)
        rightPartsVBoxLayout.addStretch()
        
        topPartsHLayout.addLayout(laftPartsVBoxLayout)
        topPartsHLayout.addLayout(rightPartsVBoxLayout)
        
        applyButton = QtWidgets.QPushButton('Apply')
        applyButton.setToolTip(
            u'右クリックで個別メニューを表示します。'
        )
        applyButton.clicked.connect(self.exeApply)
        applyButton.type = 'positionMove'
        applyButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        applyButton.customContextMenuRequested.connect(self.exeMenu)
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setSpacing(4)
        layout.addLayout(topPartsHLayout)
        layout.addWidget(applyButton)
        
        for le in [self.xLineEdit,self.yLineEdit,self.zLineEdit]:
            le.setText('0.%s' % ('0'*10))
            le.setEnabled(False)
            self.editCheckBox.toggled.connect(le.setEnabled)

    # -------------------------------------------------------------------------
    
    def exePopMenuCmd(self):
        r'''
            @brief  ポップメニュー窓口
            @return (any):
        '''
        s = self.sender()
        menu = QtWidgets.QMenu()
        if s.address == 'pivot':
            m = menu.addAction(s.address.capitalize(),self.setPivot)
        menu.exec_(QtGui.QCursor.pos())
    
    # -------------------------------------------------------------------------
            
    def setPivot(self):
        r'''
            @brief  ピポットの値から数値を代入
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            print(u'+ 何も選択されていません。')
            return
        r_attr = '%s.rotatePivot'%(sel[0])
        s_attr = '%s.scalePivot' %(sel[0])
        if not cmds.objExists(r_attr) or not cmds.objExists(s_attr):
            print(u'+ ピポットアトリビュートが存在しません。')
            return
        r_param = cmds.getAttr(r_attr)
        s_param = cmds.getAttr(s_attr)
        sum = None
        if r_param == s_param:
            sum = r_param
        else:
            sum = []
            for x in zip(r_param,s_param):
                v = ((x[0]+x[1])//2)
                sum.append(v)
        try:
            self.xLineEdit.setText(str(round(sum[0][0],10)))
            self.yLineEdit.setText(str(round(sum[0][1],10)))
            self.zLineEdit.setText(str(round(sum[0][2],10)))
        except:
            z = '0.%s'%('0'*10)
            self.xLineEdit.setText(z)
            self.yLineEdit.setText(z)
            self.zLineEdit.setText(z)
            
    def exeClear(self):
        r'''
            @brief  入力ラインの初期化
            @return (any):
        '''
        forList = []
        type = self.sender()
        
        if type.type == 'all':
            forList = [self.xLineEdit,self.yLineEdit,self.zLineEdit]
        elif type.type.startswith('each'):
            if type.type.endswith('x'):
                forList = [self.xLineEdit]
            elif type.type.endswith('y'):
                forList = [self.yLineEdit]
            elif type.type.endswith('z'):
                forList = [self.zLineEdit]
            else:
                print(u'+ each_の最後の文字が適切ではありません。')
                return
        else:
            print(u'+ 条件分岐となる変数が適切ではありません。')
            return
        
        try:
            for le in forList:
                le.setText('0.%s' % ('0'*10))
        except:
            print(u'+ 入力ラインの初期化に失敗しました。')
            
    def exeMenuClear(self):
        r'''
            @brief  クリアーメニューの設定
            @return (any):
        '''
        menuType = self.sender()
        
        menu = QtWidgets.QMenu()
        if menuType.menu == 'x':
            x = menu.addAction('X:Clear', self.exeClear)
            x.type = 'each_x'
        elif menuType.menu == 'y':
            y = menu.addAction('Y:Clear', self.exeClear)
            y.type = 'each_y'
        elif menuType.menu == 'z':
            z = menu.addAction('Z:Clear', self.exeClear)
            z.type = 'each_z'
        menu.exec_(QtGui.QCursor.pos())
            
    def exeSetTranslate(self):
        r'''
            @brief  translate値のセット
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            print(u'+ 何も選択されていません。')
            return
            
        attr = '%s.t' % (sel[0])
        if not cmds.objExists(attr):
            print(u'+ translateのアトリビュートが存在しません')
            return
        
        t = cmds.getAttr(attr)
        try:
            self.xLineEdit.setText(str(round(t[0][0],10)))
            self.yLineEdit.setText(str(round(t[0][1],10)))
            self.zLineEdit.setText(str(round(t[0][2],10)))
        except:
            z = '0.%s'%('0'*10)
            self.xLineEdit.setText(z)
            self.yLineEdit.setText(z)
            self.zLineEdit.setText(z)
        
    def exeSetVertexPoint(self):
        r'''
            @brief  vertexPoint値の中心点の値セット
            @return (any):
        '''
        loop = 0
        xp,yp,zp = [],[],[]
        
        savePoint = cmds.ls(sl=True,fl=True)
        if not savePoint:
            return
        
        try:
            for sp in savePoint:
                pv = cmds.pointPosition(sp)
                xp.append(pv[0])
                yp.append(pv[1])
                zp.append(pv[2])
                loop += 1
        except:
            print(u'+ 選択されているものがvertexではない可能性があります。')
            return
        
        ([lb.setText(str(round(((min(nb)+max(nb))*0.5),5))) for nb,lb in
            [(xp,self.xLineEdit),(yp,self.yLineEdit),(zp,self.zLineEdit)]])

    def exeApply(self):
        r'''
            @brief  実行
            @return (any):
        '''
        menuType = self.sender()
        xp = float(self.xLineEdit.text())
        yp = float(self.yLineEdit.text())
        zp = float(self.zLineEdit.text())
        cmds.undoInfo(ock=True)
        if menuType.type == 'positionMove':
            ([cmds.move(xp,yp,zp,s,a=True) for s in cmds.ls(sl=True)])
        elif menuType.type == 'joint':
            joint = cmds.joint()
            cmds.move(xp,yp,zp,joint,a=True)
        elif menuType.type == 'locator':
            loc = cmds.spaceLocator()
            cmds.move(xp,yp,zp,loc,a=True)
        elif menuType.type == 'centerMerge':
            for s in cmds.ls(sl=True, fl=True):
                fil = cmds.filterExpand(s,sm=31,ex=True)
                cmds.move(xp,yp,zp,fil,a=True) if fil else None
            mel.eval('MergeToCenter();')
        cmds.undoInfo(cck=True)
            
    def exeMenu(self):
        r'''
            @brief  メニューからの実行
            @return (any):
        '''
        menu = QtWidgets.QMenu()
        j  = menu.addAction('Joint', self.exeApply)
        l  = menu.addAction('Locator', self.exeApply)
        cm = menu.addAction('CenterMerge', self.exeApply)
        j.type  = 'joint'
        l.type  = 'locator'
        cm.type = 'centerMerge'
        menu.exec_(QtGui.QCursor.pos())
            
class PointMovedConfigurationUI(sg.EventBaseWidget):
    r'''
        @brief    選択ノードの中心位置に対してアクションを行うUI
        @inherit  sg.EventBaseWidget
        @date     2018/02/05 14:06[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  ガワの設定
            @param  parent(any) : enter description
            @return (any):
        '''
        super(PointMovedConfigurationUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.2a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/02/05'
        self.update  = '2019/04/25'
        self.setWindowTitle(self.claName)
        self.resize(260,180)
        
        main = PointMovedConfigurationMainUI()
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)

# -----------------------------------------------------------------------------

class TemplateSettingMainUI(sg.ScrolledWidget):
    r'''
        @brief    テンプレート設定UIのレイアウト部分
        @inherit  sg.ScrolledWidget
        @function buildUI                : enter description
        @function exeCommandImFunc       : 通常コマンドの窓口関数
        @function exeButtonMenu          : ボタンメニューの窓口
        @function exeMenuToFunc          : メニューから関数を実行するクッション関数
        @function setDebugFlag           : デバックフラグのスイッチ
        @function confirmMatchCheck      : optionVarとセルフ変数のリストチェック
        @function updateNode             : optionVarに設定されているノードでまだテンプレート化されているノードの区別
        @function setNode                : ノードをセルフ変数に格納
        @function exclusionNode          : ノードをセルフ変数から除外
        @function getNode                : セルフ変数に格納されたノードのリターン
        @function clearNode              : セルフ変数の初期化
        @function setOptionVar           : オプションバーを指定形式でセット
        @function getOptionVar           : オプションバーの中身を配列でリターン
        @function clearOptionVar         : オプションバーをリセット
        @function existsOptionVar        : オプションバーの存在の確認
        @function setTemplate            : オブジェクトのテンプレート化
        @function exePrintOptionVarList  : optionVarに設定されているノードリストのプリント
        @function setTempNodeSelect      : セットされているノードの選択
        @function exeSetTemplate         : 選択ノードのtemplate化
        @function exeReleaseTemplate     : 選択ノードのテンプレート解除
        @function exeToolReleaseTemplate : このツールでテンプレート化されたノードのアンテンプレート
        @function exeViewReleaseTemplate : ビュー内にあるノードのテンプレートを解除
        @function exeAllReleaseTemplate  : シーン内のテンプレートオブジェクトを全て解除
        @date     2018/10/17 11:12[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent=None):
        r'''
            @brief  enter description
            @param  parent(any) : enter description
            @return (any):
        '''
        self.optionVarName     = 'msTemplateSettingUI_ovnString'
        self.optionVarNodeList = []
        self.debugFlag = False
        
        __SCHEMALIST = [
            ['Set',['menu',True,['No saved set','Set temp select']],['isEnabled',True],(
                u'選択したオブジェクトをTemplate化します。\n'
                u'複数選択した場合は選択した全てのオブジェクトが対象です。\n'
                u'Template化できないオブジェクト又は'
                u'ロックされているものはスキップされます。\n'
                u'右クリックでノードを保存しないモードでテンプレート出来ます。\n'
                u'ショートカット : Ctrl+Shift+Z'
            ),],
            ['Release',['menu',True,['Set temp select']],['isEnabled',True],(
                u'選択したオブジェクトのTemplateを解除します。'
                u'複数選択した場合は選択した全てのオブジェクトが対象です。\n'
                u'既にTemplateが解除されている又はロックされているオブジェクトは'
                u'スキップされます。\n'
                u'ショートカット : Ctrl+Shift+X'
            ),],
            ['ToolRelease',['menu',True,['PrintOptionVarList']],['isEnabled',True],(
                u'選択状態問わずこのツールでTemplateSetされたオブジェクト全ての'
                u'状態を解除します。\n'
                u'シーン上に存在するノードし且つSet時にoptionVarに設定されたノードが'
                u'対象です。\n'
                u'右クリックのメニューで登録されているオブジェクトリストを確認できます。\n'
                u'ショートカット : Ctrl+Shift+C'
            ),],
            ['ViewRelease',['menu',False,['']],['isEnabled',True],(
                u'選択状態問わずビュー内に表示されているノードのTemplate'
                u'状態を解除します。\n'
                u'ショートカット : Ctrl+Shift+V'
            ),],
            ['AllRelease',['menu',False,['']],['isEnabled',True],(
                u'選択状態問わずシーン内に表示されているノードのTemplate'
                u'状態を解除します。\n'
                u'ショートカット : Ctrl+Shift+B'
            ),],
        ]
        
        label = QtWidgets.QLabel(u'Template command list')
        
        buttonLayout = QtWidgets.QHBoxLayout()
        for i,u in enumerate(__SCHEMALIST):
            b = QtWidgets.QPushButton(u[0])
            b.address = u[0]
            b.setToolTip(u[-1])
            if u[1][1]:
                b.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                b.customContextMenuRequested.connect(self.exeButtonMenu)
                b.menuAddress = u[1][2]
            b.setEnabled(u[2][1])
            b.clicked.connect(self.exeCommandImFunc)
            buttonLayout.addWidget(b)
            
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addWidget(label)
        layout.addLayout(buttonLayout)
        
        self.updateNode()
    
    # ---------------------------------
    
    def exeCommandImFunc(self):
        r'''
            @brief  通常コマンドの窓口関数
            @return (any):
        '''
        s = self.sender()
        if s.address == 'Set':
            self.exeSetTemplate(True)
        elif s.address == 'Release':
            self.exeReleaseTemplate()
        elif s.address == 'ToolRelease':
            self.exeToolReleaseTemplate()
        elif s.address == 'ViewRelease':
            self.exeViewReleaseTemplate()
        elif s.address == 'AllRelease':
            self.exeAllReleaseTemplate()
     
    def exeButtonMenu(self):
        r'''
            @brief  ボタンメニューの窓口
            @return (any):
        '''
        menu = QtWidgets.QMenu()
        for ad in self.sender().menuAddress:
            m = menu.addAction(ad,self.exeMenuToFunc)
            m.address = ad
        menu.exec_(QtGui.QCursor.pos())
    
    def exeMenuToFunc(self):
        r'''
            @brief  メニューから関数を実行するクッション関数
            @return (any):
        '''
        s = self.sender()
        if s.address == 'PrintOptionVarList':
            self.exePrintOptionVarList()
        elif s.address == 'No saved set':
            self.exeSetTemplate(False)
        elif s.address == 'Set temp select':
            self.setTempNodeSelect()
    
    # ---------------------------------
    
    def setDebugFlag(self,value=True):
        r'''
            @brief  デバックフラグのスイッチ
            @param  value(any) : True or False
            @return (any):
        '''
        self.debugFlag = value
        print(u'Debug mode = %s'%(str(value)))
    
    def confirmMatchCheck(self):
        r'''
            @brief  optionVarとセルフ変数のリストチェック
            @return (any):
        '''
        if self.debugFlag:
            print(u'+ self変数')
            print('\t%s'%(self.optionVarNodeList))
            print(u'+ optionVar')
            print('\t%s'%(self.getOptionVar()))
    
    def updateNode(self):
        r'''
            @brief  optionVarに設定されているノードでまだテンプレート化されているノードの区別
            @return (any):
        '''
        opn = self.getOptionVar()
        if not opn:
            return
        for n in opn:
            node = '%s.template'%(n)
            if not cmds.objExists(node):
                continue
            attr = cmds.getAttr(node)
            if attr:
                self.setNode([n])
        self.setOptionVar(node=self.getNode())
    
    def setNode(self, node=[]):
        r'''
            @brief  ノードをセルフ変数に格納
            @param  node(any) : 選択ノード
            @return (any):
        '''
        for n in node:
            if n == '':
                continue
            if not n in self.optionVarNodeList:
                self.optionVarNodeList.append(n)
    
    def exclusionNode(self, node=[]):
        r'''
            @brief  ノードをセルフ変数から除外
            @param  node(any) : 選択ノード
            @return (any):
        '''
        for n in node:
            if n in self.optionVarNodeList:
                self.optionVarNodeList.remove(n)
    
    def getNode(self):
        r'''
            @brief  セルフ変数に格納されたノードのリターン
            @return (any):
        '''
        return self.optionVarNodeList
    
    def clearNode(self):
        r'''
            @brief  セルフ変数の初期化
            @return (any):
        '''
        self.optionVarNodeList = []
    
    def setOptionVar(self, node=[]):
        r'''
            @brief  オプションバーを指定形式でセット
            @param  node(any) : [list]ノードリスト
            @return (any):
        '''
        returnList = None
        
        if not node:
            self.clearOptionVar()
            return True
        
        nodeList = ''
        for n in node:
            if n == '':
                continue
            nodeList += '%s,'%(n)
        try:
            cmds.optionVar(sv=[self.optionVarName, nodeList])
            returnList = True
        except:
            returnList = False
        
        return nodeList
    
    def getOptionVar(self):
        r'''
            @brief  オプションバーの中身を配列でリターン
            @return (any):list
        '''
        r = cmds.optionVar(q=self.optionVarName)
        if r:
            s = r.split(',')
            if s[-1] == '':
                return s[0:-1]
            else:
                return s
        else:
            return []
    
    def clearOptionVar(self):
        r'''
            @brief  オプションバーをリセット
            @return (any):
        '''
        cmds.optionVar(remove=self.optionVarName)
        
    def existsOptionVar(self):
        r'''
            @brief  オプションバーの存在の確認
            @return (any):
        '''
        return cmds.exists(remove=self.optionVarName)
    
    def setTemplate(self, node=[], type=0):
        r'''
            @brief  オブジェクトのテンプレート化
            @param  node(any) : ノードリスト
            @param  type(any) : 1=ON, 2=Off, other=NoAction
            @return (any):
        '''
        if not node:
            return False
        
        mayaFunc.setUndoInfo(True)
        for n in node:
            tempName = '%s.template'%(n)
            if not cmds.objExists(tempName):
                continue
            try:
                cmds.setAttr(tempName,type)
            except:
                pass
        mayaFunc.setUndoInfo(False)
    
    def exePrintOptionVarList(self):
        r'''
            @brief  optionVarに設定されているノードリストのプリント
            @return (any):
        '''
        opn = self.getOptionVar()
        if not opn:
            return
        
        print(u'+ OptionVar setting node list.')
        for n in opn:
            print(u'\t%s'%(n))
    
    # ---------------------------------
    
    def setTempNodeSelect(self):
        r'''
            @brief  セットされているノードの選択
            @return (any):
        '''
        node = self.getNode()
        if not node:
            return
        cmds.select(node,r=True)
    
    # ---------------------------------
    
    def exeSetTemplate(self,save=True):
        r'''
            @brief  選択ノードのtemplate化
            @param  save(any) : enter description
            @return (any):
        '''
        log = (u'+ Not save mode.')
        sel = cmds.ls(sl=True)
        if not sel:
            return False
        if save:
            self.setNode(sel)
            self.setOptionVar(node=self.getNode())
            log = (u'+ Save mode.')
        self.setTemplate(node=sel,type=1)
        print(log)
        self.confirmMatchCheck()
    
    def exeReleaseTemplate(self):
        r'''
            @brief  選択ノードのテンプレート解除
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            return False
        self.exclusionNode(sel)
        organizeNode = self.getNode()
        self.setTemplate(node=sel,type=0)
        self.setOptionVar(node=organizeNode)
        self.confirmMatchCheck()
    
    def exeToolReleaseTemplate(self):
        r'''
            @brief  このツールでテンプレート化されたノードのアンテンプレート
            @return (any):
        '''
        self.setTemplate(node=self.getNode(),type=2)
        self.clearNode()
        self.setOptionVar(node=self.getNode())
        self.confirmMatchCheck()
    
    def exeViewReleaseTemplate(self):
        r'''
            @brief  ビュー内にあるノードのテンプレートを解除
            @return (any):
        '''
        mayaFunc.activeViewSelect(mode='template')
        sel = cmds.ls(sl=True)
        if not sel:
            return False
        self.exclusionNode(sel)
        organizeNode = self.getNode()
        self.setTemplate(node=sel,type=0)
        self.setOptionVar(node=organizeNode)
        cmds.select(cl=True)
        self.confirmMatchCheck()
    
    def exeAllReleaseTemplate(self):
        r'''
            @brief  シーン内のテンプレートオブジェクトを全て解除
            @return (any):
        '''
        sel = cmds.ls()
        if not sel:
            return
        self.setTemplate(node=sel,type=0)
        self.clearNode()
        self.setOptionVar(node=self.getNode())
        self.confirmMatchCheck()
    
class TemplateSettingUI(sg.EventBaseWidget):
    r'''
        @brief    テンプレート設定のUI
        @inherit  sg.EventBaseWidget
        @function keyPressEvent : キープレス時のイベント情報
        @date     2018/10/17 10:55[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  enter description
            @param  parent(any) : enter description
            @return (any):
        '''
        super(TemplateSettingUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.0a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/10/17'
        self.update  = '2019/04/12'
        
        self.setWindowTitle(self.claName)
        self.resize(400,80)
        
        self.main = TemplateSettingMainUI()
        
        uiName = 'ms%s'%(self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}'%(uiName, ss.MAINUIBGC))
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(self.main)
    
    # Event ===================================================================

    def keyPressEvent(self, event):
        r'''
            @brief  キープレス時のイベント情報
            @param  event(any) : enter description
            @return (any):
        '''
        key  = self.getKeyType(event)
        mask = self.getKeyMask()
        
        if   (key['mod1'] == mask['ctrl,shift'] and key['press'] == 'Z'):
            self.main.exeSetTemplate()
        elif (key['mod1'] == mask['ctrl,shift'] and key['press'] == 'X'):
            self.main.exeReleaseTemplate()
        elif (key['mod1'] == mask['ctrl,shift'] and key['press'] == 'C'):
            self.main.exeToolReleaseTemplate()
        elif (key['mod1'] == mask['ctrl,shift'] and key['press'] == 'V'):
            self.main.exeViewReleaseTemplate()
        elif (key['mod1'] == mask['ctrl,shift'] and key['press'] == 'B'):
            self.main.exeAllReleaseTemplate()
        elif (key['mod1'] == mask['ctrl,shift'] and key['press'] == 'F11'):
            self.setDebugFlag(True)
        elif (key['mod1'] == mask['ctrl,shift'] and key['press'] == 'F12'):
            self.setDebugFlag(False)

# -----------------------------------------------------------------------------
            
class ModelingPaperPatternMainUI(sg.ScrolledWidget):
    r'''
        @brief    ModelingPaperPatternUIメイン記述
        @inherit  sg.ScrolledWidget
        @function buildUI                   : レイアウト部分
        @function saveBaseNameSave          : baseNodeをself変数に保存
        @function readBaseNameSave          : enter description
        @function saveDetachNode            : デタッチノードの保存
        @function readDetachNode            : デタッチノードの返し
        @function exeObjectDuplicate        : 選択オブジェクトの複製
        @function exeBaseNameSave           : baseNodeを保存します。
        @function exeDetachEdge             : エッジのデタッチを行います
        @function exeDetachNodeSave         : 選択オブジェクトをデタッチオブジェクトとして保存
        @function exeRenameToNCloth         : エッジデタッチしたノードをnCloth用のオブジェクトに変換コピー
        @function exeApplyNCloth            : デタッチノードをnCloth化する
        @function exeNClothNodeCopy         : nclothで平らになったノードをコピーする関数
        @function exeMapping                : 平べったくなったノードオブジェクトをY軸でマッピング
        @function exeTransferAttribute      : transferAttributeの設定
        @function exeOpenUVTextureEditor    : uv texture editorを起動
        @function exeEditMeshDuplicate      : 平べったくなったeditMeshを複製します。
        @function exeCreatePlane            : プレーンの作成
        @function exeEdgeToCurve            : 選択エッジからカーブを生成
        @function exeFlatPlaneSplit         : flatPlaneの分割数を変更します。
        @function exeCreateProjectCurve     : projectcurveを作成します。
        @function exeConvertProjectionCurve : 作成したprojectioncurveをプレーン投影します。
        @date     2018/02/27 15:44[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    
    det = 'detach'
    ncl = 'nCloth'
    sms = 'simMesh'
    edt = 'edit'
    edd = 'editDup'
    flp = 'flatPlane'
    ccv = 'createCurve'
    ppc = 'projectionCurve'
    fnp = 'finishPlane'
    
    def buildUI(self, parent=None):
        r'''
            @brief  レイアウト部分
            @param  parent(any) : enter description
            @return (any):
        '''
        # 1
        basedupLayout = QtWidgets.QHBoxLayout()
        basedupLabel = QtWidgets.QLabel(
            u'Duplicate the first selected node :'
        )
        basedupLabel.setToolTip(
            u'最初に選択したノードを複製します。'
        )
        basedupButton = QtWidgets.QPushButton('Original Duplicate')
        basedupButton.clicked.connect(self.exeObjectDuplicate)
        self.basedupSaveButton = QtWidgets.QPushButton('BaseNode Save')
        self.basedupSaveButton.setToolTip(
            u'baseノードをセーブします。\n'
            u'セーブ後はボタンカラーが変わります。'
        )
        self.basedupSaveButton.clicked.connect(self.exeBaseNameSave)
        basedupLayout.addWidget(basedupButton)
        basedupLayout.addWidget(self.basedupSaveButton)
        
        # 2
        inputLineLayout = QtWidgets.QHBoxLayout()
        inputLabel = QtWidgets.QLabel('Select the edge to detach :')
        inputLabel.setToolTip(
            u'デタッチするエッジを選択します。'
        )
        inputDetachButton = QtWidgets.QPushButton('Detach')
        inputDetachButton.setToolTip(
            u'エッジをデタッチします。'
        )
        inputDetachButton.clicked.connect(self.exeDetachEdge)
        self.inputSaveButton = QtWidgets.QPushButton('Detach Save')
        self.inputSaveButton.setToolTip(
            u'デタッチノード情報を保存します。\n'
            u'セーブ後はボタンカラーが変わります。'
        )
        self.inputSaveButton.clicked.connect(self.exeDetachNodeSave)
        inputCopyButton = QtWidgets.QPushButton('Detach Copy')
        inputCopyButton.setToolTip(
            u'デタッチノードに指定されたノードをコピーします。'
        )
        inputCopyButton.clicked.connect(self.exeRenameToNCloth)
        inputLineLayout.addWidget(inputDetachButton)
        inputLineLayout.addWidget(self.inputSaveButton)
        inputLineLayout.addWidget(inputCopyButton)
        
        # 3
        nclothLayout = QtWidgets.QHBoxLayout()
        nclothLabel = QtWidgets.QLabel('nCloth conversion :')
        nclothButton = QtWidgets.QPushButton('to nCloth')
        nclothButton.setToolTip(
            u'末尾に[nCloth]がついたノードをncloth化します。'
        )
        nclothButton.clicked.connect(self.exeApplyNCloth)
        nclothCopyButton = QtWidgets.QPushButton('Flat Node Copy')
        nclothCopyButton.setToolTip(
            u'フラットになったnclothノードをコピーしてください。'
        )
        nclothCopyButton.clicked.connect(self.exeNClothNodeCopy)
        nclothLayout.addWidget(nclothButton)
        nclothLayout.addWidget(nclothCopyButton)
        
        # 4
        mappingLayout = QtWidgets.QHBoxLayout()
        mappingLabel = QtWidgets.QLabel(u'Set mapping :')
        mappingLabel.setToolTip(
            u'平べったくなったノードをUVマッピングして整理し\n'
            u'デタッチオブジェクトへUVを転写します。'
        )
        mappingButton = QtWidgets.QPushButton('Y Mapping')
        mappingButton.setToolTip(
            u'Y軸からノードをUVをマッピングします。'
        )
        mappingButton.clicked.connect(self.exeMapping)
        mappingTransferUVButton = QtWidgets.QPushButton('Transfer UV')
        mappingTransferUVButton.setToolTip(
            u'Transfer UV to Detach Node.\n'
            u'UVを調整した["base"+_edit]ノードと["base"+_detach]を用意して実行してください。'
        )
        mappingTransferUVButton.order = 1
        mappingTransferUVButton.clicked.connect(self.exeTransferAttribute)
        uvTexEditorButton = QtWidgets.QPushButton('UV Texture Editor')
        uvTexEditorButton.setToolTip(
            u'UVTextureEditorを開きます。'
        )
        uvTexEditorButton.clicked.connect(self.exeOpenUVTextureEditor)
        mappingLayout.addWidget(mappingButton)
        mappingLayout.addWidget(mappingTransferUVButton)
        mappingLayout.addWidget(uvTexEditorButton)
        
        # 5
        borderingLayout = QtWidgets.QHBoxLayout()
        borderingLabel = QtWidgets.QLabel(u'Bordering node :')
        borderingLabel.setToolTip(
            u'プレーンノードにUVを縁取ってモデルを作ります。'
        )
        borderingDupButton = QtWidgets.QPushButton('EditMesh dup')
        borderingDupButton.setToolTip(
            u'editメッシュを複製します。\n'
            u'1.BaseNodeをSaveしてください。\n'
            u'2.[1]を設定したらこのボタンを実行してください。'
        )
        borderingDupButton.clicked.connect(self.exeEditMeshDuplicate)
        borderingPlaneButton = QtWidgets.QPushButton('Create plane')
        borderingPlaneButton.setToolTip(
            u'平面プレーンを作成します。\n'
            u'BaseNodeをSaveし、[BaseNode]名でプレーンが名前付けられ実行されます。'
        )
        borderingPlaneButton.clicked.connect(self.exeCreatePlane)
        borderingTransferButton = QtWidgets.QPushButton('Transfer plane')
        borderingTransferButton.order = 2
        borderingTransferButton.setToolTip(
            u'Planeにeditメッシュを移動させます。\n'
            u'（UVの大きさが1*1なのでPlaneの大きさにちょうど合うようになってます）'
        )
        borderingTransferButton.clicked.connect(self.exeTransferAttribute)
        borderingLayout.addWidget(borderingDupButton)
        borderingLayout.addWidget(borderingPlaneButton)
        borderingLayout.addWidget(borderingTransferButton)
        
        # 6a
        modelingLayoutA = QtWidgets.QHBoxLayout()
        modelingLabel = QtWidgets.QLabel(u'Plain UV modeling :')
        modelingLabel.setToolTip(
            u'UVの形に合わせたノードを使い分割モデルのモデリングを行います。'
        )
        modelingEdgeToCurveButton = QtWidgets.QPushButton('Edge to Curve')
        modelingEdgeToCurveButton.setToolTip(
            u'エッジを選択してカーブを作成します。\n'
            u'1.[base_editDup]ノードのそれぞれのモデルの外側のエッジを選択'
            u'2.当ボタンを実行してカーブを生成します。'
        )
        modelingEdgeToCurveButton.clicked.connect(self.exeEdgeToCurve)
        modelingSpinBoxLabel = QtWidgets.QLabel(u'Split :')
        self.modelingSpinBox = QtWidgets.QSpinBox()
        self.modelingSpinBox.setToolTip(
            u'プレーンの分割数を決めます。\n'
            u'下限=1,上限=100'
        )
        self.modelingSpinBox.setValue(50)
        self.modelingSpinBox.setRange(1,100)
        self.modelingSpinBox.setSingleStep(1)
        modelingSpinBoxButton = QtWidgets.QPushButton('-> Split Apply')
        modelingSpinBoxButton.setToolTip(
            u'指定した分割数でflatPlaneの分割数を変更します。'
        )
        modelingSpinBoxButton.clicked.connect(self.exeFlatPlaneSplit)
        modelingLayoutA.addWidget(modelingEdgeToCurveButton)
        modelingLayoutA.addWidget(modelingSpinBoxLabel)
        modelingLayoutA.addWidget(self.modelingSpinBox)
        modelingLayoutA.addWidget(modelingSpinBoxButton)
        
        # 6b
        modelingLayoutB = QtWidgets.QHBoxLayout()
        modelingBlankLabel = QtWidgets.QLabel(u'               ')
        modelingProjectCurveButton = QtWidgets.QPushButton(u'Project curve')
        modelingProjectCurveButton.setToolTip(
            u'作成したカーブを抽出してprojectcurveを作成します。\n'
            u'1.["baseNameNode"+_flatPlane]と["baseNameNode"+_createCurve#]を作成してください。\n'
            u'2.上記2つ（カーブは複数ある場合あり）があるとき、このコマンドが実行できます。'
        )
        modelingProjectCurveButton.clicked.connect(self.exeCreateProjectCurve)
        modelingConvertProjectionButton = QtWidgets.QPushButton('Convert curve')
        modelingConvertProjectionButton.setToolTip(
            u'flatPlaneに変換したprojectionCurveを投影した新しいplaneを作成します。\n'
            u'1.["baseNameNode"+_flatPlane]と["baseNameNode"+_projectionCurve#]があることを確認してください。\n'
            u'2.上記がある場合、このコマンドが実行できます。'
        )
        modelingConvertProjectionButton.clicked.connect(self.exeConvertProjectionCurve)
        modelingFinishTransferButton = QtWidgets.QPushButton('Finish transfer')
        modelingFinishTransferButton.order = 3
        modelingFinishTransferButton.setToolTip(
            u'余剰なフェースを削除したfinishPlaneをdetachNodeの形状に合わせます。'
        )
        modelingFinishTransferButton.clicked.connect(self.exeTransferAttribute)
        modelingLayoutB.addWidget(modelingProjectCurveButton)
        modelingLayoutB.addWidget(modelingConvertProjectionButton)
        modelingLayoutB.addWidget(modelingFinishTransferButton)
        
        # from
        layout = QtWidgets.QFormLayout(parent)
        layout.addRow(basedupLabel,basedupLayout)
        layout.addRow(inputLabel,inputLineLayout)
        layout.addRow(nclothLabel,nclothLayout)
        layout.addRow(mappingLabel,mappingLayout)
        layout.addRow(borderingLabel,borderingLayout)
        layout.addRow(modelingLabel,modelingLayoutA)
        layout.addRow(modelingBlankLabel,modelingLayoutB)

    def saveBaseNameSave(self, node):
        r'''
            @brief  baseNodeをself変数に保存
            @param  node(any) : enter description
            @return (any):
        '''
        self.baseName = node
        self.basedupSaveButton.setStyleSheet(
            'QPushButton{background-color:#FFD700;color:#222;}'
        )
        self.basedupSaveButton.setToolTip(
            u'現在["%s"]がセーブされています。' % (node)
        )
        print(u'+ [self.baseName = "%s"] save.' % node)
    
    def readBaseNameSave(self):
        # type: () -> None
        r'''
            @brief  enter description
            @return (None):成功しなかったらNone
        '''
        try:
            return self.baseName
        except:
            return None
            
    def saveDetachNode(self, node):
        r'''
            @brief  デタッチノードの保存
            @param  node(any) : エッジでタッチノードの保存
            @return (any):
        '''
        self.detachNode = node
        self.inputSaveButton.setStyleSheet(
            'QPushButton{background-color:#D2691E;color:#222;}'
        )
        self.inputSaveButton.setToolTip(
            u'現在デタッチノードに["%s"]がセットされています。' % (node)
        )
        print(u'+ [self.detachNode = "%s"] save.' % node)
    
    def readDetachNode(self):
        # type: () -> None
        r'''
            @brief  デタッチノードの返し
            @return (None):成功しなかったらNone
        '''
        try:
            return self.detachNode
        except:
            return None
        
    def exeObjectDuplicate(self):
        r'''
            @brief  選択オブジェクトの複製
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            print(u'+ 何も選択されていないため処理を終了します。')
            return
        sel = sel[0]
        
        cmds.undoInfo(ock=True)
        
        detach = cmds.duplicate(sel, n='%s_%s' % (sel, self.det))
        cmds.setAttr('%s.v' % (sel), 0)
        
        cmds.undoInfo(cck=True)
        
        self.saveBaseNameSave(node=sel)
        
    def exeBaseNameSave(self):
        r'''
            @brief  baseNodeを保存します。
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            print(u'+ 何も選択されていないため処理を終了します。')
            return
        sel = sel[0]
        self.saveBaseNameSave(node=sel)
        
    def exeDetachEdge(self):
        r'''
            @brief  エッジのデタッチを行います
            @return (any):
        '''
        edge = cmds.filterExpand(sm=32)
        if not edge:
            print(u'+ エッジが抽出できませんでした。')
            return
        cmds.polySplitEdge(edge)
        
        cmds.select(edge[0].split('.')[0],r=True)
        self.saveDetachNode(node=cmds.ls(sl=True)[0])
    
    def exeDetachNodeSave(self):
        r'''
            @brief  選択オブジェクトをデタッチオブジェクトとして保存
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            print(u'+ 何も選択されていないため処理を終了します。')
            return
        sel = sel[0]
        if not cmds.nodeType(sel) == 'transform':
            print(u'+ 選択されているノードがtransformではありません。')
            return
        self.saveDetachNode(node=sel)
            
    def exeRenameToNCloth(self):
        r'''
            @brief  エッジデタッチしたノードをnCloth用のオブジェクトに変換コピー
            @return (any):
        '''
        node = self.readDetachNode()
        if not node:
            print(u'+ デタッチノードが保存されていません。')
            return
        if not node.endswith(self.det):
            print(u'+ 末尾が[%s]ではありません。' % (self.det))
            return
        
        dstNode = node.replace(self.det,self.ncl)
        if not cmds.objExists(dstNode):
            cmds.duplicate(node, n=dstNode)
        else:
            print(u'+ [%s]が既に存在します。' % (dstNode))
        cmds.setAttr('%s.v' % (node), 0)
        
    def exeApplyNCloth(self):
        r'''
            @brief  デタッチノードをnCloth化する
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            print(u'+ 何も選択されていません。')
            return
            
        sel = sel[0]
        if not sel.endswith(self.ncl):
            print(
                u'+ node[%s]末尾が[%s]のノードではありません。' % (
                    sel, self.ncl
                )
            )
            return
        r = re.search('\d+$', sel)
        if r:
            print(
                u'+ [%s]は末尾に数字[0-9]がついている為'
                u'処理を終了します。' % (sel)
            )
            return
        
        cmds.select(sel,r=True)
        
        cmds.undoInfo(ock=True)
        
        cmds.delete(sel,ch=True)
        cn = mel.eval('createNCloth(1);')
        cn = cn[0]
        cmds.setAttr('%sShape.intermediateObject' % (sel), 0)
        
        cmds.setAttr('nucleus1.usePlane', 1)
        cmds.setAttr('nucleus1.subSteps', 20)
        cmds.setAttr('%s.thickness' % (cn), 0.0)
        cmds.setAttr('%s.bendResistance' % (cn), 100.0)
        cmds.setAttr('%s.bendAngleScale' % (cn), 0.0)
        
        cloth = cmds.listRelatives(cn, p=True, pa=True)
        newCloth = cmds.rename(
            cloth, 'nCloth_%s' % (sel.replace('_%s' % (self.ncl),''))
        )
        mesh = cmds.listConnections('%sShape' % (newCloth), s=False)
        cmds.rename(mesh[0], sel.replace(self.ncl,self.sms))
        
        [cmds.setAttr('%s.v' % (x), 0) for x in [sel, newCloth, 'nucleus1']]
        
        cmds.undoInfo(cck=True)
        
    def exeNClothNodeCopy(self):
        r'''
            @brief  nclothで平らになったノードをコピーする関数
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            print(u'+ 何も選択されていないため処理を終了します。')
            return
        sel = sel[0]
        if not sel.endswith(self.sms):
            print(u'+ 末尾が[%s]でないため処理を終了します。' % (self.sms))
            return
        
        cmds.undoInfo(ock=True)
        
        cmds.duplicate(sel, n=sel.replace(self.sms,self.edt))
        cmds.setAttr('%s.v' % (sel), 0)
        
        cmds.undoInfo(cck=True)
        
        start = cmds.playbackOptions(min=True)
        cmds.currentTime(start)
        
    def exeMapping(self):
        r'''
            @brief  平べったくなったノードオブジェクトをY軸でマッピング
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            print(u'+ 何も選択されていないため処理を終了します。')
            return
        sel = sel[0]
        
        # _editメッシュのみでマッピングできるように対応する
        
        cmds.select(sel,r=True)
        mel.eval('PolySelectConvert(1);')
        face = cmds.filterExpand(sm=34,ex=False)
        cmds.polyProjection(face,ch=1,type='Planar',ibd=False,kir=True,md='y')
        
    def exeTransferAttribute(self):
        r'''
            @brief  transferAttributeの設定
            @return (any):
        '''
        setting = self.sender()
        
        # default setting
        src  = None
        dst  = None
        tfp  = None
        tfn  = None
        tfuv = None
        tfc  = None
        ss   = None
        suvs = None
        tuvs = None
        sm   = None
        fuv  = None
        cb   = None
        
        # before processing
        # 平べったいnClothメッシュからデタッチメッシュへ
        if setting.order == 1:
            base = self.readBaseNameSave()
            if not base:
                print(u'+ baseノードが設定されていません。')
                return
            edit    = '%s_%s'%(base,self.edt)
            detach = '%s_%s'%(base,self.det)
            for n in [edit,detach]:
                if not cmds.objExists(n):
                    print(u'+ editノード[%s]がありません。'%(n))
                    return
            src  = edit
            dst  = detach
            tfp  = 0
            tfn  = 0
            tfuv = 2
            tfc  = 2
            ss   = 4
            suvs = 'map1'
            tuvs = 'map1'
            sm   = 3
            fuv  = 0
            cb   = 1
        # editdupメッシュからflatPlaneメッシュへ
        elif setting.order == 2:
            base = self.readBaseNameSave()
            if not base:
                print(u'+ baseノードが設定されていません。')
                return
            src = '%s_%s' % (base, self.flp)
            dst = '%s_%s' % (base, self.edd)
            tfp  = 1
            tfn  = 0
            tfuv = 2
            tfc  = 2
            ss   = 3
            suvs = 'map1'
            tuvs = 'map1'
            sm   = 0
            fuv  = 0
            cb   = 0
        # finishメッシュからdetachメッシュへ形状を合わせる
        elif setting.order == 3:
            base = self.readBaseNameSave()
            if not base:
                print(u'+ baseノードが設定されていません。')
                return
            detach = self.readDetachNode()
            if not detach:
                detach = '%s_%s'%(base,self.det)
                if not cmds.objExists(detach):
                    print(u'+ detachNode[%s]がありません。'%(detach))
                    return
            src = detach
            dst = '%s_%s'%(base,self.fnp)
            tfp  = 1
            tfn  = 0
            tfuv = 2
            tfc  = 2
            ss   = 3
            suvs = 'map1'
            tuvs = 'map1'
            sm   = 0
            fuv  = 0
            cb   = 0
        
        # transfer processing
        cmds.select(src,dst,r=True)
        cmds.transferAttributes(
            transferPositions = tfp,
            transferNormals   = tfn,
            transferUVs       = tfuv,
            transferColors    = tfc,
            sampleSpace       = ss,
            sourceUvSpace     = suvs,
            targetUvSpace     = tuvs,
            searchMethod      = sm,
            flipUVs           = fuv,
            colorBorders      = cb,
        )
        
        # after processing
        if setting.order == 1:
            cmds.delete(src, dst, ch=True)
            print(u'+ Transfer UV [%s] -> [%s]'%(src,dst))
        elif setting.order == 3:
            d = cmds.duplicate(dst)
            cmds.rename(d,'%s_%s'%(base,'end'))
        
    def exeOpenUVTextureEditor(self):
        r'''
            @brief  uv texture editorを起動
            @return (any):
        '''
        mel.eval('tearOffPanel("UV Texture Editor","polyTexturePlacementPanel",true);')
        
    def exeEditMeshDuplicate(self):
        r'''
            @brief  平べったくなったeditMeshを複製します。
            @return (any):
        '''
        baseNode = self.readBaseNameSave()
        if not baseNode:
            print(u'+ baseノードが設定されていません。')
            return
        
        edit = '%s_%s' % (baseNode, self.edt)
        if not cmds.objExists(edit):
            print(u'+ [editNode="%s"]が存在しません。' % (edit))
            return
        
        cmds.undoInfo(ock=True)
        
        editdup = cmds.duplicate(edit, n='%s_%s' % (baseNode, self.edd))
        cmds.setAttr('%s.v' % edit, 0)
        
        cmds.undoInfo(cck=True)
        
    def exeCreatePlane(self):
        r'''
            @brief  プレーンの作成
            @return (any):
        '''
        baseNode = self.readBaseNameSave()
        if not baseNode:
            print(u'+ baseノードがsaveされていないため処理を終了します。')
            return 
        
        p = cmds.polyPlane(
            n='%s_%s' % (baseNode, self.flp),
            w=1,h=1,sx=1,sy=1,ax=[0,1,0],cuv=2,ch=1
        )
        cmds.rename(p[1],'%s_%s'%(baseNode,p[1]))
        
    def exeEdgeToCurve(self):
        r'''
            @brief  選択エッジからカーブを生成
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            print(u'+ 何も選択されていないため処理を終了します。')
            return
        
        baseName = self.readBaseNameSave()
        if not baseName:
            print(u'+ baseノードがsaveされていないため処理を終了します。')
            return 
        
        cmds.undoInfo(ock=True)
        try:
            cc = cmds.polyToCurve(form=2,degree=3)
            cmds.rename(cc[0],'%s_%s#' % (baseName,self.ccv))
        except:
            print(
                u'+ エッジを抽出できませんでした。\n'
                u'+ エッジの他に何か選択されている可能性があります。'
            )
        finally:
            cmds.undoInfo(cck=True)
        
    def exeFlatPlaneSplit(self):
        r'''
            @brief  flatPlaneの分割数を変更します。
            @return (any):
        '''
        baseNode = self.readBaseNameSave()
        if not baseNode:
            print(u'+ baseノードが設定されていません。')
            return
            
        flatPlane = '%s_%s' % (baseNode,self.flp)
        if not cmds.objExists(flatPlane):
            print(u'+ [%s]が存在しないため処理を終了します。' % (flatPlane))
            return
            
        fpShape = cmds.listRelatives(flatPlane,c=True,s=True,pa=True)[0]
        b_pp = cmds.listConnections('%s.inMesh'%(fpShape))[0]
        
        num = self.modelingSpinBox.value()
        cmds.undoInfo(ock=True)
        cmds.setAttr('%s.subdivisionsWidth' %(b_pp), num)
        cmds.setAttr('%s.subdivisionsHeight'%(b_pp), num)
        cmds.undoInfo(cck=True)

    def exeCreateProjectCurve(self):
        r'''
            @brief  projectcurveを作成します。
            @return (any):
        '''
        baseNode = self.readBaseNameSave()
        if not baseNode:
            print(u'+ baseノードが設定されていません。')
            return
        flatPlane = '%s_%s' % (baseNode,self.flp)
        if not cmds.objExists(flatPlane):
            print(u'+ [%s]が存在しないため処理を終了します。' % (flatPlane))
            return
        curveName = '%s_%s*'%(baseNode,self.ccv)
        curveList = cmds.ls(curveName,type='transform')
        if not curveList:
            print(u'+ [%s]系のカーブがないため処理を終了します。' % (curveName))
            return

        cmds.undoInfo(ock=True)
        for c in curveList:
            r = cmds.polyProjectCurve(
                c,flatPlane,
                ch=True,pointsOnEdges=0,curveSamples=50,automatic=1
            )
            rn = cmds.rename(r[0],c.replace(self.ccv,self.ppc))
            print(u'+ Create project curve [%s] -> [%s]'%(c,rn))
        cmds.undoInfo(cck=True)

    def exeConvertProjectionCurve(self):
        r'''
            @brief  作成したprojectioncurveをプレーン投影します。
            @return (any):
        '''
        baseNode = self.readBaseNameSave()
        if not baseNode:
            print(u'+ baseノードが設定されていません。')
            return
        flatPlane = '%s_%s' % (baseNode,self.flp)
        if not cmds.objExists(flatPlane):
            print(u'+ [%s]が存在しないため処理を終了します。' % (flatPlane))
            return
        curveName = '%s_%s*'%(baseNode,self.ppc)
        curveList = cmds.ls(curveName,type='transform')
        if not curveList:
            print(u'+ [%s]系のカーブがないため処理を終了します。' % (curveName))
            return
        
        cmds.select(flatPlane,curveList,r=True)
        
        cmds.undoInfo(ock=True)
        
        mel.eval('performSplitMeshWithProjectedCurve(0);')
        
        newFlatPlane = '%s1'%(flatPlane)
        if cmds.objExists(newFlatPlane):
            r = cmds.rename(newFlatPlane,'%s_%s'%(baseNode,self.fnp))
            cmds.select(r,r=True)
            
        cmds.undoInfo(cck=True)
        
class ModelingPaperPatternUI(sg.EventBaseWidget):
    r'''
        @brief    ModelingPaperPatternUIクラス
        @inherit  sg.EventBaseWidget
        @date     2018/02/27 15:33[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  ガワ設定
            @param  parent(any) : enter description
            @return (any):
        '''
        super(ModelingPaperPatternUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.0c'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/02/27'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(500,280)
        
        main = ModelingPaperPatternMainUI()
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)

# -----------------------------------------------------------------------------

class colorButtonWidget(QtWidgets.QPushButton):
    r'''
        @brief    カラーダイアログの入り口ボタンクラス
        @inherit  QtWidgets.QPushButton
        @function dialog      : カラーダイアログ関数
        @function update      : カラーのアップデート
        @function color       : カラーのリターン
        @function rgba        : RGBAのリターン
        @function hsv         : HSVのリターン
        @function hexadecimal : 16進数でリターン
        @function setColor    : カラーのセット
        @function setRgba     : RGBのセット
        @function setHsv      : HSVのセット
        @date     2018/07/10 14:55[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    colorChanged = QtCore.Signal(QtGui.QColor)
    
    def __init__(self, parent=None):
        r'''
            @brief  enter description
            @param  parent(any) : enter description
            @return (any):
        '''
        super(colorButtonWidget, self).__init__(parent)
        
        self.dc = (255,255,255)
        
        self.setFlat(False)
        self.clicked.connect(self.dialog)
        self.setStyleSheet(
            'QPushButton{background-color:rgb(%s,%s,%s);}'%(
                self.dc[0],self.dc[1],self.dc[2],
            )
        )
        
        self.__color = QtGui.QColor(self.dc[0],self.dc[1],self.dc[2])
    
    def dialog(self):
        r'''
            @brief  カラーダイアログ関数
            @return (any):
        '''
        color = QtWidgets.QColorDialog.getColor(self.__color)
        if not color.isValid():
            return
            
        self.__color = color
        self.update()
        self.colorChanged.emit(self.__color)
    
    def update(self):
        r'''
            @brief  カラーのアップデート
            @return (any):
        '''
        rgb = self.rgba()
        self.setStyleSheet(
            'QPushButton{background-color:rgb(%s,%s,%s);}'%(
                rgb[0],rgb[1],rgb[2],
            )
        )
    
    def color(self):
        r'''
            @brief  カラーのリターン
            @return (any):
        '''
        return self.__color
    
    def rgba(self):
        r'''
            @brief  RGBAのリターン
            @return (any):
        '''
        return self.__color.getRgb()
        
    def hsv(self):
        r'''
            @brief  HSVのリターン
            @return (any):
        '''
        return self.__color.getHsv()
    
    def hexadecimal(self):
        r'''
            @brief  16進数でリターン
            @return (any):
        '''
        return self.__color.name()
    
    def setColor(self,color):
        r'''
            @brief  カラーのセット
            @param  color(any) : enter description
            @return (any):
        '''
        self.__color = color
        self.update()
        self.colorChanged.emit(self.__color)
    
    def setRgba(self,r,g,b,a=255):
        r'''
            @brief  RGBのセット
            @param  r(any) : enter description
            @param  g(any) : enter description
            @param  b(any) : enter description
            @param  a(any) : enter description
            @return (any):
        '''
        self.__color.setRgb(r,g,b,a)
        self.update()
        self.colorChanged.emit(self.__color)
    
    def setHsv(self,h,s,v,a=255):
        r'''
            @brief  HSVのセット
            @param  h(any) : enter description
            @param  s(any) : enter description
            @param  v(any) : enter description
            @param  a(any) : enter description
            @return (any):
        '''
        self.__color.setHsv(h,s,v,a)
        self.update()
        self.colorChanged.emit(self.__color)

class MaterialColorAssignmentMainUI(sg.ScrolledWidget):
    r'''
        @brief    MaterialColorAssignmentMainUIレイアウト部分
        @inherit  sg.ScrolledWidget
        @function buildUI          : メイン部分
        @function execute          : ボタン実行の処理
        @function materialOrganize : マテリアルの整理
        @function colLabelChanged  : テキストラベルのRGBを更新する
        @date     2018/07/10 13:56[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    rgb_LISL = ('R','G','B')
    hsv_LIST = ('H','S','V')
    material_LIST = ('lambert','blinn','phong','phongE','surfaceShader')
    
    mtr_BASENAME = 'msSim_mca_%sMT'
    
    def buildUI(self, parent=None):
        r'''
            @brief  メイン部分
            @param  parent(any) : enter description
            @return (any):
        '''
        
        # -------------------------------------------------
        # setting layout
        
        settingTopVLayout = QtWidgets.QVBoxLayout()
        settingTopHLayout = QtWidgets.QHBoxLayout()
        
        materialGroup  = QtWidgets.QGroupBox('MaterialType')
        materialGroup.setStyleSheet('QGroupBox{%s}'%(ss.GROUPFONT))
        materialLayout = QtWidgets.QVBoxLayout()
        self.materialRadioTop = QtWidgets.QButtonGroup(self)
        self.mlrbList = []
        for i,ml in enumerate(self.material_LIST):
            buf = QtWidgets.QRadioButton(ml)
            if i == 0:
                buf.setChecked(True)
            materialLayout.addWidget(buf)
            self.materialRadioTop.addButton(buf, i)
            self.mlrbList.append(buf)
        
        colorGroup = QtWidgets.QGroupBox('ColorPalette')
        colorGroup.setStyleSheet('QGroupBox{%s}'%(ss.GROUPFONT))
        colorLayout = QtWidgets.QVBoxLayout()
        self.colorButton = colorButtonWidget(self)
        self.colorButton.colorChanged[QtGui.QColor].connect(self.colLabelChanged)
        # self.colorButton.colorChanged.connect(self.colLabelChanged)
        # self.colorButton.clicked.connect(self.colLabelChanged)
        rgbLayout = QtWidgets.QHBoxLayout() 
        rgbLayout.addStretch()
        self.rgbLabelList = []
        cv = self.colorButton.rgba()
        for i,rgb in enumerate(self.rgb_LISL):
            lbuf = QtWidgets.QLabel('%s :'%(rgb))
            ebuf = QtWidgets.QLabel(str(cv[i]))
            self.rgbLabelList.append(ebuf)
            rgbLayout.addWidget(lbuf)
            rgbLayout.addWidget(ebuf)
        hsvLayout = QtWidgets.QHBoxLayout()
        hsvLayout.addStretch()
        self.hsvLabelList = []
        cv = self.colorButton.hsv()
        for i,hsv in enumerate(self.hsv_LIST):
            lbuf = QtWidgets.QLabel('%s :'%(hsv))
            ebuf = QtWidgets.QLabel(str(cv[i]))
            self.hsvLabelList.append(ebuf)
            hsvLayout.addWidget(lbuf)
            hsvLayout.addWidget(ebuf)
        hexadecimalLayout = QtWidgets.QHBoxLayout()
        hexadecimalLLabel = QtWidgets.QLabel('Hexadecimal :')
        self.hexadecimalELabel = QtWidgets.QLabel(self.colorButton.hexadecimal())
        hexadecimalLayout.addStretch()
        hexadecimalLayout.addWidget(hexadecimalLLabel)
        hexadecimalLayout.addWidget(self.hexadecimalELabel)
        
        colorLayout.addWidget(self.colorButton)
        colorLayout.addLayout(rgbLayout)
        colorLayout.addLayout(hsvLayout)
        colorLayout.addLayout(hexadecimalLayout)
        colorLayout.addStretch()
        
        materialGroup.setLayout(materialLayout)
        colorGroup.setLayout(colorLayout)
        
        settingTopHLayout.addWidget(materialGroup)
        settingTopHLayout.addWidget(colorGroup)
        settingTopVLayout.addLayout(settingTopHLayout)
        
        # -------------------------------------------------
        # execute layout
        
        executeLayout = QtWidgets.QHBoxLayout()
        executeButton = QtWidgets.QPushButton('Material assign execute')
        executeButton.clicked.connect(self.execute)
        executeLayout.addStretch(1)
        executeLayout.addWidget(executeButton, 2)
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addLayout(settingTopVLayout)
        layout.addLayout(executeLayout)
        layout.addStretch()
    
    def execute(self):
        r'''
            @brief  ボタン実行の処理
            @return (any):
        '''
        def _colorCalculation(val,defval=255.0,digit=6):
            r'''
                @brief  256数値のカラーを0.0-1.0に変換する
                @param  val(any)    : 変換する関数
                @param  defval(any) : 256のMAX数値
                @param  digit(any)  : 切り捨てる桁数の値
                @return (any):
            '''
            return round((val//defval),digit)
        
        # radiobutton
        mat_name = None
        for i,r in enumerate(self.mlrbList):
            check = r.isChecked()
            if not check:
                continue
            mat_name = self.material_LIST[i]
        if not mat_name:
            mat_name = self.material_LIST[0]
        
        # color
        col = self.colorButton.rgba()
        r = _colorCalculation(col[0])
        g = _colorCalculation(col[1])
        b = _colorCalculation(col[2])
        
        node = []
        if not node:
            node = cmds.ls(sl=True)
        if not node:
            print(u'+ 何も選択されていないため処理を終了します。')
            return
        
        cmds.undoInfo(ock=True)
        
        mtr = self.mtr_BASENAME%(mat_name)
        sg  ='%sSG'%(mtr)
        
        mayaFunc.assignMaterialColor(
            nodeList = node,
            mtr      = mtr,
            sg       = sg,
            mtrType  = mat_name,
            col      = [r,g,b]
        )
    
        cmds.undoInfo(cck=True)
        
        # self.materialOrganize()
    
    def materialOrganize(self):
        r'''
            @brief  マテリアルの整理
            @return (any):
        '''
        cmds.undoInfo(ock=True)
        mtrHit = '%s%s'%(self.mtr_BASENAME%('*'),'*')
        for ml in self.material_LIST:
            for m in cmds.ls(mtrHit, type=ml):
                list = cmds.listConnections(m,p=False)
                for node in list:
                    if not cmds.objExists(node):
                        continue
                    if not cmds.objectType(node,i='shadingEngine'):
                        continue
                    sg   = node
                    mt   = m
                    flag = False
                    for sn in cmds.listConnections(sg,p=True):
                        split = sn.split('.')[-1]
                        if split == 'instObjGroups':
                            flag = True
                    if not flag:
                        if cmds.objExists(sg):
                            cmds.delete(sg)
                            print(u'Delete sg node. [%s]'%(sg))
                        if cmds.objExists(mt):
                            cmds.delete(mt)
                            print(u'Delete mt node. [%s]'%(mt))
        cmds.undoInfo(cck=True)
        
    def colLabelChanged(self, value):
        r'''
            @brief  テキストラベルのRGBを更新する
            @param  value(any) : enter description
            @return (any):
        '''       
        rgbList = self.colorButton.rgba()
        for i,rgb in enumerate(self.rgb_LISL):
            self.rgbLabelList[i].setText(str(rgbList[i]))
        
        hsvList = self.colorButton.hsv()
        for i,hsv in enumerate(self.hsv_LIST):
            self.hsvLabelList[i].setText(str(hsvList[i]))
        
        hexadecimal = self.colorButton.hexadecimal()
        self.hexadecimalELabel.setText(hexadecimal)
        
class MaterialColorAssignmentUI(sg.EventBaseWidget):
    r'''
        @brief    設定したカラーのマテリアルをオブジェクトにアサインするUI
        @inherit  sg.EventBaseWidget
        @function exeDelUnusedMtr      : 未使用ノードの削除
        @function exeDelMsMtr          : ms_mtr系の削除
        @function exeDefaultToMaterial : デフォルトのマテリアル化
        @date     2018/07/10 13:50[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  UIおおもと部分
            @param  parent(any) : enter description
            @return (any):
        '''
        super(MaterialColorAssignmentUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.0a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/07/10'
        self.update  = '2019/04/12'
        
        self.setWindowTitle(self.claName)
        self.resize(340,260)
        
        menu = QtWidgets.QMenuBar()
        menu_com = menu.addMenu('Command')
        menu_com_defaultMtr  = menu_com.addAction('Default to material')
        menu_com_defaultMtr.triggered.connect(self.exeDefaultToMaterial)
        menu_com_unusemtrdel = menu_com.addAction('DeleteUnusedMaterial')
        menu_com_unusemtrdel.triggered.connect(self.exeDelUnusedMtr)
        menu_com_msMtrDel    = menu_com.addAction('Delete <MS_mtr> Material')
        menu_com_msMtrDel.triggered.connect(self.exeDelMsMtr)
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        self.main = MaterialColorAssignmentMainUI()
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(menu)
        layout.addWidget(self.main)
    
    # func ====================================================================
    
    def exeDelUnusedMtr(self):
        r'''
            @brief  未使用ノードの削除
            @return (any):
        '''
        mel.eval('MLdeleteUnused();')
    
    def exeDelMsMtr(self):
        r'''
            @brief  ms_mtr系の削除
            @return (any):
        '''
        self.main.materialOrganize()
    
    def exeDefaultToMaterial(self):
        r'''
            @brief  デフォルトのマテリアル化
            @return (any):
        '''
        cmds.sets(e=True,fe='initialShadingGroup')

# -----------------------------------------------------------------------------
# - riggng
# -----------------------------------------------------------------------------

class PoseResetterMainUI(sg.ScrolledWidget):
    r'''
        @brief    内部レイアウト設定
        @inherit  sg.ScrolledWidget
        @function buildUI             : パーツ設定
        @function setAnimSet          : animSetの設定
        @function getAnimSet          : animSetのリターン
        @function setNameSpace        : nameSpaceの設定
        @function getNameSpace        : nameSpaceのリターン
        @function getSelectedListNode : 選択されているリストノードのリターン
        @function setOdileData        : odileデータの情報登録
        @function getOdileData        : odileデータのリターン
        @function clearListView       : enter description
        @function startup             : ui起動時の初期設定
        @function refresh             : リストのリフレッシュ
        @function exePoseReset        : ポーズ初期化実行コマンド
        @function setDebugFlag        : デバックフラグのスイッチ
        @date     2019/02/22 16:11[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  ベースレイアウト
            @param  parent(any) : enter description
            @return (any):
        '''
        super(PoseResetterMainUI, self).__init__(parent)
        self.debugFlag     = None
        self.odileDataList = []
        
    def buildUI(self, parent):
        r'''
            @brief  パーツ設定
            @param  parent(any) : enter description
            @return (any):
        '''

        topHLayout = QtWidgets.QHBoxLayout()
        
        # left
        leftVLayout = QtWidgets.QVBoxLayout()
        self.nodeList = sg.ListView()
        refButton     = QtWidgets.QPushButton('Refresh')
        refButton.clicked.connect(self.refresh)
        leftVLayout.addWidget(self.nodeList)
        leftVLayout.addWidget(refButton)
        
        # right
        rightVLayout   = QtWidgets.QVBoxLayout()
        resetLabel     = QtWidgets.QLabel('Reset param :')
        selButton      = QtWidgets.QPushButton('Rig select')
        selButton.attr = 'select'
        selButton.clicked.connect(self.exePoseReset)
        buttonHLayout  = QtWidgets.QHBoxLayout()
        buttonHLayout.addStretch()
        for p in (['t','tr'],['r','ro'],['s','sc']):
            buf = QtWidgets.QPushButton(p[1])
            buf.attr = p[0]
            buf.clicked.connect(self.exePoseReset)
            buttonHLayout.addWidget(buf,1)
        excLabel = QtWidgets.QLabel('Commands List :')
        self.excWorld = QtWidgets.QCheckBox('Exclude WorldRig')
        self.setKey   = QtWidgets.QCheckBox('Set keyframe')
        self.setKey.setToolTip(u'odileの情報を元に開始前frameにキーを打ちます。')
        
        rightVLayout.addWidget(resetLabel)
        rightVLayout.addLayout(buttonHLayout)
        rightVLayout.addWidget(selButton,alignment=QtCore.Qt.AlignRight)
        rightVLayout.addSpacing(8)
        rightVLayout.addWidget(excLabel)
        rightVLayout.addWidget(self.excWorld,alignment=QtCore.Qt.AlignLeft)
        rightVLayout.addWidget(self.setKey,alignment=QtCore.Qt.AlignLeft)
        rightVLayout.addStretch()
        
        topHLayout.addLayout(leftVLayout ,1)
        topHLayout.addLayout(rightVLayout,1)
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addLayout(topHLayout)
    
        self.startup()
    
    # -----------------------------------------------------
    
    def setAnimSet(self,namespace):
        r'''
            @brief  animSetの設定
            @param  namespace(any) : enter description
            @return (any):
        '''
        self.animSet  = cmds.ls('{}:all_anmSet'.format(namespace))[0]
        self.worldSet = cmds.ls('{}:worldCtrl_anmSet'.format(namespace))[0]
        
    def getAnimSet(self):
        r'''
            @brief  animSetのリターン
            @return (any):
        '''
        return (self.animSet,self.worldSet)
    
    def setNameSpace(self):
        r'''
            @brief  nameSpaceの設定
            @return (any):
        '''
        self.nameSpace = [
            n.split(':')[0] for n in cmds.ls('*:all_anmSet') if n.find(':') != -1
        ]
    
    def getNameSpace(self):
        r'''
            @brief  nameSpaceのリターン
            @return (any):
        '''
        return self.nameSpace
    
    def getSelectedListNode(self,listWidget):
        r'''
            @brief  選択されているリストノードのリターン
            @param  listWidget(any) : enter description
            @return (any):
        '''
        return listWidget.selectionModel().currentIndex().data()
    
    def setOdileData(self,odileFrameList):
        r'''
            @brief  odileデータの情報登録
            @param  odileFrameList(any) : odileのフレームリスト化された辞書
            @return (any):
        '''
        self.odileDataList = odileFrameList
    
    def getOdileData(self):
        r'''
            @brief  odileデータのリターン
            @return (any):
        '''
        return self.odileDataList
    
    # -----------------------------------------------------
    
    def clearListView(self):
        r'''
            @brief  enter description
            @return (any):
        '''
        self.setNameSpace()
        self.model = self.nodeList.model()
        self.model.removeRows(0,self.model.rowCount())
        self.rootItem = self.model.invisibleRootItem()
        for node in self.getNameSpace():
            item = QtGui.QStandardItem(node)
            self.rootItem.setChild(self.rootItem.rowCount(),0,item)
            
    def startup(self):
        r'''
            @brief  ui起動時の初期設定
            @return (any):
        '''
        self.clearListView()
        
    def refresh(self):
        r'''
            @brief  リストのリフレッシュ
            @return (any):
        '''
        self.clearListView()
        print('+ Refresh')

    # -----------------------------------------------------
    
    def exePoseReset(self):
        r'''
            @brief  ポーズ初期化実行コマンド
            @return (any):
        '''
        def _setting(anim,world,option):
            r'''
                @brief  setAttr実行
                @param  anim(any)   : animSetsのセット
                @param  world(any)  : worldのセット
                @param  option(any) : translate,rotate,scaleの指定
                @return (any):
            '''
            cmds.select(anim,r=True)
            select_all = cmds.ls(sl=True)
            if self.excWorld.isChecked():
                cmds.select(world,r=True)
                for w in cmds.ls(sl=True):
                    try:
                        select_all.remove(w)
                    except:
                        pass
            setKeyFlag = False
            if self.setKey.isChecked():
                frame = self.getOdileData()
                if not frame:
                    print(u'Odileから情報が登録されていません。')
                else:
                    setKeyFlag = True
                start  = frame[0]
                sample = (start -frame[4])
                runup  = (sample-frame[3])
                drop   = (runup -frame[2])
                posing = (drop  -frame[1])
            cmds.select(select_all,r=True)
            if option == 'select':
                return
            for node in cmds.ls(sl=True):
                trs_xyz = ['{}{}'.format(t,x) for t in option for x in 'xyz']
                paramList = [('{}.{}'.format(node,p),p) for p in trs_xyz]
                for set in paramList:
                    if not cmds.objExists(set[0]):
                        continue
                    if setKeyFlag:
                        cmds.cutKey(
                            node,time=(1,(start-1)),attribute=set[1],option="keys"
                        )
                        try:
                            cmds.setKeyframe(node,attribute=set[1],t=[sample,runup,drop])
                        except:
                            pass
                    try:
                        cmds.setAttr(set[0],(0 if option in 'tr' else 1))
                        if self.debugFlag:
                            print('+ setAttr : {}'.format(set[0]))
                    except:
                        pass
                    if setKeyFlag:
                        try:
                            cmds.setKeyframe(node,attribute=set[1],t=[posing])
                        except:
                            pass
                        
        s = self.sender()
        self.setAnimSet(self.getSelectedListNode(self.nodeList))
        
        anim,world = self.getAnimSet()
        if not cmds.objExists(anim):
            return
        if not cmds.objExists(world):
            return
        cmds.undoInfo(ock=True)
        select_f = cmds.ls(sl=True)
        _setting(anim,world,s.attr)
        if s.attr != 'select':
            cmds.select(select_f,r=True)
        cmds.undoInfo(cck=True)
        
    # -----------------------------------------------------
    
    def setDebugFlag(self,value=True):
        r'''
            @brief  デバックフラグのスイッチ
            @param  value(any) : True or False
            @return (any):
        '''
        self.debugFlag = value
        
class PoseResetterUI(sg.EventBaseWidget):
    r'''
        @brief    gooneys仕様で作られたリグデータのポーズ設定UI
        @inherit  sg.EventBaseWidget
        @function setOdileData : odileデータの情報登録
        @function getOdileData : odileデータのリターン
        @date     2019/02/22 16:09[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  ベースレイアウト
            @param  parent(any) : enter description
            @return (any):
        '''
        super(PoseResetterUI, self).__init__(parent)
        
        self.debugFlag = False
        self.odileData = []
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2019/02/22'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(290,220)
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        self.main = PoseResetterMainUI()
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(self.main)
        
    # func ====================================================================

    def setOdileData(self,start,posing,drop,runup,sample):
        r'''
            @brief  odileデータの情報登録
            @param  start(any)  : スタートフレーム
            @param  posing(any) : ポージングフレーム
            @param  drop(any)   : ドロップフレーム
            @param  runup(any)  : ランナップフレーム
            @param  sample(any) : サンプルフレーム
            @return (any):
        '''
        self.odileData = (start,posing,drop,runup,sample)
        self.main.setOdileData(self.odileData)
    
    def getOdileData(self):
        r'''
            @brief  odileデータのリターン
            @return (any):
        '''
        return self.odileData
        
# -----------------------------------------------------------------------------
# - animation
# -----------------------------------------------------------------------------

class CreateGeometryCacheMainUI(sg.ScrolledWidget):
    r'''
        @brief    ジオメトリキャッシュ作成の中身部分
        @inherit  sg.ScrolledWidget
        @function buildUI             : メインUI
        @function exeFrameRefresh     : タイムスライダのリフレッシュ関数
        @function exeFileDialog       : パスをダイアログから取得する
        @function exeApplyCreateCache : 選択したノード情報をキャッシュ作成関数に送って実行する
        @date     2017/06/26 14:31[matsuzawa](matsuzawa@gooneys.co.jp)
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent):
        # type: (int) -> any
        r'''
            @brief  メインUI
            @param  parent(int) : [edit]
            @return (any):None
        '''
        nameLayout = QtWidgets.QHBoxLayout()
        nameLabel = QtWidgets.QLabel(u'ベースキャッシュネーム :')
        tbuf = (
            u'指定したネームが作成されるキャッシュの名前になります。\n'
            u'何も指定していない場合、最初に選択したノードの名前を\n'
            u'キャッシュの名前に適用します。'
        )
        nameLabel.setToolTip(tbuf)
        self.nameLineEdit = QtWidgets.QLineEdit()
        self.nameLineEdit.setToolTip(tbuf)
        addNameLabel = QtWidgets.QLabel(u'追加ネーム :')
        tbuf = (
            u'指定したネームの後ろにつく追加の名前を指定します。'
        )
        addNameLabel.setToolTip(tbuf)
        self.addNameLineEdit = QtWidgets.QLineEdit()
        self.addNameLineEdit.setToolTip(tbuf)
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameLineEdit)
        nameLayout.addWidget(addNameLabel)
        nameLayout.addWidget(self.addNameLineEdit)
        
        pathLayout = QtWidgets.QHBoxLayout()
        tbuf = (
            u'キャッシュを出力するパスを設定します。'
            u'指定したパスにキャッシュを書き出します。'
        )
        pathLabel = QtWidgets.QLabel(u'パスを設定 :')
        pathLabel.setToolTip(tbuf)
        self.pathLineEdit = QtWidgets.QLineEdit()
        self.pathLineEdit.setToolTip(tbuf)
        pathDialogButton = QtWidgets.QPushButton('Dialog')
        pathDialogButton.setToolTip(
            u'ダイアログを立ち上げます。\n'
            u'選択したパスをラインエディットに書き込みます。'
        )
        pathDialogButton.clicked.connect(self.exeFileDialog)
        pathLayout.addWidget(pathLabel)
        pathLayout.addWidget(self.pathLineEdit)
        pathLayout.addWidget(pathDialogButton)
        
        rangeRadioHLayout = QtWidgets.QHBoxLayout()
        rangeRadioLabel = QtWidgets.QLabel(u'タイムレンジ設定 :')
        rangeRadioLabel.setToolTip(
            u'タイムレンジの指定方法を決めます。'
        )
        self.rangeButtonGroup = QtWidgets.QButtonGroup(self)
        self.rangeRadioA = QtWidgets.QRadioButton(u'スタートエンド指定')
        self.rangeRadioA.setToolTip(
            u'下記のスタート/エンドの値でキャッシュを取ります。'
        )
        self.rangeRadioB = QtWidgets.QRadioButton(u'タイムスライダー')
        self.rangeRadioB.setToolTip(
            u'タイムスライダーの最初/最後でキャッシュを取ります。'
        )
        self.rangeRadioC = QtWidgets.QRadioButton(u'レンダー設定')
        self.rangeRadioC.setToolTip(
            u'レンダリングで設定されている値でキャッシュを取ります。'
        )
        self.rangeButtonGroup.addButton(self.rangeRadioA, 0)
        self.rangeButtonGroup.addButton(self.rangeRadioB, 1)
        self.rangeButtonGroup.addButton(self.rangeRadioC, 2)
        self.rangeRadioA.setChecked(True)
        rangeRadioHLayout.addWidget(rangeRadioLabel)
        rangeRadioHLayout.addWidget(self.rangeRadioA)
        rangeRadioHLayout.addWidget(self.rangeRadioB)
        rangeRadioHLayout.addWidget(self.rangeRadioC)
        rangeRadioHLayout.addStretch()
        
        radioStartEndHLayout = QtWidgets.QHBoxLayout()
        tbuf = (u'キャッシュのスタートの値です。')
        radioStartLabel = QtWidgets.QLabel('Start')
        radioStartLabel.setToolTip(tbuf)
        radioStartLabel.setAlignment(QtCore.Qt.AlignRight)
        self.radioStartSpinBox = QtWidgets.QSpinBox()
        self.radioStartSpinBox.setToolTip(tbuf)
        self.radioStartSpinBox.setRange(-999, 9999)
        self.radioStartSpinBox.setValue(int(cmds.playbackOptions(q=True, min=True)))
        self.rangeRadioA.toggled.connect(self.radioStartSpinBox.setEnabled)
        tbuf = (u'キャッシュのエンドの値です。')
        radioEndLabel = QtWidgets.QLabel('End')
        radioEndLabel.setToolTip(tbuf)
        radioEndLabel.setAlignment(QtCore.Qt.AlignRight)
        self.radioEndSpinBox = QtWidgets.QSpinBox()
        self.radioEndSpinBox.setToolTip(tbuf)
        self.radioEndSpinBox.setRange(-999, 9999)
        self.radioEndSpinBox.setValue(int(cmds.playbackOptions(q=True, max=True)))
        self.rangeRadioA.toggled.connect(self.radioEndSpinBox.setEnabled)
        frameRefreshButton = QtWidgets.QPushButton('refresh')
        frameRefreshButton.setToolTip(
            u'タイムスライダの値をセットします。'
        )
        frameRefreshButton.clicked.connect(self.exeFrameRefresh)
        radioStartEndHLayout.addSpacing(95)
        radioStartEndHLayout.addWidget(radioStartLabel)
        radioStartEndHLayout.addWidget(self.radioStartSpinBox)
        radioStartEndHLayout.addWidget(radioEndLabel)
        radioStartEndHLayout.addWidget(self.radioEndSpinBox)
        radioStartEndHLayout.addWidget(frameRefreshButton)
        radioStartEndHLayout.addStretch()
        
        mergeLayout = QtWidgets.QHBoxLayout()
        mergeLabel  = QtWidgets.QLabel(u'キャッシュファイルのマージ')
        mergeLabel.setToolTip(
            u'オブジェクトを複数選択した場合単一にすると複数オブジェクトを\n'
            u'一つのキャッシュファイルにまとめます。複数を選択すると選択した\n'
            u'オブジェクトそれぞれにキャッシュファイルを作成します。'
        )
        self.mergeButtonGroup = QtWidgets.QButtonGroup(self)
        self.mergeRadioA = QtWidgets.QRadioButton(u'単一')
        self.mergeRadioB = QtWidgets.QRadioButton(u'複数')
        self.mergeRadioA.setChecked(True)
        self.mergeButtonGroup.addButton(self.mergeRadioA, 1)
        self.mergeButtonGroup.addButton(self.mergeRadioB, 0)
        mergeLayout.addWidget(mergeLabel)
        mergeLayout.addWidget(self.mergeRadioA)
        mergeLayout.addWidget(self.mergeRadioB)
        mergeLayout.addStretch()
        
        fileTypeLayout = QtWidgets.QHBoxLayout()
        fileTypeLabel = QtWidgets.QLabel(u'キャッシュファイルタイプ :')
        fileTypeLabel.setToolTip(
            u'書き出すキャッシュファイルのタイプを選択します。\n'
            u'単一orフレーム毎の2種類あります。(デフォルト：OneFile<単一>)'
        )
        self.ftButtonGroup = QtWidgets.QButtonGroup(self)
        self.ftRadioA = QtWidgets.QRadioButton(u'OneFile(単一)')
        self.ftRadioA.setToolTip(
            u'書き出すキャッシュファイルを単一で出力します。'
        )
        self.ftRadioB = QtWidgets.QRadioButton(u'OneFilePerFrame(1フレーム毎)')
        self.ftRadioB.setToolTip(
            u'書き出すキャッシュファイルを複数(フレーム毎)で出力します。'
        )
        self.ftRadioA.setChecked(True)
        self.ftButtonGroup.addButton(self.ftRadioA, 0)
        self.ftButtonGroup.addButton(self.ftRadioB, 1)
        fileTypeLayout.addWidget(fileTypeLabel)
        fileTypeLayout.addWidget(self.ftRadioA)
        fileTypeLayout.addWidget(self.ftRadioB)
        fileTypeLayout.addStretch()
        
        formatLayout = QtWidgets.QHBoxLayout()
        tbuf = (
            u'書き出すキャッシュのフォーマットタイプを選択します。\n'
            u'2つの違いは書き出されるキャッシュの大きいものはmcxを選びますが\n'
            u'基本的にmccのファイル形式で大丈夫です。'
        )
        formatLabel = QtWidgets.QLabel(u'フォーマットタイプ :')
        formatLabel.setToolTip(tbuf)
        self.formatButtonGroup = QtWidgets.QButtonGroup(self)
        self.formatRadioA = QtWidgets.QRadioButton(u'mcc')
        self.formatRadioA.setToolTip(tbuf)
        self.formatRadioB = QtWidgets.QRadioButton(u'mcx')
        self.formatRadioB.setToolTip(tbuf)
        self.formatRadioA.setChecked(True)
        self.formatButtonGroup.addButton(self.formatRadioA, 0)
        self.formatButtonGroup.addButton(self.formatRadioB, 1)
        formatLayout.addWidget(formatLabel)
        formatLayout.addWidget(self.formatRadioA)
        formatLayout.addWidget(self.formatRadioB)
        formatLayout.addStretch()
        
        backupLayout = QtWidgets.QHBoxLayout()
        tbuf = (
            u'キャッシュ作成時にバックアップを行います。\n'
            u'同一階層に<_BU>フォルダを作成しその下に日付フォルダを作成し\n'
            u'その直下にファイルをバックアップします。\n'
            u'同一日にファイルを複数バックアップした場合はインクリメントされます。'
        )
        backupLabel = QtWidgets.QLabel(
            u'キャッシュ作成時にバックアップを行う'
        )
        backupLabel.setToolTip(tbuf)
        self.backupCheckBox = QtWidgets.QCheckBox()
        self.backupCheckBox.setToolTip(tbuf)
        self.backupCheckBox.setChecked(True)
        backupLayout.addWidget(backupLabel)
        backupLayout.addWidget(self.backupCheckBox)
        backupLayout.addStretch()
        
        tbuf = (
            u'ローカルでキャッシュを作成します。\n'
            u'サーバー上でキャッシュを取ると若干速度が落ちるため\n'
            u'少しでも早くキャッシュを取りたい場合はこちらのチェックを入れてください。\n'
            u'ローカルでキャッシュを取った後指定したパスにコピーします。\n'
            u'キャッシュパスも指定したパスへと自動置換されます。'
        )
        localCreateLayout = QtWidgets.QHBoxLayout()
        localCreateLabel = QtWidgets.QLabel(
            u'キャッシュをローカルで作成し指定したパスにコピーする(若干高速)'
        )
        localCreateLabel.setToolTip(tbuf)
        self.localCreateCheckBox = QtWidgets.QCheckBox()
        self.localCreateCheckBox.setToolTip(tbuf)
        self.localCreateCheckBox.setChecked(True)
        localCreateLayout.addWidget(localCreateLabel)
        localCreateLayout.addWidget(self.localCreateCheckBox)
        localCreateLayout.addStretch()
        
        apcaLayout = QtWidgets.QHBoxLayout()
        apcaApplyButton = QtWidgets.QPushButton((' '*4)+'Apply'+(' '*4))
        apcaApplyButton.setToolTip(
            u'キャッシュ作成を実行します。'
        )
        apcaApplyButton.clicked.connect(self.exeApplyCreateCache)
        apcaCloseButton = QtWidgets.QPushButton((' '*4)+'Close'+(' '*4))
        apcaCloseButton.setToolTip(
            u'ウィンドウを閉じます。'
        )
        self.closeButtonClicked = apcaCloseButton.clicked
        apcaLayout.addStretch()
        apcaLayout.addWidget(apcaApplyButton)
        apcaLayout.addWidget(apcaCloseButton)
        
        # print('>>>', self.rangeButtonGroup.checkedId())
        # print('>>>', self.rangeRadioA.text())
        
        # layout ------------------------------------------
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setSpacing(ss.SP+ss.SP)
        layout.addLayout(nameLayout)
        layout.addLayout(pathLayout)
        layout.addLayout(rangeRadioHLayout)
        layout.addLayout(radioStartEndHLayout)
        layout.addLayout(mergeLayout)
        layout.addLayout(fileTypeLayout)
        layout.addLayout(formatLayout)
        layout.addLayout(backupLayout)
        layout.addLayout(localCreateLayout)
        layout.addLayout(apcaLayout)
        layout.addStretch()
    
    def exeFrameRefresh(self):
        r'''
            @brief  タイムスライダのリフレッシュ関数
            @return (any):None
        '''
        self.radioStartSpinBox.setValue(int(cmds.playbackOptions(q=True, min=True)))
        self.radioEndSpinBox.setValue(int(cmds.playbackOptions(q=True, max=True)))
        
    def exeFileDialog(self):
        r'''
            @brief  パスをダイアログから取得する
            @return (any):None
        '''
        dialog = QtWidgets.QFileDialog.getExistingDirectory()
        if dialog:
            self.pathLineEdit.setText(dialog)
        
    def exeApplyCreateCache(self):
        r'''
            @brief  選択したノード情報をキャッシュ作成関数に送って実行する
            @return (any):None
        '''
        fn = sys._getframe().f_code.co_name
        
        node         = []
        confirmation = True
        path         = sg.toBasePath(self.pathLineEdit.text())
        backup       = self.backupCheckBox.isChecked()
        local        = self.localCreateCheckBox.isChecked()
        cacheName    = self.nameLineEdit.text()
        addCacheName = self.addNameLineEdit.text()
        merge        = True
        frame        = 0
        min          = 0
        max          = 1
        file         = ''
        type         = ''
        perf         = 'add'

        if self.rangeRadioA.isChecked():
            frame = 0
            min = self.radioStartSpinBox.value()
            max = self.radioEndSpinBox.value()
        elif self.rangeRadioB.isChecked():
            frame = 2
            min = int(cmds.playbackOptions(q=True, min=True))
            max = int(cmds.playbackOptions(q=True, max=True))
        elif self.rangeRadioC.isChecked():
            frame = 1
            min = int(cmds.getAttr('defaultRenderGlobals.startFrame'))
            max = int(cmds.getAttr('defaultRenderGlobals.endFrame'))
        
        if self.mergeRadioA.isChecked():
            merge = True
        elif self.mergeRadioB.isChecked():
            merge = False
            
        if self.ftRadioA.isChecked():
            file = 'OneFile'
        elif self.ftRadioB.isChecked():
            file = 'OneFilePerFrame'
        
        if self.formatRadioA.isChecked():
            type = 'mcc'
        elif self.formatRadioB.isChecked():
            type = 'mcx'
        
        mayaFunc.createGeometryCache(
            node         = [],
            confirmation = True,
            path         = path,
            backup       = backup,
            local        = local,
            cacheMerge   = merge,
            cacheName    = cacheName,
            addCacheName = addCacheName,
            frame        = frame,
            min          = min,
            max          = max,
            file         = file,
            type         = type,
        ) 

class CreateGeometryCacheUI(sg.EventBaseWidget):
    r'''
        @brief    ジオメトリキャッシュ作成のメインUI
        @inherit  sg.EventBaseWidget
        @function dropEvent : ドロップのイベント
        @date     2017/06/26 14:50[matsuzawa](matsuzawa@gooneys.co.jp)
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  メインUI
            @param  parent(any) : [edit]
            @return (any):None
        '''
        super(CreateGeometryCacheUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2017/06/26'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(480,300)
        self.setAcceptDrops(True)
        
        self.main = CreateGeometryCacheMainUI()
        self.main.closeButtonClicked.connect(self.close)
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}'%(uiName, ss.MAINUIBGC))
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(self.main)
    
    # Event ===================================================================
    
    def dropEvent(self, event):
        r'''
            @brief  ドロップのイベント
            @param  event(any) : イベントアクション
            @return (any):
        '''
        mime = event.mimeData()
        path = mime.urls()
        for p in path:
            fp = p.toLocalFile()
            # パスラインにドロップしたパスを設定
            orgPath = os.path.dirname(fp) if os.path.isfile(fp) else fp
            self.main.pathLineEdit.setText(orgPath)

# -----------------------------------------------------------------------------

class AlembicOptionToolsExportAttrUI(sg.ScrolledWidget):
    r'''
        @brief    Exportアトリビュート領域のウィジェット
        @inherit  sg.ScrolledWidget
        @function buildUI  : 承した関数内にUIを作成する
        @function getParam : チェックボックスの状態を返す
        @date     2018/05/17 15:15[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    AL = [
        ['-verbose','-v',False,(
            u'スクリプトエディタ(Script Editor)または\n'
            u'出力ウィンドウにフレーム番号情報を出力します。'
        )],
        ['-noNormals','-nn',False,(
            u'Alembicキャッシュファイルからソースオブジェクトの\n'
            u'法線データを除外する場合にオンにします。'
        )],
        ['-renderableOnly','-ro',False,(
            u'Alembicファイルから非表示オブジェクトなどの\n'
            u'レンダリング不可のノードまたは階層を除外する場合にオンにします。'
        )],
        ['-stripNamespaces','-sn',False,(
            u'書き出したオブジェクトに関連付けられたネームスペースを\n'
            u'Alembicファイルに保存される前に除去する場合はオンにします。\n'
            u'たとえば<taco:foo:bar>というネームスペースを持つオブジェクトは\n'
            u'Alembicファイルでは<bar>として表示されます。'
        )],
        ['-uvWrite','-uv',False,(
            u'Alembicファイルにポリゴンメッシュおよび\n'
            u'サブディビジョンオブジェクトからのUVデータを\n'
            u'書き込む場合にオンにします。\n'
            u'現在のUVマップだけが含まれます。'
        )],
        ['-writeColorSets','-wcs',False,(
            u'ソースポリゴンメッシュからAlembicファイルに頂点単位の\n'
            u'カラーデータを書き込むことができます。\n'
            u'レンダー時にモーションブラー効果のメッシュから\n'
            u'モーションベクトルデータを書き出すのに\n'
            u'このデータを使用することができます。'
        )],
        ['-writeFaceSets','-wfs',False,(
            u'Alembicキャッシュにフェースごとのシェーディンググループの\n'
            u'割り当てを保存する場合にオンにします。\n'
            u'Mayaはファイルにはシェーディンググループの名前のみを保存します。\n'
            u'マテリアル情報はキャッシュに書き込まれません。'
        )],
        ['-wholeFrameGeo','-wfg',False,(
            u'オンにするとフレーム全体のジオメトリデータがサンプルされて\n'
            u'ファイルに書き込まれます。オフ(既定)にするとジオメトリデータが\n'
            u'サブフレームでサンプリングされてファイルに書き込まれます。'
        )],
        ['-worldSpace','-ws',True,(
            u'ノード階層のトップノードをワールド空間として\n'
            u'保存する場合にオンにします。既定ではこれらのノードは\n'
            u'ローカル空間として格納されます。'
        )],
        ['-writeVisibility','-wv',False,(
            u'Alembicファイル内のオブジェクトの可視性の状態を\n'
            u'保存する場合にオンにします。これがオンでない場合は\n'
            u'すべてのオブジェクトが可視とみなされます。'
        )],
        ['-eulerFilter','-ef',False,(
            u'オイラーフィルタでX、Y、Z 回転データを\n'
            u'フィルタする場合にオンにします。オイラーフィルタは\n'
            u'特に X、Y、Z の回転が360度を超える場合に\n'
            u'回転の不規則性を解決するときに役立ちます。'
        )],
        ['-writeCreases','-wc',False,(
            u'ジオメトリのエッジや頂点の折り目の情報を\n'
            u'Alembicファイルに書き出しする場合にオンにします。'
        )],
    ]
    
    def buildUI(self, parent=None):
        r'''
            @brief  承した関数内にUIを作成する
            @param  parent(any) : enter description
            @return (any):
        '''
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setSpacing(2)
        
        self.cbList = []
        for i,al in enumerate(self.AL):
            buf = QtWidgets.QCheckBox(al[0])
            buf.setToolTip('%s\n\n%s'%(al[0],al[3]))
            buf.setChecked(al[2])
            layout.addWidget(buf)
            self.cbList.append(buf)
    
    def getParam(self):
        r'''
            @brief  チェックボックスの状態を返す
            @return (any):
        '''
        return {x[0]:y.isChecked() for x,y in zip(self.AL,self.cbList)}
        
class AlembicOptionToolsExportUI(sg.ScrolledWidget):
    r'''
        @brief    Exportメイン関数
        @inherit  sg.ScrolledWidget
        @function buildUI        : 継承した関数内にUIを作成する
        @function dragEnterEvent : ドラッグのイベント
        @function dropEvent      : ドロップのイベント
        @function rangeSetting   : タイムレンジの設定
        @function exeDialog      : ダイアログからパス情報を設定する
        @function exeRefresh     : 入力数値のリフレッシュ
        @function flagReturn     : フラグ状態のリターン
        @function execute        : ボタン実行コマンド
        @date     2018/05/17 14:28[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent=None):
        r'''
            @brief  継承した関数内にUIを作成する
            @param  parent(any) : enter description
            @return (any):
        ''' 
        self.setAcceptDrops(True)
        
        # -------------------------------------------------
        # パスライン設定
        
        pathLayout    = QtWidgets.QHBoxLayout()
        pathLabel     = QtWidgets.QLabel('Export path :')
        self.pathLine = QtWidgets.QLineEdit()
        pathButton    = QtWidgets.QPushButton('Dialog')
        pathButton.clicked.connect(self.exeDialog)
        pathLayout.addWidget(pathLabel)
        pathLayout.addWidget(self.pathLine)
        pathLayout.addWidget(pathButton)
        
        # --------------------------------------------------
        # 名前の追加
        
        addNameLayout      = QtWidgets.QHBoxLayout()
        tbuf = (u'Base名の前につく名前を設定します。')
        addNameLabel       = QtWidgets.QLabel('Name :')
        addNameBeforeL     = QtWidgets.QLabel('Before')
        addNameBeforeL.setToolTip(tbuf)
        self.addNameBefore = QtWidgets.QLineEdit('')
        addNameBeforeL.setToolTip(tbuf)
        tbuf = (u'Baseが空白の場合、選択しているオブジェクトの名前を使用します。')
        addNameBaseL       = QtWidgets.QLabel('Base')
        addNameBaseL.setToolTip(tbuf)
        self.addNameBase   = QtWidgets.QLineEdit('')
        self.addNameBase.setToolTip(tbuf)
        tbuf = (u'Base名の後につく名前を設定します。')
        addNameRearL       = QtWidgets.QLabel('Rear')
        addNameRearL.setToolTip(tbuf)
        self.addNameRear   = QtWidgets.QLineEdit('')
        self.addNameRear.setToolTip(tbuf)
        addNameLayout.addWidget(addNameLabel)
        addNameLayout.addWidget(addNameBeforeL)
        addNameLayout.addWidget(self.addNameBefore)
        addNameLayout.addWidget(addNameBaseL)
        addNameLayout.addWidget(self.addNameBase)
        addNameLayout.addWidget(addNameRearL)
        addNameLayout.addWidget(self.addNameRear)
        
        # --------------------------------------------------
        # タイムレンジ設定
        
        timeLayout    = QtWidgets.QHBoxLayout()
        timeLabel     = QtWidgets.QLabel(u'Time range setting :')
        self.rbGroup  = QtWidgets.QButtonGroup(self)
        self.rbRadioA = QtWidgets.QRadioButton('TimeSlider')
        self.rbRadioB = QtWidgets.QRadioButton('StartEnd')
        self.rbRadioC = QtWidgets.QRadioButton('RenderSetting')
        self.rbRadioA.setChecked(True)
        self.rbGroup.addButton(self.rbRadioA, 0)
        self.rbGroup.addButton(self.rbRadioB, 1)
        self.rbGroup.addButton(self.rbRadioC, 2)
        timeLayout.addWidget(timeLabel)
        timeLayout.addWidget(self.rbRadioA)
        timeLayout.addWidget(self.rbRadioB)
        timeLayout.addWidget(self.rbRadioC)
        timeLayout.addStretch()
        
        timeValueLayoutA     = QtWidgets.QHBoxLayout()
        seLabel              = QtWidgets.QLabel('StartEnd |')
        seStartLabel         = QtWidgets.QLabel('Start :')
        self.seStartSpinBox  = QtWidgets.QSpinBox()
        self.seStartSpinBox.setEnabled(False)
        self.seStartSpinBox.setRange(-9999,9999)
        seEndLabel           = QtWidgets.QLabel('End :')
        self.seEndSpinBox    = QtWidgets.QSpinBox()
        self.seEndSpinBox.setEnabled(False)
        self.seEndSpinBox.setRange(-9999,9999)
        seRefreshButton      = QtWidgets.QPushButton('Refresh') 
        seRefreshButton.type = 'se'
        seRefreshButton.setEnabled(False)
        seRefreshButton.clicked.connect(self.exeRefresh)
        self.rbRadioB.toggled.connect(self.seStartSpinBox.setEnabled)
        self.rbRadioB.toggled.connect(self.seEndSpinBox.setEnabled)
        self.rbRadioB.toggled.connect(seRefreshButton.setEnabled)
        timeValueLayoutA.addStretch()
        timeValueLayoutA.addWidget(seLabel)
        timeValueLayoutA.addWidget(seStartLabel)
        timeValueLayoutA.addWidget(self.seStartSpinBox)
        timeValueLayoutA.addWidget(seEndLabel)
        timeValueLayoutA.addWidget(self.seEndSpinBox)
        timeValueLayoutA.addWidget(seRefreshButton)
        
        timeValueLayoutB         = QtWidgets.QHBoxLayout()
        renderLabel              = QtWidgets.QLabel('RenderSetting |')
        renderStartLabel         = QtWidgets.QLabel('Start :')
        self.renderStartSpinBox  = QtWidgets.QSpinBox()
        self.renderStartSpinBox.setEnabled(False)
        self.renderStartSpinBox.setRange(-9999,9999)
        renderEndLabel           = QtWidgets.QLabel('End :')
        self.renderEndSpinBox    = QtWidgets.QSpinBox()
        self.renderEndSpinBox.setEnabled(False)
        self.renderEndSpinBox.setRange(-9999,9999)
        renderRefreshButton      = QtWidgets.QPushButton('Refresh') 
        renderRefreshButton.type = 'render'
        renderRefreshButton.setEnabled(False)
        renderRefreshButton.clicked.connect(self.exeRefresh)
        self.rbRadioC.toggled.connect(self.renderStartSpinBox.setEnabled)
        self.rbRadioC.toggled.connect(self.renderEndSpinBox.setEnabled)
        self.rbRadioC.toggled.connect(renderRefreshButton.setEnabled)
        timeValueLayoutB.addStretch()
        timeValueLayoutB.addWidget(renderLabel)
        timeValueLayoutB.addWidget(renderStartLabel)
        timeValueLayoutB.addWidget(self.renderStartSpinBox)
        timeValueLayoutB.addWidget(renderEndLabel)
        timeValueLayoutB.addWidget(self.renderEndSpinBox)
        timeValueLayoutB.addWidget(renderRefreshButton)
        
        # -------------------------------------------------
        # アトリビュート
        
        self.abcCb = AlembicOptionToolsExportAttrUI()
        
        # -------------------------------------------------
        # 実行ボタン
        
        buttonLayout = QtWidgets.QHBoxLayout()
        exeButton = QtWidgets.QPushButton('Execute')
        exeButton.clicked.connect(self.execute)
        buttonLayout.addWidget(exeButton)
        
        # -------------------------------------------------
        # レイアウト総合
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addLayout(pathLayout)
        layout.addLayout(addNameLayout)
        layout.addLayout(timeLayout)
        layout.addLayout(timeValueLayoutA)
        layout.addLayout(timeValueLayoutB)
        layout.addWidget(self.abcCb)
        layout.addLayout(buttonLayout)
        layout.addStretch()
        
        # -------------------------------------------------
        # 設定など
        
        self.rangeSetting()
    
    # Event ===================================================================
    
    def dragEnterEvent(self, event):
        r'''
            @brief  ドラッグのイベント
            @param  event(any) : イベントアクション
            @return (any):
        '''
        mime = event.mimeData()
        if mime.hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        r'''
            @brief  ドロップのイベント
            @param  event(any) : イベントアクション
            @return (any):
        '''
        mime = event.mimeData()
        path = mime.urls()
        for p in path:
            fp = p.toLocalFile()
            # パスラインにドロップしたパスを設定
            orgPath = os.path.dirname(fp) if os.path.isfile(fp) else fp
            self.pathLine.setText(orgPath)
    
    # Func ====================================================================
    
    def rangeSetting(self,type='all'):
        r'''
            @brief  タイムレンジの設定
            @param  type(any) : enter description
            @return (any):
        '''
        if type == 'all' or type == 'se':
            val = mayaFunc.getTimeSlider()
            self.seStartSpinBox.setValue(val[0])
            self.seEndSpinBox.setValue(val[1])
        if type == 'all' or type == 'render':
            val = mayaFunc.getRanderGlobalFrameRange()
            self.renderStartSpinBox.setValue(val[0])
            self.renderEndSpinBox.setValue(val[1])

    def exeDialog(self):
        r'''
            @brief  ダイアログからパス情報を設定する
            @return (any):
        '''
        dialog = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.pathLine.setText(dialog)
    
    def exeRefresh(self):
        r'''
            @brief  入力数値のリフレッシュ
            @return (any):
        '''
        self.rangeSetting(type=self.sender().type)
    
    def flagReturn(self):
        r'''
            @brief  フラグ状態のリターン
            @return (any):
        '''
        returnList = []
        flagA = ''
        flagB = []
        for x,y in self.abcCb.getParam().items():
            if y and x.endswith('verbose'):
                flagA = x
            elif y:
                flagB.append(x)
        
        '''
        returnList.append(
            ' '.join([x for x,y in self.abcCb.getParam().items() if y])
        )
        '''
        returnList.append(flagA)
        returnList.append(' '.join(flagB))
        return returnList
    
    def execute(self):
        r'''
            @brief  ボタン実行コマンド
            @return (any):
        '''
        path  = self.pathLine.text()
        flag  = self.flagReturn()
        node  = self.addNameBase.text()
        nameP = self.addNameBefore.text()
        nameS = self.addNameRear.text()
        min   = 0
        max   = 1
        
        if self.rbRadioA.isChecked():
            min = cmds.playbackOptions(q=True,min=True)
            max = cmds.playbackOptions(q=True,max=True)
        elif self.rbRadioB.isChecked():
            min = self.seStartSpinBox.value()
            max = self.seEndSpinBox.value()
        elif self.rbRadioC.isChecked():
            min = self.renderStartSpinBox.value()
            max = self.renderEndSpinBox.value()
        
        q = QtWidgets.QMessageBox.question(
            None, (u'書き出し確認'), (
                u'以下の設定で書き出します。よろしいでしょうか？\n'
                u'Path : %s\nNode : %s\nOption : %s' % (
                    path, cmds.ls(sl=True), flag
                )
            ),
            QtWidgets.QMessageBox.StandardButton.Yes,
            QtWidgets.QMessageBox.StandardButton.No
        )
        if q == QtWidgets.QMessageBox.StandardButton.No:
            print(u'+ Export cancel.')
            return
    
        mayaFunc.alembicExporter(
            exportPath = path,
            option     = [flag[0],flag[1]],
            node       = node,
            namePrifix = nameP,
            nameSuffix = nameS,
            start      = min,
            end        = max,
        )
        
class AlembicOptionToolsImportUI(sg.ScrolledWidget):
    r'''
        @brief    Importメイン関数
        @inherit  sg.ScrolledWidget
        @function buildUI        : 継承した関数内にUIを作成する
        @function dragEnterEvent : ドラッグのイベント
        @function dropEvent      : ドロップのイベント
        @function exeDialog      : ダイアログからパス情報を設定する
        @function execute        : ボタン実行コマンド
        @date     2018/05/17 14:28[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent=None):
        r'''
            @brief  継承した関数内にUIを作成する
            @param  parent(any) : enter description
            @return (any):
        ''' 
        self.setAcceptDrops(True)
        
        # -------------------------------------------------
        # パスライン設定
        
        pathLayout    = QtWidgets.QHBoxLayout()
        pathLabel     = QtWidgets.QLabel('Import path :')
        self.pathLine = QtWidgets.QLineEdit()
        pathButton    = QtWidgets.QPushButton('Dialog')
        pathButton.clicked.connect(self.exeDialog)
        pathLayout.addWidget(pathLabel)
        pathLayout.addWidget(self.pathLine)
        pathLayout.addWidget(pathButton)
        
        # -------------------------------------------------
        # 実行ボタン
        
        buttonLayout = QtWidgets.QHBoxLayout()
        exeButton = QtWidgets.QPushButton('Execute')
        exeButton.clicked.connect(self.execute)
        buttonLayout.addWidget(exeButton)
        
        # -------------------------------------------------
        # レイアウト総合
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addLayout(pathLayout)
        layout.addLayout(buttonLayout)
        layout.addStretch()
    
    # Event ===================================================================
    
    def dragEnterEvent(self, event):
        r'''
            @brief  ドラッグのイベント
            @param  event(any) : イベントアクション
            @return (any):
        '''
        mime = event.mimeData()
        if mime.hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        r'''
            @brief  ドロップのイベント
            @param  event(any) : イベントアクション
            @return (any):
        '''
        mime = event.mimeData()
        path = mime.urls()
        for p in path:
            fp = p.toLocalFile()
            # パスラインにドロップしたパスを設定
            orgPath = os.path.dirname(fp) if os.path.isfile(fp) else fp
            self.pathLine.setText(orgPath)
    
    # Func ====================================================================
    
    def exeDialog(self):
        r'''
            @brief  ダイアログからパス情報を設定する
            @return (any):
        '''
        dialog = QtWidgets.QFileDialog.getOpenFileName(self,filter='*.abc')[0]
        self.pathLine.setText(dialog)
    
    def execute(self):
        r'''
            @brief  ボタン実行コマンド
            @return (any):
        '''
        mayaFunc.alembicImporter(self.pathLine.text())
        
class AlembicOptionToolsUI(sg.EventBaseWidget):
    r'''
        @brief    アレンビック関係のコマンドをまとめたツールUI
        @inherit  sg.EventBaseWidget
        @date     2018/05/17 14:23[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  ガワ設定
            @param  parent(any) : enter description
            @return (any):
        '''
        super(AlembicOptionToolsUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/05/17'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(420,360)
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        exportUI = AlembicOptionToolsExportUI()
        importUI = AlembicOptionToolsImportUI()
        
        tab = QtWidgets.QTabWidget()
        tab.setStyleSheet('QTabWidget{%s}'%(ss.TABBGC))
        tab.addTab(exportUI, 'Export')
        tab.addTab(importUI, 'Import')
            
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
    
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(tab)

# -----------------------------------------------------------------------------

class CacheSettingMainUI(sg.ScrolledWidget):
    r'''
        @brief    CacheSettingMainUIのメインコード
        @inherit  sg.ScrolledWidget
        @function buildUI                     : メインUI
        @function attributeList               : sceneから持ってきたアトリビュート情報をselfに入れて
        @function refreshListView             : ListViewのリフレッシュ
        @function exeOpenDialog               : キャッシュパスのダイアログを参照してLineEditにセットし
        @function exeListBranch               : list関数へ渡すための分岐関数
        @function exeListRefresh              : refreshListViewを実行するためのクッション関数
        @function exeSceneCacheRefresh        : リストしたキャッシュをListViewにセットする
        @function exeSelectCacheOpenAttribute : シーンキャッシュをダブルクリックしたときに
        @function exeAttributeListBranch      : アトリビュート関数への分岐関数
        @function exeAttibuteList_reset       : アトリビュートアイテムのリセット
        @function exeAttributeList_read       : タイムスライダー（要変更）の最小・最大値の値をリストアイテムにセットする
        @function exeAttributeList_set        : 設定したアイテムの値を選択しているシーンのキャッシュにセットする
        @date     2017/08/03 11:09[matsuzawa](matsuzawa@gooneys.co.jp)
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent):
        r'''
            @brief  メインUI
            @param  parent(any) : [edit]
            @return (any):None
        '''
        
        # ---------------------------------------------------------------------
        
        headerLayout = QtWidgets.QVBoxLayout()
        tbuf = (u'キャッシュパスを入力してください。')
        headerLayout_2 = QtWidgets.QHBoxLayout()
        cachePathLabel = QtWidgets.QLabel('Cache path :')
        cachePathLabel.setToolTip(tbuf)
        self.cachePathLine = QtWidgets.QLineEdit()
        self.cachePathLine.setToolTip(tbuf)
        self.cachePathLine.returnPressed.connect(self.exeListRefresh)
        dialogButton = QtWidgets.QPushButton('Dialog')
        dialogButton.setToolTip(u'ダイアログを開いてパスを設定します。')
        dialogButton.clicked.connect(self.exeOpenDialog)
        headerLayout_2.addWidget(cachePathLabel)
        headerLayout_2.addWidget(self.cachePathLine)
        headerLayout_2.addWidget(dialogButton)
        
        headerLayout.addLayout(headerLayout_2)
        
        # ---------------------------------------------------------------------
        
        self.vbLayoutList = []
        self.listViewList = []
        self.cacheEnable  = ''
        self.spinBoxList  = []
        
        __LIST_SCHEMALIST = (
            [
                ['listView',['','dir',
                    u'キャッシュパスで指定されたフォルダにあるキャッシュの一覧リスト。\n'
                    u'※リストされるキャッシュの条件は.xmlファイルがあるかで判別します。'
                ]],
                ['button',['Dir cache refresh','dir',
                    u'キャッシュリストをリフレッシュします。'
                ]],
            ],
            [
                ['listView',['','scene',
                    u'シーン内にあるキャッシュの一覧リスト。\n'
                    u'リストアイテムをダブルクリックすると'
                    u'対象のアトリビュートエディタを開きます。'
                ]],
                ['button',['Scene cache refresh','scene',
                    u'キャッシュリストをリフレッシュします。'
                ]],
            ],
        )
        __ATTR_SCHEMALIST = (
            ['Enable',True,
                u'キャッシュを有効/無効にするかどうかの設定。'
            ],
            ['Start frame',(-9999,9999),1,
                u'simのスタートフレームの設定。'
            ],
            ['Source start',(-9999,9999),1,
                u'simのソーススタートフレームの設定。'
            ],
            ['Source end',(-9999,9999),1,
                u'simのソースエンドフレームの設定。'
            ],
            ['Original start',(-9999,9999),1,
                u'simのオリジナルスタートフレームの設定。'
            ],
            ['Original end',(-9999,9999),1,
                u'simのオリジナルエンドフレームの設定。'
            ],
            [
                ['Reset','#A44',
                    u'アトリビュートをリセットします。\n'
                    u'Enable=True\n'
                    u'Source start=1, Source end=1\n'
                    u'Original start=1, Original end=1'
                ],
                ['Read','#4A4',
                    u'simのスタート、エンドフレームを設定します。\n'
                    u'proj,episode,shotを設定しsceneInfoから'
                    u'フレーム数を取得出来る場合はそちらを優先して設定し\n'
                    u'取得できなければ現在設定されている'
                    u'タイムスライダの開始/終了の値を設定します。'
                ],
                ['Set','#44A',
                    u'設定したアトリビュートと指定したdirCacheパスのデータを\n'
                    u'選択したsceneCacheに適用します。'
                ],
            ]
        )
        
        footerLayout = QtWidgets.QVBoxLayout()
        footerLayout.setSpacing(ss.SP)
        footerHLayout = QtWidgets.QHBoxLayout()
        
        for i,u in enumerate(__LIST_SCHEMALIST):
            vl = QtWidgets.QVBoxLayout() 
            for i2,u2 in enumerate(u):
                if u2[0] == 'listView':
                    list = sg.ListView()
                    list.setToolTip(u2[1][-1])
                    if u2[1][1] == 'scene':
                        list.doubleClicked.connect(
                            self.exeSelectCacheOpenAttribute
                        )
                    vl.addWidget(list)
                    self.listViewList.append(list)
                elif u2[0] == 'button':
                    hl = QtWidgets.QHBoxLayout()
                    b  = QtWidgets.QPushButton(u2[1][0])
                    b.attr = u2[1][1]
                    b.clicked.connect(self.exeListBranch)
                    b.setToolTip(u2[1][-1])
                    hl.addStretch(1)
                    hl.addWidget(b,2)
                    vl.addLayout(hl)
            self.vbLayoutList.append(vl)
        
        
        gl = QtWidgets.QGroupBox('Attribute list')
        gl.setToolTip(u'アトリビュートの設定を行う簡易メニュー。')
        fvLayoutR = QtWidgets.QVBoxLayout(gl)
        fvLayoutR.setContentsMargins(ss.LM[0], 0, 0, 0)
        fvLayoutR.setSpacing(ss.SP)
        for i,u in enumerate(__ATTR_SCHEMALIST):
            # 一番最初(Enableボタン)
            if i == 0:
                hl = QtWidgets.QHBoxLayout()
                e = QtWidgets.QCheckBox(u[0])
                e.setToolTip(u[-1])
                e.setChecked(u[1])
                self.cacheEnable = e
                fvLayoutR.addWidget(e)
            # 一番最後(ボタンリスト)
            elif i == (len(__ATTR_SCHEMALIST)-1):
                fvLayoutR.addStretch()
                hl = QtWidgets.QHBoxLayout()
                for i2,u2 in enumerate(u):
                    b = QtWidgets.QPushButton(u2[0])
                    b.setToolTip(u2[-1])
                    b.attr = u2[0]
                    b.clicked.connect(self.exeAttributeListBranch)
                    b.setStyleSheet('QPushButton{background-color:%s;}'%(u2[1]))
                    hl.addWidget(b)
                fvLayoutR.addLayout(hl)
            # それ以外(スピンボックス)
            else:
                hl = QtWidgets.QHBoxLayout()
                l  = QtWidgets.QLabel(u[0])
                l.setToolTip(u[-1])
                sp = QtWidgets.QSpinBox()
                sp.setRange(u[1][0],u[1][1])
                sp.setValue(u[2])
                sp.setToolTip(u[-1])
                self.spinBoxList.append(sp)
                hl.addWidget(l,4)
                hl.addWidget(sp,1)
                fvLayoutR.addLayout(hl)

        for vb in self.vbLayoutList:
            footerHLayout.addLayout(vb)
        footerHLayout.addWidget(gl)
        
        footerLayout.addLayout(footerHLayout)
        
        # layout --------------------------------------------------------------
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setSpacing(ss.SP)
        layout.addLayout(headerLayout)
        layout.addLayout(footerLayout)
    
    def attributeList(self, keywords):
        r'''
            @brief  sceneから持ってきたアトリビュート情報をselfに入れて
                    共有化する関数
            @param  keywords(any) : [dict]sceneから持ってきた辞書情報データ
            @return (any):None
        '''
        self.keywordsList = keywords
    
    def refreshListView(self):
        r'''
            @brief  ListViewのリフレッシュ
            @return (any):None
        '''
        fn = sys._getframe().f_code.co_name
        
        path = self.cachePathLine.text()
        
        if not path:
            print(
                u'+ [Func:%s] [path]が空のため処理を終了します。' % (fn)
            )
            return
        if not os.path.isdir(path):
            print(
                u'+ [Func:%s] [path:%s]のフォルダが存在しないため'
                u'処理を終了します。' % (
                    fn, path
                )
            )
            return
        
        model = self.listViewList[0].model()
        model.removeRows(0, model.rowCount())
        rootItem = model.invisibleRootItem()
        
        # cacheのデータはxmlを参照してリストする
        cacheList = []
        for cache in os.listdir(path):
            xml = re.search('^.*[.]xml$', cache)
            if xml:
                cacheList.append(os.path.splitext(xml.group())[0])
        
        for i in cacheList:
            item = QtGui.QStandardItem(i)
            rootItem.setChild(rootItem.rowCount(), 0, item)
            
        print(u'+ [Func:%s] Refresh dir cache list [path:%s]' % (fn, path))
        
    def exeOpenDialog(self):
        r'''
            @brief  キャッシュパスのダイアログを参照してLineEditにセットし
                    リストのリフレッシュを行う
            @return (any):None
        '''
        fn = sys._getframe().f_code.co_name
        
        path = os.path.join(
            os.environ["USERPROFILE"],'Documents/maya/projects/default/data'
        ).replace('\\','/')
        dialog = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select folder', path
        )
        if not dialog:
            print(
                u'+ [Func:%s] ダイアログからパスを選択しなかったため'
                u'処理を終了します。' % (fn)
            )
            return
        self.cachePathLine.setText(dialog)
        self.refreshListView()
    
    def exeListBranch(self):
        r'''
            @brief  list関数へ渡すための分岐関数
            @return (any):
        '''
        s = self.sender()

        if s.attr == 'dir':
            self.refreshListView()
        elif s.attr == 'scene':
            self.exeSceneCacheRefresh()
        print(s.attr)
    
    def exeListRefresh(self):
        r'''
            @brief  refreshListViewを実行するためのクッション関数
            @return (any):None
        '''
        self.refreshListView()
    
    def exeSceneCacheRefresh(self):
        r'''
            @brief  リストしたキャッシュをListViewにセットする
            @return (any):None
        '''
        fn = sys._getframe().f_code.co_name
        
        model = self.listViewList[1].model()
        model.removeRows(0, model.rowCount())
        rootItem = model.invisibleRootItem()
        
        cacheList = cmds.ls(type='cacheFile')
        if not cacheList:
            print(
                u'+ [Func:%s] シーン内にキャッシュがないため'
                u'処理を終了します。' % (fn)
            )
            return
        for i in cacheList:
            item = QtGui.QStandardItem(i)
            rootItem.setChild(rootItem.rowCount(), 0, item)
            
        print(u'+ [Func:%s] Refresh scene cache list.' % (fn))
    
    def exeSelectCacheOpenAttribute(self):
        r'''
            @brief  シーンキャッシュをダブルクリックしたときに
                    選択したキャッシュのアトリビュートエディタを開く関数
            @return (any):None
        '''
        node = self.listViewList[1].selectionModel().currentIndex().data()
        if not cmds.objExists(node):
            print(
                u'+ [Func:%s] [node:%s]が見つかりません。' % (fn, node)
            )
            return
        mel.eval('showEditor "%s";' % (node))
    
    def exeAttributeListBranch(self):
        r'''
            @brief  アトリビュート関数への分岐関数
            @return (any):
        '''
        s = self.sender()

        if s.attr == 'Reset':
            self.exeAttibuteList_reset()
        elif s.attr == 'Read':
            self.exeAttributeList_read()
        elif s.attr == 'Set':
            self.exeAttributeList_set()
    
    def exeAttibuteList_reset(self):
        r'''
            @brief  アトリビュートアイテムのリセット
            @return (any):None
        '''
        self.cacheEnable.setChecked(True)
        [box.setValue(1.0) for box in self.spinBoxList]
    
    def exeAttributeList_read(self):
        r'''
            @brief  タイムスライダー（要変更）の最小・最大値の値をリストアイテムにセットする
            @return (any):None
        '''
        fn = sys._getframe().f_code.co_name
        
        def _simStartFrame(startFrame=0, posingFrame=0, dropFrame=0, runupFrame=0):
            r'''
                @brief  simのスタートフレームを計算して返す関数
                @param  startFrame(any)  : ベースのスタートフレーム
                @param  posingFrame(any) : posingFrame数
                @param  dropFrame(any)   : dropFrame数
                @param  runupFrame(any)  : runupFrame数
                @return (any):計算されたスタートフレーム
            '''
            return (startFrame - posingFrame - dropFrame - runupFrame)

        def _simEndFrame(endFrame=0):
            r'''
                @brief  simのエンドフレームを計算して返す関数
                @param  endFrame(any) : ベースのエンドフレーム
                @return (any):計算されたエンドフレーム
            '''
            return (endFrame + 1)
        
        startFrame,endFrame,posingFrame  = '','',''
        dropFrame,runupFrame,sampleFrame = '','',''
        try:
            startFrame  = self.keywordsList['startFrame']
            endFrame    = self.keywordsList['endFrame']
            posingFrame = self.keywordsList['posingFrame']
            dropFrame   = self.keywordsList['dropFrame']
            runupFrame  = self.keywordsList['runupFrame']
            sampleFrame = self.keywordsList['sampleFrame']
        except:
            print(u'keywordsListから値を習得できませんでした。')
            
        if not startFrame:
            print(u'+ [Func:%s] [startFrame]がありません。' % (fn))
            startFrame  = 0
        if not endFrame:
            print(u'+ [Func:%s] [endFrame]がありません。'   % (fn))
            endFrame    = 0
        if not posingFrame:
            print(u'+ [Func:%s] [posingFrame]がありません。'% (fn))
            posingFrame = 0
        if not dropFrame:
            print(u'+ [Func:%s] [dropFrame]がありません。'  % (fn))
            dropFrame   = 0
        if not runupFrame:
            print(u'+ [Func:%s] [runupFrame]がありません。' % (fn))
            runupFrame  = 0
        if not sampleFrame:
            print(u'+ [Func:%s] [sampleFrame]がありません。'% (fn))
            sampleFrame = 0
        simStFrame=(
            _simStartFrame(
                startFrame  = startFrame,
                posingFrame = posingFrame,
                dropFrame   = dropFrame,
                runupFrame  = runupFrame,
            )
        )
        simEdFrame=(
            _simEndFrame(endFrame=endFrame)
        )
        
        min = 0
        max = 1
        
        if simStFrame and simEdFrame:
            min = simStFrame
            max = simEdFrame
            print(
                u'+ [Func:%s] SSGに入力されている情報から取得しました。' % (fn)
            )
        else:
            min = int(cmds.playbackOptions(q=True, min=True))
            max = int(cmds.playbackOptions(q=True, max=True))
            print(
                u'+ [Func:%s] [sceneInfo]から情報を取得できなかったため'
                u'現在設定されているタイムスライダの値を取得しました。' % (fn)
            )
        
        [i[1].setValue(i[0]) for i in zip((min,min,max,min,max),self.spinBoxList)]
        
    def exeAttributeList_set(self):
        r'''
            @brief  設定したアイテムの値を選択しているシーンのキャッシュにセットする
            @return (any):None
        '''
        fn = sys._getframe().f_code.co_name
        
        dirCache   = self.listViewList[0].selectionModel().currentIndex().data()
        sceneCache = self.listViewList[1].selectionModel().currentIndex().data()
        path       = self.cachePathLine.text()
        enable     = self.cacheEnable.isChecked()
        sf         = self.spinBoxList[0].value()
        ss         = self.spinBoxList[1].value()
        se         = self.spinBoxList[2].value()
        os         = self.spinBoxList[3].value()
        oe         = self.spinBoxList[4].value()
        
        if not cmds.objExists(sceneCache):
            print(
                u'+ [Func:%s] [Cache:%s]が存在しないため処理を終了します。' % (
                    fn, sceneCache
                )
            )
            return
        
        if path:
            cmds.setAttr('%s.cachePath' % (sceneCache), path, type='string')
        if dirCache:
            cmds.setAttr('%s.cacheName' % (sceneCache), dirCache, type='string')
        
        mayaFunc.setUndoInfo(True)
        cmds.setAttr('%s.enable'        % (sceneCache), enable)
        cmds.setAttr('%s.startFrame'    % (sceneCache), sf)
        cmds.setAttr('%s.sourceStart'   % (sceneCache), ss)
        cmds.setAttr('%s.sourceEnd'     % (sceneCache), se)
        cmds.setAttr('%s.originalStart' % (sceneCache), os)
        cmds.setAttr('%s.originalEnd'   % (sceneCache), oe)
        mayaFunc.setUndoInfo(False)

        print(u'+ [Func:%s] SetAttr cache attribute.'%(fn))
        print(u'\tcachePath     : %s'%(path))
        print(u'\tcacheName     : %s'%(dirCache))
        print(u'\tenable        : %s'%(enable))
        print(u'\tstartFrame    : %s'%(sf))
        print(u'\tsourceStart   : %s'%(ss))
        print(u'\tsourceEnd     : %s'%(se))
        print(u'\toriginalStart : %s'%(os))
        print(u'\toriginalEnd   : %s'%(oe))
        
class CacheSettingUI(sg.EventBaseWidget):
    r'''
        @brief    CacheSettingUIのメインコード
        @inherit  sg.EventBaseWidget
        @function dropEvent     : ドロップのイベント
        @function attributeList : CacheSettingMainUIへsceneのアトリビュート情報を持っていくためのクッション関数
        @date     2017/08/03 11:09[matsuzawa](matsuzawa@gooneys.co.jp)
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  メインコード
            @param  parent(any) : [edit]
            @return (any):None
        '''
        super(CacheSettingUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2017/08/03'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(500,270)
        self.setAcceptDrops(True)
        
        self.main = CacheSettingMainUI()
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}'%(uiName,ss.MAINUIBGC))
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(self.main)
    
    # Event ===================================================================
    
    def dropEvent(self, event):
        r'''
            @brief  ドロップのイベント
            @param  event(any) : イベントアクション
            @return (any):
        '''
        mime = event.mimeData()
        path = mime.urls()
        for p in path:
            fp = p.toLocalFile()
            # パスラインにドロップしたパスを設定
            orgPath = os.path.dirname(fp) if os.path.isfile(fp) else fp
            self.main.cachePathLine.setText(orgPath)
        
    # func ====================================================================
    
    def attributeList(self, **keywords):
        r'''
            @brief  CacheSettingMainUIへsceneのアトリビュート情報を持っていくためのクッション関数
            @param  keywords(any) : enter description
            @return (any):None
        '''
        self.main.attributeList(keywords)
        
# -----------------------------------------------------------------------------

class SimPlayblastMainUI(sg.ScrolledWidget):
    r'''
        @brief    SimPlayblastUIレイアウト部分
        @inherit  sg.ScrolledWidget
        @function buildUI                   : enter description
        @function setOptionVar              : オプションバーのセット
        @function readOptionVar             : オプションネームの読み込みと返し
        @function exeMenu                   : パスラインのメニューアップ
        @function exeFrameSetMenu           : フレームセットのメニューアップ
        @function exeDialog                 : ダイアログからパスをセットする
        @function exeOpenFolder             : 入力されているパスをエクスプローラーで開く
        @function exeExistence              : 入力パスの確認存在しなければ赤色
        @function exeSetPathName            : pathラインの記憶
        @function exeSetFileName            : filenameの記憶
        @function exeFrameSet               : フレームを右クリックでセット
        @function exeSetMayaScene           : シーンネームを取得してセット
        @function exePlayblastFormatSet     : プレイブラストのフォーマットの設定
        @function exePlayblastEncodingSet   : プレイブラストのエンコーディング設定
        @function exePlayblastEncodingClear : プレイブラストのエンコーディング初期化
        @function exeChangeEncoding         : フォーマットを参照してエンコーディングを設定
        @function exeChangeResolution       : レゾリューションのリストの解像度を設定する
        @function exeNowResoSet             : 設定されているシーンの解像度をセット
        @function exePlayblast              : プレイブラストの実行
        @function exePlayback               : パス+ファイル名のデータを実行する
        @function setLogPath                : ログパスを設定
        @function getLogPath                : ログパスを取得
        @function exeOpenLogPath            : ログパスのフォルダを開く
        @function playblastTimeRecord       : プレイブラストの記録ログの作成
        @date     2018/08/13 07:35[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    
    playList = mayaFunc.playblastFormatEncodingList()
    resoList = mayaFunc.resolutionList()
    
    def buildUI(self, parent):
        r'''
            @brief  enter description
            @param  parent(any) : enter description
            @return (any):
        '''
        
        # ---------------------------------------------------------------------
        # path line
        
        T_BUF = (
            u'エクスポート先のパスを指定します。\n'
            u'ファイルフォルダをドロップするとそのパスを設定します。'
        )
        pathLayoutA   = QtWidgets.QHBoxLayout()
        pathLabel     = QtWidgets.QLabel('Export path :')
        pathLabel.setToolTip(T_BUF)
        self.pathLine = QtWidgets.QLineEdit('')
        self.pathLine.setToolTip(T_BUF)
        self.pathLine.address = 'path'
        self.pathLine.textChanged.connect(self.exeExistence)
        self.pathLine.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pathLine.customContextMenuRequested.connect(self.exeMenu)
        pathLayoutA.addWidget(pathLabel)
        pathLayoutA.addWidget(self.pathLine)
        pathLayoutB    = QtWidgets.QHBoxLayout()
        self.pathCheck = QtWidgets.QCheckBox('Create Dir Flag')
        self.pathCheck.setToolTip(
            u'チェックが入っていると指定先のパスがない場合フォルダを作成します。'
        )
        pathButton    = QtWidgets.QPushButton('Path Dialog')
        pathButton.setToolTip(u'パスをダイアログから指定してセットします。')
        pathButton.clicked.connect(self.exeDialog)
        pathLayoutB.addStretch()
        pathLayoutB.addWidget(self.pathCheck)
        pathLayoutB.addWidget(pathButton)
        
        # ---------------------------------------------------------------------
        # name line
        
        T_BUF = (u'作成されるムービーのフォルダ名を指定します。')
        nameLayout    = QtWidgets.QHBoxLayout()
        nameLabel     = QtWidgets.QLabel('File name :')
        nameLabel.setToolTip(T_BUF)
        self.nameLine = QtWidgets.QLineEdit('playblast')
        self.nameLine.address = 'filename'
        self.nameLine.setToolTip(T_BUF)
        self.nameLine.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.nameLine.customContextMenuRequested.connect(self.exeMenu)
        nameButton    = QtWidgets.QPushButton('Scene name set')
        nameButton.setToolTip(
            u'シーンが開かれている場合、現在のシーン名をセットします。'
        )
        nameButton.clicked.connect(self.exeSetMayaScene)
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameLine)
        nameLayout.addWidget(nameButton)
        
        # ---------------------------------------------------------------------
        # format and encoding
        
        formatLayout       = QtWidgets.QHBoxLayout()
        T_BUF = (u'フォーマットタイプを指定します。')
        formatLabel        = QtWidgets.QLabel('Format :')
        formatLabel.setToolTip(T_BUF)
        self.formatCombo   = QtWidgets.QComboBox()
        self.formatCombo.setToolTip(T_BUF)
        self.formatCombo.currentIndexChanged.connect(self.exeChangeEncoding)
        T_BUF = (u'エンコードタイプを指定します。')
        encodingLabel      = QtWidgets.QLabel('Encoding :')
        encodingLabel.setToolTip(T_BUF)
        self.encodingCombo = QtWidgets.QComboBox()
        self.encodingCombo.setToolTip(T_BUF)
        self.exePlayblastFormatSet()
        self.exePlayblastEncodingSet()
        try:
            self.formatCombo.setCurrentText('avi')
            self.encodingCombo.setCurrentText('Lagarith')
        except:
            pass
        formatLayout.addWidget(formatLabel       ,1)
        formatLayout.addWidget(self.formatCombo  ,2)
        formatLayout.addWidget(encodingLabel     ,1)
        formatLayout.addWidget(self.encodingCombo,2)
        
        # ---------------------------------------------------------------------
        # frame
        
        frameLayout    = QtWidgets.QHBoxLayout()
        T_BUF = (u'スタートフレームを指定します。')
        startLabel     = QtWidgets.QLabel('Start frame :')
        startLabel.setToolTip(T_BUF)
        self.startLine = QtWidgets.QLineEdit(str(int(cmds.playbackOptions(q=True,min=True))))
        self.startLine.setToolTip(T_BUF)
        self.startLine.seFlag = 'start'
        self.startLine.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.startLine.customContextMenuRequested.connect(self.exeFrameSetMenu)
        T_BUF = (u'エンドフレームを指定します。')
        endLabel       = QtWidgets.QLabel('End frame :')
        endLabel.setToolTip(T_BUF)
        self.endLine   = QtWidgets.QLineEdit(str(int(cmds.playbackOptions(q=True,max=True))))
        self.endLine.setToolTip(T_BUF)
        self.endLine.seFlag = 'end'
        self.endLine.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.endLine.customContextMenuRequested.connect(self.exeFrameSetMenu)
        frameLayout.addWidget(startLabel)
        frameLayout.addWidget(self.startLine)
        frameLayout.addWidget(endLabel)
        frameLayout.addWidget(self.endLine)
        
        
        # ---------------------------------------------------------------------
        # resolution
        
        resoLayoutA    = QtWidgets.QHBoxLayout()
        resoLabel      = QtWidgets.QLabel('resolution ')
        resoLabel.setToolTip(u'解像度を指定します。')
        T_BUF = (u'横幅の解像度を指定します。')
        resoWLabel     = QtWidgets.QLabel('W :')
        resoWLabel.setToolTip(T_BUF)
        self.resoWLine = QtWidgets.QLineEdit('')
        self.resoWLine.setToolTip(T_BUF)
        T_BUF = (u'縦幅の解像度を指定します。')
        resoHLabel     = QtWidgets.QLabel('H :')
        resoHLabel.setToolTip(T_BUF)
        self.resoHLine = QtWidgets.QLineEdit('')
        self.resoHLine.setToolTip(T_BUF)
        resoLayoutA.addWidget(resoLabel,2)
        resoLayoutA.addWidget(resoWLabel)
        resoLayoutA.addWidget(self.resoWLine,4)
        resoLayoutA.addWidget(resoHLabel)
        resoLayoutA.addWidget(self.resoHLine,4)
        
        T_BUF = (u'指定したリストの解像度を設定します。')
        resoLayoutB   = QtWidgets.QHBoxLayout()
        resoListLabel = QtWidgets.QLabel('Reso list:')
        resoListLabel.setToolTip(T_BUF)
        self.resoListCombo = QtWidgets.QComboBox()
        self.resoListCombo.setToolTip(T_BUF)
        self.resoListCombo.currentIndexChanged.connect(self.exeChangeResolution)
        [self.resoListCombo.addItem(rl[0]) for rl in self.resoList]
        try:
            self.resoListCombo.setCurrentText('HD 720')
        except:
            pass
        nowResoButton = QtWidgets.QPushButton('Now rezo set')
        nowResoButton.clicked.connect(self.exeNowResoSet)
        resoLayoutB.addStretch(1)
        resoLayoutB.addWidget(resoListLabel,1)
        resoLayoutB.addWidget(self.resoListCombo,2)
        resoLayoutB.addWidget(nowResoButton,1)
        
        
        # ---------------------------------------------------------------------
        # option
        
        optionLayoutA = QtWidgets.QHBoxLayout()
        T_BUF = (
            u'解像度の大きさの割合を指定します。\n'
            u'100の場合はW,Hで指定されているそのままの大きさで\n'
            u'それ以下の場合は「解像度の大きさ×Precent」で書き出されます。'
        )
        perLabel      = QtWidgets.QLabel('Percent :')
        perLabel.setToolTip(T_BUF)
        self.perBox   = QtWidgets.QSpinBox()
        self.perBox.setToolTip(T_BUF)
        self.perBox.setRange(0,100)
        self.perBox.setSingleStep(1)
        self.perBox.setValue(100)
        T_BUF = (u'書き出されるムービーの精度を指定します。')
        qualityLabel    = QtWidgets.QLabel('Quality :')
        qualityLabel.setToolTip(T_BUF)
        self.qualityBox = QtWidgets.QSpinBox()
        self.qualityBox.setToolTip(T_BUF)
        self.qualityBox.setRange(0,100)
        self.qualityBox.setSingleStep(1)
        self.qualityBox.setValue(75)
        optionLayoutA.addStretch()
        optionLayoutA.addWidget(perLabel)
        optionLayoutA.addWidget(self.perBox)
        optionLayoutA.addWidget(qualityLabel)
        optionLayoutA.addWidget(self.qualityBox)
        
        optionLayoutB       = QtWidgets.QHBoxLayout()
        self.overwriteCheck = QtWidgets.QCheckBox('Overwrite')
        self.overwriteCheck.setToolTip(
            u'チェックが入っていると書き出される先に\n'
            u'同一のファイルが有った場合上書きをします。'
        )
        self.overwriteCheck.setChecked(True)
        self.showArnamentsCheck = QtWidgets.QCheckBox('Show ornaments')
        self.showArnamentsCheck.setToolTip(
            u'チェックが入っていると書き出されるムービーに\n'
            u'ヘッドアップディスプレイやグリッドなどの情報を非表示にしてムービーを作成します。'
        )
        self.showArnamentsCheck.setChecked(True)
        optionLayoutB.addStretch()
        optionLayoutB.addWidget(self.overwriteCheck)
        optionLayoutB.addWidget(self.showArnamentsCheck)
        
        # ---------------------------------------------------------------------
        # execute
        
        executeLayout = QtWidgets.QHBoxLayout()
        executeButton = QtWidgets.QPushButton('Playblast execute')
        executeButton.setToolTip(u'設定されている情報を元にムービーを作成します。')
        executeButton.setStyleSheet(
            'QPushButton{color:#000;background-color:#87CEEB;}'
        )
        executeButton.clicked.connect(self.exePlayblast)
        executeButton.address = 'execute'
        executeButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        executeButton.customContextMenuRequested.connect(self.exeMenu)
        playbackButton = QtWidgets.QPushButton('Playback')
        playbackButton.setToolTip(
            u'設定されているパスとファイル名のデータを再生します。'
        )
        playbackButton.setStyleSheet(
            'QPushButton{color:#000;background-color:#676793;}'
        )
        playbackButton.clicked.connect(self.exePlayback)
        executeLayout.addWidget(executeButton,3)
        executeLayout.addWidget(playbackButton,1)
        
        # ---------------------------------------------------------------------
        # layout
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addLayout(pathLayoutA)
        layout.addLayout(pathLayoutB)
        layout.addLayout(nameLayout)
        layout.addLayout(formatLayout)
        layout.addLayout(frameLayout)
        layout.addLayout(resoLayoutA)
        layout.addLayout(resoLayoutB)
        layout.addLayout(optionLayoutA)
        layout.addLayout(optionLayoutB)
        layout.addLayout(executeLayout)
        layout.addStretch()
        
        # ---------------------------------------------------------------------
        # other setting
        
        self.setLogPath()
        
    # -------------------------------------------------------------------------
    
    def setOptionVar(self,opName,stword):
        r'''
            @brief  オプションバーのセット
            @param  opName(any) : optionVarの名前
            @param  stword(any) : 記録する文字列
            @return (any):
        '''
        cmds.optionVar(sv=[opName,stword])
        print(u'OptionVar set.')
        print(u'\toptionVar name : %s'%(opName))
        print(u'\tword           : %s'%(stword))
    
    def readOptionVar(self,opName):
        r'''
            @brief  オプションネームの読み込みと返し
            @param  opName(any) : optionVarの名前
            @return (any):
        '''
        return cmds.optionVar(q=opName)
    
    # -------------------------------------------------------------------------
    
    def exeMenu(self):
        r'''
            @brief  パスラインのメニューアップ
            @return (any):
        '''
        s    = self.sender()
        menu = QtWidgets.QMenu()
        if s.address == 'path':
            menu.addAction(
                'Open folder',lambda:self.exeOpenFolder(self.pathLine.text())
            )
            m=menu.addAction('Path name set' ,self.exeSetPathName)
            m.type = 'set'
            m=menu.addAction('Path name read',self.exeSetPathName)
            m.type = 'read'
        elif s.address == 'filename':
            m=menu.addAction('Path name set' ,self.exeSetFileName)
            m.type = 'set'
            m=menu.addAction('Path name read',self.exeSetFileName)
            m.type = 'read'
        elif s.address == 'execute':
            m=menu.addAction('Open log path' ,self.exeOpenLogPath)
        menu.exec_(QtGui.QCursor.pos())
        
    def exeFrameSetMenu(self):
        r'''
            @brief  フレームセットのメニューアップ
            @return (any):
        '''
        line = self.sender()
        menu = QtWidgets.QMenu()
        frameMenu = menu.addAction('[%s] Frame set'%(line.seFlag), self.exeFrameSet)
        frameMenu.seMenuFlag = line.seFlag
        menu.exec_(QtGui.QCursor.pos())
    
    # -------------------------------------------------------------------------
    
    def exeDialog(self):
        r'''
            @brief  ダイアログからパスをセットする
            @return (any):
        '''
        dialog = QtWidgets.QFileDialog.getExistingDirectory(self)
        aft    = self.pathLine.text() if not dialog else dialog
        self.pathLine.setText(aft)

    def exeOpenFolder(self,path):
        r'''
            @brief  入力されているパスをエクスプローラーで開く
            @param  path(any) : enter description
            @return (any):
        '''
        if not os.path.exists(path):
            return
        sg.openExplorer(path)
    
    def exeExistence(self):
        r'''
            @brief  入力パスの確認存在しなければ赤色
            @return (any):
        '''
        p = self.pathLine.text()
        if os.path.exists(p) or not p:
            self.pathLine.setStyleSheet('QLineEdit{background-color:rgb(43,43,43)}')
        else:
            self.pathLine.setStyleSheet('QLineEdit{background-color:rgb(123,43,43)}')
    
    def exeSetPathName(self):
        r'''
            @brief  pathラインの記憶
            @return (any):
        '''
        s   = self.sender()
        opn = 'msappSimPlayblastPathName'
        if s.type == 'set':
            self.setOptionVar(opn,self.pathLine.text())
        elif s.type == 'read':
            op = self.readOptionVar(opn)
            self.pathLine.setText(op)
    
    def exeSetFileName(self):
        r'''
            @brief  filenameの記憶
            @return (any):
        '''
        s   = self.sender()
        opn = 'msappSimPlayblastFileName'
        if s.type == 'set':
            self.setOptionVar(opn,self.nameLine.text())
        elif s.type == 'read':
            op = self.readOptionVar(opn)
            self.nameLine.setText(op)
    
    def exeFrameSet(self):
        r'''
            @brief  フレームを右クリックでセット
            @return (any):
        '''
        line = self.sender()
        
        if line.seMenuFlag == 'start':
            self.startLine.setText(
                str(int(cmds.playbackOptions(q=True, min=True)))
            )
        elif line.seMenuFlag == 'end':
            self.endLine.setText(
                str(int(cmds.playbackOptions(q=True, max=True)))
            )
        else:
            print(
                u'+ [start or end] 以外の文字列がセットされています。 => [%s]' % (
                    line.seMenuFlag
                )
            )
    
    def exeSetMayaScene(self):
        r'''
            @brief  シーンネームを取得してセット
            @return (any):
        '''
        scene = os.path.splitext(cmds.file(q=True,shn=True,sn=True))[0]
        if scene:
            self.nameLine.setText(scene)
    
    def exePlayblastFormatSet(self):
        r'''
            @brief  プレイブラストのフォーマットの設定
            @return (any):
        '''
        [self.formatCombo.addItem(p) for p in self.playList]
        
    def exePlayblastEncodingSet(self, format=None):
        r'''
            @brief  プレイブラストのエンコーディング設定
            @param  format(any) : フォーマットのタイプ
            @return (any):
        '''
        formatText = format if format else self.formatCombo.currentText()
        self.encodingCombo.addItems(self.playList[formatText])
    
    def exePlayblastEncodingClear(self):
        r'''
            @brief  プレイブラストのエンコーディング初期化
            @return (any):
        '''
        self.encodingCombo.clear()
    
    def exeChangeEncoding(self):
        r'''
            @brief  フォーマットを参照してエンコーディングを設定
            @return (any):
        '''
        self.exePlayblastEncodingClear()
        formatText = self.formatCombo.currentText()
        self.exePlayblastEncodingSet(format=formatText)
    
    def exeChangeResolution(self):
        r'''
            @brief  レゾリューションのリストの解像度を設定する
            @return (any):
        '''
        currentText = self.resoListCombo.currentText()
        for rl in self.resoList:
            if currentText == rl[0]:
                self.resoWLine.setText(str(rl[1]))
                self.resoHLine.setText(str(rl[2]))
                break
    
    def exeNowResoSet(self):
        r'''
            @brief  設定されているシーンの解像度をセット
            @return (any):
        '''
        self.resoWLine.setText(str(cmds.getAttr('defaultResolution.w')))
        self.resoHLine.setText(str(cmds.getAttr('defaultResolution.h')))
    
    def exePlayblast(self):
        r'''
            @brief  プレイブラストの実行
            @return (any):
        '''
        q = QtWidgets.QMessageBox.question(
            None, (u'Execution confirmation'), (
                u'playblastを実行します。よろしいでしょうか？'
            ),
            QtWidgets.QMessageBox.StandardButton.Yes,
            QtWidgets.QMessageBox.StandardButton.No
        )
        if q == QtWidgets.QMessageBox.StandardButton.No:
            print(u'+ Export cancel.')
            return
        
        path = self.pathLine.text()
        if not path:
            print(u'+ Pathが何も入力されていません。')
            return
        if self.pathCheck.isChecked():
            if not os.path.exists(path):
                os.makedirs(path)
                print(u'+ Create folder : %s' % (path))
        else:
            if not os.path.exists(path):
                print(
                    u'+ 入力されているパスが存在しません。\n'
                    u'\tPath : %s' % (path)
                )
                return
        
        filePath = sg.toBasePath(
            os.path.join(path,self.nameLine.text())
        )
        
        _TE.flowProcessStartTime()
        mayaFunc.executePlayblast(
            fileName       = filePath,
            format         = self.formatCombo.currentText(),
            compression    = self.encodingCombo.currentText(),
            width          = int(self.resoWLine.text()),
            height         = int(self.resoHLine.text()),
            startTime      = int(self.startLine.text()),
            endTime        = int(self.endLine.text()),
            percent        = self.perBox.value(),
            quality        = self.qualityBox.value(),
            forceOverwrite = self.overwriteCheck.isChecked(),
            showOrnaments  = self.showArnamentsCheck.isChecked(),
        )
        end = _TE.flowProcessEndTime()
        self.playblastTimeRecord(time=end)
        print(u'+ Processing time : %s sec'%(round(end,2)))
    
    def exePlayback(self):
        r'''
            @brief  パス+ファイル名のデータを実行する
            @return (any):
        '''
        path,file = self.pathLine.text(),self.nameLine.text()
        
        if not path or os.path.isfile(path):
            print(u'+ Pathが入力されていないか対象のフォルダパスが見つかりません。')
            return
        
        ext,extFlag = '',False
        for f in os.listdir(path):
            sp1,sp2 = os.path.splitext(f)
            if sp1 == file:
                ext     = sp2
                extFlag = True
                break
        
        if not extFlag:
            print(u'+ 対象のファイル[%s]が見つかりませんでした。'%(file))
            return
            
        sg.executeFile(os.path.join(path,'%s%s'%(file,ext)))
    
    def setLogPath(self):
        r'''
            @brief  ログパスを設定
            @return (any):
        '''
        homePath = sg.getPathList(
            company='gooneys',pathType='homepath'
        )
        if not homePath:
            self.__logPath = None
            return
        
        self.__logPath = os.path.join(
            homePath,'_msapp','playblastTimeRecord'
        ).replace('\\','/')
        
    def getLogPath(self):
        r'''
            @brief  ログパスを取得
            @return (any):
        '''
        return self.__logPath

    def exeOpenLogPath(self):
        r'''
            @brief  ログパスのフォルダを開く
            @return (any):
        '''
        self.exeOpenFolder(sg.toReversePath(self.getLogPath()))
        
    def playblastTimeRecord(self,time):
        r'''
            @brief  プレイブラストの記録ログの作成
            @param  time(any) : 書き出す時間
            @return (any):
        '''
        exportPath = self.getLogPath()
        
        if exportPath is None:
            raise RuntimeError(u'+ exportPathが取得できませんでした。')
            return
        if not os.path.isdir(exportPath):
            os.makedirs(exportPath)
            print('+ Create dir.')
            print('\t{}'.format(exportPath))
        
        writePath = os.path.join(exportPath,'log.txt').replace('\\','/')
        log = ', '.join([
            str(sg.getDateTime()['ymd'][2]),
            str(sg.getDateTime()['hms'][1]),
            str(self.nameLine.text()),
            str('{}sec'.format(round(time,1))),
            str(self.pathLine.text().replace('\\','/')),
            '\n'
        ])
        f = open(writePath,'a')
        f.write(log)
        f.close()
        
        print('+ Playblast time record.')
        print('\t{}'.format(log))

class SimPlayblastUI(sg.EventBaseWidget):
    r'''
        @brief    SimPlayblastUIのメインコード
        @inherit  sg.EventBaseWidget
        @function dropEvent : ドロップのイベント
        @date     2017/08/03 11:09[matsuzawa](matsuzawa@gooneys.co.jp)
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  メインコード
            @param  parent(any) : [edit]
            @return (any):None
        '''
        super(SimPlayblastUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.2a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/08/13'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(380,360)
        self.setAcceptDrops(True)
        
        self.main = SimPlayblastMainUI()
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(self.main)
    
    # Event ===================================================================
    
    def dropEvent(self, event):
        r'''
            @brief  ドロップのイベント
            @param  event(any) : イベントアクション
            @return (any):
        '''
        mime = event.mimeData()
        path = mime.urls()
        for p in path:
            fp = p.toLocalFile()
            # パスラインにドロップしたパスを設定
            orgPath = os.path.dirname(fp) if os.path.isfile(fp) else fp
            self.main.pathLine.setText(orgPath)

    # func ====================================================================

# =============================================================================

# -----------------------------------------------------------------------------
# - deformer
# -----------------------------------------------------------------------------

class TransferBlendShapeMainUI(sg.ScrolledWidget):
    r'''
        @brief    TransferBlendShapeのMainUI部分
        @inherit  sg.ScrolledWidget
        @function buildUI    : レイアウトコマンド総合
        @function exeSet     : setボタン実行時のコマンドapply
        @function exeExecute : Execute実行時のコマンド
        @date     2018/06/04 15:50[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    
    nameList = ('Goal','Move','Wrap')
    
    def buildUI(self, parent=None):
        r'''
            @brief  レイアウトコマンド総合
            @param  parent(any) : enter description
            @return (any):
        '''
        
        layout = QtWidgets.QVBoxLayout(parent)
        
        self.inputLine = []
        for i,NL in enumerate(self.nameList):
            bufLayout = QtWidgets.QHBoxLayout()
            label  = QtWidgets.QLabel('%s geo : '%(NL))
            label.setAlignment(QtCore.Qt.AlignRight)
            line   = QtWidgets.QLineEdit('')
            line.setStyleSheet('QLineEdit{background-color:#000;}')
            line.setEnabled(True)
            self.inputLine.append(line)
            button = QtWidgets.QPushButton(' Set ')
            button.type = NL
            button.clicked.connect(self.exeSet)
            bufLayout.addWidget(label ,2)
            bufLayout.addWidget(line  ,5)
            bufLayout.addWidget(button,1)
            layout.addLayout(bufLayout)
        
        bottomLayout = QtWidgets.QHBoxLayout()
        spinLabel    = QtWidgets.QLabel('Moving distance')
        self.spinBox = QtWidgets.QDoubleSpinBox()
        self.spinBox.setRange(0.0,1.0)
        self.spinBox.setSingleStep(0.1)
        self.spinBox.setValue(0.5)
        exeButton    = QtWidgets.QPushButton('Execute')
        exeButton.clicked.connect(self.exeExecute)
        bottomLayout.addWidget(spinLabel,   1)
        bottomLayout.addWidget(self.spinBox,1)
        bottomLayout.addWidget(exeButton,   2)
        
        # -------------------------------------------------
        # layout
        layout.setSpacing(2)
        layout.addLayout(bottomLayout)
        layout.addStretch()

    def exeSet(self):
        r'''
            @brief  setボタン実行時のコマンドapply
            @return (any):
        '''
        button = self.sender()
        
        sel = cmds.ls(sl=True)
        if not sel:
            return
        
        if button.type == self.nameList[0]:
            self.inputLine[0].setText(sel[0])
        if button.type == self.nameList[1]:
            self.inputLine[1].setText(sel[0])
        if button.type == self.nameList[2]:
            self.inputLine[2].setText(','.join(sel))
    
    def exeExecute(self):
        r'''
            @brief  Execute実行時のコマンド
            @return (any):
        '''
        def _identityCheck(nodeList=[]):
            r'''
                @brief  ノード２つのバーテックス数が違ったらTrueを返す
                @param  nodeList(any) : enter description
                @return (any):
            '''
            SL   = []
            FLAG = None
            LOG  = []
            if not nodeList:
                LOG.append(u'+ No array node.')
                FLAG = True
            if not len(nodeList) == 2:
                LOG.append(u'+ Two other array nodes.')
                FLAG = True
            for node in nodeList:
                try:
                    if not cmds.objExists(node):
                        LOG.append(u'+ [Node:%s] Not found.'%(node))
                        FLAG = True
                        break
                    vx = cmds.polyListComponentConversion(node,tv=True)[0]
                    SL.append(len(cmds.ls(vx,fl=True)))
                except:
                    LOG.append(u'+ [Node:%s] Possibility of "None" in the node.'%(node))
                    FLAG = True
            if FLAG == None:
                if not SL[0] == SL[1]:
                    LOG.append(
                        u'+ Vertex is different. ["%s:%s" != "%s:%s"]' % (
                            nodeList[0],SL[0],nodeList[1],SL[1]
                        )
                    )
                    FLAG = True
                else:
                    LOG.append(u'+ No problem. Successful completion.')
                    FLAG = False            
            return (FLAG,LOG)
        
        nodeCheck = lambda node: None if node == '' else node
        goal = nodeCheck(self.inputLine[0].text())
        move = nodeCheck(self.inputLine[1].text())
        wrap = nodeCheck(self.inputLine[2].text().split(','))
        
        for wn in wrap:
            if not cmds.objExists(wn):
                print('+ Not found wrap node. [%s]'%(wn))
                return
        
        result = _identityCheck([goal,move])
        if result[0]:
            print('#'+('+-'*50))
            print(u'+ ERROR : Topology is different. ["%s" != "%s"]'%(goal,move))
            for r in result[1]:
                print(r)
            print('#'+('+-'*50))
            raise 
        
        bsn = ('transferBlendShape_%s__%s'%(goal,move))
        
        cmds.undoInfo(ock=True)
        wp = mayaFunc.wrapAssign(src=move,dst=wrap)
        bs = mayaFunc.blensShapeAssign(
            src    = move,
            dst    = goal,
            name   = bsn,
            weight = [0.0,self.spinBox.value()],       
            origin = 'world',
        )
        cmds.delete(move,ch=True)
        cmds.delete(wrap,ch=True)
        delBase = lambda node: cmds.delete(node) if cmds.objExists(node) else None
        delBase('%sBase'%(move))
        cmds.xform(move,cpc=True)
        cmds.xform(wrap,cpc=True)
        cmds.undoInfo(cck=True)
        
class TransferBlendShapeUI(sg.EventBaseWidget):
    r'''
        @brief    TransferBlendShapeのUI
        @inherit  sg.EventBaseWidget
        @date     2018/06/04 15:47[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  UIおおもと部分
            @param  parent(any) : enter description
            @return (any):
        '''
        super(TransferBlendShapeUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/06/04'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(300,170)
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        main  = TransferBlendShapeMainUI()
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)

# -----------------------------------------------------------------------------

class SearchSkinClusterMainUI(sg.ScrolledWidget):
    r'''
        @brief    SearchSkinClusterUIレイアウト部分
        @inherit  sg.ScrolledWidget
        @function buildUI    : レイアウトコマンド総合
        @function exeSet     : 選択ノードをセット
        @function exeSelect  : リストされたアイテムを選択
        @function exeExecute : スキンノードのサーチ
        @date     2018/06/07 14:33[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent=None):
        r'''
            @brief  レイアウトコマンド総合
            @param  parent(any) : enter description
            @return (any):
        '''
        descLabel = QtWidgets.QLabel(u'+ Input joint name.')
        
        lineLayout = QtWidgets.QHBoxLayout()
        self.line  = QtWidgets.QLineEdit('')
        lineButton = QtWidgets.QPushButton(' Set ')
        lineButton.clicked.connect(self.exeSet)
        exeButton  = QtWidgets.QPushButton('Execute')
        exeButton.clicked.connect(self.exeExecute)
        lineLayout.addWidget(self.line)
        lineLayout.addWidget(lineButton)
        lineLayout.addWidget(exeButton)
        
        self.list = QtWidgets.QListView()
        self.list.setMinimumSize(1,1)
        self.list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list.setAlternatingRowColors(True)
        self.list.setSelectionMode(self.list.ExtendedSelection)
        # self.list.clicked.connect(self.exeSelect)
        self.list.doubleClicked.connect(self.exeSelect)
        model = QtGui.QStandardItemModel(0,1)
        self.list.setModel(model)
        self.list.selModel = QtCore.QItemSelectionModel(model)
        self.list.setSelectionModel(self.list.selModel)
        # self.list.selModel.currentChanged.connect(self.exeSelect) # 小森さんに聞く部分
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addWidget(descLabel)
        layout.addLayout(lineLayout)
        layout.addWidget(self.list)
        layout.addStretch()
    
    def exeSet(self):
        r'''
            @brief  選択ノードをセット
            @return (any):
        '''
        sel = cmds.ls(sl=True)
        if not sel:
            print(u'+ 何も選択されていません。')
            return
        self.line.setText(sel[0])
    
    def exeSelect(self):
        r'''
            @brief  リストされたアイテムを選択
            @return (any):
        '''
        node = self.list.selectionModel().currentIndex().data()
        if not cmds.objExists(node):
            return
        
        cmds.select(node,r=True)
    
    def exeExecute(self):
        r'''
            @brief  スキンノードのサーチ
            @return (any):
        '''
        node = self.line.text()
        if not node:
            print(u'+ 何も選択されていません。')
            return
        if not cmds.objExists(node):
            print(u'+ 選択ノード[%s]が存在しません。'%(node))
            return
        
        skin = cmds.ls(type='skinCluster')
        if not skin:
            print(u'+ スキンクラスターが取得出来ませんでした。')
            return
        
        FLAG      = False
        SKIN_LIST = []
        for s in skin:
            con = cmds.listConnections(s,s=True,t='joint')
            for check in con:
                if node == check:
                    if FLAG:
                        continue
                    SKIN_LIST.append(s)
                    FLAG = True
            FLAG = False
        
        NODE_LIST = []
        for sl in SKIN_LIST:
            for t in ['mesh','nurbsSurface','lattice']:
                con = cmds.listConnections(sl,d=True,t=t)
                if not con:
                    continue
                for add in con:
                    NODE_LIST.append(add)
        
        border = ('#'+'+='*40)
        print(border)
        for nl in NODE_LIST:
            print(nl)
        print(border)
        
        model = self.list.model()
        model.removeRows(0, model.rowCount())
        rootItem = model.invisibleRootItem()
        for nl in NODE_LIST:
            item = QtGui.QStandardItem(nl)
            rootItem.setChild(rootItem.rowCount(),0,item)

class SearchSkinClusterUI(sg.EventBaseWidget):
    r'''
        @brief    SearchSkinClusterのUI
        @inherit  sg.EventBaseWidget
        @date     2018/06/07 14:31[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  UIおおもと部分
            @param  parent(any) : enter description
            @return (any):
        '''
        super(SearchSkinClusterUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/06/07'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(280,180)
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}' % (uiName, ss.MAINUIBGC))
        
        main  = SearchSkinClusterMainUI()
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)
    
    # Event ===================================================================
    
    # func ====================================================================

# =============================================================================

# -----------------------------------------------------------------------------
# - simulation
# -----------------------------------------------------------------------------

class FitToMeshMainUI(sg.ScrolledWidget):
    r'''
        @brief    FitToMeshUIメイン部分
        @inherit  sg.ScrolledWidget
        @function buildUI    : レイアウトメイン部分
        @function execute    : fitToMeshの実行
        @function loadObject : 選択している最初のオブジェクトをラインにセットする
        @date     2019/03/11 17:38[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent):
        r'''
            @brief  レイアウトメイン部分
            @param  parent(any) : enter description
            @return (any):
        '''
        self.nameLine = QtWidgets.QLineEdit()
        loadButton = QtWidgets.QPushButton('Load')
        loadButton.clicked.connect(self.loadObject)
        loadLayout = QtWidgets.QHBoxLayout()
        loadLayout.addWidget(self.nameLine)
        loadLayout.addWidget(loadButton)
        
        self.refreshBox = QtWidgets.QCheckBox('Refresh')
        self.geoBox = QtWidgets.QCheckBox('GeometryMode')
        cbLayout = QtWidgets.QHBoxLayout()
        cbLayout.addWidget(self.refreshBox)
        cbLayout.addWidget(self.geoBox)
        cbLayout.addStretch()
        
        apply = QtWidgets.QPushButton('Apply')
        apply.clicked.connect(self.execute)
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addLayout(loadLayout)
        layout.addLayout(cbLayout)
        layout.addStretch()
        layout.addWidget(apply)
        
    def execute(self):
        r'''
            @brief  fitToMeshの実行
            @return (any):None
        '''
        mayaFunc.fitToMesh(
            node    = self.nameLine.text(),
            refresh = self.refreshBox.isChecked(),
            geomode = self.geoBox.isChecked(),
        )
    
    def loadObject(self):
        r'''
            @brief  選択している最初のオブジェクトをラインにセットする
            @return (any):None
        '''
        text = ''
        node = cmds.ls(sl=True)
        if len(node):
            text = node[0]
        self.nameLine.setText(text)

        
class FitToMeshUI(sg.EventBaseWidget):
    r'''
        @brief    FitToMeshのUI
        @inherit  sg.EventBaseWidget
        @date     2017/06/02 9:10[matsuzawa](matsuzawa@gooneys.co.jp)
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  メインUI
            @param  parent(any) : [edit]
            @return (any):None
        '''
        super(FitToMeshUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2017/06/02'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(240,160)
        
        main = FitToMeshMainUI()
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)

# -----------------------------------------------------------------------------

class MoveVertexSameNodeMainUI(sg.ScrolledWidget):
    r'''
        @brief    レイアウト部分
        @inherit  sg.ScrolledWidget
        @function buildUI  : レイアウト記述
        @function setNode  : ノードをセットする関数
        @function exeApply : 実行する関数
        @date     2019/03/11 17:20[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent):
        r'''
            @brief  レイアウト記述
            @param  parent(any) : enter description
            @return (any):
        '''
        fitNodeLayout = QtWidgets.QHBoxLayout()
        fitNodeLabel = QtWidgets.QLabel('Fit Node :')
        self.fitNodeLineEdit = QtWidgets.QLineEdit()
        fitNodeButton = QtWidgets.QPushButton('Set Node')
        fitNodeButton.clicked.connect(self.setNode)
        fitNodeLayout.addWidget(fitNodeLabel)
        fitNodeLayout.addWidget(self.fitNodeLineEdit)
        fitNodeLayout.addStretch()
        fitNodeLayout.addWidget(fitNodeButton)
        
        ratioLayout = QtWidgets.QHBoxLayout()
        ratioLabel = QtWidgets.QLabel('Ratio :')
        self.ratioSpinBox = QtWidgets.QDoubleSpinBox()
        self.ratioSpinBox.setValue(1.0)
        self.ratioSpinBox.setRange(0.0, 1.0)
        self.ratioSpinBox.setSingleStep(0.01)
        self.debugCheckBox = QtWidgets.QCheckBox('Debug :')
        self.debugCheckBox.setChecked(False)
        applyButton = QtWidgets.QPushButton(' Fit Apply ')
        applyButton.clicked.connect(self.exeApply)
        ratioLayout.addWidget(ratioLabel)
        ratioLayout.addWidget(self.ratioSpinBox)
        ratioLayout.addStretch()
        ratioLayout.addWidget(self.debugCheckBox)
        ratioLayout.addWidget(applyButton)
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addLayout(fitNodeLayout)
        layout.addLayout(ratioLayout)

    def setNode(self):
        r'''
            @brief  ノードをセットする関数
            @return (any):None
        '''
        selNode = cmds.ls(sl=True)
        if not selNode:
            return
        self.fitNodeLineEdit.setText(selNode[0])
        
    def exeApply(self):
        r'''
            @brief  実行する関数
            @return (any):None
        '''
        mayaFunc.moveVertexSameNode(
            fitNode  =self.fitNodeLineEdit.text(),
            ratio    =self.ratioSpinBox.value(),
            debugFlag=self.debugCheckBox.isChecked(),
        )
        
class MoveVertexSameNodeUI(sg.EventBaseWidget):
    r'''
        @brief    MoveVertexSameNodeのUI
        @inherit  sg.EventBaseWidget
        @date     2017/07/14 12:26[matsuzawa](matsuzawa@gooneys.co.jp)
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  メインUI
            @param  parent(any) : [edit]
            @return (any):None
        '''
        super(MoveVertexSameNodeUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2017/07/14'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(280,120)
        
        main = MoveVertexSameNodeMainUI()
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)
    
    # Event ===================================================================
    
    # func ====================================================================

# -----------------------------------------------------------------------------

class NClothAttrValuesMainUI(sg.ScrolledWidget):
    r'''
        @brief    NClothAttrValuesUIメイン部分
        @inherit  sg.ScrolledWidget
        @function buildUI     : メインレイアウト部分
        @function exePrint    : nClothAttrValuesの実行
        @function exeSetPaint : 指定のアトリビュートタイプのペイントを実行する
        @date     2019/03/11 17:29[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    nClothParam = (
        'thickness',
        'bounce',
        'friction',
        'damp',
        'stickiness',
        'collideStrength',
        'mass',
        'fieldMagnitude',
        'stretch',
        'bend',
        'bendAngleDropoff',
        'restitutionAngle',
        'rigidity',
        'deform',
        'inputAttract',
        'restLengthScale',
        'lift',
        'drag',
        'tangentialDrag',
        'wrinkle',
    )
    def buildUI(self, parent=None):
        r'''
            @brief  メインレイアウト部分
            @param  parent(any) : enter description
            @return (any):
        '''
        listLabel = QtWidgets.QLabel('Attribute :')
        listLabel.setStyleSheet('QLabel{font-size:11;color:#DDDDDD;}')
        self.listComboBox = QtWidgets.QComboBox()
        self.listComboBox.addItems(self.nClothParam)
        listLayout = QtWidgets.QHBoxLayout()
        listLayout.addWidget(listLabel)
        listLayout.addWidget(self.listComboBox)
        listLayout.addStretch()
        
        setPaintLayout = QtWidgets.QHBoxLayout()
        setPaintLabel = QtWidgets.QLabel(
            u'nClothメッシュを選択してください。'
        )
        self.setPaintCheckBox = QtWidgets.QCheckBox('Open attribute window :')
        self.setPaintCheckBox.setChecked(False)
        setPaintButton = QtWidgets.QPushButton('Set paint')
        setPaintButton.clicked.connect(self.exeSetPaint)
        setPaintLayout.addWidget(self.setPaintCheckBox)
        setPaintLayout.addWidget(setPaintButton)
        
        printLabelA = QtWidgets.QLabel('Paint Attribute Values Print.')
        printLabelA.setStyleSheet('QLabel{font:bold 11px;}')
        printLabelB = QtWidgets.QLabel(
            u'nClothノードを選択してください。'
        )
        printHLayout = QtWidgets.QHBoxLayout()
        printNumLabel = QtWidgets.QLabel(u'Wrap num:')
        self.printNum = QtWidgets.QSpinBox()
        self.printNum.setValue(10)
        self.printNum.setRange(1, 30)
        self.printObjCheckBox = QtWidgets.QCheckBox(u'Write "objExists"')
        self.printObjCheckBox.setChecked(True)
        printHLayout.addWidget(printNumLabel)
        printHLayout.addWidget(self.printNum)
        printHLayout.addWidget(self.printObjCheckBox)
        printButton = QtWidgets.QPushButton('Print')
        printButton.clicked.connect(self.exePrint)
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addLayout(listLayout)
        layout.addStretch()
        layout.addWidget(setPaintLabel)
        layout.addLayout(setPaintLayout)
        layout.addStretch()
        layout.addWidget(printLabelA)
        layout.addWidget(printLabelB)
        layout.addLayout(printHLayout)
        layout.addWidget(printButton)
        
    def exePrint(self):
        r'''
            @brief  nClothAttrValuesの実行
            @return (any):None
        '''
        comboA = self.listComboBox.currentIndex()
        mayaFunc.nClothAttrValuesPrint(
            attribute=self.listComboBox.currentText(),
            wrapNum=self.printNum.value(),
            writeObjExists=self.printObjCheckBox.isChecked(),
        )
    
    def exeSetPaint(self):
        r'''
            @brief  指定のアトリビュートタイプのペイントを実行する
            @return (any):None
        '''
        mayaFunc.nClothAttrValuesPaint(
            attribute  = self.listComboBox.currentText(),
            windowFlag = self.setPaintCheckBox.isChecked(),
        )
        
class NClothAttrValuesUI(sg.EventBaseWidget):
    r'''
        @brief    nClothのアトリビュートを書き出すUI
        @inherit  sg.EventBaseWidget
        @date     2017/06/02 14:18[matsuzawa](matsuzawa@gooneys.co.jp)
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  メインUI
            @param  parent(any) : [edit]
            @return (any):None
        '''
        super(NClothAttrValuesUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/06/02'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(270,240)
        
        main = NClothAttrValuesMainUI()
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)

# -----------------------------------------------------------------------------

class AlignPolyGridMainUI(sg.ScrolledWidget):
    r'''
        @brief    AlignPolyGridUIメイン部分
        @inherit  sg.ScrolledWidget
        @function buildUI    : メイン部分
        @function createGrid : createGridの実行コマンド
        @function cleanup    : cleanupの実行コマンド
        @function finish     : finishの実行コマンド
        @date     2019/03/11 17:41[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self, parent=None):
        r'''
            @brief  メイン部分
            @param  parent(any) : enter description
            @return (any):
        '''
        sel = 'Select'
        grid = 'gridPlane'
        labelFont = 'QLabel{font:bold 11px;}'
        
        labelA = QtWidgets.QLabel('%s Polygon Mesh.' % sel)
        labelB = QtWidgets.QLabel('%s "%s".' % (sel, grid))
        labelC = QtWidgets.QLabel('%s "%s".' % (sel, grid))
        labelA.setStyleSheet('%s' % labelFont)
        labelB.setStyleSheet('%s' % labelFont)
        labelC.setStyleSheet('%s' % labelFont)
        
        buttonA = QtWidgets.QPushButton('Create Grid')
        buttonB = QtWidgets.QPushButton('Cleanup')
        buttonC = QtWidgets.QPushButton('Finish')
        buttonA.clicked.connect(self.createGrid)
        buttonB.clicked.connect(self.cleanup)
        buttonC.clicked.connect(self.finish)
        
        layout = QtWidgets.QVBoxLayout(parent)
        layout.addWidget(labelA)
        layout.addWidget(buttonA)
        layout.addWidget(labelB)
        layout.addWidget(buttonB)
        layout.addWidget(labelC)
        layout.addWidget(buttonC)
    
    def createGrid(self):
        r'''
            @brief  createGridの実行コマンド
            @return (any):None
        '''
        mayaFunc.alignPolyGridCreate()
        
    def cleanup(self):
        r'''
            @brief  cleanupの実行コマンド
            @return (any):None
        '''
        mayaFunc.alignPolyGridCleanup()
        
    def finish(self):
        r'''
            @brief  finishの実行コマンド
            @return (any):None
        '''
        mayaFunc.alignPolyGridFinish()

class AlignPolyGridUI(sg.EventBaseWidget):
    r'''
        @brief    AlignPolyGridのUI
        @inherit  sg.EventBaseWidget
        @date     2017/06/05 9:06[matsuzawa](matsuzawa@gooneys.co.jp)
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self, parent=None):
        r'''
            @brief  UIのメインコード
            @param  parent(any) : [edit]
            @return (any):None
        '''
        super(AlignPolyGridUI, self).__init__(parent)
        
        self.debugFlag = False
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2018/06/05'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(180,230)

        main = AlignPolyGridMainUI()
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(we.getWidget())
        layout.addWidget(main)

# -----------------------------------------------------------------------------
# - other
# -----------------------------------------------------------------------------

class SetDropImageMainUI(sg.ScrolledWidget):
    r'''
        @brief    ドロップテストレイアウト構築ウィジェット
        @inherit  sg.ScrolledWidget
        @function buildUI           : オーバーライド用レイアウト関数
        @function setImageWidget    : enter description
        @function setButtonWidget   : enter description
        @function setLineEditWidget : enter description
        @date     2019/04/02 12:33[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def buildUI(self,parent=None):
        r'''
            @brief  オーバーライド用レイアウト関数
            @param  parent(any) : enter description
            @return (any):
        '''
        self.layout = QtWidgets.QVBoxLayout(parent)
    
    def setImageWidget(self):
        r'''
            @brief  enter description
            @return (any):
        '''
        self.label  = QtWidgets.QLabel('')
        self.layout.addWidget(self.label,alignment=QtCore.Qt.AlignCenter)
    
    def setButtonWidget(self):
        r'''
            @brief  enter description
            @return (any):
        '''
        self.button = QtWidgets.QPushButton('')
        self.layout.addWidget(self.button,alignment=QtCore.Qt.AlignCenter)
    
    def setLineEditWidget(self):
        r'''
            @brief  enter description
            @return (any):
        '''
        self.lineEdit = QtWidgets.QLineEdit('')
        self.layout.addWidget(self.lineEdit,alignment=QtCore.Qt.AlignCenter)
    
class SetDropImageUI(sg.EventBaseWidget):
    r'''
        @brief    ドロップテストUI
        @inherit  sg.EventBaseWidget
        @function dropEvent : ドロップのイベント
        @date     2019/03/26 18:01[matsuzawa@gooneys.co.jp]
        @update   2019/04/22 18:47[matsuzawa@gooneys.co.jp]
    '''
    def __init__(self,parent=None):
        r'''
            @brief  メイン関数
            @param  parent(any) : enter description
            @return (any):
        '''
        super(SetDropImageUI,self).__init__(parent)

        self.debugFlag = False
        self.setAcceptDrops(True)
        self.claName = self.__class__.__name__
        self.version = '1.1a'
        self.author  = 'Matsuzawa Shinya'
        self.release = '2019/03/26'
        self.update  = '2019/04/12'
        self.setWindowTitle(self.claName)
        self.resize(300,300)
        
        uiName = 'ms%s' % (self.claName)
        self.setObjectName(uiName)
        self.setStyleSheet('QWidget#%s{%s}'%(uiName,ss.MAINUIBGC))
        
        tab = QtWidgets.QTabWidget()
        tab.setStyleSheet('QTabWidget{%s}'%(ss.TABBGC))
        
        self.widgetList = []
        for n in ('Replace','Add'):
            buf = SetDropImageMainUI()
            buf.setImageWidget()
            tab.addTab(buf,n)
            self.widgetList.append(buf)
        
        we = sg.WidgetEventAction()
        we.setTitle(self.claName)
        we.setWidget()
        we.setSelf(self)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(we.getWidget())
        self.layout.addWidget(tab)
        
    # Event ===================================================================
    
    def dropEvent(self, event):
        r'''
            @brief  ドロップのイベント
            @param  event(any) : イベントアクション
            @return (any):
        '''
        mime = event.mimeData()
        path = mime.urls()
        for p in path:
            fp = p.toLocalFile()
            A = sg.ImageWidget()
            
            # replace
            A.setSendLabel(self.widgetList[0].label)
            # A.setScaled(0.4,0.4)
            A.setImage(fp)
            
            # add
            A.newLabel()
            # A.setScaled(0.25,0.25)
            A.setImage(fp)
            self.widgetList[1].layout.addWidget(
                A.getImage(),alignment=QtCore.Qt.AlignCenter
            )
            A.setText(fp)
            self.widgetList[1].layout.addWidget(
                A.getText(),alignment=QtCore.Qt.AlignCenter
            )
        
# -----------------------------------------------------------------------------
# =============================================================================
# =============================================================================

def showWindow(widgetType, wfFlag=True, *args, **keywords):
    r'''
        @brief  ウィンドウの表示
        @param  widgetType(any) : [表示するウィンドウの名前]
        @param  wfFlag(any)     : windowFlag取り込ませるかどうかのフラグ
        @param  args(any)       : enter description
        @param  keywords(any)   : enter description
        @return (any):None
    '''
    window = widgetType(MainWindow)
    if wfFlag:
        window.setWindowFlags(QtCore.Qt.Window) # 親に取り込ませないようにする処理
    window.show()
    return window
    
# =============================================================================
# -----------------------------------------------------------------------------
# =============================================================================