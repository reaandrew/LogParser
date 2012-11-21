import unittest
from iislogparser.filters import UriStemPrefixFilter, FilterMode

class TestUriStemCollectionFilter(unittest.TestCase):

    def testCanFilterWithOneUriStemFilter(self):
        logCollection = []
        logCollection.append( {"cs_uri_stem":"/something"} )
        logCollection.append( {"cs_uri_stem":"/nothing"} )
        filter = UriStemPrefixFilter(["/something"],FilterMode.Exclude)
        logItemsToKeep = []
        for logitem in logCollection:
            if not filter.should_skip(logitem):
                logItemsToKeep.append(logitem)

        self.assertEquals(1, len(logItemsToKeep))
        self.assertEquals("/nothing", logItemsToKeep[0]["cs_uri_stem"])


