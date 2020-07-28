from datetime import date
import calendar

from flask import Blueprint, request

bp = Blueprint('mfcdeck.api', __name__, template_folder='templates')

@bp.route('/calendar')
def cal():
	bg_gradient = '#4a6d88,#001e38'
	fg_color = request.args.get('color', default='#ffffff', type=str)
	month_color = request.args.get('month_color', default='#59b3f2', type=str)
	wday_color = request.args.get('wday_color', default='#888892', type=str)
	today_color = request.args.get('today_color', default='#fb00fc', type=str)
	wend_color = request.args.get('wend_color', default='#fec44c', type=str)
	
	first_day = request.args.get('week_start', default=0, type=int)
	fs_small = request.args.get('fs_small', default=10, type=int)
	fs_med = request.args.get('fs_medium', default=13, type=int)
	fs_large = request.args.get('fs_large', default=16, type=int)
	
	timezone = request.args.get('timezone', default='Europe/Berlin', type=str)
	locale = request.args.get('locale', default='de_DE', type=str)
	
	spacing = .8
	
	calendar.setfirstweekday(first_day)
	today = date.today()
	cal = calendar.monthcalendar(today.year, today.month)
	wdays = [{'color': wday_color, 'fontWeight': 'medium', 'content':x} for x in calendar.weekheader(2).split(' ')]
	
	weekends = [(5-first_day)%7,(6-first_day)%7]

	card = {
		'mfcdeck': True,
		'version': 2,
		'backgroundGradients': bg_gradient,
		'fontDesign': 'monospaced',
		'fontSize': fs_small,
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
				row.append({'content':dstr,'color': fg_color})
		cal_items.append({'items':row})
	for i in range(3):
		card['items'][1]['items'][i+1]['items'] = cal_items
	return card
