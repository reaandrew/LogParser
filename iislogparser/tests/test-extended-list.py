import unittest
from iislogparser.utilities import ExtendedList

class TestExtendedList(unittest.TestCase):
    
    def testAddingAnElementWhichDoesNotExist(self):
        item = "A1"
        list = ExtendedList()
        list.add_if_not_exists(item)
        list.add_if_not_exists(item)
        self.assertEqual(1, len(list))
