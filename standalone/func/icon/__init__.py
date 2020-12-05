#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    アイコンに関するメソッドまとめ
    iconの設定をclass内(Widget)
"""
###############################################################################
## base lib

import os
import re
import sys
import traceback

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from msAppTools.settingFiles import pyside2
QtWidgets,QtCore,QtGui = pyside2.QtWidgets,pyside2.QtCore,pyside2.QtGui

###############################################################################
## path

rootPath = os.path.dirname(__file__)
    
###############################################################################
## default icon

def iconPath(icon=None,ext='png',type='icon',size=[10,10]):
    r'''
        @brief  アイコンを設定する関数
        @param  icon(any) : アイコン名
        @param  ext(any)  : enter description
        @param  type(any) : アイコンタイプ
        @param  size(any) : サイズ(縦*横)
        @return (any):
    '''
    ic = (os.path.join(rootPath,('{}.{}'.format(icon,ext))))
    if not os.path.isfile(ic):
        ic = (os.path.join(rootPath,('default.{}'.format(ext))))
    if type == 'pixmap':
        icon = QtGui.QPixmap(ic)
        icon = icon.scaled(
            size[0],size[1],
            transformMode=QtCore.Qt.SmoothTransformation
        )
    else:
        icon = QtGui.QIcon(ic)
    return icon

###############################################################################
## END
