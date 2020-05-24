from flask import Blueprint, request, current_app, g, render_template

from pathlib import Path

from .generators import *

bp = Blueprint('gruwigen', __name__, template_folder='templates')

@bp.route('/', methods=('GET','POST'))
def start():
	return __name__
