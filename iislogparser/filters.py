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

    def __init__(self, prefixes, mode = FilterMode.Exclude):
        self.prefixes = prefixes
        self.mode = mode

    def should_skip(self, logitem):
        return self.mode != (self.prefixes != None \
            and any ([(logitem["cs_uri_stem"].startswith(prefix)) for prefix in self.prefixes]))
