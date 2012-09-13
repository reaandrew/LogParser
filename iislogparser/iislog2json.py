from parsers import W3CIISLogJsonConverter
import argparse
import glob
import os

parser = argparse.ArgumentParser(description='Convert IIS Log in W3C Format into JSON')
parser.add_argument('file',  help='The path to the file to convert.  filename or wildcard e.g. "*.log". Enclose the wildcard pattern in single or double quotes.')
parser.add_argument('output',  help='The output file to write the converted log')

args = parser.parse_args()

for file in glob.glob(args.file):
    filepath = os.path.abspath(file)
    outputpath = os.path.abspath(args.output)
    print(filepath, outputpath)
    converter = W3CIISLogJsonConverter()
    converter.convert(filepath, outputpath)

