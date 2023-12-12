class Ship:
  def __init__(self, name, country, type, tier):
    self.name = name
    self.country = country
    self.type = type
    self.tier = tier
    if tier == "":
      self.tier = 10

  def is_B_ship(self):
    return self.name in " B"
  
  def is_ARP_ship(self):
    return self.name in " ARP"
  
  def is_CLR_ship(self):
    return self.name in " CLR"