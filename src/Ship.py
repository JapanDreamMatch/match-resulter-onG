# Ship.py

class Ship:
  def __init__(self, name, country, type, tier, banned):
    self.names = name.split(',')
    self.country = country
    self.type = type
    self.tier = tier
    self.banned = "ban" in banned.lower()
    if tier == "":
      self.tier = 10

  def is_B_ship(self):
    return self.names in " B"
  
  def is_ARP_ship(self):
    return self.names in "ARP "
  
  def is_CLR_ship(self):
    return self.names in " CLR"
  
  def is_name(self, name):
    return name in self.names
  
  def is_names(self, search_name):
    self_upper_names = []
    for name in self.names:
      print("search_name: " + str(search_name))
      self_upper_names.append(name.upper() if name.isascii() else name)
    print("upper_names: " + str(self_upper_names))

    return any(search_name in self_upper_names)