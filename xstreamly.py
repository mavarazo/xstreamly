from flask.cli import FlaskGroup

from app import app, db
from app.models import Serie, TheMovieDb, TheTvDb


cli = FlaskGroup(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Serie': Serie, 'TheMovieDb': TheMovieDb, 'TheTvDb': TheTvDb}


if __name__ == '__main__':
    cli()