from json import dumps
import os
from urllib import urlopen

from bottle import route, run, request, template, response

from analysis import analyze_text, initialize_third_order_matrix, analyze_text_third_order_responsive, compute_most_probable_digraph


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
	
	response.set_header("Access-Control-Allow-Origin", "*")
	yield callback
	
	text = urlopen(text_link).read()
	char_analysis = analyze_text(text, 1, skip)
	
	yield "(" + dumps(char_analysis) + ")"
	return

@route('/so')
def so():
	"""Fetches text from provided link, analyzes text (second-order) and returns results as JSONP"""

	callback = request.query.callback
	text_link = request.query.txt
	skip = (request.query.skip == "True")
	
	print "/so with callback=" + callback + " text_link=" + text_link + " skip= " + str(skip)
	
	response.set_header("Access-Control-Allow-Origin", "*")
	yield callback
	
	text = urlopen(text_link).read()
	char_analysis = analyze_text(text, 2, skip)
	
	yield "(" + dumps(char_analysis) + ")"
	return

@route('/to')
def to():
	"""Fetches text from provided link, analyzes text (third-order) and returns results as JSONP"""

	callback = request.query.callback
	text_link = request.query.txt
	skip = (request.query.skip == "True")
	
	print "/to with callback=" + callback + " text_link=" + text_link + " skip= " + str(skip)
	
	response.set_header("Access-Control-Allow-Origin", "*")
	yield callback
	
	text = urlopen(text_link).read()
	
	"""
	Unlike first- and second-order analysis, third-order analysis
	raises serious computational complexity concerns and is likely to cause response
	timeouts on executing servers. In order to avoid timeouts, the analysis is
	split up into chunks of 500 words and an empty string yielded after each chunk, 
	in order to keep the connection alive.
	"""  
	char_analysis = initialize_third_order_matrix();
	
	chars_left = True
	lower_bound = 0
	upper_bound = min(500, len(text))
	while(chars_left):
		if(upper_bound >= len(text)): # text is shorter than 500 chars
			upper_bound = len(text)
			char_analysis = analyze_text_third_order_responsive(text[lower_bound:upper_bound], char_analysis)
			chars_left = False
		else: # text is longer than 500 chars
			if(lower_bound == 0): # first chunk, there are no last two characters of previous chunk
				char_analysis = analyze_text_third_order_responsive(text[lower_bound:upper_bound], char_analysis)
			else:
				char_analysis = analyze_text_third_order_responsive(text[(lower_bound - 2):upper_bound], char_analysis)
			yield " "
			print "Processed " + str(upper_bound) + "/" + str(len(text)) + " chars"
			lower_bound += 500
			upper_bound += 500
		
	
	yield "(" + dumps(char_analysis) + ")"
	return

@route('/digraph')
def digraph():
	"""Computes the most probable digraph starting with a given character and input text"""
	callback = request.query.callback
	text_link = request.query.txt
	start = request.query.start
	
	print "/pc with callback=" + callback + " text_link=" + text_link + " start=" + start
	
	response.set_header("Access-Control-Allow-Origin", "*")
	yield callback
	
	text = urlopen(text_link).read()
	char_analysis = analyze_text(text, 2, True)
	
	digraph = compute_most_probable_digraph(char_analysis, start)
	yield "( 'digraph': " + digraph + ")"
	return

run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
