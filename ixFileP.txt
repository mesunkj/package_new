以下是 ixFileP.py 中每個函式與類別的描述：

---

### **JSON 與資料處理相關函式**
1. **`writeJsonFile(fname, content)`**
   - 將資料以 JSON 格式寫入檔案。

2. **`writeJsonCFile(fname, content)`**
   - 將資料以 JSON 格式寫入檔案，支援中文（`ensure_ascii=False`）。

3. **`readJsonFile(fname)`**
   - 從 JSON 檔案讀取資料，若失敗則嘗試以字典格式讀取。

4. **`save_dict_to_file_R(filename, dic)`**
   - 將字典以字串形式儲存至檔案。

5. **`read_txt_to_dict(filename)`**
   - 將文字檔案內容轉換為字典。

6. **`read_txt(filename)`**
   - 讀取文字檔案內容。

7. **`writeBinCsv(filename, data)`**
   - 將資料以二進位格式儲存至檔案。

8. **`readBinCsv(filename)`**
   - 從二進位檔案讀取資料。

9. **`readDictWithPD(f1)`**
   - 使用 `pickle` 從檔案讀取字典。

10. **`saveDictWithPD(dicDate, f1)`**
    - 使用 `pickle` 將字典儲存至檔案。

---

### **檔案操作相關函式**
11. **`fileExistCheck(fname)`**
    - 檢查檔案是否存在。

12. **`dirExistCheck(dir)`**
    - 檢查目錄是否存在。

13. **`fullnameDirExistCheck(fname)`**
    - 檢查檔案的完整目錄是否存在。

14. **`creatFolder(directory)`**
    - 建立目錄。

15. **`renamefile(fromFile, toFile)`**
    - 重命名檔案。

16. **`deletFiles(f, fd)`**
    - 刪除指定檔案。

17. **`deletetree(fd)`**
    - 刪除整個目錄。

18. **`recursive_overwrite(src, dest, ignore)`**
    - 遞迴覆寫目錄內容。

19. **`copyfile(src, dest)`**
    - 複製檔案。

20. **`getFullPath(path, fname)`**
    - 取得完整檔案路徑。

21. **`getfileDate(fname)`**
    - 取得檔案的最後修改日期。

22. **`get_file_size_in_bytes(file_path)`**
    - 取得檔案大小（以位元組為單位）。

23. **`chkBytes(f1, f2)`**
    - 比較兩個檔案的大小是否相近。

24. **`perf(f1, f2)`**
    - 計算兩個檔案大小的相對差異。

25. **`saveListToFile(fname, lc)`**
    - 將清單內容儲存至檔案。

26. **`inplace_change(filename, old_string, new_string)`**
    - 在檔案中替換指定字串。

27. **`writef(name, content)`**
    - 將內容寫入檔案。

---

### **壓縮與解壓縮相關函式**
28. **`zipdir(path, filename)`**
    - 將目錄壓縮為 ZIP 檔案。

29. **`get_size_under_folder(start_path, deTC)`**
    - 計算目錄下所有檔案的總大小。

---

### **CSV 與檔案讀寫相關函式**
30. **`saveToCsv(filename, list1, columnsP, indexP, dump)`**
    - 將資料儲存為 CSV 檔案。

31. **`readCSVFile(filename)`**
    - 讀取 CSV 檔案，若失敗則嘗試以二進位格式讀取。

32. **`readLargerFile(filename, lineReturn)`**
    - 逐行讀取大型檔案。

33. **`readTextFile(filename, encoding)`**
    - 讀取文字檔案。

34. **`openTextFile(filename, mode, encoding)`**
    - 開啟文字檔案。

35. **`writeTextFile(filename, content, mode, encoding)`**
    - 寫入文字檔案。

---

### **目錄與檔案清單相關函式**
36. **`getListOfFiles(dirName, ext)`**
    - 遞迴取得目錄中的檔案清單，支援副檔名過濾。

37. **`scanAllLocalFile(fd)`**
    - 掃描目錄中的所有檔案。

38. **`getAllLocalFile(fd, isort)`**
    - 取得目錄中的所有檔案，並可選擇排序。

39. **`get_files_size_in_bytes(path, files, ext)`**
    - 計算指定檔案的大小。

40. **`get_files_size_in_bytes_v1(path_list)`**
    - 計算多個檔案的總大小。

41. **`count_files_size(path_list)`**
    - 計算多個檔案的大小總和。

---

### **圖片與目錄結構相關函式**
42. **`takePic(f)`**
    - 取得圖片的拍攝日期（需要 `exifread` 模組）。

43. **`create_img_Dir(dirName, parentDirName)`**
    - 建立圖片目錄。

44. **`getAllPath(dirName, parentDirName)`**
    - 取得目錄的完整路徑。

---

### **類別**
1. **`NpEncoder`**
   - 自訂 JSON 編碼器，支援 NumPy 資料型別。

2. **`fileP`**
   - 提供檔案操作的主要功能。

3. **`fAddress`**
   - 管理目錄結構，支援目錄快取與更新。

4. **`fileStructure`**
   - 儲存檔案的基本資訊（如名稱、路徑、大小等）。

---

### **其他功能**
1. **`select_files(initial_path)`**
   - 使用檔案對話框選擇檔案。

---

如果需要更詳細的解釋或修改，請告訴我！