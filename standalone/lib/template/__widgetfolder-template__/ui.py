#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    TemplateClassNames/Explanation,ui
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

from msAppTools.settingFiles import systemGeneral as sg
QtWidgets,QtCore,QtGui = sg.QtWidgets,sg.QtCore,sg.QtGui

from . import func as fc
from ... import settings as st
    
###############################################################################

class TemplateClassNames(sg.ScrolledWidget):
    r"""
    """
    def __init__(self,parent=None,masterDict=None):
        r"""
            初期設定
        """
        self._dict = masterDict
        super(TemplateClassNames,self).__init__(parent)
    
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
