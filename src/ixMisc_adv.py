# _*_ coding:utf-8 _*_

from datetime import datetime, timedelta, time, date
import datetime as dtime
import dateutil.relativedelta
import re
import numpy as np
import calendar


class datetimeUtils:
    """
    一個提供日期和時間相關實用方法的類別。

    此類別包含用於處理日期格式、時間戳、日期區間和週末檢查的函數。
    """
    def getNowDateTimeStr(self, format="%y%m%d %H%M%S%f"):
        """
        獲取當前日期和時間，並以指定格式返回為字串。

        Args:
            format (string, optional): 輸出的日期時間格式。預設為 "%y%m%d %H%M%S%f"。
            
        Returns:
            string: 格式化後的當前日期時間字串。
        """
        date_time = datetime.now()
        return date_time.strftime(format)

    def getTime(self, format="%H%M%S%f"):
        """
        獲取當前時間，並以指定格式返回為字串。

        Args:
            format (string, optional): 輸出的時間格式。預設為 "%H%M%S%f"。
            
        Returns:
            string: 格式化後的當前時間字串。
        """
        return self.getNowDateTimeStr(format=format)

    def getDateList(self, dateIdx=None):
        """
        根據索引獲取日期清單。

        此方法似乎是從一個外部未定義的清單中獲取日期資訊。

        Args:
            dateIdx (int, optional): 日期索引。預設為 None。
            
        Returns:
            list: 包含年、月、日的整數列表。
        """
        if dateIdx is None:
            return [0, 0, 0]
        dateStr = self.getList()["selectDate"][dateIdx]
        if "年" in dateStr:
            return [int(dateStr.split("年")[0]), 0, 0]
        if "月" in dateStr:
            return [0, int(dateStr.split("月")[0]), 0]
        if "日" in dateStr:
            return [0, 0, int(dateStr.split("日")[0])]

    def listDateBetweenExceptWeekend(self, fr, to):
        """
        列出兩個日期之間的所有工作日（不包含週末）。

        Args:
            fr (int or string): 起始日期，格式為 YYYYMMDD。
            to (int or string): 結束日期，格式為 YYYYMMDD。
            
        Returns:
            list: 包含兩個日期之間所有工作日的整數列表。
        """
        dU = self
        sdate = dU.strToDate(str(fr))  # start date
        edate = dU.strToDate(str(to))  # end date

        delta = edate - sdate
        sC = []
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            dt = datetime.combine(day, datetime.min.time())
            dt1 = dU.datetimeToStrByFormat(dt, formate="%Y%m%d")
            weekend = {5, 6}  # 5是星期六，6是星期日
            if dt.weekday() not in weekend:
                sC.append(int(dt1))
        return sC

    def getNow(self):
        """
        獲取當前日期。

        Returns:
            string: 當前日期字串，格式為 'YYYY-MM-DD'。
        """
        return str(datetime.now().date())

    def getNowDate(self, dd1=""):
        """
        獲取當前日期，並移除分隔符。

        Args:
            dd1 (string, optional): 日期字串，格式為 YYYY-MM-DD。預設為空字串，將使用當前日期。
            
        Returns:
            string: 格式為 YYYYMMDD 的日期字串。
        """
        if dd1 == "":
            dd = self.getNow()
        else:
            dd = dd1
        try:
            dd = str(dd).split()[0].replace("-", "")
        except Exception as err:
            print("Error at getNowDate ", err)
        return dd

    def datetimeFormat(self):
        """
        返回預設的日期時間格式字串。

        Returns:
            string: 格式字串 "%Y-%m-%d"。
        """
        return datetime.strftime("%Y-%m-%d")

    def datetimeToStrByFormat_R(self, dTime, formate="%Y-%m-%d"):
        """
        將 datetime 物件格式化為字串。

        Args:
            dTime (datetime): datetime 物件。
            formate (string, optional): 輸出的格式字串。預設為 "%Y-%m-%d"。
            
        Returns:
            string: 格式化後的日期時間字串。
        """
        return dTime.strftime(formate)

    def datetimeToStrByFormat(self, timestamp, formate="%Y-%m-%d"):
        """
        將 Unix 時間戳轉換為格式化的日期時間字串。

        Args:
            timestamp (float): Unix 時間戳。
            formate (string, optional): 輸出的格式字串。預設為 "%Y-%m-%d"。
            
        Returns:
            string: 格式化後的日期時間字串。
        """
        dTime = datetime.fromtimestamp(timestamp)
        return dTime.strftime(formate)

    def strToDateTime(self, dstr=None):
        """
        將格式為 YYYYMMDD 的字串轉換為 datetime 物件。

        Args:
            dstr (string, optional): 格式為 YYYYMMDD 的日期字串。
            
        Returns:
            datetime.datetime or None: 轉換後的 datetime 物件，如果格式不正確則返回 None。
        """
        string = dstr
        if self.checkDate(string) is None:
            return None
        return datetime(int(string[0:4]), int(string[4:6]), int(string[6:]))

    def strToDate(self, dstr):
        """
        將格式為 YYYYMMDD 的字串轉換為 date 物件。

        Args:
            dstr (string): 格式為 YYYYMMDD 的日期字串。
            
        Returns:
            datetime.date: 轉換後的 date 物件。
        """
        string = dstr
        return date(int(string[0:4]), int(string[4:6]), int(string[6:]))

    def floatToTimestamp(self, mtime=None):
        """
        將浮點數時間戳轉換為 datetime 物件。

        Args:
            mtime (float, optional): Unix 時間戳。
            
        Returns:
            datetime.datetime: 轉換後的 datetime 物件。
        """
        return datetime.fromtimestamp(mtime)

    def strToDateTimeDelima(self, dstr, delima=None):
        """
        將帶有分隔符的日期字串（如 2018-03-01）轉換為 datetime 物件。

        Args:
            dstr (string): 帶有分隔符的日期字串。
            delima (string, optional): 日期字串中的分隔符。
            
        Returns:
            datetime.datetime or None: 轉換後的 datetime 物件，如果格式不正確則返回 None。
        """
        string = dstr
        if delima != None:
            string = dstr.replace(delima, "")
        if self.checkDate(string) is None:
            return None
        return datetime.strptime(string, "%Y%m%d")

    def checkDate(self, string=None, format="YYYYmmdd"):
        """
        檢查字串是否為有效日期，格式為 YYYYmmdd。

        Args:
            string (string, optional): 要檢查的日期字串。
            format (string, optional): 預期的日期格式。預設為 "YYYYmmdd"。
            
        Returns:
            re.Match or None: 如果匹配則返回匹配物件，否則返回 None。
        """
        if format == "YYYYmmdd":
            pattern = "[0-9]{8}"
            prog = re.compile(pattern)
            result = prog.match(string)
            return result

    def checkDayInDuration(self, string=None, format="YYYYmmdd"):
        """
        檢查給定日期是否在當前日期之前，並返回兩者之間的 timedelta。

        Args:
            string (string, optional): 格式為 YYYYmmdd 的日期字串。
            format (string, optional): 預期的日期格式。預設為 "YYYYmmdd"。
            
        Returns:
            datetime.timedelta or None: 如果日期有效且在當前日期之前，則返回 timedelta 物件，否則返回 None。
        """
        if self.checkDate(string) is None:
            return None
        d = datetime(int(string[0:4]), int(string[4:6]), int(string[6:]))
        d2 = datetime.now()
        t = d2 - d
        if t.days < 0:
            return None
        return t

    def dateTimeDuration(self, start, end):
        """
        計算兩個 datetime 物件之間的日數差異。

        Args:
            start (datetime.datetime): 起始日期時間。
            end (datetime.datetime): 結束日期時間。
            
        Returns:
            int: 兩個日期之間的天數。
        """
        v = end - start
        return v.days

    def getStartDateList(self, dateList):
        """
        根據給定的年、月、日偏移量獲取一個過去的起始日期。

        Args:
            dateList (list): 包含年、月、日偏移量的整數列表。
            
        Returns:
            tuple: 包含 datetime.datetime 物件和天數差異的元組。
        """
        shiftYear = dateList[0]
        shfitMonth = dateList[1]
        shiftDay = dateList[2]
        return self.getStartDate(shiftYear=shiftYear, shfitMonth=shfitMonth, shiftDay=shiftDay)

    def getStartDateString(self, string):
        """
        根據一個格式為 YYYYMMDD 的字串獲取一個過去的起始日期。

        Args:
            string (string): 格式為 YYYYMMDD 的日期字串。
            
        Returns:
            tuple: 包含 datetime.datetime 物件和天數差異的元組。
        """
        d = datetime(int(string[0:4]), int(string[4:6]), int(string[6:]))
        d2 = datetime.now()
        days = (d2 - d).days
        return self.getStartDate(shiftYear=0, shfitMonth=0, shiftDay=days)

    def getStartDate(self, shiftYear=0, shfitMonth=0, shiftDay=0):
        """
        根據年、月、日偏移量從當前日期獲取一個過去的起始日期。

        Args:
            shiftYear (int, optional): 年份偏移量。預設為 0。
            shfitMonth (int, optional): 月份偏移量。預設為 0。
            shiftDay (int, optional): 日期偏移量。預設為 0。
            
        Returns:
            tuple: 包含 datetime.datetime 物件和天數差異的元組。
        """
        d = datetime.now()
        d2 = d - dateutil.relativedelta.relativedelta(years=shiftYear)
        d3 = d2 - dateutil.relativedelta.relativedelta(months=shfitMonth)
        d4 = d3 - dateutil.relativedelta.relativedelta(days=shiftDay)
        return d4, (d - d4).days

    def getDateBySubstract(self, dDate, forward=True, shiftDay=0):
        """
        在給定日期上增加或減少指定的天數。

        Args:
            dDate (string): 格式為 "%Y-%m-%d" 的日期字串。
            forward (bool, optional): 如果為 True，則日期向前偏移（減去天數）；如果為 False，則向後偏移（加上天數）。
                                     預設為 True。
            shiftDay (int, optional): 要偏移的天數。預設為 0。
            
        Returns:
            datetime.datetime: 偏移後的 datetime 物件。
        """
        dDate = datetime.strptime(dDate, "%Y-%m-%d")
        if forward:
            nDate = dDate - timedelta(days=shiftDay)
        else:
            nDate = dDate + timedelta(days=shiftDay)
        return nDate

    def getWeeklyDay(self, date=None):
        """
        獲取當前日期的星期數。

        Args:
            date (string, optional): 日期字串。預設為 None，將使用當前日期。
            
        Returns:
            int: 星期數（0=星期一，6=星期日）。
        """
        if date is None:
            date = self.getNowDateTimeStr(format="%Y%m%d")
        return datetime.today().weekday()  # 0是星期一，6是星期日

    def isOutWorkDate_(self, date=None):
        """
        檢查給定日期是否為週末。

        Args:
            date (string, optional): 日期字串。預設為 None，將使用當前日期。
            
        Returns:
            bool: 如果是週末則返回 True，否則返回 False。
        """
        if date is None:
            date = self.getNowDateTimeStr(format="%Y%m%d")
        dayNum = self.getWeeklyDay(date)
        if dayNum in [5, 6]:  # 5是星期六，6是星期日
            return True
        else:
            return False

    def secToDateTime(self, ss):
        """
        將秒數轉換為格式化後的持續時間字串。

        Args:
            ss (int): 秒數。
            
        Returns:
            string: 格式為 '小時:分鐘:秒' 的持續時間字串。
        """
        return str(dtime.timedelta(seconds=ss))

    def strToTime(self, dd, sep=""):
        """
        將格式為 YYYYMMDD 的日期字串插入分隔符。

        Args:
            dd (string): 格式為 YYYYMMDD 的日期字串。
            sep (string, optional): 用於分隔的字元。預設為空字串。
            
        Returns:
            string: 插入分隔符後的日期字串。
        """
        return sep.join([dd[:4], dd[4:6], dd[6:8]])

    def strTostTime(self, start, op="start"):
        """
        將日期字串轉換為帶有預設時間的格式。

        Args:
            start (string or int): 日期字串。
            op (string, optional): 操作類型，如果不是 'start'，將使用不同的預設時間。預設為 "start"。
            
        Returns:
            string: 格式為 "YYYY-MM-DD 13:30:00" 的日期時間字串。
        """
        test = "20170101"
        if start is not None:
            if (start).find("13:30:00") >= 0:
                return start
        if op != "start":
            test = "20171232"
        if type(start) == int:
            start = str(start)
        if len(start) < 8:
            start = start + test[8 - len(start) :]
        return "-".join([start[:4], start[4:6], start[6:8]]) + " 13:30:00"

    def last_day_of_month(self, any_day):
        """
        獲取指定月份的最後一天。

        Args:
            any_day (tuple): 包含年和月的元組，例如 (year, month)。
            
        Returns:
            int: 月份的最後一天。
        """
        return calendar.monthrange(any_day[0], any_day[1])[1]

    def strToDatetime(self, strP, inFormat="%Y:%m:%d %H:%M:%S", outFormat="%Y%m%d_%H%M%S"):
        """
        將一個格式化日期字串轉換為另一個格式的日期字串。

        Args:
            strP (string): 格式化日期時間字串。
            inFormat (string, optional): 輸入的日期時間格式。預設為 "%Y:%m:%d %H:%M:%S"。
            outFormat (string, optional): 輸出的日期時間格式。預設為 "%Y%m%d_%H%M%S"。
            
        Returns:
            string: 轉換後的日期時間字串。
        """
        date_time_obj = datetime.strptime(strP, inFormat)
        return date_time_obj.strftime(outFormat)


dt = datetimeUtils()


class utils:
    """
    一個包含各種通用實用方法的類別。

    這些方法涵蓋了格式化數字、轉換資料類型、處理字串以及檢查數值和資料狀態。
    """
    def floatFormat(self, val, fix=2):
        """
        格式化浮點數，保留指定的小數點位數。

        Args:
            val (float): 要格式化的浮點數。
            fix (int, optional): 要保留的小數點位數。預設為 2。
            
        Returns:
            float: 格式化後的浮點數。
        """
        ff = "{0:." + str(fix) + "f}"
        return float(ff.format(val))

    def percentFormat(self, var):
        """
        將浮點數轉換為百分比格式。

        Args:
            var (float): 要轉換的浮點數，例如 0.5。
            
        Returns:
            string: 格式為 "xx.x%" 的百分比字串。
        """
        return "{0:.1f}%".format(var * 100)

    def strTostTime(self, start, op="start"):
        """
        將日期字串轉換為帶有預設時間的格式。

        Args:
            start (string or int): 日期字串。
            op (string, optional): 操作類型，如果不是 'start'，將使用不同的預設時間。預設為 "start"。
            
        Returns:
            string: 格式為 "YYYY-MM-DD 13:30:00" 的日期時間字串。
        """
        test = "20170101"
        if op != "start":
            test = "20171232"
        if type(start) == int:
            start = str(start)
        if len(start) < 8:
            start = start + test[8 - len(start) :]
        return "-".join([start[:4], start[4:6], start[6:8]]) + " 13:30:00"

    def convType(self, itype, val):
        """
        將值轉換為指定的類型。

        Args:
            itype (string): 目標類型，可以是 'float', 'str' 或 'int'。
            val (any): 要轉換的值。
            
        Returns:
            any or None: 轉換後的值，如果轉換失敗則返回 None。
        """
        try:
            if itype == "float":
                return float(val)
            if itype == "str":
                return str(val)
            if itype == "int":
                return int(val)
        except:
            return None

    def listToString(self, cList=[], splitLine=""):
        """
        將列表中的元素連接成一個字串。

        Args:
            cList (list, optional): 要連接的字串列表。預設為空列表。
            splitLine (string, optional): 用於連接的分隔符。預設為空字串。
            
        Returns:
            string: 連接後的字串。
        """
        return splitLine.join(cList)

    def strToList(self, str="", splitLine=""):
        """
        將字串拆分為一個列表。

        Args:
            str (string, optional): 要拆分的字串。預設為空字串。
            splitLine (string, optional): 用於拆分的分隔符。預設為空字串。
            
        Returns:
            list: 包含拆分後字串的列表。
        """
        return str.split(splitLine)

    def NOK(self, errDesc, data=None):
        """
        創建一個表示失敗狀態的字典。

        Args:
            errDesc (string): 失敗的描述。
            data (any, optional): 相關數據。預設為 None。
            
        Returns:
            dict: 包含 'state', 'comment' 和 'data' 的字典。
        """
        return {"state": "Not OK", "comment": errDesc, "data": data}

    def OK(self, data, comment=""):
        """
        創建一個表示成功狀態的字典。

        Args:
            data (any): 相關數據。
            comment (string, optional): 成功註解。預設為空字串。
            
        Returns:
            dict: 包含 'state', 'data', 'date' 和 'comment' 的字典。
        """
        return {
            "state": "OK",
            "data": data,
            "date": dt.getNowDate(),
            "comment": comment,
        }

    def OK_(self, obj, isPrint=False):
        """
        檢查狀態字典是否成功。

        Args:
            obj (dict): 包含 'state' 鍵的字典。
            isPrint (bool, optional): 如果為 True，則打印註解。預設為 False。
            
        Returns:
            bool: 如果狀態為 "OK" 則返回 True，否則返回 False。
        """
        if isPrint:
            print(obj["comment"])
        if obj["state"] == "OK":
            return True
        else:
            return False

    def combineStr(self, strL):
        """
        將字串列表連接成一個字串。

        Args:
            strL (list): 要連接的字串列表。
            
        Returns:
            string: 連接後的字串。
        """
        return "".join(strL)

    def chkAryIsNumber(self, vals):
        """
        檢查列表中的所有值是否都是數字。

        Args:
            vals (list): 包含值的列表。
            
        Returns:
            bool: 如果所有值都是數字則返回 True，否則返回 False。
        """
        return not (True in np.isnan(np.array(vals)))

    def chkDivdZero(self, vals, chkKeys=None, dtype="dict"):
        """
        檢查字典或列表中的特定值是否為零。

        Args:
            vals (dict or list): 要檢查的值。
            chkKeys (list, optional): 要檢查的鍵列表。預設為 None，將使用預設的鍵列表。
            dtype (string, optional): 數據類型，可以是 "dict" 或 "csv"。預設為 "dict"。
            
        Returns:
            bool: 如果任何一個值為零則返回 True，否則返回 False。
        """
        div_ = ["股本合計", "股東權益總額", "營業收入", "稅前淨利"]
        if chkKeys is not None:
            div_ = chkKeys
        if dtype == "dict":
            return len([vals[fd] for fd in vals if fd in div_ and vals[fd] == 0]) > 0
        if dtype == "csv":
            return len([vals[div_.index(fd)] for fd in vals if fd in div_ and vals[fd] == 0]) > 0
        return True

    def convertString(self, val):
        """
        將包含逗號的字串數字轉換為浮點數。

        Args:
            val (string): 包含逗號的數字字串。
            
        Returns:
            float: 轉換後的浮點數。
        """
        return float(val.replace(",", ""))

    def stTimeTostr(self, dd):
        """
        將日期時間字串轉換為格式為 YYYYMMDD 的日期字串。

        Args:
            dd (string): 日期時間字串。
            
        Returns:
            string: 格式為 YYYYMMDD 的日期字串。
        """
        return dd.split(" ")[0].replace("-", "")

    def chkPriceIfNull(self, fdName, val):
        """
        檢查價格相關欄位的值是否為空。

        Args:
            fdName (string): 欄位名稱。
            val (any): 要檢查的值。
            
        Returns:
            bool: 如果值為空則返回 True，否則返回 False。
        """
        chkfd = ["Volume", "Open", "High", "Low", "Close", "rate"]
        if chkfd.index(fdName) < 0:
            return False
        else:
            return self.chkNull(val)

    def chkNull(self, val):
        """
        檢查值是否為空或無法轉換為數字。

        Args:
            val (any): 要檢查的值。
            
        Returns:
            bool: 如果值為空或無法轉換則返回 True，否則返回 False。
        """
        try:
            valx = float(val)
            return self.chkBoth(valx)
        except:
            return False

    def chkBoth(self, val):
        """
        檢查數字是否為 None 或空。

        Args:
            val (any): 要檢查的值。
            
        Returns:
            bool: 如果值為 None 或 0 則返回 True，否則返回 False。
        """
        if self.chkNumberIsNull(val):
            return True
        if self.chkNumberIsEmpty(val):
            return True
        return False

    def chkNumberIsNull(self, val):
        """
        檢查數字是否為 None。

        Args:
            val (any): 要檢查的值。
            
        Returns:
            bool: 如果值為 None 則返回 True，否則返回 False。
        """
        if val == None:
            return True
        return False

    def chkNumberIsEmpty(self, val):
        """
        檢查數字是否為 None 或 0。

        Args:
            val (any): 要檢查的值。
            
        Returns:
            bool: 如果值為 None 或 0 則返回 True，否則返回 False。
        """
        if val == None or val == 0:
            return True
        return False

    def getValue_(self, fd, fds, data, dtype="csv"):
        """
        從數據中獲取指定欄位的值。

        Args:
            fd (string): 欄位名稱。
            fds (list): 欄位名稱列表。
            data (dict or list): 數據。
            dtype (string, optional): 數據類型，可以是 "JSON" 或 "csv"。預設為 "csv"。
            
        Returns:
            any: 獲取到的值。
        """
        if dtype == "JSON":
            return data[fd]
        else:
            return data[fds.index(fd)]

    def getValueByField_(self, data_, fds, fd):
        """
        根據欄位名稱從數據中獲取值。

        Args:
            data_ (list): 數據列表。
            fds (list): 欄位名稱列表。
            fd (string): 要獲取值的欄位名稱。
            
        Returns:
            any: 獲取到的值。
        """
        return self.getValue_(fd, fds, data_, dtype="csv")


class _expressFunction:
    """
    一個包含用於檢查狀態的輔助函數的類別。
    """
    def checkOK(self, state, key):
        """
        檢查狀態字典是否為 'ok'。

        Args:
            state (dict): 包含狀態資訊的字典。
            key (string): 狀態鍵的名稱。
            
        Returns:
            bool: 如果狀態為 'ok' 則返回 True，否則返回 False。
        """
        if key == None:
            key = "state"
        if "stat" in state:
            key = "stat"
        if state is None or state[key] is None or state[key].lower() != "ok":
            return False
        return True