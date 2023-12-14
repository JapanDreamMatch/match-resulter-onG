# Ready.py

from VisionOCR import VisionOCR
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import Rules
from rapidfuzz.process import extractOne

class Ready(VisionOCR):
  def __init__(self, image_url, credentials_json, member_sheet_url, wows_ships):
    super().__init__(image_url, credentials_json)
    self.member_sheet_url = member_sheet_url
    self.ocr_members = []
    self.team_members = []
    self.ocr_ships_name = []
    self.team_name = ''
    self.book = None
    self.wows_ships = wows_ships
    self.rules = Rules.Rules(self.wows_ships.book)
    self.detect_member()
    self.detect_ship()
    


  def detect_ship(self):
    # 文字列を行ごとに分割し、'X 'を含む行のみをリストに追加
    lines = [line for line in self.ocr_text.split('\n') if 'X ' in line]

    #'VIX 'もしくは'X 'を削除
    lines = [line.replace('VIX ', '').replace('X ', '') for line in lines]
    
    # 結果をshipsへ格納
    self.ocr_ships_name = self.wows_ships.detect_ships(lines)



  def detect_member(self):
    text = self.ocr_text

    # 正規表現パターン: アルファベット、数字、アンダースコア、ピリオド、角括弧のみで構成された行
    pattern = re.compile(r'^[A-Za-z0-9_\.\[\]-]+$')
    
    # テキストを行ごとに分割し、パターンにマッチする行のみをリストに追加
    lines = [line for line in text.split('\n') if pattern.match(line)]

    # 'X'だけが格納された行を削除
    lines = [line for line in lines if line != 'X']

    # split(']')を行い、その最後の要素だけでリストを作成
    ocr_members = []
    for line in lines:
      ocr_members.append(line.split(']')[-1])

    # Google SpreadSheet APIの認証情報を使用してクライアントを設定
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_json, scope)
    client = gspread.authorize(credentials)

    # 各チームの登録メンバーリストを取得
    self.book = client.open_by_url(self.member_sheet_url)
    worksheets = self.book.worksheets()

    # 一致するメンバーが最も多いチームを特定
    max_matches = 0
    best_team = None
    for ws in worksheets:
      tmp_members = ws.col_values(1)
      matches = sum(member in tmp_members for member in ocr_members) # 一致するメンバーの数を計算、最大値を更新したらチーム名を更新
      if(matches > max_matches):
        self.team_members = tmp_members
        max_matches = matches
        best_team = ws.title

    # チーム名を格納
    self.team_name = best_team

    # 出場した選手の「...」を補正
#    for name in self.book.worksheet(self.team_name).col_values(1):
#      for ocr_member in ocr_members:
#        if ocr_member.replace(".", "") in name:
#          ocr_members.append(name)
#          ocr_members.remove(ocr_member)
    true_player_names = self.book.worksheet(self.team_name).col_values(1)
    operators = self.book.worksheet('RoomOperator').col_values(1)
    true_members = []
    for untrue_name in ocr_members:
      true_member = extractOne(untrue_name, true_player_names)
      if(float(true_member[1]) > 60):
        true_members.append(true_member[0])
        continue
      
      operator = extractOne(untrue_name, operators)
      if(float(operator[1]) > 60):
        true_members.append(operator[0])
        continue

      true_members.append(untrue_name)


    # 運営メンバーを除く
    for op in self.book.worksheet('RoomOperator').col_values(1):
      if op in true_members:
        ocr_members.remove(op)

    self.ocr_members = ocr_members




  # チームメンバーの出場状況を記録、知らないメンバーを返す 
  def player_participation(self):
    # Google SpreadSheet APIの認証情報を使用してクライアントを設定
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_json, scope)
    client = gspread.authorize(credentials)
    book = client.open_by_url(self.member_sheet_url)
    ws = book.worksheet(self.team_name)

    unknown_members = self.ocr_members.copy()
    for i, row in enumerate(ws.get_all_values()):
      if row[0] in self.ocr_members:
        ws.update_cell(i+1, 2, '出場')
        unknown_members.remove(row[0])

    return unknown_members
  

  # 艦艇がルールに沿っているか検証、不適切な艦艇の理由を返す
  def ships_participation(self):
    unknown_ships = []
    for ship_name in self.ocr_ships_name:
      reason = self.rules.is_confirmed(ship_name, self.wows_ships)
      if not reason is None:
        unknown_ships.append(ship_name + "は"+ reason)
    return unknown_ships

  def detect_from_reply(self, reply_text):
    # メンバーリストの名前を抽出し、リストに格納
    self.ocr_members = [name.strip() for name in reply_text.split("艦艇リスト:")[0].replace("メンバーリスト:\n", "").split("\n") if name.strip()]
    # 艦艇リストの名前を抽出し、リストに格納
    self.ocr_ships_name = self.wows_ships.detect_ships([name.strip() for name in reply_text.split("艦艇リスト:")[1].split("\n") if name.strip()])
