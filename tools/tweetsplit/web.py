import textwrap
from flask import Blueprint, render_template

def tweetsplit(tweet, length=280, mode='word'):
	return textwrap.fill(tweet)
	tweets = []
	words = tweet.split(' ')
	tweet = ''
	for w in words:
		if len(tweet)+len(w)+11 > 280:
			tweets.append(tweet)
			tweet = w
		else:
			tweet += f' {w}'
	return tweets

bp = Blueprint('tweetsplit.web', __name__, template_folder='templates')

@bp.route('/')
def start():
	return __name__

t='''
The Cabal, operating with its knowledge of the extreme long view through the power of the Acuity, sought to bring about Horus' victory by convincing Alpharius Omegon of the truth of their predictions. They asked the twin Primarchs to place themselves and the forces of the XX Legion under the banner of Horus and Chaos Undivided, despite their sworn loyalty to the Emperor, and do all they could to ensure the Warmaster's victory over the Emperor, thus sacrificing humanity to destroy the Chaos Gods once and for all.

The Primarch of the Alpha Legion appears to have acceded to this request, believing that such a sacrifice is what the Emperor would have Himself wanted if He had been presented with a similar choice. As the Heresy ended with the victory of the Emperor's Loyalist forces and the second outcome foreseen by the Acuity, it appears that the Cabal's machinations failed and that, if they are to be believed, the galaxy is ultimately doomed to be consumed by Chaos not long after the end of the 41st Millennium.
'''
tweets = tweetsplit(t)
for i,t in enumerate(tweets):
	t = t.strip()
	print(f'({i+1}/{len(tweets)}) {t}')
	print('='*12)
