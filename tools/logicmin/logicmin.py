from flask import Blueprint, request, current_app, g, render_template

from pathlib import Path

from .generators import *

bp = Blueprint('logicmin.web', __name__, template_folder='templates')

@bp.route('/', methods=('GET','POST'))
def start():
	if request.method == 'POST':
		expr = request.form.get('expr', '')
		
		expr_min = expr

		return render_template('logicmin/output.html', expr=expr_min, original_expr=expr)
	else:
		return render_template('logicmin/input.html')
