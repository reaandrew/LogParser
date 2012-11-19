from datetime import datetime
from utilities import ExtendedList
import json

class ByHourMaxHitCounts:

    def __init__(self, output, filters=[]):
        self.output = output
        self.filters = filters
        self.dates = {}

    def logitem(self, logitem):
        key = logitem["year"] + logitem["month"] + logitem["day"]
        if key not in self.dates:
            self.dates[key] = {}

        if logitem["hour"] not in self.dates[key]:
            self.dates[key][logitem["hour"]] = 0
        self.dates[key][logitem["hour"]] += 1

    def end(self):
        returnObj = {}
        for hour in range(0,24):
            returnObj[hour] = 0
            for key in self.dates.keys():
                if hour in self.dates[key]:
                    if self.dates[key][hour] > returnObj[hour]:
                        returnObj[hour] = self.dates[key][hour]
        self.__write_to__(self.output, returnObj)

    def __write_to__(self, outputpath, obj):
        with open(outputpath, "ab") as out:
            jsonEncoded = json.dumps(obj, indent=4)
            out.write(jsonEncoded)

class ByHourHitCounts:

    def __init__(self, output, filters=[]):
        self.output = output
        self.dates = ExtendedList()
        self.serverips = ExtendedList()
        self.sums = {}
        self.filters = filters
    
    def logitem(self, logitem):
        if any([(filter.should_skip(logitem)) for filter in self.filters]):
            return

        date = datetime(logitem["year"],logitem["month"],logitem["day"])
        self.dates.add_if_not_exists(date)
        serverip = logitem["s_ip"]
        self.serverips.add_if_not_exists(serverip)
        if not str(logitem["hour"]) in self.sums:
            self.sums[str(logitem["hour"])] = float(0)
        self.sums[str(logitem["hour"])] += 1
    
    def end(self):
        for key in self.sums.keys():
            self.sums[key] /= len(self.dates) * len(self.serverips)

        self.__write_to__(self.output)

    def __write_to__(self, outputpath):
        with open(outputpath, "ab") as out:
            jsonEncoded = json.dumps(self.sums, indent=4)
            out.write(jsonEncoded)

class IISJsonWriter:

    def __init__(self, output):
        self.output = output

    def logitem(self, logitem):
        with open(self.output, "ab") as out:
            jsonEncoded = json.dumps(logitem)
            out.write(jsonEncoded)

    def end(self):
        pass
