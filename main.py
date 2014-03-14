from bottle import route, run, get, request, template
from json import dumps
from urllib import urlopen
from analysis import analyze_text

@route('/')
def index():
	return template('index.tpl')

@get('/fo')
def fo():
	callback = request.query.callback
	# text_link = 'https://wiki.eecs.yorku.ca/course_archive/2013-14/W/6339/_media/assignments:christmas_carol.txt' - works
	text_link = request.query.txt
	skip = request.query.skip
	text = urlopen(text_link)
	char_analysis = analyze_text(text, 1, skip)
	return callback + "(" + dumps(char_analysis) + ")"

run(host='localhost', port=8080)