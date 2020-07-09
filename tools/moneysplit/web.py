from flask import Blueprint, request, current_app, g, render_template

from pathlib import Path

from pprint import pprint

from .transaction import *


bp = Blueprint('moneysplit.web', __name__, template_folder='templates')

@bp.route('/', methods=('GET','POST'))
def start():
	if request.method == 'POST':
		schema = request.form.get('schema', '').split('\n')
		users = request.form.get('users', '').split('\n')

		balances = []
		for id,name in enumerate(users):
			balances.append(
				balance(int(id), name)
			)

		transactions = []
		for t in schema:
			type,params = t.split('|')
			p = params.split(',')

			if type == 'i':
				transactions.append(
					income(int(p[0]), float(p[1]))
				)
			elif type == 'e':
				transactions.append(
					expense(int(p[0]), float(p[1]))
				)
			elif type == 't':
				transactions.append(
					transaction(int(p[0]), int(p[1]), float(p[2]))
				)

		balances = apply_transactions(balances, transactions)
		balances = calc_debts(balances)
		model = generate_model(balances)
		final_balances = apply_transactions(balances, model)

		result = []
		for t in model:
			_f = users[t['from']]['name']
			_t = users[t['to']]['name']
			_a = t['amount']
			result.append(
				f'💸 {_f} pays {_t} {_a} €'
			)

		result.append(f'Ding Ding ... everyone is even at {target} €')
		result.append(f'  (The model fit is {calc_fit(model)} with a max of {max_fitness})')

		return render_template('moneysplit/output.html', result='\n'.join(result), schema=schema, users=users)
	else:
		return render_template('moneysplit/input.html')
