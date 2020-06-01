
from copy import deepcopy as copy

EXPENSE			= 0
TRANSACTION = 1
INCOME 			= 2

def balance(id, name, initial=0.0):
	return {'id': id, 'name': name, 'balance': initial}

def expense(fro, amount):
	return {'type':EXPENSE, 'from': fro, 'amount': amount}

def income(to, amount):
	return {'type':INCOME, 'to': to, 'amount': amount}

def transaction(fro, to, amount):
	return {'type':TRANSACTION, 'from': fro, 'to': to, 'amount': amount}

def apply_transactions(balances, transactions):
	new_balances = copy(balances)
	for t in transactions:
		if t['type'] == EXPENSE:
			new_balances[t['from']]['balance'] -= t['amount']
		elif t['type'] == INCOME:
			new_balances[t['to']]['balance'] += t['amount']
		elif t['type'] == TRANSACTION:
			new_balances[t['from']]['balance'] -= t['amount']
			new_balances[t['to']]['balance'] += t['amount']
	for i in range(len(new_balances)):
		new_balances[i]['balance'] = round(new_balances[i]['balance'], 2)
	return new_balances

def calc_target_balance(balances):
	return round(sum([b['balance'] for b in balances]) / len(balances), 2)

def calc_debts(balances, target_amount=None):
	if not target_amount:
		target_amount = calc_target_balance(balances)

	new_balances = copy(balances)
	for b in range(len(new_balances)):
		new_balances[b]['debts'] = round(new_balances[b]['balance'] - target_amount, 2)
	return new_balances

def calc_fit(transactions):
	return 1/len(transactions)

def calc_max_fit(balances):
	pos_fitness = 1/len(list(filter(lambda b: b['debts'] > 0.0, balances)))
	neg_fitness = 1/len(list(filter(lambda b: b['debts'] < 0.0, balances)))
	return min(pos_fitness, neg_fitness)

def generate_model(balances, target=None, base_model=[]):
	if not 'debts' in balances[0]:
		balances = calc_debts(balances)

	if not target:
		target = calc_target_balance(balances)

	balances = apply_transactions(balances, base_model)

	pos = list(filter(lambda b: b['debts'] > 0, balances))
	neg = list(filter(lambda b: b['debts'] < 0, balances))

	pos = sorted(pos, key=lambda t: t['debts'])
	neg = sorted(neg, key=lambda t: t['debts'])

	_result = copy(base_model)
	_from = pos.pop(0)
	for _to in neg:
		while abs(_to['debts']) > 0.01:
			if _from['debts'] <= abs(_to['debts']):
				_amount = _from['debts']
			else:
				_amount = abs(_to['debts'])

			_result.append(transaction(_from['id'], _to['id'], round(_amount,2)))
			_to['debts'] = round(_to['debts'] + _amount, 2)
			_from['debts'] = round(_from['debts'] - _amount, 2)

			if _from['debts'] == 0.0 and len(pos) > 0:
				_from = pos.pop(0)
	return _result

def fit_model(balances):
	return []
