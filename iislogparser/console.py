from outputs import JsonFileStream
from parsers import W3CIISLogParser
from reports import ByHourHitCounts, ByHourMaxHitCounts
from filters import *
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

    if args.uI != None and args.uI.strip() != "":
        uriargs = args.uI.split(",")
        parserFilters.append(UriStemPrefixFilter(uriargs, FilterMode.Include))
    if args.uE != None and args.uE.strip() != "":
        uriargs = args.uE.split(",")
        parserFilters.append(UriStemPrefixFilter(uriargs, FilterMode.Exclude))

    avg_hit_count = ByHourHitCounts(avgoutput, filters=parserFilters)
    max_hit_count = ByHourMaxHitCounts(maxoutput, filters=parserFilters)

    converter.addListener(avg_hit_count)
    converter.addListener(max_hit_count)
    converter.enumerate_files(args.file)
