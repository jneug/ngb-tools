import os
import importlib
import random

from utilities import generate_numbers

for _,_,files in os.walk(os.path.abspath('./generators')):
  _generators = filter(lambda f: f.endswith('.py'), files)

_generators = map(lambda f: f[:-3], _generators)
_generators = filter(lambda m: m not in ['__init__', 'generator'], _generators)

generators = []
for m in _generators:
  _module = importlib.import_module('generators.%s' % m)
  _class = getattr(_module, dir(_module)[0])
  #_class = getattr(_module, m.title())
  generators.append(_class)

tasks = ([],[])
numbers = generate_numbers()

# generate tasks
for l in range(2):
  for i in range(5):
    gen = random.choice(generators)()
    task = gen.generate(level=l+1, numbers=numbers)
    tasks[l].append(task)
  

for task in tasks[0]:
  print(task[0].format('?'))
print('-'*10)
for task in tasks[1]:
  print(task[0].format('?'))
print('='*10)
for task in tasks[0]:
  print(task[0].format(task[1]))
print('-'*10)
for task in tasks[1]:
  print(task[0].format(task[1]))
