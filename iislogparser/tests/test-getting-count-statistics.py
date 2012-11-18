import unittest
import tempfile
import cjson
import os
from iislogparser.reports import ByHourHitCounts
from iislogparser.parsers import W3CIISLogJsonConverter

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
        with tempfile.NamedTemporaryFile(suffix="test.json") as tmp:
            tmp.write(self.testContent)
            tmp.seek(0)
            with tempfile.NamedTemporaryFile() as output:
                converter = W3CIISLogJsonConverter()
                by_hour_counts = ByHourHitCounts(output.name)
                converter.addListener(by_hour_counts)
                #print("Converting")
                #converter.count_by_hour_multiple(tmp.name, output.name)
                converter.enumerate_files(os.path.dirname(tmp.name)+"/*test.json")
                fileData = output.file.read()
                self.jsonObj = cjson.decode(fileData)

    def testGettingCountByHour(self):
        self.assertEquals(self.jsonObj['12'], 1)
        self.assertEquals(self.jsonObj['13'], 2)

