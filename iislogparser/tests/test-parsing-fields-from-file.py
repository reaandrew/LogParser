import unittest
import os
from iislogparser.parsers import W3CFieldParser

class TestParsingFieldsFromFile(unittest.TestCase):

    def testParsingW3CFile(self):
        filename = "tmp.log"
        testContent = """#Software: Microsoft Internet Information Services 7.5
#Version: 1.0
#Date: 2012-07-30 00:00:00
#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) sc-status sc-substatus sc-win32-status time-taken
        """
        with os.tmpfile() as tmp:
            tmp.write(testContent)
        fieldParser = W3CFieldParser()
        fields = fieldParser.parse(filename)
        self.assertEqual(len(fields), 14)

