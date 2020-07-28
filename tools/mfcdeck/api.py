from flask import Blueprint, request, current_app, g, render_template, url_for

import requests

bp = Blueprint('mfcdeck.api', __name__, template_folder='templates')

@bp.route('/calendar')
def start():
	card = {
		'mfcdeck': True,
		'version': 2,
		'items': []
	}
	row = []
	for day in range(31):
		row.append(day)
		if day%7 == 6:
			card['items'].append(row)
			row = []
	return card