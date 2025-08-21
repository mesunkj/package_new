# _*_ coding:utf-8 _*_


import pandas as pd
import sys, os
import subprocess
from io import StringIO
import random

try:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
finally:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait


from urllib.parse import urlparse

# ref https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/3/
from bs4 import BeautifulSoup as bsO
import re

from PIL import Image
import requests
from io import BytesIO
from IPython.display import display  # to display images

import time

import urllib.request as ulib

# from urlparse import urlparse
from os.path import splitext, basename

from urllib.request import urlopen
import itertools

sys.path.append("/content/drive/My Drive/app/Package/new/")
# os.chdir('/content/drive/My Drive/app/Package/new/')
# from ixFileP import fileP as _fp, fAddress as _fAdd  # fp# fAddress as  _fAdd
from ixStockProperty import USProperty
from ixMisc import datetimeUtils as dt, utils
from methods import *

# fAdd = _fAdd()
# fp = _fp()
_P = USProperty()
gP = None
_dU = dt()

# hm = Net.htmlFile()
class Net:
    hm = None

    def __init__(self):
        # print('in net')
        self.hm = Net.htmlFile()
        pass

    class htmlFile:
        def readUrlAsHtml(self, url, decode="utf-8"):
            # url = r'https://en.wikipedia.org/wiki/Python_(programming_language)'
            html = urlopen(url)
            doc = html.read().decode(decode, "ignore")
            return doc

        def requestText(self, url):
            r = self.request(url)
            return StringIO(r.text).getvalue()

        def request(self, url):
            return requests.post(url)

        def coDataFormUrlRequest(self, url, decode="utf-8"):  # decode like ['big5','utf-8' ]
            return urlopen(url).read().decode(decode, "ignore")

        def catchUrlNew(self, url, decode="utf-8"):
            try:
                html = urlopen(url, timeout=5)
                doc = html.read().decode(decode, "ignore")
                return doc
            except ConnectionResetError:
                print("==> ConnectionResetError")
                pass
            # except timeout:
            #     print("==> Timeout")
            #     pass
            return None

    def getURL(self, url, decode="utf-8", func=None):
        """funcS: ['request , requestText']"""
        # if(self.hm  is None): self.hm = htmlFile()
        # hm = self.hm
        if func is None:
            return self.hm.readUrlAsHtml(url, decode)
        if func == "request":
            return self.hm.request(url)

        if func == "requestText":
            return self.hm.requestText(url)
        return None


class netApp:
    # session requests
    session = None

    def __init__(self):
        self.session = None

    def connectSession(self):
        # global session
        self.session = requests.Session()

    def closeSession(self):
        # global session
        self.session.close(self)

    def getUserAgent(self, id_=-1):
        if id_ < 0:
            id_ = random.randint(0, len(_P.user_agent) - 1)
        return _P.user_agent[id_]

    def getUrlContent(self, url, id_=-1):

        req = self.getUrlrequest(url=url, id_=id_)
        req.encoding = req.apparent_encoding
        time.sleep(1)
        return req.text

    def getUrlContent_v(self, url, id_=-1):

        req = self.getUrlrequest(url=url, id_=id_)
        req.encoding = req.apparent_encoding
        time.sleep(1)
        return req, req.text

    def doRequest(self, url, tryAgain=True, tryC=3):
        ic = 0
        err = ""
        while ic < tryC:
            try:
                return self.getUrlrequest(url)
            except Exception as e:
                self.closeSession()
                err = "Fail to request, due to " + str(e)

                if not tryAgain:
                    return None, err
                ic += 1
                time.sleep(30)
        return None, "up tp Max try connection " + str(tryC) + ", due to " + err
    def doRequest_post(self, url,header,data_json, tryAgain=True, tryC=3):
        ic = 0
        err = ""
        while ic < tryC:
            try:
                return self.getUrlrequest_post(url,header,data_json)
            except Exception as e:
                self.closeSession()
                err = "Fail to request, due to " + str(e)

                if not tryAgain:
                    return None, err
                ic += 1
                time.sleep(30)
        return None, "up tp Max try connection " + str(tryC) + ", due to " + err

    def getUrlrequest(self, url, id_=-1):
        # global session
        if self.session is None:
            self.connectSession()
        # user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        accept = "text/html,application/xhtml+xml,application/xml;" "q=0.9,image/webp,*/*;q=0.8"
        if id_ < 0:
            id_ = random.randint(0, len(_P.user_agent) - 1)
        user_agent = self.getUserAgent(id_)
        headers = {"User-Agent": user_agent, "Accept": accept}

        req = self.session.get(url, headers=headers)
        return req
    def getUrlrequest_post(self, url,header,data_json, id_=-1):
        # global session
        if self.session is None:
            self.connectSession()
        # # user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        # accept = "text/html,application/xhtml+xml,application/xml;" "q=0.9,image/webp,*/*;q=0.8"
        # if id_ < 0:
        #     id_ = random.randint(0, len(_P.user_agent) - 1)
        # user_agent = self.getUserAgent(id_)
        headers = header

        req = self.session.get(url, headers=headers,  json=data_json)
        return req

    def is_url_validate(self, url):
        req = self.getUrlrequest(url)
        if req.status_code == 200:
            return True
        return False

    def downloadfromUrl(self, url, fpath):
        req = self.doRequest(url)
        open(fpath, "wb").write(req.content)
        print("done to download", fpath)


# nt_ = netApp()



def htmlURLSimpleCodeCvt(url):
    return url.replace("%3A", ":").replace("%2F", "/")


def findPageCount(fwC, parserf, ptype, divClass="page both"):
    oo1 = fwC.getAllFrTagName(tagName="div", clsName=divClass)
    count = 0
    # try:
    if len(oo1) > 0:
        oo2 = fwC.getAllFrTagName(tagName="li", iObj=oo1[0])
        if len(oo2) > 0:
            # get a href at last element
            oo3 = fwC.getAllFrTagName(tagName="a", iObj=oo2[-1])
            if len(oo3) > 0:
                # get href
                # print(type(oo3), 'oo3[0] ',oo3[0])
                hf_ = oo3[0]["href"]
                # print(type(hf_), hf_)
                # analysis like <a href="/aiss/index_155.html">尾页</a>
                count = parserf(p=ptype, val=hf_)  # int(hf_.split('_')[1].split('.')[0])
    # except Exception as e: print('error occure , due to : ',e)
    return count


def lastParseF(p, val):
    if p == "main":
        return int(val.split("_")[1].split(".")[0])
    # if(p=='model_main'):return int(val.split('_')[1].split('.')[0])
