from __future__ import unicode_literals

import logging
from logging.handlers import RotatingFileHandler
import os

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    render_template,
    request,
    redirect,
    url_for
)

import youtube_dl

def create_app():
    app = Flask(__name__)
    
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/xstreamly.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('xstreamly startup')

    return app


app = create_app()


@app.route("/", methods=["GET", "POST"])
def index():
    stream_url = None
    if request.method == "POST":
        result = {}
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(request.form['url'], download=False)
        
        return render_template('index.html', stream=result)
    return render_template('index.html')