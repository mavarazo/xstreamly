import os

import tmdbsimple as tmdb
from app import db
from app.models import Serie
from app.serie import bp
from flask import (current_app, flash, g, jsonify, redirect, render_template,
                   request, url_for)

tmdb.API_KEY = os.environ.get('TMDB_API_KEY')


@bp.route('/', methods=['GET','POST'])
def index():
    return render_template('serie.index.html', series=Serie.query.order_by(Serie.id.desc()).all())


@bp.route('/search', methods=['GET','POST'])
def search():
    results = []
    if request.method == 'POST' and request.form['name']:
        search = tmdb.Search()
        search.tv(query=request.form['name'])
        results = search.results
    
    print(results)
    return render_template('serie.search.html', results=results)


@bp.route('/add', methods=['POST'])
def add():
    if request.form['tmdb_id'] and request.form['tmdb_name']:
        if Serie.query.filter_by(tmdb_id = request.form['tmdb_id']).first():
            return
        
        serie = Serie(tmdb_id=request.form['tmdb_id'], name=request.form['tmdb_name'], overview=request.form['tmdb_overview'], poster=request.form['tmdb_poster'])
        db.session.add(serie)
        db.session.commit()
        return redirect(url_for('serie.index'))
    return redirect(url_for('serie.search'))
    
@bp.route('/<int:serie_id>', methods=['GET'])
def show(serie_id):
    print(serie_id)
    return redirect(url_for('serie.index'))

