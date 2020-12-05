#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    指定された名前のGUIを起動する
"""
###############################################################################
## base lib

import os
import sys
import time
import traceback

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from . import ui
from msAppTools.settingFiles import systemGeneral as sg

QtWidgets,QtCore,QtGui = sg.QtWidgets,sg.QtCore,sg.QtGui

###############################################################################
        
def main(param):
    r"""
        gui起動窓口関数
        
        Args:
            param (any):batから送られてきたgui起動タイプのリスト
            
        Returns:
            any:None
    """
    app = QtWidgets.QApplication(sys.argv)
    for p in param:
        MW = ui.func.MainWindow(p)
        MW.show()
        if MW.startupFlag:
            print(u'起動できないGUI:{}'.format(p))
            QtCore.QTimer.singleShot(1,MW.close)
    sys.exit(app.exec_()) # app.exec_()
    
###############################################################################
## END
