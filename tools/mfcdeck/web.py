from flask import Blueprint, request, current_app, g, render_template, url_for

bp = Blueprint('mfcdeck.web', __name__, template_folder='templates')

@bp.route('/')
def start():
	opts = {
		'calendar': [
			('fs_small', 'Fontsize for small cards', 'int', 10),
			('fs_medium', 'Fontsize for medium cards', 'int', 13),
			('fs_large', 'Fontsize for large cards', 'int', 16),
		]
	}

	return render_template('mfcdeck/options.html', commands=opts)
