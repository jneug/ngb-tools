from flask import Blueprint, request, current_app, g, render_template

from pyeda.inter import *

bp = Blueprint('logicmin.web', __name__, template_folder='templates')

@bp.route('/', methods=('GET','POST'))
def start():
	if request.method == 'POST':
		expression = request.form.get('expr', '')

		expr_orig = expr(expression)
		expr_min = espresso_exprs(expr_orig)

		return render_template('logicmin/output.html', expr=expr_min, original_expr=expr_orig)
	else:
		return render_template('logicmin/input.html')
