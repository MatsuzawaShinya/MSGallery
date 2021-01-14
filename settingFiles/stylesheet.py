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
        self.MAINUIBGC_C = self.getDefaultMainBackgroundColor()
        self.MAINUIBGC   = self.combinationBackgroundColor(self.MAINUIBGC_C)
        self.TABBGC_C    = self.getDefaultMainTabColor()
        self.TABBGC      = self.combinationBackgroundColor(self.TABBGC_C)
        self.PBC_C       = self.getDefaultButtonColor()
        self.PBC         = self.combinationBackgroundColor(self.PBC_C)
        self.LEC_C       = self.getDefaultInputBoxColor()
        self.LEC         = self.combinationBackgroundColor(self.LEC_C)
        
        self.GRD_C            = self.baseGradientStyleWord()
        self.GRD_C_DEF        = self.baseDefaultGradationColor()
        self.GRD_C_VERTICAL   = self.baseVerticalGradationColor2()
        self.GRD_C_VERTICAL_3 = self.baseVerticalGradationColor3()
        self.GRD_C_HORIZON    = self.baseHorizonGradationColor2()
        self.GRD_C_SIDE       = self.GRD_C_HORIZON
        self.GRD_C_HORIZON_3  = self.baseHorizonGradationColor3()
        self.GRD_C_SIDE_3     = self.GRD_C_HORIZON_3
        self.GRD_C_DIAGONAL   = self.baseDiagonalGradationColor2()
        self.GRD_C_DIAGONAL_3 = self.baseDiagonalGradationColor3()
        
        self.HOVER_H = (
            '%s:hover{background-color:rgb(%s,%s,%s)}')
        self.HOVER_P = (
            '%s:pressed{background-color:rgb(%s,%s,%s);border:1px none;}')
        self.HOVER_BC = (
            '%s%s'%(self.HOVER_H,self.HOVER_P))
        self.HOVER_BC_R = (
            self.HOVER_BC%('%s','222','44' ,'44' ,'%s','111','11' ,'11' ))
        self.HOVER_BC_G = (
            self.HOVER_BC%('%s','44' ,'222','44' ,'%s','11' ,'111','11' ))
        self.HOVER_BC_B = (
            self.HOVER_BC%('%s','44' ,'44' ,'222','%s','11' ,'11' ,'111'))
        self.HOVER_BC_LIST = [self.HOVER_BC_R,self.HOVER_BC_G,self.HOVER_BC_B]
    
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
    
    def getCommonTabColor(self):
        r"""
            msAppTools共通タブカラーのスタイル情報を取得
        """
        return self.commonTabColor()
    
    ## ------------------------------------------------------------------------
    ## color combination
    
    def combinationBackgroundColor(self,color):
        r"""
            background-color形式で書式を返す
        """
        return('background-color:{};'.format(color) if color else '')
    
_CSM_ = ColorStyleManagement()

## ----------------------------------------------------------------------------
## - default background color (互換性維持)

MAINUIBGC_C = _CSM_.MAINUIBGC_C
MAINUIBGC   = _CSM_.MAINUIBGC
TABBGC_C    = _CSM_.TABBGC_C
TABBGC      = _CSM_.TABBGC
PBC_C       = _CSM_.PBC_C
PBC         = _CSM_.PBC
LEC_C       = _CSM_.LEC_C
LEC         = _CSM_.LEC

## ----------------------------------------------------------------------------
## - gradation color (互換性維持)

GRD_C            = _CSM_.GRD_C
GRD_C_DEF        = _CSM_.GRD_C_DEF
GRD_C_VERTICAL   = _CSM_.GRD_C_VERTICAL
GRD_C_VERTICAL_3 = _CSM_.GRD_C_VERTICAL_3
GRD_C_HORIZON    = _CSM_.GRD_C_HORIZON
GRD_C_SIDE       = _CSM_.GRD_C_HORIZON
GRD_C_HORIZON_3  = _CSM_.GRD_C_HORIZON_3
GRD_C_SIDE_3     = _CSM_.GRD_C_HORIZON_3
GRD_C_DIAGONAL   = _CSM_.GRD_C_DIAGONAL
GRD_C_DIAGONAL_3 = _CSM_.GRD_C_DIAGONAL_3

## ----------------------------------------------------------------------------
## - hover color (互換性維持)

HOVER_H       = _CSM_.HOVER_H
HOVER_P       = _CSM_.HOVER_P
HOVER_BC      = _CSM_.HOVER_BC
HOVER_BC_R    = _CSM_.HOVER_BC_R
HOVER_BC_G    = _CSM_.HOVER_BC_G
HOVER_BC_B    = _CSM_.HOVER_BC_B
HOVER_BC_LIST = _CSM_.HOVER_BC_LIST

###############################################################################
## - font style (互換性維持)

class FontStyleManagement(object):
    r"""
        フォントマネジメント総合クラス
    """
    def __init__(self):
        r"""
        """
        self.fontSetting()

    def fontSetting(self):
        r"""
        """
        self.BORDER_STYLE_1 = (
        'QPushButton{'
            'border-style:none;'
            'background-color:transparent;'
        '}'
        )
        self.BORDER_STYLE_2 = '{}{}'.format(self.BORDER_STYLE_1,(
            'QPushButton:pressed{'
                'padding-left:2px;'
                'padding-top:2px;'
            '}'
        ))
        # border-left:1px solid black;
        # border-top :1px solid black;
        self.LABEL_STYLE = 'QLabel{font-family:GEORGIA;font-size:13px;}'
        self.GROUPFONT   = 'font-family:arial black;' # グループタイトルのフォント
      
_FSM_ = FontStyleManagement()      

BORDER_STYLE_1 = _FSM_.BORDER_STYLE_1
BORDER_STYLE_2 = _FSM_.BORDER_STYLE_2
LABEL_STYLE    = _FSM_.LABEL_STYLE
GROUPFONT      = _FSM_.GROUPFONT

###############################################################################
## - margin (互換性維持)

class SpaceStyleManagement(object):
    r"""
        スペースマネジメント総合クラス
    """
    def __init__(self):
        r"""
        """
        self.spaceSetting()
    
    def spaceSetting(self):
        r"""
        """
        # スペーシングの間隔
        self.SP  = 2
        # カラムのマージン
        self.GM  = [2, 2, 2, 2]
        # ラベルマージン
        self.LM  = [4, 0, 4, 2]
        # ラベルの上部のマージン
        self.LTM = 8
        # ラベルの下部のマージン
        self.LBM = 2

_SSM_ = SpaceStyleManagement()
   
SP  = _SSM_.SP
GM  = _SSM_.GM
LM  = _SSM_.LM
LTM = _SSM_.LTM
LBM = _SSM_.LBM

###############################################################################
## END
