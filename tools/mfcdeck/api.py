from flask import Blueprint

bp = Blueprint('mfcdeck.api', __name__, template_folder='templates')

@bp.route('/calendar')
def calendar():
	card = {
		'mfcdeck': True,
		'version': 2,
		'backgroundGradients': '#4a6d88,#001e38',
		'items': []
	}
	row = []
	for day in range(31):
		row.append(str(day+1))
		if day%7 == 6:
			card['items'].append({'items':row})
			row = []
	for s in range(7-len(row)):
		row.append(" ")
	card['items'].append({'font':'Courier','fontSize':12,'items':row})
	return card