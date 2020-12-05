#!/usr/b    in/python
# -*- coding: utf-8 -*-
r"""
    createWorkHierarchy/Explanation,func
"""
###############################################################################
## base lib

import os
import re
import sys
import json
import shutil
import traceback

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from ... import settings as st
from msAppTools.settingFiles import systemGeneral as sg

###############################################################################
## base settings

REP      = sg.slashConversion
TEMPNAME = 'TemplateClassNames'
TEMPDATE = '9999/99/99'

PREFDATA = {
    'TAB' : 'TABINFO'
}

READWRITE  = ['read','write']
WINDOWFLAG = ['default','tophint=True','tophint=False']

###############################################################################
## common func

def getModuleName():
    r"""
        パスからモジュールネームを相対的に取得
    """
    return (os.path.basename(os.path.dirname(__file__)))
    
def getAboutInfo():
    r"""
        aboutベースデータ取得
    """
    return {
        'title'   : getModuleName(),
        'version' : '1.0.1',
        'author'  : st._author,
        'release' : '2020/07/27',
        'update'  : '2020/07/27',
    }
    
###############################################################################
## sub func

class SubMethod(object):
    r"""
        処理をサポートするメソッドを集約したクラス
    """
    def __init__(self):
        r"""
        """
        self._basename = 'DEFAULTBASENAME'
    
    ## ------------------------------------------------------------------------
    ## method
    
    def pathJoin(self,pathlist=[]):
        r"""
            指定されたリスト配列の文字をjoinする
        """
        return ('/'.join(pathlist))
    
    ## ------------------------------------------------------------------------
    ## setting
    
    def setBasename(self,name):
        r"""
            新しく作成するトップネームを指定
        """
        self._basename = name
        
    def getBasename(self):
        r"""
            新しく作成するトップネームを取得
        """
        return self._basename
    
    ## ------------------------------------------------------------------------
    ## dir
    
    def createDir(self,path,log=False):
        r"""
            指定したパスまでのディレクトリを作成する
        """
        result = True
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
                if log:
                    print('>>> Create dir.')
                    print('\t{}'.format(path))
            else:
                if log:
                    print('>>> Already has a folder.')
                    print('\t{}'.format(path))
        except:
            result = False
            if log:
                traceback.print_exc()
        return result
    
    ## ------------------------------------------------------------------------
    ## copy
    
    def copy(self,src,dst,log=True):
        r"""
            コピーを実行/メタデータ無し
        """
        shutil.copy(src,dst)
        if log:
            print(u'>>> ファイルコピーを行いました。')
            print(u'\tメタデータ -> False')
            print('\tsrc -> {}'.format(src))
            print('\tdst -> {}'.format(dst))
        
    def copy2(self,src,dst,log=True):
        r"""
            コピーを実行/メタデータ有り
        """
        shutil.copy2(src,dst)
        if log:
            print(u'>>> ファイルコピーを行いました。')
            print(u'\tメタデータ -> True')
            print('\tsrc -> {}'.format(src))
            print('\tdst -> {}'.format(dst))
    
    def copydir(self,src,dst,force=False,log=True):
        r"""
            ディレクトリコピー
            すでにあるディレクトリにコピーする場合,force=Trueを指定
        """
        if not os.path.isdir(dst):
            shutil.copytree(src,dst)
            if log:
                print(u'>>> ディレクトリコピーを行いました。')
                print('\tsrc -> {}'.format(src))
                print('\tdst -> {}'.format(dst))
        else:
            if force:
                from distutils.dir_util import copy_tree
                copy_tree(src,dst)
                if log:
                    print(u'>>> ディレクトリコピーを強制的に行いました。')
                    print('\tsrc -> {}'.format(src))
                    print('\tdst -> {}'.format(dst))
            else:
                if log:
                    print(u'>>> コピー先にディレクトリが'
                          u'存在するため処理を中断しました。')
    
    ## ------------------------------------------------------------------------
    ## remove
    
    def remove(self,path):
        r"""
            指定ファイルの削除
        """
        try:
            os.remove(path)
            print(u'>>> ファイルを削除。')
            print(u'\t{}'.format(path))
            return True
        except:
            print(u'!!! ファイルの削除に失敗しました。')
            print(u'\t{}'.format(path))
            return False
            
    ## ------------------------------------------------------------------------
    ## name
    
    def capitalizeFirstLetter(self,word):
        r"""
            指定したワードの先頭文字を大文字にして返す
        """
        return (''.join([word[0].upper(),word[1:]])) if word else ''
    
    ## ------------------------------------------------------------------------
    ## json
    
    def getJsonFile(self,path):
        r"""
            jsonデータの情報をリターン
        """
        if not path:
            return None
        try:
            with open(path,'r') as f:
                d = json.load(f)
            return d
        except:
            return None
    
    def getWindowPrefInfo(self):
        r"""
            windowPrefパスを参照しデータを取得
        """
        return self.getJsonFile(self.getWidgetJsonPath())
    
    def dumpJsonFile(self,dstpath,jsoninfo):
        r"""
            json情報を書き込む
        """
        def _exe(p):
            r"""
                json/dump
            """
            updir = os.path.dirname(p)
            if not os.path.isdir(updir):
                print(u'!! 実行ディレクトリが確認出来なかったので'
                      u'処理を中断しました。')
                print(u'\t Path : {}'.format(updir))
                return
            with open(p,'w') as f:
                json.dump(jsoninfo,f,
                    indent=4,sort_keys=True,ensure_ascii=False)
        
        # main
        _exe(dstpath)
        
        # backup
        fpath  = os.path.dirname(dstpath)
        bname  = '.'.join([str(os.path.basename(dstpath)),'BU'])
        bupath = '/'.join([fpath,bname])
        _exe(bupath)
        
    ## ------------------------------------------------------------------------
    ## path
    
    def getFuncUiPath(self):
        r"""
            standalone/func/uiまでのパスを相対的に返す
        """
        _dn_ = os.path.dirname
        return REP(_dn_(_dn_(__file__)))
    
    def getBatPath(self):
        r"""
            bat実行ファイルまでのパスを取得
        """
        stPath      = self.dirupRecursiveFunction(REP(__file__),'standalone')
        batpathlist = ([self.pathJoin([stPath,'bat',x,
            '{}.bat'.format(self.getBasename())]) for x in ['27','37']])
        return batpathlist
        
    def getWidgetJsonPath(self):
        r"""
            widgetinfo.jsonまでのパスを相対的に取得する
        """
        return REP(os.path.join(self.getFuncUiPath(),'widgetinfo.json'))

    def dirupRecursiveFunction(self,path,endDirName=''):
        r"""
            指定したフォルダ名までdirnameを達したらそのパスを返す
        """
        limit = 99
        def _open(tpath,act=0):
            r"""
                ディレクトリを開く再帰関数
            """
            active = act+1
            if active>limit:
                return tpath
            updir = os.path.dirname(tpath)
            bname = os.path.basename(updir)
            if os.path.isdir(updir) and bname==endDirName:
                return updir
            return _open(updir,active)
        return _open(path)
        
    def getLibTempPath(self):
        r"""
            standalone/lib/temoplateまでのパスを相対的に設定し辞書で返す
        """
        JO = os.path.join
        filePathChecker = (lambda p:REP(p) if os.path.exists(p) else '')
        
        stPath     = self.dirupRecursiveFunction(REP(__file__),'standalone')
        tempPath   = JO(stPath,'lib','template')
        dirPath    = JO(tempPath,'__widgetfolder-template__')
        
        returnDict = {
            'dir' : {
                'path' : {
                    'base' : filePathChecker(dirPath),
                    'init' : filePathChecker(JO(dirPath,'__init__.py')),
                    'func' : filePathChecker(JO(dirPath,'func.py')),
                    'ui'   : filePathChecker(JO(dirPath,'ui.py')),
                },
            },
            'bat' : {
                'path' : {
                    'bat' : filePathChecker(
                        JO(tempPath,'__bat-template__.bat')),
                },
            },
        }
        
        return returnDict  

###############################################################################
## main func
    
###############################################################################
## END

