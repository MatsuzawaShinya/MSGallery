#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    system系コアメソッドを収集したライブラリファイル
"""
###############################################################################
## add inrtall module
r"""
    playsound
    requests
"""
###############################################################################
## base lib

import os
import re
import sys
import json
import math
import time
import random
import shutil
import string
import base64
import traceback
import subprocess
import unicodedata
from stat import *

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from . import stylesheet as ss
from .sglib import (
    widget as sgwidget, func as sgfunc, info as sginfo
)
PC     = sgfunc.PathClass()
MSINFO = sginfo.MsAppToolsBaseInfo()

## ----------------------------------------------------------------------------
## local lib / ローカル環境に合わせたインポート

try:
    from PySide2 import QtWidgets,QtGui,QtCore
except:
    from . import pyside2
    QtWidgets,QtCore,QtGui = pyside2.QtWidgets,pyside2.QtCore,pyside2.QtGui
try:
    from msAppTools import msAppIcons
    iconFlag = True
except:
    iconFlag = False
try:
    import shiboken2
    from maya import OpenMayaUI
    MainWindow = shiboken2.wrapInstance(
        long(OpenMayaUI.MQtUtil.mainWindow()),QtWidgets.QWidget
    )
    shibokenFlag = True
except:
    shibokenFlag = False

###############################################################################
## - Setting

def path():
    r"""
        ファイルパスのリターン
    """
    return (__file__)

NOW_COMPANY = 'GOONEYS'

_ESTIMATION = MSINFO.getEstimationName()

_defaultFrame = (QtCore.Qt.Window|QtCore.Qt.FramelessWindowHint)
_setWindowFlagsDict = sgwidget._setWindowFlagsDict

msAppToolsName = os.path.basename(os.path.dirname(os.path.dirname(path())))

###############################################################################
## - Global common func

class KeyMethod(sgwidget.KeyMethod):
    r"""
        キーメソッド内包/取得クラス/sgwidget継承
        
    """
    def __init__(self):
        r"""
        """
        super(KeyMethod,self).__init__()

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

## ----------------------------------------------------------------------------
## main widget class

class EventBaseWidget(sgwidget.EventBaseWidget):
    r"""
        << sgwidget継承 >>
        イベントとメニュー付きのウィジェットクラス
    """
    def __init__(self,parent=None):
        r"""
        """
        super(EventBaseWidget,self).__init__(parent)
    
class WidgetEventAction(sgwidget.WidgetEventAction):
    r"""
        << sgwidget継承 >>
        ウィジェット外部の共有パーツクラス
        タイトル/オプション/クローズボタンなど
    """
    def __init__(self,parent=None):
        r"""
        """
        super(WidgetEventAction,self).__init__(parent)

class OptionWidget(sgwidget.OptionWidget):
    r"""
        << sgwidget継承 >>
        オプションウィジェット用のカスタマイズクラス
    """
    def __init__(self,parent=None):
        r"""
        """
        super(OptionWidget,self).__init__(parent)

class ScrolledWidget(sgwidget.ScrolledWidget):
    r"""
        << sgwidget継承 >>
        UIをスクロールを行うための設定
    """
    def __init__(self,parent=None):
        r"""
        """
        super(ScrolledWidget,self).__init__(parent)

## ----------------------------------------------------------------------------
## sub widget class

class AboutUI(sgwidget.EventBaseWidget):
    r"""
        << sgwidget継承 >>
        aboutUI
    """
    def __init__(self,parent=None):
        r"""
        """
        super(AboutUI,self).__init__(parent)

class ImageWidget(sgwidget.ImageWidget):
    r"""
        << sgwidget継承 >>
        イメージをラベル化する
    """
    def __init__(self, parent=None):
        r"""
        """
        super(ImageWidget,self).__init__(parent)
        
class ListView(sgwidget.ListView):
    r"""
        << sgwidget継承 >>
        カテゴリ毎のアイテムを作るリストビュー
    """
    def __init__(self,parent=None):
        r"""
        """
        super(ListView,self).__init__(parent)

class PushButton(sgwidget.PushButton):
    r"""
        << sgwidget継承 >>
        PushButton/カスタムウィジェット
    """
    def __init__(self,textbutton='',parent=None):
        r"""
        """
        super(PushButton,self).__init__(textbutton,parent)

class SuggestView(sgwidget.SuggestView):
    r"""
        << sgwidget継承 >>
        予測変換サジェストウィジェット
    """
    def __init__(self,parent=None):
        r"""
        """
        super(SuggestView,self).__init__(parent)

class FlodingFrameLayout(sgwidget.FlodingFrameLayout):
    r"""
        << sgwidget継承 >>
        折畳式のフレームウィジェットを作成するクラス
    """
    def __init__(self,parent=None):
        r"""
        """
        super(FlodingFrameLayout,self).__init__(parent)

class SystemTrayIcon(sgwidget.SystemTrayIcon):
    r"""
        << sgwidget継承 >>
        システムトレイアイコンの設定
    """
    def __init__(self,showTime=10000,parent=None):
        r"""
        """
        super(SystemTrayIcon,self).__init__(showTime,parent)

class TimeLine(sgwidget.TimeLine):
    r"""
        << sgwidget継承 >>
        タイムライン設定のクラス
    """
    def __init__(self,timeout=100,interval=10,curveShape='linearCurve'):
        r"""
        """
        super(TimeLine,self).__init__(timeout,interval,curveShape)

class HorizonFrame(sgwidget.HorizonFrame):
    r"""
        << sgwidget継承 >>
        横線を入れるクラス
    """
    def __init__(self,bold=1,color='#EEE',parent=None):
        r"""
        """
        super(HorizonFrame,self).__init__(bold,color,parent)

class SliderField(sgwidget.SliderField):
    r"""
        << sgwidget継承 >>
        スライダーフィールド親元コード
    """
    def __init__(self, parent=None):
        r"""
            メインUI
        """
        super(SliderField, self).__init__(parent)

class BusyBar(sgwidget.BusyBar):
    r"""
        << sgwidget継承 >>
        ビジー状態のウィジェットバーを表示するクラス
    """
    def __init__(self,iconName='bar-1',parent=None):
        r"""
        """
        super(BusyBar,self).__init__(iconName,parent)
        
class ProgressBar(sgwidget.ProgressBar):
    r"""
        << sgwidget継承 >>
        プログレスバーウィジェット
    """
    def __init__(self,parent=None):
        r"""
        """
        super(ProgressBar,self).__init__(parent)

## ----------------------------------------------------------------------------
## custom class

class PathStoreList(sgwidget.PathStoreList):
    r"""
        << sgwidget継承 >>
        パス情報のまとめクラス
    """
    def __init__(self,uiname='SYSTEMGENERAL',parent=None):
        r"""
        """
        super(PathStoreList,self).__init__(uiname,parent)

class VariableManagement(sgwidget.VariableManagement):
    r"""
        << sgwidget継承 >>
        ウィジェット作成された情報をまとめ管理/運用するクラス
    """
    def __init__(self):
        r"""
        """
        super(VariableManagement,self).__init__()

class ConstructionUiFunction(sgwidget.ConstructionUiFunction):
    r"""
        << sgwidget継承 >>
        共通のクラスUIを作成しオブジェクト変数をリターンするクラス
    """
    def __init__(self):
        r"""
        """
        super(ConstructionUiFunction,self).__init__()

class TimeEvent(sgwidget.TimeEvent):
    r"""
        << sgwidget継承 >>
        タイムイベントの設定
    """
    def __init__(self,parent=None):
        r"""
        """
        super(TimeEvent,self),__init__(parent)

class SpecifiedKeyLimitJudgment(sgwidget.SpecifiedKeyLimitJudgment):
    r"""
        << sgwidget継承 >>
        決められた秒数内で指定されたリストのキー情報を取得し
        判定を返すメソッドを集約した専用クラス
    """
    def __init__(self,conditionKeyList=[],limitKeyTime=1.0):
        r"""
        """
        super(SpecifiedKeyLimitJudgment,self).__init__(
            conditionKeyList,limitKeyTime)

###############################################################################
###############################################################################
## - Common func
        
###############################################################################
## - Path func / 互換性を維持するため関数を整理して格納

getPathList     = PC.getPathList
slashConversion = PC.slashConversion
toBasePath      = PC.toBasePath
toReversePath   = PC.toReversePath
getExtension    = PC.getExtension
getRoamingPath  = PC.getRoamingPath

###############################################################################
## - webbrowser

def webbrowser(url='',browser='chrome'):
    r"""
        webページへのアクセス
    """
    import webbrowser
    
    iePath     = r'C:/Program Files (x86)/Internet Explorer/iexplore.exe'
    chromePath = r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    EXPLORER_LIST = {
        'ie'               : iePath,
        'internetexplorer' : iePath,
        'google'           : chromePath,
        'chrome'           : chromePath,
        'googlechrome'     : chromePath,
    }
    
    try:
        browserPath = EXPLORER_LIST[browser]
    except KeyError as instance:
        print(u'+ EXPLORER_LISTのKeyError => [%s]' % (instance))
        return
    
    try:
        if os.path.isfile(browserPath):
            b = webbrowser.get('"'+browserPath+'" %s')
            b.open(url)
        else:
            webbrowser.open(url)
    except:
        print(u'+ webbrowserの実行中にエラーが発生しました。')
        
###############################################################################
## - ffmpeg

def ffmpegOption(option='help',**keywords):
    r"""
        ffmpegに関する関数
    """
    # 順番通りに回したいのでリスト
    __SCHEMA_LIST = (
        ['help',[
            (u'ヘルプコマンドを表示'),
        ]],
        ['resolution',[
            (u'レゾリューションを返す。[0]=width,[1]=height'),
            (u'必要引数:'),
            (u'\tpath = [解像度を取得するデータパス]'),
        ]],
        ['conversion',[
            (u'動画のサイズを指定した割合大きさで変換'),
            (u'必要引数:'),
            (u'\ts_path = [元データのパス]'),
            (u'\td_path = [変換先の出力パス]'),
            (u'\tratio  = [サイズを変更する割合]'),
            (u'\t\tratio推奨数値 : "100"=(100%),"75"=(3/4),"50"=(半分),"25"=(1/4)'),
        ]],
    )
    
    # 動画解像度の下限は最低でも1px(1桁)
    # 上限は基本4桁で十分だが10000px以上に対応する為5桁に設定
    mm = ('1','5')
    __FFMPEG_REGULAR_EXPRESSION_LIST = (
        {'resolution' : (
                '(, )([0-9]{%(min)s,%(max)s})(x)([0-9]{%(min)s,%(max)s})(, )'%{
                    'min':mm[0],'max':mm[1] },
                '(, )([0-9]{%(min)s,%(max)s})(x)([0-9]{%(min)s,%(max)s})( [[])'%{
                    'min':mm[0],'max':mm[1] },
            )
        }
    )
    
    ffmpegPath = None
    
    if NOW_COMPANY == 'GOONEYS':
        try:
            from gnExternal import ffmpeg
        except:
            print(u'+ gnExternalからffmpegを読み込めませんでした')
            return
        ffmpegPath = ffmpeg.ffmpeg().path()
    
    s_path  = None
    d_path  = None
    ratio   = 100
    dirFlag = True
    
    for key in keywords:
        if key == 's_path':
            s_path  = keywords[key]
        elif key == 'd_path':
            d_path  = keywords[key]
        elif key == 'ratio':
            ratio   = keywords[key]
        elif key == 'dirFlag':
            dirFlag = keywords[key]
            
    def _extraction(s_path):
        r"""
            情報の抽出
        """
        if not os.path.isfile(s_path):
            print(u'+ 対象のパスにデータがありませんでした。[path="%s"]'%(s_path))
            return None
        
        devnull = open(os.devnull, "wb")
        data = subprocess.Popen(
            [ffmpegPath,'-i',s_path],
            shell  = True,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            stdin  = devnull
        )
        devnull.close()
        c = data.communicate() # [0]=data,[1]=None, -> use=[0]
        
        return c[0]
    
    def exe_help():
        r"""
            helpコマンドの表示
        """
        LINE = ('%s%s%s'%('+',('-'*120),'+')) 
        print(LINE)
        print(u"option='XXX'でXXXにコマンドを指定して実行する")
        print(u"デフォルト設定='option=help'")
        for _SL in __SCHEMA_LIST:
            print('\t%s :'%(_SL[0]))
            for _sl in _SL[1]:
                print('\t\t%s'%(_sl))
        print(LINE)
        
        return True
    
    def exe_resolution(s_path):
        r"""
            解像度のリターン
        """
        ext    = _extraction(s_path)
        s_list = []
        for f_re in __FFMPEG_REGULAR_EXPRESSION_LIST['resolution']:
            re_res = re.search(f_re,ext)
            if not re_res:
                continue
            s_list = re_res.groups()
        
        return((s_list[1],s_list[3]) if s_list else (0,0))
    
    def exe_conversion(s_path,d_path,ratio):
        r"""
            動画を半分のサイズに変換
        """
        def _round(num):
            r"""
                数値の下一桁切り捨て
            """
            return int((num//10)*10)
            
        if not os.path.isfile(s_path):
            print(u'+ 対象のファイルパスが見つかりません。[path=%s]'%(p))
            return None
        
        # 書き出す先のフォルダパスがない場合
        # 処理が失敗するのでフォルダを作成する
        if dirFlag:
            dirPath = os.path.dirname(d_path)
            if not os.path.isdir(dirPath):
                os.makedirs(dirPath)
                
        rezo = exe_resolution(s_path)
        w    = int(int(rezo[0])*(ratio//100.0))
        h    = int(int(rezo[1])*(ratio//100.0))
        # 動画変換する際、決まった数値(100%,75%,50%,25%)以外の割合比率で変換すると
        # 解像度の下一桁が0になっていないとエラーになる？(1864→NG,1860→OK)
        if not ratio in [25,50,75,100]:
            w = _round(w)
            h = _round(h)
        subprocess.Popen(
            [ffmpegPath,'-y','-i',s_path,'-s','x'.join(map(w,h)),d_path]
        )
        print(u'Base width  : %s'%(rezo[0]))
        print(u'Conv width  : %s'%(w))
        print(u'Base height : %s'%(rezo[1]))
        print(u'Conv height : %s'%(h))
        
        return True
        
    ## ------------------------------------------------------------------------
    ## execute
    
    returnList = None
    
    if option == 'help':
        returnList = exe_help()
    elif option == 'resolution':
        returnList = exe_resolution(
            s_path = s_path
        )
    elif option == 'conversion':
        returnList = exe_conversion(
            s_path = s_path,
            d_path = d_path,
            ratio  = ratio,
        )
    else:
        print(u'+ option引数[%s]の不一致'%(option))
    
    return returnList
    
###############################################################################
## - Time data func

def getDateTime(returnType=True):
    r"""
        現在の日付などを配列にしてリターンする
    """
    dict = None
    if returnType:
        dict = {}
    else:
        dict = {'keyTypeList':['year','month','day','time','ymd','hms']}
        return dict
    
    import datetime
    now = datetime.datetime.now()
    y1  = now.strftime('%Y')
    y2  = now.strftime('%y')
    mo  = now.strftime('%m')
    d   = now.strftime('%d')
    h   = now.strftime('%H')
    m   = now.strftime('%M')
    s   = now.strftime('%S')
    dict.update({'year' :[y1,y2]})
    dict.update({'month':[mo]})
    dict.update({'day'  :[d]})
    dict.update({'time' :[h,m,s]})
    dict.update({'hms'  :['%s%s%s'%(h,m,s),'%s:%s:%s'%(h,m,s)]})
    dict.update({'ymd'  :[
        '%s%s%s'  %(y1,mo,d),'%s%s%s'  %(y2,mo,d),
        '%s/%s/%s'%(y1,mo,d),'%s/%s/%s'%(y2,mo,d)
    ]})

    return dict
    
def getFileData(path,mode=None):
    r"""
        ファイルデータのメタデータを返す
    """
    if not path or not os.path.isfile(path):
        return
    '''
    os.stat(path)
    st_mode  : 保護モードビット
    st_ino   : i ノード番号
    st_dev   : デバイス
    st_nlink : ハードリンク数,
    st_uid   : 所有者のユーザ ID
    st_gid   : 所有者のグループ ID
    st_size  : ファイルのバイトサイズ
    st_atime : 最終アクセス時刻
    st_mtime : 最終更新時刻
    st_ctime : プラットフォーム依存：
                Unix では最終メタデータ変更時刻
                Windows では作成時刻
    '''
    st_d = {
        'mode' :ST_MODE,
        'ino'  :ST_INO,
        'dev'  :ST_DEV,
        'nlink':ST_NLINK,
        'uid'  :ST_UID,
        'gid'  :ST_GID,
        'size' :ST_SIZE,
        'atime':ST_ATIME,
        'mtime':ST_MTIME,
        'ctime':ST_CTIME,
    }
    if not mode in st_d:
        raise RuntimeError('+ Dictionary data mismatch')
    return os.stat(path)[st_d[mode]]
    
def getLastUpdateTime(path, returnType=True):
    r"""
        ファイルの最終更新日のデータを返す
    """
    dict = None
    if returnType:
        dict = {}
    else:
        dict = {'keyTypeList':['year','month','day','time','ymd','hms','all']}
        return dict

    if not os.path.isfile(path):
        return dict
    
    _TD = {
        'ts':time.strftime,
        'tl':time.localtime,
    }
    mt = getFileData(path,'mtime')
    y1 = _TD['ts']('%Y',_TD['tl'](mt))
    y2 = _TD['ts']('%y',_TD['tl'](mt))
    mo = _TD['ts']('%m',_TD['tl'](mt))
    d  = _TD['ts']('%d',_TD['tl'](mt))
    h  = _TD['ts']('%H',_TD['tl'](mt))
    m  = _TD['ts']('%M',_TD['tl'](mt))
    s  = _TD['ts']('%S',_TD['tl'](mt))
    dict.update({'year' :[y1,y2]})
    dict.update({'month':[mo]})
    dict.update({'day'  :[d]})
    dict.update({'time' :[h,m,s]})
    dict.update({'hms'  :['%s%s%s'%(h,m,s),'%s:%s:%s'%(h,m,s)]})
    dict.update({'ymd'  :[
        '%s%s%s'  %(y1,mo,d),'%s%s%s'  %(y2,mo,d),
        '%s/%s/%s'%(y1,mo,d),'%s/%s/%s'%(y2,mo,d),
    ]})
    dict.update({'all'  :[time.ctime(mt)]})
    
    return dict

###############################################################################
## - Zip

def createZipFile(srcpath,dstpath,dstname,createMode=1,**keywords):
    r"""
        対象データをzip化
        Args:
            srcpath (any):zip化するデータパス
            dstpath (any):書き出し先のパス
            dstname (any):書き出しzipのファイル名
            createMode (any):圧縮タイプのモデル
            **keywords (any):
    """
    if not srcpath or not os.path.exists(srcpath):
        raise RuntimeError(u'+ Error in srcpath.')
    if not dstpath or not os.path.exists(dstpath):
        raise RuntimeError(u'+ Error in dstpath.')
    
    _ext = 'zip'
    _exeFilterList ,_nameFilterList  = [],[]
    _extExcludeList,_nameExcludeList = [],[]
    for key in keywords:
        if key == 'extFilter':
            _exeFilterList   = keywords[key]
        elif key == 'nameFilter':
            _nameFilterList  = keywords[key]
        elif key == 'extExclude':
            _extExcludeList  = keywords[key]
        elif key == 'nameExclude':
            _nameExcludeList = keywords[key]
    
    filterValue  = len([x for x in (_exeFilterList ,_nameFilterList)  if x])
    excludeValue = len([x for x in (_extExcludeList,_nameExcludeList) if x])
        
    checkExt = getExtension(dstname)
    dstname  = ('{}{}'.format(
            dstname,('.{}'.format(_ext) if createMode == 1 else '')
        ) if not checkExt or not checkExt in 'zip' else dstname)
    
    def _mode1():
        r"""
            zip圧縮実行 mode=1
        """
        try:
            import zipfile
        except ImportError:
            print(u'+ "zipfile"のインポートに失敗しました。')
            return False
            
        _targetFileList = []
        def _recursive(fp):
            r"""
                ターゲットフォルダ以下のファイルを格納する再帰関数
            """
            def _PRINT(type,file,name=True,mode=True):
                r"""
                    ログ出力のまとめ
                """
                name_t = 'Ext'     if name == 1 else 'Name'
                mode_t = 'exclude' if mode == 1 else 'filter'
                try:
                    log  = ('+ {} {} hit.\n'.format(name_t,mode_t))
                    log += ('\t{} => {}\n'.format(
                        mode_t.title(),toEncode(type,'cp932')))
                    log += ('\t{} => {}'.format(
                        'File'.ljust(len(mode_t)),toEncode(file,'cp932')))
                except:
                    log += (u'!! プリント文字列が正常に処理できませんでした !!')
                print(log)
            
            _fp = toBasePath(fp)
            if os.path.isfile(_fp):
                ext,_excludeFlag,_filterFlag = getExtension(_fp),0,0
                # filter設定がされている場合
                if filterValue:
                    if ext in _exeFilterList:
                        _filterFlag += 1
                        _PRINT(ext,_fp,True,False)
                    for n in _nameFilterList:
                        if n in os.path.basename(_fp):
                            _filterFlag += 1
                            _PRINT(n,_fp,False,False)
                    if _filterFlag >= filterValue:
                        _targetFileList.append(_fp)
                # excludeが設定されている場合
                elif excludeValue:
                    if ext in _extExcludeList:
                        _excludeFlag += 1
                        _PRINT(ext,_fp,True,True)
                    for n in _nameExcludeList:
                        if n in os.path.basename(_fp):
                            _excludeFlag += 1
                            _PRINT(n,_fp,False,True)
                    if _excludeFlag == 0:
                        _targetFileList.append(_fp)
                # filter,exclude設定無しファイルすべて圧縮
                else:
                    _targetFileList.append(_fp)
            else:
                ([_recursive(os.path.join(_fp,u)) for u in os.listdir(_fp)])

        _recursive(srcpath)
        if not _targetFileList:
            return
        _targetFileList.sort()
        
        with zipfile.ZipFile(
            toBasePath(os.path.join(dstpath,dstname)),
            mode='w',compression=zipfile.ZIP_DEFLATED
        ) as new_zip:
            for file in _targetFileList:
                _f = toBasePath(file)
                _d = toBasePath(srcpath)
                _a = toEncode(_f.replace(_d,''),'cp932')
                new_zip.write(_f,arcname=_a)
        
        print(u'+ Complite zip file, mode = 1')
        print(u'\t Export dir  = {}'.format(dstpath))
        print(u'\t Export name = {}'.format(dstname))
        print('')
        
    def _mode2():
        r"""
            zip圧縮実行 mode=2
        """
        src   = srcpath
        dst   = toBasePath(os.path.join(dstpath,dstname))
        ftype = _ext
        shutil.make_archive(dst,ftype,root_dir=src)
        
        print(u'+ Complite zip file, mode = 2')
        print('')
        
    cmd_dict = {
        1 : _mode1,
        2 : _mode2,
    }
    success = None

    try:
        cmd_dict[createMode]()
        success = True
    except:
        traceback.print_exc()
        success = False
    
    return success
        
###############################################################################
## - Desktop

class DesktopInfo(object):
    r"""
        デスクトップ情報管理クラス
    """
    def __init__(self):
        r"""
        """
        self.__qdesktopwidget = QtWidgets.QDesktopWidget()
        
    def getWidgetDesktopSize(self,widget,listtype=False):
        r"""
            指定したウィジェットがあるディスプレイのQRect情報を取得
        """
        rect = self.__qdesktopwidget.availableGeometry(
            self.getWidgetDesktopNumber(widget))
        return (rect if not listtype else
            [rect.x(),rect.y(),rect.width(),rect.height()])
            
    def getWidgetDesktopNumber(self,widget):
        r"""
            指定したウィジェットが存在するディスプレイナンバーを取得
        """
        return self.__qdesktopwidget.screenNumber(widget)

###############################################################################
## - System

def setDontWriteBytecode(val):
    r"""
        dont_write_bytecode/設定
    """
    sys.dont_write_bytecode = val

def getDontWriteBytecode():
    r"""
        dont_write_bytecode/取得
    """
    return sys.dont_write_bytecode

def getPythonInstallPath(full=False):
    r"""
        pythonがインストールされているディレクトリを取得
            full=Trueでexeまでのパス
    """
    return (slashConversion(sys.executable)
        if full else slashConversion(sys.exec_prefix))

def getPythonVersion():
    r"""
        pythonバージョンを確認し状態を返す
        27/37
    """
    pt = re.compile('[0-9]+')
    rr = pt.search(os.path.basename(getPythonInstallPath()))
    return (rr.group() if rr else '')

def fileTypeCheck(filePath):
    r"""
        ファイルパスのタイプチェック
    """
    return (True if os.path.isfile(filePath) else False)

def getFileSize(filepath):
    r"""
        ファイルのサイズを返す。取得できなかった場合はｰ1を返す
    """
    try:
        return int(os.path.getsize(filepath))
    except:
        return -1

def getFileLine(filepath):
    r"""
        ファイルのライン数を返す。取得できなかった場合はｰ1を返す
    """
    pver = int(getPythonVersion()[0])
    try:
        # version : 2
        if pver == 2:
            return (sum([1 for x in open(filepath)]))
        # version : 3
        elif pver == 3:
            return (sum([1 for x in open(filepath,'r',encoding='utf-8')]))
        # other
        else:
            pass
    except:
        traceback.print_exc()
        return -1

def numberFiles(filePath,countup=False):
    r"""
        パスにあるファイル個数のリターン
    """
    if not filePath or not os.path.isdir(filePath):
        return None
    return ((len(([f for f in os.listdir(filePath)
        if os.path.isfile(os.path.join(filePath,f))]))+(1 if countup else 0)))
    
def dirTypeCheck(filePath):
    r"""
        フォルダパスのタイプチェック
    """
    return (True if os.path.isdir(filePath) else False)

def getString():
    r"""
        stringを参照して指定文字列を返す
    """
    _D = {}
    _D['help'] = [
        'ascii_letters',
        'letters',
        'ascii_lowercase',
        'ascii_uppercase',
        'digits',
        'hexdigits',
        'octdigits',
        'punctuation',
        'whitespace',
        'printable',
    ]
    # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _D['ascii_letters'] = string.ascii_letters
    # _D['letters'] = string.letters
    
    # abcdefghijklmnopqrstuvwxyz
    _D['ascii_lowercase'] = string.ascii_lowercase
    
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    _D['ascii_uppercase'] = string.ascii_uppercase
    
    # 0123456789
    _D['digits'] = string.digits
    
    # 01234567
    _D['octdigits'] = string.octdigits
    
    # 0123456789abcdefABCDEF
    _D['hexdigits'] = string.hexdigits
    
    # !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    _D['punctuation'] = string.punctuation
    
    # \t\n\x0b\x0c\r '
    _D['whitespace'] = string.whitespace
    
    # 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    # !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c
    _D['printable'] = string.printable

    return _D
    
def getWordList():
    r"""
        ワードリストのリターン
        
        Returns:
            any:
    """
    _D = getString()
    return {
        0:_D['ascii_lowercase'],
        1:_D['ascii_uppercase'],
        2:_D['digits'],
    }

def returnRandomString(
    length=4,word='%s%s%s'%(getWordList()[0],getWordList()[1],getWordList()[2])
):
    r"""
        文字列をランダムに羅列して返す
    """
    return ''.join([random.choice(word) for i in range(length)])

def connectStringDigits(prefix='',index=[0,1],suffix='',padding=0,addword='0'):
    r"""
        文字+インデント数+文字を接合しリストで返す
        生成する文字列数はindex回数分行う
    """
    return ([('{}{:%s>%s}{}'%(addword,padding)).format(
        prefix,str(i),suffix) for i in range(index[0],index[1]+1)])

def toEncode(w,code='utf-8'):
    r"""
        encode(unicode -> bytes)への変換
            Python2 -> unicodeとstrの互換で必要
            Python3 -> strとstrのみのなので処理は不要
    """
    if getPythonVersion()=='27':
        return w.encode(code)
    else:
        return w
    
def toDecode(w,code='utf-8'):
    r"""
        decode(bytes -> unicode)への変換
            Python2 -> unicodeとstrの互換で必要
            Python3 -> strとstrのみのなので処理は不要
    """
    if getPythonVersion()=='27':
        return w.decode(code)
    else:
        return w
    
def threeByteWordCheck(word=''):
    r"""
        2byte文字(日本語)がある場合のチェック
    """
    RES = False
    try:
        # RES = (True if ([w for w in word.decode('utf-8')
        RES = (True if ([w for w in word
            if unicodedata.east_asian_width(w) == 'W']) else False)
    except:
        RES = True
    return RES
    
def toUnicode(unistr):
    r"""
        unicode文字列への変換
    """
    for charset in [u'cp932',u'utf-8',u'euc-jp',u'shift-jis',u'iso2022-jp']:
        try:
            return unistr.decode(charset)
        except:
            pass
    return unistr
        
def checkJapanese(STR):
    r"""
        日本語のチェック
    """
    for ch in STR:
        name = unicodedata.name(ch) 
        if 'CJK UNIFIED'  in name \
            or 'HIRAGANA' in name \
            or 'KATAKANA' in name:
            return True
    return False

def alphabeticNumberConversion(word,output=True):
    r"""
        アルファベットと進数の変換関数
    """
    _N  = 26
    _D  = getString()
    _E1 = _D['ascii_uppercase']
    _E2 = _D['ascii_lowercase']
    
    # if isinstance(word,bytes):
    if isinstance(word,str):
        _res = re.search('^[A-Za-z]+$',word)
        if _res:
            _RETURN = 0
            R = _res.group()
            for i,r in enumerate(R):
                _STR = _E1 if r.isupper() else _E2
                _RETURN += ((_STR.index(r)+1)*(_N**(len(R)-i-1)))
            return _RETURN
    elif isinstance(word,int):
        _STR = _E1 if output else _E2
        def _loop(_INT,BUF=''):
            r"""
                数値から英字に変換する再帰関数
            """
            _RETURN = ''
            _BUF = ''+BUF
            _int = (_INT // _N)
            _rem = (_INT %  _N)
            if _int > _N:
                _BUF += _STR[_rem-1]
                return _loop(_int+(-1 if _rem==0 else 0),_BUF)
            # Z(26番目)は余りに0が来て処理が正しく行われないため
            # 数値を決め打ちで合わせて処理を合わせる
            _int = (_int-1+(-1 if _rem == 0 else 0))
            _rem = (_rem-1+(26 if _rem == 0 else 0))
            _RETURN += (_BUF[:-1] if _rem == 0 else _BUF)
            _RETURN += _STR[_rem]
            _RETURN += _STR[_int]
            return _RETURN[::-1]
        
        _RET = _loop(word)
        return _RET if word > 26 else _RET[-1]
    else:
        return None
    
def importModuleList(sortFlag=True):
    r"""
        インポートされているモジュールを返す
    """
    try:
        import pkgutil
    except ImportError:
        print(u'+ "pkgutil"のインポートに失敗しました。')
        return False
    
    L = ([str(m).split(' ')[-2].replace("'",'').replace(',','')
        for m in pkgutil.iter_modules()])
    # (str(m).split(' ')[-2].replace("'",'').replace(',',''))
    # (str(m).split(' ')[-2].replace("'",'').replace('"','')[0:-1])
    # (str(m).split(' ')[-2][1:-2].replace("'",'').replace('"',''))
    
    # L.sort() if sortFlag else None
    # return L
    return L.sort() if sortFlag else L

def getEnvironmentVariable(sort=True,printFlag=False,target=None):
    r"""
        環境変数一覧の取得
        Args:
            sort (any):リストソートフラグ
            printFlag (any):プリント許可のフラグ
            target (any):ターゲット指定にされた環境変数内容の取得無ければNone
        Returns:
            target=<True:bytes>,<False:list([0]=環境変数名,[1]=アイテム)>
    """
    # 環境変数を見る方法 -> os.environ['HOGE']
    returnList = []
    envList    = os.environ.items()
    if sort:
        envList.sort()
    for n,i in envList:
        new = i.replace('\\','/')
        returnList.append([n,new])
    targetList = None
    for n,i in returnList:
        if target and n == target:
            targetList = i
        if printFlag:
            print('Name : {}\nItem : {}\n'.format(n,i))
    return returnList if not targetList else targetList

def openExplorer(path,fileflag=False):
    r"""
        指定したパスのエクスプローラーフォルダを開く
        ファイルが指定されていた場合はそのフォルダを開く
    """
    try:
        p = toReversePath(path)
        if threeByteWordCheck(p):
            print(u'+ パスに日本語が含まれている為フォルダを開けませんでした。')
            FLAG = False
        else:
            targetpath = toReversePath(
                os.path.dirname(p) if os.path.isfile(p) and not fileflag else p)
            subprocess.Popen(['explorer',targetpath])
            FLAG = True
    except:
        traceback.print_exc()
        FLAG = False
    return FLAG
    
def executeFile(filePath,app='default'):
    r"""
        対象ファイルのアプリケーション実行
    """
    if not filePath:
        return None
    if not os.path.isfile(filePath):
        print(u'+ filePath[%s]のファイルが見つかりません'%(filePath))
        return None
    
    __APP_SCHEMA_PATH_LIST = {
        'photoshop' : r'C:\Program Files\Adobe\Adobe Photoshop CS6 (64 Bit)\Photoshop.exe',
        'paint'     : r'C:\Windows\System32\mspaint.exe',
    }
    
    cmd = []
    app = app.lower()
    
    if app == 'help':
        print(u'+ app=XXX で使えるフラグリストです（小文字強制変換有）')
        print(u'\t[help] :')
        print(u'\t\tヘルプを表示します。')
        print(u'\t[default] :')
        print(u'\t\tデフォルト設定されているアプリケーションで開きます')
        print(u'\t[photoshop] :')
        print(u'\t\tフォトショップで開きます。')
        print(u'\t[paint] :')
        print(u'\t\tデフォルトペイントソフトで開きます。')
        return True
    elif app == 'default':
        cmd = ('cmd.exe', '/C', filePath)
    elif app == 'photoshop':
        cmd = (__APP_SCHEMA_PATH_LIST[app], filePath)
    elif app == 'paint':
        cmd = (__APP_SCHEMA_PATH_LIST[app], filePath)
    
    # callだと開いたアプリ（子プロセス）を終了しないと
    # maya（親プロセス）が動かないのでPopen
    # v = subprocess.call(cmd)
    v = subprocess.Popen(cmd)
    
    return (True if v == 0 else False)

def textCopy(text):
    r"""
        引数の文字をクリップボードに貼り付け
    """
    returnFlag = None
    
    try:
        # QtWidgets.QApplication.clipboard().setText(text)
        QtGui.QClipboard().setText(text)
        returnFlag = True
    except:
        print(u'+ テキストのクリップボード貼り付けに失敗しました。')
        returnFlag = False
    
    return returnFlag

def imageCopy(imagePath):
    r"""
        イメージをクリップボードに貼り付け
    """
    if not imagePath or not os.path.isfile(imagePath):
        print(
            u'+ imagePathが無いかパス先にデータがありません。[%s]'%(imagePath)
        )
        return False
    
    returnFlag = None
    
    try:
        c = QtGui.QClipboard()
        c.setImage(QtGui.QImage(imagePath))
        if re.search('(null)', str(c.image())):
            print(
                u'+ イメージのクリップボード貼り付けに成功しましたが'
                u'nullタイプのファイル形式です。'
            )
            print(u'\tImagePath : %s'%(imagePath))
            returnFlag = False
        else:
            returnFlag = True
    except:
        print(u'+ イメージのクリップボード貼り付けに失敗しました。')
        returnFlag = False
    
    return returnFlag

def exportClipboradImage(path,name='',ext='png',opendir=False,**keywords):
    r"""
        クリップボードにイメージデータがあるなら書き出す
            path:書き出し先のパス
            name:書き出しファイル名(無名でランダムな名前を指定)
            ext:書き出し拡張子
            opendir:書き出し後に先出し先のフォルダを開くか
    """
    prefix,suffix,connect,padding,len = '','','','',20
    for key in keywords:
        if 'specify' in key:
            name = keywords[key]
        elif 'prefix' in key:
            prefix = keywords[key]
        elif 'suffix' in key:
            suffix = keywords[key]
        elif 'connect' in key:
            connect = keywords[key]
        elif 'padding' in key:
            padding = keywords[key]
        elif 'length' in key:
            len = keywords[key]
    
    def __getName():
        r"""
            prifex,suffixを交えた名前作成
        """
        TEX  = ''
        _pad = ('{:0>%s}'%(padding)).format(numberFiles(path,True))
        strt = str('-'.join(str(time.time()).split('.')))
        if name:
            if padding:
                TEX += ('{}{}{}').format(_pad,connect,name)
            else:
                TEX += '{}.{}-{}'.format(
                    name,getDateTime()['ymd'][0],getDateTime()['hms'][0])
        else:
            if padding:
                TEX += ('{}{}').format(_pad,connect)
            if prefix:
                TEX += '{}{}'.format(prefix,connect)
            TEX += ('{}_{}_{}'.format(
                getDateTime()['ymd'][0],strt,returnRandomString(length=len)))
            if suffix:
                TEX += '{}{}'.format(connect,suffix)
        return TEX
    def _nameCheck(fullPath):
        r"""
            書き出しネームが同じになっていないかのチェック
        """
        def _loop(fullPath,name=None):
            r"""
                チェックの再帰関数
            """
            if os.path.isfile(fullPath):
                print(u'+ Check for duplicate names, Repeat.')
                print(u'\t> {}'.format(fullPath))
                n = __getName()
                e = os.path.join(path,'%s.%s'%(n,ext))
                _loop(e,n)
            return (toBasePath(fullPath),name)
        return _loop(fullPath,name)
    
    if not path:
        print(u'+ パスが入力されていません。')
        return False
    if not os.path.isdir(path):
        print(u'+ 書き出し先のフォルダが見つかりません。')
        return False
    if not clipboradDataCheck() == 2:
        print(u'+ クリップボードに貼られているのがイメージではありません。')
        return False
        
    name = __getName()
    ext  = ext.lower()
    c    = QtGui.QClipboard()
    i    = QtGui.QImage(c.image())
    ep,name = _nameCheck(os.path.join(path,'%s.%s'%(name,ext)))
    
    try:
        i.save(ep,ext)
    except:
        print(u'+ 画像の書き出しに失敗しました。')
        return False
    
    if opendir:
        openExplorer(path)

    dt = getDateTime()
    print(u'+ Export log')
    print(u'\tDate : {} - {}'.format(dt['ymd'][2],dt['hms'][1]))
    print(u'\tPath : {}'.format(path))
    print(u'\tName : {}'.format(name))
    print(u'\tExt  : {}'.format(ext))
    print(u'\tWxH  : {}x{}'.format(i.width(),i.height()))
    print(u'\tFull : {}'.format(ep))
    
    return ep
        
def clipboradDataCheck():
    r"""
        クリップボードのデータをチェックしてパターンを返す
        any:[1]=text,[2]=image,[0]=それ以外
    """
    c = QtGui.QClipboard()
    return(2 if c.mimeData().hasImage() else 1 if c.mimeData().hasText() else 0)
        
def getImageSize(imagePath):
    r"""
        イメージファイルパスのリターン
        [0]=width,[1]=height
    """
    if not imagePath or not os.path.isfile(imagePath):
        print(u'+ ファイルパスが設定されてないかファイルパス先が見つかりません。')
        return
    
    img = QtGui.QImage(imagePath)
    # w,h = img.size().width(),img.size().height()
    return (img.width(),img.height())

def getImagePixelColor(imagePath,w,h,type='RGB'):
    r"""
        指定した画像ピクセルサイズの色を取得する
            imagePath (any):イメージパス
            w (any):横ピクセル数
            h (any):縦ピクセル数
            type (any):RGB or CMYK 指定以外はRGB
    """
    if not imagePath or not os.path.isfile(imagePath):
        print(u'+ ファイルパスが設定されてないかファイルパス先が見つかりません。')
        return False
    
    if not w or not isinstance(w ,int):
        print(u'+ 変数[w]の値が入力されてないかint型以外です。[%s]'%(w))
        return False
    if not h or not isinstance(h ,int):
        print(u'+ 変数[h]の値が入力されてないかint型以外です。[%s]'%(h))
        return False
    
    returnList = []
    
    # 解像度は0pxから始まるので-1して数値を合わせる
    c_w = (w-1) if not w == 0 else w
    c_h = (h-1) if not h == 0 else h
    
    maxSize = getImageSize(imagePath)
    color   = QtGui.QColor(QtGui.QImage(imagePath).pixel(c_w,c_h))

    rgba = (color.red(), color.green(),  color.blue(),  color.alpha())
    cmyk = (color.cyan(),color.magenta(),color.yellow(),color.black())
    
    # 指定範囲外のピクセルを指定した際はその数値を指定して処理を中断する
    if (rgba[0] == 0   and rgba[1] == 48  and
        rgba[2] == 57  and rgba[3] == 255 and
        cmyk[0] == 255 and cmyk[1] == 40  and
        cmyk[2] == 0   and cmyk[3] == 198
    ):
        print(u'+ 指定したピクセル数の上限か'
              u'下限がファイルサイズ外の可能性があります。')
        print(u'\tw=[max:%s,now=%s]'%(maxSize[0],w))
        print(u'\th=[max:%s,now=%s]'%(maxSize[1],h))
        return False
    
    type = type.upper()
    
    if type == 'RGB' or type == 'RGBA':
        returnList = (rgba[0],rgba[1],rgba[2],rgba[3])
    elif type == 'CMYK':
        returnList = (cmyk[0],cmyk[1],cmyk[2],cmyk[3])
    else:
        returnList = (rgba[0],rgba[1],rgba[2],rgba[3])
    
    return returnList
    
###############################################################################
## - pip/python

class PythonPackageCommand(object):
    r"""
        コマンドプロンプトでPython実行するメソッドをまとめたクラス
    """
    def __init__(self,key='',package=''):
        r"""
            初期設定
        """
        self.__basecmd = 'python -m pip'
        self.__package = '<package-name>'
        self.__cmddict = {
            # 一覧の表示
            'list'              : 'list',
            # アップデートが必要なパッケージの表示
            'list -o'           : 'list -o',
            'list --outdated'   : 'list -outdated',
            # 最新状態のパッケージのみ表示
            'list -u'           : 'list -u',
            'list --uptodate'   : 'list -uptodate',
            # パッケージをパッケージ==バージョンで表示
            'freeze'            : 'freeze',
            # pip依存関係の確認
            'chcek'             : 'chcek',
            # パッケージのインストール
            'install'           :  'install {}'.format(self.__package),
            # パッケージのアップデート
            'install -U'        : 'install -U {}'.format(self.__package),
            'install --upgrade' : 'install --upgrade {}'.format(self.__package),
            # pip自体のアップデート
            'install -U pip'        : 'install -U pip',
            'install --upgrade pip' : 'install --upgrade pip',
            # パッケージのアンインストール
            'uninstall'             :  'uninstall {}'.format(self.__package),
            # パッケージのインストール場所を調べる
            'show'                  : 'show {}'.format(self.__package),
        }
        
        self.__executecmd = None
        if key and package == '':
            self.setCmdPythonWord(key)
        elif key and package:
            self.setCmdPythonWord(key,package)
    
    def setCmdPythonWord(self,key,package=''):
        r"""
            指定したキーでcmdPythonワードを取得
        """
        cmd = self.__cmddict.get(key)
        if not cmd:
            return None
        if package and cmd.find(self.__package) != -1:
            cmd = cmd.replace(self.__package,package)
        self.__executecmd = self.jointCmd(cmd)
        
    def getCmdPythonWord(self):
        r"""
            実行コマンドを取得
        """
        return self.__executecmd
    
    def jointCmd(self,cmd):
        r"""
            コマンドプロンプトで使用できる形式にし返す
        """
        return(' '.join([self.__basecmd,cmd]))
    
    def execute(self):
        r"""
            コマンドを実行
            出力結果を返すので<subprocess.check_output>を使用
                subprocess.check_call/True=0
        """
        cmd = self.getCmdPythonWord()
        if not cmd:
            print(u'>>> 実行するcmdコマンドが見つかりませんでした。')
            print(u'\t{}'.format(cmd))
            return None
        try:
            cp = subprocess.check_output(
                cmd,cwd=getPythonInstallPath(),shell=True,
                stderr=subprocess.DEVNULL)
            return cp
        except subprocess.CalledProcessError as e:
            print(e.returncode)
            print(e.cmd)
            print(e.output)
            return None
    
    def getPythonPackageList(self,key=''):
        r"""
            インストールされているパッケージ取得
                key指定がある場合あhそのkeyパッケージのバージョン
                何も指定が無ければ辞書を取得
        """
        dict = {}
        cp = self.execute()
        # cp = subprocess.check_output(
            # 'python -m pip list',cwd=getPythonInstallPath(),shell=True)
        piplist = cp.decode().split('\n')
        for i,p in enumerate(piplist):
            # 1行目(Package-Version)と2行目(---,---)は処理スキップ
            if i<=1:
                continue
            nv = [x for x in p.split(' ') if len(x)]
            if not nv:
                continue
            if nv[-1].find('\r') != -1:
                nv[-1]  = nv[-1].replace('\r','')
            dict[nv[0]] = nv[-1]
        return dict.get(key) if key else dict

###############################################################################
## - Show window

def showWindow(widgetType,wfFlag=True):
    r"""
        ウィンドウの表示
    """
    if not shibokenFlag:
        return
    window = widgetType(MainWindow)
    # 親に取り込ませないようにする一括処理
    # 独自のUIをもたせる場合はフラグをオフにする
    if wfFlag:
        window.setWindowFlags(QtCore.Qt.Window)
    window.show()
    return window
    
###############################################################################
## - End
