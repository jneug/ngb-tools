from flask import Blueprint, request, current_app, g, render_template

from pathlib import Path

from .generators import *

bp = Blueprint('gettysetty', __name__, template_folder='templates')

@bp.route('/', methods=('GET','POST'))
def start():
	if request.method == 'POST':
		schema = request.form.get('schema', '')
		clazz  = request.form.get('class', 'Klasse')

		code = gen_class(clazz, parse_simple(schema))

		return render_template('gs_output.html', code=code, schema=schema)
	else:
		return render_template('gs_input.html')

@bp.route('/download')
def download_file():
	pass
