from flask import Flask  
from flask import render_template
from flask import request
from flask import Markup
import os
import sys
import pafy
video_link = ''
video_dir = "./static/video"
download = ''
file_size = ''
# creates a Flask application, named app

app = Flask(__name__)


# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():
	return render_template('index.html')

@app.route('/', methods=['POST'])

def getValue():
	global video_link, download
	if request.method == "POST":
		video_link = request.values.get("downloadLink")
		if len(video_link) != 0:
			video = pafy.new(video_link)
			runtime = video.duration
			a = video.getbest()
			file_size = a.get_filesize()
			file_size = str(round(int(file_size)/(1024*1024),2)) + ' MB'
			filename = a.download(filepath=video_dir)
			thumbnail = """
					<video controls controlsList="nodownload" id="player" style = "max-width : 450px;margin-top: 15px">
	   				<source src="."""+ filename + """ " type="video/mp4">	
					</video>
				"""
			thumbnail = Markup(thumbnail)
			button = '<a href="'+filename+'" download><button class="downloadButton fa fa-download">Download!</button>	</a>'
			button = Markup(button)

			return render_template('index.html',runtime= runtime, filesize=file_size ,button = button, title=video.title, thumbnail=thumbnail)
if __name__ == "__main__":  
    app.run(host=0.0.0.0, debug=True)
