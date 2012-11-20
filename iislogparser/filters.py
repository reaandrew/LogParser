class FilterMode:
    Include=True
    Exclude=False

class MethodFilter:
    
    def __init__(self, method, mode = FilterMode.Exclude):
        self.method = method
        self.mode = mode

    def should_skip(self, logitem):
        return self.mode != (self.method != None \
            and logitem["cs_method"] == self.method)

class UriStemPrefixFilter:

    def __init__(self, prefix, mode = FilterMode.Exclude):
        self.prefix = prefix
        self.mode = mode

    def should_skip(self, logitem):
        return self.mode != (self.prefix != None \
            and logitem["cs_uri_stem"].startswith(self.prefix))
