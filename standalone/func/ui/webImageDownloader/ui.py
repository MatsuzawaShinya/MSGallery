#!/usr/b    in/python
# -*- coding: utf-8 -*-
r"""
    webImageDownloder/ウィジェット設定ファイル
"""
###############################################################################
## base lib

import os
import re
import sys
import time
import json
import random
import datetime
import traceback

## ----------------------------------------------------------------------------
## third party lib

try:
    import requests
    requestsFlag = True
except:
    requestsFlag = False

try:
    import urllib2
    URLLIB = urllib2
    print(u'>>> Import urllib type => <urllib2>\n')
except:
    try:
        import urllib3
        URLLIB = urllib3
        print(u'>>> Import urllib type => <urllib3>\n')
    except:
        pass
        
## ----------------------------------------------------------------------------
## local lib

from msAppTools.settingFiles import systemGeneral as sg
QtWidgets,QtCore,QtGui = sg.QtWidgets,sg.QtCore,sg.QtGui

from . import func as fc
from ... import settings as st

tabledict = fc.TABLEHEADERLIST
column_urlindex  = ([
    k for k in tabledict if tabledict[k].get('type')=='url'])[0]
column_dataindex = ([
    k for k in tabledict if tabledict[k].get('type')=='data'])[0]

###############################################################################
## sub func

def _widgetAddMenu(widget,func):
    r"""
        指定したウィジェットにメニュー項目を追加する
    """
    flag = False
    try:
        widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        widget.customContextMenuRequested.connect(func)
        flag = True
    except:
        pass
    return flag

def _getCountLabelText(all=0,dup=0):
    r"""
        ラベル反映形式にして文字列を返す
    """
    return('{} AllFiles, {} DuplicateFiles.'.format(str(all),str(dup)))

def _getFileLogPath(targetname=''):
    r"""
        .prif.jsonをパスを相対的に参照し指定した同階層の.jsonのパスを取得する
    """
    jsonPath = fc.SPSL.getPath()
    path = os.path.dirname(jsonPath)
    file = os.path.basename(jsonPath).split('.')
    log  = '.'.join([file[0],targetname,file[-1]])
    fullpath = fc.REP(os.path.join(path,log))
    return fullpath if os.path.isfile else ''

def _getJsonData(path):
    r"""
    """
    if not path or not os.path.isfile(path):
        return
    f = open(path,'r')
    d = json.load(f)
    f.close()
    return d
   
###############################################################################
## sub class

class FileLogInfo(object):
    r"""
        URL辞書データを変数に格納しておくクラス
        !! self.preSetting で辞書をセットした後に実行する !!
    """
    def __init__(self):
        r"""
        """
        self.__saveFileLogInfo = None
    
    def setFileLogInfo(self,loginfo=None):
        r"""
            ログ情報をセット
            変数指定していないとfilelogを参照してデータをセットする
            !! __init__では実行しない !!
                
        """
        self.__saveFileLogInfo = (
            self.getJsonFileLogInfo() if loginfo==None else loginfo)
        
    def getFileLogInfo(self):
        r"""
            ログ情報を取得
        """
        return self.__saveFileLogInfo
    
    def getJsonFileLogInfo(self):
        r"""
            実行履歴を取得
        """
        beforePath   = fc.SPSL.getPath()
        fc.SPSL.setPath(_getFileLogPath('filelog'))
        _D = fc.SPSL.getJsonFile()
        dropdatalist = _D.get(fc.DROPFILELOGLIST)
        fc.SPSL.setPath(beforePath)
        return (dropdatalist if dropdatalist else {})
        
    def setJsonFileLogInfo(self,dict):
        r"""
            filelogに書き込み
        """
        beforePath   = fc.SPSL.getPath()
        fc.SPSL.setPath(_getFileLogPath('filelog'))
        _D = fc.SPSL.getJsonFile()
        if not _D.get(fc.DROPFILELOGLIST):
            _D[fc.DROPFILELOGLIST] = {}
        _D[fc.DROPFILELOGLIST] = dict
        fc.SPSL.setDict(_D)
        fc.SPSL.setBackup(True)
        fc.SPSL.setJsonFile()
        fc.SPSL.setPath(beforePath)

FLI = FileLogInfo()

## ----------------------------------------------------------------------------

class SetPathLine(QtWidgets.QLineEdit):
    r"""
        ドロップパスに対応したエクスポートパス用のラインウィジェット
    """
    def __init__(self,parent=None):
        r"""
        """
        super(SetPathLine,self).__init__(parent)
    
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
            self.setText(text)
    
    def keyPressEvent(self,event):
        r"""
            キー押下時のイベント
        """
        super(SetPathLine,self).keyPressEvent(event)
        
        key   = fc.KEYMETHOD._keyType(event)
        mask  = fc.KEYMETHOD._keyMask()
        mask2 = fc.KEYMETHOD._keyMask2()
        
        if key['mod1']==mask2(['ctrl']) and key['press'] in ('O',):
            self.openPathFolder()
    
    ## ------------------------------------------------------------------------
    ## func
    
    def openPathFolder(self):
        r"""
            セットされているパスのフォルダを開く
            ディレクトリが見つからない場合は再帰関数でディレクトリを上がり
            処理を繰り返す
        """
        def _open(path):
            r"""
                ディレクトリを開く再帰関数
            """
            if os.path.isdir(path):
                sg.openExplorer(path)
            else:
                _open(os.path.dirname(path))
        
        _open(str(self.text()))

## ----------------------------------------------------------------------------

class SetUrlPath(QtWidgets.QTreeView):
    r"""
        urlパスを格納する専用のテキストエディットウィジェット
    """
    def __init__(self,parent=None):
        r"""
        """
        super(SetUrlPath,self).__init__(parent)
        
        self.__dropFileList      = []
        self.__dataInfoList      = []
        self.__checkBoxStateList = []
        self.__sleeptime      = 5
        self.__sleeptimeFlag  = False
        self.__goBackDays     = 30
        self.__dropCountLabel = None
        self.__outputDir      = ''
        self.__executeDuplicationBool = False
        self.__executeDuplicationDays = 30
        
        self.setAcceptDrops(True)
        self.setDragEnabled(False)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setDropIndicatorShown(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.doubleClicked.connect(self.openUrlPage)
        
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
        event.accept() if mime.hasUrls() else event.ignore(a)
        
    def dropEvent(self,event):
        r"""
            ドロップ時のイベント
        """
        mine = event.mimeData()
        if mine.hasUrls():
            urls = mine.urls()
            for url in urls:
                file = url.toString()
                if self.checkUrl(file):
                    self.insertDropFile(file)
        else:
            event.ignore()
        self.reAddItem()
    
    def mouseDoubleClickEvent(self,event):
        r"""
            ダブルクリック時のイベント
        """
        super(SetUrlPath,self).mouseDoubleClickEvent(event)
    
    def keyPressEvent(self,event):
        r"""
            キー押下時のイベント
        """
        key   = fc.KEYMETHOD._keyType(event)
        mask  = fc.KEYMETHOD._keyMask()
        mask2 = fc.KEYMETHOD._keyMask2()
        
        if key['press'] in ['V']:
            self.pasteUrlData(self.getClipboardText())
        elif key['mod1']==mask2(['ctrl']) and key['press'] in ['V']:
            self.pasteUrlData(self.getClipboardText())
        elif key['mod1']==mask2(['ctrl']) and key['press'] in ['C']:
            self.getSelectTableItemText(column_urlindex)
        elif key['mod1']==mask2(['ctrl','shift']) and key['press'] in ['C']:
            self.getSelectTableItemText(column_dataindex)
        elif key['mod1']==mask2(['ctrl','shift','alt']) and key['press'] in ['C']:
            self.getSelectTableItemText()
        elif key['press'] in ['Del','Backspace']:
            [self.removeItem(x) for x in self.getSelectItemRow()]
    
    ## ------------------------------------------------------------------------
    ## setting func
    
    def setDropCountLabel(self,label):
        r"""
            ドロップ数を反映するラベルウィジェットを格納
        """
        self.__dropCountLabel = label
        
    def getDropCountLabel(self):
        r"""
            ドロップ数を反映するラベルウィジェットを取得
        """
        return self.__dropCountLabel
    
    ## ------------------------------------------------------------------------
    ## sub func
    
    def getDatetimeDifferenceData(self,src=[],dst=[]):
        r"""
            datetime情報を指定し２つ指定し差の情報を返す
            [0]=year,[1]=month,[2]=day/決め打ち
        """
        if len(src)!=3:
            print('>>> Src list element is not 3.')
            return {}
        if len(dst)!=3:
            print('>>> Dst list element is not 3.')
            return {}
        date1 = datetime.datetime(year=src[0],month=src[1],day=src[2])
        date2 = datetime.datetime(year=dst[0],month=dst[1],day=dst[2])
        date3 = abs(date2-date1)
        returndict = {}
        returndict['all']           = date3
        returndict['days']          = date3.days
        # returndict['seconds']       = date3.seconds
        # returndict['microseconds']  = date3.microseconds
        returndict['total_seconds'] = date3.total_seconds()
        return returndict
    
    ## ------------------------------------------------------------------------
    ## view func
    
    def _tmpprint_(self):
        r"""
            tmpプリント
        """
        print('+++ PRINT +++')
        print(self.__dropFileList)
    
    def clearResultLog(self):
        r"""
            ログリストをクリアする
        """
        self.__resultLogDict.clear()
    
    def setDropFile(self,f):
        r"""
            ファイルをドロップリストへ追加
        """
        self.__dropFileList.append(f)
        self.saveUrlInfo()
    
    def delDropFile(self,f):
        r"""
            指定ファイルをリストから削除
        """
        try:
            self.__dropFileList.remove(f)
        except:
            pass
        finally:
            self.saveUrlInfo()
    
    def getDropFile(self):
        r"""
            ドロップリスト取得
        """
        return self.__dropFileList
        
    def clearDropFile(self):
        r"""
            ドロップファイルの初期化
        """
        self.__dropFileList = []
        self.saveUrlInfo()
    
    def insertDropFile(self,file):
        r"""
            重複ファイルでなければテーブル表示リストへ格納
        """
        if file in self.__dropFileList:
            return
        self.setDropFile(file)
    
    def setDataInfo(self,list):
        r"""
            info情報をセットする
        """
        self.__dataInfoList = list
        
    def getDataInfo(self):
        r"""
            info情報を取得
        """
        return self.__dataInfoList
        
    def clearDataInfo(self):
        r"""
            info情報をクリア
        """
        self.__dataInfoList = []
    
    def setCheckBoxStateInfo(self,statelist=[]):
        r"""
            テーブルリストのチェックボックスのステート状態を保存
        """
        self.__checkBoxStateList = (
            self.getTableCheckBoxState() if not statelist else statelist)
        
    def getCheckBoxStateInfo(self):
        r"""
            テーブルリストのチェックボックスのステート状態を取得
        """
        return self.__checkBoxStateList
    
    def delCheckBoxStateInfo(self,index):
        r"""
            指定インデックスのリストから要素を削除
        """
        try:
            self.__checkBoxStateList.pop(index)
        except:
            pass
    
    def checkUrl(self,url):
        r"""
            url(http)のチェック
        """
        return True if re.search('^http',url) else False
    
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
    
    def removeItem(self,index=0):
        r"""
            アイテムの削除
        """
        model = self.model()
        model.removeRow(index,QtCore.QModelIndex())
        self.delDropFile(self.getDropFile()[index])
        self.delCheckBoxStateInfo(index)
        self.reflectDateInformationList() # updateTable実行前にDATE情報を更新
        self.updateTable()
        
    def removeAllItem(self,clear=False):
        r"""
            全てのアイテムの削除
        """
        model = self.model()
        ([model.removeRow(0,QtCore.QModelIndex())
            for r in range(model.rowCount())])
        if clear:
            self.clearDropFile()
        self.updateTable()
    
    def reAddItem(self,dataInfoClear=False):
        r"""
            編集されたアイテムをビューにセット
        """
        self.removeAllItem()
        self.reflectDateInformationList()
        
        model = self.model()
        row   = model.rowCount()
        FILE  = self.getDropFile()
        INFO  = self.getDataInfo()
        STATE = self.getCheckBoxStateInfo()
        
        for i,file in enumerate(FILE):
            index = i+row
            bufitem = QtGui.QStandardItem('')
            bufitem.setCheckable(True)
            # QtCore.Qt.Unchecked = 0 
            # QtCore.Qt.Checked   = 2
            try:
                bufitem.setCheckState(
                    QtCore.Qt.Checked if STATE[i] else QtCore.Qt.Unchecked)
            except:
                bufitem.setCheckState(QtCore.Qt.Unchecked)
            # "model_"+"type名"で変数を指定
            # type名はfunc.pyに記載されたテーブル辞書のtype
            model_checkbox = bufitem
            model_url      = QtGui.QStandardItem(file)
            model_data     = QtGui.QStandardItem(INFO[i])
            for k in tabledict:
                typename = tabledict[k].get('type')
                if not typename:
                    raise RuntimeError(
                        u'!! 指定されたパラメータが見つかりません !!\b'
                        u'\tTABLEHEADERLIST = "type"')
                targetvalue = ('model_{}'.format(typename))
                try:
                    model.setItem(index,k,eval(targetvalue))
                except:
                    raise RuntimeError(u'!! evalにて変数"{}"を'
                        u'取得出来ませんでした !!'.format(targetvalue))
        
        self.updateTable()
        if dataInfoClear:
            self.clearDataInfo()
        
    def updateTable(self):
        r"""
            テーブルに反映があったら実行するメソッド
        """
        self.refrectDropFilesCount()
    
    def saveUrlInfo(self):
        r"""
            現在セットされているテーブルURLのリスト情報を外部に保存
        """
        _D = fc.SPSL.getJsonFile()
        if not _D.get(fc.TABLEURLINFOLIST):
            _D[fc.TABLEURLINFOLIST] = []
        _D[fc.TABLEURLINFOLIST] = self.getDropFile()
        fc.SPSL.setDict(_D)
        fc.SPSL.setBackup(True)
        fc.SPSL.setJsonFile()
    
    def setSleepTime(self,t):
        r"""
            毎処理スリープタイムフラグのセット
        """
        self.__sleeptime = t
    
    def getSleepTime(self):
        r"""
            毎処理スリープタイムフラグの取得
        """
        return self.__sleeptime
    
    def setSleepTimeFlag(self,f):
        r"""
            毎処理スリープタイムフラグのセット
        """
        self.__sleeptimeFlag = f
        
    def getSleepTimeFlag(self):
        r"""
            毎処理スリープタイムフラグの取得
        """
        return self.__sleeptimeFlag
    
    def setGoBackDays(self,v):
        r"""
            GoBackDaysをセット
        """
        self.__goBackDays = v
        
    def getGoBackDays(self):
        r"""
            GoBackDaysを取得
        """
        return self.__goBackDays
    
    def setExecuteDuplication(self,f,v):
        r"""
            重複履歴を参照して実行するフラグのセット
        """
        self.__executeDuplicationBool = f
        self.__executeDuplicationDays = v
        
    def getExecuteDuplication(self):
        r"""
            重複履歴を参照して実行するフラグ取得
        """
        return(self.__executeDuplicationBool,self.__executeDuplicationDays)
    
    def setOutputDir(self,dir):
        r"""
            アウトプットされるディレクトリを設定
        """
        self.__outputDir = dir
        
    def getOutputDir(self):
        r"""
            アウトプットされるディレクトリを取得
        """
        return self.__outputDir
    
    def getTableCheckBoxState(self):
        r"""
            テーブルリストのチェックボックス状態をリストに保存する
        """
        statelist = [None for x in self.getDropFile()]
        for i,v in enumerate(statelist):
            for k in tabledict:
                if tabledict[k].get('type') == 'checkbox':
                    state = self.model().item(i,k).checkState()
                    statelist[i] = (True if int(state) == 2 else False)
                    break
        return statelist
    
    def reflectDateInformationList(self):
        r"""
            リストが変更されたらURLをチェックし日付情報をDATEに反映する
        """
        droplist = self.getDropFile()
        infolist = ['' for x in droplist]
        for i,item in enumerate(droplist):
            url = self.urlScrutiny(item)
            historyinfo = self.getProcessingHistoryReference(url)
            infolist[i] = ((','.join(historyinfo['hit']))
                if historyinfo.get('hit') else '')
        self.setDataInfo(infolist)
        
    ## ------------------------------------------------------------------------
    ## execute func
    
    def getHeaderItemCount(self):
        r"""
            ヘッダー数を取得
        """
        return self.header().count()
    
    def openUrlPage(self):
        r"""
            ダブルクリックでセットされているページを開く
        """
        ([sg.webbrowser(self.urlScrutiny(x))
            for i,x in enumerate(self.getSelectItemData()) if
                x and i%self.getHeaderItemCount() == column_urlindex])
    
    def getClipboardText(self):
        r"""
            クリップボードのテキストを取得
        """
        return str(QtGui.QClipboard().text())
    
    def pasteUrlData(self,data):
        r"""
            クリップボードに保存されたデータをテーブルへ送る
            クッションメソッドで親のショートカット、ボタンから呼ばれる
        """
        # チェックボックスのステート状態をURL挿入前に保存
        # (self.reAddItem前に実行)
        self.setCheckBoxStateInfo()
        
        list = data.split('\n')
        for d in list:
            if self.checkUrl(d) and not(d in self.getDropFile()):
                self.insertDropFile(d)
            self.reAddItem()
        
    def insertUrlData(self,datalist):
        r"""
            外部保存されたリスト形式で送られてきたURLをテーブルに反映
        """
        [self.insertDropFile(d) for d in datalist if self.checkUrl(d)]
        self.reAddItem()
    
    def refrectDropFilesCount(self):
        r"""
            ドロップされた個数をラベルに反映する
        """
        label = self.getDropCountLabel()
        if not label:
            return
        label.setText(_getCountLabelText(
            str(len(self.getDropFile())),
            str(len([x for x in self.getDataInfo() if x]))
        ))
        
    def getSelectTableItemText(self,index=0):
        r"""
            選択されているテーブルアイテムのテキスト情報をクリップボードに保存
            アイテムはNone以外かつリストアイテムの各1番目、URL列
            (0/"1"/2, 3/"4"/5, 6/"7"/8...)を指定
            index=0(変数指定無し)でURLと日付をスペースで区切り取得
        """  
        _X = (lambda index,space='\n':
            space.join([x for i,x in enumerate(self.getSelectItemData())
            if x and i%self.getHeaderItemCount() == index])
        )
        _K = (lambda text: '{}\n'.format(text))
        
        _sp = ' '
        sg.textCopy(('\n'.join(['{} {}'.format(u,d)
            for u,d in zip(
                _X(column_urlindex ,_sp).split(_sp),
                _X(column_dataindex,_sp).split(_sp)
            )])) if index==0 else _K(_X(index)))
    
    def openOutputDir(self):
        r"""
            セットされているディレクトリを開く
        """
        dir = self.getOutputDir()
        if not dir or not os.path.isdir(dir):
            return
        sg.openExplorer(dir)
    
    def urlScrutiny(self,url):
        r"""
            URL情報をオプションに基づき精査する
            指定したURLは最終的に[dsturl]変数にまとまりリターンする
        """
        dsturl = url
        
        # twitter
        if 'twimg' in dsturl:
            pat = re.compile('^(https.+)([?]format=.+)([&]name=)(\w+)$')
            rr  = pat.search(dsturl)
            # https://pbs.twimg.com/media/EZSeBUwVcAEIrjZ?format=jpg&name=orig
            # 上記形式の場合
            if rr:
                ck = rr.groups()
                if not ck[3]==fc.TWSIZE:
                    dsturl = '{}{}{}{}'.format(ck[0],ck[1],ck[2],fc.TWSIZE)
            # 上記以外の場合
            else:
                pat2 = re.compile('^(https.*)[.]([a-z]+)$')
                rr2  = pat2.search(dsturl)
                # https://pbs.twimg.com/media/EZSeBUwVcAEIrjZ.jpg
                # 上記形式の場合
                if rr2:
                    ck = rr2.groups()
                    dsturl = '{}?format={}&name=orig'.format(ck[0],ck[1])
                    print(u'+ Full conversion of Twitter image format URL.')
                    print(u'\tsrc = {}'.format(url))
                    print(u'\tdst = {}'.format(dsturl))
                # 上記以外の場合
                else:
                    # [=拡張子][=拡張子&]で終わっていた場合の処理
                    dsturl += ('{}name={}'.format(
                        ('' if dsturl.endswith('&') else '&'),fc.TWSIZE))
                    
                    print(u'+ Add orig to URL of Twitter image format.')
                    print(u'\tsrc = {}'.format(url))
                    print(u'\tdst = {}'.format(dsturl))
        # 5ch
        elif 'http://jump.5ch.net/?' in dsturl:
            dsturl = re.sub('^http://jump.5ch.net/\?','',dsturl)
        else:
            pass
        return dsturl
    
    def getProcessingHistoryReference(self,url,difday=9999):
        r"""
            書き出し履歴を参照してboolを返す
            重複したらTrue,それ以外はFalse
        """
        def _checkDifferenceDay():
            r"""
                実行日付と記録されているjsonの日付の差が指定された
                数値外だった場合ヒットした日付を返す。
            """
            resultList   = {'hit':[],'full':[]}
            for sd in savejsondict:
                y0,m0,d0 = sg.getDateTime()['ymd'][2].split('/')
                y1,m1,d1 = sd.split('/')
                dufday = self.getDatetimeDifferenceData(
                    [int(y1),int(m1),int(d1)],[int(y0),int(m0),int(d0)])
                resultList['full'].append(sd)
                if difday == 0:
                    continue
                if dufday['days'] <= difday:
                    resultList['hit'].append(sd)
            return resultList
        
        # 実行履歴を取得
        savejsondict = FLI.getFileLogInfo()
        daylist      = _checkDifferenceDay()
        returnlist   =  {'hit':[],'full':[]}
        for target in ['hit','full']:
            for sd in daylist[target]:
                exehistory = savejsondict.get(sd)
                if not exehistory:
                    continue
                for data in exehistory.values():
                    if data['url'] == url:
                        returnlist[target].append(sd)
                        break
        return returnlist
    
    def execute(self,outputpath):
        r"""
            URLパスのイメージ保存を実行
        """
        def _getTime(timeflag=False):
            r"""
                日時データを返すローカルメソッド
            """
            base = sg.getDateTime()['ymd'][0]
            if timeflag:
                t = str('-'.join(str(time.time()).split('.')))
                base += '_{}'.format(t)
            base += '_{}'.format(sg.returnRandomString(8))
            return base
            
        def _getExtension(url):
            r"""
                URLから拡張子をサーチしてリターンするローカルメソッド
                標準で使用頻度の高いjpg,png,gifを対象
            """
            extlist = ['jpg','png','gif','jpeg']
            match   = ''
            for e in extlist:
                # URL最後の文字を見る
                pattern = re.compile('%s$'%(e))
                r = pattern.search(url)
                if r:
                    match = r.group()
                    break
                # URL全体を見る
                pattern = re.compile(e)
                r = pattern.search(url)
                if r:
                    match = r.group()
                    break
            return (match if match else 'jpg')
            
        def _sleeptimeCalculation(syou=4):
            r"""
                スリープタイムの処理時間を計算
            """
            offsettime = -0.1
            noisetime  = (random.random()+1.01)
            randtime   = ((random.random()+offsettime)*noisetime)
            sleeptime  = (self.getSleepTime()+randtime)
            return round(sleeptime,syou)
            
        def _urlImageExport(url,path,now):
            r"""
                URL保存のローカルメソッド
            """
            result = None
            stb    = 0.0
            sta    = 0.0
            returndict = {
                'date' : '',
                'bool' : False,
                'beforeprocesstime' : 0.0,
                'afterprocesstime'  : 0.0,
            }
            try:
                stb = time.time()
                print(u'>>> Sleep time\n\t{}sec.'.format(sleeptimelist[now]))
                time.sleep(sleeptimelist[now])
                sta = time.time()
                returndict['date'] = sg.getDateTime()['hms'][1]
                
                # requests
                if requestsFlag:
                    responce = requests.get(url,timeout=15)
                    # URLアクセスの確認
                    if responce.status_code != 200:
                        print('>>> Status error : {}'.format(
                            responce.status_code))
                        return returndict
                    # 画像タイプの判別
                    content = responce.headers['content-type']
                    if 'image' not in content:
                        print('>>> No image url : {}'.format(str(content)))
                        print('\tURL = {}'.format(url))
                        print()
                        return
                    images  = responce.content
                    with open(path,'wb') as f:
                        f.write(images)
                # urllib
                else:
                    u = URLLIB.urlopen(url)
                    if not u:
                        u.close()
                        return returndict
                    datatowr = u.read()
                    with open(path,'wb') as f:
                        f.write(datatowr)
                    u.close()
                returndict['bool'] = True
            except Exception as e:
                returndict['bool'] = False
                err = traceback.format_exception(*sys.exc_info())
                if err:
                    if 'HTTPError' in str(err[-1]):
                        print(u'>>> HTTPError: HTTP Error 404: Not Found.')
                else:
                    traceback.print_exc()
                    # print(traceback.format_exc())
            finally:
                ptb = round(time.time()-stb,4)
                pta = round(time.time()-sta,4)
                returndict['beforeprocesstime'] = ptb
                returndict['afterprocesstime']  = pta
                if returndict['bool']:
                    print('+ ({}/{}) Output url image done.'.format(now+1,max))
                    print('\tBase url     = {}'.format(url))
                    print('\tOutput path  = {}'.format(path))
                    print('\tProcess time = {}sec'.format(pta))
                    print('\tTotal processing time = {}sec'.format(ptb))
                    print('')
                return returndict

        ## --------------------------------------------------------------------
        
        print()
        print('+'*100)
        print(u'+ Start process.')
        print()
        
        op    = outputpath
        rml   = []
        URL   = self.getDropFile()
        max   = len(URL)
        
        if not URL:
            return
        
        # スリープ時間をリスト個数分事前に計算
        sleeptimelist = [_sleeptimeCalculation() for x in range(max)]
        
        msg  = ('> File items = {}files\n'.format(max))
        msg += ('> Estimated time = {}sec'.format(round(sum(sleeptimelist),4)))
        STIS = sg.SystemTrayIcon(1)
        STIS.setTitle('Executed.')
        STIS.setMsg(msg)
        STIS.showMsg()
        STIS.exeHide()
        time.sleep(1)
        
        # テーブルのチェック情報を取得 
        checkboxstatelist = self.getTableCheckBoxState()
        # 実行履歴を取得
        savejsondict      = FLI.getFileLogInfo()
        calculationtime   = []
        sendtabledatalist = []
        
        for i,burl in enumerate(URL):
            url      = self.urlScrutiny(burl)
            name     = '{}.{}'.format(_getTime(True),_getExtension(url))
            eop      = fc.REP(os.path.join(op,name))
            ck_state = checkboxstatelist[i]
            
            # 重複処理の条件判定を確認
            sendtabledatalist.append('')
            exeDupData = self.getExecuteDuplication()
            # 個別チェックフラグがオン場合重複処理を回避
            if ck_state:
                print(u'>>> Force state checkbox\n\tTrue.')
            # そうでない場合（全体の重複チェックON、かつ
            # テーブルチェックフラグがオフ）は重複チェック処理を実行
            elif exeDupData[0] and not ck_state:
                historyinfo = self.getProcessingHistoryReference(
                    url,exeDupData[1])
                hitlist  = historyinfo.get('hit')
                fulllist = historyinfo.get('full')
                if hitlist:
                    # tableview/DATAに日付リストを反映
                    dayinfo = (','.join([x for x in hitlist]))
                    sendtabledatalist[i] = dayinfo
                    print('>>> URL with duplicates confirmed '
                          '"{}"days.'.format(exeDupData[1]))
                    print('\tURL : {}'.format(url))
                    print('\tDAY : {}'.format(', '.join(fulllist)))
                    print()
                    continue
                
            # 画像保存処理を実行
            res  = _urlImageExport(url,eop,i)
            if not res['bool']:
                continue
                
            # 書き出し情報を外部jsonに保存
            now_ymd = sg.getDateTime()['ymd'][2]
            if not savejsondict.get(now_ymd):
                savejsondict[now_ymd] = {}
            savejsondict[now_ymd][name] = {
                'url'  : url,
                'date' : res['date'],
            }
            
            rml.append(i)
            calculationtime.append(res['beforeprocesstime'])
            if self.getSleepTimeFlag() and i != (max-1):
                msg  = ('> Files {}/{}\n'.format((i+1),max))
                msg += ('> Sleep time = {}sec\n'.format(sleeptimelist[i]))
                msg += ('> Processing time = {}sec'.format(
                    res['afterprocesstime']))
                msg += ('> Estimated time = {}sec'.format(
                    res['beforeprocesstime']))
                STIM = sg.SystemTrayIcon(1)
                STIM.setTitle('Executed.')
                STIM.setMsg(msg)
                STIM.showMsg()
                STIM.exeHide()
                time.sleep(1)
        
        self.setDataInfo(sendtabledatalist)
        self.reAddItem(True)
        
        # 処理実行終了時に更新された辞書データを変数に再度保存する
        FLI.setJsonFileLogInfo(savejsondict)
        
        # 保存に成功したカテゴリをツリーから削除
        # 頭から回すとindexがズレるので逆順から処理する
        if rml:
            [self.removeItem(x) for x in sorted(rml,reverse=True)]
        
        caumsg  = ('> Processing time = {}sec\n'.format(
            round(sum(calculationtime),4)))
        caumsg += ('> Successes files = {}/{}files'.format(len(rml),max))
        print()
        print('+'*100)
        print(u'+ Process finish...')
        print(caumsg)
        print()
        
        STIE = sg.SystemTrayIcon(9999)
        STIE.setTitle('Finished.')
        STIE.setMsg(caumsg)
        STIE.setActivedMethod(self.openOutputDir)
        STIE.showMsg()
        if self.getSleepTimeFlag():
            time.sleep(10)
        
###############################################################################
## main func

class WebImageDownloader(sg.ScrolledWidget):
    r"""
        <WebImageDownloader>メインレイアウトクラス
    """
    _layout = None
    _uiinfo = {}
    
    def __init__(self,parent=None,masterDict=None):
        r"""
            初期設定
        """
        self.preSetting()
        
        super(WebImageDownloader,self).__init__(parent)
        
        self.debugFlag  = False
        self._parent    = parent
        self._dict      = masterDict
        
        self.uiSetting()
    
    ## ------------------------------------------------------------------------
    ## common parent event setting
    
    def setEventPackage(self,packaging):
        r"""
            子と関連性を保つためのメソッドパッケージを親から引き継いで設定する
        """
        super(WebImageDownloader,self).setEventPackage(packaging)
        
        # 親eventと連動
        if packaging:
            packaging()['set']('closeEvent',self.exeCloseEventFunc)
    
    ## ------------------------------------------------------------------------
    ## Post process
    
    def exePostProcess(self):
        r"""
            PostProcessのオーバーライドメソッド
        """
        super(WebImageDownloader,self).exePostProcess()
        self.headerResized()
    
    ## ------------------------------------------------------------------------
    ## ui
    
    def buildUI(self,parent=None):
        r"""
            ウィジェット構築のオーバーライド用メインメソッド
        """
        __styleLabelWhite    = (
            lambda x:x.setStyleSheet('QLabel{color:#FFF;}'))
        __styleCheckBoxWhite = (
            lambda x:x.setStyleSheet('QCheckBox{color:#FFF;}'))
        
        def __addHorizonLine():
            r"""
                横線の挿入
            """
            self._layout.addWidget(sg.HorizonFrame())
        
        self.preStyleSheet()
        self._layout = QtWidgets.QVBoxLayout(parent)
        self._layout.setContentsMargins(16,16,16,16)
        
        # path line
        vbl = QtWidgets.QVBoxLayout()
        la1 = QtWidgets.QLabel('+ Set output image path.')
        __styleLabelWhite(la1)
        le  = SetPathLine()
        le.textChanged.connect(self.editLineSettings)
        le.relationWidget = ['exportImagePath','exportLine']
        _widgetAddMenu(le,self.openSetPathExplorerMenu)
        self.setUiInfo('exportImagePath','exportLine','widget',le)
        me  = SetPathLine()
        me.setReadOnly(True)
        me.relationWidget = ['exportImagePath','exportMirrorLine']
        _widgetAddMenu(me,self.openSetPathExplorerMenu)
        self.setUiInfo('exportImagePath','exportMirrorLine','widget',me)
        me.hide() # 初期状態は非表示。チェックボックスの状態で変化する
        vbl.addWidget(la1)
        vbl.addWidget(le)
        vbl.addWidget(me)
        self._layout.addLayout(vbl)
        
        __addHorizonLine() ## -------------------------------------------------
        
        # option
        vbl = QtWidgets.QVBoxLayout()
        vbl.setContentsMargins(0,8,0,8)
        la1 = QtWidgets.QLabel('+ Widget option settings.')
        __styleLabelWhite(la1)
        vbl.addWidget(la1)

        hvl = QtWidgets.QHBoxLayout()
        ck1 = QtWidgets.QCheckBox(u'Create day folder')
        ck1.toggled.connect(self.checkBoxStateChange)
        __styleCheckBoxWhite(ck1)
        self.setUiInfo('optionWidget','checkCreateFolder','widget',ck1)
        la2 = QtWidgets.QLabel(u' Date format :')
        __styleLabelWhite(la2)
        le1 = QtWidgets.QLineEdit('yyyymmdd')
        le1.textChanged.connect(self.inputBanLatterReflection)
        le1.setEnabled(False) # チェックボックスと連動して切り替わる
        le1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        le1.customContextMenuRequested.connect(self.templateDateMenu)
        self.setUiInfo('optionWidget','inputDayLine','widget',le1)
        hvl.addWidget(ck1)
        hvl.addWidget(la2)
        hvl.addWidget(le1)
        vbl.addLayout(hvl)
        
        hvl = QtWidgets.QHBoxLayout()
        ck1 = QtWidgets.QCheckBox('Tray display every time')
        ck1.setChecked(False)
        __styleCheckBoxWhite(ck1)
        self.setUiInfo('optionWidget','trayDisplayEveryTime','widget',ck1)
        la1 = QtWidgets.QLabel('Sleep time :')
        __styleLabelWhite(la1)
        sb1 = QtWidgets.QSpinBox()
        sb1.setRange(3,99)
        sb1.setValue(7)
        sb1.setSingleStep(1)
        self.setUiInfo('optionWidget','sleepTimeValue','widget',sb1)
        hvl.addWidget(ck1,5)
        hvl.addStretch()
        hvl.addWidget(la1,2)
        hvl.addWidget(sb1,2)
        vbl.addLayout(hvl)
        
        hvl = QtWidgets.QHBoxLayout()
        ck1 = QtWidgets.QCheckBox('Execute duplication history')
        ck1.setChecked(True)
        ck1.setToolTip(u'以前に実行したURLを確認し'
                       u'重複した場合は処理をスキップする。')
        __styleCheckBoxWhite(ck1)
        self.setUiInfo('optionWidget','executeDuplicationBool','widget',ck1)
        la1 = QtWidgets.QLabel('Go back days :')
        __styleLabelWhite(la1)
        sb1 = QtWidgets.QSpinBox()
        sb1.setRange(0,999)
        sb1.setValue(30)
        sb1.setSingleStep(1)
        sb1.setToolTip(u'重複した日付を入力した日付分まで遡って検索します。')
        self.setUiInfo('optionWidget','executeDuplicationDays','widget',sb1)
        hvl.addWidget(ck1,5)
        hvl.addStretch()
        hvl.addWidget(la1,2)
        hvl.addWidget(sb1,2)
        vbl.addLayout(hvl)
        
        self._layout.addLayout(vbl)
        
        __addHorizonLine() ## -------------------------------------------------
        
        # table list
        vbl = QtWidgets.QVBoxLayout()
        hbl = QtWidgets.QHBoxLayout()
        la1 = QtWidgets.QLabel('+ Set the URL saved in the clipboard,')
        la1.setToolTip(u'ウィジェットにフォーカスが合っている時に'
                       u'Vキー押下でテーブルにペースト')
        la2 = QtWidgets.QLabel(_getCountLabelText())
        __styleLabelWhite(la1)
        __styleLabelWhite(la2)
        self.setUiInfo('dropFileCount','refrectLabel','widget',la2)
        bu  = QtWidgets.QPushButton('set url')
        bu.clicked.connect(self.setPasteClipboradInfo)
        hbl.addWidget(la1,6)
        hbl.addStretch(2)
        hbl.addWidget(la2,1)
        hbl.addWidget(bu,1)
        tv  = SetUrlPath()
        tv.setDropCountLabel(
            self.getUiInfo('dropFileCount','refrectLabel','widget'))
        model = QtGui.QStandardItemModel(0,len(tabledict))
        ([model.setHeaderData(k,QtCore.Qt.Horizontal,v['header'])
            for k,v in sorted(tabledict.items())])
        tv.setModel(model)
        tv.header().setStretchLastSection(True)
        tv.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        tv.customContextMenuRequested.connect(self.tableMenuList)
        self.setUiInfo('urlPathInfo','pathTableView','widget',tv)
        vbl.addLayout(hbl)
        vbl.addWidget(tv)
        self._layout.addLayout(vbl)
        
        # button       
        bu = sg.PushButton('Execute')
        bu.addStyleWord('color:#FFF;')
        bu.addStyleWord(bu.getGradientColor(12,'#888','#222'))
        bu.setStyleSheetWord()
        bu.applyStyleSheet()
        bu.setFixedHeight(28)
        bu.clicked.connect(self.execute)
        self._layout.addWidget(bu)
        self.setUiInfo('executeFunc','executeButton','widget',bu)
        
        self.buildSetting()
    
    def uiSetting(self):
        r"""
            UI全体セッティング
        """
        self.setting()
    
    def checkBoxStateChange(self,state):
        r"""
            dayチェックボックスが切り替わった際に実行されるメソッド
        """
        le1 = self.getUiInfo('optionWidget','inputDayLine','widget')
        le2 = self.getUiInfo('exportImagePath','exportMirrorLine','widget')
        if state:
            le1.setEnabled(True)
            le2.show()
        else:
            le1.setEnabled(False)
            le2.hide()
    
    ## ------------------------------------------------------------------------
    ## event
        
    def keyPressEvent(self,event):
        r"""
            キープレスイベント(オーバーライド)
        """
        # 親keyPressEvent(Esc,windowClose等)をオーバーライドしてしてしまうので
        # superしてイベント情報を継承する
        super(WebImageDownloader,self).keyPressEvent(event)
        
        key   = self.getKeyType(event)
        mask  = self.getKeyMask()
        mask2 = self.getKeyMask2()
        
        if key['press'] in ['V']:
            self.setPasteClipboradInfo()
        elif key['mod1']==mask2(['ctrl']) and key['press'] in ['V']:
            self.setPasteClipboradInfo()
    
    def mouseDoubleClickEvent(self,event):
        r"""
            ダブルクリック時のイベント
        """
        # super(WebImageDownloader,self).mouseDoubleClickEvent(event)
        self.setPasteClipboradInfo()
    
    def resizeEvent(self,event):
        r"""
            リサイズされた際のイベント
        """
        super(WebImageDownloader,self).resizeEvent(event)
        self.headerResized()
    
    ## ------------------------------------------------------------------------
    ## setting
    
    def buildSetting(self):
        r"""
            build時に設定されるセッティングメソッド
        """
        D = fc.SPSL.getJsonFile()
        
        # 書き出しパスの情報を取得しセット
        sd = D.get(fc.OUTPUTLINEPATH)
        if sd:
            sd   = sd.get('0')
            path = (sd if sd else '')
            self.getUiInfo(
                'exportImagePath','exportLine','widget').setText(path)
        self.inputBanLatterReflection()
        
        # sleeptimeをセット
        st = D.get(fc.SLEEPTIMEINFO)
        if st:
            st = st.get('TIME')
            st = (int(st) if st else 7)
            self.getUiInfo(
                'optionWidget','sleepTimeValue','widget').setValue(st)
        
        # GoBackDaysを反映
        gb = D.get(fc.GOBACKDAYS)
        if gb:
            gb = gb.get('VALUE')
            gb = (int(gb) if gb else fc.GOBACKDAYSDEFVAL)
            self.getUiInfo(
                'optionWidget','executeDuplicationDays','widget').setValue(gb)
        
        # ymd情報を反映
        ymd = D.get(fc.INPUTDAYLINE)
        if ymd and ymd.get('0'):
            w = self.getUiInfo('optionWidget','inputDayLine','widget')
            w.setText(ymd.get('0'))
        
        # ドロップされたURLのリストを取得しセット
        td = D.get(fc.TABLEURLINFOLIST)
        if td:
            w = self.getUiInfo('urlPathInfo','pathTableView','widget')
            w.insertUrlData(td)
        
        # ドロップされたファイルの個数をラベルに反映
        self.refrectDropFileCount()
        
        # checkbox状態の設定
        self.getUiInfo(
            'optionWidget','checkCreateFolder','widget').setChecked(True)
        
    def preSetting(self):
        r"""
            __init__設定を先行して行う
        """
        # AppData/Roaming/msAppTools/<FILENAME>までのパスを設定
        fc.SPSL.setSeriesPath(fc.SPSL.getSavePath(fc.getModuleName()))
        
        # 起動時にURL情報の辞書データを変数に保存
        FLI.setFileLogInfo()
    
    def preStyleSheet(self):
        r"""
            スタイルシート設定
        """
        pass
    
    def setting(self):
        r"""
            初期設定の窓口関数
        """
        pass
    
    def setUiInfo(self,key1,key2,key3,value):
        r"""
            uiInfoにkeyを指定し保存する
        """
        try:
            if not self._uiinfo.get(key1):
                self._uiinfo[key1] = {}
            self._uiinfo[key1].update({key2:{key3:value}})
            return True
        except:
            return False
    
    def getUiInfo(self,key1='',key2='',key3=''):
        r"""
            keyを指定しuiInfoから情報を取得する
            何もヒットしなかった場合はNoneを返す
        """
        try:
            if key1=='' and key2=='':
                return self._uiinfo
            else:
                if key3=='':
                    return self._uiinfo[key1][key2]
                else:
                    return self._uiinfo[key1][key2][key3]
        except:
            return None
    
    def refrectDropFileCount(self):
        r"""
            ドロップされたファイルの個数を指定ラベルに反映
        """
        table = self.getUiInfo('urlPathInfo','pathTableView','widget')
        table.refrectDropFilesCount()
    
    def headerResized(self):
        r"""
            リサイズイベントが反応したらヘッダーの大きさを変えるメソッド
        """
        tv = self.getUiInfo('urlPathInfo','pathTableView','widget')
        w  = self._parent.rect().width()
        tv.setColumnWidth(0,42)
        tv.setColumnWidth(1,int((w*0.9)*0.725))
    
    ## ------------------------------------------------------------------------
    ## menu
    
    def templateDateMenu(self):
        r"""
            日付のテンプレート設定メニュー
        """
        menu = QtWidgets.QMenu()
        for i,d in enumerate(fc.YMDLIST):
            m = menu.addAction(d,self.resetTemplateDate)
            m.dateformat = d
        menu.exec_(QtGui.QCursor.pos())
    
    def updateDate(self,updatedate):
        r"""
            処理実行前に日付を更新
            同一のデータフォーマットが設定された場合かつ日付を跨いだとき
            日付の更新がされないので一度テキストを変更し再度指定する
        """
        w = self.getUiInfo('optionWidget','inputDayLine','widget')
        w.setText('ymdymdymdymdymdymdymdymd')
        w.setText(updatedate)
    
    def resetTemplateDate(self):
        r"""
            メニューで選択された日付フォーマットをテキスト設定
        """
        s = self.sender()
        self.updateDate(s.dateformat)
        
    def openSetPathExplorerMenu(self):
        r"""
            セットされているパスからエクスプローラーを開くメニューコマンド
        """
        s = self.sender()
        menu = QtWidgets.QMenu()
        mw = menu.addAction(
            'Open path to explorer',self.openSetPathExplorerMethod)
        mw.relationWidget = s.relationWidget
        menu.exec_(QtGui.QCursor.pos())
    
    def openSetPathExplorerMethod(self):
        r"""
            セットされているパスからエクスプローラーを開くメソッド
        """
        s = self.sender()
        p = self.getUiInfo(s.relationWidget[0],s.relationWidget[1],'widget')
        p.openPathFolder()
        
    def tableMenuList(self):
        r"""
            QTableViewのメニューリスト
        """
        menu = QtWidgets.QMenu()
        menu.addAction(
            'Paste clipborad text info',self.setPasteClipboradInfo)
        menu.addAction(
            'All item removed',self.tableMenuAllRemove)
        menu.exec_(QtGui.QCursor.pos())
        
    def tableMenuAllRemove(self):
        r"""
            テーブルアイテムを全て削除
        """
        tv = self.getUiInfo('urlPathInfo','pathTableView','widget')
        tv.removeAllItem(True)
    
    ## ------------------------------------------------------------------------
    ## func
    
    def exeCloseEventFunc(self):
        r"""
            close時に実行するメソッドのクッション関数（親のcloseEventで実行）
        """
        _D = fc.SPSL.getJsonFile()
        
        # パスラインの入力情報
        bufDict = {}
        w = self.getUiInfo('exportImagePath','exportLine','widget')
        bufDict['0'] = w.text()
        _D[fc.OUTPUTLINEPATH] = bufDict
        
        # sleepタイム情報
        bufDict = {}
        s = self.getUiInfo('optionWidget','sleepTimeValue','widget')
        bufDict['TIME'] = str(s.value())
        _D[fc.SLEEPTIMEINFO] = bufDict
        
        # GoBackDays
        bufDict = {}
        g = self.getUiInfo('optionWidget','executeDuplicationDays','widget')
        bufDict['VALUE'] = str(g.value())
        _D[fc.GOBACKDAYS] = bufDict
        
        fc.SPSL.setDict(_D)
        fc.SPSL.setBackup(True)
        fc.SPSL.setJsonFile()
    
    def toggledMirrorLine(self):
        r"""
            書き出し先のミラーラインを表示させるトグルメソッド
        """
        me = self.getUiInfo(
            'exportImageMirrorPath','exportMirrorLine','widget')
        me.show() if me.isHidden() else me.hide()
    
    def editLineSettings(self):
        r"""
            ラインエディット入力時に実行されるメソッドのまとめ
        """
        self.checkPathColor()
        self.mirrorLineRefrect()
        self.inputBanLatterReflection()
    
    def mirrorLineRefrect(self):
        r"""
            dayチェックの情報をプラスしてミラーラインへテキスト情報を送る
        """
        src = self.getUiInfo('exportImagePath','exportLine','widget')
        dst = self.getUiInfo('exportImagePath','exportMirrorLine','widget')
        dst.setText(src.text())
        
    def checkPathColor(self):
        r"""
            入力されているパスをチェックしフォルダが存在すれば黒
            そうでなければ赤色のセットをする
        """
        w = self.getUiInfo('exportImagePath','exportLine','widget')
        s = '#000' if os.path.isdir(fc.REP(w.text())) else '#D22'
        w.setStyleSheet('QLineEdit{color:%s;}'%s)
    
    def inputBanLatterReflection(self):
        r"""
            入力されている文字の受け付けを「y,m,d」以外禁止
        """
        def _changeDayLength(ni,YMD,inverse=True):
            r"""
                文字列とYMDそれぞれの長さに適用したインデックスの情報を返す
            """
            am = (ni % len(YMD))
            return ((len(YMD) if am==0 else am) * (-1 if inverse else 1))
        
        w = self.getUiInfo('optionWidget'   ,'inputDayLine'    ,'widget')
        e = self.getUiInfo('exportImagePath','exportLine'      ,'widget')
        m = self.getUiInfo('exportImagePath','exportMirrorLine','widget')
        
        if not w.text():
            m.setText(e.text())
            return
        
        # 入力文字のチェック
        # 指定文字以外が入力されていた場合末尾一文字を削除し処理を抜け
        # setTextによりtextChecngedが反映され再度このメソッドが実行される。
        pat = re.compile('([^ymd_\-]{1,})')
        rr  = pat.search(w.text())
        if rr:
            w.setText(w.text()[:-1])
            return
        new = str(w.text())
        
        # 書き出し先フォルダのネーミングカスタマイズ
        Y,M,D = sg.getDateTime()['ymd'][2].split('/')
        ni,mw = 1,''
        for i,x in enumerate(reversed(new)):
            # index最後の処理はエラーになるのでスキップ
            now  = new[-(i+1)]
            next = (-1 if len(new)==i+1 else new[-(i+2)])
            mw += (eval('{0}[_changeDayLength(ni,{0},True)]'.format(x.upper()))
                if x in ['y','m','d'] else x)
            # 次の検索文字が連続していない場合は初期化
            ni = (ni+1 if now==next else 1)
        
        m.setText(fc.REP(os.path.join(e.text(),mw[::-1])))
        self.saveInputDayLineInfo()
        
    def saveInputDayLineInfo(self):
        r"""
            ymd情報を外部へ保存
        """
        bufDict = {}
        _D = fc.SPSL.getJsonFile()

        w = self.getUiInfo('optionWidget','inputDayLine','widget')
        t = (w.text())
        bufDict['0'] = t
        
        _D[fc.INPUTDAYLINE] = bufDict
        fc.SPSL.setDict(_D)
        fc.SPSL.setBackup(True)
        fc.SPSL.setJsonFile()
    
    def setPasteClipboradInfo(self):
        r"""
            クリップボードに保存されたURLテキスト情報をテーブルに挿入
            テーブルへの挿入はQTableViewが持っているメソッドで実行する
        """
        tv = self.getUiInfo('urlPathInfo','pathTableView','widget')
        if sg.clipboradDataCheck()!=1:
            return
        tv.pasteUrlData(tv.getClipboardText())
    
    def execute(self):
        r"""
            セットされているパスを参照しイメージ保存を実行
        """
        ck  = self.getUiInfo('optionWidget','checkCreateFolder','widget')
        cke = self.getUiInfo('optionWidget','trayDisplayEveryTime','widget')
        ckd = self.getUiInfo('optionWidget','executeDuplicationBool','widget')
        te  = self.getUiInfo('exportImagePath',
            ('exportMirrorLine' if ck.isChecked() else 'exportLine'),'widget')
        spt = self.getUiInfo('optionWidget','sleepTimeValue','widget')
        spd = self.getUiInfo('optionWidget','executeDuplicationDays','widget')
        idl = self.getUiInfo('optionWidget','inputDayLine','widget')
        tv  = self.getUiInfo('urlPathInfo','pathTableView','widget')
        tv.setSleepTime(spt.value())
        tv.setGoBackDays(spd.value())
        tv.setSleepTimeFlag(cke.isChecked())
        tv.setExecuteDuplication(ckd.isChecked(),spd.value())
        
        # date更新
        self.updateDate(str(idl.text()))
        
        # 保存先のディレクトリを確認
        t  = str(te.text())
        if not t:
            print(u'+ Nothing entered.')
            return
        tv.setOutputDir(t)
        if not os.path.isdir(t):
            if ck.isChecked():
                os.makedirs(t)
                print(u'> Mirror line execute,')
                print(u'  create folder = "{}"'.format(t))
                print
            else:
                print(u'+ Export path not found.')
                return
        
        # セットURLイメージを保存（QTableViewメソッド）
        # 処理中はGUIが邪魔になるので最小化して避難させておく
        # 処理が終わったら元に戻す。
        # ドロップファイルを確認した場合のみ実行する
        if tv.getDropFile():
            self._parent.showMinimized()
            tv.execute(t)
            self._parent.showNormal()
    
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
## END
