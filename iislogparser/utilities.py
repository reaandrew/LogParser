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
