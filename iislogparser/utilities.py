def getLineStartingWith(linePrefix, file):  
    file.seek(0)
    current = 0
    line = None
    while(True):
        line = file.readline()
        if line.startswith(linePrefix):
            return line
        if line == '':
            break

    return None

class ExtendedList(list):

    def add_if_not_exists(self, item):
        if item not in self:
            self.append(item)
