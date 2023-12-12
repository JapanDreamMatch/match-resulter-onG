# WowsShips.py

from rapidfuzz.process import extractOne
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import Rules
import Ship

class WowsShips:
  def __init__(self, credentials_json, ships_sheeet_url):
    # Google SpreadSheet APIの認証情報を使用してクライアントを設定
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
    client = gspread.authorize(credentials)
    self.book = client.open_by_url(ships_sheeet_url)
    self.ships = []
    self.load_ships()

  # 艦を取得
  def load_ships(self):
    for type in Rules.SHIPTYPES:
      worksheets = self.book.worksheets(type)
      for row in worksheets.get_all_values():
        self.ships.append(Ship(row[0], row[1], type, row[3], row[4]))


  # shipsの中から、unture_ship_namesに含まれる艦艇名を検出して返す
  def detect_ships(self, unture_ship_names):
    result_ship_names = []
    for uship in unture_ship_names:
      result_ship_name = extractOne(uship, self.ships)[0]
      result_ship_names.append(result_ship_name)
    return result_ship_names
