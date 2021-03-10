from flask import current_app
from app import db


class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer)
    name = db.Column(db.String(64), index=True, unique=True)
    overview = db.Column(db.Text)
    poster = db.Column(db.String(255))


class YoutubeDl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'))
    name = db.Column(db.String(255))
    webpage_url= db.Column(db.Text)
