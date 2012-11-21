from datetime import datetime
from utilities import ExtendedList
import json
import os

class UniqueUriStem:

    def __init__(self, output, filters=[]):
        pass

class ByHourMaxHitCounts:

    def __init__(self, output, filters=[]):
        self.output = output
        self.filters = filters
        self.dates = {}

    def logitem(self, logitem):
        if any([( filter.should_skip(logitem)) for filter in self.filters]):
            return

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
        self.output.write(returnObj)


class ByHourHitCounts:

    def __init__(self, output, filters=[]):
        self.output = output
        self.dates = ExtendedList()
        self.serverips = ExtendedList()
        self.sums = {}
        for hour in range(0,24):
            self.sums[str(hour)] = float(0)
        self.filters = filters
    
    def logitem(self, logitem):
        if any([(filter.should_skip(logitem)) for filter in self.filters]):
            return

        date = datetime(logitem["year"],logitem["month"],logitem["day"])
        self.dates.add_if_not_exists(date)
        serverip = logitem["s_ip"]
        self.serverips.add_if_not_exists(serverip)
        self.sums[str(logitem["hour"])] += 1
    
    def end(self):
        for key in self.sums.keys():
            if len(self.dates) == 0:
                self.sums[key] = 0
            else:
                self.sums[key] /= len(self.dates) * len(self.serverips)

        self.output.write(self.sums)

class IISJsonWriter:

    def __init__(self, output):
        self.output = output

    def logitem(self, logitem):
        with open(self.output, "ab") as out:
            jsonEncoded = json.dumps(logitem)
            out.write(jsonEncoded)

    def end(self):
        pass
