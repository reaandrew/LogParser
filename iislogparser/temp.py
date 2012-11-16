    def count_by_hour(self, infilename, outfilename):

        counts = dict()
        linecount = 0
        logItemParser = W3CLogItemParser(fieldsLine)
        encoder = json.JSONEncoder(ensure_ascii=False)
        with open(infilename, "rb") as logfile:
            with open(outfilename, "ab") as out:
                for line in logfile:
                    linecount += 1
                    if not line.startswith("#"):
                        logitem = logItemParser.parse(line)
                        if not logitem.h in counts:
                            counts[logitem.h] = 0

                        counts[logitem.h] += 1
                jsonEncoded = cjson.encode(counts)
                out.write(jsonEncoded)
