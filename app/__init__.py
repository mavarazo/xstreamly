from __future__ import unicode_literals

import logging
from logging.handlers import RotatingFileHandler
import os
import sqlite3

from werkzeug.utils import secure_filename
from flask import (
    g,
    Flask,
    jsonify,
    send_from_directory,
    render_template,
    request,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import youtube_dl

from config import Config

HISTORY_TABLE = '''
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY,
    title TEXT,
    webpage_url TEXT UNIQUE)
'''


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.serie import bp as serie_bp
    app.register_blueprint(serie_bp)

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

from app import models
        