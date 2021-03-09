from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from app import db
from app.models import Serie
from app.serie import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return "Hello, Serie!"
