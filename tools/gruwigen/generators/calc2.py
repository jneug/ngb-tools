from .generator import GruwiGenerator

class Calc2(GruwiGenerator):
  description = 'Einfache umgekehrte Rechenaufgaben mit den Grundrechenarten für Jahrgangsstufe 5.'
  
  examples = (
      ('{} - 2 = 6','8'),
      ('9 * {} = 63', '7')
    )
  
  tags = [
      'Jg.5',
      'Sek.I',
      'Rechnen', 
      'Grundrechenarten'
    ]
  
  def generate(self, level=1, numbers=set()):
    return ('{}', '0')
