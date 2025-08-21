# image

from IPython.display import display,clear_output
import numpy as np
import cv2, sys, os, random
from urllib.parse import urlparse, urljoin
import urllib.request as ulib
import urllib

# import moviepy.editor as mpe
import glob
from PIL import Image, ImageDraw, ImageFont

sys.path.append("/content/drive/My Drive/app/Package/new/")
from ixFileP import fileP, select_files
from methods import *  # convertCv2ToImage,jop,getNowDateTimeStr,getUserAgent

# from ixNet import netApp

# nt_ = netApp()
fp_ = fileP()


class image_load:
    def __init__(self, path, fname=None):  # path: url or dir , fname: must be full path
        self.path = path
        self.url = None
        self.local = None
        self.__parsalPath(path)  # decide image from url or local
        if self.url is None and self.local is None:
            print("fail to initial, pls check path ", path)
        self.image = None
        self.fname = fname
        self.__fname()  # given filename from info above

    def __parsalPath(self, path):  # decide image from url or local
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
            print("error at __parsalPath, due to ", e)
        return

    def __fname(self):
        if self.local is not None:
            self.fname = self.path if self.fname is None else jop(self.path, self.fname)
        if self.url is not None:
            if self.fname is None:
                try:
                    self.fname = jop(googlepath, getfnameFromWebAddress([self.url])[0][1])
                    fp_.creatFolder(googlepath)
                    # googlepath = '/concent/drive/MyDrive/tmp/google_grapse_out/'
                except Exception as e:
                    raise Exception("file name is necessary as url is active, pls give a filename, url {} \n error at {}".format(self.url, e))
            # self.fname = self.fname if self.fname is not None else "img" + "_" + getNowDateTimeStr(format="%y%m%d_%H%M%S")

    def __getImageFromUrl(self):
        fname = self.fname
        # print('fname: ',fname)
        url = self.url
        try:
            urllib.request.urlretrieve(url, fname)
        except Exception as e:
            # opener = urllib.request.URLopener()
            # opener.addheader('User-Agent', net_.getUserAgent())
            # filename, headers = opener.retrieve(url, 'Test.pdf')
            # raise Exception(e)
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-Agent", getUserAgent())]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, fname)

        return Image.open(fname)

    def __getGoogleImagURl(self, gID):
        # Getting the File id
        file2_id = gID
        fname = self.fname

        # Requesting data
        file2 = requests.get("https://drive.google.com/uc?export=download&confirm=9_s_&id=" + file2_id)

        # Saving data
        f = open(fname, "wb").write(file2.content)
        return Image.open(fname)

    def get_image(self):
        if self.image is not None:
            return self.image
        self.image = self.__imgFrom()
        return self.image

    def __imgFrom(self):
        if self.local is not None:
            return Image.open(self.fname).convert("RGB")
        if self.url is not None:
            url = self.url
            gID = self.__getGIDFormUrl()
            if gID is None:
                return self.__getImageFromUrl()
            else:
                return self.__getGoogleImagURl(gID)

    def __getGIDFormUrl(self):
        url = self.url
        # usage:
        # tar_url = 'https://drive.google.com/file/d/1YPpFm_OJHHQoLTrBOcelOMRLoHOtbcbT/view?usp=sharing' ##google URL
        # target_ID =  getGIDFormUrl( tar_url ) # for google
        # targetInfo = { 'url' :tar_url , 'gID': target_ID  ,'fname':'tar_.png'}
        o = urlparse(url)
        if o.netloc == "drive.google.com":
            return os.path.split(os.path.split(o.path)[0])[1]
        return None

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


# usage
# fps = [ ims( path=jop( path , f) )  for f in fns]
# images= [im_.get_img() for im_ in fps]
class ims(image_load):
    def __init__(self, path, image=None, fname=None):
        super(ims, self).__init__(path, fname=fname)  # 呼叫父類別__init__()
        self.name = os.path.split(self.fname)[1] if fname is not None else None

    def get_img(self, numpy_=False):  # numpy_ = array() which belong to cv2
        self.get_image()
        if self.image is None:
            raise Exception("error at get image, please check local name {} and path {} ".format(self.fname, self.path))
        return self.image if not numpy_ else cvR(self.image, reverse=True)

    def show_img(self, numpy_=True):
        img = self.get_img(numpy_=numpy_) if self.image is None else self.image
        if img is not None:
            plt.imshow(img)
            plt.show()
        else:
            print("no image founded")

    def get_name(self, path=False):
        if self.local and self.name is None:
            self.name = os.path.split(self.fname)[1]
        return self.name if not path else self.fname

    def get_url(self):
        return self.url

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
        except Exception as e:
            if iprint:
                print("\nFail to save", fname,', error at ',e)
            pass
        return False
    def save(self, path, formatP="jpeg"):
        img =self.get_img()
        self.saveImgPIL(path, img, formatP=formatP)


class img_File(fileP):
    def get_image_paths(self, directory):
        fL = self.scanAllLocalFile(directory)
        return [x.path for x in fL if x.name.endswith(".jpg") or x.name.endswith(".png")]

    def cv2_read_im(self,path): return  cv2.imread(path)
    def cv2_write_im(self,filename, image): return  cv2.imwrite(filename, image)
    
    def cv2_read(self, fn):
        return cv2.imread(fn)

    def cv_imread(self, file_path=""):
        cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        return cv_img

    def load_images(self, image_paths, convert=None, size=(256, 256)):
        iter_all_images = (self._resize(self.cv2_read(fn), size) for fn in image_paths)
        if convert:
            iter_all_images = (convert(img) for img in iter_all_images)
        for i, image in enumerate(iter_all_images):
            if i == 0:
                all_images = np.empty((len(image_paths),) + image.shape, dtype=image.dtype)
            all_images[i] = image
        return all_images

    def isImage(self, file_path, file_list):
        if os.path.splitext(os.path.join(file_path, file_list))[1] not in [".jpg", ".JPG", ".PNG", ".png"]:
            return False
        return True

    def get_transpose_axes(self, n):
        if n % 2 == 0:
            y_axes = list(range(1, n - 1, 2))
            x_axes = list(range(0, n - 1, 2))
        else:
            y_axes = list(range(0, n - 1, 2))
            x_axes = list(range(1, n - 1, 2))
        return y_axes, x_axes, [n - 1]

    def stack_images(self, images):
        images_shape = np.array(images.shape)
        new_axes = self.get_transpose_axes(len(images_shape))
        new_shape = [np.prod(images_shape[x]) for x in new_axes]
        return np.transpose(images, axes=np.concatenate(new_axes)).reshape(new_shape)

    def showG(self, test_A, test_B, path_A, path_B, batchSize):
        figure_A = np.stack([test_A, np.squeeze(np.array([path_A([test_A[i : i + 1]]) for i in range(test_A.shape[0])])), np.squeeze(np.array([path_B([test_A[i : i + 1]]) for i in range(test_A.shape[0])])),], axis=1)
        figure_B = np.stack([test_B, np.squeeze(np.array([path_B([test_B[i : i + 1]]) for i in range(test_B.shape[0])])), np.squeeze(np.array([path_A([test_B[i : i + 1]]) for i in range(test_B.shape[0])])),], axis=1)

        figure = np.concatenate([figure_A, figure_B], axis=0)
        figure = figure.reshape((4, batchSize // 2) + figure.shape[1:])
        figure = self.stack_images(figure)
        figure = np.clip((figure + 1) * 255 / 2, 0, 255).astype("uint8")
        figure = cv2.cvtColor(figure, cv2.COLOR_BGR2RGB)
        display(Image.fromarray(figure))

    def save_preview_image(self, test_A, test_B, path_A, path_B, path_bgr_A, path_bgr_B, path_mask_A, path_mask_B, batchSize, save_fn="preview.jpg"):
        figure_A = np.stack([test_A, np.squeeze(np.array([path_bgr_B([test_A[i : i + 1]]) for i in range(test_A.shape[0])])), (np.squeeze(np.array([path_mask_B([test_A[i : i + 1]]) for i in range(test_A.shape[0])]))) * 2 - 1, np.squeeze(np.array([path_B([test_A[i : i + 1]]) for i in range(test_A.shape[0])])),], axis=1)
        figure_B = np.stack([test_B, np.squeeze(np.array([path_bgr_A([test_B[i : i + 1]]) for i in range(test_B.shape[0])])), (np.squeeze(np.array([path_mask_A([test_B[i : i + 1]]) for i in range(test_B.shape[0])]))) * 2 - 1, np.squeeze(np.array([path_A([test_B[i : i + 1]]) for i in range(test_B.shape[0])])),], axis=1)

        figure = np.concatenate([figure_A, figure_B], axis=0)
        figure = figure.reshape((4, batchSize // 2) + figure.shape[1:])
        figure = self.stack_images(figure)
        figure = np.clip((figure + 1) * 255 / 2, 0, 255).astype("uint8")
        cv2.imwrite(save_fn, figure)

    def image_resize(self, image, size=None, inter=cv2.INTER_AREA):
        width = size[0]
        height = size[1]
        # if(width < height): dim = image_resize_H(image, size)
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        print("dim", dim)
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    def _resize(self, img, size):
        return cv2.resize(img, size)


"""
text = {'font':"./Liberary/mingliu.ttc" , 'text':'Hello world \n\n歡迎','size':30, 'position':(10,150),'color':'black'}
text['text'] ='方法一：可以使用//求取两数相除的商、%求取两数相除的余数。'
newPic((1024,500), text = text ,color=(255,0,255),  show=True )
"""


class Video:
    def newPic(self, shape=(1024, 768), color=(255, 255, 255), text=None, show=True):
        # shape: tuple
        image = Image.new("RGB", shape, color)
        draw = ImageDraw.Draw(image)
        if text is not None:
            draw = drawText(draw, shape, text)
        if show:
            display(image)

    def textLine(self, shape, textContent, textSize):
        width = shape[0]
        uTextLen = len(textContent.encode())
        w1 = int(width * 0.95 / textSize)
        chunks = [textContent[i : i + w1] for i in range(0, uTextLen, w1) if (len(textContent[i : i + w1]) > 0)]
        print(uTextLen, w1, chunks)
        return "-\n\n".join(chunks)

    # def getTextPos(shape, position):

    def drawText(self, draw, shape, text):
        # text:{'font':"./Liberary/mingliu.ttc" , 'text':'test','size':40, 'position':(),'color':'black'}
        font = "./Liberary/mingliu.ttc"
        if text is not None:
            font = text["font"]
        content = "No text input"
        if text is not None:
            content = text["text"]
        textSize = 40
        if text is not None:
            textSize = text["size"]
        textPos = (100, 50)
        if text is not None:
            textPos = text["position"]
        textColor = "black"
        if text is not None:
            textColor = text["color"]
        fnt = ImageFont.truetype(font, textSize, encoding="unic")  # 设置字体

        content = textLine(shape, content, textSize)

        draw.text(textPos, content, textColor, fnt)
        return draw

    def getAudioFile(self, audioPath):
        return [a for a in glob.glob1(audioPath, "*.mp3")]

    def getRandomL(self, audL, cnt=4):
        randomlist = []
        for i in range(0, cnt):
            n = random.randint(0, len(audL))
            print(n, len(audL))
            randomlist.append(audL[n])
        return randomlist

    def genAudio(self, audL, cnt=4):
        global audioPath
        audiofs = getRandomL(audL, cnt=cnt)
        audios = []
        for audio in audiofs:
            audios.append(mpe.AudioFileClip(os.path.join(audioPath, audio)))
        return audios

    def getAudio(self, audL, cnt=4):
        audiofs = genAudio(audioFiles, cnt=cnt)
        audioClip = mpe.concatenate_audioclips([audio for audio in audiofs])
        return audioClip

    def frename(self, fo, namex="R"):
        filename, file_extension = os.path.splitext(fo)
        return filename + namex + file_extension


class img_face(img_File):
    def showG_mask(self, test_A, test_B, path_A, path_B, batchSize):
        figure_A = np.stack([test_A, (np.squeeze(np.array([path_A([test_A[i : i + 1]]) for i in range(test_A.shape[0])]))) * 2 - 1, (np.squeeze(np.array([path_B([test_A[i : i + 1]]) for i in range(test_A.shape[0])]))) * 2 - 1,], axis=1)
        figure_B = np.stack([test_B, (np.squeeze(np.array([path_B([test_B[i : i + 1]]) for i in range(test_B.shape[0])]))) * 2 - 1, (np.squeeze(np.array([path_A([test_B[i : i + 1]]) for i in range(test_B.shape[0])]))) * 2 - 1,], axis=1)

        figure = np.concatenate([figure_A, figure_B], axis=0)
        figure = figure.reshape((4, batchSize // 2) + figure.shape[1:])
        figure = self.stack_images(figure)
        figure = np.clip((figure + 1) * 255 / 2, 0, 255).astype("uint8")
        figure = cv2.cvtColor(figure, cv2.COLOR_BGR2RGB)
        display(Image.fromarray(figure))

    def showG_eyes(self, test_A, test_B, bm_eyes_A, bm_eyes_B, batchSize):
        figure_A = np.stack([(test_A + 1) / 2, bm_eyes_A, bm_eyes_A * (test_A + 1) / 2,], axis=1)
        figure_B = np.stack([(test_B + 1) / 2, bm_eyes_B, bm_eyes_B * (test_B + 1) / 2,], axis=1)

        figure = np.concatenate([figure_A, figure_B], axis=0)
        figure = figure.reshape((4, batchSize // 2) + figure.shape[1:])
        figure = self.stack_images(figure)
        figure = np.clip(figure * 255, 0, 255).astype("uint8")
        figure = cv2.cvtColor(figure, cv2.COLOR_BGR2RGB)

        display(Image.fromarray(figure))


class ims_facial(ims):
    def __init__(self, fname=None, image=None, url=None):  # forward = link url, fname= location of file saved,
        super(ims_facial, self).__init__(fname=fname, image=image, url=url)  # 呼叫父類別__init__()

    def get_img(self):
        self.image = Image.open(self.fname).convert("RGB")
        return self.image

    def show_img(self):
        img = self.get_img() if self.image is None else self.image
        if img is not None:
            plt.imshow(img)
        else:
            print("not found any image")


# usage
# pl = image_plot(figSize=figSize, imageSize=imageSize, columns=columns, rows=rows)
# pl.plot_images(images)
class image_plot:
    def __init__(self, figSize=(20, 15), imageSize=(200, 200), columns=3, rows=5, titles=None, grid=None, axis=None) -> None:
        self.figSize = figSize
        self.imageSize = imageSize
        self.columns = columns
        self.rows = rows
        self.titles = titles
        self.grid = False if grid is None else grid
        self.axis = axis

    def showimagePIL(self, imgs):
        for img in imgs:
            display(img)

    def plot_image_with_np(self, x):
        plt.imshow(np.clip(x + 0.5, 0, 1))

    def plot_images_with_np(self, nps):
        figSize = self.figSize
        imageSize = self.imageSize
        columns = self.columns
        rows = self.rows
        # cvR = convertCv2ToImage
        w = imageSize[0]
        h = imageSize[1]
        fig = plt.figure(figsize=figSize)
        # columns = 3
        # rows = 5
        if len(nps) > columns * rows:
            rows = int(len(nps) / columns)
        for i in range(1, columns * rows + 1):
            if i - 1 < len(nps):
                # imgAry = cv2.resize(cvR(images[i - 1], reverse=True), dsize=(h, w))
                fig.add_subplot(rows, columns, i)

                plt.imshow(nps[i - 1], aspect="auto")
        plt.show()

    def plot_image_gray(self, image):  # images=list()
        size = self.figSize
        plt.figure(figsize=size)
        plt.imshow(image, cmap="gray", aspect="auto")
        plt.show()

    def plot_images(self, images):
        # images type can be PIL and np(cv2),
        cvR = convertCv2ToImage
        # if type(images[0]) == numpy.ndarray:
        images = [cvR(img) for img in images]

        figSize = self.figSize
        imageSize = self.imageSize
        columns = self.columns
        rows = self.rows
        titles = self.titles
        grid = self.grid
        axis_ = self.axis

        w = imageSize[0]
        h = imageSize[1]
        fig = plt.figure(figsize=figSize)
        # columns = 3
        # rows = 5
        if len(images) > columns * rows:
            rows = int(len(images) / columns) + 1
        for i in range(0, len(images)):
            # if i - 1 < len(images):
            imgAry = cv2.resize(cvR(images[i], reverse=True), dsize=(h, w))  # due to image keep PIL type, so reverse =True
            # fig.add_subplot(rows, columns, i)

            ax1 = fig.add_subplot(rows, columns, i + 1)
            if titles is not None:
                ax1.title.set_text(titles[i])
            ax1.grid(grid)
            if axis_ is None:
                # Hide axes ticks
                ax1.set_xticks([])
                ax1.set_yticks([])
                # ax1.set_zticks([])
            plt.imshow(cvR(imgAry), aspect="auto")
        plt.show()

    def show_1_ps(self,img1):
        plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()


# by ref
def show_image_list(list_images, list_titles=None, list_cmaps=None, grid=True, num_cols=2, figsize=(20, 10), title_fontsize=30):
    """
    Shows a grid of images, where each image is a Numpy array. The images can be either
    RGB or grayscale.

    Parameters:
    ----------
    images: list
        List of the images to be displayed.
    list_titles: list or None
        Optional list of titles to be shown for each image.
    list_cmaps: list or None
        Optional list of cmap values for each image. If None, then cmap will be
        automatically inferred.
    grid: boolean
        If True, show a grid over each image
    num_cols: int
        Number of columns to show.
    figsize: tuple of width, height
        Value to be passed to pyplot.figure()
    title_fontsize: int
        Value to be passed to set_title().
    """

    assert isinstance(list_images, list)
    assert len(list_images) > 0
    assert isinstance(list_images[0], np.ndarray)

    if list_titles is not None:
        assert isinstance(list_titles, list)
        assert len(list_images) == len(list_titles), "%d imgs != %d titles" % (len(list_images), len(list_titles))

    if list_cmaps is not None:
        assert isinstance(list_cmaps, list)
        assert len(list_images) == len(list_cmaps), "%d imgs != %d cmaps" % (len(list_images), len(list_cmaps))

    num_images = len(list_images)
    num_cols = min(num_images, num_cols)
    num_rows = int(num_images / num_cols) + (1 if num_images % num_cols != 0 else 0)

    # Create a grid of subplots.
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)

    # Create list of axes for easy iteration.
    if isinstance(axes, np.ndarray):
        list_axes = list(axes.flat)
    else:
        list_axes = [axes]

    for i in range(num_images):

        img = list_images[i]
        title = list_titles[i] if list_titles is not None else "Image %d" % (i)
        cmap = list_cmaps[i] if list_cmaps is not None else (None if img_is_color(img) else "gray")

        list_axes[i].imshow(img, cmap=cmap)
        list_axes[i].set_title(title, fontsize=title_fontsize)
        list_axes[i].grid(grid)

    for i in range(num_images, len(list_axes)):
        list_axes[i].set_visible(False)

    fig.tight_layout()
    _ = plt.show()


def plot_images_v(images, figSize=(20, 15), imageSize=(200, 200), columns=3, rows=5, titles=None, grid=None, axis=None):
    pl = image_plot(figSize=figSize, imageSize=imageSize, columns=columns, rows=rows, titles=titles, grid=grid, axis=axis)
    pl.plot_images(images)


imF = img_File()
cv2_read_im= imF.cv2_read_im
cv2_write_im = imF.cv2_write_im

im_plot = image_plot()
show_1_ps = im_plot.show_1_ps

from PIL import Image

class image_process():
    def start_up_g_mouse_2points(self,f_path_,image_src = None):
        f_path = f_path_
        # Load the image
        image = cv2.imread(f_path) if image_src is None else image_src
        if(image is None or image.shape is None):
            print(f'Error while read image { f_path_}')
            return []

        # Display the image
        disp_h,disp_w = 480, 640
        img_h,img_w,_ = image.shape
        ratio = disp_h /img_h if disp_h/ img_h < disp_w/img_w else  disp_w/img_w
        mImg_h, mImg_w = img_h*ratio, img_w * ratio
        mImg = cv2.resize( image, ( int(mImg_w), int(mImg_h )))
        print('\n mouse to click 2 points')
        print(f' modify image shape {mImg.shape}, original image shape {image.shape}')
        pts=[]
        def setpoint(x_,y_):
            if(len(pts)==4):
                print(f'Note, 2 points already done, not accept any other points, get {(x_,y_)}' )
                return
            pts.append(x_)
            pts.append(y_)
            print(f'done points {pts}' )
        # function to display the coordinates of 
        # of the points clicked on the image  
        def show_window():
            cv2.imshow("image", mImg)
            # cv2.imshow("Image", image, cv2.WINDOW_AUTOSIZE)
            # Resize the window
            cv2.resizeWindow("image", 640, 480)

        def click_event(event, x, y, flags, params): 
            img = mImg
            # checking for left mouse clicks 
            if event == cv2.EVENT_LBUTTONDOWN: 

                # displaying the coordinates 
                # on the Shell 
                print(f'modify {x}, {y}, original ratio {ratio} {int(x/ratio)}, {int(y/ratio)}') 

                # displaying the coordinates 
                # on the image window 
                font = cv2.FONT_HERSHEY_SIMPLEX 
                cv2.putText(img, str(x) + ',' +
                            str(y), (x,y), font, 
                            1, (255, 0, 0), 2) 
        #         cv2.imshow('image', img) 
                show_window()
                setpoint( int(x/ratio), int(y/ratio ) )

            # checking for right mouse clicks      
            if event==cv2.EVENT_RBUTTONDOWN: 

                # displaying the coordinates 
                # on the Shell 
                print(x, ' ', y) 

                # displaying the coordinates 
                # on the image window 
                font = cv2.FONT_HERSHEY_SIMPLEX 
                b = img[y, x, 0] 
                g = img[y, x, 1] 
                r = img[y, x, 2] 
                cv2.putText(img, str(b) + ',' +
                            str(g) + ',' + str(r), 
                            (x,y), font, 1, 
                            (255, 255, 0), 2) 
        #         cv2.imshow('image', img) 
                show_window()
        show_window()
        # setting mouse handler for the image 
        # and calling the click_event() function 
        cv2.setMouseCallback('image', click_event) 

        # wait for a key to be pressed to exit 
        cv2.waitKey(0) 
        # Close the window
        cv2.destroyAllWindows()
        return pts

    def g_2points_in_image(self,dir_path, src_fs_=None, ruc=None,keep_image=False):
        ru_={} if ruc is None else ruc
        # pg=6
        # src_path = fr'D:\tmp\nude_tmp\nude_facebook_Fitness_Gurls_swim\{pg}'
        src_path=dir_path
        src_fs = getListOfFiles(src_path, ext=['.jpg'], statInfo=False, verbose=False, sub=True, sort=True) if src_fs_ is None else src_fs_
        sr_ =''
        for idx,f in enumerate(src_fs):
            clear_output()
            f_info = g_file_info( f )  
            if(idx==0):print(f'work path {f_info["path"]}')
            print(f'{idx}/{len(src_fs )} {f_info["file_name"] }')
            image = None if(not keep_image) else  cv2.imread(f)
            pts = self.start_up_g_mouse_2points(f, image_src = image)
            print(f'done {idx} {f}, {pts} ')
            ru_[f] = pts  if not keep_image else {'box': pts, 'image': image}
            cc=input(f'go on to press any key, but type key "c" to abort ')   
            if(cc=='c'):
                print('program already abort by user interrupt it ')
                break 
        print('done')    
        return ru_





    def merge_images(self,img1, img2, alpha):
    #     # 读取两张图片
    #     img1 = cv2.imread(image1_path)
    #     img2 = cv2.imread(image2_path)

        # 调整图片大小以确保它们具有相同的尺寸
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        # 设置第一张图片的透明度
        img1 = cv2.addWeighted(img1, alpha / 255, img2, 1 - alpha / 255, 0)
        return img1.copy()

    #     # 显示合并后的图片
    #     plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    #     plt.axis('off')
    #     plt.show()
    def merge_images_PIL(self,img1, img2, alpha):
    #     # 打开两张图片
    #     img1 = Image.open(image1_path)
    #     img2 = Image.open(image2_path)

        # 设置第一张图片的透明度
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")
        img1 = Image.blend(img1, Image.new('RGBA', img1.size, (255, 255, 255, alpha)), alpha)

        # 合并两张图片
        merged_image = Image.alpha_composite(img1, img2)

        # 显示合并后的图片
        display(merged_image)

    def g_crop_image_from_bbox(self, src_img, bbox=[]):
        #bbox : (x, y, w, h)
        if(len(bbox)==0): return src_img
        (x, y, w, h) = bbox[0]
        return src_img[y:y + h, x:x + w]
    def g_clip_image(self, src=None, src_path= None):
        if(src is None):
            src = select_files() if src_path is None else select_files(initial_path=src_path)
            
        assert type(src) is list , f'invalidate type, need "list", get {type(src)}'
        rU_boxs = self.g_2points_in_image(src_path, src_fs_ = src, keep_image=True)
        rU_data = { f: self.g_crop_image_from_bbox(rU_boxs[f]['image'],rU_boxs[f]['box']) for f in rU_boxs}
        return rU_data

    # do image to half
    def g_image_horz_half(self,image):
        # 获取图像的宽度和高度
        height, width = image.shape[:2]
        # 裁剪图像的水平一半
        return image[:, :width // 2]

    def do_half_f(self,src, dest=None,iprint=False):
        cv_in = cv2_read_im( src )
        cv_half = self.g_image_horz_half(cv_in)
        if(dest is not None): cv2_write_im(dest, cv_half) 
        if(iprint): print('\ndone to cut image into a half') 
        return cv_half

            

imP = image_process()
merge_images = imP.merge_images
g_clipimage = imP.start_up_g_mouse_2points
start_up_g_mouse_2points = imP.start_up_g_mouse_2points
g_2points_in_image = imP.g_2points_in_image
g_clip_image = imP.g_clip_image
g_image_horz_half = imP.g_image_horz_half
do_half_f = imP.do_half_f