import unittest
import tempfile
from iislogparser.parsers import W3CIISLogParser
from mock import Mock
import os

class TestEventsFromParser(unittest.TestCase):
    
    def setUp(self):
        self.testContent1 = """#Software: Microsoft Internet Information Services 7.5
#Version: 1.0
#Date: 2012-07-30 00:00:00
#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) sc-status sc-substatus sc-win32-status time-taken 
2012-07-24 12:13:14 10.8.5.123 GET /en/zee_page.html a=1&b=2&c=3 80 Bongo 192.168.0.1 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 1 2 858
"""

    def testEndIsFiredOnSingleListener(self):
        with tempfile.NamedTemporaryFile(suffix="test.json") as tmp1:
            tmp1.write(self.testContent1)
            tmp1.seek(0)
            converter = W3CIISLogParser()
            listener = Mock()
            listener.end = Mock()
            converter.addListener(listener)
            converter.enumerate_files(os.path.dirname(tmp1.name)+"/*test.json")
            self.assertTrue(listener.end.called)

    def testLogitemEventIsFiredOnSingleListener(self):
        with tempfile.NamedTemporaryFile(suffix="test.json") as tmp1:
            tmp1.write(self.testContent1)
            tmp1.seek(0)
            converter = W3CIISLogParser()
            listener = Mock()
            listener.logitem = Mock()
            converter.addListener(listener)
            converter.enumerate_files(os.path.dirname(tmp1.name)+"/*test.json")
            call_args = listener.logitem.call_args[0][0]
            self.assertEqual(call_args["year"],2012)
