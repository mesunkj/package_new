# _*_ coding:utf-8 _*_

"""
File Processor Utility Library

This module provides a comprehensive set of functions and classes for file and directory
operations, including reading, writing, moving, copying, compressing, and managing
file metadata.

It is structured into three main classes:
- fileProcessor: Handles core file I/O and manipulation.
- fileAddress: Manages and resolves directory paths.
- fileStructure: A data structure for file metadata.

How to use:
--------------------------------------------------------------------------------
# Example 1: Reading a text file
from ixFileP import fileProcessor
fp = fileProcessor()
content = fp.read_text_file(filename='example.txt')

# Example 2: Saving a list to a CSV file
from ixFileP import fileProcessor
fp = fileProcessor()
data = [['col1_val1', 'col2_val1'], ['col1_val2', 'col2_val2']]
columns = ['column1', 'column2']
fp.save_to_csv(filename='output.csv', data_list=data, columns=columns)

# Example 3: Managing directories with fileAddress
from ixFileP import fileAddress
fa = fileAddress(update=True)  # Scans and caches directory paths
app_dir_path = fa.get_dir('app')
print(f"The path to 'app' directory is: {app_dir_path}")

--------------------------------------------------------------------------------
"""

import os
import errno
import sys
import json
import numpy as np
from ast import literal_eval
import shutil
import pandas as pd
import pickle
from subprocess import call
import filecmp
import zipfile
import zipfile
from typing import List, Dict, Any, Union
from datetime import datetime, date

# Assuming ixMisc and utils are available
from ixMisc import utils as _ut
ut = _ut()

class NpEncoder(json.JSONEncoder):
    """
    A custom JSON encoder that handles NumPy data types.

    This encoder converts numpy integers, floats, and ndarrays into standard
    Python types to ensure they are JSON serializable.
    """
    def default(self, obj: Any) -> Any:
        """
        Overrides the default method to handle numpy types.

        Args:
            obj (Any): The object to be serialized.

        Returns:
            Any: The serialized object.
        """
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


class fileProcessor:
    """
    A class containing various utility methods for file and directory operations.
    """
    class specialFile:
        """
        Methods for handling special file types or operations.
        """
        def read_larger_file(self, filename: str, line_return: str = "\n") -> str:
            """
            Reads a large text file line by line and concatenates the content.

            This method is suitable for handling very large files that may not
            fit entirely into memory, optimizing memory usage by avoiding
            large single string creation in a loop.

            Args:
                filename (str): The path to the file to be read.
                line_return (str, optional): The string to append after each line.
                                             Defaults to "\n".

            Returns:
                str: The concatenated content of the file.
            """
            parts = []
            try:
                with open(filename, encoding="utf8") as f:
                    for line in f:
                        parts.append(line.strip("\n") + line_return)
            except FileNotFoundError:
                print(f"Error: The file '{filename}' was not found.")
                return ""
            except Exception as e:
                print(f"An error occurred while reading the file: {e}")
                return ""
            return "".join(parts)

    def save_to_csv(self, filename: str, data_list: list, columns: Union[List[str], str] = "", index: Union[str, None] = "", dump: bool = True):
        """
        Saves a list of data to a CSV file.

        Args:
            filename (str): The name of the output CSV file.
            data_list (list): The list of data to save.
            columns (Union[List[str], str], optional): A list of column names for the DataFrame.
                                                       Defaults to "".
            index (Union[str, None], optional): The column name to set as the index.
                                                Defaults to "".
            dump (bool, optional): If True, saves the DataFrame in a binary (pickle) format.
                                   If False, saves as a standard CSV file. Defaults to True.
        """
        if len(columns) > 0:
            df = pd.DataFrame(data_list, columns=columns)
        else:
            df = pd.DataFrame(data_list)
        if index != "":
            df = df.set_index(index)

        if dump:
            self.write_bin_csv(filename=filename, data=df)
        else:
            df.to_csv(filename, encoding="utf-8")

    def read_csv_file(self, filename: str) -> pd.DataFrame:
        """
        Reads data from a CSV file into a pandas DataFrame.

        First attempts to read as a standard CSV. If it fails, it tries
        to read it as a binary (pickle) file.

        Args:
            filename (str): The path to the CSV file.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the file's data.
                          Returns an empty DataFrame if the file doesn't exist
                          or an error occurs.
        """
        if not self.file_exist_check(filename):
            print(f"File not found: {filename}")
            return pd.DataFrame()
        try:
            df = pd.read_csv(filename, encoding="utf-8")
            return df
        except Exception as err:
            try:
                df = self.read_bin_csv(filename=filename)
                return df
            except Exception as e:
                print(f"Failed to read file '{filename}' as CSV or pickle: {e}")
                return pd.DataFrame()

    def _read_text_file_core(self, filename: str, encoding: str) -> str:
        """
        核心內部函數，負責讀取文字檔案。
        此函數不直接暴露給外部，用於統一處理邏輯。
        """
        try:
            with open(filename, "r", encoding=encoding) as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            return ""
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return ""

    def readTextFile(self, filename: str, encoding: str = "utf-8") -> str:
        """
        讀取文字檔案的內容。

        此函數作為一個公開入口，內部調用核心處理函數。
        Args:
            filename (str): 檔案的路徑。
            encoding (str, optional): 檔案的編碼。預設為 "utf-8"。

        Returns:
            str: 檔案的內容。若發生錯誤則返回空字串。
        """
        return self._read_text_file_core(filename, encoding)

    def read_txt(self, filename: str, encoding: str = "utf-8") -> str:
        """
        另一個讀取文字檔案的公開入口。

        此函數與 readTextFile 功能相同，提供給不同命名習慣的使用者。
        Args:
            filename (str): 檔案的路徑。
            encoding (str, optional): 檔案的編碼。預設為 "utf-8"。

        Returns:
            str: 檔案的內容。若發生錯誤則返回空字串。
        """
        return self._read_text_file_core(filename, encoding)

    def openTextFile(self, filename: str, encoding: str = "utf-8") -> str:
        """
        另一個讀取文字檔案的公開入口，功能與 readTextFile 相同。
        """
        return self._read_text_file_core(filename, encoding)
    def write_text_file(self, filename: str, content: str, mode: str = "w", encoding: str = "utf-8"):
        """
        Writes content to a text file.

        Args:
            filename (str): The path to the file.
            content (str): The content to write.
            mode (str, optional): The file open mode. Defaults to "w" (write).
            encoding (str, optional): The character encoding. Defaults to "utf-8".
        """
        try:
            with open(filename, mode, encoding=encoding) as f:
                f.write(content)
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

    def delete_files(self, filename: str, directory: str = ""):
        """
        Deletes a specific file.

        Args:
            filename (str): The name of the file to delete.
            directory (str, optional): The directory containing the file.
                                       Defaults to "".
        """
        filepath = os.path.join(directory, filename) if directory else filename
        if os.path.isfile(filepath):
            os.remove(filepath)

    def delete_tree(self, directory: str):
        """
        Recursively deletes a directory and all its contents.

        Args:
            directory (str): The path to the directory to delete.
        """
        if os.path.isdir(directory):
            shutil.rmtree(directory)

    def zip_directory(self, path: str, filename: str):
        """
        Compresses a directory into a ZIP archive.

        Args:
            path (str): The path to the directory to compress.
            filename (str): The name of the output ZIP file.
        """
        ziph = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))
        ziph.close()
        print(f"Done zipping file: {filename}")

    def copy_directory(self, source: str, target: str):
        """
        Recursively copies an entire directory tree.

        Args:
            source (str): The source directory path.
            target (str): The destination directory path.
        """
        try:
            shutil.copytree(source, target)
        except Exception as e:
            print(f"Error copying directory from '{source}' to '{target}': {e}")

    def get_file_size_in_bytes(self, file_path: str) -> int:
        """
        Gets the size of a file in bytes.

        Args:
            file_path (str): The path to the file.

        Returns:
            int: The size of the file in bytes. Returns 0 if the file doesn't exist.
        """
        try:
            return os.path.getsize(file_path)
        except FileNotFoundError:
            return 0

    def create_folder(self, directory: str):
        """
        Creates a directory if it does not already exist.

        Args:
            directory (str): The path of the directory to create.
        """
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def rename_file(self, from_file: str, to_file: str):
        """
        Renames a file.

        Args:
            from_file (str): The original file path.
            to_file (str): The new file path.
        """
        try:
            os.rename(from_file, to_file)
        except Exception as e:
            print(f"Error renaming file from '{from_file}' to '{to_file}': {e}")

    def file_exist_check(self, filename: str) -> bool:
        """Checks if a file exists."""
        return os.path.isfile(filename)

    def dir_exist_check(self, directory: str) -> bool:
        """Checks if a directory exists."""
        return os.path.exists(directory)

    def write_bin_csv(self, filename: str, data: Any):
        """
        Writes data to a binary file using pickle.

        Args:
            filename (str): The path of the output file.
            data (Any): The data to be pickled (e.g., a pandas DataFrame).
        """
        try:
            with open(filename, "wb") as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"An error occurred while writing binary file: {e}")

    def read_bin_csv(self, filename: str) -> Any:
        """
        Reads data from a binary file using pickle.

        Args:
            filename (str): The path of the binary file.

        Returns:
            Any: The unpickled data. Returns None if an error occurs.
        """
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"An error occurred while reading binary file: {e}")
            return None

    def write_json_file(self, filename: str, content: dict, ensure_ascii: bool = True):
        """
        Writes a dictionary to a JSON file.

        Args:
            filename (str): The path of the output JSON file.
            content (dict): The dictionary to write.
            ensure_ascii (bool, optional): If False, allows writing non-ASCII characters.
                                           Defaults to True.
        """
        try:
            with open(filename, "w", encoding="UTF-8") as f:
                json.dump(content, f, cls=NpEncoder, ensure_ascii=ensure_ascii)
        except Exception as e:
            print(f"An error occurred while writing JSON file: {e}")

    def read_json_file(self, filename: str) -> Union[Dict[Any, Any], None]:
        """
        Reads a JSON file into a dictionary.

        Args:
            filename (str): The path of the JSON file.

        Returns:
            dict: The content of the JSON file as a dictionary.
                  Returns None if an error occurs.
        """
        try:
            with open(filename, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error in file '{filename}': {e}")
            # Fallback to literal_eval for non-standard JSON-like files
            try:
                return self.read_txt_to_dict(filename)
            except Exception as e:
                print(f"Failed to read file as literal dictionary: {e}")
                return None
        except Exception as e:
            print(f"An unknown error occurred while reading JSON file: {e}")
            return None

    def read_txt_to_dict(self, filename: str) -> Dict[Any, Any]:
        """
        Reads a file as a string and evaluates it as a Python dictionary.

        This is a fallback for non-standard JSON-like files (e.g., using single quotes).

        Args:
            filename (str): The path of the file.

        Returns:
            dict: The content of the file as a dictionary.

        Raises:
            ValueError: If the file content is not a valid dictionary representation.
        """
        content = self.read_text_file(filename).replace("\n", "")
        return literal_eval(content)

    def get_all_local_files(self, directory: str, sort: bool = False) -> List[str]:
        """
        Gets a list of all files in a given directory.

        Args:
            directory (str): The path to the directory.
            sort (bool, optional): If True, the list will be sorted alphabetically.
                                   Defaults to False.

        Returns:
            List[str]: A list of file names.
        """
        if not self.dir_exist_check(directory):
            print(f"Directory not found: {directory}")
            return []
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if sort:
            files.sort()
        return files


class fileAddress(fileProcessor):
    """
    A class for managing and resolving directory paths.

    It can scan a root directory to create a mapping of all subdirectories
    and their paths, which can be cached in a file.
    """
    def __init__(self, p_dir: str = "", update: bool = False, update_save: bool = True):
        """
        Initializes the fileAddress instance.

        Args:
            p_dir (str, optional): The base directory path to scan.
                                   Defaults to "".
            update (bool, optional): If True, forces a rescan of the directory tree.
                                     Defaults to False.
            update_save (bool, optional): If True, saves the updated directory mapping
                                          to a JSON file. Defaults to True.
        """
        self.p_dir = p_dir or "/content/drive/My Drive/"
        self.dir_fname = "dir_map.json"
        self.dir_cache: Dict[str, str] = {}

        if update:
            self.dir_cache = self._get_all_dirs(self.p_dir, update_save=update_save)
        else:
            self.dir_cache = self.get_full_dir_from_file()
            if not self.dir_cache:
                self.dir_cache = self._get_all_dirs(self.p_dir, update_save=update_save)

    def get_dir(self, dir_name: str) -> Union[str, None]:
        """
        Returns the full path of a directory from the cache.

        Args:
            dir_name (str): The name of the directory.

        Returns:
            Union[str, None]: The full path of the directory, or None if not found.
        """
        if dir_name not in self.dir_cache:
            return None
        return os.path.join(self.dir_cache[dir_name], dir_name)

    def _get_all_dirs(self, root_dir: str, update_save: bool = True) -> Dict[str, str]:
        """
        Recursively scans a directory and maps directory names to their paths.

        Args:
            root_dir (str): The starting path for the scan.
            update_save (bool): If True, saves the mapping to a file.

        Returns:
            Dict[str, str]: A dictionary mapping directory names to their parent paths.
        """
        dir_cache = {}
        for dirpath, dirnames, _ in os.walk(root_dir):
            for dirname in dirnames:
                if dirname not in dir_cache:
                    dir_cache[dirname] = dirpath
        if update_save:
            self.write_json_file(self.path_join(self.p_dir, self.dir_fname), dir_cache)
        print("Done scanning all directories.")
        return dir_cache

    def get_full_dir_from_file(self, filename: Union[str, None] = None) -> Dict[str, str]:
        """
        Loads the directory mapping from a JSON file.

        Args:
            filename (Union[str, None], optional): The name of the cache file.
                                                   Defaults to None, using the
                                                   default `dir_fname`.

        Returns:
            Dict[str, str]: The loaded directory mapping.
        """
        fname = filename or self.path_join(self.p_dir, self.dir_fname)
        if not self.file_exist_check(fname):
            return {}
        content = self.read_json_file(fname)
        return content if content is not None else {}

    def path_join(self, fpath: str, fname: str) -> str:
        """
        Joins a path and a filename.

        Args:
            fpath (str): The path.
            fname (str): The filename.

        Returns:
            str: The joined full path.
        """
        return os.path.join(fpath, fname)

    def find_empty_folders(self, path: str) -> List[str]:
        """
        Finds and returns a list of empty folders within a given path.

        Args:
            path (str): The path to start the search from.

        Returns:
            List[str]: A list of full paths to empty folders.
        """
        empty_folders = []
        for dirpath, dirnames, filenames in os.walk(path):
            if not dirnames and not filenames:
                empty_folders.append(dirpath)
        return empty_folders


class fileStructure:
    """
    A data structure to hold and represent file metadata.
    """
    def __init__(self, filename: str, path: str):
        """
        Initializes the fileStructure instance.

        Args:
            filename (str): The name of the file.
            path (str): The path to the file.
        """
        self.filename = filename
        self.path = path
        self.file_type: str = None
        self.size: int = 0
        self.create_date: Union[date, None] = None

    def set_info(self, finfo: Dict[str, Any]):
        """
        Sets the file's attributes from a dictionary.

        Args:
            finfo (Dict[str, Any]): A dictionary containing file information.
        """
        self.path = finfo.get("path")
        self.filename = finfo.get("filename")
        self.file_type = finfo.get("fileType")
        self.size = finfo.get("size")
        self.create_date = finfo.get("createDate")

    def get_info(self, options: List[str] = ["path", "filename"]) -> Dict[str, Any]:
        """
        Returns a dictionary of selected file attributes.

        Args:
            options (List[str], optional): A list of attribute names to include.
                                           Defaults to ["path", "filename"].

        Returns:
            Dict[str, Any]: A dictionary containing the requested attributes.
        """
        return {
            "path": self.path,
            "filename": self.filename,
            "fileType": self.file_type,
            "size": self.size,
            "createDate": self.create_date,
        }

if __name__ == "__main__":
    # Example usage demonstration
    print("Initializing fileProcessor...")
    fp = fileProcessor()

    # Create a dummy file for demonstration
    fp.write_text_file("test_file.txt", "This is a test file.\nIt has two lines.")

    print("\nReading the file...")
    content = fp.read_text_file("test_file.txt")
    print(f"File content:\n'{content}'")

    print("\nInitializing fileAddress and scanning directories...")
    # This will scan your drive and create dir_map.json
    # Be aware that this might take a while depending on your directory size.
    fa = fileAddress(p_dir=os.getcwd(), update=True)

    print("\nGetting the path of the current directory...")
    current_dir = fa.get_dir('tests')
    if current_dir:
        print(f"Found 'tests' directory at: {current_dir}")
    else:
        print("The 'tests' directory was not found in the cache.")

    # Clean up the dummy file
    fp.delete_files("test_file.txt")
    fp.delete_files(fa.dir_fname)
    print("\nCleaned up test files.")