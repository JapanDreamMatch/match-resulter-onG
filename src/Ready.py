# Ready.py

from VisionOCR import VisionOCR
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Ready(VisionOCR):
  def __init__(self, image_url, credentials_json, sheet_url):
    super().__init__(image_url, credentials_json)
    self.sheet_url = sheet_url
    self.members = []
    self.team_members = []
    self.ships = []
    self.team_name = ''
    self.detect_member()
    self.detect_ship()
    


  def detect_ship(self):
    # 文字列を行ごとに分割し、'X 'を含む行のみをリストに追加
    lines = [line for line in self.ocr_text.split('\n') if 'X ' in line]

    #'VIX 'もしくは'X 'を削除
    lines = [line.replace('VIX ', '').replace('X ', '') for line in lines]
    
    # 結果をshipsへ格納
    self.ships = lines



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
    book = client.open_by_url(self.sheet_url)
    worksheets = book.worksheets()

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

    # 出場した選手を記録
    ws = book.worksheet(self.team_name)  # 最適なチームのワークシートを取得
    for i, member in enumerate(self.team_members, start=1):  # メンバーリストをループ（start=1はスプレッドシートが1から始まるため
      for ocr_member in ocr_members:
        if ocr_member.replace(".", "") in member:
          self.members.append(member)



  def player_participation(self):
    # Google SpreadSheet APIの認証情報を使用してクライアントを設定
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_json, scope)
    client = gspread.authorize(credentials)
    book = client.open_by_url(self.sheet_url)
    ws = book.worksheet(self.team_name)  

    for i, member in enumerate(self.team_members, start=1):  # メンバーリストをループ（start=1はスプレッドシートが1から始まるため
      for ocr_member in self.members:
        if ocr_member in member:
          ws.update_cell(i, 2, '出場')  # 出場メンバーの場合右側に'出場'を記入



  def detect_member_from_reply(self, reply_text):
    # メンバーリストと艦艇リストの間のテキストを抽出
    member_list_text = reply_text.split("艦艇リスト:")[0]

    # メンバーリストの名前を抽出し、リストに格納
    member_names = [name.strip() for name in member_list_text.split("メンバーリスト:")[1].split("\n") if name.strip()]

    print(member_names)