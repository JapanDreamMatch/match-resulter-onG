# 実行環境
[開発環境](./devEnvironment.md)の構築が終わって、プロジェクトディレクトリで実行するものとする。

## .env
.envファイルには次の内容を書き込みます。TOKEN等は必要に応じて書き換えてください。 
ダブルクオーテーションは要りません。     
あと、このファイルは流出するとヤバイので扱いには気を付けてください。  
```.env
DISCORD_TOKEN=your-discord-bot-token
GOOGLE_CREDENTIALS_JSON=your-google-credentials.json
SPREADSHEET_NAME=your-spreadsheet-name
CHANNEL_ID=your-channel-id
```

## keyディレクトリ
GCPのカギ関係はこのフォルダに入れてます。
管理注意！

## gcloud
PowerShellやTerminalでgcloudを使う場合これを入れる  
[gcloud CLI をインストールする](https://cloud.google.com/sdk/docs/install?hl=ja)

Windowsで、次のコマンドを先に実行してログインしないとエラーになったりならなかったり...  
多分最初のインストール時のログインをやってなかったらなるんだと思う  
`gcloud auth application-default login`  
cf. [【GCP】環境変数「GOOGLE_APPLICATION_CREDENTIALS」の設定でエラーが発生する](https://qiita.com/sola-msr/items/8d5f4ae6485a8817edfe)

## Spreadsheet
スプレッドシートの設定はここを見てやった
[Google SpreadSheetのデータを Pythonで取得する](https://qiita.com/venect_qiita/items/4e0f00a70c1b57f948dd)
