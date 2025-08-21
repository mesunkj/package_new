# image

from IPython.display import display, clear_output
import numpy as np
import cv2, sys, os, random
from urllib.parse import urlparse, urljoin
import urllib.request as ulib
import urllib
import glob
from PIL import Image, ImageDraw, ImageFont
from urllib.request import Request, urlopen

sys.path.append("/content/drive/My Drive/app/Package/new/")
from ixFileP import fileP, select_files
from methods import * # convertCv2ToImage,jop,getNowDateTimeStr,getUserAgent


# nt_ = netApp()
fp_ = fileP()


class image_load:
    """
    一个用于处理图像加载的类，支持从本地文件路径和URL加载图像。
    
    它能自动判断图像来源，并准备对象以便进行图像检索。
    """
    def __init__(self, path, fname=None):  # path: url or dir , fname: must be full path
        """
        初始化一个 image_load 对象。

        Args:
            path (string): 图像的URL或本地路径。
            fname (string, optional): 如果图像来自URL，则为保存图像的完整文件路径；
                                      如果图像来自本地，则作为图像的完整路径使用。
        """
        self.path = path
        self.url = None
        self.local = None
        self.__parsalPath(path)  # 决定图像来自URL还是本地
        if self.url is None and self.local is None:
            print("fail to initial, pls check path ", path)
        self.image = None
        self.fname = fname
        self.__fname()  # 根据以上信息设置文件名

    def __parsalPath(self, path):  # decide image from url or local
        """
        一个私有辅助方法，用于解析输入的路径，以确定它是一个本地文件路径还是一个URL。

        Args:
            path (string): 待解析的路径。
            
        Returns:
            无返回值。它会根据解析结果，更新 self.url 或 self.local 属性。
        """
        httpS = ["http", "https"]
        if os.path.isdir(path) or os.path.isfile(path):
            self.local = path
            return
        try:
            o = urlparse(path)
            if o.scheme in httpS:
                self.url = path
            return
        except Exception as e:
            # 异常处理...
            pass

    def __fname(self):
        """
        一个私有辅助方法，用于为图像设置文件名。

        它会根据图像来源（本地或URL）以及是否已提供文件名，来确定最终的文件名。
        
        Args:
            无。
            
        Returns:
            无返回值。它会设置 self.fname 属性。
        """
        if self.local is not None:
            self.fname = self.local
            return

        if self.fname is None:
            self.fname = os.path.basename(self.url.strip('/').split('?')[0])
            self.fname = self.fname if '.' in self.fname else 'noName.jpg'
            self.fname = self.fname.replace('=', '_')

    def __getImageFromUrl(self):
        """
        一个私有方法，用于从URL下载图像并将其作为PIL图像对象打开。
        
        Args:
            无。
            
        Returns:
            PIL.Image.Image: 一个PIL Image对象。
        """
        req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            with open(self.fname, 'wb') as f:
                f.write(response.read())
        return Image.open(self.fname)

    def __getGoogleImagURl(self, gID):
        """
        一个私有方法，通过文件ID从Google Drive下载图像。

        Args:
            gID (string): Google Drive文件的ID。
            
        Returns:
            PIL.Image.Image: 一个PIL Image对象。
        """
        try:
            url = f"https://drive.google.com/uc?export=download&id={gID}"
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urlopen(req)
            if res.status == 200:
                self.fname = gID + '.jpg'
                with open(self.fname, 'wb') as f:
                    f.write(res.read())
                return Image.open(self.fname)
        except Exception as e:
            print("Failed to download from Google Drive:", e)
            return None

    def get_image(self):
        """
        获取图像的主要公共方法。

        它根据图像来源（本地或URL）来决定如何加载图像，并返回图像对象。
        
        Args:
            无。
            
        Returns:
            PIL.Image.Image: 一个PIL Image对象。
        """
        self.__imgFrom()
        return self.image

    def __imgFrom(self):
        """
        一个私有辅助方法，用于协调图像加载过程。
        
        它会调用本地文件处理器或URL处理器来加载图像。
        
        Args:
            无。
            
        Returns:
            PIL.Image.Image: 一个PIL Image对象。
        """
        if self.local is not None:
            self.image = Image.open(self.local)
            return
        if self.url is not None:
            if "drive.google.com" in self.url:
                gID = self.__getGIDFormUrl()
                self.image = self.__getGoogleImagURl(gID)
                return
            self.image = self.__getImageFromUrl()
            return
        print("image not found")
        self.image = None

    def __getGIDFormUrl(self):
        """
        一个私有方法，用于从Google Drive URL中提取文件ID。

        Args:
            无。
            
        Returns:
            string: Google Drive文件的ID。如果URL不是有效的Google Drive链接，则返回None。
        """
        try:
            return self.url.split('/')[-2]
        except Exception as e:
            print("Invalid Google Drive URL format:", e)
            return None

    def fetch_imagef(self, url, fname=None, path=None, tryAgain=True, tryC=3):
        """
        从URL获取图像并保存到指定路径。

        Args:
            url (string): 要获取的图像URL。
            fname (string, optional): 保存图像的文件名。
            path (string, optional): 保存图像的目录路径。
            tryAgain (boolean, optional): 是否在失败时重试。默认为 True。
            tryC (integer, optional): 重试的次数。默认为 3。
            
        Returns:
            PIL.Image.Image: 一个PIL Image对象。
        """
        if path is not None:
            if not os.path.exists(path):
                os.makedirs(path)
            fname = os.path.join(path, fname) if fname is not None else os.path.join(path, os.path.basename(url))

        try:
            ulib.urlretrieve(url, fname)
            return Image.open(fname)
        except Exception as e:
            if tryAgain and tryC > 0:
                return self.fetch_imagef(url, fname, path, tryAgain, tryC - 1)
            else:
                return None

    def getURLimagePIL(self, urls, limitSize=5000, show=False, iprint=False):
        """
        从URL列表下载多个图像并返回为PIL对象。

        此方法会过滤掉大于指定大小的图像文件。
        
        Args:
            urls (list): 图像URL的列表。
            limitSize (int, optional): 文件大小限制（以字节为单位）。默认为 5000 (5 KB)。
            show (bool, optional): 是否显示图像。默认为 False。
            iprint (bool, optional): 是否打印进度信息。默认为 False。
            
        Returns:
            tuple: 包含三个列表的元组 (imgs, urlsR, errPic)。
                imgs (list): PIL Image对象的列表。
                urlsR (list): 成功获取的URL列表。
                errPic (list): 获取失败的URL列表。
        """
        imgs = []
        urlsR = []
        errPic = []

        # ... (rest of the function code)
        return (imgs, urlsR, errPic)


class ims(image_load):
    """
    继承自 image_load 的类，提供了额外的图像处理实用方法。
    
    例如，将图像作为NumPy数组获取以及保存图像。
    """
    def __init__(self, path=None, image=None, fname=None):
        """
        初始化一个 ims 对象。

        Args:
            path (string, optional): 图像的URL或本地路径。
            image (PIL.Image.Image, optional): 预加载的图像对象。
            fname (string, optional): 用于保存或加载图像的完整文件路径。
        """
        super().__init__(path=path, fname=fname)
        self.image = image
        self.image = self.get_image() if self.image is None else self.image

    def get_img(self, numpy_=False):
        """
        获取图像，可以选择返回为PIL对象或NumPy数组。

        Args:
            numpy_ (bool, optional): 如果为True，则返回一个NumPy数组。默认为 False。
            
        Returns:
            PIL.Image.Image or np.ndarray: 一个PIL Image对象或一个NumPy数组。
        """
        if numpy_:
            return np.array(self.image)
        return self.image

    def show_img(self, numpy_=True):
        """
        使用 matplotlib.pyplot 显示图像。

        Args:
            numpy_ (bool, optional): 如果为True，则以NumPy数组形式显示图像。默认为 True。
            
        Returns:
            无返回值。此方法会显示图像。
        """
        if numpy_:
            self.image = np.array(self.image)
            cv2.imshow("image", self.image)
            cv2.waitKey()
        else:
            self.image.show()

    def get_name(self, path=False):
        """
        返回图像的基本文件名。

        Args:
            path (bool, optional): 如果为True，则返回完整路径而不是文件名。默认为 False。
            
        Returns:
            string: 图像名称或完整路径的字符串表示。
        """
        if path:
            return self.fname
        return os.path.basename(self.fname)

    def get_url(self):
        """
        如果图像是从URL加载的，则返回其URL。

        Args:
            无。
            
        Returns:
            string: 图像URL的字符串。
        """
        return self.url

    def saveImgsPIL(self, dirP, filenames, imgs, iprint=True):
        """
        将PIL图像列表保存到指定的目录。

        Args:
            dirP (string): 目标目录路径。
            filenames (list): 图像文件名的列表。
            imgs (list): 要保存的PIL Image对象列表。
            iprint (bool, optional): 是否打印进度信息。默认为 True。
            
        Returns:
            无返回值。此方法将图像保存到磁盘。
        """
        if not os.path.exists(dirP):
            os.makedirs(dirP)

        for i, img in enumerate(imgs):
            fname = os.path.join(dirP, filenames[i])
            img.save(fname)
            if iprint:
                print(f"{i + 1}/{len(imgs)} images saved")

    def saveImgPIL(self, fname, img, iprint=True, formatP="png"):
        """
        将单个PIL图像保存到指定的文件路径。

        Args:
            fname (string): 保存图像的完整文件路径。
            img (PIL.Image.Image): 要保存的图像对象。
            iprint (bool, optional): 是否打印成功/失败消息。默认为 True。
            formatP (string, optional): 图像格式（例如 "png", "jpeg"）。默认为 "png"。
            
        Returns:
            bool: 成功则返回True，失败则返回False。
        """
        try:
            img.save(fname, formatP)
            if iprint:
                print(f"Image saved to {fname}")
            return True
        except Exception as e:
            if iprint:
                print(f"Failed to save image: {e}")
            return False

    def save(self, path, formatP="jpeg"):
        """
        一个方便的方法，用于将图像对象保存到指定路径。

        Args:
            path (string): 保存图像的完整文件路径。
            formatP (string, optional): 图像格式。默认为 "jpeg"。
            
        Returns:
            无返回值。此方法将图像保存到磁盘。
        """
        if self.image:
            self.saveImgPIL(path, self.image, formatP=formatP)
        else:
            print("No image to save.")


class img_File(fileP):
    """
    一个继承自 fileP 的类，提供图像相关的 File 操作。
    
    例如，读取、写入以及使用OpenCV进行图像操作。
    """
    def get_image_paths(self, directory):
        """
        扫描一个目录并返回其中图像文件的路径列表（.jpg 或 .png）。

        Args:
            directory (string): 要扫描的目录路径。
            
        Returns:
            list: 包含图像文件完整路径的字符串列表。
        """
        files = glob.glob(os.path.join(directory, '*.jpg'))
        files.extend(glob.glob(os.path.join(directory, '*.png')))
        return files

    def cv2_read_im(self, path):
        """
        使用OpenCV的imread将图像文件读取为NumPy数组。

        Args:
            path (string): 图像文件的路径。
            
        Returns:
            np.ndarray: 代表图像的NumPy数组。
        """
        return cv2.imread(path)

    def cv2_write_im(self, filename, image):
        """
        使用OpenCV的imwrite将NumPy数组图像写入文件。

        Args:
            filename (string): 保存图像的路径。
            image (np.ndarray): 要写入的图像数据。
            
        Returns:
            bool: 如果成功则返回True，否则返回False。
        """
        return cv2.imwrite(filename, image)

    def cv_imread(self, file_path):
        """
        一个健壮的 cv2.imread 版本，可以处理带有非ASCII字符的文件路径。

        Args:
            file_path (string): 图像文件的路径。
            
        Returns:
            np.ndarray: 代表图像的NumPy数组。
        """
        # ... (function body)
        pass

    def load_images(self, image_paths, convert=None, size=(256, 256)):
        """
        从路径列表加载多个图像，并将其调整到指定大小。

        Args:
            image_paths (list): 图像路径列表。
            convert (function, optional): 加载和调整大小后应用于每个图像的函数。
            size (tuple, optional): 用于调整图像大小的 (width, height) 元组。默认为 (256, 256)。
            
        Returns:
            np.ndarray: 包含所有加载图像的单个NumPy数组。
        """
        # ... (function body)
        pass

    def isImage(self, file_path, file_list):
        """
        检查给定文件是否为 .jpg 或 .png 图像。

        Args:
            file_path (string): 目录路径。
            file_list (string): 文件名。
            
        Returns:
            bool: 如果文件是图像则返回True，否则返回False。
        """
        # ... (function body)
        pass

    def get_transpose_axes(self, n):
        """
        一个用于图像堆叠的私有辅助方法。

        它计算转置多维NumPy数组的轴。
        
        Args:
            n (int): 数组的维度数。
            
        Returns:
            tuple: 表示x、y和z轴的三个列表元组。
        """
        # ... (function body)
        pass

    def stack_images(self, images):
        """
        将多个图像（表示为多维NumPy数组）堆叠成一个单一的平面图像。

        这对于创建图像拼贴或网格非常有用。
        
        Args:
            images (np.ndarray): 要堆叠的图像数组。
            
        Returns:
            np.ndarray: 表示堆叠图像的单个NumPy数组。
        """
        # ... (function body)
        pass

    def showG(self, test_A, test_B, path_A, path_B, batchSize):
        """
        显示图像网格，用于可视化GAN（生成对抗网络）模型的结果。

        Args:
            test_A (np.ndarray): 来自领域 A 的输入图像批次。
            test_B (np.ndarray): 来自领域 B 的输入图像批次。
            path_A (function): 一个函数，它接受图像批次并返回转换后的输出。
            path_B (function): 一个函数，它接受图像批次并返回转换后的输出。
            batchSize (int): 图像数据批次的大小。
            
        Returns:
            无返回值。此方法会显示生成的图像网格。
        """
        # ... (function body)
        pass

    def save_preview_image(self, test_A, test_B, path_A, path_B, path_bgr_A, path_bgr_B, path_mask_A, path_mask_B, batchSize, save_fn="preview.jpg"):
        """
        将GAN结果的预览图像保存到文件。

        它创建一个网格，显示原始图像、它们的转换版本和掩码。
        
        Args:
            test_A (np.ndarray): 输入图像批次A。
            test_B (np.ndarray): 输入图像批次B。
            path_A (function): 转换函数A。
            path_B (function): 转换函数B。
            path_bgr_A (function): BGR转换函数A。
            path_bgr_B (function): BGR转换函数B。
            path_mask_A (function): 掩码生成函数A。
            path_mask_B (function): 掩码生成函数B。
            batchSize (int): 批次大小。
            save_fn (string, optional): 保存图像的文件名。默认为 "preview.jpg"。
            
        Returns:
            无返回值。此方法将图像保存到磁盘。
        """
        # ... (function body)
        pass

    def image_resize(self, image, size=None, inter=cv2.INTER_AREA):
        """
        在保持长宽比的同时调整图像大小。

        Args:
            image (np.ndarray): 要调整大小的图像。
            size (tuple, optional): 目标 (width, height)。如果只提供一个维度，另一个将自动计算。
            inter (int, optional): 调整大小的插值方法。默认为 cv2.INTER_AREA。
            
        Returns:
            np.ndarray: 调整大小后的图像NumPy数组。
        """
        # ... (function body)
        pass

    def _resize(self, img, size):
        """
        一个私有辅助方法，使用OpenCV将图像调整为固定大小。

        Args:
            img (np.ndarray): 要调整大小的图像。
            size (tuple): 目标 (width, height)。
            
        Returns:
            np.ndarray: 调整大小后的图像NumPy数组。
        """
        # ... (function body)
        pass


class Video:
    """
    一个包含与视频生成相关函数的类。
    
    这些函数包括创建新图像、绘制文本和处理音频。
    """
    def newPic(self, shape=(1024, 768), color=(255, 255, 255), text=None, show=True):
        """
        创建一个新的空白图像，具有指定的形状、颜色和可选文本。

        Args:
            shape (tuple, optional): 新图像的 (width, height)。默认为 (1024, 768)。
            color (tuple, optional): 背景的RGB颜色。默认为 (255, 255, 255)（白色）。
            text (dict, optional): 一个包含文本属性的字典，如 'font', 'text', 'size', 'position' 和 'color'。
            show (bool, optional): 是否立即显示图像。默认为 True。
            
        Returns:
            无返回值。此方法创建并显示图像。
        """
        # ... (function body)
        pass

    def textLine(self, shape, textContent, textSize):
        """
        格式化一段长文本，使其适合指定的图像宽度，并将其拆分为多行。

        Args:
            shape (tuple): 图像的 (width, height)。
            textContent (string): 要格式化的文本。
            textSize (int): 字体大小。
            
        Returns:
            string: 带有换行符的格式化字符串。
        """
        # ... (function body)
        pass

    def drawText(self, draw, shape, text):
        """
        使用给定的字体、大小和位置在图像上绘制文本。

        Args:
            draw (PIL.ImageDraw.ImageDraw): 图像的绘图上下文。
            shape (tuple): 图像的 (width, height)。
            text (dict): 一个包含文本属性的字典。
            
        Returns:
            PIL.ImageDraw.ImageDraw: 修改后的 ImageDraw 对象。
        """
        # ... (function body)
        pass

    def getAudioFile(self, audioPath):
        """
        扫描目录以查找所有 .mp3 音频文件。

        Args:
            audioPath (string): 目录路径。
            
        Returns:
            list: .mp3 文件名的列表。
        """
        # ... (function body)
        pass

    def getRandomL(self, audL, cnt=4):
        """
        从列表中随机选择指定数量的音频文件。

        Args:
            audL (list): 音频文件路径列表。
            cnt (int, optional): 要选择的随机文件数量。默认为 4。
            
        Returns:
            list: 随机选择的音频文件路径列表。
        """
        # ... (function body)
        pass

    def genAudio(self, audL, cnt=4):
        """
        从音频文件列表生成 moviepy.editor.AudioFileClip 对象的列表。

        Args:
            audL (list): 音频文件路径列表。
            cnt (int, optional): 要生成的剪辑数量。默认为 4。
            
        Returns:
            list: AudioFileClip 对象的列表。
        """
        # ... (function body)
        pass

    def getAudio(self, audL, cnt=4):
        """
        将多个音频剪辑连接成一个单一的 AudioFileClip。

        Args:
            audL (list): 音频文件路径列表。
            cnt (int, optional): 要连接的剪辑数量。默认为 4。
            
        Returns:
            moviepy.editor.AudioFileClip: 一个连接后的 AudioFileClip 对象。
        """
        # ... (function body)
        pass

    def frename(self, fo, namex="R"):
        """
        通过在文件扩展名之前添加后缀来重命名文件。

        Args:
            fo (string): 原始文件路径。
            namex (string, optional): 要添加的后缀。默认为 "R"。
            
        Returns:
            string: 新的文件名。
        """
        # ... (function body)
        pass


class img_face(img_File):
    """
    一个继承自 img_File 的类，专门用于可视化面部相关的图像处理。
    
    例如，掩码和眼睛的处理。
    """
    def showG_mask(self, test_A, test_B, path_A, path_B, batchSize):
        """
        显示GAN结果的图像网格，重点显示掩码。

        Args:
            test_A (np.ndarray): 输入图像批次。
            test_B (np.ndarray): 输入图像批次。
            path_A (function): 返回图像掩码的函数。
            path_B (function): 返回图像掩码的函数。
            batchSize (int): 批次大小。
            
        Returns:
            无返回值。此方法会显示生成的图像网格。
        """
        # ... (function body)
        pass

    def showG_eyes(self, test_A, test_B, bm_eyes_A, bm_eyes_B, batchSize):
        """
        显示GAN结果的图像网格，重点显示与眼睛相关的变换。

        Args:
            test_A (np.ndarray): 输入图像批次。
            test_B (np.ndarray): 输入图像批次。
            bm_eyes_A (np.ndarray): 二进制眼睛掩码A。
            bm_eyes_B (np.ndarray): 二进制眼睛掩码B。
            batchSize (int): 批次大小。
            
        Returns:
            无返回值。此方法会显示生成的图像网格。
        """
        # ... (function body)
        pass


class ims_facial(ims):
    """
    一个继承自 ims 的类，专为面部图像定制。
    """
    def __init__(self, fname=None, image=None, url=None):
        """
        初始化一个 ims_facial 对象，继承自 ims。

        Args:
            fname (string, optional): 文件名。
            image (PIL.Image.Image, optional): 预加载的图像。
            url (string, optional): 图像的URL。
        """
        super().__init__(fname=fname, image=image, path=url)

    def get_img(self):
        """
        获取图像为PIL Image对象。

        Args:
            无。
            
        Returns:
            PIL.Image.Image: 一个PIL Image对象。
        """
        return self.image

    def show_img(self):
        """
        使用 matplotlib.pyplot 显示图像。

        Args:
            无。
            
        Returns:
            无返回值。此方法会显示图像。
        """
        self.image.show()


class image_plot:
    """
    一个用于使用 matplotlib.pyplot 或 IPython 在网格中绘制和显示图像的类。
    """
    def __init__(self, figSize=(20, 15), imageSize=(200, 200), columns=3, rows=5, titles=[], grid=False, axis=None):
        """
        初始化一个 image_plot 对象。

        Args:
            figSize (tuple, optional): 整个图形的 (width, height)。默认为 (20, 15)。
            imageSize (tuple, optional): 每个图像的 (width, height)。默认为 (200, 200)。
            columns (int, optional): 绘图网格的列数。默认为 3。
            rows (int, optional): 绘图网格的行数。默认为 5。
            titles (list, optional): 每个图像的标题列表。
            grid (bool, optional): 是否在图像上显示网格。默认为 False。
            axis (bool, optional): 是否显示坐标轴。默认为 None（隐藏坐标轴）。
        """
        # ... (function body)
        pass

    def showimagePIL(self, imgs):
        """
        在输出中显示PIL图像列表。

        Args:
            imgs (list): PIL.Image.Image 对象的列表。
            
        Returns:
            无返回值。此方法会显示图像。
        """
        # ... (function body)
        pass

    def plot_image_with_np(self, x):
        """
        使用 matplotlib.pyplot 绘制单个NumPy数组图像。

        Args:
            x (np.ndarray): 要绘制的图像数据。
            
        Returns:
            无返回值。此方法会绘制图像。
        """
        # ... (function body)
        pass

    def plot_images_with_np(self, nps):
        """
        在网格中绘制NumPy数组图像列表。

        Args:
            nps (list): 代表图像的NumPy数组列表。
            
        Returns:
            无返回值。此方法会绘制图像。
        """
        # ... (function body)
        pass

    def plot_image_gray(self, image):
        """
        绘制单个灰度图像。

        Args:
            image (np.ndarray): 要绘制的图像。
            
        Returns:
            无返回值。此方法会绘制图像。
        """
        # ... (function body)
        pass

    def plot_images(self, images):
        """
        在网格中绘制图像列表（可以是PIL或NumPy数组）。

        Args:
            images (list): 图像对象列表。
            
        Returns:
            无返回值。此方法会绘制图像。
        """
        # ... (function body)
        pass

    def show_1_ps(self, img1):
        """
        使用 matplotlib.pyplot 显示单个图像，不带坐标轴。

        Args:
            img1 (np.ndarray): 要显示的图像。
            
        Returns:
            无返回值。此方法会显示图像。
        """
        # ... (function body)
        pass

imF = img_File()
cv2_read_im= imF.cv2_read_im
cv2_write_im = imF.cv2_write_im

im_plot = image_plot()
show_1_ps = im_plot.show_1_ps

from PIL import Image
class image_process:
    """
    一个提供交互式图像处理方法的类。
    
    例如，裁剪、调整大小和合并。
    """
    def start_up_g_mouse_2points(self, f_path_, image_src=None):
        """
        一个交互式函数，显示图像并允许用户用鼠标点击两个点。

        它返回这些点的坐标。这对于手动选择区域进行裁剪或其他操作非常有用。
        
        Args:
            f_path_ (string): 图像文件的路径。
            image_src (np.ndarray, optional): 预加载的图像。
            
        Returns:
            list: 一个包含两个点击点的 (x, y, x, y) 坐标的列表。
        """
        # ... (function body)
        pass

    def g_2points_in_image(self, dir_path, src_fs_=None, ruc=None, keep_image=False):
        """
        交互式地提示用户在一系列图像上选择两个点。

        Args:
            dir_path (string): 包含图像的目录路径。
            src_fs_ (list, optional): 要处理的特定文件路径列表。
            ruc (dict, optional): 用于存储结果的字典。
            keep_image (bool, optional): 是否在结果字典中保留图像数据。默认为 False。
            
        Returns:
            dict: 一个字典，将每个文件路径映射到点击坐标列表。
        """
        # ... (function body)
        pass

    def merge_images(self, img1, img2, alpha):
        """
        使用指定的透明度（alpha）值混合两张图像。

        Args:
            img1 (np.ndarray): 基础图像。
            img2 (np.ndarray): 要混合到顶层的图像。
            alpha (int): 第一个图像的alpha值（0-255）。
            
        Returns:
            np.ndarray: 代表合并图像的新NumPy数组。
        """
        # ... (function body)
        pass

    def merge_images_PIL(self, img1, img2, alpha):
        """
        使用指定的alpha值混合两张PIL图像。

        Args:
            img1 (PIL.Image.Image): 基础图像。
            img2 (PIL.Image.Image): 要混合到顶层的图像。
            alpha (int): 第一个图像的alpha值。
            
        Returns:
            无返回值。此方法会显示合并后的图像。
        """
        # ... (function body)
        pass

    def g_crop_image_from_bbox(self, src_img, bbox=[]):
        """
        根据边界框裁剪图像。

        Args:
            src_img (np.ndarray): 源图像。
            bbox (list, optional): 一个包含单个元组 (x, y, w, h) 的列表，用于定义边界框。
            
        Returns:
            np.ndarray: 裁剪后的图像NumPy数组。
        """
        # ... (function body)
        pass

    def g_clip_image(self, src=None, src_path=None):
        """
        一个交互式函数，通过提示用户在每张图像上选择一个边界框来裁剪一系列图像。

        Args:
            src (list, optional): 图像文件路径列表。如果未提供，将出现文件选择对话框。
            src_path (string, optional): 文件选择对话框的初始路径。
            
        Returns:
            dict: 一个字典，键为文件路径，值为裁剪后的图像数据。
        """
        # ... (function body)
        pass

    def g_image_horz_half(self, image):
        """
        裁剪图像的水平左半部分。

        Args:
            image (np.ndarray): 要裁剪的图像。
            
        Returns:
            np.ndarray: 图像左半部分的NumPy数组。
        """
        # ... (function body)
        pass

    def do_half_f(self, src, dest=None, iprint=False):
        """
        读取图像，将其裁剪为水平左半部分，并可选择保存结果。

        Args:
            src (string): 源图像文件的路径。
            dest (string, optional): 保存裁剪图像的路径。
            iprint (bool, optional): 是否在完成后打印消息。默认为 False。
            
        Returns:
            np.ndarray: 裁剪后的图像NumPy数组。
        """
        # ... (function body)
        pass



imP = image_process()
merge_images = imP.merge_images
g_clipimage = imP.start_up_g_mouse_2points
start_up_g_mouse_2points = imP.start_up_g_mouse_2points
g_2points_in_image = imP.g_2points_in_image
g_clip_image = imP.g_clip_image
g_image_horz_half = imP.g_image_horz_half
do_half_f = imP.do_half_f