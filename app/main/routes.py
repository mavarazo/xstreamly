from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from app import db
from app.models import Serie, YoutubeDl
from app.main import bp

import youtube_dl


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    stream_url = request.form['url'] if request.method == 'POST' else request.args.get('url')

    if stream_url:
        result = {}
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(stream_url, download=False)
            save_history(result['title'], result['webpage_url'])
        
        return render_template('index.html', stream=result, history=load_history())
    return render_template('index.html', history=load_history())


def load_history():
    return YoutubeDl.query.order_by(YoutubeDl.id.desc()).all()


def save_history(name, webpage_url):
    if not name or not webpage_url:
        return

    if YoutubeDl.query.filter_by(webpage_url = webpage_url).first():
        return
    
    history = YoutubeDl(name = name, webpage_url = webpage_url)
    db.session.add(history)
    db.session.commit()
