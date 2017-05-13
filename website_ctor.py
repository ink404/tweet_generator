import os
import argparse
import glob


web1 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ink</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:800|Roboto" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Barrio" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script type="text/javascript" src="scripts.js"></script>
<br>
<div id="tweet_container">"""


web2 = """
<br>
<br>
</div>
</body>
</html>"""

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    return parser

def make_p(content):
    return("""<p id="tweets" class="para" href="" >"""+content+"""</p1><br>""")

def clean(word):
    word = word.strip().lower()
    cleaned = ''
    for char in word:
        if char.isalpha():
            cleaned+=char
    return cleaned

def word_count():
    word_map = {}
    read_files = glob.glob('./streams/*.txt')

    for f in read_files:
        f_cur  = open(f,'r')
        for line in f_cur:
            line = line.split()
            for word in line:
                word = clean(word)
                try:
                    word_map[word]+=1
                except KeyError:
                    word_map[word]=0
    freq_map = {}
    for key in word_map:
            freq_map[word_map[key]] = key
    for freq, word in freq_map.items():
        if freq > 50:
            if len(word) > 5:
                print(word)


#word_count()

parser = get_parser()
args = parser.parse_args()
query = args.query

os.system("python chaingen.py -q "+query)
with open("./out/output_"+query+".txt",'r') as f:
    web1+="""<br><p id="hashtag" class="para" href="" >#"""+query+""":</p1><br>"""
    for line in f:
        web1+=make_p(line)


website = web1+web2
with open('./website/index.html','w') as f2:
    f2.write(website)

os.system("open ./website/index.html")
