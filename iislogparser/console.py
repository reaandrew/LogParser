from outputs import JsonFileStream
from parsers import W3CIISLogParser
from reports import ByHourHitCounts, ByHourMaxHitCounts, UniqueUriStems
from filters import *
import os

def get_applicable_filters(args):
    
    parserFilters = []
    if args.method != None and args.method.strip() != "":
        parserFilters.append(MethodFilter(args.method))

    if args.uI != None and len(args.uI) > 0:
        uriargs = args.uI.split(",")
        parserFilters.append(UriStemPrefixFilter(uriargs, FilterMode.Include))
    if args.uE != None and len(args.uE) > 0:
        uriargs = args.uE.split(",")
        parserFilters.append(UriStemPrefixFilter(uriargs, FilterMode.Exclude))

    return parserFilters

def count_by_hour(args):
    
    outputdir = os.path.abspath(args.outputdirectory)
    avgoutputpath = os.path.join(outputdir ,"avgbyhour.json")
    maxoutputpath = os.path.join(outputdir, "maxbyhour.json")
    avgoutput = JsonFileStream(avgoutputpath)
    maxoutput = JsonFileStream(maxoutputpath)

    converter = W3CIISLogParser()
    parserFilters = get_applicable_filters(args)

    avg_hit_count = ByHourHitCounts(avgoutput, filters=parserFilters)
    max_hit_count = ByHourMaxHitCounts(maxoutput, filters=parserFilters)

    converter.addListener(avg_hit_count)
    converter.addListener(max_hit_count)
    converter.enumerate_files(args.file)

def unique_uri_stems(args):
    outputdir = os.path.abspath(args.outputdirectory)
    uristemspath = os.path.join(outputdir, "uniqueuristems.json")
    uristems = JsonFileStream(uristemspath)

    converter = W3CIISLogParser()
    parserFilters = get_applicable_filters(args)

    unique_uri_stems = UniqueUriStems(uristems, filters=parserFilters)

    converter.addListener(unique_uri_stems)
    converter.enumerate_files(args.file)
