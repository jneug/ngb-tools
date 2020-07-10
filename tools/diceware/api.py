import requests
from flask import Blueprint, request, current_app, g, render_template
from random import choices,shuffle

from pathlib import Path

import re

bp = Blueprint('diceware.api', __name__, template_folder='templates')

@bp.route('/new')
def new():
	count = request.args.get('count', default=1, type=int)
	word_count = request.args.get('words', default=4, type=int)
	sep = request.args.get('separator', default=' ', type=str)[0:1]
	num_count = request.args.get('numbers', default=0, type=int)
	cap_count = request.args.get('capitals', default=0, type=int)

	result = []
	numbers = range(10000)
	with current_app.open_instance_resource('words.txt', 'r') as f:
		words = f.read().split('\n')
	for i in range(count):
		passwords = choices(words, k=word_count)
		passwords = passwords + choices(numbers, k=num_count)
		for i in range(min(len(passwords),cap_count)):
			passwords[i] = passwords[i].capitalize()
		shuffle(passwords)
		result.append(sep.join(str(x) for x in passwords).lower())
	return '\n'.join(result)

@bp.route('/words/generate')
def words():
	url = 'http://api.corpora.uni-leipzig.de/ws/words/deu_news_2012_1M/randomword/?limit=8000'
	resp = requests.get(url, headers={'accept': 'application/json'})
	if resp.status_code == 200:
		n = 7776
		with current_app.open_instance_resource('words.txt', 'w') as f:
			for data in resp.json():
				word = data['word']

				if n > 0 and re.fullmatch(r'[a-z]{4,8}', word, re.I):
					f.write(word.lower())
					f.write('\n')
					n -= 1
	return ({}, 200)
