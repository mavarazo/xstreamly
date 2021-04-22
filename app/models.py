from flask import current_app
from app import db


class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    tmdb_id = db.Column(db.Integer)
    overview = db.Column(db.Text)
    backdrop = db.Column(db.String(255))
    poster = db.Column(db.String(255))
    episodes = db.relationship("Episode", back_populates="serie", order_by="Episode.season_nr, Episode.episode_nr")


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'))
    serie = db.relationship("Serie", back_populates="episodes")
    name = db.Column(db.String(255))
    season_nr = db.Column(db.Integer)
    episode_nr = db.Column(db.Integer)
    origin_name = db.Column(db.String(255))
    origin_url = db.Column(db.Text)
    tmdb_id = db.Column(db.Integer)
    overview = db.Column(db.Text)

