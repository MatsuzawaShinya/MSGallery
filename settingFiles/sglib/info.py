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

###############################################################################
## base setting

class MsAppToolsBaseInfo(object):
    r"""
    """
    def __init__(self):
        r"""
        """
        pass
    
    def getMsAppToolsName(self,designation=True):
        r"""
            ツール名の取得
                designation = True  / 固定名で取得
                designation = False / パス位置から相対的に取得
        """
        _bn_ = os.path.basename
        _dn_ = os.path.dirname
        return ('msAppTools'
            if designation else _bn_(_dn_(_dn_(_dn_(__file__)))))
    
    def getNowCompany(self):
        r"""
        """
        return 'GOONEYS'

###############################################################################
## END