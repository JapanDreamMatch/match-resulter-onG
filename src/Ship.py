# Ship.py

class Ship:
  def __init__(self, name, country, type, tier, banned):
    self.names = name.upper().split(',')
    self.country = country
    self.type = type
    self.tier = tier
    self.banned = "ban" in banned.lower()
    if tier == "":
      self.tier = 10

  def is_B_ship(self):
    return any(" B" in name for name in self.names)
  
  def is_ARP_ship(self):
    return any("ARP " in name for name in self.names)
  
  def is_CLR_ship(self):
    return any(" CLR" in name for name in self.names)
  
  def is_name(self, search_name):
    return any(search_name in name for name in self.names)
  
  # 検索する名前がself.namesに含まれているかどうかを返す
  def is_names(self, search_names: list):
    self_upper_names = []
    for name in self.names:
      self_upper_names.append(name.upper() if name.isascii() else name)

    return any(sname in self_upper_names for sname in search_names)