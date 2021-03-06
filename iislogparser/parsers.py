from datetime import datetime
import urlparse
import glob
import json
import utilities
import cStringIO
from utilities import ExtendedList

class W3CLogItemParser:

    def __init__(self, fields):
        self.items = fields.strip()[fields.find(": ")+2:].replace("\n","").split(" ")

        self.indexes = {}
        for item in self.items:
            self.indexes[item] = self.items.index(item)

    def getIndex(self, key):
        if self.indexes.has_key(key):
            return self.indexes[key]
        return -1

    def parse(self, line):
        lineitems = line.split(" ")
        logitem = {}
        for item in self.items:
            index = self.indexes[item] 
            namereplacement = item.replace("-","_").replace("(","").replace(")","").lower()
            currentFunction = getattr(self, "__add_"+namereplacement+"__")
            currentResult = currentFunction(lineitems, self.indexes[item])
            logitem.update(currentResult)
    
        return logitem
    
    def __add_date__(self, lineitems, index):
        output = {}
        if(index > -1):
            #parsedDate = datetime.strptime(lineitems[index],"%Y-%m-%d")
            parsedDate = lineitems[index]
            output["year"] = int(parsedDate[0:4])
            output["month"] = int(parsedDate[5:7])
            output["day"] = int(parsedDate[8:10])
        return output
    
    def __add_time__(self, lineitems, index):
        output = {}
        if(index > -1):
            #parsedTime = datetime.strptime(lineitems[index],"%H:%M:%S")
            parsedTime = lineitems[index]
            output["hour"] = int(parsedTime[0:2])
            output["minute"] = int(parsedTime[3:5])
            output["second"] = int(parsedTime[6:8])
        return output
        
    def __add_c_ip__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["c_ip"] = lineitems[index]
        return output

    def __add_cs_username__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["cs_username"] = lineitems[index]
        return output

    def __add_s_sitename__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["s_sitename"] = lineitems[index]
        return output

    def __add_s_computername__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["s_computername"] = lineitems[index]
        return output

    def __add_s_ip__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["s_ip"] = lineitems[index]
        return output
    
    def __add_s_port__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["s_port"] = lineitems[index]
        return output

    def __add_cs_method__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["cs_method"] = lineitems[index]
        return output

    def __add_cs_uri_stem__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["cs_uri_stem"] = lineitems[index]
        return output

    def __add_cs_uri_query__(self, lineitems, index):
        output = {}
        if(index > -1):
            querystring = lineitems[index]
            parsedQuerystring = urlparse.parse_qs(querystring)
            for key in parsedQuerystring.keys():
                if len(parsedQuerystring[key]) == 1:
                    parsedQuerystring[key] = parsedQuerystring[key][0]
            output["cs_uri_query"] = parsedQuerystring
        return output

    def __add_sc_status__(self, lineitems, index):
        output = {}
        if(index > -1):
            try:
                output["sc_status"] = int(lineitems[index])
            except ValueError:
                pass
        return output

    def __add_sc_substatus__(self, lineitems, index):
        output = {}
        if(index > -1):
            try:
                output["sc_substatus"] = int(lineitems[index])
            except ValueError:
                #Not an int, apparantly in python they go with EAFP "Easier to ask for forgiveness than permission"
                pass
        return output

    def __add_sc_win32_status__(self, lineitems, index):
        output = {}
        if(index > -1):
            try:
                output["sc_win32_status"] = int(lineitems[index])
            except ValueError:
                pass
        return output

    def __add_sc_bytes__(self, lineitems, index):
        output = {}
        if(index > -1):
            try:
                output["sc_bytes"] = int(lineitems[index])
            except ValueError:
                pass
        return output

    def __add_cs_bytes__(self, lineitems, index):
        output = {}
        if(index > -1):
            try:
                output["cs_bytes"] = int(lineitems[index])
            except ValueError:
                pass
        return output

    def __add_time_taken__(self, lineitems, index):
        output = {}
        if(index > -1):
            try:
                output["time_taken"] = int(lineitems[index])
            except ValueError:
                pass
        return output

    def __add_cs_version__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["cs_version"] = lineitems[index]
        return output

    def __add_cs_host__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["cs_host"] = lineitems[index]
        return output

    def __add_csuser_agent__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["cs_user_agent"] = lineitems[index]
        return output

    def __add_cscookie__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["cs_cookie"] = lineitems[index]
        return output

    def __add_csreferer__(self, lineitems, index):
        output = {}
        if(index > -1):
            output["cs_referer"] = lineitems[index]
        return output


class W3CIISLogParser:

    def __init__(self):
        self.itemListeners = []

    def addListener(self, listener):
        self.itemListeners.append(listener)

    def __call_end__(self):
        for listener in self.itemListeners:
            listener.end()

    def __call_log_item__(self, logitem):
        for listener in self.itemListeners:
            listener.logitem(logitem)

    def enumerate_files(self, file_pattern, filter=None):
        files = glob.glob(file_pattern)
        for infilename in files:
            with open(infilename, "rb") as logfile:
                fieldsLine = utilities.getLineStartingWith("#Fields", logfile)
                logItemParser = W3CLogItemParser(fieldsLine)
                for line in logfile:
                    if line.startswith("#"):
                        continue
                    logitem = logItemParser.parse(line)
                    self.__call_log_item__(logitem)
        self.__call_end__()

