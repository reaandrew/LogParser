import unittest
import tempfile

from iislogparser.parsers import W3CIISLogJsonConverter

class TestConvertingW3CIISLog(unittest.TestCase):

    def testConvertingSimpleFile(self):
        print("TEST")
        testContent = """#Software: Microsoft Internet Information Services 7.5
#Version: 1.0
#Date: 2012-07-30 00:00:00
#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) sc-status sc-substatus sc-win32-status time-taken
        2012-07-30 00:00:00 10.8.5.123 GET /en/indonesia/gili_trawangan/191229-manta_bungalows.html - 80 - 195.245.125.101 Mozilla/5.0+(iPad;+CPU+OS+5_1_1+like+Mac+OS+X)+AppleWebKit/534.46+(KHTML,+like+Gecko)+Version/5.1+Mobile/9B206+Safari/7534.48.3 200 0 0 858
"""
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(testContent)
            tmp.seek(0)
            with tempfile.NamedTemporaryFile() as output:
                converter = W3CIISLogJsonConverter()
                print("Converting")
                converter.convert(tmp.name, output.name)
                output.seek(0)
                count = 0
                for line in output:
                    count += 1

                self.assertEqual(count, 1)

