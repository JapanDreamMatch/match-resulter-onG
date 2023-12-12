# なにこれ
このプログラムの開発をしてくれる人への開発環境構築のメモ帳  
~~Seaoftrees08とかいうやつが記憶喪失レベルに忘れるので備忘録。~~

# 開発環境
次を実行して環境構築してください。
環境すでにできてる場合は4からで大丈夫です。

## 1. Pythonのインストール(適宜)  
[Python公式サイト](https://www.python.org/downloads/)からPython落としてインストールします。  
Path通すのを忘れずに。
2023/12/7現在、3.12.0が死んでる(ライブラリがまだ未対応)なので3.11.7でやってます。

## 2. pipのアプデ(適宜)
必要に応じてpipをアプデしてください。
### Windows
`python.exe -m pip install --upgrade pip`  

### Mac/Linux
`python3 -m pip install --upgrade pip`

**※これ以降はコマンド実行ディレクトリがプロジェクトディレクトリ前提で進めます※**

## 3. 仮想環境の作成(clone時のみ)
`venv`という名の仮想環境を作成します。
`python -m venv venv`

## 4. 仮想環境のアクティベート
仮想環境をアクティベートします。
OSによってやり方が異なるので注意。
### Windows
`.\venv\Scripts\activate`

## Mac/Linux
`. ./venv/bin/activate`

アクティベートできていれば`(venv)`がくっついてるはずです。

## 5.ライブラリをインストール
`pip install -r requirements.txt`

## 6. 仮想環境のディアクティベート
終了する場合はこのコマンドで開発環境を抜けることができます。
`deactivate`


## おまけ：VSCodeでvenvを読み込む
VSCodeのsettings.jsonで次を追記  
```json
"python.venvFolders": [
        "envs"
    ]
```
その後、コマンドパレット(ctrl+shift+p)で`Python Interpreter`とか打つと、「Python: インタプリターを選択」が出てくる。
> Note
> Windowsで出てこない人は、インストール場所の権限設定をみましょう。読み取り専用になってるはず
> Python3.11.xはココ→ `C:\Users\USERNAME\AppData\Local\Programs\Python\Python311`
> え、インタプリタも出てこない？
> `venv`フォルダも読み取り専用か確認しましょう。

# ライブラリを新規に入れた場合
ルートディレクトリで次のコマンドを実行して、requirements.txtを更新する。  
`pip freeze > requirements.txt`  

# その他
## discordがimportできないって怒られる
VSCodeのsettings.jsonに次を追記しましょう。
```json
"python.analysis.extraPath" : [
        "${workspaceRoot}/.venv/Lib/site-packages/"
    ],
```