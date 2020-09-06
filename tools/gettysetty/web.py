from flask import Blueprint, request, current_app, g, render_template

from pathlib import Path

from .generators import *

bp = Blueprint('gettysetty.web', __name__, template_folder='templates')

@bp.route('/', methods=('GET','POST'))
def start():
	if request.method == 'POST':
		schema = request.form.get('schema', '')
		clazz  = request.form.get('class', '')
		if len(clazz) == 0:
			clazz = 'Klasse'

		classname, attris, methods = parse_umlet(schema)
		if not classname:
			classname = clazz

		#code = gen_class(clazz, parse_simple(schema))
		code = gen_class(classname, attris, methods)

		return render_template('gettysetty/output.html', code=code, schema=schema)
	else:
		return render_template('gettysetty/input.html')

@bp.route('/download')
def download_file():
	pass
