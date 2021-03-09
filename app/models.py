from flask import current_app
from app import db


class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)


class TheMovieDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'), nullable=False)


class TheTvDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tvdb_id = db.Column(db.Integer, primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'), nullable=False)


class YoutubeDl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'))
    name = db.Column(db.String(255))
    webpage_url= db.Column(db.Text)
