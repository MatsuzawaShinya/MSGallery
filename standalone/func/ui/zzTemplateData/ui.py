#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    指定したフォルダ内にあるすべてのファイルをzip化するGUI
"""
###############################################################################
## base lib

import os
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
    
###############################################################################

class ZzTemplateData(sg.ScrolledWidget):
    r"""
        zip作成gui
    """
    def __init__(self,parent=None,masterDict=None):
        r"""
            初期設定
        """
        super(ZzTemplateData,self).__init__(parent)
        self._dict = masterDict
    
    ## ------------------------------------------------------------------------
    ## common parent event setting
    
    ## ------------------------------------------------------------------------
    ## build
    
    def buildUI(self,parent=None):
        r"""
            enter description
        """
        self.layout = QtWidgets.QVBoxLayout(parent)
    
    ## ------------------------------------------------------------------------
    ## event
    
    ## ------------------------------------------------------------------------
    ## setting
    
    def getAboutData(self):
        r"""
            about情報の取得
        """
        return fc.getAboutInfo()
    
    ## ------------------------------------------------------------------------
    ## func


###############################################################################
## END
