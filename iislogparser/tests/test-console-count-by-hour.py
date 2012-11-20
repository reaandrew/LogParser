import unittest
import tempfile
import json
import os
import iislogparser.console

class dotdict(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
        __setattr__= dict.__setitem__
        __delattr__= dict.__delitem__

class TestConvertingW3CIISLog(unittest.TestCase):

    def setUp(self):
        self.testContent = """#Software: Microsoft Internet Information Services 7.5
#Version: 1.0
#Date: 2012-07-30 00:00:00
#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) sc-status sc-substatus sc-win32-status time-taken 
2012-07-30 12:13:14 10.8.5.123 GET /en/zee_page.html a=1&b=2&c=3 80 Bongo 192.168.0.1 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 1 2 858
2012-07-30 13:13:14 10.8.5.123 GET /en/zee_page.html a=1&b=2&c=3 80 Bongo 192.168.0.1 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 1 2 858
2012-07-30 13:14:14 10.8.5.123 GET /en/zee_page.html a=1&b=2&c=3 80 Bongo 192.168.0.1 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 1 2 858
"""

    def testGettingCountByHour(self):
        with tempfile.NamedTemporaryFile() as inputfile:
            inputfile.write(self.testContent)
            inputfile.seek(0)
            args = dotdict()
            args.outputdirectory = tempfile.gettempdir() 
            args.file = inputfile.name
        
            print(inputfile.name)
            iislogparser.console.count_by_hour(args)
            filename = os.path.join(args.outputdirectory, "maxbyhour.json")
            with open(filename, "rb") as test:
                obj = json.loads(test.read())
            self.assertEquals(obj["12"], 1)


                
            

