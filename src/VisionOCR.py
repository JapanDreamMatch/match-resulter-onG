# VisionOCR.py

from google.cloud import vision
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

class VisionOCR:
  def __init__(self, image_url, credentials_json):
    self.image_url = image_url
    self.credentials_json = credentials_json


    self.ocr_text = self.perform_ocr(credentials_json) # 本番ではここで読み取り

    # 本番はFalseに
    if(False):
      with open(os.getenv('TEST_TEXT_PATH'), 'r', encoding='utf-8') as file:
        self.ocr_text = file.read()

    load_dotenv()

  def perform_ocr(self, credentials_json):
    # Google Vision APIクライアントを設定
    credentials = service_account.Credentials.from_service_account_file(credentials_json)
    vision_client = vision.ImageAnnotatorClient(credentials=credentials)

    # 画像データを取得
    image = vision.Image()
    image.source.image_uri = self.image_url

    # Google Vision APIを使用してテキスト検出
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    # 最初のテキストアノテーションは画像全体のテキスト
    if texts:
      return texts[0].description
    else:
      return 'テキストが検出されませんでした。'

  def get_ocr_text(self):
    return self.ocr_text
