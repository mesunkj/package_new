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
    # If selenium is not installed, the code attempts to install it.
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
    """
    A class containing methods for handling network requests and HTML file operations.
    
    This class serves as a container for related network utilities, primarily
    focused on fetching web content.
    """
    hm = None

    def __init__(self):
        """
        Initializes the Net class.
        
        This constructor creates an instance of the htmlFile class and assigns it
        to the hm attribute. This ensures that the Net instance has access to the
        HTML file-related methods.
        """
        # print('in net')
        self.hm = Net.htmlFile()
        pass

    class htmlFile:
        """
        A nested class dedicated to HTML file and URL content operations.

        This class provides a set of methods for reading content from URLs,
        making HTTP requests, and handling different decoding schemes.
        """
        def readUrlAsHtml(self, url, decode="utf-8"):
            """
            Reads the content of a given URL and returns it as a decoded HTML document.

            This function opens a URL, reads its content, and then decodes it using the
            specified character encoding. It is a simple utility for fetching web page
            content for further processing.

            Args:
                url (str): The URL of the web page to be read.
                decode (str, optional): The character encoding to be used for decoding the
                                        HTML content. Defaults to "utf-8".
            
            Returns:
                str: The decoded HTML content of the URL.
            """
            # Open the URL
            # The urlopen function from urllib.request is used to open the URL object.
            html = urlopen(url)
            
            # Read and decode the content
            # The .read() method reads the entire content from the opened URL object.
            # .decode() then converts the bytes read into a string using the specified encoding,
            # ignoring any errors that may occur during the decoding process.
            doc = html.read().decode(decode, "ignore")
            
            # Return the decoded document
            return doc

        def requestText(self, url):
            """
            Performs a POST request to a URL and returns the text content.

            This function first makes an HTTP POST request using `requests.post()` and then
            extracts the text content from the response object. It uses `StringIO` to
            efficiently get the value of the text.

            Args:
                url (str): The URL to which the POST request is made.

            Returns:
                str: The text content of the response.
            """
            r = self.request(url)
            # Use StringIO to create an in-memory text buffer from the response text,
            # then get its value. This is a clean way to handle the text content.
            return StringIO(r.text).getvalue()

        def request(self, url):
            """
            Makes an HTTP POST request to a specified URL.

            This is a basic wrapper around `requests.post()` to perform a POST request.
            It's a foundational method for sending data to a server.

            Args:
                url (str): The URL for the POST request.

            Returns:
                requests.Response: The response object from the HTTP POST request.
            """
            return requests.post(url)

        def coDataFormUrlRequest(self, url, decode="utf-8"):
            """
            Requests data from a URL and decodes it.

            This function is similar to `readUrlAsHtml` but is named differently and
            explicitly mentions 'data' in its name, suggesting a focus on raw data fetching.

            Args:
                url (str): The URL to request data from.
                decode (str, optional): The character encoding to use for decoding the content.
                                        Can be a list of encodings. Defaults to "utf-8".

            Returns:
                str: The decoded content of the URL.
            """
            # Open the URL, read the content, and decode it with the specified encoding.
            # The 'ignore' parameter handles decoding errors gracefully.
            return urlopen(url).read().decode(decode, "ignore")

        def catchUrlNew(self, url, decode="utf-8"):
            """
            Attempts to open a URL with a timeout and handles connection errors.

            This method is an improvement over simple `urlopen` by incorporating a timeout
            to prevent the program from hanging and by catching specific connection errors.

            Args:
                url (str): The URL to be opened.
                decode (str, optional): The character encoding for decoding the content.
                                        Defaults to "utf-8".

            Returns:
                str or None: The decoded HTML document if successful, otherwise None if an error occurs.
            """
            try:
                # Attempt to open the URL with a 5-second timeout.
                html = urlopen(url, timeout=5)
                # Read and decode the content if the connection is successful.
                doc = html.read().decode(decode, "ignore")
                return doc
            except ConnectionResetError:
                # Print a message if a ConnectionResetError occurs and return None.
                print("==> ConnectionResetError")
                pass
            return None

    def getURL(self, url, decode="utf-8", func=None):
        """
        A high-level method to fetch content from a URL using different strategies.

        This function acts as a dispatcher. It can use `readUrlAsHtml`, `request`,
        or `requestText` to retrieve content based on the `func` parameter.

        Args:
            url (str): The URL to fetch.
            decode (str, optional): The character encoding for `readUrlAsHtml`. Defaults to "utf-8".
            func (str, optional): The name of the function to use for fetching.
                                  Possible values are 'request' and 'requestText'.
                                  If None, it defaults to `readUrlAsHtml`.

        Returns:
            str or requests.Response or None: The content fetched from the URL. The type of the
                                              return value depends on the `func` parameter.
        """
        # If no specific function is requested, use the default `readUrlAsHtml`.
        if func is None:
            return self.hm.readUrlAsHtml(url, decode)
        
        # If 'request' is specified, return the requests.Response object.
        if func == "request":
            return self.hm.request(url)

        # If 'requestText' is specified, return the text content from the response.
        if func == "requestText":
            return self.hm.requestText(url)
            
        # If an unknown function is specified, return None.
        return None


class netApp:
    """
    A class for managing advanced network operations using `requests.Session`.

    This class provides a more robust way to handle network requests, including
    managing sessions, user agents, retries, and different request types (GET, POST).
    """
    session = None

    def __init__(self):
        """
        Initializes the netApp class.
        
        This constructor sets the session attribute to None, indicating that no
        session is currently active.
        """
        self.session = None

    def connectSession(self):
        """
        Establishes a new `requests.Session`.
        
        This method creates a new session object. Using a session can improve performance
        by reusing the underlying TCP connection and can also persist cookies across requests.
        """
        # Create and assign a new requests.Session object.
        self.session = requests.Session()

    def closeSession(self):
        """
        Closes the current `requests.Session`.
        
        This method properly closes the session to release any resources held by it.
        """
        # Call the .close() method on the session object.
        self.session.close(self)

    def getUserAgent(self, id_=-1):
        """
        Retrieves a user-agent string from a predefined list.

        This function is used to rotate user agents to mimic different browsers,
        which can help in avoiding bot detection.

        Args:
            id_ (int, optional): The index of the user agent to retrieve. If -1, a random
                                 user agent is selected. Defaults to -1.

        Returns:
            str: A user-agent string.
        """
        # If id_ is -1, select a random user agent.
        if id_ < 0:
            id_ = random.randint(0, len(_P.user_agent) - 1)
        # Return the user agent at the specified index.
        return _P.user_agent[id_]

    def getUrlContent(self, url, id_=-1):
        """
        Fetches the content of a URL as a string.

        This function performs a GET request, handles the character encoding,
        and returns the text content. It includes a delay to prevent overloading
        the target server.

        Args:
            url (str): The URL to fetch content from.
            id_ (int, optional): The index of the user agent to use. Defaults to -1 (random).

        Returns:
            str: The decoded text content of the URL.
        """
        # Perform the GET request.
        req = self.getUrlrequest(url=url, id_=id_)
        # Set the encoding based on the apparent encoding of the response.
        req.encoding = req.apparent_encoding
        # Pause execution for 1 second.
        time.sleep(1)
        # Return the text content.
        return req.text

    def getUrlContent_v(self, url, id_=-1):
        """
        Fetches the content of a URL and returns both the response object and the text.

        This is a variation of `getUrlContent` that provides more flexibility by returning
        the full response object, which can be useful for inspecting headers or status codes.

        Args:
            url (str): The URL to fetch content from.
            id_ (int, optional): The index of the user agent to use. Defaults to -1 (random).

        Returns:
            tuple: A tuple containing the `requests.Response` object and the decoded text content.
        """
        # Perform the GET request.
        req = self.getUrlrequest(url=url, id_=id_)
        # Set the encoding.
        req.encoding = req.apparent_encoding
        # Pause execution for 1 second.
        time.sleep(1)
        # Return the response object and the text content as a tuple.
        return req, req.text

    def doRequest(self, url, tryAgain=True, tryC=3):
        """
        Executes a GET request with a retry mechanism.

        This method attempts to perform a GET request up to a maximum number of tries.
        If an error occurs, it closes the session, waits, and retries the request.

        Args:
            url (str): The URL for the GET request.
            tryAgain (bool, optional): Whether to retry the request on failure. Defaults to True.
            tryC (int, optional): The maximum number of retry attempts. Defaults to 3.

        Returns:
            tuple: A tuple containing the `requests.Response` object and an error message.
                   If successful, the error message is an empty string. If it fails, the
                   response object is None and the error message describes the failure.
        """
        ic = 0
        err = ""
        # Loop for the maximum number of tries.
        while ic < tryC:
            try:
                # Attempt to get the URL request.
                return self.getUrlrequest(url)
            except Exception as e:
                # If an exception occurs, close the session.
                self.closeSession()
                err = "Fail to request, due to " + str(e)

                # If retries are not enabled, return None and the error.
                if not tryAgain:
                    return None, err
                # Increment the retry counter and wait before the next attempt.
                ic += 1
                time.sleep(30)
        # If the loop finishes without success, return a final error message.
        return None, "up tp Max try connection " + str(tryC) + ", due to " + err
        
    def doRequest_post(self, url, header, data_json, tryAgain=True, tryC=3):
        """
        Executes a POST request with a retry mechanism.

        This function is similar to `doRequest` but is specifically designed for POST
        requests, allowing data to be sent in JSON format with custom headers.

        Args:
            url (str): The URL for the POST request.
            header (dict): A dictionary of headers to be included in the request.
            data_json (dict): The data to be sent in JSON format.
            tryAgain (bool, optional): Whether to retry the request on failure. Defaults to True.
            tryC (int, optional): The maximum number of retry attempts. Defaults to 3.

        Returns:
            tuple: A tuple containing the `requests.Response` object and an error message.
                   If successful, the error message is an empty string. If it fails, the
                   response object is None and the error message describes the failure.
        """
        ic = 0
        err = ""
        # Loop for the maximum number of tries.
        while ic < tryC:
            try:
                # Attempt to get the URL request using the POST method.
                return self.getUrlrequest_post(url, header, data_json)
            except Exception as e:
                # If an exception occurs, close the session.
                self.closeSession()
                err = "Fail to request, due to " + str(e)

                # If retries are not enabled, return None and the error.
                if not tryAgain:
                    return None, err
                # Increment the retry counter and wait before the next attempt.
                ic += 1
                time.sleep(30)
        # If the loop finishes without success, return a final error message.
        return None, "up tp Max try connection " + str(tryC) + ", due to " + err

    def getUrlrequest(self, url, id_=-1):
        """
        Performs a GET request with a user-agent and `requests.Session`.

        This is a core method that handles the actual GET request. It ensures that a session
        is connected, sets a random user agent to mimic a real browser, and includes
        an 'Accept' header for proper content negotiation.

        Args:
            url (str): The URL for the GET request.
            id_ (int, optional): The index of the user agent to use. Defaults to -1 (random).

        Returns:
            requests.Response: The response object from the HTTP GET request.
        """
        # Ensure a session is active.
        if self.session is None:
            self.connectSession()
        
        # Define the 'Accept' header.
        accept = "text/html,application/xhtml+xml,application/xml;" "q=0.9,image/webp,*/*;q=0.8"
        # Get a user agent, either a random one or one specified by id_.
        if id_ < 0:
            id_ = random.randint(0, len(_P.user_agent) - 1)
        user_agent = self.getUserAgent(id_)
        # Construct the headers dictionary.
        headers = {"User-Agent": user_agent, "Accept": accept}

        # Perform the GET request with the session and headers.
        req = self.session.get(url, headers=headers)
        return req
        
    def getUrlrequest_post(self, url, header, data_json, id_=-1):
        """
        Performs a POST request with a user-agent, headers, and `requests.Session`.

        This is a core method for POST requests. It sets up the session and includes
        custom headers and JSON data in the request body.

        Args:
            url (str): The URL for the POST request.
            header (dict): A dictionary of headers for the request.
            data_json (dict): The data to be sent in JSON format.
            id_ (int, optional): The index of the user agent to use. Defaults to -1 (random).
        
        Returns:
            requests.Response: The response object from the HTTP POST request.
        """
        # Ensure a session is active.
        if self.session is None:
            self.connectSession()

        # The headers are passed directly as an argument.
        headers = header

        # Perform the POST request with the session, headers, and JSON data.
        # The 'json' parameter handles the serialization of the dictionary to a JSON string
        # and sets the 'Content-Type' header accordingly.
        req = self.session.post(url, headers=headers, json=data_json)
        return req

    def is_url_validate(self, url):
        """
        Checks if a URL is valid by attempting a GET request.

        A URL is considered 'valid' if the server returns a 200 OK status code.
        This is a simple way to verify if a link is live and accessible.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the status code is 200, otherwise False.
        """
        # Perform the GET request.
        req = self.getUrlrequest(url)
        # Check if the status code is 200 (OK).
        if req.status_code == 200:
            return True
        return False

    def downloadfromUrl(self, url, fpath):
        """
        Downloads a file from a URL and saves it to a specified path.

        This method uses `doRequest` to fetch the file content as bytes and then
        writes it to a local file.

        Args:
            url (str): The URL of the file to download.
            fpath (str): The local file path to save the downloaded content.
        """
        # Perform the request to get the response object.
        req = self.doRequest(url)
        # Open the file in binary write mode ('wb') and write the content.
        open(fpath, "wb").write(req.content)
        # Print a confirmation message.
        print("done to download", fpath)


# nt_ = netApp()


def htmlURLSimpleCodeCvt(url):
    """
    Performs a simple conversion on a URL string.

    This utility function replaces URL-encoded characters with their
    human-readable equivalents, specifically for colon and forward slash.

    Args:
        url (str): The URL string to be converted.

    Returns:
        str: The converted URL string.
    """
    # Replace '%3A' with ':' and '%2F' with '/'.
    return url.replace("%3A", ":").replace("%2F", "/")


def findPageCount(fwC, parserf, ptype, divClass="page both"):
    """
    Finds the total number of pages from a paginated HTML structure.

    This function is designed to parse an HTML fragment, typically a navigation bar,
    to determine the total number of pages. It looks for a specific `div` and then
    the last `a` tag's `href` attribute to extract the page count.

    Args:
        fwC (object): An object that provides HTML parsing methods (e.g., `getAllFrTagName`).
        parserf (function): A function to parse the URL string and extract the page count.
        ptype (str): The type of page to determine the correct parsing logic.
        divClass (str, optional): The CSS class of the `div` element containing the page links.
                                  Defaults to "page both".

    Returns:
        int: The total number of pages found, or 0 if not found.
    """
    count = 0
    # Get all div elements with the specified class name.
    oo1 = fwC.getAllFrTagName(tagName="div", clsName=divClass)
    
    # Check if any matching div elements were found.
    if len(oo1) > 0:
        # Get all list items (`li`) within the first matching div.
        oo2 = fwC.getAllFrTagName(tagName="li", iObj=oo1[0])
        # Check if any list items were found.
        if len(oo2) > 0:
            # Get all anchor tags (`a`) within the last list item.
            oo3 = fwC.getAllFrTagName(tagName="a", iObj=oo2[-1])
            # Check if an anchor tag was found.
            if len(oo3) > 0:
                # Get the 'href' attribute of the anchor tag.
                hf_ = oo3[0]["href"]
                # Use the parser function to extract the page count from the href.
                count = parserf(p=ptype, val=hf_)
    return count


def lastParseF(p, val):
    """
    A specific parser function to extract the page number from a URL string.

    This function is a utility for `findPageCount`. It splits the URL string
    based on underscores and periods to isolate the numerical page count.

    Args:
        p (str): A parameter indicating the parsing type (e.g., 'main').
        val (str): The URL string from which to extract the page number.

    Returns:
        int: The extracted page number.
    """
    # If the parsing type is 'main', split the string to get the page number.
    if p == "main":
        # Example: '/aiss/index_155.html' -> split by '_' -> ['/aiss/index', '155.html']
        # -> take the second part -> '155.html' -> split by '.' -> ['155', 'html']
        # -> take the first part -> '155' -> convert to int.
        return int(val.split("_")[1].split(".")[0])