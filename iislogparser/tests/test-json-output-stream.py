import unittest
import tempfile
from iislogparser.outputs import JsonFileStream

class TestJsonOutputStream(unittest.TestCase):

    def setUp(self):
        pass

    def testSomething(self):
        bob = dict({"1": 1, "2": 2})
        with tempfile.NamedTemporaryFile() as file:
            stream = JsonFileStream(file.name)
            stream.write(bob)
            self.obj = stream.read()
        self.assertEquals(self.obj["1"], 1)
