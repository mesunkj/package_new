# _*_ coding:utf-8 _*_

# procedure detailed in readme.txt
# from datetime import datetime
from datetime import datetime, timedelta, time, date
import datetime as dtime
import dateutil.relativedelta
import re
import numpy as np
import calendar


class datetimeUtils:
    def getNowDateTimeStr(self, format="%y%m%d %H%M%S%f"):
        # time.sleep(1)
        date_time = datetime.now()
        return date_time.strftime(format)

    def getTime(self, format="%H%M%S%f"):
        return self.getNowDateTimeStr(format=format)

    def getDateList(self, dateIdx=None):
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
        dU = self
        sdate = dU.strToDate(str(fr))  # start date
        edate = dU.strToDate(str(to))  # end date

        delta = edate - sdate  # as timedelta
        sC = []
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            dt = datetime.combine(day, datetime.min.time())
            dt1 = dU.datetimeToStrByFormat(dt, formate="%Y%m%d")
            weekend = {5, 6}
            if dt.weekday() not in weekend:
                sC.append(int(dt1))
        return sC

    def getNow(self):
        return str(datetime.now().date())

    def getNowDate(self, dd1=""):
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
        return datetime.strftime("%Y-%m-%d")

    def datetimeToStrByFormat_R(self, dTime, formate="%Y-%m-%d"):  # "%Y-%m-%d %H:%M:%S"
        return dTime.strftime(formate)

    def datetimeToStrByFormat(self, timestamp, formate="%Y-%m-%d"):  # "%Y-%m-%d %H:%M:%S"

        dTime = datetime.fromtimestamp(timestamp)
        return dTime.strftime(formate)

    def strToDateTime(self, dstr=None):
        string = dstr
        if self.checkDate(string) is None:
            return None
        return datetime(int(string[0:4]), int(string[4:6]), int(string[6:]))

    def strToDate(self, dstr):
        string = dstr
        return date(int(string[0:4]), int(string[4:6]), int(string[6:]))

    def floatToTimestamp(self, mtime=None):
        return datetime.fromtimestamp(mtime)

    def strToDateTimeDelima(self, dstr, delima=None):
        """ex 2018-03-01"""
        string = dstr
        if delima != None:
            string = dstr.replace(delima, "")
        if self.checkDate(string) is None:
            return None
        return datetime.strptime(string, "%Y%m%d")

    def checkDate(self, string=None, format="YYYYmmdd"):
        if format == "YYYYmmdd":
            # string ='20170808'
            pattern = "[0-9]{8}"
            prog = re.compile(pattern)

            result = prog.match(string)
            return result

    def checkDayInDuration(self, string=None, format="YYYYmmdd"):
        if self.checkDate(string) is None:
            return None
        d = datetime(int(string[0:4]), int(string[4:6]), int(string[6:]))
        d2 = datetime.now()
        t = d2 - d
        if t.days < 0:
            return None
        return t

    def dateTimeDuration(self, start, end):
        """ type of start and end is datetime"""
        v = end - start
        return v.days

    def getStartDateList(self, dateList):
        shiftYear = dateList[0]
        shfitMonth = dateList[1]
        shiftDay = dateList[2]
        return self.getStartDate(shiftYear=shiftYear, shfitMonth=shfitMonth, shiftDay=shiftDay)

    def getStartDateString(self, string):
        d = datetime(int(string[0:4]), int(string[4:6]), int(string[6:]))
        d2 = datetime.now()
        days = (d2 - d).days
        return self.getStartDate(shiftYear=0, shfitMonth=0, shiftDay=days)

    def getStartDate(self, shiftYear=0, shfitMonth=0, shiftDay=0):
        d = datetime.now()
        d2 = d - dateutil.relativedelta.relativedelta(years=shiftYear)
        d3 = d2 - dateutil.relativedelta.relativedelta(months=shfitMonth)
        d4 = d3 - dateutil.relativedelta.relativedelta(days=shiftDay)

        return d4, (d - d4).days

    def getDateBySubstract(self, dDate, forward=True, shiftDay=0):
        # usage: d2 = getDateBySubstract(dEnd, forward = True, shiftDay = 90)
        dDate = datetime.strptime(dDate, "%Y-%m-%d")
        if forward:
            nDate = dDate - timedelta(days=shiftDay)
        else:
            nDate = dDate + timedelta(days=shiftDay)

        return nDate

    def getWeeklyDay(self, date=None):
        if date is None:
            date = self.getNowDateTimeStr(format="%Y%m%d")
        return datetime.today().weekday()  # Sunday:0 Staurday:6

    def isOutWorkDate_(self, date=None):
        if date is None:
            date = self.getNowDateTimeStr(format="%Y%m%d")
        dayNum = self.getWeeklyDay(date)
        if dayNum in [0, 6]:
            return True
        else:
            return False

    def secToDateTime(self, ss):
        return str(dtime.timedelta(seconds=ss))

    def strToTime(self, dd, sep=""):
        return sep.join([dd[:4], dd[4:6], dd[6:8]])

    def strTostTime(self, start, op="start"):
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

    def last_day_of_month(self, any_day):  # like tuple as (year,month)
        return calendar.monthrange(any_day[0], any_day[1])[1]

    def strToDatetime(self, strP, inFormat="%Y:%m:%d %H:%M:%S", outFormat="%Y%m%d_%H%M%S"):
        date_time_obj = datetime.strptime(strP, inFormat)
        return date_time_obj.strftime(outFormat)


dt = datetimeUtils()


class utils:
    def floatFormat(self, val, fix=2):
        ff = "{0:." + str(fix) + "f}"
        return float(ff.format(val))

    def percentFormat(self, var):
        return "{0:.1f}%".format(var * 100)

    def strTostTime(self, start, op="start"):
        test = "20170101"
        if op != "start":
            test = "20171232"
        if type(start) == int:
            start = str(start)
        if len(start) < 8:
            start = start + test[8 - len(start) :]
        return "-".join([start[:4], start[4:6], start[6:8]]) + " 13:30:00"

    def convType(self, itype, val):
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
        return splitLine.join(cList)

    def strToList(self, str="", splitLine=""):
        return str.split(splitLine)

    def NOK(self, errDesc, data=None):
        return {"state": "Not OK", "comment": errDesc, "data": data}

    def OK(self, data, comment=""):
        return {
            "state": "OK",
            "data": data,
            "date": dt.getNowDate(),
            "comment": comment,
        }

    def OK_(self, obj, isPrint=False):
        if isPrint:
            print(obj["comment"])
        if obj["state"] == "OK":
            return True
        else:
            return False

    def combineStr(self, strL):
        return "".join(strL)

    def chkAryIsNumber(self, vals):
        return not (True in np.isnan(np.array(vals)))  # vals like list contained value

    def chkDivdZero(self, vals, chkKeys=None, dtype="dict"):  # vals like dict , chkkeys: like fields to be checked
        div_ = ["股本合計", "股東權益總額", "營業收入", "稅前淨利"]
        if chkKeys is not None:
            div_ = chkKeys
        if dtype == "dict":
            return len([vals[fd] for fd in vals if fd in div_ and vals[fd] == 0]) > 0
        if dtype == "csv":
            return len([vals[div_.index(fd)] for fd in vals if fd in div_ and vals[fd] == 0]) > 0
        return True

    def convertString(self, val):
        return float(val.replace(",", ""))

    def stTimeTostr(self, dd):
        return dd.split(" ")[0].replace("-", "")

    def chkPriceIfNull(self, fdName, val):
        chkfd = ["Volume", "Open", "High", "Low", "Close", "rate"]
        if chkfd.index(fdName) < 0:
            return False
        else:
            return self.chkNull(val)

    def chkNull(self, val):
        # self.chkDivdZero()
        # chkfd = ["Volume", "Open", "High", "Low", "Close", "rate"]
        # if chkfd.index(fdName) < 0:
        #     return False

        try:
            valx = float(val)
            return self.chkBoth(valx)
        except:
            return False

    def chkBoth(self, val):
        if self.chkNumberIsNull(val):
            return True
        if self.chkNumberIsEmpty(val):
            return True
        return False

    def chkNumberIsNull(self, val):

        if val == None:
            return True
        return False

    def chkNumberIsEmpty(self, val):
        if val == None or val == 0:
            return True
        return False

    def getValue_(self, fd, fds, data, dtype="csv"):
        # print('fd {} fds {} ，data {} '.format(fd,fds,data))
        if dtype == "JSON":
            return data[fd]
        else:
            return data[fds.index(fd)]

    def getValueByField_(self, data_, fds, fd):
        return self.getValue_(fd, fds, data_, dtype="csv")


class _expressFunction:
    def checkOK(self, state, key):
        if key == None:
            key = "state"
        if "stat" in state:
            key = "stat"  # for daily stock file
        if state is None or state[key] is None or state[key].lower() != "ok":
            return False
        return True
