#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
"""
###############################################################################
## base lib

import os

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from . import info as sginfo
MSINFO = sginfo.MsAppToolsBaseInfo()

###############################################################################

###############################################################################
## path method

class PathClass(object):
    r"""
        パス関係の処理を集約したクラス
    """
    def __init__(self):
        r"""
        """
        pass

    def slashConversion(self,path,type=True):
        r"""
            スラッシュバックスラッシュの変換
                :True  : \ -> /
                :False : / -> \
        """
        L = ('\\','/')
        src,dst = (L[0],L[1]) if type else (L[1],L[0])
        return path.replace(src,dst)
        
    def toBasePath(self,path):
        r"""
            "\" -> "/" への変換
        """
        return self.slashConversion(path,True)

    def toReversePath(self,path):
        r"""
            "/" -> "\" への変換
        """
        return self.slashConversion(path,False)
    
    def getPathList(self,company=None,**keywords):
        r"""
            パスの取得
        """
        if not company:
            return
        
        path     = None
        company  = company.upper()
        pathType = None
        for key in keywords:
            k = key.upper()
            if k == 'PATHTYPE':
                pathType = keywords[key]
        pathType = pathType.upper()
        
        if company == MSINFO.NOW_COMPANY:
            try:
                from gnCommon import common_path
                if pathType == 'HOMEPATH':
                    path = os.path.dirname(
                        os.path.dirname(
                            common_path.getDataProjectPath(public=False)
                        )
                    )
            except:
                path = None
        
        return path
    
    def getExtension(self,name):
        r"""
            拡張子を返す
        """
        return os.path.splitext(name)[-1][1:]
        
    def getRoamingPath(self):
        r"""
            Roamingパスのリターン（環境変数で参照）
        """
        doc = os.environ.get('USERPROFILE')
        if not doc:
            return None
        roaming = self.toBasePath(
            os.path.join(os.environ.get('USERPROFILE'),'AppData','Roaming'))
        return roaming if os.path.isdir(roaming) else None
    
    def getEstimationData(self):
        r"""
            キー予測情報のjsonファイルを取得する
        """
        pass
        
    def getEstimationMasterData(self):
        r"""
            キー予測情報のjsonマスターファイルを取得する
        """
        pass
        
    def getEstimationIndividualData(self):
        r"""
            キー予測情報のファイルごとのjsonファイルを取得する
        """
        pass
    
###############################################################################
## END
