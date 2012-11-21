import unittest
import tempfile
import cjson
import iislogparser.utilities
from iislogparser.parsers import W3CIISLogParser
from iislogparser.filters import *
from iislogparser.reports import ByHourHitCounts
from iislogparser.outputs import MemoryStream


class TestConvertingW3CIISLog(unittest.TestCase):

    def setUp(self):
        self.testContent = """#Software: Microsoft Internet Information Services 7.5
#Version: 1.0
#Date: 2012-07-30 00:00:00
#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) sc-status sc-substatus sc-win32-status time-taken 
2012-07-30 13:13:14 10.8.5.123 GET /en/zee_page.html a=1&b=2&c=3 80 Bongo 192.168.0.1 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 1 2 858
2012-07-30 13:13:14 10.8.5.123 GET /en/zee_other_page.html a=1&b=2&c=3 80 Bongo 192.168.0.1 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 1 2 858
2012-07-30 13:14:14 10.8.5.123 POST /en/zee_page.html a=1&b=2&c=3 80 Bongo 192.168.0.1 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 1 2 858
"""

    def testApplyingIncludeMethodFilter(self):
        method = "POST"
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(self.testContent)
            tmp.seek(0)
            stream = MemoryStream()
            converter = W3CIISLogParser()
            by_hour_hit_counts = ByHourHitCounts(stream, [MethodFilter(method, FilterMode.Include)])
            converter.addListener(by_hour_hit_counts)
            converter.enumerate_files(tmp.name)
            self.obj = stream.read()
        self.assertEquals(1, self.obj["13"])

    def testApplyingExcludeMethodFilter(self):
        method = "POST"
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(self.testContent)
            tmp.seek(0)
            stream = MemoryStream()
            converter = W3CIISLogParser()
            by_hour_hit_counts = ByHourHitCounts(stream, [MethodFilter(method, FilterMode.Exclude)])
            converter.addListener(by_hour_hit_counts)
            converter.enumerate_files(tmp.name)
            self.obj = stream.read()
        self.assertEquals(2, self.obj["13"])

    def testApplyingUriStemPrefixFilter(self):
        stemPrefixToFind = ["/en/zee_page"]
        filter = UriStemPrefixFilter(stemPrefixToFind, FilterMode.Exclude)

        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(self.testContent)
            tmp.seek(0)
            stream = MemoryStream()
            converter = W3CIISLogParser()
            by_hour_hit_counts = ByHourHitCounts(stream, [filter])
            converter.addListener(by_hour_hit_counts)
            converter.enumerate_files(tmp.name)
            self.obj = stream.read()
        self.assertEquals(1, self.obj["13"])
