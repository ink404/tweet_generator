welcome

REQUIRED:
for the stream collect to work you must enter your:
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
to do this you have to register an app with twitter which is quick and free
this: https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
explains well how do do that under the 'Register your app with Twitter heading'

to use, collect the data you want using the stream collect script with specified
arguements -q (query/tag) -d (directory),

example:
"python main.py -q hashtag -d streams"

notes: 
- IMPORTANT: make sure you’re in the same directory as the python files by using cd(change directory) ex: cd ~/Document/folder_where_code_is/twitter_emulator_v2
- directory must be created before saving output
- when tracking specific
tags the tag must be popular enough to generate sufficient data within a reasonable
amount of time
- to stop collecting hit ctrl-c

to generate tweets
use the website_ctor.py file with specified query

example: "python website_ctor.py -q replace_this_with_tag”

note: this will open up a page in your web browser with the generated content
the queries are case sensitive, so it must be spelled how it is in the produced file, it also, logically, won’t produce any output if you have no data collected
