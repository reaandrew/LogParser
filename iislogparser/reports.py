from datetime import datetime
from utilities import ExtendedList
import json

class ByHourHitCounts:

    def __init__(self, output, filters=[]):
        self.output = output
        self.dates = ExtendedList()
        self.serverips = ExtendedList()
        self.sums = {}
        self.filters = filters
        self.count = 0;
    
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
        self.count += 1
        if self.count % 10000 == 0:
            print(self.count)
    
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
