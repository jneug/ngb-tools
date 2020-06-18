import requests
from flask import Blueprint, request, current_app, g, render_template
from random import choices,shuffle

from pathlib import Path

bp = Blueprint('diceware', __name__, template_folder='templates')

@bp.route('/new')
def new():
	word_count = request.args.get('words', default=4, type=int)
	sep = request.args.get('separator', default=' ', type=str)[0:1]
	num_count = request.args.get('numbers', default=0, type=int)

	with current_app.open_instance_resource('words.txt', 'r') as f:
		words = f.read().split('\n')
		passwords = choices(words, k=word_count)
	passwords = passwords + choices(range(100), k=num_count)
	shuffle(passwords)
	return sep.join(str(x) for x in passwords).lower()

@bp.route('/words/generate')
def start():
	url = 'http://api.corpora.uni-leipzig.de/ws/words/deu_news_2012_1M/randomword/?limit=7776'
	resp = requests.get(url, headers={'accept': 'application/json'})
	if resp.status_code == 200:
		with current_app.open_instance_resource('words.txt', 'w') as f:
			for data in resp.json():
				word = data['word']

				f.write(word.lower())
				f.write('\n')
	return ({}, 200)
