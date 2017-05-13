#https://github.com/jsvine/markovify
import markovify
import argparse

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    return parser

def clean(model):
    cleaned = ''
    if model:
        for char in model:
            if char != ' ':
                char = char.lower().strip()
            elif char == '.':
                char = ' '
            cleaned+=char
        cleaned = cleaned[0].upper()+cleaned[1:]
        if cleaned.find(' i ') != -1:
            cleaned = cleaned.replace(' i ', ' I ')
    return cleaned

parser = get_parser()
args = parser.parse_args()
query = args.query

with open("streams/formatted_"+query+"_stream_.txt") as f:
    text = f.read()

text_model = markovify.Text(text)

with open('./out/output_'+query+'.txt','w') as f:
    for i in range(17):
        model = text_model.make_short_sentence(400,state_size=1)
        if model:
            f.write(model+'\n')
