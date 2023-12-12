#MatchResulterG.py

import os
from dotenv import load_dotenv
import discord
from Ready import Ready  # GameResultクラスをインポート

# .envファイルから環境変数をロード
load_dotenv()

# 環境変数を取得
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_CREDENTIALS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Botのクライアントを作成
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # ボット自身のメッセージは無視
    if message.author == client.user:
        return

    # CHANNEL_IDのチャンネルに画像が投稿されたか確認
    if message.channel.id == CHANNEL_ID and len(message.attachments) > 0:
        # 画像が添付されているか確認
        if any(attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) for attachment in message.attachments):
            # Readyクラスのインスタンスを作成
            game_result = Ready(message.attachments[0].url, GOOGLE_CREDENTIALS_JSON)
            # OCRテキストを取得
            ocr_text = game_result.get_ocr_text()
            # OCRテキストを返信
            await message.channel.send(f'{ocr_text}')

# Botを起動
client.run(DISCORD_TOKEN)
