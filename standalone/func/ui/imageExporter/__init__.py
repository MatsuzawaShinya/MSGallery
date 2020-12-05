#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
## base lib

import os

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from .  import ui
from .  import func
from .. import lib as parentlib
WSI = parentlib.WidgetSettingInfo()

###############################################################################

def openWindow(parent=None):
    r"""
        親(__init__,MainWindow)から実行されてきた情報を元に
        フォルダ内に存在するui.pyのGUIを起動する
    """
    name = func.getModuleName()
    dict = WSI.getSettingInfo()
    widget = eval('ui.{}(parent,dict)'.format(dict[name]['name']))
    return widget

###############################################################################
## END
