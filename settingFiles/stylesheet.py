#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    UIのスタイル設定まとめ
"""
###############################################################################
## base lib

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

from .sslib import basecolor

###############################################################################
## - color management class

class ColorStyleManagement(basecolor.ColorLibrary):
    r"""
        styleSheetのカラーマネジメント総合クラス
    """
    def __init__(self):
        r"""
        """
        self.allColorSetting()
        
    def allColorSetting(self):
        r"""
            カラーの初期設定
        """
        pass
    
    ## ------------------------------------------------------------------------
    ## color method
        
    def getDefaultMainBackgroundColor(self):
        r"""
            GUIベースカラー取得
        """
        return self.mainBackgrondColor()
        
    def getDefaultMainTabColor(self):
        r"""
            タブベースカラー取得
        """
        return self.mainTabColor()
    
    def getDefaultButtonColor(self):
        r"""
            ボタンベースカラー取得
        """
        return self.buttonColor()
    
    def getDefaultInputBoxColor(self):
        r"""
            入力ボックスベースカラー取得
        """
        return self.inputBoxColor()
    
    ## ------------------------------------------------------------------------
    ## color combination
    
    def combinationBackgroundColor(self,color):
        r"""
            background-color形式で書式を返す
        """
        return('background-color:{};'.format(color) if color else '')
    
_CSM_ = ColorStyleManagement()

###############################################################################
## - default background color (互換性維持)

MAINUIBGC_C = _CSM_.getDefaultMainBackgroundColor()
MAINUIBGC   = _CSM_.combinationBackgroundColor(MAINUIBGC_C)
TABBGC_C    = _CSM_.getDefaultMainTabColor()
TABBGC      = _CSM_.combinationBackgroundColor(TABBGC_C)
PBC_C       = _CSM_.getDefaultButtonColor()
PBC         = _CSM_.combinationBackgroundColor(PBC_C)
LEC_C       = _CSM_.getDefaultInputBoxColor()
LEC         = _CSM_.combinationBackgroundColor(LEC_C)

###############################################################################
## - gradation color (互換性維持)

GRD_C            = _CSM_.baseGradientStyleWord()
GRD_C_DEF        = _CSM_.baseDefaultGradationColor()
GRD_C_VERTICAL   = _CSM_.baseVerticalGradationColor2()
GRD_C_VERTICAL_3 = _CSM_.baseVerticalGradationColor3()
GRD_C_HORIZON    = _CSM_.baseHorizonGradationColor2()
GRD_C_SIDE       = GRD_C_HORIZON
GRD_C_HORIZON_3  = _CSM_.baseHorizonGradationColor3()
GRD_C_SIDE_3     = GRD_C_HORIZON_3
GRD_C_DIAGONAL   = _CSM_.baseDiagonalGradationColor2()
GRD_C_DIAGONAL_3 = _CSM_.baseDiagonalGradationColor3()

###############################################################################
## - hover color (互換性維持)

HOVER_H = (
    '%s:hover{background-color:rgb(%s,%s,%s)}'
)
HOVER_P = (
    '%s:pressed{background-color:rgb(%s,%s,%s);border:1px none;}'
)
HOVER_BC = (
    '%s%s'%(HOVER_H,HOVER_P)
)
HOVER_BC_R = (HOVER_BC%('%s','222','44' ,'44' ,'%s','111','11' ,'11' ))
HOVER_BC_G = (HOVER_BC%('%s','44' ,'222','44' ,'%s','11' ,'111','11' ))
HOVER_BC_B = (HOVER_BC%('%s','44' ,'44' ,'222','%s','11' ,'11' ,'111'))
HOVER_BC_LIST = [HOVER_BC_R,HOVER_BC_G,HOVER_BC_B]

###############################################################################
## - font style (互換性維持)

BORDER_STYLE_1 = '''
QPushButton{
    border-style:none;
    background-color:transparent;
}
'''
BORDER_STYLE_2 = '{}{}'.format(BORDER_STYLE_1,'''
QPushButton:pressed{
    padding-left:2px;
    padding-top:2px;
}
''')
# border-left:1px solid black;
# border-top :1px solid black;
LABEL_STYLE = 'QLabel{font-family:GEORGIA;font-size:13px;}'

GROUPFONT = 'font-family:arial black;' # グループタイトルのフォント

###############################################################################
## - margin (互換性維持)

SP  = 2 # スペーシングの間隔
GM  = [2, 2, 2, 2] # カラムのマージン
LM  = [4, 0, 4, 2] # ラベルマージン
LTM = 8 # ラベルの上部のマージン
LBM = 2 # ラベルの下部のマージン

###############################################################################
## END