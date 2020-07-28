from datetime import date
import calendar

from flask import Blueprint

bp = Blueprint('mfcdeck.api', __name__, template_folder='templates')

@bp.route('/calendar')
def cal():
	bg_gradient = '#4a6d88,#001e38'
	fg_color = '#ffffff'
	today_color = '#fb00fc'
	wend_color = '#fec44c'
	first_day = 0
	timezone = 'Europe/Berlin'
	month = 0
	
	calendar.setfirstweekday(first_day)
	today = date.today()
	cal = calendar.monthcalendar(today.year, today.month)

	card = {
		'mfcdeck': True,
		'version': 2,
		'backgroundGradients': bg_gradient,
		'fontDesign': 'monospaced',
		'fontSize':10,
		'color': fg_color,
		'items': [
			{'content':'spacer', 'visibility': 'show-for-small'}
		]
	}
	for week in cal:
		row = []
		for wday,day in enumerate(week):
			dstr = f'{day:02}'
			if day == 0:
				row.append('  ')
			elif day == today.day:
				row.append({'content':dstr,'color':today_color})
			elif wday == 5 or wday == 6:
				row.append({'content':dstr,'color':wend_color})
			else:
				row.append(dstr)
		card['items'].append({'items':row})
	card['items'].append('spacer')
	return card
