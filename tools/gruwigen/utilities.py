import datetime

def generate_numbers():
  numbers = set()
  _today = datetime.date.today()
  numbers.add(_today.day)
  numbers.add(_today.month)
  numbers.add(_today.year)
  for n in numbers.copy():
    m = str(n)
    for o in m:
      numbers.add(int(o))
  _year = str(_today.year)
  for i in range(len(_year)-1):
    numbers.add(int(_year[i:(i+2)]))
  return numbers - {0}
