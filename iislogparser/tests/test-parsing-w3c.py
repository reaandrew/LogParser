import unittest
from iislogparser.parsers import W3CLogItemParser

class TestParsingW3CFormat(unittest.TestCase):

    def testParsingFieldWithNewLine(self):
        fields="#Fields: time-taken\n"
        parser = W3CLogItemParser(fields)
        line = "1234"
        logItem = parser.parse(line)
        self.assertEqual(logItem["time_taken"], 1234)

    def testParsingDate(self):
        fields = "#Fields: date"
        parser = W3CLogItemParser(fields)
        line = "2012-07-30"
        logItem = parser.parse(line)
        self.assertEqual(logItem['year'], 2012)
        self.assertEqual(logItem['month'], 7)
        self.assertEqual(logItem['day'], 30)

    def testParsingTime(self):
        fields = "#Fields: time"
        parser = W3CLogItemParser(fields)
        line = "12:13:14"
        logItem = parser.parse(line)
        self.assertEqual(logItem['hour'], 12)
        self.assertEqual(logItem['minute'], 13)
        self.assertEqual(logItem['second'], 14)

    def testParsingClientIPAddress(self):
        fields = "#Fields: c-ip"
        parser = W3CLogItemParser(fields)
        line = "10.6.111.6"
        logItem = parser.parse(line)
        self.assertEqual(logItem["c_ip"], line)

    def testParsingUserName(self):
        fields = "#Fields: cs-username"
        parser = W3CLogItemParser(fields)
        line = "BOBO"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_username"], line)

    def testParsingSiteName(self):
        fields = "#Fields: s-sitename"
        parser = W3CLogItemParser(fields)
        line = "somesitename"
        logItem = parser.parse(line)
        self.assertEqual(logItem["s_sitename"], line)

    def testParsingComputerName(self):
        fields = "#Fields: s-computername"
        parser = W3CLogItemParser(fields)
        line = "COMP"
        logItem = parser.parse(line)
        self.assertEqual(logItem["s_computername"], line)

    def testParsingSIP(self):
        fields = "#Fields: s-ip"
        parser = W3CLogItemParser(fields)
        line = "10.8.8.900"
        logItem = parser.parse(line)
        self.assertEqual(logItem["s_ip"], line)

    def testParsingSPort(self):
        fields = "#Fields: s-port"
        parser = W3CLogItemParser(fields)
        line = "80"
        logItem = parser.parse(line)
        self.assertEqual(logItem["s_port"], line)

    def testParsingCsMethod(self):
        fields = "#Fields: cs-method"
        parser = W3CLogItemParser(fields)
        line = "POST"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_method"], line)

    def testParsingCsUriStem(self):
        fields = "#Fields: cs-uri-stem"
        parser = W3CLogItemParser(fields)
        line = "/a/b/c/d.aspx"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_uri_stem"], line)

    def testParsingCsUriQuery(self):
        fields = "#Fields: cs-uri-query"
        parser = W3CLogItemParser(fields)
        line = "a=1&b=2"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_uri_query"]["a"],"1")
        self.assertEqual(logItem["cs_uri_query"]["b"],"2")

    def testParsingScStatus(self):
        fields = "#Fields: sc-status"
        parser = W3CLogItemParser(fields)
        line = "200"
        logItem = parser.parse(line)
        self.assertEqual(logItem["sc_status"], 200)
    
    def testParsingScSubStatus(self):
        fields = "#Fields: sc-sub-status"
        parser = W3CLogItemParser(fields)
        line = "0"
        logItem = parser.parse(line)
        self.assertEqual(logItem["sc_sub_status"], 0)

    def testParsingNonIntSubStatus(self):
        fields = "#Fields: sc-sub-status"
        parser = W3CLogItemParser(fields)
        line = "-"
        logItem = parser.parse(line)
        self.assertFalse("sc_sub_status" in logItem.keys())

    def testParsingScWin32Status(self):
        fields = "#Fields: sc-win32-status"
        parser = W3CLogItemParser(fields)
        line = "0"
        logItem = parser.parse(line)
        self.assertEqual(logItem["sc_win32_status"], 0)

    def testParsingScBytes(self):
        fields = "#Fields: sc-bytes"
        parser = W3CLogItemParser(fields)
        line = "3456"
        logItem = parser.parse(line)
        self.assertEqual(logItem["sc_bytes"], 3456)

    def testParsingCsBytes(self):
        fields = "#Fields: cs-bytes"
        parser = W3CLogItemParser(fields)
        line = "1234"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_bytes"], 1234)

    def testParsingTimeTaken(self):
        fields = "#Fields: time-taken"
        parser = W3CLogItemParser(fields)
        line = "234"
        logItem = parser.parse(line)
        self.assertEqual(logItem["time_taken"], 234)

    def testParsingCsVersion(self):
        fields = "#Fields: cs-version"
        parser = W3CLogItemParser(fields)
        line = "12"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_version"], "12")

    def testParsingCsHost(self):
        fields = "#Fields: cs-host"
        parser = W3CLogItemParser(fields)
        line = "host"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_host"], line)

    def testParsingCsUserAgent(self):
        fields = "#Fields: cs(User-Agent)"
        parser = W3CLogItemParser(fields)
        line = "blablaMozillaChromeEI"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_user_agent"],line) 

    def testParsingCsCookie(self):
        fields = "#Fields: cs(Cookie)"
        parser = W3CLogItemParser(fields)
        line = "monster"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_cookie"], line)

    def testParsingCsReferer(self):
        fields = "#Fields: cs(Referer)"
        parser = W3CLogItemParser(fields)
        line = "http://www.google.com"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_referer"], line)

    def testParsingMultipleFields(self):
        fields = "#Fields: cs-host time-taken"
        parser = W3CLogItemParser(fields)
        line = "host 1234"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_host"], "host")
        self.assertEqual(logItem["time_taken"], "1234")
