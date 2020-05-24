from .generator import GruwiGenerator
import random

class Calc1(GruwiGenerator):
  description = 'Einfache Rechenaufgaben mit den Grundrechenarten für Jahrgangsstufe 5. Keine negativen Zahlen.'
  
  examples = (
      ('5 + 6 = {}','11'),
      ('9 * 24 = {}', '216')
    )
  
  tags = [
      'Jg.5',
      'Sek.I',
      'Rechnen', 
      'Grundrechenarten'
    ]
  
  def generate(self, level=1, numbers=None:
  	if not numbers:
  		numbers = [random.randint(n,n+50) for n in range(12)]
    operators = ('+','-','*','/')
    n = random.sample(numbers, 2)
    op = random.choice(operators)
    if op in ['-', '/']:
      t = n[0]
      n[0] = max(n)
      n[1] = min(n[1],t)
    if op == '/':
    	solution = n[0]
      n[0] = n[0]*n[1]
    task = f'{n[0]} {op} {n[1]}'
    solution = eval(task)
    return ('%s %s %s = {}' % (n[0], op, n[1]), solution)
