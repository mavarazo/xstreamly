from flask import Blueprint

bp = Blueprint('serie', __name__, url_prefix='/serie')

from app.serie import routes