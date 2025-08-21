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
    """
    A class for managing Google search and image-related web scraping operations.

    This class provides methods to interact with Google's search pages using Selenium,
    find image links, download images, and manage session and data records.
    """
    driver = None
    recordDf = None

    class gApp:
        """
        A nested class for high-level Google application functionalities.

        This class contains methods for querying Google Images, managing Selenium drivers,
        and handling image downloads and data persistence.
        """
        def q_Google(self, query, pics=None, start=0, scroll=True, xL=None):
            """
            Performs a Google Images search and downloads the images.

            This is a comprehensive function that automates the process of searching
            for images on Google, scrolling to load more, extracting image links,
            and saving the images to a local directory.

            Args:
                query (str): The search query string for Google Images.
                pics (int, optional): The maximum number of pictures to download. If None,
                                      it downloads all found. Defaults to None.
                start (int, optional): The starting index of the images to download.
                                       Defaults to 0.
                scroll (bool, optional): Whether to scroll the page to load more images.
                                         Defaults to True.
                xL (list, optional): A list of specific image indices to download. If
                                     None, it downloads based on `start` and `pics`.
                                     Defaults to None.

            Returns:
                tuple: A tuple containing the Selenium driver object and a list of
                       errors encountered during the process.
            """
            gP = google()
            # Construct the Google Images search URL.
            addr = "https://www.google.co.in/search?q=" + query.replace(" ", "+") + "&source=lnms&tbm=isch"
            
            # Define directory and file names for saving records.
            key = "googleSearch_" + query.replace(" ", "").capitalize()
            pDir = "graspOut_1"
            dirp = fp.getAllPath(key, parentDirName=pDir)
            retFCC = {}
            errorC = []

            # Initialize the Selenium driver with the search URL.
            driver = gP.initPCDriver(webAddr=addr, waittime=1, initRecord=True)

            # Scroll the window to reveal all images if requested.
            if scroll:
                gP.widowFreeScroll(driver)  # , waitTime = 0.25
            
            # Get the BeautifulSoup object for parsing the HTML.
            bsObj = gP.getBsObj(driver=driver)
            xC = {"driver": driver, "bsObj": bsObj}

            # Find the main image frame.
            frmeL = xC["bsObj"].find_all("div", {"jsname": "r5xl4", "class": "islrc"})
            
            # Find the inner image tags within the frame.
            vCTag = frmeL[0].find_all("img", {"class": "rg_i Q4LuWd tx8vtf"})
            cnt = -1
            
            # Loop through the image tags to process each one.
            for tag in vCTag:
                cnt += 1
                if cnt < start:
                    continue
                if cnt in errorC:
                    continue
                if xL is not None and len(xL) > 0:
                    if cnt not in xL:
                        continue
                if pics is not None:
                    if cnt > pics:
                        break

                print("\rEpoch {}/{}".format(cnt, len(vCTag)), end="", flush=True)
                
                # Get the XPath of the image tag for Selenium interaction.
                xpath = gP.xpath_soup(tag)

                try:
                    # Find the element and click it to open the preview.
                    selenium_element = xC["driver"].find_element_by_xpath(xpath)
                    selenium_element.click()
                    time.sleep(5)
                except:
                    print("error", cnt)
                    errorC.append([cnt, tag.get("alt")])
                    continue
                try:
                    # Find the full-size image within the preview.
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
                
                # Generate a unique file name.
                xname = "_".join([key, gP.getNowDateTimeStr()]) + ".png"
                fname = os.path.join(dirp, xname)
                retFCC[src] = fname

                # Download the image using multiple methods if one fails.
                if not gP.isDowLoaded(src):
                    try:
                        if not gP.ulib_save(src, fname, iprint=None):
                            print("in ulib false")
                            if not gP.google_data_save(fname, src, iprint=None):
                                print("in google_data_save false")
                                if not gP.request_data_save(fname, src, iprint=None):
                                    print("in request_data_save false")
                                    raise
                        # Append the download record to the DataFrame.
                        gP.appendRecord(src, title, dirp, xname)
                        continue
                    except:
                        print("error download", cnt)
                        errorC.append([cnt, title, src])
                break
            # Save the final download records.
            gP.saveRecord()
            return driver, errorC

        def google_seagch_save(self, gP, urls, key="sexy", pDir="graspOut", iprint=False):
            """
            Saves images from a list of URLs obtained from a Google search.

            This function iterates through a list of URLs and attempts to save each
            image to a specified directory using different saving methods.

            Args:
                gP (google): An instance of the google class.
                urls (list): A list of image URLs to be saved.
                key (str, optional): A keyword for the directory name. Defaults to "sexy".
                pDir (str, optional): The parent directory for saving. Defaults to "graspOut".
                iprint (bool, optional): Whether to print progress messages. Defaults to False.

            Returns:
                None
            """
            cnt = 0
            dirp = fp.getAllPath(key, parentDirName=pDir)
            for datai in urls:
                # Generate a unique file name.
                fname = os.path.join(dirp, "_".join([key, gP.getNowDateTimeStr()]) + ".png")
                # Attempt to save the image using different methods.
                if gP.google_data_save(fname, datai, iprint=iprint):
                    continue
                imgs, urlsR, errPic = gP.getURLimagePIL([urls], limitSize=1024 * 5, show=False, iprint=False)
                if len(imgs) > 0:
                    if gP.saveImgsPIL(fname, imgs[0], iprint=iprint):
                        continue

                if iprint:
                    print("\nFail to save: url", datai)
                    
        def getPhoto(
            self, addr, driver=None, bsObj=None, urls=None, options={"dirP": "graspOut", "bsObj": True, "urls": {"tag": {"tagName": "img", "srcName": "src"}, "link": True, "img": True, "save": True,},},
        ):
            """
            A generic function to fetch and save photos from a URL.

            This method uses a set of configurable options to fetch images from a web page.
            It can handle driver initialization, HTML parsing with BeautifulSoup, and
            image downloading and saving based on the provided options.

            Args:
                addr (str): The URL of the web page.
                driver (webdriver, optional): An existing Selenium driver instance. If None,
                                              a new one is initialized. Defaults to None.
                bsObj (BeautifulSoup, optional): An existing BeautifulSoup object. If None,
                                                 a new one is created. Defaults to None.
                urls (list, optional): A list of image URLs. If None, the function will
                                       try to find them on the page. Defaults to None.
                options (dict, optional): A dictionary of configurable options for the process.
                                          Defaults to a predefined set.

            Returns:
                dict: A dictionary containing the driver, BeautifulSoup object, and details
                      about the fetched images.
            """
            # Initialize the driver if one is not provided.
            if driver is None:
                driver = self.initPCDriver(webAddr=addr, waittime=1)
            # Create a BeautifulSoup object if one is not provided.
            if not options["bsObj"]:
                return {"driver": driver}
            if bsObj is None:
                bsObj = self.getBsObj(driver=driver)
            if not options["urls"]["link"]:
                return {"driver": driver, "bsObj": bsObj}
            
            # Find image links from the page if not provided.
            tagName = options["urls"]["tag"]["tagName"]
            srcName = options["urls"]["tag"]["srcName"]
            if urls is None:
                urls = self.getImagesLink_bs4(bsObj, tagName=tagName, srcName=srcName)

            # Get image content from URLs.
            if not options["urls"]["img"]:
                return {"driver": driver, "bsObj": bsObj, "urls": urls}
            imgsC, urlsR, errPic = self.getURLimagePIL(urls, show=False, iprint=False)
            print("find count of images", len(imgsC))
            if len(imgsC) == 0:
                return {"driver": driver, "bsObj": bsObj, "urls": urls}
            
            # Get filenames and directory path.
            filenames = self.getfnameFromWebAddress(urlsR)
            parentDirName = options["dirP"]
            title = self.getHtmlTitle_bs4(bsObj)
            print("title", title)
            dirName = title
            dirp = fp.getAllPath(dirName, parentDirName=parentDirName)
            
            # Save images if requested.
            if options["urls"]["save"]:
                self.saveImgsPIL(dirName, filenames, imgsC)
            
            # Return a dictionary of results.
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
            """
            An uncompleted function intended for updating a Facebook page.
            
            This function appears to be a work in progress for handling Facebook-specific
            web scraping, but it's not fully implemented.

            Args:
                xC (dict): A dictionary containing context information, including a Selenium driver.

            Returns:
                dict: The updated context dictionary.
            """
            # The function seems to be a placeholder or a test function as it does
            # not perform a clear, defined task. It gets a photo, modifies a list
            # of URLs, and then gets photos again.
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

            return xC

    def initDf(
        self, dirp="graspOut", fname="search.csv", columns=["url", "title", "folder", "fname"],
    ):
        """
        Initializes the DataFrame for recording search and download history.

        This method attempts to load an existing CSV file into a pandas DataFrame.
        If the file does not exist, it creates a new empty DataFrame with predefined columns.

        Args:
            dirp (str, optional): The directory path. Defaults to "graspOut".
            fname (str, optional): The filename. Defaults to "search.csv".
            columns (list, optional): The list of column names for the DataFrame.
                                      Defaults to a predefined list.
        """
        # Try to read the existing CSV file.
        if self.recordDf is None:
            try:
                self.recordDf = pd.read_csv(os.path.join(dirp, fname))
            except:
                pass
            # If reading fails, create a new DataFrame.
            if self.recordDf is None:
                self.recordDf = pd.DataFrame(columns=["url", "title", "folder", "fname"])

    def isDowLoaded(self, url):
        """
        Checks if a given URL has already been recorded as downloaded.

        This function searches the internal DataFrame to see if a specific URL
        exists, which helps in avoiding duplicate downloads.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL is found in the download record, False otherwise.
        """
        try:
            # Check if the URL is a valid URL format.
            if self.validators.url(url):
                # Query the DataFrame for the URL.
                df1 = self.recordDf[self.recordDf["url"] == url]
                # Return True if a match is found.
                if df1 is not None and len(df1) > 0:
                    return True
        except:
            pass
        return False

    def appendRecord(self, url, title, folder, fname):
        """
        Appends a new download record to the DataFrame.

        This method creates a new row with the provided data and appends it to the
        DataFrame that stores the download history.

        Args:
            url (str): The URL of the downloaded content.
            title (str): The title associated with the content.
            folder (str): The folder where the content is saved.
            fname (str): The filename of the saved content.
        """
        # Create a new DataFrame from the provided data.
        df1 = pd.DataFrame([{"url": url, "title": title, "folder": folder, "fname": fname}])
        # Append the new DataFrame to the existing record.
        self.recordDf = self.recordDf.append(df1, ignore_index=True)

    def saveRecord(self, dirp="graspOut", fname="search.csv"):
        """
        Saves the download record DataFrame to a CSV file.

        This function writes the entire download history DataFrame to a CSV file
        in a specified location, ensuring the data is persistent.

        Args:
            dirp (str, optional): The directory path. Defaults to "graspOut".
            fname (str, optional): The filename. Defaults to "search.csv".
        """
        # Save the DataFrame to a CSV file without the index.
        self.recordDf.to_csv(os.path.join(dirp, fname), index=False)

    def getDriver(self):
        """
        Returns the current Selenium driver instance.

        Returns:
            webdriver: The Selenium driver object.
        """
        return self.driver

    def changUrl(self, url):
        """
        Navigates the current driver to a new URL.

        Args:
            url (str): The URL to navigate to.
        """
        self.driver.get(url)

    def initDriver(self, webAddr="", waittime=20):
        """
        Initializes a new headless Selenium WebDriver.

        This method sets up a Chrome WebDriver with headless options, which means
        it runs without a visible browser UI. It's useful for web scraping on servers.

        Args:
            webAddr (str, optional): The initial URL to load after driver initialization.
                                     Defaults to an empty string.
            waittime (int, optional): The implicit wait time for elements to load.
                                      Defaults to 20 seconds.

        Returns:
            webdriver: The initialized Selenium driver object.
        """
        if self.driver is None:
            # Set up Chrome options for headless mode.
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            # Initialize the driver with the specified options.
            wd = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(wd, waittime)
            self.driver = wd
        if webAddr is not None and len(webAddr) > 0:
            self.getHtmlContent(self.driver, webAddr)
        return self.driver

    def initPCDriver(self, webAddr="", waittime=20, initRecord=True):
        """
        Initializes a new Selenium WebDriver for a personal computer (non-headless).

        This function sets up a standard Chrome WebDriver that is not headless,
        making it suitable for running on a desktop environment where a visible
        browser is needed. It also initializes the download record DataFrame.

        Args:
            webAddr (str, optional): The initial URL to load. Defaults to an empty string.
            waittime (int, optional): The implicit wait time for elements. Defaults to 20.
            initRecord (bool, optional): Whether to initialize the download record DataFrame.
                                         Defaults to True.

        Returns:
            webdriver: The initialized Selenium driver object.
        """
        if self.driver is None:
            # Initialize a non-headless Chrome driver.
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            wd = webdriver.Chrome("chromedriver")
            wait = WebDriverWait(wd, waittime)
            self.driver = wd

        if webAddr is not None and len(webAddr) > 0:
            self.getHtmlContent(self.driver, webAddr)
        if initRecord:
            self.initDf()
        return self.driver

    def getHtmlContent(self, driver, webAddr):
        """
        Loads the content of a specified URL into the Selenium driver.

        This method navigates the Selenium driver to the given URL, but first
        it checks if the URL is valid.

        Args:
            driver (webdriver): The Selenium driver instance.
            webAddr (str): The URL to load.
        """
        # Check if the URL is valid.
        isM = self.IsURL(webAddr)
        if not isM:
            return
        # Navigate to the URL.
        driver.get(webAddr)

    def getBsObj(self, driver=None, content=""):
        """
        Creates a BeautifulSoup object from either a Selenium driver's page source or a string.

        This function is a utility to parse HTML content. It can take the HTML source
        directly from a Selenium driver or from a provided string.

        Args:
            driver (webdriver, optional): The Selenium driver. If provided, its page
                                          source is used. Defaults to None.
            content (str, optional): A string containing the HTML content. Defaults to "".

        Returns:
            BeautifulSoup: The parsed BeautifulSoup object, or None if no content is provided.
        """
        if driver is not None:
            # Parse the driver's page source.
            return bsO(driver.page_source, features="html.parser")
        if len(content) > 0:
            # Parse the provided string content.
            return bsO(content)
        return None

    def getTag_bs4(self, bsObj, tag="", iprint=False):
        """
        Finds all HTML tags of a specified type using BeautifulSoup.

        Args:
            bsObj (BeautifulSoup): The BeautifulSoup object to search.
            tag (str, optional): The name of the HTML tag to find (e.g., 'a', 'img').
                                 Defaults to an empty string.
            iprint (bool, optional): Whether to print the found tags' text. Defaults to False.

        Returns:
            list: A list of BeautifulSoup tag objects.
        """
        a_tags = bsObj.find_all(tag)
        if iprint:
            for tag in a_tags:
                print(type(tag), tag.text)
        return a_tags

    def getAttr_bs4(self, obj, attr=None, iprint=False):
        """
        Finds all HTML tags with a specified attribute and value using BeautifulSoup.

        Args:
            obj (BeautifulSoup or Tag): The object to search within.
            attr (dict, optional): A dictionary representing the attribute and its value
                                   to search for (e.g., `{'class': 'ep_23'}`). Defaults to None.
            iprint (bool, optional): Whether to print the found tags' text. Defaults to False.

        Returns:
            list: A list of BeautifulSoup tag objects.
        """
        # Find all tags with the specified attributes.
        eles = obj.find_all(attrs=attr)
        if iprint:
            for tag in eles:
                print(type(tag), tag.text)
        return eles

    def getHtmlTitle_bs4(self, bsObj, tagName="title"):
        """
        Extracts the title of the HTML document.

        This method finds the `<title>` tag and returns its text content, after
        stripping control characters.

        Args:
            bsObj (BeautifulSoup): The BeautifulSoup object of the page.
            tagName (str, optional): The name of the tag to search for. Defaults to "title".

        Returns:
            str: The cleaned title of the page, or "temp" if no title is found.
        """
        # Find all tags with the specified name.
        rr = self.getTag_bs4(bsObj, tag=tagName)
        if (rr is not None) or len(rr) > 0:
            # Strip control characters from the text of the first tag found.
            return self.strip_control_characters(rr[0].text)
        return "temp"

    def getImagesLink_bs4(self, bsObj, tagName="img", srcName="src"):
        """
        Finds and returns all image links on a page using BeautifulSoup.

        This function searches for all `img` tags and extracts the URL from their
        `src` attribute.

        Args:
            bsObj (BeautifulSoup): The BeautifulSoup object of the page.
            tagName (str, optional): The name of the image tag. Defaults to "img".
            srcName (str, optional): The attribute name containing the image URL.
                                     Defaults to "src".

        Returns:
            list: A list of strings, where each string is an image URL.
        """
        vCTag = self.getTag_bs4(bsObj, tag=tagName, iprint=False)
        urls = []
        for tag in vCTag:
            # Get the value of the 'src' attribute for each image tag.
            urls.append(tag.get(srcName))
        return urls

    def strip_control_characters(self, s):
        """
        Removes non-alphanumeric and non-printable characters from a string.

        Args:
            s (str): The input string.

        Returns:
            str: The cleaned string.
        """
        word = ""
        for i in s:
            if not (ord(i) < 48 or (ord(i) in range(91, 97)) or (ord(i) in range(123, 128))):
                word += i
        return word

    def xpath_soup(self, element):
        """
        Generate xpath of soup element.

        This function creates a unique XPath string for a given BeautifulSoup element,
        which is essential for locating the same element with Selenium.

        Args:
            element (bs4.element.Tag): The BeautifulSoup element.

        Returns:
            str: The generated XPath as a string.
        """
        # Build the XPath components by traversing up the parent nodes.
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:
            previous = itertools.islice(parent.children, 0, parent.contents.index(child))
            xpath_tag = child.name
            xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
            components.append(xpath_tag if xpath_index == 1 else "%s[%d]" % (xpath_tag, xpath_index))
            child = parent
        # Reverse the components to get the correct path from root.
        components.reverse()
        return "/%s" % "/".join(components)

    def IsURL(self, str_url):
        """
        Checks if a string is a valid URL using a regular expression.
        
        Note: The implementation of this function is flawed, as it always returns True
        regardless of the input. The regular expression part is not being used correctly.

        Args:
            str_url (str): The string to validate.

        Returns:
            bool: Always returns True.
        """
        # The function currently always returns True, making the regex check ineffective.
        return True
        strRegex = "^((https|http|ftp|rtsp|mms)?://)" + "?(([0-9a-zA-Z_!~*'().&=+$%-]+: )?[0-9a-zA-Z_!~*'().&=+$%-]+@)?" + "(([0-9]{1,3}.){3}[0-9]{1,3}" + "|" + "([0-9a-zA-Z_!~*'()-]+.)*" + "([0-9a-zA-Z][0-9a-zA-Z-]{0,61})?[0-9a-zA-Z]." + "[a-z]{2,6})" + "(:[0-9]{1,4})?" + "((/?)|" + "(/[0-9a-zA-Z_!~*'().;?:@&=+$,%#-]+)+/?)$"
        isM = re.match(strRegex, str_url)
        if isM:
            return True
        else:
            return False

    def fetch_imagef(self, url, fname=None, path=None, tryAgain=True, tryC=3):
        """
        Fetches an image from a URL and saves it as a file.

        This method requests the image content, opens it with PIL (Pillow),
        and saves it to the specified file path, converting it to JPEG if needed.

        Args:
            url (str): The URL of the image to fetch.
            fname (str, optional): The name of the file to save. If None, a
                                   timestamp-based name is generated. Defaults to None.
            path (str, optional): The directory path to save the file. Defaults to None.
            tryAgain (bool, optional): Whether to retry the request on failure. Defaults to True.
            tryC (int, optional): The number of retry attempts. Defaults to 3.

        Returns:
            PIL.Image.Image: The PIL Image object if successful, otherwise None.
        """
        # Generate a filename if one is not provided.
        fname = "test_src" + "_" + getNowDateTimeStr(format="%y%m%d_%H%M%S") if fname is None else fname
        if path is not None:
            fname = os.path.join(path, fname)
        
        # Perform the request with retry logic.
        req = nt_.doRequest(url)
        err = None
        img = None
        if req.status_code == 200:
            # Open the image content with PIL.
            im = BytesIO(req.content)
            img = Image.open(im)

            # Get the file extension.
            extension = os.path.splitext(fname)[1].lower()

            # Save the image based on its format.
            if extension == ".png":
                img.save(fname, "PNG")
            else:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(fname, "JPEG")
        else:
            print("fail to fetch url", url, "\nerror at: ", req)
        return img
        
    def getURLimagePIL(self, urls, limitSize=1024 * 5, show=False, iprint=False):
        """
        Fetches images from a list of URLs, filters them by size, and returns PIL image objects.

        This function iterates through a list of URLs, downloads the content,
        and converts it into PIL Image objects. It also checks the size of the
        image against a limit.

        Args:
            urls (list): A list of URLs of the images to fetch.
            limitSize (int, optional): The minimum size in bytes for an image to be
                                       included. Defaults to 1024 * 5.
            show (bool, optional): Whether to display the images. Defaults to False.
            iprint (bool, optional): Whether to print progress messages. Defaults to False.

        Returns:
            tuple: A tuple containing:
                   - `imgs`: A list of PIL Image objects.
                   - `urlsR`: A list of the URLs that were successfully fetched.
                   - `errPic`: A list of URLs and their corresponding errors.
        """
        imgs = []
        cnt = 0
        urlsR = []
        errPic = []
        for url in urls:
            try:
                # Get image content and size from the URL.
                response = requests.get(url)
                im = BytesIO(response.content)
                image_file_size = sys.getsizeof(im.getvalue())
            except Exception as e:
                if iprint:
                    print("invalidate url", url, "due to:", e)
                errPic.append([url, e])
                continue

            if iprint:
                print(cnt, url)
                cnt += 1
                print("image_file_size", image_file_size, "limitSize", limitSize)
            
            # Open the image with PIL and check its size.
            img = Image.open(im)
            if image_file_size > limitSize:
                imgs.append(img)
                urlsR.append(url)
            if show:
                self.showimagePIL(img)
        return imgs, urlsR, errPic

    def showimagePIL(self, imgs):
        """
        Displays a list of PIL Image objects.

        Args:
            imgs (list): A list of PIL Image objects to display.
        """
        for img in imgs:
            display(img)

    def saveImgsPIL(self, dirP, filenames, imgs, iprint=True):
        """
        Saves a list of PIL Image objects to files.

        This function iterates through a list of images and saves each one
        to the specified directory with a corresponding filename.

        Args:
            dirP (str): The directory path to save the images.
            filenames (list): A list of filenames for the images.
            imgs (list): A list of PIL Image objects.
            iprint (bool, optional): Whether to print progress messages. Defaults to True.
        """
        if iprint:
            print("save processing...")
        dirP = fAdd.getDir(dirP)
        for imIdx in range(0, len(imgs)):
            fname = os.path.join(dirP, filenames[imIdx][2])
            self.saveImgPIL(fname, imgs[imIdx], iprint=iprint)
        if iprint:
            print("done to save")

    def saveImgPIL(self, fname, img, iprint=True, formatP="png"):
        """
        Saves a single PIL Image object to a file.

        Args:
            fname (str): The full path and filename to save the image to.
            img (PIL.Image.Image): The PIL Image object to save.
            iprint (bool, optional): Whether to print error messages. Defaults to True.
            formatP (str, optional): The file format (e.g., 'png', 'jpeg'). Defaults to "png".

        Returns:
            bool: True if the save was successful, False otherwise.
        """
        try:
            # Save the image with the specified format.
            imgx = img.save(fname, formatP)
            return True
        except:
            if iprint:
                print("\nFail to save", fname)
            pass
        return False

    def ulib_save(self, url, fname, iprint=True):
        """
        Saves a file from a URL using `urllib.request`.

        This function is an alternative method for downloading a file, with a
        built-in retry mechanism using a custom user agent.

        Args:
            url (str): The URL of the file to download.
            fname (str): The filename and path to save to.
            iprint (bool, optional): Whether to print error messages. Defaults to True.

        Returns:
            bool: True if the download was successful, False otherwise.
        """
        try:
            r, cm = ulib.urlretrieve(url, fname)
            return True
        except Exception as e:
            # Retry with a custom user agent.
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-Agent", getUserAgent())]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, fname)

            if iprint:
                print("\nFail to save", url, fname, ",due to ", e)
            pass
        return False

    def request_data_save(self, fname, url, iprint=True):
        """
        Saves a file from a URL using `requests`.

        This is another alternative method for downloading a file, which uses the
        `requests` library to get the content and then writes it to a file.

        Args:
            fname (str): The filename and path to save to.
            url (str): The URL of the file to download.
            iprint (bool, optional): Whether to print error messages. Defaults to True.

        Returns:
            bool: True if the save was successful, False otherwise.
        """
        try:
            # Perform a GET request to get the file content.
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
        """
        Saves a Base64-encoded image data URL to a file.

        This function is specifically designed to handle and decode Base64-encoded
        image data often found on Google search results pages.

        Args:
            fname (str): The filename and path to save to.
            data (str): The Base64-encoded image data string.
            iprint (bool, optional): Whether to print error messages. Defaults to True.

        Returns:
            bool: True if the save was successful, False otherwise.
        """
        try:
            # Split the header from the Base64 data.
            header, encoded = data.split(",", 1)
            # Decode the Base64 data.
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
        """
        Generates a filename from a URL string.

        This utility function parses the URL to extract the filename and extension,
        and returns it in a structured list format.

        Args:
            urls (list): A list of URL strings.

        Returns:
            list: A list of lists, where each inner list contains the filename,
                  extension, and full filename for a URL.
        """
        xpath = []
        for url in urls:
            # Parse the URL to get the path.
            disassembled = urlparse(url)
            # Split the path to get the filename and extension.
            filename, file_ext = splitext(basename(disassembled.path))
            xpath.append([filename, file_ext, "".join([filename, file_ext])])
        return xpath

    def widowFreeScroll(self, driver, waitTime=0.25, print_=True):
        """
        Performs a free-form scroll on the web page to load dynamic content.

        This function scrolls the window by a fixed step until it reaches the
        bottom of the page, or until the page height no longer increases.

        Args:
            driver (webdriver): The Selenium driver instance.
            waitTime (float, optional): The time to wait between scrolls. Defaults to 0.25.
            print_ (bool, optional): Whether to print progress messages. Defaults to True.
        """
        if print_:
            print("start to scroll")
        part = 2
        ht = 1080
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            for Y_ in range(1, int(ht / part)):
                Y = Y_ * 250
                sj = "window.scrollTo(0," + str(Y) + " )"
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
        """
        Performs a full scroll to the bottom of the page.

        This function repeatedly scrolls down until the page height stops increasing,
        indicating that all dynamic content has been loaded.

        Args:
            driver (webdriver): The Selenium driver instance.
            waitTime (int, optional): The time to wait after each scroll. Defaults to 5.
            nextto (int, optional): The maximum number of scrolls to perform. If -1,
                                    it scrolls until the end. Defaults to -1.
        """
        SCROLL_PAUSE_TIME = waitTime
        last_height = driver.execute_script("return document.body.scrollHeight")
        cnt = 0
        while True:
            # Scroll to the bottom of the page.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            print("\rscroll Epoch {} height {}/{}".format(cnt + 1, last_height, new_height), end="", flush=True)
            if new_height == last_height:
                break
            last_height = new_height
            cnt += 1
            if nextto > 0 and nextto <= cnt:
                break
        print("\ndone to scroll")

    def window_scroll_by_step(self, driver, waitTime=5, nextto=-1):
        """
        Scrolls the window by a step and records the page source at each step.

        This is a variation of the scroll function that saves the page source
        after each scroll, which can be useful for analyzing how content loads
        dynamically.

        Args:
            driver (webdriver): The Selenium driver instance.
            waitTime (int, optional): The time to wait after each scroll. Defaults to 5.
            nextto (int, optional): The maximum number of scrolls. Defaults to -1.

        Returns:
            dict: A dictionary mapping the scroll count to the page source string.
        """
        rcc = {}
        SCROLL_PAUSE_TIME = waitTime
        last_height = driver.execute_script("return document.body.scrollHeight")
        cnt = 0
        rcc[-1] = driver.page_source
        while True:
            # Scroll to the bottom.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            rcc[cnt] = driver.page_source
            new_height = driver.execute_script("return document.body.scrollHeight")
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
        """
        Fetches an image from a URL and saves it.

        This is a duplicate method of the `fetch_imagef` found earlier. It fetches
        an image, opens it, and saves it to a file, handling format conversions.

        Args:
            url (str): The URL of the image.
            fname (str, optional): The filename. Defaults to a timestamp-based name.
            path (str, optional): The path to save the file. Defaults to None.
            tryAgain (bool, optional): Whether to retry on failure. Defaults to True.
            tryC (int, optional): The number of retries. Defaults to 3.

        Returns:
            PIL.Image.Image: The PIL Image object, or None if the fetch fails.
        """
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
        else:
            print("fail to fetch url", url, "\nerror at: ", req)
        return img
        
    def g_screenShot_driver(self):
        """
        Takes a screenshot of the current page in the Selenium driver and saves it.

        This method captures the full-page screenshot as a PNG and then saves it
        to a file named "test.png" using the PIL library.

        Returns:
            None
        """
        imp = self.driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(imp))
        image.save("test.png")


class navWebSite(google):
    """
    A class for navigating and interacting with a website.

    This class inherits from `google` and provides a set of methods for
    general website navigation, content scraping, and image downloading.
    """
    def __init__(self, url=None, connect=False):
        """
        Initializes the `navWebSite` object.

        This constructor calls the parent class's `__init__` and can optionally
        connect to a URL immediately.

        Args:
            url (str, optional): The initial URL to navigate to. Defaults to None.
            connect (bool, optional): Whether to initialize the connection to the URL.
                                      Defaults to False.
        """
        super(navWebSite, self).__init__()
        if connect:
            self.initObj(url)
        
    def g_driver(self, refresh=True):
        """
        Gets the Selenium driver instance.

        If the driver is not yet initialized or if `refresh` is True, it creates
        a new one.

        Args:
            refresh (bool, optional): If True, forces the creation of a new driver.
                                      Defaults to True.

        Returns:
            webdriver: The Selenium driver object.
        """
        if self.driver is None or refresh:
            self.initDriver(webAddr=None, waittime=20)
        return self.driver

    def initObj(self, url):
        """
        Initializes the internal state of the object for a new URL.

        This method sets up the driver, gets the page source, and creates the
        BeautifulSoup object for the given URL.

        Args:
            url (str): The URL to initialize the object with.
        """
        self.imgslink = []
        self.bsObj = None
        self.xObj = None
        self.webUrl = None
        self.dnload = False
        self.downloadC = {}
        # get driver
        self.g_driver()

        # get bs4 obj
        if url is None:
            return
        else:
            self.getHtmlContent(self.driver, url)
        bsObj = bsO(self.driver.page_source, features="html.parser")
        self.bsObj = bsObj
        self.xObj = {"driver": self.driver, "bsObj": bsObj}
        self.webUrl = url

    def setObjByTest(self, oo_):
        """
        Sets the internal object state from a test object.

        This is a utility function for testing purposes, allowing the internal
        `xObj` to be set directly.

        Args:
            oo_ (dict): A dictionary containing the driver and BeautifulSoup objects.
        """
        self.xObj = oo_

    def navUrl(self, url):
        """
        Navigates to a new URL and re-initializes the object.

        This method is a wrapper for `initObj`, providing a clear function name
        for navigation.

        Args:
            url (str): The URL to navigate to.
        """
        self.initObj(url)

    def getAllFrTagName(self, iObj=None, tagName="a", idNamd=None, clsName=None, attr=None):
        """
        Finds all HTML tags within an object based on name, ID, or class.

        This is a flexible function for scraping, allowing the user to find tags
        using different criteria.

        Args:
            iObj (BeautifulSoup or Tag, optional): The object to search within. If
                                                    None, it uses the object's `bsObj`.
                                                    Defaults to None.
            tagName (str, optional): The name of the tag to find. Defaults to "a".
            idNamd (str, optional): The ID of the tag. Defaults to None.
            clsName (str, optional): The class name of the tag. Defaults to None.
            attr (dict, optional): A dictionary of attributes to search for. Defaults to None.

        Returns:
            list: A list of BeautifulSoup tag objects.
        """
        if iObj is None:
            iObj = self.bsObj
        if clsName is not None:
            return iObj.find_all(tagName, {"class": clsName})
        if idNamd is not None:
            return iObj.find_all(tagName, {"id": idNamd})
        if attr is not None:
            return iObj.find_all(tagName, attr)
        return iObj.find_all(tagName)

    def getSrc(self, tag, scope=None):
        """
        Gets the `src` attribute from a tag, optionally filtered by a scope string.

        Args:
            tag (BeautifulSoup.Tag): The tag object.
            scope (str, optional): A string that the `src` attribute must contain.
                                   Defaults to None.

        Returns:
            str or None: The `src` attribute string if it matches the criteria,
                         otherwise None.
        """
        if (scope is None) or (scope is not None and len(scope) > 0 and tag["src"].index(scope) >= 0):
            return tag["src"]
        return None

    def getImsLink(self):
        """
        Returns the list of image links that have been found.

        Returns:
            list: A list of URL strings.
        """
        return self.imgslink

    def getallImagesLink(self, tagName="img", scope=None, idNamd=None, clsName=None, url=None, refresh=False, filter=[], host=None):
        """
        Finds all image links on a page, with filtering and host-prepending options.

        This method scrapes the page for image tags, filters the URLs based on
        keywords, and can prepend a host URL if the links are relative.

        Args:
            tagName (str, optional): The name of the tag to find. Defaults to "img".
            scope (str, optional): A string that the `src` must contain. Defaults to None.
            idNamd (str, optional): The ID of the tag. Defaults to None.
            clsName (str, optional): The class name of the tag. Defaults to None.
            url (str, optional): The URL to navigate to. Defaults to None.
            refresh (bool, optional): Whether to refresh the driver and content. Defaults to False.
            filter (list, optional): A list of keywords that the URL must contain. Defaults to [].
            host (str, optional): The host URL to prepend to relative links. Defaults to None.
        """
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
        """
        Filters the list of image links based on keywords.

        This method refines the `imgslink` list by keeping only those URLs
        that contain all the specified keywords.

        Args:
            scopes (list, optional): A list of keywords to filter by. Defaults to [].
            printOriginal (bool, optional): Whether to print the original list before filtering.
                                            Defaults to False.
        """
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

    def dnloadImages(self, prnp=False, urls_=None, urls_name=None):
        """
        Downloads the images from the found links.

        This method iterates through the list of image URLs and downloads each one,
        creating an `ims` object to manage the saved file.

        Args:
            prnp (bool, optional): Whether to print progress messages. Defaults to False.
            urls_ (list, optional): A specific list of URLs to download. If None,
                                    it uses the object's `imgslink`. Defaults to None.
            urls_name (list, optional): A list of URLs for generating filenames.
                                        If None, it uses `urls_`. Defaults to None.
        """
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
            try:
                self.downloadC[key] = ims(fname=key, path=urls[n_])
            except Exception as e:
                print("\nerror occ at download... , ", e, "\n")
                pass

        if len(self.downloadC) > 0:
            self.dnload = True
        print("\ndone to download {} images, ".format(len(list(self.downloadC.keys()))))

    def showAllIms(self, figSize=(20, 15), imageSize=(200, 200), columns=3, rows=5):
        """
        Downloads all images and displays them.

        This is a utility function to visually inspect the downloaded images
        in a grid format.

        Args:
            figSize (tuple, optional): The size of the figure. Defaults to (20, 15).
            imageSize (tuple, optional): The size of each image. Defaults to (200, 200).
            columns (int, optional): The number of columns in the grid. Defaults to 3.
            rows (int, optional): The number of rows in the grid. Defaults to 5.
        """
        self.dnloadImages()
        cnt = 1
        for k_ in self.downloadC:
            ims_ = self.downloadC[k_]
            print("%d  fname %s, src %s ", cnt, ims_.get_name(), ims_.get_url())
            cnt += 1
        images = self.get_all_images()
        plot_images_with_np(images, figSize=figSize, imageSize=imageSize, columns=columns, rows=rows)

    def get_all_images(self):
        """
        Retrieves all downloaded image objects.

        Returns:
            list: A list of `ims` image objects.
        """
        r_ = []
        for k_ in self.downloadC:
            ims_ = self.downloadC[k_]
            r_.append(ims_.get_img())
        return r_

    def saveImgs(self, path, fnames=[]):
        """
        Saves all downloaded images to a specified path.

        This method iterates through the downloaded images and saves each one
        to the local file system.

        Args:
            path (str): The directory path to save the images to.
            fnames (list, optional): A list of specific filenames to save. If empty,
                                     all images are saved. Defaults to [].
        """
        fp_.creatFolder(path)
        err_=[]
        for idx,k_ in enumerate(self.downloadC):
            ims_ = self.downloadC[k_]
            if len(fnames) > 0 and ims_.get_name not in fnames:
                continue
            path_ = os.path.join(path, ims_.get_name())
            if(os.path.isfile( path_ )):continue
            try:
                ims_.get_img().save(path_, "JPEG")
            except Exception as e:
                err_.append([idx,k_])
            print("\rEpoch idx/count {}/{} err {}".format(idx + 1, len(self.downloadC), len(err_)), end="", flush=True,)
        if(len(err_)>0):
            print(f'there are {len(err_)} errors found,\n{err_}')


class mInfo:
    """
    A data class to hold information about a web model or content item.

    This class serves as a simple data structure to store attributes like title,
    URL, and image links for a web element.
    """
    def _init_(self):
        """
        Initializes the mInfo object with default values.
        """
        self.title = None
        self.navUrl = None
        self.imageTitle = None
        self.imHref = None
        self.mslike = []

    def setP(self, p, val):
        """
        Sets an attribute of the object.

        Args:
            p (str): The name of the attribute to set.
            val (any): The value to assign to the attribute.
        """
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
        """
        Gets the value of an attribute.

        Args:
            p (str): The name of the attribute to get.

        Returns:
            any: The value of the attribute.
        """
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
        """
        Prints the contents of the object for debugging.

        Args:
            sub (bool, optional): Whether to print a condensed version. Defaults to False.
        """
        if not sub:
            print(" [ 'title': {}, 'href': {}, 'imTitle': {},'imLink': {}] ".format(self.title, self.navUrl, self.imageTitle, self.imHref))
            for s in self.mslike:
                s._prn(sub=False)
        else:
            print(" [   'imTitle': {},'imLink': {}] ".format(self.imageTitle, self.imHref))


def collectMInfo(fwC, mLC, mainUrl_=None):
    """
    Collects model information from a web page and populates a collection.

    This function scrapes the page for elements representing models or items
    and extracts their title, URL, and image links.

    Args:
        fwC (object): The web scraper object.
        mLC (dict): The dictionary to store the collected information.
        mainUrl_ (str, optional): The main URL to prepend to relative links.
                                  Defaults to None.
    """
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
        if "title" == "":
            mLC["err"].append(t_)
        else:
            mLC["R"][title] = mL_


def collectMInfoDetail(fwC, mInfoC, mainUrl_=None):
    """
    Collects detailed image information from a model's page.

    This function scrapes a page for a list of images and stores their titles
    and links within a given `mInfo` object.

    Args:
        fwC (object): The web scraper object.
        mInfoC (mInfo): The `mInfo` object to store the details in.
        mainUrl_ (str, optional): The main URL to prepend to relative links.
                                  Defaults to None.
    """
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
    """
    A class for performing advanced Google-specific scraping tasks.

    This class inherits from `navWebSite` and adds methods tailored for
    navigating and interacting with Google's search results.
    """
    def __init__(self, url=None, connect=False):
        """
        Initializes the `q_GoogleC` object.

        This constructor calls the parent class's `__init__`.

        Args:
            url (str, optional): The initial URL. Defaults to None.
            connect (bool, optional): Whether to connect to the URL on initialization.
                                      Defaults to False.
        """
        super(q_GoogleC, self).__init__(url, connect=connect)

    def getBSOObj(self):
        """
        Creates and returns a BeautifulSoup object from the current driver's page source.

        Returns:
            BeautifulSoup: The BeautifulSoup object.
        """
        return bsO(self.driver.page_source, features="html.parser")

    def findAllTag(self, iObj=None, tagName="a", idNamd=None, clsName=None, attr=None):
        """
        Finds all HTML tags within an object based on various criteria.

        This method is a simple alias for the parent class's `getAllFrTagName`.

        Args:
            iObj (BeautifulSoup or Tag, optional): The object to search within. Defaults to None.
            tagName (str, optional): The name of the tag. Defaults to "a".
            idNamd (str, optional): The ID of the tag. Defaults to None.
            clsName (str, optional): The class name of the tag. Defaults to None.
            attr (dict, optional): A dictionary of attributes to search for. Defaults to None.

        Returns:
            list: A list of BeautifulSoup tag objects.
        """
        return self.getAllFrTagName(iObj=iObj, tagName=tagName, idNamd=idNamd, clsName=clsName, attr=attr)

    def doAction(self, tag, delay=2, google_xpath=None):
        """
        Performs a click action on a Selenium element and extracts the source URL.

        This method is designed for a specific task on Google search results pages:
        clicking a thumbnail to reveal the full-size image and its source URL.

        Args:
            tag (BeautifulSoup.Tag): The BeautifulSoup tag of the element to click.
            delay (int, optional): The time in seconds to wait after clicking. Defaults to 2.
            google_xpath (str, optional): The XPath to the full-size image element.
                                          Defaults to None.

        Returns:
            str or None: The source URL of the full-size image, or None on failure.
        """
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
        """
        Filters a list of URLs based on a list of keywords.

        This is a duplicate of the `filterLink` method in the parent class.

        Args:
            urls (list, optional): A list of URLs to filter. If None, it uses the
                                   object's `imgslink`. Defaults to None.
            scopes (list, optional): A list of keywords to filter by. Defaults to [].
            printOriginal (bool, optional): Whether to print the original list before
                                            filtering. Defaults to False.

        Returns:
            list: The filtered list of URLs.
        """
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
        """
        Generates a filename from a single URL.

        This is a convenience wrapper around the parent class's `getfnameFromWebAddress`.

        Args:
            url (str): The URL string.

        Returns:
            str: The generated filename.
        """
        return self.getfnameFromWebAddress([url])[0][2]