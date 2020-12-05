#!/usr/bin/python
# -*- coding: utf-8 -*-
# old_style:google style:google
r"""
    enter description
    
    Dates:
        date:2019/03/07 12:20[matsuzawa@gooneys.co.jp]
        update:2020/04/08 20:21 StudioGOONEYS,Inc.[matsuzawa@gooneys.co.jp]
        
    License:
        Copyright 2019 StudioGOONEYS,Inc.[matsuzawa@gooneys.co.jp] - All Rights Reserved
        Unauthorized copying of this file, via any medium is strictly prohibited
        Proprietary and confidential
"""
import os,re,sys,json,math,time,shutil,traceback
from stat import *
from maya import cmds,mel,OpenMaya,OpenMayaUI
from ..settingFiles import systemGeneral as sg

_TE = sg.TimeEvent()

# =============================================================================
# common func系

def uc(command,*args,**keywords):
    r"""
        undoを一つにまとめる
        
        Args:
            command (any):[関数]
            *args (any):
            **keywords (any):
            
        Returns:
            any:None
    """
    cmds.undoInfo(ock=True)
    try:
        command(*args,**keywords)
    except Exception as e:
        raise e
    finally:
        cmds.undoInfo(cck=True)

# =============================================================================
# - modeling

def deleteHistroy(select=[]):
    r"""
        選択or引数のオブジェクトのヒストリー削除
        
        Args:
            select (any):[edit]
            
        Returns:
            any:None
    """
    fn = sys._getframe().f_code.co_name
    
    if not select:
        select = cmds.ls(sl=True)
    if not select:
        print(
            u'+ [Func:%s] 何もノードが選択されていないので'
            u'処理を終了します。' % (fn)
        )
        return
    
    for sel in select:
        cmds.delete(sel,ch=True)
        print(
            u'+ [Func:%s] [Node:%s]ヒストリーを削除しました。' % (fn, sel)
        )

def setBackfaceCulling(type=0,toggle=False):
    r"""
        バックフェースカリングの設定
        
        Args:
            type (any):0=off,1=wire,2=hard,3=full
            toggle (any):True=ToggleFlag->ON
            
        Returns:
            any:
    """
    for sel in cmds.ls(sl=True):
        name = '%s.%s' % (sel,'backfaceCulling')
        if not cmds.objExists(name):
            continue
        if toggle:
            type = 1 if cmds.getAttr(name) == 0 else 0
        cmds.setAttr(name,type)

def setFreeze(t=True,r=True,s=True,j=False,history=False):
    r"""
        フリーズの設定
        
        Args:
            t (any):translateフラグ
            r (any):rotateフラグ
            s (any):scaleフラグ
            j (any):jointフラグ
            history (any):enter description
            
        Returns:
            any:
    """
    sel = cmds.ls(sl=True)
    if not sel:
        return False
    setUndoInfo(True)
    try:
        for n in sel:
            cmds.makeIdentity(n,apply=True,t=t,r=r,s=s,jo=j,n=2,pn=False)
            print(u'+ Freeze [t=%s,r=%s,s=%s,jo=%s], node=%s'%(t,r,s,j,n))
            if history:
                cmds.delete(n,ch=True)
    except Exception as e:
        raise e
    finally:
        setUndoInfo(False)

def setRenderVisible(node,value=True):
    r"""
        レンダー情報のON/OFF化
        
        Args:
            node (any):ノード名
            value (any):TrueでOFF,FalseでON
            
        Returns:
            any:
    """
    P = ('castsShadows','receiveShadows','holdOut','motionBlur',
           'primaryVisibility','smoothShading','visibleInReflections',
           'visibleInRefractions','doubleSided')
    E = ('doubleSided',) if value else P
    FLAG = {x:x in E for x in P}
    [cmds.setAttr('{}.{}'.format(node,x),FLAG[x]) for x in FLAG]
        
def normalizedCv(type=1):
    r"""
        CVの初期化(=0設定)
        
        Args:
            type (any):enter description
            
        Returns:
            any:
    """
    node = cmds.ls(sl=True)
    if not node:
        return False
    setUndoInfo(True)
    try:
        for sel in cmds.ls(sl=True):
            if type == 1:
                for axis in 'xyz':
                    point=cmds.ls('%s.pnts[*].pnt%s'%(sel,axis))
                    for p in point:
                        try:
                            cmds.setAttr(p,0)
                        except:
                            print(u'+ CVの初期化に失敗 node=%s'%(p))
            elif type == 2:
                # cvを0にセットしただけじゃ数値がキレイにならない場合があるので
                # デフォーマーを掛けてリセットする
                cmds.cluster(sel,n='msapp_normalizedCv_setdef_%s'%(sel))
                cmds.delete(sel,ch=True)
    except Exception as e:
        raise e
    finally:
        setUndoInfo(False)
        
def resetPivot(type=True):
    r"""
        ピポットをオブジェクトの中心に移動する
        
        Args:
            type (any):True=オブジェクト中心 False=原点
            
        Returns:
            any:
    """
    if type:
        cmds.xform(cp=True)
    else:
        [cmds.move(0,0,0,'%s.%s'%(n,p),a=True) for n in cmds.ls(sl=True)
            for p in ('scalePivot','rotatePivot') if cmds.objExists('%s.%s'%(n,p))]

def axisZeroMove(axis='x'):
    r"""
        頂点orエッジを中心点(xyz)に移動
        
        Args:
            axis (any):enter description
            
        Returns:
            any:
    """
    if not axis in 'xyz':
        return False
    x,y,z,max = False,False,False,None
    sel = cmds.ls(sl=True)
    ver = cmds.filterExpand(sel,sm=31,ex=True)
    edg = cmds.filterExpand(sel,sm=32,ex=True)
    if ver or edg:
        if ver:
            max = ver
        elif edg:
            mel.eval('PolySelectConvert 3;')
            sel = cmds.ls(sl=True)
            max = cmds.filterExpand(sel,sm=31,ex=True)
    print(u'+ Vertex[%s]'%(len(max)))
    cmds.select(max,r=True)
    if axis == 'x':
        x = True
    elif axis == 'y':
        y = True
    elif axis == 'z':
        z = True
    cmds.move(0,a=True,x=x,y=y,z=z)
    return True

def applyAverageVertex(iterations=1):
    r"""
        アベレージバーテックスの適用
        
        Args:
            iterations (any):丸みのステップ数
            
        Returns:
            any:
    """
    cmds.polyAverageVertex(i=iterations)

def duplicateReversal(axis='X',merge=False):
    r"""
        オブジェクトの複製フラグでマージも実行
        
        Args:
            axis (any):コピーする軸
            merge (any):マージを行うかのフラグ
            
        Returns:
            any:
    """
    revList = ('_%s','%s_','_%s_')
    LRList  = ('L','R')
    LRListR = ('R','L')
    piv     = ('scalePivot','rotatePivot')
    sel     = cmds.ls(sl=True)
    if not sel:
        return False
    setUndoInfo(True)
    try:
        for s in sel:
            cmds.select(s,r=True)
            xp = cmds.xform(s,q=True,t=True)
            ps = cmds.xform(s,q=True,sp=True)
            pr = cmds.xform(s,q=True,rp=True)
            for ax_s in ['sx','sy','sz']:
                at = '%s.%s'%(s,ax_s)
                if cmds.getAttr(at,l=True):
                    cmds.setAttr(at,l=False)
            cmds.move(0,0,0,'%s.%s'%(s,piv[0]),'%s.%s'%(s,piv[1]))
            repName = '%s_#'%(s)
            for i,LR in enumerate(LRList):
                for rL in revList:
                    rxp  = '%s'%(rL%(LR))
                    rxpR = '%s'%(rL%(LRListR[i]))
                    r = re.search(rxp,s)
                    if r:
                        repName = s.replace(rxp,rxpR)
                        break
            dup   = cmds.duplicate(rr=True,n=repName)[0]
            axis  = axis.lower()
            scale = (
                [-1,1,1]
                    if axis == 'x' else
                [1,-1,1]
                    if axis == 'y' else
                [1,1,-1]
                    if axis == 'z' else
                [-1,1,1]
            )
            cmds.scale(scale[0],scale[1],scale[2],dup,r=True)
            cmds.move(
                (xp[0]),(xp[1]),(xp[2]),
                '%s.%s'%(s,piv[0]),'%s.%s'%(s,piv[1]),a=True,ws=True,
            )
            cmds.move(
                (xp[0]*scale[0]),(xp[1]*scale[1]),(xp[2]*scale[2]),
                '%s.%s'%(dup,piv[0]),'%s.%s'%(dup,piv[1]),a=True,ws=True,
            )
            cmds.select(dup,r=True)
            
            if merge:
                p = cmds.listRelatives(s,p=True)
                if p:
                    cmds.parent(s,dup,w=True)
                buf = cmds.polyUnite(s,dup,ch=True,mergeUVSets=True)
                cmds.polyMergeVertex(buf[0],d=0.00001,am=True,ch=True)
                cmds.delete(buf[0],ch=True)
                [cmds.delete(d) for d in [s,dup] if cmds.objExists(d)]
                cmds.select(cmds.rename(buf[0],s),r=True)
                if p:
                    cmds.parent(s,p[0])
    except Exception as e:
        raise e
    finally:
        setUndoInfo(False)

def originPositionCheck(axis='x',accuracy=15,selectFlag=True):
    r"""
        axis指定の頂点位置が原点位置にあるかどうかのチェック
        
        Args:
            axis (any):調べる軸位置
            accuracy (any):精度
            selectFlag (any):フラグオンでヒットした頂点を選択する
            
        Returns:
            any:ヒットした頂点位置を格納したリスト
    """
    sel   = cmds.ls(sl=True)
    if not sel:
        return []
    ver   = cmds.filterExpand(sel,sm=31,ex=True)
    axis  = axis.lower()
    table = float(('0.{:0<%s}1'%(str(accuracy))).format(''))
    hit   = []
    for v in ver:
        pos = cmds.pointPosition(v)
        target_pos = (
            pos[0]
                if axis=='x' else
            pos[1]
                if axis=='y' else
            pos[2]
                if axis=='z' else
            pos[0]
        )
        if target_pos < table and target_pos > (table*-1):
            hit.append(v)
    if hit and selectFlag:
        cmds.select(hit,r=True)
    return hit
    
def fitToMesh(node, refresh, geomode):
    r"""
        fitToMeshのメイン関数
        
        Args:
            node (any):貼り付けるオブジェクト
            refresh (any):リフレッシュを行うか
            geomode (any):頂点の移動モード
            
        Returns:
            any:None
    """
    fn = sys._getframe().f_code.co_name
    
    def refresh():
        r"""
            リフレッシュ関数
            
            Returns:
                any:None
        """
        if refresh is True:
            cmds.refresh
    
    # print(node, refresh, geomode)
    
    vertex = cmds.filterExpand(ex=True, sm=[28, 31])
    if not vertex:
        print(
            u'+ [Func:%s] vertexが選択されていないため'
            u'処理を終了します。' % (fn)
        )
        return
    size = len(vertex)
    
    # geometryMode ON
    if geomode:
        setUndoInfo(True)
        try:
            for i in range(size):
                cls = 'tmpCluster%s' % (i)
                cmds.cluster(vertex[i], n=cls)
                handle = '%sHandle' % (cls)
                cmds.geometryConstraint(node, handle)
                sp = vertex[i].split('.')[0]
                cmds.delete(sp, ch=True)
                cmds.delete(handle)
                refresh()
        except Exception as e:
            raise e
        finally:
            setUndoInfo(False)
    # geometryMode OFF
    if not geomode:
        cpom = '%stdsFitToMeshCPOM' % (node)
        if cmds.objExists(cpom):
            cmds.delete(cpom)
        cmds.createNode('closestPointOnMesh', n=cpom)
        shape = cmds.listRelatives(node, s=True)
        cmds.connectAttr('%s.outMesh'%(shape[0]), '%s.inMesh'%(cpom), f=True)
        setUndoInfo(True)
        try:
            for i in range(size):
                obj = vertex[i]
                pos = cmds.pointPosition(obj, w=True)
                cmds.setAttr('%s.inPositionX'%(cpom), pos[0])
                cmds.setAttr('%s.inPositionY'%(cpom), pos[1])
                cmds.setAttr('%s.inPositionZ'%(cpom), pos[2])
                # print(obj, pos)
                posX = cmds.getAttr('%s.positionX'%(cpom))
                posY = cmds.getAttr('%s.positionY'%(cpom))
                posZ = cmds.getAttr('%s.positionZ'%(cpom))
                # print(posX, posY, posZ)
                cmds.move(posX, posY, posZ, obj, ws=True)
                refresh()
        except Exception as e:
            raise e
        finally:
            setUndoInfo(False)
        
        if cmds.objExists(cpom):
            cmds.delete(cpom)        
        
# =============================================================================
# - material

def assignMaterialColor(nodeList=[],mtr='',sg='',mtrType='',col=[1.0,1.0,1.0]):
    r"""
        マテリアルカラーのアサイン関数
        
        Args:
            nodeList (any):ノードリスト
            mtr (any):マテリアルネーム
            sg (any):シェーディングネーム
            mtrType (any):マテリアルタイプ
            col (any):アサインカラー数値
            
        Returns:
            any:
    """
    if not nodeList:
        nodeList = cmds.ls(sl=True)
    
    setColor = 'outColor' if mtrType == 'surfaceShader' else 'color'
        
    if not mtrType:
        mtrType = 'lambert'
    
    if not mtr:
        mtr = 'msSim_amc_%sMT'%(mtrType)
    if not sg:
        sg  = '%sSG'%(mtr)
    
    for ms in [mtr,sg]:
        suf = 1
        while(1):
            mtrname = ('%s%s'%(ms,suf))
            if not cmds.objExists(mtrname):
                break
            suf += 1
        if cmds.objExists(ms):
            rem = cmds.rename(ms, ('%s%s'%(ms,str(suf))))
            print(
                u'+ Rename node. [%s]->[%s]' % (ms,rem)
            )
    
    mtr = cmds.shadingNode(mtrType,n=mtr,asShader=True)
    cmds.sets(n=sg,r=True,nss=True,em=True)
    cmds.connectAttr('%s.outColor'%(mtr),'%s.surfaceShader'%(sg),f=True)
    cmds.setAttr('%s.%s'%(mtr,setColor),col[0],col[1],col[2])
    # for node in nodeList:
        # un = cmds.listRelatives(node,s=True,pa=True)
        # if un is None:
            # un = node
        # cmds.sets(un,e=True,fe=sg)
        # print(u'Assing material node. [%s]'%(un))
    cmds.select(nodeList,r=True)
    cmds.hyperShade(assign=mtr)
            
# =============================================================================
# - cache

def createEmptyCache(node,cacheName=''):
    r"""
        空のキャッシュファイルを作成
        
        Args:
            node (any):コネクションするノード(シェイプ)名
            cacheName (any):作成するキャッシュ名(何も指定しなければランダムネーム)
            
        Returns:
            any:
    """
    if not node or not cmds.objExists(node):
        print(u'+ node名が指定されていないか見つかりません。')
        print(u'\tnode : %s'%(node))
        return False
    if not cmds.objExists('%s.inMesh'%(node)):
        print(u'+ node名にinMeshアトリビュートが存在しません。')
        return False
    if not cacheName:
        cacheName = returnRandomString(6)
    cf = None
    setUndoInfo(True)
    try:
        cf = cmds.createNode('cacheFile',n='%s_cacheFile'%(cacheName))
        hs = cmds.createNode('historySwitch',n='%s_historySwitch'%(cacheName))
        cmds.connectAttr('time1.outTime','%s.time'%(cf))
        cmds.connectAttr('%s.outCacheData[0]'%(cf),'%s.inPositions[0]'%(hs))
        cmds.connectAttr('%s.inRange'%(cf),'%s.playFromCache'%(hs))
        cmds.connectAttr('%s.outputGeometry[0]'%(hs),'%s.inMesh'%(node),f=True)
        # undeformedGeometryに情報を差し込む。その後はコネクションを削除しても良い
        cmds.connectAttr('%s.outMesh'%(node),'%s.undeformedGeometry[0]'%(hs),f=True)
        cmds.disconnectAttr('%s.outMesh'%(node),'%s.undeformedGeometry[0]'%(hs))
    except Exception as e:
        raise e
    finally:
        setUndoInfo(False)
    return cf
    
def createGeometryCache(node=[],path='',confirmation=True,
    backup=False,local=False,cacheMerge=False,**keywords
):
    r"""
        ジオメトリキャッシュの作成
        
        Args:
            node (any):[list]キャッシュノードを作成するリスト
            path (any):[bytes]パス
            confirmation (any):[boolean]確認のダイアログを出すか出さないか
            backup (any):[bool]バックアップをするかの有無
            local (any):[bool]ローカルでキャッシュを取るか
            cacheMerge (any):[bool]リストで選択されたノード単一かまとめてキャッシュ取るか
            **keywords (any):
            
        Returns:
            any:None
    """
    def _createCache(node,path):
        r"""
            キャッシュ作成
            
            Args:
                node (any):[bytes or list]ノード
                path (any):enter description
                
            Returns:
                any:
        """
        n = node[0] if isinstance(node,list) else node
        frame = 2
        tMin = int(cmds.playbackOptions(q=True, min=True))
        tMax = int(cmds.playbackOptions(q=True, max=True))
        perf = 'add'
        file = 'OneFile'
        type = 'mcc'
        cacheName = n.replace(':','_')
        addCacheName = ''
        for key in keywords:
            if key == 'frame':
                frame = keywords[key]
            elif key == 'min':
                tMin = keywords[key]
            elif key == 'max':
                tMax = keywords[key]
            elif key == 'file':
                file = keywords[key]
            elif key == 'type':
                type = keywords[key]
            elif key == 'addCacheName':
                addCacheName = keywords[key]
            elif key == 'cacheName':
                if not keywords[key]:
                    cacheName = n
                    print(
                        u'+ [Func:%s] cacheName set. [n:%s] ' % (
                            fn, cacheName
                        )
                    )
                else:
                    cacheName = keywords[key]
                    print(
                        u'+ [Func:%s] cacheName set. [keywords[key]:%s]' % (
                            fn, cacheName
                        )
                    )
        cacheName += addCacheName
        createExtension = ('mc' if type == 'mcc' else 'mcx')
        _TE.flowProcessStartTime()
        # backup
        if backup:
            extMc      = 'mc'
            extMcx     = 'mcx'
            extXml     = 'xml'
            backupName = '_BU'
            # _BUフォルダを作成
            if not path:
                print(
                    u'+ [Func:%s] [path]が指定されていないため'
                    u'処理を終了します。'%(fn)
                )
                return
            if not os.path.isdir(path):
                print(
                    u'+ s[Func:%s] [path:%s]のフォルダが見つからないため'
                    u'処理を終了します。' % (fn, path)
                )
                return
            buFolder = os.path.join(path, '_BU')
            if not os.path.isdir(buFolder):
                os.mkdir(buFolder)
                print(u'+ [Func:%s] Create backup dir.[path:%s]' % (fn, buFolder))
            for ext in [extMc, extMcx, extXml]:
                srcFile = ('%s/%s.%s' % (path, cacheName, ext))
                if not os.path.isfile(srcFile):
                    print(u'+ [Func:%s] Skip file [file:%s]' % (fn, srcFile))
                    continue
                # index番号を調べる
                hitList = []
                dstDir = buFolder
                buFolderList = os.listdir(dstDir)
                for item in buFolderList:
                    hit = re.search('^%s[\.].*[\.]%s$' % (cacheName, ext), item)
                    if hit:
                        hitList.append(hit)
                index = len(hitList)+1
                dstFile = ('%s/%s.%s.%s' % (dstDir, cacheName, str(index), ext))
                shutil.copy2(srcFile, dstFile)
                print(
                    u'+ [Func:%s] File backup [src:%s] -> [dst:%s]' % (
                        fn, srcFile, dstFile
                    )
                )
        if local:
            origPath = path
            path     = os.path.join(
                os.environ["USERPROFILE"],'Documents','maya',
                'projects','default','data','cache','Temp'
            ).replace('\\','/')
            print(
                u'+ [Func:%s] Export path local set. -> [path:%s]' % (
                    fn, path
                )
            )
        '''
        frame:
            time range mode = 0 : use $args[1] and $args[2] as start-end
            time range mode = 1 : use render globals
            time range mode = 2 : use timeline
        '''
        cycleCheckSwitch(switch=False)
        # cmds.select(n, r=True)
        cmds.select(node, r=True)
        cmd = ('doCreateGeometryCache 6 {'
            '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",'
            '"%s","%s","%s","%s","%s","%s","%s"};' ) % (
            frame, tMin, tMax, file, '1', path, '0', cacheName, '0', perf,
            '0', '1', '1', '0', '1', type, '0',)
        mel.eval(cmd)
        cc = '%sCache1'%(cacheName)
        if cmds.objExists(cc):
            cmds.rename(cc,cacheName)
            print(u'\t+ rename cache. [%s] -> [%s]'%(cc,cacheName))
        print(
            u'+ [Func:%s] Export Cache. [Node:%s] [Path:%s] [cmd:%s]' % (
                fn, cacheName, path, cmd
            )
        )
        cycleCheckSwitch(switch=True)
        if local:
            localMcFile  = ('%s/%s.%s' %(path, cacheName, createExtension))
            localXmlFile = ('%s/%s.xml'%(path, cacheName))
            origMcFile   = ('%s/%s.%s' %(origPath, cacheName, createExtension))
            origXmlFile  = ('%s/%s.xml'%(origPath, cacheName))
            shutil.move(localMcFile, origMcFile)
            shutil.move(localXmlFile,origXmlFile)
            print(
                u'+ [Func:%s] Copy from cache data local. '
                u'[local:%s] -> [orig:%s]' % (fn, path, origPath)
            )
            '''
            # nameを指定した場合そのノードが存在しないのでsel=[0]のノード名を適用する
            if not cmds.objExists(cacheName):
                cacheName = n
                print(
                    u'+ [Func:%s] Set node name. <sel[0]=[%s]>' % (fn, n)
                )
            '''
            # for cn in cmds.listRelatives(cacheName, c=True, pa=True, s=True):
            for cn in cmds.listRelatives(n, c=True, pa=True, s=True):
                if cn.endswith('Orig'):
                    continue
                switch = cmds.listConnections('%s.inMesh' % cn)
                if not switch or not cmds.ls(switch,st=True)[1] == 'historySwitch':
                    continue
                cacheNode = cmds.listConnections('%s.playFromCache' % switch[0])
                if not cacheNode:
                    continue
                cacheNode = cacheNode[0]
                break   
            cmds.setAttr('%s.cachePath'%(cacheNode), origPath, type='string')
            print(
                u'+ [Func:%s] Re-cache the cache path '
                u'-> [node:%s] [path:%s]' % (
                    fn, cacheNode, origPath
                )
            )
            path = origPath
        for cache in cmds.ls(type='cacheFile'):
            rx = 'Cache[0-9]+$'
            if (not re.search(rx,cache) or
                re.search('^{}'.format(rx),cache) or
                re.search('^.+:{}'.format(rx),cache)
            ):
                continue
            ren = re.sub(rx,'',cache)
            cmds.rename(cache,ren)
            print(u'+ Rename cache[0-9]? :\n\t{} => {}'.format(cache,ren))
        end = _TE.flowProcessEndTime()
        print(u'+ Processing time : %s sec'%(round(end,2)))
        print
    fn = sys._getframe().f_code.co_name
    if confirmation:
        Y,N = 'Yes','No'
        res = cmds.confirmDialog(
            t=u'実行確認', m=u'キャッシュ作成を実行しますか？',
            b=[Y, N], db=Y, cb=N, ds=N,
        )
        if res == N:
            return
    if not node:
        node = cmds.ls(sl=True)
    if not node:
        print(u'+ [Func:%s] Nothing selected processing exit.'%(fn))
        return
    if not path:
        print(u'+ [Func:%s] Pass empty processing end.'%(fn))
        return
    if not os.path.isdir(path):
        print(
            u'+ [Func:%s] File path can not be checked Finish processing. '
            u'[Path:%s]' % (fn, path)
        )
        return
    if cacheMerge:
        _createCache(node,path)
    else:
        [_createCache(n,path) for n in node]
    return True
        
def replaceCache(confirmation=True,node=[],start=None,end=None,noBackup=True):
    r"""
        キャッシュを置き換えて更新する関数
        
        Args:
            confirmation (any):確認ダイアログぼのフラグ
            node (any):キャッシュを取るノードリスト
            start (any):キャッシュのスタートフレーム
            end (any):キャッシュのエンドフレーム
            noBackup (any):noBackupの有無
            
        Returns:
            any:None
    """
    fn = sys._getframe().f_code.co_name
    
    if confirmation:
        Y = 'Yes'
        N = 'No'
        res = cmds.confirmDialog(
            t=u'実行確認', m=u'キャッシュ更新を実行しますか？',
            b=[Y, N], db=Y, cb=N, ds=N,
        )
        if res == N:
            return False
    
    if not node:
        print(u'%s[Func:%s] [node]が選択されていません。' % (_CT, fn))
        return
    if not start:
        print(u'%s[Func:%s] [start]の値が設定されていません。' % (_CT, fn))
        return
    if not end:
        print(u'%s[Func:%s] [end]の値が設定されていません。' % (_CT, fn))
        return
    
    sel = []
    for n in node:
        shape = cmds.listRelatives(n, pa=True, c=True, s=True)
        if not shape:
            continue
        shapeNode = shape[0]
        type = cmds.ls(shapeNode, st=True)[1]
        if not type == 'mesh':
            continue
        sel.append(shapeNode)
    
    if not sel:
        print(u'%s[Func:%s] Shapeノードが見つかりません。' % (_CT, fn))
        return False
    
    cmds.cacheFile(
        replaceCachedFrame = True,
        points             = sel,
        startTime          = start,
        endTime            = end,
        simulationRate     = 1,
        sampleMultiplier   = 1,
        noBackup           = noBackup
    )
    
    print(u'%s[Func:%s] Replace update cache.' % (_CT, fn))

# =============================================================================
# - animation

def cycleCheckSwitch(switch=False):
    r"""
        サイクルチェックのオンorオフ設定
        
        Args:
            switch (any):[boolean]cycleCheck True or False
            
        Returns:
            any:None
    """
    fn = sys._getframe().f_code.co_name
    
    cmds.cycleCheck(e=switch)
    print(u'+ [Func:%s] CycleCheck [%s]' % (fn, switch))

def getTimeSlider():
    r"""
        タイムスライダーの最小・最大値を返す
        
        Returns:
            any:最小値と最大値
    """
    return (
        int(cmds.playbackOptions(q=True,min=True)),
        int(cmds.playbackOptions(q=True,max=True)),
    )
    
def getRanderGlobalFrameRange():
    r"""
        レンダー設定のスタートエンドフレーム数を返す
        
        Returns:
            any:レンダー設定の最小値と最大値
    """
    return (
        int(cmds.getAttr('defaultRenderGlobals.startFrame')),
        int(cmds.getAttr('defaultRenderGlobals.endFrame')),
    )

def setTimeRange(startFrame=0, endFrame=0):
    r"""
        start,endの値の数値でタイムレンジを設定する
        
        Args:
            startFrame (any):タイムスライダの開始の値
            endFrame (any):タイムスライダの終了の値
            
        Returns:
            any:None
    """
    cmds.playbackOptions(
        ast=startFrame, min=startFrame,
        aet=endFrame, max=endFrame
    )
    cmds.currentTime(cmds.playbackOptions(q=True,min=True))
    
def playbackViewChange(type=None):
    r"""
        playbackViewの設定
        
        Args:
            type (any):all or active
            
        Returns:
            any:
    """
    set = 'active' if 'all' == cmds.playbackOptions(q=True,v=True) else 'all'
    if type:
        set = type
    try:
        cmds.playbackOptions(v=set)
        print(u'+ Set playbackOptions [set:%s]' % (set))
    except:
        print(
            u'+ playbackOptionsを設定できませんでした。 変数[set:%s]' % (set)
        )

def alembicExporter(exportPath='',option=['',''],**keywords):
    r"""
        アレンビックのエクスポーター
        
        Args:
            exportPath (any):エクスポート先のパス
            option (any):[0]=verbose,[1]=それ以外のフラグ
            **keywords (any):
            
        Returns:
            any:
    """
    if not exportPath:
        print(u'+ exportPathが設定されていません。')
        return
    if not os.path.isdir(exportPath):
        print(u'+ エクスポートするフォルダが見つかりません。[%s]' % (exportPath))
        return
    
    nodeN = ''
    nPref = ''
    nSuff = ''
    start = cmds.playbackOptions(q=True,min=True)
    end   = cmds.playbackOptions(q=True,max=True)
    
    for key in keywords:
        if key == 'node':
            nodeN = keywords[key]
        if key == 'namePrifix' or key == 'np':
            nPref = keywords[key]
        if key == 'nameSuffix' or key == 'ns':
            nSuff = keywords[key]
        if key == 'start':
            start = keywords[key]
        if key == 'end':
            end = keywords[key]
        
    sel = cmds.ls(sl=True)
    if not sel:
        print(u'何も選択されていません。')
        return
    
    for i,s in enumerate(sel):
        if nodeN:
            node = '%s%s' % (nodeN,str(i))
        else:
            node = s
            check1 = referenceNodeCheck(node)
            check2 = re.search(':',node)
            if check1 and check2:
                sp = node.split(':')
                node = sp[1]
                print(
                    '+ Reference node name split. -> [%s] and [%s]' % (
                        sp[0],sp[1]
                    )
                )
        
        srcName = '%s%s%s.abc' % (nPref,node,nSuff)
        dstPath = sg.toBasePath(os.path.join(exportPath,srcName))
        
        alembicCmd = (
            'AbcExport %s -j "-frameRange %s %s %s '
            '-dataFormat ogawa -root %s -file %s";' % (
                option[0], start, end, option[1], s, dstPath
            )
        )
        
        try:
            mel.eval(alembicCmd)
            print('+ Export alembic data : [name=%s,path=%s]' % (srcName,dstPath))
            print('+ cmd : [%s]' % (alembicCmd))
        except:
            print(
                u'+ alembicファイルの書き出しに失敗しました。'
                u'[name=%s,path=%s]' % (srcName,dstPath)
            )

def alembicImporter(importPath=''):
    r"""
        アレンビックファイルのインポート
        
        Args:
            importPath (any):インポートするアレンビックファイル
            
        Returns:
            any:
    """
    check = True
    try:
        from PySide2 import QtWidgets
    except:
        check = False
    
    if not importPath:
        if not check:
            print(
                u'+ QtWidgetsが読み込めずimportPathが'
                u'設定されていないため処理を終了します。'
            )
            return
        importPath = QtWidgets.QFileDialog.getOpenFileName()[0]
    else:
        if not os.path.isfile(importPath):
            print(
                u'+ importPathの設定先にファイルが存在しません。\n'
                u'+ [importPath=%s]' % (importPath)
            )
            return
    
    # [\]だとインポートがうまくいかないため変換
    importPath = sg.toBasePath(importPath)
    
    abcImportCmd = 'AbcImport -mode import "%s";' % (importPath);
    try:
        mel.eval(abcImportCmd)
        print('+ Import alembic data : [path=%s]' % (importPath))
    except:
        print(
            u'+ alembicファイルの書き出しに失敗しました。'
            u'[path=%s]' % (importPath)
        )

def executePlayblast(**keywords):
    r"""
        プレイブラストの実行
        
        Args:
            **keywords (any):
            
        Returns:
            any:
    """
    forceOverwrite = True
    offScreen      = True
    sequenceTime   = False
    clearCache     = True
    viewer         = True
    showOrnaments  = True
    framePadding   = 4
    percent        = 100
    quality        = 75
    startTime      = 1
    endTime        = 2
    fileName       = 'playblast'
    format         = None
    compression    = None
    width          = 320
    height         = 240
    
    for key in keywords:
        if key == 'fo'  or key == 'forceOverwrite':
            forceOverwrite = keywords[key]
        if key == 'os'  or key == 'offScreen':
            offScreen      = keywords[key]
        if key == 'sqt' or key == 'sequenceTime':
            sequenceTime   = keywords[key]
        if key == 'cc'  or key == 'clearCache':
            clearCache     = keywords[key]
        if key == 'v'   or key == 'viewer':
            viewer         = keywords[key]
        if key == 'orn' or key == 'showOrnaments':
            showOrnaments  = keywords[key]
        if key == 'fp'  or key == 'framePadding':
            framePadding   = keywords[key]
        if key == 'p'   or key == 'percent':
            percent        = keywords[key]
        if key == 'qlt' or key == 'quality':
            quality        = keywords[key]
        if key == 'st'  or key == 'startTime':
            startTime      = keywords[key]
        if key == 'et'  or key == 'endTime':
            endTime        = keywords[key]
        if key == 'f'   or key == 'fileName':
            fileName       = keywords[key]
        if key == 'fmt' or key == 'format':
            format         = keywords[key]
        if key == 'c'   or key == 'compression':
            compression    = keywords[key]
        if key == 'w'   or key == 'width':
            width          = keywords[key]
        if key == 'h'   or key == 'height':
            height         = keywords[key]
    
    if not format:
        print(u'+ formatタイプが入力されていません。')
        return
    if not compression:
        print(u'+ compressionタイプが入力されていません。')
        return
    
    cmds.playblast(
        forceOverwrite = forceOverwrite,
        offScreen      = offScreen,
        sequenceTime   = sequenceTime,
        clearCache     = clearCache,
        viewer         = viewer,
        showOrnaments  = showOrnaments,
        framePadding   = framePadding,
        percent        = percent,
        quality        = quality,
        startTime      = startTime,
        endTime        = endTime,
        filename       = fileName,
        format         = format,
        compression    = compression,
        width          = width,
        height         = height,
    )
    
    print(u'+'+('-'*80))
    print(u'+ Playblast write complete.')
    print(u'\tExport path    : %s'%(fileName))
    print(u'\tWidthHeight    : %s %s'%(width, height))
    print(u'\tStart time     : %s'%(startTime))
    print(u'\tEnd time       : %s'%(endTime))
    print(u'\tFormat         : %s'%(format))
    print(u'\tCompression    : %s'%(compression))
    print(u'\tPercent        : %s'%(percent))
    print(u'\tQuality        : %s'%(quality))
    print(u'\tForceOverwrite : %s'%(forceOverwrite))
    print(u'\tOffScreen      : %s'%(offScreen))
    print(u'\tSequenceTime   : %s'%(sequenceTime))
    print(u'\tClearCache     : %s'%(clearCache))
    print(u'\tViewer         : %s'%(viewer))
    print(u'\tShowOrnaments  : %s'%(showOrnaments))
    print(u'\tFramePadding   : %s'%(framePadding))
    print(u'+'+('-'*80))

def playblastFormatEncodingList(printFlag=False):
    r"""
        playblastのフォーマットコーディングのプリント
        
        Args:
            printFlag (any):enter description
            
        Returns:
            any:
    """
    returnList = {}
    
    formatList = mel.eval('playblast -format "" -q;')
    for m1 in formatList:
        EncodingList = mel.eval('playblast -format "%s" -q -compression;' % (m1))
        returnList[m1] = EncodingList
        if printFlag:
            print(m1)
            for m2 in EncodingList:
                print(u'\t%s' % m2)
    
    return returnList
    
# =============================================================================
# - defomer

def wrapAssign(src='', dst=[], **keywords):
    r"""
        ラップ処理をする
        
        Args:
            src (any):[ベースとなるノード]
            dst (any):[ターゲットのノードリスト]
            **keywords (any):
            
        Returns:
            any:None
    """
    fn = sys._getframe().f_code.co_name
    
    threshold = 0.0
    maxDist = 1.0
    inflType = 2
    exclusiveBind = 1
    autoWeightThreshold = 0
    parentFlag = False
    
    for key in keywords:
        if key == 'threshold':
            threshold = keywords[key]
        if key == 'maxDist':
            maxDist = keywords[key]
        if key == 'inflType':
            inflType = keywords[key]
        if key == 'exclusiveBind':
            exclusiveBind = keywords[key]
        if key == 'autoWeightThreshold':
            autoWeightThreshold = keywords[key]
        if key == 'parentFlag':
            parentFlag = keywords[key]
    
    sel = cmds.ls(sl=True)
    if src is '':
        src = sel[-1]
    if not dst:
        dst = sel[:-1]
    
    if not src:
        print(
            u'+ [Func:%s] [src]が何も選択されていないため処理を終了します。' % (
                fn
            )
        )
        return
    if not dst:
        print(
            u'+ [Func:%s] [dst]が何も選択されていないため処理を終了します。' % (
                fn
            )
        )
        return
    
    cmds.select(dst, src, r=True)
    res = mel.eval(
        'doWrapArgList("6",{"1","%s","%s","%s","%s","%s","1"});' %
        (threshold, maxDist, inflType, exclusiveBind, autoWeightThreshold)
    )
    
    if parentFlag:
        cmds.parent('%sBase'%src, src)
    
    returnList = []
    for d in dst:
        buf = cmds.listHistory(d, pdo=True, gl=True)
        for n in buf:
            if cmds.nodeType(n) == 'wrap':
                returnList.append(n)
                baseShape = cmds.listConnections('%s.basePoints[0]' % (n))
                if baseShape:
                    returnList.extend(baseShape)
    
    return returnList

def blensShapeAssign(src='', dst=[], **keywords):
    r"""
        ブレンドシェイプの適用関数
        
        Args:
            src (any):[bytes]デフォームジオメトリ
            dst (any):[bytes]ターゲットジオメトリ
            **keywords (any):
            
        Returns:
            any:作成されたブレンドシェイプ名
    """
    fn = sys._getframe().f_code.co_name
    
    name   = None
    origin = 'local'
    weight = [0,0.0]
    
    for key in keywords:
        if key == 'name' or key == 'n':
            name = keywords[key]
        if key == 'origin' or key == 'o':
            origin = keywords[key]
        if key == 'weight' or key == 'w':
            weight = [keywords[key][0], keywords[key][1]]
    
    sel = cmds.ls(sl=True)
    if not src:
        src = sel[-1]
    if not dst:
        dst = sel[:-1]
        
    if not src:
        print(
            u'+ [Func:%s] [src]が何も選択されていないため処理を終了します。' % (
                fn
            )
        )
        return
    if not dst:
        print(
            u'+ [Func:%s] [dst]が何も選択されていないため処理を終了します。' % (
                fn
            )
        )
        return
        
    if not origin in ['local', 'world']:
        print(
            u'+ [Func:%s] [origin:%s]の値が適切ではありません。\n'
            u'+ ["local"or"world"]を指定してください。' % (
                fn, origin
            )
        )
        return
    
    if not name:
        name = src
        print(
            u'+ [Func:%s] [name]が空なので[src:%s]の名前にセットしました。' % (
                fn, src
            )
        )
    if not len(weight) == 2:
        print(
            u'+ [Func:%s] [weight]の配列個数が2個以外だったので'
            u'既定値[0, 1.0]にセットしました。' % (fn)
        )
    
    bs = cmds.blendShape(
        dst, src, n='%s_BS' % (name), o=origin, w=[weight[0], weight[1]]
    )[0]
    
    print(
        u'+ [Func:%s] Create blendShape. [name:%s] [src:%s -> dst:%s]' % (
            fn, bs, src, dst
        )
    )
    
    return bs
    
# =============================================================================
# - simulation

def setConstraintMembership(type=None,constraint=''):
    r"""
        メンバーシップの編集関数
        
        Args:
            type (any):メンバーシップの実行タイプ
            constraint (any):対象のコンストレインノード名
            
        Returns:
            any:
    """
    
    def _dcc(node):
        r"""
            ダイナミックコンストレイントのチェック
            
            Args:
                node (any):チェック対象ノード
                
            Returns:
                any:
        """
        targetType = 'dynamicConstraint'
        t = cmds.ls(node, st=True)
        if t[1] == targetType:
            return True
        ut = cmds.listRelatives(t[0],c=True,pa=True)
        if not ut:
            return False
        t = cmds.ls(ut[0], st=True)
        if t[1] == targetType:
            return True
        return False
    
    constraintNode = ''
    vertexList     = []
    
    for sel in cmds.ls(sl=True):
        if _dcc(sel):
            constraintNode = sel
        else:
            if re.search('vtx',sel):
                vertexList.append(sel)

    if constraint and cmds.objExists(constraint):
        if _dcc(constraint):
            constraintNode = constraint
    
    if not vertexList:
        print(u'+ 頂点が選択されていません。')
        return
    if not constraintNode:
        print(u'+ コンストレインノードが設定されていません。')
        return
    
    cmds.select(constraintNode,vertexList)
    mel.eval('dynamicConstraintMembership("%s");' % (type))
    
    print(u'+'+('-'*80))
    print(u'+ Execute dynamic constraint membership.')
    print(u'\tMembership type : %s' % (type))
    print(u'\tConstraint node : %s' % (constraintNode))
    print(u'\tVertex point    : %s' % ([i for i in vertexList]))
    print(u'+'+('-'*80))
        
def nConstraintSetting(flag=None,type=None):
    r"""
        dynamicConstraint系のアトリビュートの切り替え関数
        
        Args:
            flag (any):None and Toggle=ON<->OFF, True=ON, False=OFF
            type (any):0=enable,1=displayConnections,
            
        Returns:
            any:
    """
    TYPE_LIST = [
        'enable',
        'displayConnections',
    ]
    try:
        attrType = TYPE_LIST[type]
    except:
        print(
            u'+ 変数[TYPE_LIST]のレンジの範囲外です。\n'
            u'\ttype=%s,TYPE_LIST=%s' % (type,TYPE_LIST)
        )
        return
    
    sel = cmds.ls(sl=True)
    if not sel:
        sel = cmds.ls(type='dynamicConstraint')
    if not sel:
        print(u'+ dynamicConstraintがシーンにありません。')
        return
    
    finalNode = []
    
    setUndoInfo(True)
    try:
        for n in sel:
            src = n
            under = cmds.listRelatives(src,c=True,pa=True)
            if not under == None:
                src = under[0]
            attr = '%s.%s' % (src,attrType)
            if not cmds.objExists(attr):
                continue
            finalNode.append(src)
            setValue = None
            if flag == 'True':
                setValue = True
            elif flag == 'False':
                setValue = False
            elif flag == 'Toggle':
                setValue = False if cmds.getAttr(attr) else True
            else:
                setValue = False if cmds.getAttr(attr) else True
            cmds.setAttr(attr,setValue)
    except Exception as e:
        raise e
    finally:
        setUndoInfo(False)
    
    print(u'+ Set displayConnections :')        
    print(u'\tFlag : %s' % (flag))
    print(u'\tType : %s(%s)' % (type,attrType))
    for fn in finalNode:
        print(u'\tNode : %s' % (fn))

# -----------------------------------------------------------------------------

def nClothAttrValuesPaint(attribute=None, windowFlag=False):
    r"""
        nClothのペイント表示するコマンド
        
        Args:
            attribute (any):[bytes]実行するアトリビュートタイプ
            windowFlag (any):[bool]ペイント時にアトリビュートウィンドウを表示するかどうか
            
        Returns:
            any:None
    """
    fn = sys._getframe().f_code.co_name
    
    if not attribute:
        print(
            u'+ [Func:%s] 引数[attribute:%s]が指定されていないため'
            u'処理を終了します。' % (fn, attribute)
        )
        return
    nClothParam = pref.nClothAttrValues()
    if not attribute in nClothParam:
        print(
            u'+ [Func:%s] [attribute:%s]が指定のn系アトリビュートタイプでは'
            u'ないので処理を終了します。' % (fn, attribute)
        )
        return
    sel = cmds.ls(sl=True)
    if not sel:
        print(
            u'+ [Func:%s] 何もノードが選択されていないので'
            u'処理を終了します。' % (fn)
        )
        return
    
    if not windowFlag:
        return
    
    mel.eval('artAttrNClothToolScript(3,"%s");' % (attribute))
    
# -----------------------------------------------------------------------------

def nClothAttrValuesPrint(
    attribute=None, wrapNum=10, writeObjExists=True
):
    r"""
        選択しているnClothのアトリビュートをプリントする
        
        Args:
            attribute (any):[bytes]実行するアトリビュートタイプ
            wrapNum (any):[int]折り返す行数
            writeObjExists (any):[boolean]objExists形式にするか
            
        Returns:
            any:None
    """
    fn = sys._getframe().f_code.co_name
    
    if not attribute:
        print(
            u'+ [Func:%s] 引数[attribute:%s]が指定されていないため'
            u'処理を終了します。' % (fn, attribute)
        )
        return
    nClothParam = pref.nClothAttrValues()
    if not attribute in nClothParam:
        print(
            u'+ [Func:%s] [attribute:%s]が指定のn系アトリビュートタイプでは'
            u'ないので処理を終了します。' % (fn, attribute)
        )
        return
    
    sel = cmds.ls(sl=True, dag=True, s=True)
    if not sel:
        print(
            u'+ [Func:%s] 何もノードが選択されていないので'
            u'処理を終了します。' % (fn)
        )
        return
    sel = sel[0]
    type = cmds.objectType(sel)
    if not 'nCloth' == type:
        befsel = sel
        sel = cmds.listConnections('%s.inMesh'%(sel))[0]
        print(
            u'+ [Func:%s] 選択しているノードがnClothMeshなので'
            u'nClothShapeに置換します。\n'
            u'[%s] -> [%s]' % (
                fn, befsel, sel
            )
        )
    
    printCmd = ''
    inputAttr = cmds.getAttr('%s.%sPerVertex' % (sel, attribute))
    if not inputAttr:
        print(
            u'+ [Func:%s] PerVertexが取得出来なかったため処理を終了します。\n'
            u'+ 対象のパラメータ[%s]のペイントがされていない可能性があります。'
            % (fn, attribute)
        )
        return
    num = len(inputAttr)
    
    P  = ''
    P2 = '\t'
    if writeObjExists:
        P  = '\t'
        P2 = '\t\t'
        printCmd += 'if( `objExists "%s"` ){\n' % (sel)

    printCmd += ('%ssetAttr "%s.%sMapType" 1;\n' % (P, sel, attribute))
    printCmd += (
        '%ssetAttr "%s.%sPerVertex" -type "doubleArray" %s \n' % (
            P, sel, attribute, num
        )
    )
    printCmd += P2
    
    sum = 0
    for i in range(num):
        printCmd += ('%03.3f ' % (inputAttr[i])) # 小数点3桁で表示
        sum += 1 # 指定回数実行したら折り返し
        if sum >= wrapNum:
            printCmd += '\n'
            printCmd += P2
            sum = 0
    printCmd += (';\n')
    
    if writeObjExists:
        printCmd += '}\n'
    
    print(printCmd)

# -----------------------------------------------------------------------------

apgc = {'dup' :'dupMdl','tgt' :'tgtMdl','grid':'gridPlane','bld' :'bldMid'}

def alignPolyGridCreate():
    r"""
        ポリゴンのグリッドを作成する
        
        Returns:
            any:None
    """    
    fn = sys._getframe().f_code.co_name
    
    sel = cmds.ls(sl=True)
    if not sel:
       print(
            u'+ [Func:%s] 何も選択されていないため処理を終了します。' % (fn)
       )
       return
    
    sel  = cmds.duplicate(n=apgc['dup'],rr=True)
    maps = cmds.ls('%s.map[*]'%(sel[0]),fl=True)
    
    cmds.hilite(sel[0])
    cmds.select(maps[0], r=True)
    mel.eval('polySelectBorderShell(1);')
    mel.eval('PolySelectConvert(2);')
    cmds.ls(sl=True)
    mel.eval('PolySelectTraverse(2);')
    cmds.ls(sl=True)
    mel.eval('performDetachComponents;')
    cmds.select(sel[0], r=True)
    tgtMdl = cmds.duplicate(n=apgc['tgt'],rr=True)
    
    posUV = 0.0
    for n in maps:
        posUV = cmds.polyEditUV(n, q=True)
        cmds.select(n, r=True)
        mel.eval('PolySelectConvert(3)')
        cmds.move(posUV[0],0,(posUV[1]*-1),a=True,ws=True)
    
    gPlane = cmds.polyPlane(
        n='gridPlane',w=1,h=1,sx=10,sy=10,ax=[0,1,0],cuv=2,ch=1
    )
    cmds.setAttr ('%s.t'%(gPlane[0]),0.5,0,-0.5)
    
    cmds.transferAttributes(
        sel[0],gPlane[0],pos=1,nml=0,uvs=2,col=2,spa=0,
        sus='map1',tus='map1',sm=3,fuv=0,clb=1
    )
    
    cmds.select(apgc['dup'],r=True)
    dup2 = cmds.duplicate(n=apgc['bld'],rr=True)
    cmds.select(apgc['grid'],dup2,r=True)
    mel.eval('doWrapArgList("7",{"1","0","1","2","1","1","0","0"});')
    
    blend = cmds.blendShape(apgc['tgt'],dup2[0],bf=True)
    cmds.setAttr('%s.%s'%(blend[0],apgc['tgt']),1)
    
    ([cmds.setAttr('%s.template'%(n),1)
        for n in (apgc['dup'],apgc['tgt'],apgc['bld'])])

def alignPolyGridCleanup():
    r"""
        クリーンアップ処理を施す
        
        Returns:
            any:None
    """
    fn = sys._getframe().f_code.co_name
    
    sel = cmds.ls(sl=True)
    if not sel:
       print(
        u'+ [Func:%s] 何も選択されていないため処理を終了します。' % (fn)
    )
       return
    if not sel[0] == apgc['grid']:
        print(
            u'+ [Func:%s]%sではないため処理を終了します。'%(fn,apgc['grid'])
        )
        return
    mel.eval(
        'polyCleanupArgList(3,{"0","2","0","0","1","1","0","0",'
        '"1","1e-006","1","1e-006","0","1e-005","0","-1","0"});'
    )

def alignPolyGridFinish():
    r"""
        編集が終了したときのフィニッシング処理を施す
        
        Returns:
            any:None
    """
    fn = sys._getframe().f_code.co_name
    
    sel = cmds.ls(sl=True)
    if not sel:
       print(
        u'+ [Func:%s] 何も選択されていないため処理を終了します。'%(fn)
    )
       return
    if not sel[0] == apgc['grid']:
        print(
            u'+ [Func:%s]%sではないため処理を終了します。'%(fn,apgc['grid'])
        )
        return
        
    cmds.delete(sel[0],ch=True)
    cmds.makeIdentity(a=True ,t=True,r=True,s=True,n=False)
    cmds.makeIdentity(a=False,t=True,r=True,s=True,n=False)
    cmds.delete(apgc['dup'],apgc['tgt'],apgc['bld'],'%sBase'%(apgc['bld']))
    
def moveVertexSameNode(fitNode='',ratio=1.0,debugFlag=False):
    r"""
        fitNodeと同一なメッシュのバーテックスの移動値をratioの割合分だけ移動させる関数
        
        Args:
            fitNode (any):[bytes]バーテックスを移動させる目的のノードメッシュ
            ratio (any):[float]移動させる割合量
            debugFlag (any):[bool]デバック用のプリントフラグ
            
        Returns:
            any:None
    """
    fn = sys._getframe().f_code.co_name
    
    if not fitNode:
        print(
            u'+ [Func:%s] [fitNode]が空白のため処理を終了します。'%(fn)
        )
        return
    if not cmds.objExists(fitNode):
        print(
            u'+ [Func:%s] [fitNode:%s]が存在しないため処理を終了します。'%(
                fn,fitNode
            )
        )
        return
    
    origSelCV = cmds.ls(sl=True, fl=True)
    if not origSelCV:
        print(
            u'+ [Func:%s] CV(vertex)が選択されていないため'
            u'処理を終了します。' % (fn)
        )
        return
    
    for origCv in origSelCV:
        origTK = origCv.split('.')
        fitCv  = ('%s.%s'%(fitNode,origTK[1]))
        if not cmds.objExists(fitCv):
            print(
                u'[Func:%s]itさせる目的のvertexが見つからないため'
                u'処理をスキップします。' % (fn)
            )
            continue
            
        resPos  = []
        origPos = cmds.pointPosition(origCv)
        fitPos  = cmds.pointPosition(fitCv)
        resPos.append((fitPos[0]-origPos[0])*ratio)
        resPos.append((fitPos[1]-origPos[1])*ratio)
        resPos.append((fitPos[2]-origPos[2])*ratio)
        if debugFlag:
            print(
                '+ [Func:%s] [Node:%s -> %s] [PosX:%s] [PosY:%s] [PosZ:%s]'%(
                    fn,origCv,fitCv,resPos[0],resPos[1],resPos[2]
                )
            )
        cmds.move(resPos[0],resPos[1],resPos[2],origCv,r=True)
    
# =============================================================================
# - attribute

def getSceneCurrentUnit():
    r"""
        シーンのユニット情報を返す
        
        Returns:
            any:
    """
    return (
        cmds.currentUnit(q=True,l=True,f=True),
        cmds.currentUnit(q=True,a=True,f=True),
        cmds.currentUnit(q=True,t=True,f=True),
    )

def setAttribute(enable=True,type=None,lock=True,key=True,log=False):
    r"""
        attributeのlock,unlockの設定
        
        Args:
            enable (any):lock or unlock
            type (any):lock,unlockするアトリビュートタイプ
            lock (any):attributeをlockするかどうか
            key (any):attributeをkeyableするかどうか
            log (any):アトリビュート設定のプリント文を出力するかどうか
            
        Returns:
            any:
    """
    sel = cmds.ls(sl=True)
    if not sel:
        print(u'+ 何も選択されていないので処理を終了します。')
        return
    
    trs,xyz,axis  = 'trs','xyz',[]
    try:
        # type(len=1)...[t,r,s]
        if len(type) == 1 and type in trs:
            axis = ['%s%s'%(type,x) for x in xyz]
        # type(len=1)...[v]
        elif len(type) == 1 and type == 'v':
            axis.append(type)
        # type(len=2)...[tx,ty,tz,rx,ry,rz,sx,sy,sz]
        elif len(type) == 2:
            axis.append(type)
        # type(len=3)...[all]
        elif len(type) == 3 and type == 'all':
            axis = ['%s%s'%(t,x) for t in trs for x in xyz]
            axis.append('v')
        else:
            print(u'+ 変数[type:%s]の値が正しくありません。'%(type))
            return
    except:
        print(u'+ 変数[type:%s]の値が正しくありません。'%(type))
        return
    
    L_E = True  if enable else False
    L_K = False if enable else True
    
    setUndoInfo(True)
    try:
        for s in sel:
            for a in axis:
                attrName = '%s.%s' % (s,a)
                if not cmds.objExists(attrName):
                    continue
                if lock:
                    cmds.setAttr(attrName, l=L_E)
                if key:
                    cmds.setAttr(attrName, k=L_K)
                if log:
                    print(
                        u'+ Attribute setting [name:%s] [lock:%s] [key:%s]'%(
                            attrName,L_E,L_K
                        )
                    )
    except Exception as e:
        raise e
    finally:
        setUndoInfo(False)
    
def openAttributeEditor(node=''):
    r"""
        引数nodeにある物のアトリビュートエディタを開く
        
        Args:
            node (any):[bytes]アトリビュートエディタを開くノード
            
        Returns:
            any:None
    """
    fn = sys._getframe().f_code.co_name
    
    if not node:
        print(
            u'+ [Func:%s] [引数:node]が指定されていません。'%(fn)
        )
        return
    if not cmds.objExists(node):
        print(
            u'+ [Func:%s] [node:%s]が見つかりません。'%(fn,node)
        )
        return
        
    mel.eval('showEditor "%s";'%(node))

def getDisplayLayerList():
    r"""
        ディスプレイレイヤの一覧をリスト化して取得
    """
    dsplayer=cmds.ls(type='displayLayer')
    return [x for x in dsplayer if not x.endswith('defaultLayer')]

# =============================================================================
# - name

def renameReplacePasted():
    r"""
        [pasted__]を消してリネームする
        
        Returns:
            any:
    """
    rep = 'pasted__'
    for s in cmds.ls(sl=True):
        src = s
        if not re.search(rep,src):
            continue
        dst = src.replace(rep,'')
        if cmds.objExists(dst):
            dst += '#'
        dstRename = cmds.rename(src,dst)
        print('+ Rename [src:%s] -> [dst:%s]'%(src,dstRename))

def renameObjectAddOldName(name='old'):
    r"""
        複製し末尾にネームを付与する
        
        Args:
            name (any):付与するネーム
            
        Returns:
            any:
    """
    sel = cmds.ls(sl=True)
    if not sel:
        print(u'+ 何も選択されていません。')
        return
    
    for s in sel:
        setUndoInfo(True)
        try:
            src = s
            duplicate = cmds.duplicate(src,rr=True,n=('%s_dup'%(src)))
            rem = cmds.rename(src,('%s_%s'%(src,name)))
            cmds.hide(rem)
            cmds.rename(duplicate,src)
        except Exception as e:
            raise e
        finally:
            setUndoInfo(False)

# =============================================================================
# - view

def template(set=True):
    r"""
        templateの設定
        
        Args:
            set (any):ON=True, OFF=False
            
        Returns:
            any:
    """
    def _check(node=None):
        r"""
            template設定する際のロックチェックなど
            
            Args:
                node (any):ノード名(.template付き)
                
            Returns:
                any:判定に引っかかったらTrueを返す
        """
        if not node:
            return True
        # templateアトリビュートの有無
        if not cmds.objExists(node):
            print(u'+ ".template"がありません。')
            return True
        # ロック判定
        if cmds.getAttr(node,l=True):
            print(u'+ ロックが掛かっています。')
            return True
        # キー設定判定
        if not cmds.getAttr(node,se=True):
            print(u'+ アトリビュートが設定出来ません。')
            return True
        return False
    
    sel = cmds.ls(sl=True)
    if not sel:
        print(u'+ 何も選択されてないので処理を終了します。')
        return
    
    for s in sel:
        tmp = '%s.template'%(s)
        if _check(tmp):
            return
        cmds.setAttr(tmp,set)
        print(u'+ Set template [node=%s,set=%s]'%(s,set))

def useDefMatChange(enable=True,type=None):
    r"""
        useDefaultMaterialの切り替え
        
        Args:
            enable (any):useDefaultMaterialの有効無効
            type (any):個々or全体で設定するか
            
        Returns:
            any:
    """
    # 個別
    if type == 'single' or type == 's':
        p = cmds.getPanel(wf=True)
        cmds.modelEditor(p,e=True,udm=enable)
    # ビュー全て
    elif type == 'all' or type == 'a':
        all_p = cmds.getPanel(type='modelPanel')
        [cmds.modelEditor(p,e=True,udm=enable) for p in all_p]
    else:
        print(u'+ [type]が設定されていません。')
        
def setViewState(target=[],switch=True,allView=False,printFlag=False,log=False):
    r"""
        ビュー表示非表示の設定
        
        Args:
            target (any):切り替えのアトリビュート
            switch (any):スイッチングタイプ
            allView (any):全てのビューに適用するか
            printFlag (any):フラグをプリントする
            log (any):ログの出力
            
        Returns:
            any:
    """
    P = ['nurbsCurves','nurbsSurfaces','controlVertices','hulls','polymeshes',
         'subdivSurfaces','planes','lights','cameras','imagePlane','joints',
         'ikHandles','deformers','dynamics','particleInstancers','fluids','hairSystems',
         'follicles','nCloths','nParticles','nRigids','dynamicConstraints',
         'locators','dimensions','pivots','handles','textures','displayTextures',
         'strokes','motionTrails','pluginShapes','clipGhosts','greasePencils',
         'allObjects','xray','manipulators','grid','headsUpDisplay',
         'holdOuts','selectionHiliteDisplay']
    D = {}
    
    if printFlag:
        P.sort()
        line = '{}{}'.format('+',('-'*80))
        print(line)
        for p in P:
            print('\t{}'.format(p))
        print(line)
        return
    
    if not target:
        return
    if switch != True and switch != False:
        return
    
    for p in P:
        value = p in target if switch else not p in target
        sw = None
        if p in target:
            sw = True
            if 'allObjects' == p:
                D = {}
                D[p] = value
                break
        else:
            sw = False
            
        if 'gpuCacheDisplayFilter' == p:
            D['pluginObjects'] = [p,sw]
        else:
            D[p] = value
    
    if allView:
        all_p = cmds.getPanel(type='modelPanel')
        [cmds.modelEditor(p,e=True,**D) for p in all_p]
    else:
        p = cmds.getPanel(wf=True)
        cmds.modelEditor(p,e=True,**D)
    
    if log:
        print(log)
        
# =============================================================================
# - window

def windowOption(type='open',w=500,h=300,min=0,max=99):
    r"""
        簡易ウィンドウ作成削除関数
        
        Args:
            type (any):実行タイプ
            w (any):enter description
            h (any):enter description
            min (any):enter description
            max (any):enter description
            
        Returns:
            any:
    """
    win_min = min
    win_max = max
    _wbn    = 'msappWindowName'
    d_type  = {
        1:['o','open','cr','create'],
        2:['cl','close','d','delete'],
    }
    def openWindow(w=500,h=300):
        r"""
            簡易ウィンドウのオープン
            
            Args:
                w (any):横幅
                h (any):縦幅
                
            Returns:
                any:
        """
        for i in range(win_min,win_max):
            winName = '%s%s'%(_wbn,str(i))
            if cmds.window(winName,ex=True):
                continue
            win = cmds.window(winName,title='Window[%s]'%(str(i)))
            cmds.paneLayout()
            cmds.modelPanel()
            cmds.showWindow(win)
            cmds.window(winName,e=True,w=w,h=h)
            return win
    def deleteWindow():
        r"""
            開いているウィンドウの削除
            
            Returns:
                any:
        """
        for i in range(win_min,win_max):
            winName = '%s%s'%(_wbn,str(i))
            if not cmds.window(winName,ex=True):
                continue
            cmds.deleteUI(winName,wnd=True)
            print('+ Delete window [%s]'%(winName))
    type = type.lower()
    if   type in d_type[1]:
        openWindow(w,h)
    elif type in d_type[2]:
        deleteWindow()
    else:
        raise (u'+ 変数エラー type=[%s]'%(type))

# =============================================================================
# - referenece
    
def returnReferencePath():
    r"""
        読み込まれているアセットのパスのリターン
        
        Returns:
            any:True=リファレンスパス,False=None
    """
    refList = cmds.file(q=True,r=True)
    returnList = []
    
    if not refList:
        return
    for ref in refList:
        buf = ref.split('{')
        returnList.append(buf[0])
    
    return list(set(returnList))

def returnReferencePathFull():
    r"""
        読み込まれているアセットのパスのリターン(重複削除なし)
        
        Returns:
            any:True=リファレンスパス,False=None
    """
    refList = cmds.file(q=True,r=True)
    returnList = []
    
    if not refList:
        return
    for ref in refList:
        buf = ref.split('{')
        returnList.append(buf[0])
    
    return returnList

def returnReferenceName():
    r"""
        読み込まれているアセットのリファレンスネームのリターン
        
        Returns:
            any:True=リファレンスネーム,False=None
    """
    refList = returnReferencePath()
    if not refList:
        return None
    return [cmds.file(x,q=True,rpl=True)[0] for x in refList]
    
def returnReferenceNameFull():
    r"""
        読み込まれているアセットのリファレンスネームのリターン(重複削除なし)
        
        Returns:
            any:True=リファレンスネーム,False=None
    """
    referenceList = returnReferencePathFull()
    returnList = set()
    if not referenceList:
        return
    for ref in referenceList:
        returnList.update(cmds.file(ref,q=True,rpl=True))
    returnList = list(returnList)
    
    return returnList

def referenceNodeCheck(node):
    r"""
        選択ノードがリファレンスかどうかの確認
        
        Args:
            node (any):検索するノード
            
        Returns:
            any:
    """
    return cmds.referenceQuery(node,inr=True)

# =============================================================================
# - rendering

def resolutionList():
    r"""
        解像度リストの取得
        
        Returns:
            any:
    """
    # リスト順に使いたい為辞書ではなくリスト化
    # データ参考元
    #   C:/Program Files/Autodesk/Maya2017/scripts/others/resolutionFormats.mel
    
    return [
    #   name                      width  height aspect dpi
    # -------------------------------------------------------------------------
        ['320*240',               320 ,  240 ,  1.333, 72.000 ],
        ['640*480',               640 ,  480 ,  1.333, 72.000 ],
        ['1k Square',             1024,  1024,  1.000, 72.000 ],
        ['2k Square',             2048,  2048,  1.000, 72.000 ],
        ['3k Square',             3072,  3072,  1.000, 72.000 ],
        ['4k Square',             4096,  4096,  1.000, 72.000 ],
        ['CCIR PAL/Quantel PAL',  720 ,  576 ,  1.333, 72.000 ],
        ['CCIR 601/Quantel NTSC', 720 ,  486 ,  1.333, 72.000 ],
        ['Full 1024',             1024,  768 ,  1.333, 72.000 ],
        ['Full 1280/Screen',      1280,  1024,  1.333, 72.000 ],
        ['HD 540',                960 ,  540 ,  1.777, 72.000 ],
        ['HD 720',                1280,  720 ,  1.777, 72.000 ],
        ['HD 1080',               1920,  1080,  1.777, 72.000 ],
        ['NTSC 4d',               646 ,  485 ,  1.333, 72.000 ],
        ['PAL 768',               768 ,  576 ,  1.333, 72.000 ],
        ['PAL 780',               780 ,  576 ,  1.333, 72.000 ],
        ['Targa 486(tga)',        512 ,  486 ,  1.333, 72.000 ],
        ['Targa NTSC(tga)',       512 ,  482 ,  1.333, 72.000 ],
        ['Targa PAL(tga)',        512 ,  576 ,  1.333, 72.000 ],
        ['Letter',                2550,  3300,  0.773, 300.000],
        ['Legal',                 2550,  4200,  0.607, 300.000],
        ['Tabloid',               5100,  3300,  1.545, 300.000],
        ['A4',                    2480,  3508,  0.707, 300.000],
        ['A3',                    3507,  4962,  0.707, 300.000],
        ['B5',                    2079,  2952,  0.704, 300.000],
        ['B4',                    2952,  4170,  0.708, 300.000],
        ['B3',                    4170,  5907,  0.706, 300.000],
        ['2"x3"',                 600 ,  900 ,  0.667, 300.000],
        ['4"x6"',                 1200,  1800,  0.667, 300.000],
        ['5"x7"',                 1500,  2100,  0.714, 300.000],
        ['8"x10"',                2400,  3000,  0.800, 300.000],
    ]

# =============================================================================
# - system

def returnRandomString(length=4,word=''):
    r"""
        文字列をランダムに羅列して返す
        
        Args:
            length (any):文字列の長さ
            word (any):ランダムワード
            
        Returns:
            any:
    """
    import random
    
    if not word:
        w,v  = 'abcdefghijklmnopqrstuvwxyz','0123456789'
        word = '%s%s%s'%(w,w.upper(),v)
    return (''.join([random.choice(word) for i in range(length)]))

def numberConversion(val=None,convType=[-1,-1]):
    r"""
        進数から進数への変換
        
        Args:
            val (any):変換元の文字列or数字
            convType (any):X -> Y への変換数字
            
        Returns:
            any:
    """
    if not val:
        return -1
    if convType[0] == convType[1]:
        return -2
    
    if   convType[0] == 10 and convType[1] == 16 and isinstance(val,int):
        f = 1 
    elif convType[0] == 16 and convType[1] == 10 and isinstance(val,bytes):
        f = 2
    else:
        f = None
        
    def _calculation(val):
        r"""
            進数変換処理
            
            Args:
                val (any):数字
                
            Returns:
                any:
        """
        def _conv1016(num,type):
            r"""
                10進数と16進数どおしの変換
                
                Args:
                    num (any):変換元文字
                    type (any):1=10->16,2=16->10
                    
                Returns:
                    any:
            """
            if type == 1:
                vv = (
                    'A' if num == 10 else
                    'B' if num == 11 else
                    'C' if num == 12 else
                    'D' if num == 13 else
                    'E' if num == 14 else
                    'F' if num == 15 else
                    str(num)
                )
            elif type == 2:
                if re.search('[A-F]',num):
                    vv = (
                        10 if num == 'A' else
                        11 if num == 'B' else
                        12 if num == 'C' else
                        13 if num == 'D' else
                        14 if num == 'E' else
                        15 
                    )
                elif re.search('[0-9]',num):
                    vv = int(num)
                else:
                    raise RuntimeError('+ Not specifie., "[A-F]","[0-9]"')
            return vv
            
        if f == 1:
            def _loop(num):
                r"""
                    数値を最後のあまりまで計算する再帰関数
                    
                    Args:
                        num (any):次の計算数値
                        
                    Returns:
                        any:
                """
                a = (num//16)
                rst.append(str(_conv1016((num%16),1)))
                if not a == 0:
                    _loop(a)
            
            rst = []
            _loop(val)
            ret = ''
            for i in rst[::-1]:
                ret += str(i)
        elif f == 2:
            ret,index = 0,0
            for i in range((len(val)-1),-1,-1):
                ret   += (_conv1016(val[i],2)*(16**index))
                index += 1
        else:
            ret = None

        return ret
        
    return _calculation(val)
    
def setUndoInfo(type=True):
    r"""
        undoInfoの設定
        
        Args:
            type (any):True=open,False=close
            
        Returns:
            any:
    """
    if type:
        cmds.undoInfo(ock=True)
    else:
        cmds.undoInfo(cck=True)
    
def checkPluginCmd(pname='',auto=False):
    r"""
        プラグインのチェック
        
        Args:
            pname (any):プラグインネーム
            auto (any):autoで読み込むかどうか
            
        Returns:
            any:
    """
    if not pname:
        return
    
    result = None
    
    # 通常プラグイン
    if not auto:
        result = cmds.pluginInfo(pname,q=True,l=True)
    # autoプラグイン
    else:
        result = cmds.pluginInfo(pname,q=True,a=True)
    
    return result

def loadPluginSetting(pname='',auto=False):
    r"""
        プラグインの読み込み
        
        Args:
            pname (any):プラグインネーム
            auto (any):autoで読み込むかどうか
            
        Returns:
            any:
    """
    if not pname:
        return
    
    result,log = None,''
    # 通常プラグイン
    if not auto:
        if not checkPluginCmd(pname=pname,auto=False):
            cmds.loadPlugin(pname)
            print('+ Load plugin : %s'%(pname))
            result = True
        else:
            print(
                u'+ "%s"のプラグインがロードされています。'%(pname)
            )
            result = False
    # autoプラグイン
    else:
        if not checkPluginCmd(pname=pname,auto=True):
            cmds.pluginInfo(pname,e=True,a=True)
            print('+ Load auto plugin : %s'%(pname))
            result = True
        else:
            print(
                u'+ "%s"のプラグインがオートロードされています。'%(pname)
            )
            result = False
    
    return result

def viewCapture(
    path='',name='',ext='png',w=None,h=None,
    sizeRatio=100,createDirFlag=False,logPring=True
):
    r"""
        maya画面のキャプチャ
        
        Args:
            path (any):画像を書き出す先のパス
            name (any):画像の名前
            ext (any):書き出す画像拡張子
            w (any):書き出す横幅
            h (any):書き出す縦幅
            sizeRatio (any):サイズ倍率
            createDirFlag (any):書き出す先のフォルダパスがなかった場合作成するかのフラグ
            logPring (any):enter description
            
        Returns:
            any:処理成功で書き出したファイルパス,横幅,縦幅
    """
    # mask https://download.autodesk.com/us/maya/2009help/API/class_m3d_view.html#552977f93e8b3b3c78698f7dc681c24e
    # ビューの状態を変更したいので、グリッドは必ずオフになるようにする。
    # 「OpenMayaUI.M3dView.kDisplayGrid」は使用しない
    __displayMask = (
        OpenMayaUI.M3dView.kDisplayNurbsSurfaces |
        OpenMayaUI.M3dView.kDisplayMeshes
    )
    
    if not path:
        print(
            u'+ パスが入力されていません。\n'
            u'\t path : %s' % (path)
        )
        return False
    
    if not name:
        name = '%s_%s'%(
            cmds.about(cd=True).replace('/',''),returnRandomString(24)
        )
    
    abovePath = os.path.dirname(path)
    if not os.path.isdir(abovePath):
        if createDirFlag:
            os.makedirs(abovePath)
            print(u'+ Creata dir path [%s]'%(abovePath))
        else:
            print(u'+ 画像書き出し先のフォルダ作成を中断しました。')
            print(u'+ フォルダ作成をするには[createDirFlag=True]を設定してください')
            return False

    try:
        view = OpenMayaUI.M3dView.active3dView()
        
        # .setObjectDisplayでグリッドマスクを変更し
        # 実行しないとアクティブビューでキャプチャ出来ない？
        oldView = view.objectDisplay()
        view.setObjectDisplay(__displayMask)
        view.setObjectDisplay(oldView)
        view.refresh()
        
        img = OpenMaya.MImage()
        view.readColorBuffer(img,True)
        
        # imageのresizeは「.readColorBuffer」を実行した後にやる
        if not w or not isinstance(w,int):
            w = int(view.portWidth())
        if not h or not isinstance(h,int):
            h = int(view.portHeight())
        w = int(w*(sizeRatio//100.0))
        h = int(h*(sizeRatio//100.0))
        img.resize(w,h)
        
        ext    = ext.lower()
        e_path = os.path.join(path,'%s.%s'%(name,ext))
        img.writeToFile(e_path,ext)
        if logPring:
            print(u'+ Export img path data.')
            print(u'\tpath   : %s'%(e_path))
            print(u'\twidth  : %s'%(w))
            print(u'\theight : %s'%(h))
    except:
        print(u'+ キャプチャーに失敗しました。')
        traceback.print_exc()
        return False
    return (e_path,w,h)

def activeViewSelect(mode='object'):
    r"""
        アクティブビューの選択範囲内に入っている物を選択する
        
        Args:
            mode (any):enter description
            
        Returns:
            any:
    """
    # 0 ; kSelectObjectMode
    # 1 ; kSelectComponentMode
    # 2 ; kSelectRootMode
    # 3 ; kSelectLeafMode
    # 4 ; kSelectTemplateMode
    
    w,h = getViewSize()
    nvm = OpenMaya.MGlobal.selectionMode()
    if mode == 'template':
        OpenMaya.MGlobal.setSelectionMode(OpenMaya.MGlobal.kSelectTemplateMode)
    OpenMaya.MGlobal.selectFromScreen(
        0,0,w,h,OpenMaya.MGlobal.kReplaceList,
    )
    OpenMaya.MGlobal.setSelectionMode(nvm)

def getViewSize():
    r"""
        アクティブビューサイズの取得
        
        Returns:
            any:[0]=widthSize,[1]=heightSize,
    """
    view = OpenMayaUI.M3dView.active3dView()
    return (int(view.portWidth()),int(view.portHeight()))
        
def modifiersCommand(type=None,printCategory=None):
    r"""
        mayaのmodifiersコマンドのオプションやあれこれ
        
        Args:
            type (any):実行するタイプの指定
            printCategory (any):print時のオプション
            
        Returns:
            any:
    """
    fn = sys._getframe().f_code.co_name
    
    L = ('default','shift','ctrl','alt','command')
    DICT = {
        0  : '%s'               %(L[0]),
        1  : '%s'               %(L[1]),
        4  : '%s'               %(L[2]),
        5  : '%s + %s'          %(L[1],L[2]),
        8  : '%s'               %(L[3]),
        9  : '%s + %s'          %(L[1],L[3]),
        12 : '%s + %s'          %(L[2],L[3]),
        13 : '%s + %s + %s'     %(L[1],L[2],L[3]),
        16 : '%s'               %(L[4]),
        17 : '%s + %s'          %(L[1],L[4]),
        20 : '%s + %s'          %(L[2],L[4]),
        21 : '%s + %s + %s'     %(L[1],L[2],L[4]),
        24 : '%s + %s'          %(L[3],L[4]),
        28 : '%s + %s + %s'     %(L[2],L[3],L[4]),
        29 : '%s + %s + %s + %s'%(L[1],L[2],L[3],L[4]),
    }
    
    if not type:
        print(u'+ [Func:%s] [引数<type>]が指定されていません。' % (fn))
        return
    
    CL = []
    order = []
    
    if type == 'h' or type == 'help':
        CL.append(u'+ 引数のリスト')
        CL.append(u'\t第一引数[help(h)]       : この関数の引数をプリントします。')
        CL.append(u' ')
        CL.append(u'\t第一引数[modifiers(m)]  : modifiersCommand実行の返り値を返します。')
        CL.append(u' ')
        CL.append(u'\t第一引数[print(p)]      : modifiersCommandのコマンドをプリントします。')
        CL.append(u'\t\t第二引数[sort]        : modifiersCommandを文字でソートしプリント。')
        CL.append(u'\t\t第二引数[word]        : modifiersCommandをワード数でソートしプリント。')
        CL.append(u'\t\t第二引数[number]      : modifiersCommandを数字の若い順にソートしプリント。')
    
    if type == 'p' or type == 'print':
        if   printCategory == 'sort':
            order = [0,1,5,9,17,13,21,29,4,12,20,28,8,24,16]
            for o in order:
                CL.append('[%s] %s'%(DICT[o],o))
        elif printCategory == 'word':
            order = [0,1,4,8,16,5,9,17,12,20,24,13,21,28,29]
            for o in order:
                CL.append('[%s] %s'%(DICT[o],o))
        elif printCategory == 'number':
            order = [0,1,4,5,8,9,12,13,16,17,20,21,24,28,29]
            for o in order:
                CL.append('%s [%s]'%(o,DICT[o]))
        else:
            order = [0,1,5,9,17,13,21,29,4,12,20,28,8,24,16]
            for o in order:
                CL.append('[%s] %s'%(DICT[o],o))
    
    if type == 'm' or type == 'modifiers':
        mod = cmds.getModifiers()
        print('Get modifiers number : [%s]'%(mod))
        return mod
        
    print('/'*120)
    for P in CL:
        print(P)
    print('/'*120)
    
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# =============================================================================