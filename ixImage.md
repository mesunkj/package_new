---

### **1\. image\_load Class**

image\_load is a class for handling image loading from both local file paths and URLs.

#### **\_\_init\_\_**

**Overview**: Initializes an image\_load object with a path to an image, which can be either a URL or a local file path. It automatically determines the source and prepares the object for image retrieval.

**Details**:

* path (string, required): The URL or local directory path of the image.  
* fname (string, optional): The full file path to save the image to if the source is a URL. If the source is a local file, it's used as the full path to the image.

---

#### **\_\_parsalPath**

**Overview**: A private helper method that parses the input path to determine if it's a local file path or a URL.

**Details**:

* path (string): The path to be parsed.  
* **No return value**: It updates the self.url or self.local attributes based on the parsing result.

---

#### **\_\_fname**

**Overview**: A private helper method that sets the filename for the image based on whether the source is a local file or a URL. For URLs, it generates a filename if one isn't provided.

**Details**:

* **No parameters**: It uses self.local, self.url, and self.fname to determine the final filename.  
* **No return value**: It sets the self.fname attribute.

---

#### **\_\_getImageFromUrl**

**Overview**: A private method that downloads an image from a URL and opens it as a PIL (Pillow) image object. It handles common user-agent issues during the download.

**Details**:

* **No parameters**: It uses self.url and self.fname.  
* **Returns**: A PIL Image object.

---

#### **\_\_getGoogleImagURl**

**Overview**: A private method to download an image hosted on Google Drive using a file ID.

**Details**:

* gID (string): The Google Drive file ID.  
* **Returns**: A PIL Image object.

---

#### **get\_image**

**Overview**: The main public method to retrieve the image. It determines whether to load from a local file or a URL and returns the image object.

**Details**:

* **No parameters**.  
* **Returns**: A PIL Image object.

---

#### **\_\_imgFrom**

**Overview**: A private helper method that orchestrates the image loading process, calling either the local file handler or the URL handler.

**Details**:

* **No parameters**.  
* **Returns**: A PIL Image object.

---

#### **\_\_getGIDFormUrl**

**Overview**: A private method to extract the Google Drive file ID from a Google Drive URL.

**Details**:

* **No parameters**: It uses self.url.  
* **Returns**: A string containing the Google Drive ID or None if the URL is not a Google Drive link.

---

#### **fetch\_imagef**

**Overview**: Fetches an image from a URL and saves it to a specified file path.

**Details**:

* url (string): The URL of the image to fetch.  
* fname (string, optional): The filename for the saved image.  
* path (string, optional): The directory path to save the image in.  
* tryAgain (boolean, optional): Whether to retry the request if it fails.  
* tryC (integer, optional): The number of times to retry.  
* **Returns**: A PIL Image object.

---

#### **getURLimagePIL**

**Overview**: Downloads multiple images from a list of URLs and returns them as PIL objects, filtering out files larger than a specified size.

**Details**:

* urls (list): A list of image URLs.  
* limitSize (integer, optional): The maximum file size in bytes. Defaults to 5 KB.  
* show (boolean, optional): Whether to display the images.  
* iprint (boolean, optional): Whether to print progress information.  
* **Returns**: A tuple containing three lists:  
  * imgs: List of PIL Image objects.  
  * urlsR: List of URLs corresponding to the fetched images.  
  * errPic: List of URLs that failed to be fetched.

---

### **2\. ims Class**

ims is a subclass of image\_load that provides additional utility methods for image handling, such as retrieving images as NumPy arrays and saving images.

#### **\_\_init\_\_**

**Overview**: Initializes an ims object, inheriting functionality from image\_load.

**Details**:

* path (string, required): The URL or local directory path of the image.  
* image (PIL Image, optional): A pre-loaded image object.  
* fname (string, optional): The full file path to save or load the image from.

---

#### **get\_img**

**Overview**: Retrieves the image as either a PIL Image object or a NumPy array.

**Details**:

* numpy\_ (boolean, optional): If True, returns the image as a NumPy array (compatible with OpenCV). Defaults to False.  
* **Returns**: A PIL Image object or a NumPy array.

---

#### **show\_img**

**Overview**: Displays the image using matplotlib.pyplot.

**Details**:

* numpy\_ (boolean, optional): If True, displays the image as a NumPy array. Defaults to True.  
* **No return value**: Displays the image.

---

#### **get\_name**

**Overview**: Returns the base filename of the image.

**Details**:

* path (boolean, optional): If True, returns the full path instead of just the filename. Defaults to False.  
* **Returns**: A string representing the image name or full path.

---

#### **get\_url**

**Overview**: Returns the URL of the image if it was loaded from a URL.

**Details**:

* **No parameters**.  
* **Returns**: A string containing the image URL.

---

#### **saveImgsPIL**

**Overview**: Saves a list of PIL images to a specified directory.

**Details**:

* dirP (string): The destination directory path.  
* filenames (list): A list of filenames for the images.  
* imgs (list): A list of PIL Image objects to save.  
* iprint (boolean, optional): Whether to print progress. Defaults to True.  
* **No return value**: Saves the images to disk.

---

#### **saveImgPIL**

**Overview**: Saves a single PIL image to a specified file path.

**Details**:

* fname (string): The full file path to save the image to.  
* img (PIL Image): The image object to save.  
* iprint (boolean, optional): Whether to print success/failure messages. Defaults to True.  
* formatP (string, optional): The image format (e.g., "png", "jpeg"). Defaults to "png".  
* **Returns**: True on success, False on failure.

---

#### **save**

**Overview**: A convenience method to save the image object to a specified path.

**Details**:

* path (string): The full file path to save the image to.  
* formatP (string, optional): The image format. Defaults to "jpeg".  
* **No return value**: Saves the image to disk.

---

### **3\. img\_File Class**

img\_File inherits from fileP and provides methods for image-related file operations, such as reading, writing, and manipulating images with OpenCV.

#### **get\_image\_paths**

**Overview**: Scans a directory and returns a list of paths to image files (.jpg or .png).

**Details**:

* directory (string): The path to the directory to scan.  
* **Returns**: A list of strings, each being a full path to an image file.

---

#### **cv2\_read\_im**

**Overview**: Reads an image file into a NumPy array using OpenCV's imread.

**Details**:

* path (string): The path to the image file.  
* **Returns**: A NumPy array representing the image.

---

#### **cv2\_write\_im**

**Overview**: Writes a NumPy array image to a file using OpenCV's imwrite.

**Details**:

* filename (string): The path to save the image to.  
* image (NumPy array): The image data to be written.  
* **Returns**: True if successful, False otherwise.

---

#### **cv\_imread**

**Overview**: A robust version of cv2.imread that can handle file paths with non-ASCII characters.

**Details**:

* file\_path (string): The path to the image file.  
* **Returns**: A NumPy array representing the image.

---

#### **load\_images**

**Overview**: Loads multiple images from a list of paths, resizing them to a specified size.

**Details**:

* image\_paths (list): A list of paths to the images.  
* convert (function, optional): A function to apply to each image after loading and resizing.  
* size (tuple, optional): A tuple (width, height) for resizing the images. Defaults to (256, 256).  
* **Returns**: A single NumPy array containing all loaded images.

---

#### **isImage**

**Overview**: Checks if a given file is a .jpg or .png image.

**Details**:

* file\_path (string): The directory path.  
* file\_list (string): The filename.  
* **Returns**: True if the file is an image, False otherwise.

---

#### **get\_transpose\_axes**

**Overview**: A private helper method for stacking images. It calculates the axes for transposing a multi-dimensional NumPy array.

**Details**:

* n (integer): The number of dimensions of the array.  
* **Returns**: A tuple of three lists representing the x, y, and z axes.

---

#### **stack\_images**

**Overview**: Stacks multiple images (represented as a multi-dimensional NumPy array) into a single, flattened image. Useful for creating a collage or grid of images.

**Details**:

* images (NumPy array): The array of images to be stacked.  
* **Returns**: A single NumPy array representing the stacked images.

---

#### **showG**

**Overview**: Displays a grid of images for visualizing results from a GAN (Generative Adversarial Network) model.

**Details**:

* test\_A, test\_B (NumPy arrays): Input image batches from two different domains.  
* path\_A, path\_B (functions): Functions that take an image batch and return the transformed output.  
* batchSize (integer): The batch size of the image data.  
* **No return value**: Displays the resulting grid of images.

---

#### **save\_preview\_image**

**Overview**: Saves a preview image of GAN results to a file. It creates a grid showing original images, their transformed versions, and masks.

**Details**:

* test\_A, test\_B (NumPy arrays): Input image batches.  
* path\_A, path\_B (functions): Transformation functions.  
* path\_bgr\_A, path\_bgr\_B (functions): BGR transformation functions.  
* path\_mask\_A, path\_mask\_B (functions): Mask generation functions.  
* batchSize (integer): The batch size.  
* save\_fn (string, optional): The filename to save the image as. Defaults to "preview.jpg".  
* **No return value**: Saves the image to disk.

---

#### **image\_resize**

**Overview**: Resizes an image while maintaining its aspect ratio.

**Details**:

* image (NumPy array): The image to be resized.  
* size (tuple, optional): The target (width, height). If only one dimension is provided, the other is calculated.  
* inter (integer, optional): The interpolation method for resizing. Defaults to cv2.INTER\_AREA.  
* **Returns**: The resized image as a NumPy array.

---

#### **\_resize**

**Overview**: A private helper method to resize an image to a fixed size using OpenCV.

**Details**:

* img (NumPy array): The image to be resized.  
* size (tuple): The target (width, height).  
* **Returns**: The resized image as a NumPy array.

---

### **4\. Video Class**

Video contains functions related to creating new images, drawing text, and manipulating audio for video generation.

#### **newPic**

**Overview**: Creates a new, blank image with a specified shape, color, and optional text.

**Details**:

* shape (tuple, optional): The (width, height) of the new image. Defaults to (1024, 768).  
* color (tuple, optional): The RGB color of the background. Defaults to (255, 255, 255\) (white).  
* text (dict, optional): A dictionary containing text properties like font, text, size, position, and color.  
* show (boolean, optional): Whether to display the image immediately. Defaults to True.  
* **No return value**: Creates and displays the image.

---

#### **textLine**

**Overview**: Formats a long string of text to fit within a specified image width, breaking it into multiple lines.

**Details**:

* shape (tuple): The (width, height) of the image.  
* textContent (string): The text to be formatted.  
* textSize (integer): The size of the font.  
* **Returns**: The formatted string with newline characters.

---

#### **drawText**

**Overview**: Draws text onto an image using a given font, size, and position.

**Details**:

* draw (PIL ImageDraw object): The drawing context for the image.  
* shape (tuple): The (width, height) of the image.  
* text (dict): A dictionary with text properties.  
* **Returns**: The modified ImageDraw object.

---

#### **getAudioFile**

**Overview**: Scans a directory for all .mp3 audio files.

**Details**:

* audioPath (string): The path to the directory.  
* **Returns**: A list of filenames of the .mp3 files.

---

#### **getRandomL**

**Overview**: Selects a specified number of random audio files from a list.

**Details**:

* audL (list): A list of audio file paths.  
* cnt (integer, optional): The number of random files to select. Defaults to 4\.  
* **Returns**: A list of randomly selected audio file paths.

---

#### **genAudio**

**Overview**: Generates a list of moviepy.editor.AudioFileClip objects from a list of audio files.

**Details**:

* audL (list): A list of audio file paths.  
* cnt (integer, optional): The number of clips to generate. Defaults to 4\.  
* **Returns**: A list of AudioFileClip objects.

---

#### **getAudio**

**Overview**: Concatenates multiple audio clips into a single AudioFileClip.

**Details**:

* audL (list): A list of audio file paths.  
* cnt (integer, optional): The number of clips to concatenate. Defaults to 4\.  
* **Returns**: A single concatenated AudioFileClip.

---

#### **frename**

**Overview**: Renames a file by appending a suffix before its extension.

**Details**:

* fo (string): The original file path.  
* namex (string, optional): The suffix to append. Defaults to "R".  
* **Returns**: The new filename as a string.

---

### **5\. img\_face Class**

img\_face is a subclass of img\_File with specialized methods for visualizing face-related image processing, such as masks and eyes.

#### **showG\_mask**

**Overview**: Displays a grid of images for GAN results, focusing on masks.

**Details**:

* test\_A, test\_B (NumPy arrays): Input image batches.  
* path\_A, path\_B (functions): Functions that return image masks.  
* batchSize (integer): The batch size.  
* **No return value**: Displays the resulting grid of images.

---

#### **showG\_eyes**

**Overview**: Displays a grid of images for GAN results, focusing on eye-related transformations.

**Details**:

* test\_A, test\_B (NumPy arrays): Input image batches.  
* bm\_eyes\_A, bm\_eyes\_B (NumPy arrays): Binary eye masks.  
* batchSize (integer): The batch size.  
* **No return value**: Displays the resulting grid of images.

---

### **6\. ims\_facial Class**

ims\_facial is a subclass of ims tailored for facial images.

#### **\_\_init\_\_**

**Overview**: Initializes an ims\_facial object, inheriting from ims.

**Details**:

* fname (string, optional): The filename.  
* image (PIL Image, optional): The pre-loaded image.  
* url (string, optional): The URL of the image.

---

#### **get\_img**

**Overview**: Retrieves the image as a PIL Image object.

**Details**:

* **No parameters**.  
* **Returns**: A PIL Image object.

---

#### **show\_img**

**Overview**: Displays the image using matplotlib.pyplot.

**Details**:

* **No parameters**.  
* **No return value**: Displays the image.

---

### **7\. image\_plot Class**

image\_plot is a class for plotting and displaying images in a grid format using matplotlib.pyplot or IPython.

#### **\_\_init\_\_**

**Overview**: Initializes an image\_plot object with parameters for controlling the size and layout of image plots.

**Details**:

* figSize (tuple, optional): The (width, height) of the overall figure. Defaults to (20, 15).  
* imageSize (tuple, optional): The (width, height) of each individual image. Defaults to (200, 200).  
* columns (integer, optional): The number of columns in the plot grid. Defaults to 3\.  
* rows (integer, optional): The number of rows in the plot grid. Defaults to 5\.  
* titles (list, optional): A list of titles for each image.  
* grid (boolean, optional): Whether to display a grid on the images. Defaults to False.  
* axis (boolean, optional): Whether to display the axes. Defaults to None (hides axes).

---

#### **showimagePIL**

**Overview**: Displays a list of PIL images in the output.

**Details**:

* imgs (list): A list of PIL Image objects.  
* **No return value**: Displays the images.

---

#### **plot\_image\_with\_np**

**Overview**: Plots a single NumPy array image using matplotlib.pyplot.

**Details**:

* x (NumPy array): The image data to plot.  
* **No return value**: Plots the image.

---

#### **plot\_images\_with\_np**

**Overview**: Plots a list of NumPy array images in a grid.

**Details**:

* nps (list): A list of NumPy arrays representing images.  
* **No return value**: Plots the images.

---

#### **plot\_image\_gray**

**Overview**: Plots a single grayscale image.

**Details**:

* image (NumPy array): The image to plot.  
* **No return value**: Plots the image.

---

#### **plot\_images**

**Overview**: Plots a list of images (either PIL or NumPy arrays) in a grid, with options for titles and axis display.

**Details**:

* images (list): A list of image objects.  
* **No return value**: Plots the images.

---

#### **show\_1\_ps**

**Overview**: Displays a single image using matplotlib.pyplot without axes.

**Details**:

* img1 (NumPy array): The image to display.  
* **No return value**: Displays the image.

---

### **8\. image\_process Class**

image\_process provides methods for interactive image processing, such as cropping, resizing, and merging.

#### **start\_up\_g\_mouse\_2points**

**Overview**: An interactive function that displays an image and allows the user to click two points with the mouse. The coordinates of these points are returned. This is useful for manual selection of regions for cropping or other operations.

**Details**:

* f\_path\_ (string): The path to the image file.  
* image\_src (NumPy array, optional): A pre-loaded image.  
* **Returns**: A list of four integers representing the (x1, y1, x2, y2) coordinates of the two clicked points, relative to the original image dimensions.

---

#### **g\_2points\_in\_image**

**Overview**: Interactively prompts the user to select two points on a series of images from a directory or a list of files.

**Details**:

* dir\_path (string): The directory path containing the images.  
* src\_fs\_ (list, optional): A list of specific file paths to process.  
* ruc (dict, optional): A dictionary to store the results.  
* keep\_image (boolean, optional): Whether to keep the image data in the results dictionary. Defaults to False.  
* **Returns**: A dictionary mapping each file path to the list of clicked coordinates.

---

#### **merge\_images**

**Overview**: Blends two images using a specified alpha (transparency) value.

**Details**:

* img1 (NumPy array): The base image.  
* img2 (NumPy array): The image to be blended on top.  
* alpha (integer): The alpha value (0-255) for the first image.  
* **Returns**: A new NumPy array representing the merged image.

---

#### **merge\_images\_PIL**

**Overview**: Blends two PIL images with a specified alpha value.

**Details**:

* img1 (PIL Image): The base image.  
* img2 (PIL Image): The image to be blended on top.  
* alpha (integer): The alpha value for the first image.  
* **No return value**: Displays the merged image.

---

#### **g\_crop\_image\_from\_bbox**

**Overview**: Crops an image based on a bounding box.

**Details**:

* src\_img (NumPy array): The source image.  
* bbox (list, optional): A list containing a single tuple (x, y, w, h) defining the bounding box.  
* **Returns**: The cropped image as a NumPy array.

---

#### **g\_clip\_image**

**Overview**: An interactive function to clip a series of images by prompting the user to select a bounding box on each one.

**Details**:

* src (list, optional): A list of file paths to images. If not provided, a file selection dialog will appear.  
* src\_path (string, optional): The initial path for the file selection dialog.  
* **Returns**: A dictionary where keys are file paths and values are the cropped image data.

---

#### **g\_image\_horz\_half**

**Overview**: Crops the horizontal left half of an image.

**Details**:

* image (NumPy array): The image to crop.  
* **Returns**: The NumPy array representing the left half of the image.

---

#### **do\_half\_f**

**Overview**: Reads an image, crops it to its horizontal left half, and optionally saves the result.

**Details**:

* src (string): The path to the source image file.  
* dest (string, optional): The path to save the cropped image.  
* iprint (boolean, optional): Whether to print a message upon completion. Defaults to False.  
* **Returns**: The NumPy array of the cropped image.