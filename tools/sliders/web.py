from flask import Blueprint, request, current_app, g, render_template

from pathlib import Path


bp = Blueprint('sliders.web', __name__, template_folder='templates')

@bp.route('/')
def start():
		return render_template('sliders/index.html')
