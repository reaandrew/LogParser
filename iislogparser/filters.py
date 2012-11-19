class MethodFilter:
    
    def __init__(self, method):
        self.method = method

    def should_skip(self, logitem):
        return self.method != None \
            and logitem["cs_method"] != self.method
