from datetime import datetime

class W3CParser:

    def __init__(self, fields):
        self.items = fields[fields.find(": ")+2:].split(" ")
        self.itemparsers = []
        for item in self.items:
            self.itemparsers.append(lambda lineitems,output: \
                    getattr(self, "__add_"+item.replace("-","_")+"__") \
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
