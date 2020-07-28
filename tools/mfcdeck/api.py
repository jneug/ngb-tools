from datetime import date
import calendar

from flask import Blueprint

bp = Blueprint('mfcdeck.api', __name__, template_folder='templates')

@bp.route('/calendar')
def cal():
	bg_gradient = '#4a6d88,#001e38'
	fg_color = '#ffffff'
	month_color = '#59b3f2'
	wday_color = '#888892'
	today_color = '#fb00fc'
	wend_color = '#fec44c'
	first_day = 0
	timezone = 'Europe/Berlin'
	fs_small = 10
	fs_med = 13
	fs_large = 16
	
	spacing = .8
	
	calendar.setfirstweekday(first_day)
	today = date.today()
	cal = calendar.monthcalendar(today.year, today.month)
	wdays = [{'color': wday_color, 'fontWeight': 'medium', 'content':x} for x in calendar.weekheader(2).split(' ')]

	card = {
		'mfcdeck': True,
		'version': 2,
		'backgroundGradients': bg_gradient,
		'fontDesign': 'monospaced',
		'fontSize': fs_small,
		'color': fg_color,
		'items': [
			'spacer',
			{
				'items': [
					'spacer',
					{'visibility':'show-for-small-only','spacing':(fs_small*spacing)},
					{'visibility':'show-for-medium-only','fontSize':fs_med,'spacing':(fs_med*spacing)},
					{'visibility':'show-for-large-only','fontSize':fs_large,'spacing':(fs_large*spacing)},
					'spacer'
				]
			},
			'spacer'
		]
	}
	cal_items = [
		{'items': ['spacer', {'content':calendar.month_name[today.month],'color': month_color, 'fontWeight': 'bold'}, 'spacer']},
		{'items': wdays}
	]
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
		cal_items.append({'items':row})
	for i in range(3):
		card['items'][1]['items'][i+1]['items'] = cal_items
	return card
