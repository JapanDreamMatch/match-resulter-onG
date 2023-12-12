
import Ship

LIMITLESS = 32767
SHIPTYPES = ['dd', 'cr', 'bb', 'cv', 'sb']

class Rules:
  def __init__(self, workbook):
    self.countrys = workbook.worksheet("country").col_values(1)
    self.rules = [Rule(row[0], self.countrys) for row in workbook.worksheet("rules").get_all_values()]

  def is_confirmed(self, ship_name:str, wows_ships:list):
    for rule in self.rules:
      if rule.is_confirmed(wows_ships.get_ship(ship_name)):
        return True

class Rule:
  def __init__(self, rule_literal, exist_countrys):
    self.b_limit = LIMITLESS
    self.arp_limit = LIMITLESS
    self.clr_limit = LIMITLESS
    self.restricted_limit = LIMITLESS
    self.restricted_types = []
    self.restricted_countys = []
    self.restricted_ships = []
    self.shipCount = 0

    split_literal = rule_literal.split(',')
    limit = split_literal[-1]

    if '*B' in split_literal[0]:
      self.b_limit = limit
      
    elif '*ARP' in split_literal[0]:
      self.arp_limit = limit

    elif '*CLR' in split_literal[0]:
      self.clr_limit = limit

    elif any(country in split_literal[0] for country in exist_countrys):
      for country in split_literal:
        if(country in exist_countrys):
          self.restricted_countys.append(country)

    elif any(TYPE in split_literal[0] for TYPE in SHIPTYPES):
      for type in split_literal:
        if(type in SHIPTYPES):
          self.restricted_types.append(type)
    
    else:
      self.restricted_ships = split_literal
      self.restricted_ships.pop()

  def is_confirmed(self, ship: Ship):
    if ship is None:
      return False

    if ship.banned:
      return False

    if self.b_limit != LIMITLESS and self.shipCount >= self.b_limit and ship.is_B_ship():
      return False
    if self.arp_limit != LIMITLESS and self.shipCount >= self.arp_limit and ship.is_ARP_ship():
      return False
    if self.clr_limit != LIMITLESS and self.shipCount >= self.clr_limit and ship.is_CLR_ship():
      return False
    if ship.type in self.restricted_types and self.shipCount >= self.restricted_limit:
      return False
    if ship.country in self.restricted_countys and self.shipCount >= self.restricted_limit:
      return False
    if ship.is_names(self.restricted_ships) and self.shipCount >= self.restricted_limit:
      return False
    
    self.shipCount += 1
    return True



