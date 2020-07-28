from datetime import date
from calendar import monthrange

from flask import Blueprint

bp = Blueprint('mfcdeck.api', __name__, template_folder='templates')

@bp.route('/calendar')
def calendar():
	bg_gradient = '#4a6d88,#001e38'
	fg_color = '#ffffff'
	today_color = '#fb00fc'
	first_day = 0
	timezone = 'Europe/Berlin'
	month = 0
	
	today = date.today()
	first = date(today.year, today.month, 1)
	first_wday, days_in_month = monthrange(today.year, today.month)
	day_range = first_wday+1+days_in_month

	card = {
		'mfcdeck': True,
		'version': 2,
		'backgroundGradients': bg_gradient,
		'fontDesign': 'monospaced',
		'fontSize':10,
		'color': fg_color,
		'items': []
	}
	row = []
	for cell in range(first_wday):
		row.append(' ')
	for day in range(days_in_month):
		dstr = f'{day+1:02}'
		if day+1 == today.day:
			row.append({'content':dstr,'color':today_color})
		else:
			row.append(dstr)
		if day%7 == 6:
			card['items'].append({'items':row})
			row = []
	for cell in range(7-len(row)):
		row.append(" ")
	card['items'].append({'items':row})
	return card
