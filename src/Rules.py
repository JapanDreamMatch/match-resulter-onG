
import Ship
import WowsShips

LIMITLESS = 32767
SHIPTYPES = ['dd', 'cr', 'bb', 'cv', 'sb']

class Rules:
  def __init__(self, workbook):
    self.countrys = workbook.worksheet("country").col_values(1)
    self.rules = []
    for row in workbook.worksheet("rules").get_all_values():
      self.rules.append(Rule(row[0], self.countrys))

  # 艦艇が全てのルールに沿っているか検証、不適切な艦艇を返す
  def is_confirmed(self, ship_name:str, wows_ships:WowsShips):
    wship = wows_ships.get_ship(ship_name)
    reason = ""
    for rule in self.rules:
      reason = rule.is_confirmed(wship)
      if not reason is None:
        return reason
    return reason

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
      self.b_limit = int(limit)
      
    elif '*ARP' in split_literal[0]:
      self.arp_limit = int(limit)

    elif '*CLR' in split_literal[0]:
      self.clr_limit = int(limit)

    elif any(country in split_literal[0] for country in exist_countrys):
      for country in split_literal:
        if(country in exist_countrys):
          self.restricted_countys.append(country)

    elif any(TYPE in split_literal[0] for TYPE in SHIPTYPES):
      for type in split_literal:
        if(type in SHIPTYPES):
          self.restricted_types.append(type)
    
    else:
      for literal in split_literal:
        self.restricted_ships.append(literal.upper())
      self.restricted_ships.pop()

    self.restricted_limit = int(limit)


  # 艦艇がルールに沿っているか検証、不適切な理由を返す. 通ればNoneを返す.
  def is_confirmed(self, ship: Ship):
    
    if ship is None:
      return "isNone"

    if ship.banned:
      return "isBanned"
    

    if self.b_limit != LIMITLESS and self.shipCount >= self.b_limit and ship.is_B_ship():
      return "B-Shipの制限数 " + str(self.b_limit) + " を超えています。"
    if self.arp_limit != LIMITLESS and self.shipCount >= self.arp_limit and ship.is_ARP_ship():
      return "ARP-Shipの制限数 " + str(self.arp_limit) + " を超えています。"
    if self.clr_limit != LIMITLESS and self.shipCount >= self.clr_limit and ship.is_CLR_ship():
      return "CLR-Shipの制限数 " + str(self.clr_limit) + " を超えています。"
    
    # 艦種制限
    if self.restricted_types and ship.type in self.restricted_types:
      if self.shipCount >= self.restricted_limit:
        return "艦種制限" + str(self.restricted_types) + "が制限数 " + str(self.restricted_limit) + " を超えています。"
      else:
        self.shipCount += 1
        return None

    # 国籍制限
    if self.restricted_countys and ship.country in self.restricted_countys:
      if self.shipCount >= self.restricted_limit:
        return "国籍制限" + str(self.restricted_countys) + "が制限数 " + str(self.restricted_limit) + " を超えています。"
      else:
        self.shipCount += 1
        return None

    # 艦名で制限
    print("shipname: " + ship.names[0] + ", restricted_ships:" + str(self.restricted_ships))
    if self.restricted_ships and ship.is_names(self.restricted_ships):
      if self.shipCount >= self.restricted_limit:
        return "艦名制限" + str(self.restricted_ships) + "が制限数 " + str(self.restricted_limit) + " を超えています。"
      else:
        self.shipCount += 1
        return None
    
    return None



