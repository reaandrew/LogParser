import unittest
import tempfile
import cjson
import iislogparser.utilities
from iislogparser.parsers import W3CIISLogJsonConverter
from iislogparser.parsers import MethodFilter
from iislogparser.reports import ByHourHitCounts


class TestConvertingW3CIISLog(unittest.TestCase):

    def setUp(self):
        self.testContent = """#Software: Microsoft Internet Information Services 7.5
#Version: 1.0
#Date: 2012-07-30 00:00:00
#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) sc-status sc-substatus sc-win32-status time-taken 
2012-07-30 12:13:14 10.8.5.123 GET /en/zee_page.html a=1&b=2&c=3 80 Bongo 192.168.0.1 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 1 2 858
2012-07-30 13:13:14 10.8.5.123 GET /en/zee_page.html a=1&b=2&c=3 80 Bongo 192.168.0.1 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 1 2 858
2012-07-30 13:14:14 10.8.5.123 POST /en/zee_page.html a=1&b=2&c=3 80 Bongo 192.168.0.1 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 1 2 858
"""

    def testGettingLineN(self):
        method = "POST"
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(self.testContent)
            tmp.seek(0)
            with tempfile.NamedTemporaryFile() as output:
                converter = W3CIISLogJsonConverter()
                by_hour_hit_counts = ByHourHitCounts(output.name, [MethodFilter(method)])
                #converter.count_by_hour_multiple(tmp.name, output.name, filter=Filter(method))
                converter.addListener(by_hour_hit_counts)
                converter.enumerate_files(tmp.name)
                fileData = output.file.read()
                self.jsonObj = cjson.decode(fileData)
        print("DICT", self.jsonObj)
        self.assertEquals(1, len(self.jsonObj.keys()))

