import time

import argparse

import streamcollect
import os

# https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory")
    return parser



parser = get_parser()
args = parser.parse_args()
directory = args.data_dir
query = args.query

timer = 1
print("data dir: "+directory)
print("query: "+query)
timeout = time.time() + 60*60*timer   #1hr
try:
    while True:
        streamcollect.load_stream(directory, query)
        if time.time() > timeout:
            timer+=1
            break
except:
    os.system("python main.py -q "+query+" -d streams")

# with open("%s/formatted_stream_%s.txt" % (directory, query)) as f:
#     text = f.read()
