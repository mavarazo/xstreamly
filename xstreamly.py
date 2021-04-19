from flask.cli import FlaskGroup

from app import app, db
from app.models import Serie, Episode


cli = FlaskGroup(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Serie': Serie, Episode: Episode}


if __name__ == '__main__':
    cli()