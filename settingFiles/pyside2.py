#!/usr/bin/python
# -*- coding: utf-8 -*-
r'''
    @file     pyside2.py
    @brief    PySideをPySide2との互換を図るためのモジュール。
    @date     2019/04/22 15:28[matsuzawa@gooneys.co.jp]
    @update   2019/04/22 15:28[matsuzawa@gooneys.co.jp]
    このソースの版権は[StudioGOONEYS,Inc.]にあります
    無断転載、改ざん、無断使用は基本的に禁止しておりますので注意して下さい
    このソースを使用して不具合や不利益等が生じても[StudioGOONEYS,Inc.]
    は一切責任を負いませんのであらかじめご了承ください
'''
###############################################################################
## base lib

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

###############################################################################

# from ~ import *時に下３つのみをインポートするように明示。
__all__ = ['QtCore', 'QtGui', 'QtWidgets', 'QtWebKit', 'phonon', 'Package']
Package = 'PySide2'
try:
    from PySide2 import QtGui,QtCore,QtWidgets
except:
    from PySide import QtGui,QtCore
    Package = 'PySide'
    __OLDGUIATTRS = [
        'QAbstractButton',
        'QAbstractGraphicsShapeItem',
        'QAbstractItemDelegate',
        'QAbstractItemView',
        'QAbstractScrollArea',
        'QAbstractSlider',
        'QAbstractSpinBox',
        'QAction',
        'QActionGroup',
        'QApplication',
        'QBoxLayout',
        'QButtonGroup',
        'QCalendarWidget',
        'QCheckBox',
        'QColorDialog',
        'QColumnView',
        'QComboBox',
        'QCommandLinkButton',
        'QCommonStyle',
        'QCompleter',
        'QDataWidgetMapper',
        'QDateEdit',
        'QDateTimeEdit',
        'QDesktopWidget',
        'QDial',
        'QDialog',
        'QDialogButtonBox',
        'QDirModel',
        'QDockWidget',
        'QDoubleSpinBox',
        'QErrorMessage',
        'QFileDialog',
        'QFileIconProvider',
        'QFileSystemModel',
        'QFocusFrame',
        'QFontComboBox',
        'QFontDialog',
        'QFormLayout',
        'QFrame',
        'QGesture',
        'QGestureEvent',
        'QGestureRecognizer',
        'QGraphicsAnchor',
        'QGraphicsAnchorLayout',
        'QGraphicsBlurEffect',
        'QGraphicsColorizeEffect',
        'QGraphicsDropShadowEffect',
        'QGraphicsEffect',
        'QGraphicsEllipseItem',
        'QGraphicsGridLayout',
        'QGraphicsItem',
        'QGraphicsItemAnimation',
        'QGraphicsItemGroup',
        'QGraphicsLayout',
        'QGraphicsLayoutItem',
        'QGraphicsLineItem',
        'QGraphicsLinearLayout',
        'QGraphicsObject',
        'QGraphicsOpacityEffect',
        'QGraphicsPathItem',
        'QGraphicsPixmapItem',
        'QGraphicsPolygonItem',
        'QGraphicsProxyWidget',
        'QGraphicsRectItem',
        'QGraphicsRotation',
        'QGraphicsScale',
        'QGraphicsScene',
        'QGraphicsSceneContextMenuEvent',
        'QGraphicsSceneDragDropEvent',
        'QGraphicsSceneEvent',
        'QGraphicsSceneHelpEvent',
        'QGraphicsSceneHoverEvent',
        'QGraphicsSceneMouseEvent',
        'QGraphicsSceneMoveEvent',
        'QGraphicsSceneResizeEvent',
        'QGraphicsSceneWheelEvent',
        'QGraphicsSimpleTextItem',
        'QGraphicsTextItem',
        'QGraphicsTransform',
        'QGraphicsView',
        'QGraphicsWidget',
        'QGridLayout',
        'QGroupBox',
        'QHBoxLayout',
        'QHeaderView',
        'QInputDialog',
        'QItemDelegate',
        'QItemEditorCreatorBase',
        'QItemEditorFactory',
        'QKeyEventTransition',
        'QLCDNumber',
        'QLabel',
        'QLayout',
        'QLayoutItem',
        'QLineEdit',
        'QListView',
        'QListWidget',
        'QListWidgetItem',
        'QMainWindow',
        'QMdiArea',
        'QMdiSubWindow',
        'QMenu',
        'QMenuBar',
        'QMessageBox',
        'QMouseEventTransition',
        'QPanGesture',
        'QPinchGesture',
        'QPlainTextDocumentLayout',
        'QPlainTextEdit',
        'QProgressBar',
        'QProgressDialog',
        'QPushButton',
        'QRadioButton',
        'QRubberBand',
        'QScrollArea',
        'QScrollBar',
        'QShortcut',
        'QSizeGrip',
        'QSizePolicy',
        'QSlider',
        'QSpacerItem',
        'QSpinBox',
        'QSplashScreen',
        'QSplitter',
        'QSplitterHandle',
        'QStackedLayout',
        'QStackedWidget',
        'QStatusBar',
        'QStyle',
        'QStyleFactory',
        'QStyleHintReturn',
        'QStyleHintReturnMask',
        'QStyleHintReturnVariant',
        'QStyleOption',
        'QStyleOptionButton',
        'QStyleOptionComboBox',
        'QStyleOptionComplex',
        'QStyleOptionDockWidget',
        'QStyleOptionFocusRect',
        'QStyleOptionFrame',
        'QStyleOptionGraphicsItem',
        'QStyleOptionGroupBox',
        'QStyleOptionHeader',
        'QStyleOptionMenuItem',
        'QStyleOptionProgressBar',
        'QStyleOptionRubberBand',
        'QStyleOptionSizeGrip',
        'QStyleOptionSlider',
        'QStyleOptionSpinBox',
        'QStyleOptionTab',
        'QStyleOptionTabBarBase',
        'QStyleOptionTabWidgetFrame',
        'QStyleOptionTitleBar',
        'QStyleOptionToolBar',
        'QStyleOptionToolBox',
        'QStyleOptionToolButton',
        'QStyleOptionViewItem',
        'QStylePainter',
        'QStyledItemDelegate',
        'QSwipeGesture',
        'QSystemTrayIcon',
        'QTabBar',
        'QTabWidget',
        'QTableView',
        'QTableWidget',
        'QTableWidgetItem',
        'QTableWidgetSelectionRange',
        'QTapAndHoldGesture',
        'QTapGesture',
        'QTextBrowser',
        'QTextEdit',
        'QTileRules',
        'QTimeEdit',
        'QToolBar',
        'QToolBox',
        'QToolButton',
        'QToolTip',
        'QTreeView',
        'QTreeWidget',
        'QTreeWidgetItem',
        'QTreeWidgetItemIterator',
        'QUndoCommand',
        'QUndoGroup',
        'QUndoStack',
        'QUndoView',
        'QVBoxLayout',
        'QWhatsThis',
        'QWidget',
        'QWidgetAction',
        'QWidgetItem',
        'QWizard',
        'QWizardPage',
        'qApp'
    ]
    
    __OLDCOREATTRS = [
        'QAbstractProxyModel',
        'QItemSelection',
        'QItemSelectionModel',
        'QItemSelectionRange',
        'QSortFilterProxyModel',
    ]

    from PySide import QtCore as core
    from PySide import QtGui as gui
    # /////////////////////////////////////////////////////////////////////////
    # ダミーのQtWidgetsを作成する。                                          //
    # /////////////////////////////////////////////////////////////////////////
    class __DMYCLASS(object):
        r"""
            QtWidgets, QtGuiを模倣するためのダミークラス。
        """
        def __init__(self, moduleName):
            r"""
                初期化する。モジュール名を引数として渡す。
            """
            self.__modulename = moduleName

        def __repr__(self):
            r"""
                このクラスの目的を表示する。
            """
            return "<imitate '%s' of PySide2 from '%s'>" % (
                self.__modulename, __file__
            )

    QtWidgets = __DMYCLASS('QtWidgets')
    QtGui = __DMYCLASS('QtGui')
    for attr in dir(gui):
        m = QtWidgets if attr in  __OLDGUIATTRS else QtGui
        setattr(m, attr, getattr(gui, attr))

    for attr in __OLDCOREATTRS:
        setattr(QtCore, attr, getattr(gui, attr))
    # /////////////////////////////////////////////////////////////////////////
    #                                                                        //
    # /////////////////////////////////////////////////////////////////////////

# その他のモジュールの読み込み。（失敗した場合はNoneになる）
for mod in ('QtWebKit', 'phonon'):
    import importlib
    try:
        locals()[mod] = importlib.import_module(Package+'.'+mod)
    except Exception as e:
        locals()[mod] = None

###############################################################################
## END
