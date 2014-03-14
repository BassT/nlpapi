from bottle import route, run, get, request, template
from json import dumps
from urllib import urlopen
from analysis import analyze_text

@route('/')
def index():
	return template('index.tpl')

@route('/fo')
def fo():
	"""Fetches text from provided link, analyzes text (first-order) and returns results as JSONP"""
	
	callback = request.query.callback
	text_link = request.query.txt
	skip = (request.query.skip == "True")
	
	print "/fo with callback=" + callback + " text_link=" + text_link + " skip= " + str(skip)
	
	text = urlopen(text_link).read()
	
	char_analysis = analyze_text(text, 1, skip)
	return callback + "( " + dumps(char_analysis, indent=2) + " )"

@route('/so')
def so():
	"""Fetches text from provided link, analyzes text (second-order) and returns results as JSONP"""

	callback = request.query.callback
	text_link = request.query.txt
	skip = (request.query.skip == "True")
	
	print "/so with callback=" + callback + " text_link=" + text_link + " skip= " + str(skip)
	
	text = urlopen(text_link).read()
	
	char_analysis = analyze_text(text, 2, skip)
	return callback + "(" + dumps(char_analysis) + ")"

@route('/to')
def to():
	"""Fetches text from provided link, analyzes text (third-order) and returns results as JSONP"""

	callback = request.query.callback
	text_link = request.query.txt
	skip = (request.query.skip == "True")
	
	print "/to with callback=" + callback + " text_link=" + text_link + " skip= " + str(skip)
	
	text = urlopen(text_link).read()
	
	char_analysis = analyze_text(text, 3, skip)
	return callback + "(" + dumps(char_analysis) + ")"

run(host='localhost', port=8080)