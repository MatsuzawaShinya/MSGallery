#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
"""
###############################################################################
## base lib

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

###############################################################################
## 

class ColorLibrary(object):
    r"""
        基本カラーの設定クラス
    """
    def __init__(self):
        r"""
        """
        pass
        
    def __repr__(self):
        r"""
        """
        return '+ Func <<{}>>'.format(self.__class__.__name__)

    ## ------------------------------------------------------------------------
    ## base color setting
        
    def mainBackgrondColor(self):
        r"""
            ウィジェットベースカラー
        """
        return '#232323'
        
    def mainTabColor(self):
        r"""
            タブベースカラー
        """
        return '#373737'
        
    def buttonColor(self):
        r"""
            ボタンベースカラー
        """
        return '#585858'
        
    def inputBoxColor(self):
        r"""
            ボタンベースカラー
        """
        return '#252525'
        
    ## ------------------------------------------------------------------------
    ## msAppTools base tab color
    
    def commonTabColor(self):
        r"""
            msAppTools共通タブカラーのスタイル情報を取得
        """
        return (
            'QTabWidget::pane{'
                'border: 3px solid #252525;'
            '}'
            'QTabWidget::tab-bar{'
                'left: 2px;'
            '}'
            'QTabBar::tab{'
                'color: #DDD;'
                'background: qlineargradient('
                    'x1:0, y1:0, x2:0, y2:1, stop:0 #666, stop:1 #333'
                ');'
                'min-width: 22ex;'
                'padding: 4px;'
                'border-top-left-radius:1px; border-top-right-radius:1px;'
            '}'
            'QTabBar::tab:selected, QTabBar::tab:hover {'
                'background-color:qlineargradient'
                    '(x1:0, y1:0, x2:0, y2:1, stop:0 #888, stop:1 #555'
                ')'
            '}'
            'QTabBar::tab:selected {'
                'margin-left: 1px; margin-right: 1px;'
            '}'
            'QTabBar::tab:first:selected {'
                'margin-left: 0px;'
            '}'
            'QTabBar::tab:last:selected {'
                'margin-right: 0px;'
            '}'
            'QTabBar::tab:pressed {'
                'background: qlineargradient('
                    'x1:0, y1:0, x2:0, y2:1, stop:0 #555, stop:1 #222'
                ');'
            '}'
        )
    
    ## ------------------------------------------------------------------------
    ## gradation color setting
    
    def baseGradientStyleWord(self):
        r"""
            グラデーションのベースとなるスタイルワードの取得(%記述)
        """
        return (
            'background:qlineargradient('
                'x1:%(x1)s,'
                'y1:%(y1)s,'
                'x2:%(x2)s,'
                'y2:%(y2)s,'
                'stop:0 %(stop0)s,'
                '%(stopA)s%(stopB)s%(stopC)s'
                'stop:1.0 %(stop1)s'
            ');'
        )
        
    def baseDefaultGradationColor(self):
        r"""
            デフォルトのグラデーションカラースタイル配列を返す
        """
        return self.baseGradientStyleWord() % {
            'x1'   :'0' ,'y1'   :'0' ,
            'x2'   :'1' ,'y2'   :'1' ,
            'stop0':'%s','stop1':'%s',
            'stopA':''  ,'stopB':''  ,'stopC':'',
        }
        
    def baseVerticalGradationColor2(self):
        r"""
            垂直2色のグラデーションカラースタイル配列を返す
        """
        return self.baseGradientStyleWord() % {
            'x1'   :'0' ,'y1'   :'0' ,
            'x2'   :'0' ,'y2'   :'1' ,
            'stop0':'%s','stop1':'%s',
            'stopA':''  ,'stopB':''  ,'stopC':'',
        }
        
    def baseVerticalGradationColor3(self):
        r"""
            垂直3色のグラデーションカラースタイル配列を返す
        """
        return self.baseGradientStyleWord() % {
            'x1'   :'0'           ,'y1'   :'0' ,
            'x2'   :'0'           ,'y2'   :'1' ,
            'stop0':'%s'          ,'stop1':'%s',
            'stopA':'stop:0.5 %s,','stopB':''  ,'stopC':'',
        }
        
    def baseHorizonGradationColor2(self):
        r"""
            横2色のグラデーションカラースタイル配列を返す
        """
        return self.baseGradientStyleWord() % {
            'x1'   :'0' ,'y1'   :'0' ,
            'x2'   :'1' ,'y2'   :'0' ,
            'stop0':'%s','stop1':'%s',
            'stopA':''  ,'stopB':''  ,'stopC':'',
        }
        
    def baseHorizonGradationColor3(self):
        r"""
            横3色のグラデーションカラースタイル配列を返す
        """
        return self.baseGradientStyleWord() % {
            'x1'   :'0'           ,'y1'   :'0' ,
            'x2'   :'1'           ,'y2'   :'0' ,
            'stop0':'%s'          ,'stop1':'%s',
            'stopA':'stop:0.5 %s,','stopB':''  ,'stopC':'',
        }
        
    def baseDiagonalGradationColor2(self):
        r"""
            対角線2色のグラデーションカラースタイル配列を返す
        """
        return self.baseGradientStyleWord() % {
            'x1'   :'0' ,'y1'   :'0' ,
            'x2'   :'1' ,'y2'   :'1' ,
            'stop0':'%s','stop1':'%s',
            'stopA':''  ,'stopB':''  ,'stopC':'',
        }
        
    def baseDiagonalGradationColor3(self):
        r"""
            対角線3色のグラデーションカラースタイル配列を返す
        """
        return self.baseGradientStyleWord() % {
            'x1'   :'0'           ,'y1'   :'0' ,
            'x2'   :'1'           ,'y2'   :'1' ,
            'stop0':'%s'          ,'stop1':'%s',
            'stopA':'stop:0.5 %s,','stopB':''  ,'stopC':'',
        }

###############################################################################
## END
