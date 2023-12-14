#MatchResulterG.py

import os
from dotenv import load_dotenv
import discord
from Ready import Ready #VisionOCR使いすぎないための措置
import asyncio
import WowsShips

# .envファイルから環境変数をロード
load_dotenv()

# 環境変数を取得
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_CREDENTIALS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')
MEMBER_SPREADSHEET_URL = os.getenv('MEMBERS_SPREADSHEET_URL')
SHIPS_SHEET_URL = os.getenv('SHIPS_SHEET_URL')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Botのクライアントを作成
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

awaiting = []
wows_ships = WowsShips.WowsShips(GOOGLE_CREDENTIALS_JSON, SHIPS_SHEET_URL)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  # ボット自身のメッセージは無視
  if message.author == client.user:
    return

@client.event
async def on_message(message):
  # ボット自身のメッセージは無視
  if message.author == client.user:
    return

  # CHANNEL_IDのチャンネル以外、または添付ファイルがない場合は処理をスキップ
  if message.channel.id != CHANNEL_ID or len(message.attachments) <= 0:
    return
  
  # 承認待ちの場合は処理をスキップ
  if message.author in awaiting:
    return
  
  # 承認待ちをリセット
  if message.content == '!matchresulter flush':
    awaiting.clear()
    await message.channel.send('承認待ちをリセットしました。')
    return
  
  # debug用
  if message.content == '!matchresulter debug':
    msg = ""
    await message.channel.send(msg)
    return

  # 画像が添付されているか確認
  if any(attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) for attachment in message.attachments):
    # Readyクラスのインスタンスを作成
    ready_info = Ready(message.attachments[0].url, 
                        GOOGLE_CREDENTIALS_JSON, 
                        MEMBER_SPREADSHEET_URL, 
                        wows_ships
                      )
    
    # メンバーリストと艦艇リストを整形してメッセージとして送信
    member_list = '\n'.join(ready_info.ocr_members)
    ship_list = '\n'.join(ready_info.ocr_ships_name)
    confirmation_message = str(f"メンバーリスト:\n{member_list}\n\n艦艇リスト:\n{ship_list}\n\nこのリストを修正してください。修正が完了したら、'修正完了'と返信してください。"
      + "\n修正する場合は内容をコピー&ペーストして内容を修正してください。\n1分経過で自動承認とします。")
    
    # 返信メッセージを送信
    confirmation_msg = await message.reply(confirmation_message)
    awaiting.append(message.author)
    
    # ユーザーからの応答を待つ
    def check(m):
      return m.author == message.author and (m.content == '修正完了' or '艦艇リスト:' in m.content)
    
    try:
      # ユーザーからの応答を待つ（タイムアウトは60秒）
      user_response = await client.wait_for('message', check=check, timeout=60.0)
      
      # ユーザーの応答に基づいて処理
      if user_response.content == '修正完了':
        await confirmation_msg.reply('リストが承認されました。')
      elif '艦艇リスト:' in user_response.content:
        # 修正されたメンバーリストと艦艇リストを取得
        ready_info.detect_from_reply(user_response.content)
        confirmation_message = str(f"メンバーリスト:\n{member_list}\n\n艦艇リスト:\n{ship_list}\n\nこのリストを修正してください。修正が完了したら、'修正完了'と返信してください。"
      + "\n修正する場合は内容をコピー&ペーストして内容を修正してください。\n1分経過で自動承認とします。")
        await confirmation_msg.reply('修正されました。spreadsheetに記入します。')
      else:
        await confirmation_msg.reply('リストの修正が中止されました。')
        return

    except asyncio.TimeoutError:
      await confirmation_msg.reply('タイムアウトしましたので自動承認とします。')

    awaiting.remove(message.author)

    #Spreadsheetに記述
    unknown_memebers = ready_info.player_participation()
    unknown_ships = ready_info.ships_participation()
    await user_response.reply(f'選手を記録しました。')
    if unknown_memebers:
      await message.channel.send(f'以下のメンバーは登録されていません。再確認をお願いします。\n{unknown_memebers}')
    if unknown_ships:
      reasons = ""
      for unknown_ship in unknown_ships:
        reasons += unknown_ship + "\n"
      await user_response.reply(f'以下の艦艇は登録されていません。再確認をお願いします。\n' + reasons)




# Botを起動
client.run(DISCORD_TOKEN)
