#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
    ツイッターAPI情報の取得クラス
"""
###############################################################################
## base lib

import os
import re
import sys
import json
import traceback
import unicodedata
sys.dont_write_bytecode = True

## ----------------------------------------------------------------------------
## third party lib

## ----------------------------------------------------------------------------
## local lib

import lib

###############################################################################

class MsTwitter(object):
    r"""
        ツイッター情報を取得する総合クラス
    """
    ## ------------------------------------------------------------------------
    ## common method
    
    def __init__(self):
        r"""
            初期設定
        """
        self.TWITTER = lib.Twitter()
        
    def __call__(self):
        r"""
            呼び出し設定
        """
        pass
    
    def timelineJsonUrl(self):
        r"""
            ツイッタータイムラインのjsonデータを取得
        """
        return 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    
    def emojiExclusion(self,w):
        r"""
            ツイートのテキスト情報に絵文字のパターンがある場合は
            それを除去してテキストを返す
        """
        text = w.encode('unicode_escape')
        rr   = re.findall('U00\w{6}',text)
        if rr:
            for r in rr:
                ckw  = '\\{}'.format(r)
                text = text.replace(ckw,'')
        return text.decode('unicode_escape')
        
    ## ------------------------------------------------------------------------
    ## token key method
    
    def getApiData(self):
        r"""
            ツイッターAPIキー情報を取得
        """
        return self.TWITTER.getApiInfo()
    
    def getTwitterApiData(self,key=None,full=False):
        r"""
            キーリスト情報に応じたツイッターAPIのトークンキーを取得
        """
        returndict = {}
        twapilist  = self.getApiData()
        targetlist = (['CK','CS','AT','ATS']
            if not key else [key]
            if isinstance(key,bytes) else key
            if isinstance(key,list)  else []
        )
        for t in targetlist:
            info = twapilist.get(t)
            if not info:
                print(u'> Key acquisition error:')
                print(u'\t指定キー"{}"で'
                      u'情報が取得できませんでした。'.format(t))
                continue
            returndict.update({t:info})
        return returndict.get(key) if not full else returndict
    
    def getAllAPI(self):
        r"""
            apiすべてのトークンを取得
        """
        return self.getTwitterApiData()
    
    def getIndividualAPI(self,key,full=True):
        r"""
           指定したキーのトークンを取得
        """
        return (self.getTwitterApiData(key)
            if not full else self.getTwitterApiData(key).get(key))
    
    def getConsumerKeyAPI(self,full=False):
        r"""
            CONSUMER_KEYのトークンを取得
        """
        return self.getTwitterApiData('CONSUMER_KEY',full)
    
    def getConsumerSecretAPI(self,full=False):
        r"""
            CONSUMER_SECRETのトークンを取得
        """
        return self.getTwitterApiData('CONSUMER_SECRET',full)
    
    def getAccessTokenAPI(self,full=False):
        r"""
            ACCESS_TOKENのトークンを取得
        """
        return self.getTwitterApiData('ACCESS_TOKEN',full)
    
    def getAccessTokenSecretAPI(self,full=False):
        r"""
            ACCESS_TOKEN_SECRETのトークンを取得
        """
        return self.getTwitterApiData('ACCESS_TOKEN_SECRET',full)
    
    ## ------------------------------------------------------------------------
    ## api method
    
    def getTwiiterApiData(self,type='1'):
        r"""
            トークンキーを入力しAPIデータを取得
            type = 1: tweepy
            type = 2: OAuth1Session
        """
        pass
        
    def getTwiiterApiDataType1(self):
        r"""
            tweepyを使用し認証データを取得
        """
        try:
            import tweepy
        except:
            print('*'*80)
            traceback.print_exc()
            print('*'*80)
            return
            
        auth = tweepy.OAuthHandler(
            self.getConsumerKeyAPI(),self.getConsumerSecretAPI())
        auth.set_access_token(
            self.getAccessTokenAPI(),self.getAccessTokenSecretAPI())
        api = tweepy.API(auth_handler=auth)
        return api
        
    def getTwiiterApiDataType2(self):
        r"""
            OAuth1Sessionを使用し認証データを取得
        """
        try:
            from requests_oauthlib import OAuth1Session
        except:
            print('*'*80)
            traceback.print_exc()
            print('*'*80)
            return
            
        twitter = OAuth1Session(
            self.getConsumerKeyAPI(),self.getConsumerSecretAPI(),
            self.getAccessTokenAPI(),self.getAccessTokenSecretAPI()
        )
        return twitter
    
    def getTimeLineData(self,count=10):
        r"""
            タイムライン情報を取得
        """
        twitter = self.getTwiiterApiDataType2()
        url     = self.timelineJsonUrl()
        params = {
            'count' : count
        }
        res = twitter.get(url,params=params)
        if res.status_code==200:
            return json.loads(res.text)
        else:
            print('Failed: %d'%res.status_code)
    
    ## ------------------------------------------------------------------------
    ## other method
    
    def getText(self):
        r"""
        """
        timelines  = self.getTimeLineData()
        return [self.emojiExclusion(l['text']) for l in timelines]
    
###############################################################################
## other

## タイムラインのテキストをPythonで読み込める状態にしてプリント
# t=MsTwitter()
# for w in t.getText():
    # print(w)

###############################################################################
