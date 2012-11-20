
from outputs import JsonFileStream
from parsers import W3CIISLogParser
from reports import ByHourHitCounts, ByHourMaxHitCounts
from filters import MethodFilter
import os

def count_by_hour(args):
    
    outputdir = os.path.abspath(args.outputdirectory)
    avgoutputpath = os.path.join(outputdir ,"avgbyhour.json")
    maxoutputpath = os.path.join(outputdir, "maxbyhour.json")
    avgoutput = JsonFileStream(avgoutputpath)
    maxoutput = JsonFileStream(maxoutputpath)

    converter = W3CIISLogParser()
    parserFilters = []
    if args.method != None and args.method.strip() != "":
        parserFilters.append(MethodFilter(args.method))

    avg_hit_count = ByHourHitCounts(avgoutput, filters=parserFilters)
    max_hit_count = ByHourMaxHitCounts(maxoutput, filters=parserFilters)

    converter.addListener(avg_hit_count)
    converter.addListener(max_hit_count)
    converter.enumerate_files(args.file)
