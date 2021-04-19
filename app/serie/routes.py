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

    
@bp.route('/<int:serie_id>', methods=['GET'])
def show(serie_id):
    serie = Serie.query.filter_by(id=serie_id).first()
    return render_template('serie.html', serie=serie)

