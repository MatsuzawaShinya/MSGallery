#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    batから指定された名前に沿ってGUIを起動するスクリプト
"""
###############################################################################
## base lib

import os
import sys
import traceback
sys.dont_write_bytecode = True

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

###############################################################################

path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0,path) if not path in sys.path else None

_LINE = (lambda w,length=100:(w*length))

###############################################################################
    
def _main():
    r'''
        @brief  main
        @return (any):None
    '''
    try:
        from func import mainGui
    except Exception as e:
        print('{0}{1}{0}{1}{0}'.format('\n',_LINE('*')))
        traceback.print_exc()
        print('{0}{1}{0}{1}{0}'.format('\n',_LINE('*')))
        raise e
    mainGui.main(([p for p in sys.argv])[1:])

###############################################################################

if __name__ == '__main__':
    _main()
    
###############################################################################
## END
