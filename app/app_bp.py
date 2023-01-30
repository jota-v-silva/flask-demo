from flask import (
    Blueprint, request, Response, current_app, url_for, render_template
)

bp = Blueprint('app', __name__, url_prefix='/app')

# a simple page that says hello
@bp.route('/')
def landing_page():
    return render_template('base.html')