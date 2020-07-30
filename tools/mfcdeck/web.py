from flask import Blueprint, request, current_app, g, render_template, url_for

bp = Blueprint('mfcdeck.web', __name__, template_folder='templates')

@bp.route('/')
def start():
	opts = {
		'calendar': [
			('week_start', 'First day of the week gor the calendar display. 0=Monday,...,6=Sunday', 'int', 0),
			('locale', 'Locale for date formating and names. (Not supported yet.)', 'str', 'de_DE'),
			('background','Background gradient for the cards. Set to a comma separated list of hex colors.', 'str', '#4a6d88,#001e38'),
			('color', 'Text color as hex color.', 'str', '#ffffff'),
			('today_color', 'Color highlight for the current day as hex color.', 'str', '#fb00fc'),
			('wend_color', 'Color highlight for weekends as hex color.', 'str', '#fec44c'),
			('month_color', 'Color for the month name as hex color.', 'str', '#59b3f2'),
			('wday_color', 'Color for the weekday names as hex color.', 'str', '#888892'),
			('fs_small', 'Fontsize for small cards', 'int', 10),
			('fs_medium', 'Fontsize for medium cards', 'int', 12),
			('fs_large', 'Fontsize for large cards', 'int', 16),
			('margin', 'Margin for the cards', 'int', 8)
		]
	}

	return render_template('mfcdeck/options.html', commands=opts)
