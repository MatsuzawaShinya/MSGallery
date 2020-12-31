#!/usr/b    in/python
# -*- coding: utf-8 -*-
r"""
    TemplateClassNames/Explanation,func
"""
###############################################################################
## base lib

import os
import re
import sys

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from ... import settings as st
from msAppTools.settingFiles import systemGeneral as sg

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
        'release' : '9999/99/99',
        'update'  : '9999/99/99',
    }

###############################################################################
## base settings
    
###############################################################################
## sub func

###############################################################################
## main func
    
###############################################################################
## END
