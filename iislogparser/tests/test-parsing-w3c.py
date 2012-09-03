import unittest
from iislogparser.parsers import W3CParser

class TestParsingW3CFormat(unittest.TestCase):

    def testParsingDate(self):
        fields = "#Fields: date"
        parser = W3CParser(fields)
        line = "2012-07-30"
        logItem = parser.parse(line)
        self.assertEqual(logItem['year'], 2012)
        self.assertEqual(logItem['month'], 7)
        self.assertEqual(logItem['day'], 30)

    def testParsingTime(self):
        fields = "#Fields: time"
        parser = W3CParser(fields)
        line = "12:13:14"
        logItem = parser.parse(line)
        self.assertEqual(logItem['hour'], 12)
        self.assertEqual(logItem['minute'], 13)
        self.assertEqual(logItem['second'], 14)

    def testParsingClientIPAddress(self):
        fields = "#Fields: c-ip"
        parser = W3CParser(fields)
        line = "10.6.111.6"
        logItem = parser.parse(line)
        self.assertEqual(logItem["c_ip"], line)

    def testParsingUserName(self):
        fields = "#Fields: cs-username"
        parser = W3CParser(fields)
        line = "BOBO"
        logItem = parser.parse(line)
        self.assertEqual(logItem["cs_username"], line)

    def testParsingSiteName(self):
        fields = "#Fields: s-sitename"
        parser = W3CParser(fields)
        line = "somesitename"
        logItem = parser.parse(line)
        self.assertEqual(logItem["s_sitename"], line)
