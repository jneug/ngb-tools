from flask import Blueprint

bp = Blueprint('mfcdeck.api', __name__, template_folder='templates')

@bp.route('/calendar')
def calendar():
	card = {
		'mfcdeck': True,
		'version': 2,
		'items': []
	}
	row = []
	for day in range(31):
		row.append(day)
		if day%7 == 6:
			card['items'].append({'items':row})
			row = []
	return card