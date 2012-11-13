import unittest
import tempfile
import cjson

from iislogparser.parsers import W3CIISLogJsonConverter

class TestConvertingW3CIISLog(unittest.TestCase):

    def setUp(self):
        self.testContent = """#Software: Microsoft Internet Information Services 7.5
#Version: 1.0
#Date: 2012-07-30 00:00:00
#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) sc-status sc-substatus sc-win32-status time-taken
2012-07-30 12:13:14 10.8.5.123 GET /en/zee_page.html a=1&b=2&c=3 80 Bongo 192.168.0.1 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 1 2 858
"""
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(self.testContent)
            tmp.seek(0)
            with tempfile.NamedTemporaryFile() as output:
                converter = W3CIISLogJsonConverter()
                print("Converting")
                converter.convert(tmp.name, output.name)

                fileData = output.file.read()
                self.jsonObj = cjson.decode(fileData)

    def testConvertsDateInJsonOutputFile(self):
        self.assertEquals(self.jsonObj['year'], 2012)
        self.assertEquals(self.jsonObj['month'], 7)
        self.assertEquals(self.jsonObj['day'], 30)

    def testConvertsTimeInJsonOutputFile(self):
        self.assertEquals(self.jsonObj['hour'], 12)
        self.assertEquals(self.jsonObj['minute'], 13)
        self.assertEquals(self.jsonObj['second'], 14)

    def testConvertsServerIPInJsonOutputFile(self):
        self.assertEquals(self.jsonObj["s_ip"], "10.8.5.123")

    def testConvertsCsMethodInJsonOutputFile(self):
        self.assertEquals(self.jsonObj["cs_method"], "GET")

    def testConvertsCsUriStemInJsonOutputFile(self):
        self.assertEquals(self.jsonObj["cs_uri_stem"], "/en/zee_page.html")

    def testConvertCsUriQueryInJsonOutputFile(self):
        self.assertEquals(self.jsonObj["cs_uri_query"]["a"], "1")
        self.assertEquals(self.jsonObj["cs_uri_query"]["b"], "2")
        self.assertEquals(self.jsonObj["cs_uri_query"]["c"], "3")

    def testConvertsServerPortInJsonOutputFile(self):
        self.assertEquals(self.jsonObj["s_port"], "80")
    
    def testConvertsClientUserName(self):
        self.assertEquals(self.jsonObj["cs_username"], "Bongo")

    def testConvertsClientIPInJsonOutputFile(self):
        self.assertEquals(self.jsonObj["c_ip"], "192.168.0.1")

    def testConvertsClientUserAgentInJsonOutputFile(self):
        self.assertEquals(self.jsonObj["cs_user_agent"],"Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3")

    def testConvertsServerStatusInJsonOutputFile(self):
        self.assertEquals(self.jsonObj["sc_status"],200)

    def testConvertsServerSubStatusInJsonOutputFile(self):
        self.assertEquals(self.jsonObj["sc_substatus"],1)

    def testConvertsServerWin32Status(self):
        self.assertEquals(self.jsonObj["sc_win32_status"],2)

    def testConvertsServerTimeTaken(self):
        self.assertEquals(self.jsonObj["time_taken"], 858)
