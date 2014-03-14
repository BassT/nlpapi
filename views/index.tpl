<h1>NLP API</h1>
<p>Hello, this is an API for NLP, which was developed by Sebastian Richter in context of the 
'Computational Linguistics' given by <a href="http://http://www.cse.yorku.ca/~nick">Nick Cercone</a>.</p>
<p>These are your options:
<ul>
	<li><b>First-order correlation matrix:</b> <a href="/fo?callback=testCallback&txt=testText&skip=True">/fo?callback=testCallback&txt=testText&skip=True</a><br/>
		<ul>
			<li><pre>callback:</pre>
				This is the name of your JSONP callback.
			</li>
			<li><pre>txt:</pre>
				This is a link in the form <i>http://.../name.txt</i> to the txt file you want to analyze.
			</li>
			<li><pre>skip:</pre>
				This can be set to <i>true</i> or <i>false</i>.<br/>
				When true, characters of our alphabet, which don't occur in the text are omitted.<br/>
				This is faster and the default.
			</li>
		</ul>
	</li>
</ul>