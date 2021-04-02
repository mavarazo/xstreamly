from datetime import datetime
import os
import re
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from app import db
from app.models import Serie, Episode
from app.main import bp

import youtube_dl
import tmdbsimple as tmdb

tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

regex = r"^((?P<seriename>.+?)[ \._\-])?[Ss](?P<season_nr>[0-9]+)[\.\- ]?[Ee](?P<episode_nr>[0-9]+)[^\/]*$"

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    stream_url = request.form['url'] if request.method == 'POST' else request.args.get('url')

    if stream_url:
        result = {}
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(stream_url, download=False)
            episode = save_episode(result['title'], result['webpage_url'])
        
        return render_template('main.index.html', episode=episode, history=load_history())
    return render_template('main.index.html', history=load_history())


@bp.route('/<int:episode_id>')
def play(episode_id):
    episode = Episode.query.filter_by(id=episode_id).first()
    if not episode:
        return redirect(url_for('main.index'))
    
    with youtube_dl.YoutubeDL({}) as ydl:
        result = ydl.extract_info(episode.origin_url, download=False)
        return redirect(result['url'])


def save_episode(origin_name, origin_url):
    if not origin_name or not origin_url:
        return
    
    episode = Episode.query.filter_by(origin_url=origin_url).first()
    if episode:
        return episode

    serie = None
    matches = re.search(regex, origin_name)
    if matches and matches.group('seriename'):
        serie = save_serie(matches.group('seriename').replace('.', ' '))

    season_nr = matches.group('season_nr') if matches else None
    episode_nr = matches.group('episode_nr') if matches else None
    episode = Episode(serie=serie, season_nr=season_nr, episode_nr=episode_nr, origin_name=origin_name, origin_url=origin_url)
    db.session.add(episode)
    db.session.commit()
    return episode


def save_serie(name):
    if not name:
        return
    
    serie = Serie.query.filter_by(name=name).first()
    if serie:
        return serie
    
    response = fetch_series_from_api_by_name(name)
    if response:
        tmdb_id = response['id']
        overview = response['overview']
        poster = response['poster_path']

    serie = Serie(name=name, tmdb_id=tmdb_id, overview=overview or '', poster=poster or '')
    db.session.add(serie)
    db.session.commit()
    return serie

def fetch_series_from_api_by_name(name):
    search = tmdb.Search()
    search.tv(query=name)
    if search and len(search.results) == 1:
        return search.results[0]
    return None


def load_history():
    return Episode.query.order_by(Episode.id.desc()).all()

