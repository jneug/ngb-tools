from flask import Blueprint, request, current_app, g, render_template, url_for

bp = Blueprint('mfcdeck.web', __name__, template_folder='templates')

@bp.route('/')
def start():
	opts = {
		'calendar': [
			('week_start', 'First day of the week gor the calendar display. 0=Monday,...,6=Sunday', 'int', 0),
			('locale', 'Locale for date formating and names. (Not supported yet.)', 'str', 'de_DE'),
			('background','Background gradient for the cards. Set to a comma separated list of hex colors.', 'str', 'background'),
			('color', 'Text color as hex color.', 'str', '#ffffff'),
			('today_color', 'Color highlight for the current day as hex color.', '#fb00fc'),
			('wend_color', 'Color highlight for weekends as hex color.', '#fec44c'),
			('month_color', 'Color for the month name as hex color.', '#59b3f2'),
			('wday_color', 'Color for the weekday names as hex color.', '#888892'),
			('fs_small', 'Fontsize for small cards', 'int', 10),
			('fs_medium', 'Fontsize for medium cards', 'int', 13),
			('fs_large', 'Fontsize for large cards', 'int', 16),
			('margin', 'Margin for the cards', 'int', 8)
		]
	}

	return render_template('mfcdeck/options.html', commands=opts)
