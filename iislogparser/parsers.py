from datetime import datetime
import json
import urlparse
import linecache

class W3CFieldParser:

    def parse(self, filename):
        fieldsLine = linecache.getline(filename,4)
        fields = fieldsLine[fieldsLine.index(": ")+2:]
        return fields.split(" ")

class W3CLogItemParser:

    def __init__(self, fields):
        self.items = fields[fields.find(": ")+2:].replace("\n","").split(" ")
        self.itemparsers = []
        for item in self.items:
            #Need to change below to have a helper function for the replace.  Avoiding regex due to performance
            #Only a certain number of chars to consider replacing at this stage.  Keeping with replace or helper function
            self.itemparsers.append(lambda lineitems: \
                    getattr(self, "__add_"+item.replace("-","_").replace("(","").replace(")","").lower()+"__") \
                    (lineitems,self.items.index(item)))

    def parse(self, line):
        lineitems = line.split(" ")
        logitem = {}
        for itemparser in self.itemparsers:
            logitems = itemparser(lineitems)
            logitem.update(logitems)

        return logitem
    
    def __add_date__(self, lineitems, index):
        output = {}
        parsedDate = datetime.strptime(lineitems[index],"%Y-%m-%d")
        output["year"] = parsedDate.year
        output["month"] = parsedDate.month
        output["day"] = parsedDate.day
        print("returning", output)
        return output
    
    def __add_time__(self, lineitems, index):
        output = {}
        parsedTime = datetime.strptime(lineitems[index],"%H:%M:%S")
        output["hour"] = parsedTime.hour
        output["minute"] = parsedTime.minute
        output["second"] = parsedTime.second
        return output
        
    def __add_c_ip__(self, lineitems, index):
        output = {}
        output["c_ip"] = lineitems[index]
        return output

    def __add_cs_username__(self, lineitems, index):
        output = {}
        output["cs_username"] = lineitems[index]
        return output

    def __add_s_sitename__(self, lineitems, index):
        output = {}
        output["s_sitename"] = lineitems[index]
        return output

    def __add_s_computername__(self, lineitems, index):
        output = {}
        output["s_computername"] = lineitems[index]
        return output

    def __add_s_ip__(self, lineitems, index):
        output = {}
        output["s_ip"] = lineitems[index]
        return output
    
    def __add_s_port__(self, lineitems, index):
        output = {}
        output["s_port"] = lineitems[index]
        return output

    def __add_cs_method__(self, lineitems, index):
        output = {}
        output["cs_method"] = lineitems[index]
        return output

    def __add_cs_uri_stem__(self, lineitems, index):
        output = {}
        output["cs_uri_stem"] = lineitems[index]
        return output

    def __add_cs_uri_query__(self, lineitems, index):
        output = {}
        querystring = lineitems[index]
        parsedQuerystring = urlparse.parse_qs(querystring)
        for key in parsedQuerystring.keys():
            if len(parsedQuerystring[key]) == 1:
                parsedQuerystring[key] = parsedQuerystring[key][0]
        output["cs_uri_query"] = parsedQuerystring
        return output

    def __add_sc_status__(self, lineitems, index):
        output = {}
        try:
            output["sc_status"] = int(lineitems[index])
        except ValueError:
            pass
        return output

    def __add_sc_sub_status__(self, lineitems, index):
        output = {}
        try:
            output["sc_sub_status"] = int(lineitems[index])
        except ValueError:
            #Not an int, apparantly in python they go with EAFP "Easier to ask for forgiveness than permission"
            pass
        return output

    def __add_sc_win32_status__(self, lineitems, index):
        output = {}
        try:
            output["sc_win32_status"] = int(lineitems[index])
        except ValueError:
            pass
        return output

    def __add_sc_bytes__(self, lineitems, index):
        output = {}
        try:
            output["sc_bytes"] = int(lineitems[index])
        except ValueError:
            pass
        return output

    def __add_cs_bytes__(self, lineitems, index):
        output = {}
        try:
            output["cs_bytes"] = int(lineitems[index])
        except ValueError:
            pass
        return output

    def __add_time_taken__(self, lineitems, index):
        output = {}
        try:
            output["time_taken"] = int(lineitems[index])
        except ValueError:
            pass
        return output

    def __add_cs_version__(self, lineitems, index):
        output = {}
        output["cs_version"] = lineitems[index]
        return output

    def __add_cs_host__(self, lineitems, index):
        output = {}
        output["cs_host"] = lineitems[index]
        return output

    def __add_csuser_agent__(self, lineitems, index):
        output = {}
        output["cs_user_agent"] = lineitems[index]
        return output

    def __add_cscookie__(self, lineitems, index):
        output = {}
        output["cs_cookie"] = lineitems[index]
        return output

    def __add_csreferer__(self, lineitems, index):
        output = {}
        output["cs_referer"] = lineitems[index]
        return output

class W3CIISLogJsonConverter:

    def convert(self, infilename, outfilename):

        linecount = 0
        lines = ""
        fieldsLine = linecache.getline(infilename,4)
        logItemParser = W3CLogItemParser(fieldsLine)
        encoder = json.JSONEncoder(ensure_ascii=False)
        with open(infilename, "rb") as logfile:
            with open(outfilename, "ab") as out:
                for line in logfile:
                    linecount += 1
                    if linecount > 4:
                        logitem = logItemParser.parse(line)
                        jsonEncoded = encoder.encode(logitem)+"\n"
                        lines += jsonEncoded
                        if linecount % 25000 == 0:
                            out.write(lines)
                            lines = ""
                out.write(lines)
                        
