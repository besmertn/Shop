import os

from flask import send_from_directory, render_template, current_app, redirect, url_for
from flask_login import login_required

from src.main import bp
from src import global_shopping


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    if not global_shopping:
        return render_template('index.html', title='Home')
    else:
        return redirect(url_for('shopping.index'))
