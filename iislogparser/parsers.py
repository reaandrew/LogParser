from datetime import datetime
import urlparse

class W3CParser:

    def __init__(self, fields):
        self.items = fields[fields.find(": ")+2:].split(" ")
        self.itemparsers = []
        for item in self.items:
            #Need to change below to have a helper function for the replace.  Avoiding regex due to performance
            #Only a certain number of chars to consider replacing at this stage.  Keeping with replace or helper function
            self.itemparsers.append(lambda lineitems,output: \
                    getattr(self, "__add_"+item.replace("-","_").replace("(","").replace(")","").lower()+"__") \
                    (lineitems,output,self.items.index(item)))

    def parse(self, line):
        lineitems = line.split(" ")
        logitem = {}
        for itemparser in self.itemparsers:
            itemparser(lineitems, logitem)

        return logitem
    
    def __add_date__(self, lineitems, output, index):
        parsedDate = datetime.strptime(lineitems[index],"%Y-%m-%d")
        output["year"] = parsedDate.year
        output["month"] = parsedDate.month
        output["day"] = parsedDate.day
    
    def __add_time__(self, lineitems, output, index):
        parsedTime = datetime.strptime(lineitems[index],"%H:%M:%S")
        output["hour"] = parsedTime.hour
        output["minute"] = parsedTime.minute
        output["second"] = parsedTime.second
        
    def __add_c_ip__(self, lineitems, output, index):
        output["c_ip"] = lineitems[index]

    def __add_cs_username__(self, lineitems, output, index):
        output["cs_username"] = lineitems[index]

    def __add_s_sitename__(self, lineitems, output, index):
        output["s_sitename"] = lineitems[index]

    def __add_s_computername__(self, lineitems, output, index):
        output["s_computername"] = lineitems[index]

    def __add_s_ip__(self, lineitems, output, index):
        output["s_ip"] = lineitems[index]
    
    def __add_s_port__(self, lineitems, output, index):
        output["s_port"] = lineitems[index]

    def __add_cs_method__(self, lineitems, output, index):
        output["cs_method"] = lineitems[index]

    def __add_cs_uri_stem__(self, lineitems, output, index):
        output["cs_uri_stem"] = lineitems[index]

    def __add_cs_uri_query__(self, lineitems, output, index):
        querystring = lineitems[index]
        parsedQuerystring = urlparse.parse_qs(querystring)
        for key in parsedQuerystring.keys():
            if len(parsedQuerystring[key]) == 1:
                parsedQuerystring[key] = parsedQuerystring[key][0]
        output["cs_uri_query"] = parsedQuerystring

    def __add_sc_status__(self, lineitems, output, index):
        try:
            output["sc_status"] = int(lineitems[index])
        except ValueError:
            pass

    def __add_sc_sub_status__(self, lineitems, output, index):
        try:
            output["sc_sub_status"] = int(lineitems[index])
        except ValueError:
            #Not an int, apparantly in python they go with EAFP "Easier to ask for forgiveness than permission"
            pass

    def __add_sc_win32_status__(self, lineitems, output, index):
        try:
            output["sc_win32_status"] = int(lineitems[index])
        except ValueError:
            pass

    def __add_sc_bytes__(self, lineitems, output, index):
        try:
            output["sc_bytes"] = int(lineitems[index])
        except ValueError:
            pass

    def __add_cs_bytes__(self, lineitems, output, index):
        try:
            output["cs_bytes"] = int(lineitems[index])
        except ValueError:
            pass

    def __add_time_taken__(self, lineitems, output, index):
        try:
            output["time-taken"] = int(lineitems[index])
        except ValueError:
            pass

    def __add_cs_version__(self, lineitems, output, index):
        output["cs_version"] = lineitems[index]

    def __add_cs_host__(self, lineitems, output, index):
        output["cs_host"] = lineitems[index]

    def __add_csuser_agent__(self, lineitems, output, index):
        output["cs_user_agent"] = lineitems[index]

    def __add_cscookie__(self, lineitems, output, index):
        output["cs_cookie"] = lineitems[index]

    def __add_csreferer__(self, lineitems, output, index):
        output["cs_referer"] = lineitems[index]
