# -*- coding: utf-8 -*-

import re

from pathlib import Path
from random import randint, choice
from statistics import mean


from flask import Blueprint, request, current_app, g, render_template, url_for
from gdshortener import ISGDShortener


#colors = ['#993366','#CC6699','#FF99CC','#FF0099','#990066','#CC3399','#FF66CC','#CC0099','#FF33CC','#FF00CC','#FF00FF','#CC00CC','#FF33FF','#990099','#CC33CC','#FF66FF','#660066','#993399','#CC66CC','#FF99FF','#330033','#663366','#996699','#CC99CC','#FFCCFF','#CC00FF','#9900CC','#CC33FF','#660099','#9933CC','#CC66FF','#9900FF','#330066','#663399','#9966CC','#CC99FF','#6600CC','#9933FF','#6600FF','#330099','#6633CC','#9966FF','#3300CC','#6633FF','#3300FF','#0000FF','#0000CC','#000099','#000066','#000033','#3333FF','#3333CC','#333399','#333366','#6666FF','#6666CC','#666699','#9999FF','#9999CC','#CCCCFF','#0033FF','#0033CC','#3366FF','#003399','#3366CC','#6699FF','#0066FF','#0066CC','#3399FF','#003366','#336699','#6699CC','#99CCFF','#0099FF','#006699','#3399CC','#66CCFF','#0099CC','#33CCFF','#00CCFF','#00FFFF','#00CCCC','#009999','#006666','#003333','#33FFFF','#33CCCC','#339999','#336666','#66FFFF','#66CCCC','#669999','#99FFFF','#99CCCC','#CCFFFF','#00FFCC','#00CC99','#33FFCC','#009966','#33CC99','#66FFCC','#00FF99','#006633','#339966','#66CC99','#99FFCC','#00CC66','#33FF99','#00FF66','#009933','#33CC66','#66FF99','#00CC33','#33FF66','#00FF33','#00FF00','#00CC00','#009900','#006600','#003300','#33FF33','#33CC33','#339933','#336633','#66FF66','#66CC66','#669966','#99FF99','#99CC99','#CCFFCC','#33FF00','#33CC00','#66FF33','#339900','#66CC33','#99FF66','#66FF00','#66CC00','#99FF33','#336600','#669933','#99CC66','#CCFF99','#99FF00','#669900','#99CC33','#CCFF66','#99CC00','#CCFF33','#CCFF00','#FFFF00','#CCCC00','#999900','#666600','#333300','#FFFF33','#CCCC33','#999933','#666633','#FFFF66','#CCCC66','#999966','#FFFF99','#CCCC99','#FFFFCC','#FFCC00','#CC9900','#FFCC33','#996600','#CC9933','#FFCC66','#FF9900','#663300','#996633','#CC9966','#FFCC99','#CC6600','#FF9933','#FF6600','#993300','#CC6633','#FF9966','#CC3300','#FF6633','#FF3300','#FF0000','#CC0000','#990000','#660000','#330000','#FF3333','#CC3333','#993333','#663333','#FF6666','#CC6666','#996666','#FF9999','#CC9999','#FFCCCC','#FF0033','#CC0033','#FF3366','#990033','#CC3366','#FF6699','#FF0066','#CC0066','#FF3399','#660033']
colors = ['#993366', '#ee4035', '#f37736', '#7bc043', '#0392cf', '#fe4a49', '#2ab7ca', '#fed766', '#005b96', '#6497b1', '#851e3e', '#0e9aa7', '#f6cd61', '#fe8a71', '#63ace5', '#fe9c8f', '#009688', '#65c3ba', '#ee4035', '#f37736', '#7bc043', '#0392cf', '#ff3377']
#parts = range(0, 255, 33)

def rand_color():
	#return "#%06x" % randint(0, 0xFFFFFF)
	return choice(colors)
	#return "#{r:02x}{g:02x}{b:02x}".format(r=choice(parts), g=choice(parts), b=choice(parts))

default_definition = """
# Ich mag Regler
Stimme zu|Stimme nicht zu"""


bp = Blueprint('sliders.web', __name__, template_folder='templates')


@bp.route('/', methods=('GET','POST'))
def start():
	sliders = list()
	definition = request.values.get('sliders', default_definition)
	values = request.values.get('values')

	clr = 0
	slider_index_map = []
	for line in definition.split('\n'):
		parts = line.split('|', 4)
		if len(parts) >= 2:
			if len(parts) < 3:
				parts.append(50)
			else:
				parts[2] = int(parts[2])

			if len(parts) < 4:
				parts.append(colors[clr%len(colors)])
				clr += 1
			slider_index_map.append(len(sliders))
			sliders.append(dict(
				type='slider',
				left=parts[0],
				right=parts[1],
				value=parts[2],
				color=parts[3]
				))
		elif line.startswith('#'):
			sliders.append(dict(
				type='header',
				text=line[1:].lstrip()
				))


	pattern = r"(.+:)?([0-9,]+)"

	avg = [[] for x in range(len(slider_index_map))]
	if values:
		for line in values.split('\n'):
			m = re.match(pattern, line)
			if m:
				for i, num in enumerate(m.group(2).strip().split(',')):
					if i < len(avg):
						avg[i].append(int(num))

		for i,l in enumerate(avg):
			if l:
				sliders[slider_index_map[i]]['value'] = mean(l)
			else:
				sliders[slider_index_map[i]]['value'] = 0

	sdef = request.values.get('edit', 'true').lower()
	sdef = sdef=='0' or sdef==0 or sdef=='false' or sdef=='off' or sdef=='no'
	sdef = not sdef

	step = request.values.get('step', 1, type=int)

	shorturl = url_for('sliders.web.start', sliders=definition, step=step, edit=0, _external=True)
	if request.method == 'POST' and current_app.env == 'production':
		isgd = ISGDShortener()
		shorturl = isgd.shorten(shorturl)
	elif definition == default_definition:
		shorturl = url_for('sliders.web.start')


	return render_template('sliders/index.html', sliders=sliders, definition=definition, show_definition=sdef, step=step, values=values if values else '', shorturl=shorturl)
