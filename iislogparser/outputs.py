import json

class MemoryStream:

    def __init__(self):
        self.obj = None

    def write(self, obj):
        self.obj = obj

    def read(self):
        return self.obj

class JsonFileStream:

    def __init__(self, filepath):
        self.obj = None
        self.filepath = filepath

    def write(self, obj):
        with open(self.filepath, "wb") as output:
            output.seek(0)
            output.write(json.dumps(obj))
    
    def read(self):
        with open(self.filepath, "rb") as inputstream:
            inputstream.seek(0)
            return json.loads(inputstream.read())
