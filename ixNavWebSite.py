# _*_ coding:utf-8 _*_

import os
import pandas as pd
import json
import sys, os, json
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

# ref https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/3/
from bs4 import BeautifulSoup as bsO
import re

from PIL import Image
import requests, io
from io import BytesIO
from IPython.display import display  # to display images

from datetime import datetime

from urllib.parse import urlparse, urljoin
import urllib.request as ulib

# from urlparse import urlparse
from os.path import splitext, basename

import itertools
from base64 import b64decode

sys.path.append("/content/drive/MyDrive/app/Package/new")
from ixFileP import fAddress as _fAdd, fileP as fileOPR
from methods import *
from ixNet import netApp
from ixImage import ims

# gP = _gP()
try:
    fp = fileOPR()
    fp_ = fp
    nt_ = netApp()
    fAdd = _fAdd()
except:
    pass


class google:
    driver = None
    recordDf = None

    class gApp:
        def q_Google(self, query, pics=None, start=0, scroll=True, xL=None):
            gP = google()
            # query = r"sexy girls korean"
            addr = "https://www.google.co.in/search?q=" + query.replace(" ", "+") + "&source=lnms&tbm=isch"

            key = "googleSearch_" + query.replace(" ", "").capitalize()
            pDir = "graspOut_1"
            dirp = fp.getAllPath(key, parentDirName=pDir)
            retFCC = {}
            errorC = []

            # get driver
            driver = gP.initPCDriver(webAddr=addr, waittime=1, initRecord=True)

            # scroll window to find all hided pics
            if scroll:
                gP.widowFreeScroll(driver)  # , waitTime = 0.25
            # get bs4 obj
            bsObj = gP.getBsObj(driver=driver)
            xC = {"driver": driver, "bsObj": bsObj}

            # find frame
            frmeL = xC["bsObj"].find_all("div", {"jsname": "r5xl4", "class": "islrc"})
            # find inner within frame
            vCTag = frmeL[0].find_all("img", {"class": "rg_i Q4LuWd tx8vtf"})
            # gP.getTag_bs4(xC['bsObj'] , tag = 'img', iprint = False)
            cnt = -1
            # start = 0

            for tag in vCTag:
                cnt += 1
                if cnt < start:
                    continue
                if cnt in errorC:
                    continue
                # if(cnt> start+ 2):    break
                if xL is not None and len(xL) > 0:
                    if cnt not in xL:
                        continue
                if pics is not None:
                    if cnt > pics:
                        break

                print("\rEpoch {}/{}".format(cnt, len(vCTag)), end="", flush=True)
                # src =tag.get('src')
                xpath = gP.xpath_soup(tag)

                try:
                    selenium_element = xC["driver"].find_element_by_xpath(xpath)
                    selenium_element.click()
                    time.sleep(5)

                except:
                    print("error", cnt)
                    errorC.append([cnt, tag.get("alt")])
                    continue
                try:
                    oxpath = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img'
                    selenium_element_o = xC["driver"].find_element_by_xpath(oxpath)
                    src = selenium_element_o.get_attribute("src")
                    title = selenium_element_o.get_attribute("alt")

                except:
                    print("error selenium_element_o", cnt)
                    errorC.append([cnt, tag.get("alt")])
                    continue

                selenium_element.click()

                if src in retFCC:
                    continue
                xname = "_".join([key, gP.getNowDateTimeStr()]) + ".png"
                fname = os.path.join(dirp, xname)
                retFCC[src] = fname

                # download the image
                if not gP.isDowLoaded(src):
                    try:
                        if not gP.ulib_save(src, fname, iprint=None):
                            print("in ulib false")
                            if not gP.google_data_save(fname, src, iprint=None):
                                print("in google_data_save false")
                                if not gP.request_data_save(fname, src, iprint=None):
                                    print("in request_data_save false")
                                    raise
                        gP.appendRecord(src, title, dirp, xname)
                        continue
                    except:
                        print("error download", cnt)
                        errorC.append([cnt, title, src])
                break
            gP.saveRecord()
            return driver, errorC

        def google_seagch_save(self, gP, urls, key="sexy", pDir="graspOut", iprint=False):
            cnt = 0
            dirp = fp.getAllPath(key, parentDirName=pDir)
            for datai in urls:
                fname = os.path.join(dirp, "_".join([key, gP.getNowDateTimeStr()]) + ".png")
                # check p1
                if gP.google_data_save(fname, datai, iprint=iprint):
                    continue
                # check p2
                imgs, urlsR, errPic = gP.getURLimagePIL([urls], limitSize=1024 * 5, show=False, iprint=False)
                if len(imgs) > 0:
                    if gP.saveImgsPIL(fname, imgs[0], iprint=iprint):
                        continue

                if iprint:
                    print("\nFail to save: url", datai)

        def getPhoto(
            self, addr, driver=None, bsObj=None, urls=None, options={"dirP": "graspOut", "bsObj": True, "urls": {"tag": {"tagName": "img", "srcName": "src"}, "link": True, "img": True, "save": True,},},
        ):
            if driver is None:
                driver = self.initPCDriver(webAddr=addr, waittime=1)
            # create bs4
            if not options["bsObj"]:
                return {"driver": driver}
            if bsObj is None:
                bsObj = self.getBsObj(driver=driver)
            if not options["urls"]["link"]:
                return {"driver": driver, "bsObj": bsObj}
            tagName = options["urls"]["tag"]["tagName"]
            srcName = options["urls"]["tag"]["srcName"]
            if urls is None:
                urls = self.getImagesLink_bs4(bsObj, tagName=tagName, srcName=srcName)

            # get url images
            # def getURLimagePIL(self, urls, limitSize = 1024* 5 , show = False): # url like array
            if not options["urls"]["img"]:
                return {"driver": driver, "bsObj": bsObj, "urls": urls}
            imgsC, urlsR, errPic = self.getURLimagePIL(urls, show=False, iprint=False)
            print("find count of images", len(imgsC))
            if len(imgsC) == 0:
                return {"driver": driver, "bsObj": bsObj, "urls": urls}
            # show images
            # self.showimagePIL(imgsC)
            # get filename
            filenames = self.getfnameFromWebAddress(urlsR)
            # get dir
            parentDirName = options["dirP"]  #'graspOut'
            title = self.getHtmlTitle_bs4(bsObj)  # , tag ='title')
            print("title", title)
            dirName = title
            dirp = fp.getAllPath(dirName, parentDirName=parentDirName)
            # save
            if options["urls"]["save"]:
                self.saveImgsPIL(dirName, filenames, imgsC)
            return {
                "driver": driver,
                "bsObj": bsObj,
                "urls": urls,
                "imgsC": imgsC,
                "urlsR": urlsR,
                "errPic": errPic,
                "filenames": filenames,
            }

        def updatePage_FB(self, xC):
            # obj,urls
            addr = xC
            driver = xC["driver"]
            bsObj = None
            urls = None
            options = {
                "bsObj": True,
                "urls": {"tag": {"tagName": "img", "srcName": "src"}, "link": True, "img": False, "save": True,},
            }
            xC = self.getPhoto(addr, driver=driver, bsObj=bsObj, urls=urls, options=options)

            # modify urls
            urls = [x.replace("S_", "") for x in xC["urls"] if "S_" in x]
            len(urls)

            # save
            driver = xC["driver"]
            bsObj = xC["bsObj"]
            urls = urls  # xC['urls']
            options = {
                "bsObj": True,
                "urls": {"tag": {"tagName": "img", "srcName": "src"}, "link": True, "img": False, "save": False,},
            }
            xC = self.getPhoto(addr, options=options, driver=driver, bsObj=bsObj, urls=urls)

            # driver.page_source
            return xC

    def initDf(
        self, dirp="graspOut", fname="search.csv", columns=["url", "title", "folder", "fname"],
    ):
        if self.recordDf is None:
            try:
                self.recordDf = pd.read_csv(os.path.join(dirp, fname))
            except:
                pass
            if self.recordDf is None:
                self.recordDf = pd.DataFrame(columns=["url", "title", "folder", "fname"])

    def isDowLoaded(self, url):
        try:
            if self.validators.url(url):
                df1 = self.recordDf[self.recordDf["url"] == url]
                if df1 is not None and len(df1) > 0:
                    return True
        except:
            pass
        return False

    def appendRecord(self, url, title, folder, fname):
        df1 = pd.DataFrame([{"url": url, "title": title, "folder": folder, "fname": fname}])
        self.recordDf = self.recordDf.append(df1, ignore_index=True)

    def saveRecord(self, dirp="graspOut", fname="search.csv"):
        self.recordDf.to_csv(os.path.join(dirp, fname), index=False)

    def getDriver(self):
        return self.driver

    def changUrl(self, url):
        self.driver.get(url)

    def initDriver(self, webAddr="", waittime=20):
        if self.driver is None:
            # set options to be headless, ..
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            # open it, go to a website, and get results
            # wd = webdriver.Chrome("chromedriver", options=options)
            wd = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(wd, waittime)
            self.driver = wd
        if webAddr is not None and len(webAddr) > 0:
            self.getHtmlContent(self.driver, webAddr)
        return self.driver

    def initPCDriver(self, webAddr="", waittime=20, initRecord=True):
        if self.driver is None:
            # set options to be headless, ..
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            # open it, go to a website, and get results
            wd = webdriver.Chrome("chromedriver")
            wait = WebDriverWait(wd, waittime)
            self.driver = wd

        if webAddr is not None and len(webAddr) > 0:
            self.getHtmlContent(self.driver, webAddr)
        if initRecord:
            self.initDf()
        return self.driver

    def getHtmlContent(self, driver, webAddr):
        # driver = wd
        isM = self.IsURL(webAddr)
        # print("in", "webaddr", webAddr, "isMatch", isM)
        if not isM:
            return
        driver.get(webAddr)  # 連線至指定的網頁
        # print("done to getHtmlContent")

    def getBsObj(self, driver=None, content=""):
        if driver is not None:
            return bsO(driver.page_source, features="html.parser")  # , "html5lib")
        if len(content) > 0:
            return bsO(content)
        return None
        # print(wd.page_source)  # results
        # driver.quit()

    def getTag_bs4(self, bsObj, tag="", iprint=False):
        a_tags = bsObj.find_all(tag)
        if iprint:
            for tag in a_tags:
                # 輸出超連結的文字
                print(type(tag), tag.text)
        return a_tags

    def getAttr_bs4(self, obj, attr=None, iprint=False):
        # obj: bs or tag,  attr ={attrName: value} ex. {'class' , 'ep_23'}
        eles = obj.find_all(attrs=attr)

        if iprint:
            for tag in eles:
                # 輸出超連結的文字
                print(type(tag), tag.text)
        return eles

    def getHtmlTitle_bs4(self, bsObj, tagName="title"):
        rr = self.getTag_bs4(bsObj, tag=tagName)
        # return rr
        if (rr is not None) or len(rr) > 0:
            return self.strip_control_characters(rr[0].text)
        return "temp"

    def getImagesLink_bs4(self, bsObj, tagName="img", srcName="src"):
        vCTag = self.getTag_bs4(bsObj, tag=tagName, iprint=False)
        urls = []
        for tag in vCTag:
            # 輸出超連結的文字
            # print(type(tag),tag.text, tag.get('src'))
            urls.append(tag.get(srcName))
        return urls

    def strip_control_characters(self, s):
        word = ""
        for i in s:
            if not (ord(i) < 48 or (ord(i) in range(91, 97)) or (ord(i) in range(123, 128))):
                word += i
        return word

    def xpath_soup(self, element):
        """
        Generate xpath of soup element
        :param element: bs4 text or node
        :return: xpath as string
        """
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:
            """
            @type parent: bs4.element.Tag
            """
            previous = itertools.islice(parent.children, 0, parent.contents.index(child))
            xpath_tag = child.name
            xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
            components.append(xpath_tag if xpath_index == 1 else "%s[%d]" % (xpath_tag, xpath_index))
            child = parent
        components.reverse()
        return "/%s" % "/".join(components)

    def IsURL(self, str_url):
        return True
        strRegex = "^((https|http|ftp|rtsp|mms)?://)" + "?(([0-9a-zA-Z_!~*'().&=+$%-]+: )?[0-9a-zA-Z_!~*'().&=+$%-]+@)?" + "(([0-9]{1,3}.){3}[0-9]{1,3}" + "|" + "([0-9a-zA-Z_!~*'()-]+.)*" + "([0-9a-zA-Z][0-9a-zA-Z-]{0,61})?[0-9a-zA-Z]." + "[a-z]{2,6})" + "(:[0-9]{1,4})?" + "((/?)|" + "(/[0-9a-zA-Z_!~*'().;?:@&=+$,%#-]+)+/?)$"
        # ref = re.compile(strRegex)
        isM = re.match(strRegex, str_url)
        # re.test()
        if isM:
            return True  # //符合
        else:
            return False
            # //不符合

    def fetch_imagef(url, fname=None, path=None, tryAgain=True, tryC=3):
        fname = "test_src" + "_" + getNowDateTimeStr(format="%y%m%d_%H%M%S") if fname is None else fname
        if path is not None:
            fname = os.path.join(path, fname)
        req = nt_.doRequest(url)
        err = None
        img = None
        if req.status_code == 200:
            im = BytesIO(req.content)
            img = Image.open(im)
            img.save(fname)

        else:
            print("fail to fetch url", url, "\nerror at: ", req)
        return img

    #   print('done')
    def getURLimagePIL(self, urls, limitSize=1024 * 5, show=False, iprint=False):  # url like array
        imgs = []
        cnt = 0
        urlsR = []
        errPic = []
        for url in urls:
            """
            if(not self.IsURL(url)):
                print('invalidate url',url)
                continue
            """
            try:
                response = requests.get(url)
                im = BytesIO(response.content)
                image_file_size = sys.getsizeof(im.getvalue())  # im.tell()
            except Exception as e:
                if iprint:
                    print("invalidate url", url, "due to:", e)
                errPic.append([url, e])
                continue

            if iprint:
                print(cnt, url)
                cnt += 1
                print("image_file_size", image_file_size, "limitSize", limitSize)
            img = Image.open(im)
            if image_file_size > limitSize:
                imgs.append(img)
                urlsR.append(url)
            if show:
                self.showimagePIL(img)
        return imgs, urlsR, errPic

    def showimagePIL(self, imgs):
        for img in imgs:
            display(img)

    def saveImgsPIL(self, dirP, filenames, imgs, iprint=True):
        if iprint:
            print("save processing...")
        dirP = fAdd.getDir(dirP)
        for imIdx in range(0, len(imgs)):
            fname = os.path.join(dirP, filenames[imIdx][2])
            self.saveImgPIL(fname, imgs[imIdx], iprint=iprint)
        if iprint:
            print("done to save")

    def saveImgPIL(self, fname, img, iprint=True, formatP="png"):
        try:
            imgx = img.save(fname, formatP)
            return True
        except:
            if iprint:
                print("\nFail to save", fname)
            pass
        return False

    def ulib_save(self, url, fname, iprint=True):
        try:
            r, cm = ulib.urlretrieve(url, fname)
            return True
        except Exception as e:

            # opener = urllib.request.URLopener()
            # opener.addheader('User-Agent', net_.getUserAgent())
            # filename, headers = opener.retrieve(url, 'Test.pdf')
            # raise Exception(e)
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-Agent", getUserAgent())]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, fname)

            if iprint:
                print("\nFail to save", url, fname, ",due to ", e)
            pass
        return False

    def request_data_save(self, fname, url, iprint=True):
        try:
            r = requests.get(url)
            with open(fname, "wb") as outfile:
                outfile.write(r.content)
            return True
        except:
            if iprint:
                print("\nFail to save", url, fname)
            pass

        return False

    def google_data_save(self, fname, data, iprint=True):
        try:
            header, encoded = data.split(",", 1)
            data = b64decode(encoded)
            im = BytesIO(data)
            image_file_size = sys.getsizeof(im.getvalue())
            with open(fname, "wb") as f:
                f.write(data)
            return True
        except:
            if iprint:
                print("\nFail to save", fname)
            pass

        return False

    def getfnameFromWebAddress(self, urls):
        xpath = []
        for url in urls:
            picture_page = url  # "http://distilleryimage2.instagram.com/da4ca3509a7b11e19e4a12313813ffc0_7.jpg"
            disassembled = urlparse(picture_page)
            filename, file_ext = splitext(basename(disassembled.path))
            # a1 = "_".join([filename, _dU.getNowDateTimeStr()])
            xpath.append([filename, file_ext, "".join([filename, file_ext])])
            # print(filename, file_ext)
        return xpath

    def widowFreeScroll(self, driver, waitTime=0.25, print_=True):
        if print_:
            print("start to scroll")
        part = 2
        ht = 1080
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            for Y_ in range(1, int(ht / part)):
                Y = Y_ * 250  # int( Y_ * (ht /part) )
                # print(Y_, Y)
                sj = "window.scrollTo(0," + str(Y) + " )"
                # xC['driver'].execute_script("window.scrollTo(0, Y)")
                driver.execute_script(sj)
                time.sleep(waitTime)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if Y > new_height:
                    break
                last_height = new_height
            if new_height == last_height:
                break
        if print_:
            print("scroll done")

    def window_scroll(self, driver, waitTime=5, nextto=-1):
        # nextto: count for scroll_down
        SCROLL_PAUSE_TIME = waitTime

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        # print('in Height ',last_height)
        cnt = 0
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            # print('Height after scrollTo ',new_height)

            print("\rscroll Epoch {} height {}/{}".format(cnt + 1, last_height, new_height), end="", flush=True)
            if new_height == last_height:
                break

            last_height = new_height
            cnt += 1
            if nextto > 0 and nextto <= cnt:
                break
            # print(f'process for scroll {cnt}/{nextto}')
        print("\ndone to scroll")

    def window_scroll_by_step(self, driver, waitTime=5, nextto=-1):
        rcc = {}
        # nextto: count for scroll_down
        SCROLL_PAUSE_TIME = waitTime

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        # print('in Height ',last_height)
        cnt = 0
        rcc[-1] = driver.page_source
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            rcc[cnt] = driver.page_source

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            # print('Height after scrollTo ',new_height)

            print("\rscroll Epoch {} height {}/{}".format(cnt + 1, last_height, new_height), end="", flush=True)
            if new_height == last_height:
                break

            last_height = new_height
            cnt += 1
            if nextto > 0 and nextto <= cnt:
                break
        print("\ndone to scroll")
        return rcc
    def fetch_imagef(self, url, fname=None, path=None, tryAgain=True, tryC=3):
        fname = "test_src" + "_" + getNowDateTimeStr(format="%y%m%d_%H%M%S") if fname is None else fname
        if path is not None:
            fname = os.path.join(path, fname)
        req = nt_.doRequest(url)
        err = None
        img = None
        if req.status_code == 200:
            im = BytesIO(req.content)
            img = Image.open(im)

            extension = os.path.splitext(fname)

            if extension == "png":
                img.save(fname, "PNG")
            else:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(fname, "JPEG")
            # img.save(fname)

        else:
            print("fail to fetch url", url, "\nerror at: ", req)
        return img
        #   print('done')

    def g_screenShot_driver(self):
        imp = self.driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(imp))
        image.save("test.png")


class navWebSite(google):
    def __init__(self, url=None, connect=False):
        super(navWebSite, self).__init__()  # 呼叫父類別__init__()
        if connect:
            self.initObj(url)
        

    def g_driver(self, refresh=True):
        if self.driver is None or refresh:
            self.initDriver(webAddr=None, waittime=20)
        return self.driver

    def initObj(self, url):
        self.imgslink = []
        self.bsObj = None
        self.xObj = None
        self.webUrl = None
        self.dnload = False
        self.downloadC = {}
        # get driver
        self.g_driver()

        # print('1')
        # get bs4 obj
        if url is None:
            return
        else:
            self.getHtmlContent(self.driver, url)
        # print('2 , ',url)
        bsObj = bsO(self.driver.page_source, features="html.parser")  # self.getBsObj(driver = self.driver)
        # print('3 bsObj')
        # self.driver = driver
        self.bsObj = bsObj
        self.xObj = {"driver": self.driver, "bsObj": bsObj}
        self.webUrl = url
        # self.home =   'https://deepfakesporn.com/'

    def setObjByTest(self, oo_):
        self.xObj = oo_

    def navUrl(self, url):
        # if(self.driver.current_url == url): return
        self.initObj(url)

    def getAllFrTagName(self, iObj=None, tagName="a", idNamd=None, clsName=None, attr=None):
        if iObj is None:
            iObj = self.bsObj
        if clsName is not None:
            return iObj.find_all(tagName, {"class": clsName})
        if idNamd is not None:
            return iObj.find_all(tagName, {"id": idNamd})
        if attr is not None:
            return iObj.find_all(tagName, attr)
        # print ('\nthe function you request which find id or class is not work yet.')

        return iObj.find_all(tagName)

    def getSrc(self, tag, scope=None):
        # scope =str , which source is included by it
        if (scope is None) or (scope is not None and len(scope) > 0 and tag["src"].index(scope) >= 0):
            return tag["src"]
        return None

    def getImsLink(self):
        return self.imgslink

    def getallImagesLink(self, tagName="img", scope=None, idNamd=None, clsName=None, url=None, refresh=False, filter=[], host=None):
        if refresh and url is not None:
            self.navUrl(url)
        if self.bsObj is None:
            raise Exception("initial error, driver or bs object")
        tagL = self.getAllFrTagName(tagName=tagName, idNamd=idNamd, clsName=clsName)
        self.imgslink = []
        for t_ in tagL:
            imsrc = self.getSrc(t_, scope=scope)
            if imsrc is not None:
                if host is not None:
                    imsrc = host + imsrc
                self.imgslink.append(imsrc)
        self.imgslink = list(set(self.imgslink))
        print("\ndone to get all images src, found %d, from url %s", len(self.imgslink), self.webUrl)

        if len(filter) > 0:
            self.filterLink(scopes=filter, printOriginal=True)

    def filterLink(self, scopes=[], printOriginal=False):
        if len(scopes) == 0:
            return
        tmpC = []
        for imlk_ in self.imgslink:
            chk = True
            for sc_ in scopes:
                if imlk_.find(sc_) < 0:
                    chk = False
                if not chk:
                    break
            if chk:
                tmpC.append(imlk_)
        print("\ndone to filter scopes=", scopes, " original count ", len(self.imgslink), " after filter count ", len(tmpC))
        if printOriginal:
            print("\nprintOriginal: \n", self.imgslink)
        self.imgslink = tmpC

    def dnloadImages(self, prnp=False, urls_=None, urls_name=None):  # done_ = list() record file name in same folder
        try:
          if self.dnload:
              print("already done to download")
              return
        except:pass
        urls = self.imgslink if urls_ is None else urls_
        urls_name = urls if urls_name is None else urls_name
        self.tmpNameC = self.getfnameFromWebAddress(urls_name)
        self.tmpImgC = getImagesFromUrl(urls)
        for n_ in range(len(self.tmpNameC)):
            if prnp:
                print("\r current item/ total items  {}/{}".format(n_, len(self.tmpNameC)), end="", flush=True)
            key = self.tmpNameC[n_][2] if ("jpg" in self.tmpNameC[n_][2]) else "f" + "_" + getNowDateTimeStr(format="%y%m%d_%H%M%S%f") + ".jpg"
            # if(done_ is not None and key in done_): continue
            try:
                # self.downloadC[key] = ims(image=self.tmpImgC[n_], name=key, url=urls[n_])
                self.downloadC[key] = ims(fname=key, path=urls[n_])
            except Exception as e:
                print("\nerror occ at download... , ", e, "\n")
                pass

        if len(self.downloadC) > 0:
            self.dnload = True
        print("\ndone to download {} images, ".format(len(list(self.downloadC.keys()))))

    def showAllIms(self, figSize=(20, 15), imageSize=(200, 200), columns=3, rows=5):
        self.dnloadImages()
        cnt = 1
        for k_ in self.downloadC:
            ims_ = self.downloadC[k_]
            print("%d  fname %s, src %s ", cnt, ims_.get_name(), ims_.get_url())
            cnt += 1
        images = self.get_all_images()
        plot_images_with_np(images, figSize=figSize, imageSize=imageSize, columns=columns, rows=rows)

    def get_all_images(self):
        r_ = []
        for k_ in self.downloadC:
            ims_ = self.downloadC[k_]
            r_.append(ims_.get_img())
        return r_

    def saveImgs(self, path, fnames=[]):
        fp_.creatFolder(path)
        err_=[]
        for idx,k_ in enumerate(self.downloadC):
            ims_ = self.downloadC[k_]
            if len(fnames) > 0 and ims_.get_name not in fnames:
                continue
            path_ = os.path.join(path, ims_.get_name())
            if(os.path.isfile( path_ )):continue
            # cv2.imwrite(path, ims_.get_img)
            try:
                ims_.get_img().save(path_, "JPEG")
            except Exception as e:
                err_.append([idx,k_])
                # print(f"\nerror at save {k_}, caused by {e}")
            print("\rEpoch idx/count {}/{} err {}".format(idx + 1, len(self.downloadC), len(err_)), end="", flush=True,)
        # print("\ndone to save images to ", path)
        if(len(err_)>0):
            print(f'there are {len(err_)} errors found,\n{err_}')


class mInfo:  # model info
    def _init_(self):
        self.title = None
        self.navUrl = None
        self.imageTitle = None
        self.imHref = None
        self.mslike = []

    def setP(self, p, val):
        if p == "title":
            self.title = val
        if p == "href":
            self.navUrl = val
        if p == "imTitle":
            self.imageTitle = val
        if p == "imLink":
            self.imHref = val
        if p == "imsLink":
            self.mslike = val

    def getP(self, p):
        if p == "title":
            return self.title
        if p == "href":
            return self.navUrl
        if p == "imTitle":
            return self.imageTitle
        if p == "imLink":
            return self.imHref
        if p == "imsLink":
            return self.mslike

    def _prn(self, sub=False):
        if not sub:
            print(" [ 'title': {}, 'href': {}, 'imTitle': {},'imLink': {}] ".format(self.title, self.navUrl, self.imageTitle, self.imHref))
            for s in self.mslike:
                s._prn(sub=False)
        else:
            print(" [   'imTitle': {},'imLink': {}] ".format(self.imageTitle, self.imHref))


def collectMInfo(fwC, mLC, mainUrl_=None):
    # mLC : model list collect for page

    # bs_tag_div_list
    mL = fwC.getAllFrTagName(tagName="div", clsName="item")
    for t_ in mL:
        mL_ = mInfo()
        title = ""
        oo1 = fwC.getAllFrTagName(tagName="a", iObj=t_)
        if len(oo1) > 0:
            mL_.setP(p="title", val=oo1[0]["title"])
            title = mL_.getP(p="title")
            href_ = oo1[0]["href"] if mainUrl_ is None else mainUrl_ + oo1[0]["href"]
            mL_.setP(p="href", val=href_)
            oo2 = fwC.getAllFrTagName(tagName="img", iObj=oo1[0])
            if len(oo2) > 0:
                mL_.setP(p="imTitle", val=oo2[0]["alt"])
                href_ = oo2[0]["src"] if mainUrl_ is None else mainUrl_ + oo2[0]["src"]
                mL_.setP(p="imLink", val=href_)
                mL_.setP(p="imsLink", val=[])
        # last
        if "title" == "":
            mLC["err"].append(t_)
        else:
            mLC["R"][title] = mL_


def collectMInfoDetail(fwC, mInfoC, mainUrl_=None):
    # mInfoC : for each model, type is mInfo

    # bs_tag_div_list
    mLC_ = fwC.getAllFrTagName(tagName="div", clsName="arcBody")
    for t_ in mLC_:

        oo2 = fwC.getAllFrTagName(tagName="img", iObj=t_)
        for im in oo2:
            mL_ = mInfo()
            mL_.setP(p="imTitle", val=im["alt"])
            href_ = im["src"] if mainUrl_ is None else mainUrl_ + im["src"]
            mL_.setP(p="imLink", val=href_)
            mL_.setP(p="imsLink", val=[])
            mL_.setP(p="title", val="")
            mL_.setP(p="href", val="")
            mInfoC.mslike.append(mL_)


class q_GoogleC(navWebSite):
    def __init__(self, url=None, connect=False):
        super(q_GoogleC, self).__init__(url, connect=connect)  # 呼叫父類別__init__()
        # self.initObj(url)

    def getBSOObj(self):
        return bsO(self.driver.page_source, features="html.parser")

    def findAllTag(self, iObj=None, tagName="a", idNamd=None, clsName=None, attr=None):
        return self.getAllFrTagName(iObj=iObj, tagName=tagName, idNamd=idNamd, clsName=clsName, attr=attr)

    def doAction(self, tag, delay=2, google_xpath=None):
        xpath = self.xpath_soup(tag)
        src = None
        try:
            selenium_element = self.driver.find_element(By.XPATH, xpath)
            selenium_element.click()
            time.sleep(delay)

        except Exception as e:
            print("error", e)
            return src

        try:
            oxpath = google_xpath
            selenium_element_o = self.driver.find_element(By.XPATH, oxpath)
            src = selenium_element_o.get_attribute("src")

        except Exception as e:
            print("error selenium_element_o", e)

        selenium_element.click()
        return src

    def filterLink_(self, urls=None, scopes=[], printOriginal=False):

        if len(scopes) == 0:
            return
        if urls is not None:
            self.imgslink = urls
        tmpC = []
        for imlk_ in self.imgslink:
            chk = True
            for sc_ in scopes:
                if imlk_.find(sc_) < 0:
                    chk = False
                if not chk:
                    break
            if chk:
                tmpC.append(imlk_)
        print("\ndone to filter scopes=", scopes, " original count ", len(self.imgslink), " after filter count ", len(tmpC))
        if printOriginal:
            print("\nprintOriginal: \n", self.imgslink)
        self.imgslink = []
        return tmpC

    def getfnameFormUrl(self, url):
        return self.getfnameFromWebAddress([url])[0][2]


# q_GC = q_GoogleC()
