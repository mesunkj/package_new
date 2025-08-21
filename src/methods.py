import os
import os, sys, time
import collections
import cv2
import argparse
import matplotlib.pyplot as plt
from PIL import Image
import urllib.request
import requests
import numpy, numpy as np
from numpy import asarray
from urllib.parse import urlparse
from datetime import datetime
import random, math
import pickle
from os.path import splitext, basename
import zipfile

try:
    sys.path.append("/content/drive/My Drive/app/Package/new")
    from ixStockProperty import USProperty
    _P = USProperty()
except:
    pass

googlepath = "/concent/drive/MyDrive/tmp/google_grapse_out/"


# Get current date-time string in a given format
def getNowDateTimeStr(format="%y%m%d %H%M%S%f"):
    """
    Return current date-time string formatted according to `format`.

    Args:
        format (str): Datetime format string. Defaults to "%y%m%d %H%M%S%f".

    Returns:
        str: Formatted datetime string.
    """
    date_time = datetime.now()
    return date_time.strftime(format)


# Generate a random image filename with timestamp
def getRandomImgName(prefix=None, ext=".jpg"):
    """
    Generate a random image filename consisting of a prefix, current datetime, and extension.

    Args:
        prefix (str, optional): Prefix for the filename. Defaults to "img".
        ext (str, optional): File extension. Defaults to ".jpg".

    Returns:
        str: Generated filename in the format '<prefix>_<datetime><ext>'.
    """
    prefix = prefix if prefix is not None else "img"
    return prefix + "_" + getNowDateTimeStr() + ext


g_riName = getRandomImgName


# Convert between cv2 image and PIL Image
def convertCv2ToImage(img, reverse=False, color=cv2.COLOR_RGB2BGR):
    """
    Convert between cv2 image (numpy array) and PIL Image depending on `reverse`.

    Args:
        img (numpy.ndarray or PIL.Image.Image): Input image.
        reverse (bool): If True, convert PIL to cv2 format. Defaults to False.
        color (int): cv2 color conversion flag. Defaults to cv2.COLOR_RGB2BGR.

    Returns:
        numpy.ndarray or PIL.Image.Image: Converted image.
    """
    if reverse:
        return cv2.cvtColor(numpy.asarray(img), color) if (type(img) != numpy.ndarray) else img
    return Image.fromarray(cv2.cvtColor(img, color)) if (type(img) == numpy.ndarray) else img


cvR = convertCv2ToImage


# Get a user-agent string
def getUserAgent(id_=-1):
    """
    Return a random user-agent string from USProperty list, or by index if provided.

    Args:
        id_ (int): Index of user agent. Random if -1. Defaults to -1.

    Returns:
        str: User-agent string.
    """
    if id_ < 0:
        id_ = random.randint(0, len(_P.user_agent) - 1)
    return _P.user_agent[id_]


# Download image from URL
def getImagFromUrl(url, fname=None, path=None, ext=None):
    """
    Download an image from a given URL and return it as a PIL Image object.

    Args:
        url (str): URL of the image.
        fname (str, optional): Output filename. Defaults to None.
        path (str, optional): Directory to save file. Defaults to None.
        ext (str, optional): File extension. Defaults to None.

    Returns:
        PIL.Image.Image: Downloaded image.
    """
    fname = "test_src" + "_" + getNowDateTimeStr(format="%y%m%d_%H%M%S") + ext if fname is None else fname
    if path is not None:
        fname = os.path.join(path, fname)
    try:
        urllib.request.urlretrieve(url, fname)
    except Exception:
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-Agent", getUserAgent())]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, fname)
    return Image.open(fname)


# Download multiple images from URLs (stub)
def getImagesFromUrl(urls, fname=None, ext=".jpg", path="/content/drive/My Drive/app/AI/out/tmp"):
    """
    Download multiple images from URLs. (Not implemented)

    Args:
        urls (list): List of image URLs.
        fname (str, optional): Output filename template. Defaults to None.
        ext (str, optional): Extension of saved images. Defaults to ".jpg".
        path (str, optional): Directory to save images. Defaults to specific path.

    Returns:
        None
    """
    pass


# Download image from Google Drive by ID
def getGoogleImagURl(gID, fname="test_src.png"):
    """
    Download an image from Google Drive using its file ID.

    Args:
        gID (str): Google Drive file ID.
        fname (str): Output filename. Defaults to "test_src.png".

    Returns:
        PIL.Image.Image: Downloaded image.
    """
    file2 = requests.get("https://drive.google.com/uc?export=download&confirm=9_s_&id=" + gID)
    f = open(fname, "wb").write(file2.content)
    return Image.open(fname)


# Fetch single image
def get_1Img(url, gID, fname="test.jpg"):
    """
    Fetch a single image either from a URL or Google Drive.

    Args:
        url (str): Image URL.
        gID (str): Google Drive ID.
        fname (str): Output filename. Defaults to "test.jpg".

    Returns:
        PIL.Image.Image: Downloaded image.
    """
    return imgFrom(url, gID, fname)


# Fetch two images (src, dst)
def getOImg(src, dst):
    """
    Fetch two images (source and destination) given metadata dictionaries.

    Args:
        src (dict): Dictionary with 'url', 'gID', and 'fname'.
        dst (dict): Dictionary with 'url', 'gID', and 'fname'.

    Returns:
        list: [src_image, dst_image] as PIL Images.
    """
    src_img = imgFrom(src["url"], src["gID"], src["fname"])
    dst_img = imgFrom(dst["url"], dst["gID"], dst["fname"])
    return [src_img, dst_img]


# Get image from URL or Google Drive
def imgFrom(url, gID=None, fname="2.png"):
    """
    Return image from URL or Google Drive ID depending on arguments.

    Args:
        url (str): Image URL.
        gID (str, optional): Google Drive ID. Defaults to None.
        fname (str): Output filename. Defaults to "2.png".

    Returns:
        PIL.Image.Image: Downloaded image.
    """
    if gID is None:
        return getImagesFromUrl([url])[0]
    else:
        return getGoogleImagURl(gID, fname=fname)


# Extract Google Drive file ID
def getGIDFormUrl(url):
    """
    Extract Google Drive file ID from a share URL.

    Args:
        url (str): Google Drive share URL.

    Returns:
        str or None: Extracted file ID or None if invalid.
    """
    o = urlparse(url)
    if o.netloc == "drive.google.com":
        return os.path.split(os.path.split(o.path)[0])[1]
    return None


# Get filename and extension from web address
def getfnameFromWebAddress(urls):
    """
    Return filename, extension, and full filename for each given web URL.

    Args:
        urls (list): List of web URLs.

    Returns:
        list: List of [filename, extension, filename+extension].
    """
    xpath = []
    for url in urls:
        disassembled = urlparse(url)
        filename, file_ext = splitext(basename(disassembled.path))
        xpath.append([filename, file_ext, "".join([filename, file_ext])])
    return xpath


# Plot numpy image
def plot_image_with_np(x):
    """
    Plot a numpy array image with values adjusted/clipped between 0 and 1.

    Args:
        x (numpy.ndarray): Input image array.

    Returns:
        None
    """
    plt.imshow(np.clip(x + 0.5, 0, 1))


# Plot multiple numpy images in grid
def plot_images_with_np(nps, figSize=(20, 15), imageSize=(200, 200), columns=3, rows=5):
    """
    Plot multiple numpy array images in a grid layout.

    Args:
        nps (list): List of numpy array images.
        figSize (tuple): Figure size. Defaults to (20, 15).
        imageSize (tuple): Image resize dimensions. Defaults to (200, 200).
        columns (int): Number of columns. Defaults to 3.
        rows (int): Number of rows. Defaults to 5.

    Returns:
        None
    """
    w, h = imageSize
    fig = plt.figure(figsize=figSize)
    if len(nps) > columns * rows:
        rows = int(len(nps) / columns)
    for i in range(1, columns * rows + 1):
        if i - 1 < len(nps):
            fig.add_subplot(rows, columns, i)
            plt.imshow(nps[i - 1])
    plt.show()


# Plot grayscale image
def plot_image_gray(image, size=(20, 10), adjust=False):
    """
    Display a single grayscale image.

    Args:
        image (numpy.ndarray or PIL.Image.Image): Grayscale image.
        size (tuple): Figure size. Defaults to (20, 10).
        adjust (bool): Placeholder argument, unused. Defaults to False.

    Returns:
        None
    """
    plt.figure(figsize=size)
    plt.imshow(image, cmap="gray")
    plt.show()


# Plot multiple images
def plot_images(images, figSize=(20, 15), imageSize=(200, 200), columns=3, rows=5, reverse=True):
    """
    Plot multiple images (PIL or cv2) in a grid layout.

    Args:
        images (list): List of images (PIL or numpy arrays).
        figSize (tuple): Figure size. Defaults to (20, 15).
        imageSize (tuple): Resize dimensions. Defaults to (200, 200).
        columns (int): Number of columns. Defaults to 3.
        rows (int): Number of rows. Defaults to 5.
        reverse (bool): Whether to convert cv2 images to PIL. Defaults to True.

    Returns:
        None
    """
    cvR = convertCv2ToImage
    if type(images[0]) == numpy.ndarray:
        images = [cvR(img) for img in images]
    w, h = imageSize
    fig = plt.figure(figsize=figSize)
    if len(images) > columns * rows:
        rows = int(len(images) / columns)
    for i in range(1, columns * rows + 1):
        if i - 1 < len(images):
            imgAry = cv2.resize(cvR(images[i - 1], reverse=reverse), dsize=(h, w))
            fig.add_subplot(rows, columns, i)
            plt.imshow(cvR(imgAry))
    plt.show()


# Plot images in single row
def plot_images_x1(images, size=(20, 10), adjust=False, nrow=8, savefig=None, list_titles=None):
    """
    Plot multiple images in a single row using matplotlib subplots.

    Args:
        images (list): List of images.
        size (tuple): Figure size. Defaults to (20, 10).
        adjust (bool): Placeholder argument. Defaults to False.
        nrow (int): Number of rows (unused). Defaults to 8.
        savefig (str, optional): Path to save figure. Defaults to None.
        list_titles (list, optional): Titles for images. Defaults to None.

    Returns:
        None
    """
    print("len of images ", len(images))
    if len(images) == 1:
        plt.imshow(images[0])
        plt.show()
        return
    plt.figure(figsize=size)
    fig, ax = plt.subplots(1, len(images))
    for i in range(len(images)):
        ax[i].imshow(images[i])
    plt.show()


# Plot images vertically (stub)
def plot_images_v(images, figSize=(20, 15), imageSize=(200, 200), columns=3, rows=5, titles=None, grid=None, axis=None):
    """
    Plot images vertically. (Not implemented)

    Args:
        images (list): List of images.
        figSize (tuple): Figure size.
        imageSize (tuple): Image size.
        columns (int): Number of columns.
        rows (int): Number of rows.
        titles (list, optional): Titles. Defaults to None.
        grid (bool, optional): Grid display. Defaults to None.
        axis (bool, optional): Axis display. Defaults to None.

    Returns:
        None
    """
    pass


# Class for holding input arguments
class argInput:
    """
    Class to hold input arguments for image transformation or processing.

    Attributes:
        src (str): Source path.
        dst (str): Destination path.
        out (str): Output path.
        warp_2d (bool): Flag for 2D warp.
        correct_color (bool): Flag for color correction.
        no_debug_window (bool): Disable debug window.
    """

    def __init__(self, src, dst, out, warp_2d=False, correct_color=False, no_debug_window=False):
        self.src = src
        self.dst = dst
        self.out = out
        self.warp_2d = warp_2d
        self.correct_color = correct_color
        self.no_debug_window = no_debug_window

    def show(self):
        """
        Print argument values.

        Returns:
            None
        """
        print(" src ", self.src)
        print(" dst ", self.dst)
        print(" out ", self.out)


# Save dictionary to file
def saveDictWithPD(dicDate, f1):
    """
    Save a dictionary to a file using pickle.

    Args:
        dicDate (dict): Dictionary to save.
        f1 (str): File path.

    Returns:
        None
    """
    with open(f1, "wb") as f:
        pickle.dump(dicDate, f)


# Load dictionary from file
def readDictWithPD(f1):
    """
    Load and return a dictionary from a pickle file.

    Args:
        f1 (str): Path to pickle file.

    Returns:
        dict: Loaded dictionary.
    """
    with open(f1, "rb") as f:
        dict_ = pickle.load(f)
    return dict_


# Join path and name
def jop(path, name):
    """
    Join path and name safely.

    Args:
        path (str): Directory path.
        name (str): File name.

    Returns:
        str: Joined file path.
    """
    return os.path.join(path, name) if path is not None else name


# Round up to fixed decimals
def tofix(valx, fix=2):
    """
    Round up a value to a fixed number of decimal places.

    Args:
        valx (float): Input value.
        fix (int): Number of decimal places. Defaults to 2.

    Returns:
        float: Rounded up value.
    """
    n = 10 ** fix
    return math.ceil(valx * n) / n


# Create a zip archive
def create_zip_file(zipName, contents):
    """
    Create a zip archive containing the given list of file paths.

    Args:
        zipName (str): Output zip filename.
        contents (list): List of file paths.

    Returns:
        None
    """
    with zipfile.ZipFile(zipName, mode="w") as zf:
        for f_ in contents:
            zf.write(f_)
    print("done , forward ", zipName)

# Extract from zip archive
def extract_zip_file(zipName, outDir=None, zNames=[], limitCnt=0):
    """
    Extract files from a zip archive, with optional filtering and extraction limit.

    Args:
        zipName (str): Path to the zip file.
        outDir (str, optional): Output directory. Defaults to None (current directory).
        zNames (list, optional): Specific filenames to extract. Defaults to [].
        limitCnt (int, optional): Maximum number of files to extract. Defaults to 0 (no limit).

    Returns:
        int: Number of files extracted.
    """
    cnt = 0
    with zipfile.ZipFile(zipName, "r") as zf:
        for name in zf.namelist():
            if len(zNames) > 0 and name not in zNames:
                continue
            nameC = name if outDir is None else os.path.join(outDir, name)
            if not os.path.isfile(nameC):
                zf.extract(name, path=outDir)
                cnt += 1
            if limitCnt > 0 and cnt > limitCnt:
                return cnt
    return cnt


# Get list of files in directory
def getListOfFiles(dirName, ext=[], statInfo=False, verbose=False, sub=True, sort=False):
    """
    Return a list of files (recursively if sub=True) with optional extension filter.

    Args:
        dirName (str): Directory path.
        ext (list, optional): List of file extensions to filter. Defaults to [].
        statInfo (bool, optional): Whether to include os.stat info. Defaults to False.
        verbose (bool, optional): Verbose output flag. Defaults to False.
        sub (bool, optional): Recurse into subdirectories. Defaults to True.
        sort (bool, optional): Sort the result list. Defaults to False.

    Returns:
        list: List of file paths (or [path, stat] if statInfo=True).
    """
    listOfFile = os.listdir(dirName)
    allFiles = []
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath) and sub:
            allFiles = allFiles + getListOfFiles(fullPath, ext=ext, statInfo=statInfo, verbose=verbose)
        else:
            addin = True
            if len(ext) > 0 and os.path.splitext(fullPath)[1] not in ext:
                addin = False
            if addin:
                if not statInfo:
                    allFiles.append(fullPath)
                else:
                    allFiles.append([fullPath, os.stat(fullPath)])
    if sort:
        allFiles.sort()
    return allFiles


# Get image file paths from directory
def get_image_paths(directory, ext=[".jpg", ".png"]):
    """
    Return a list of image file paths from a directory matching given extensions.

    Args:
        directory (str): Directory path.
        ext (list): Allowed file extensions. Defaults to [".jpg", ".png"].

    Returns:
        list: List of image file paths.
    """
    return [x.path for x in os.scandir(directory) if x.name.endswith in ext]


# Get file components by path
def g_file_name_by_path(path, get_=["PATH"]):
    """
    Return requested components (PATH, EXT, NAME) from a file path.

    Args:
        path (str): File path.
        get_ (list): Components to retrieve. Options: PATH, EXT, NAME.

    Returns:
        list: List of requested components.
    """
    fC = []
    fd, ext = os.path.splitext(path)
    fd_, f = os.path.split(path)
    for cd in get_:
        if cd == "PATH":
            fC.append(fd_)
        if cd == "EXT":
            fC.append(ext)
        if cd == "NAME":
            fC.append(f)
    return fC


# Get all file paths in directory
def getfilepath(path):
    """
    Return all file paths in the given directory.

    Args:
        path (str): Directory path.

    Returns:
        list: List of file paths.
    """
    return getListOfFiles(path)


# Count number of files in directory
def countfiles(path):
    """
    Return number of files in the given directory.

    Args:
        path (str): Directory path.

    Returns:
        int: File count.
    """
    return len(getfilepath(path))


# Print duplicated items in list
def listDuplicated(list_):
    """
    Print items that are duplicated in the given list.

    Args:
        list_ (list): Input list.

    Returns:
        None
    """
    print([item for item, count in collections.Counter(list_).items() if count > 1])


# Get file information
def g_file_info(f_, file_state=None):
    """
    Return file information (path, name, basename, ext, parent folder, full path, optional state).

    Args:
        f_ (str): File path.
        file_state (bool, optional): Whether to include os.stat info. Defaults to None.

    Returns:
        dict: Dictionary with file information.
    """
    path, f_name = os.path.split(f_)
    basename, ext = os.path.splitext(f_name)
    res_ = {
        "path": path,
        "file_name": f_name,
        "basename": basename,
        "ext": ext,
        "parent_fd": os.path.basename(path),
        'full_path': f_
    }
    if file_state is not None:
        res_['file_state'] = os.stat(f_)
    return res_
