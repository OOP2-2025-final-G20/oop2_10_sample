# OMS: OMS（Order Manegiment System）


概要:
> このアプリで何ができるのか
> このアプリでは、すでに入力してあるものに対してグラフを作成してくれる。
> また新規顧客・新規製品・新規注文を受け付けることができる。

第10回 講義内資料サンプルコード

ユーザー、製品、注文のデータ登録を行う簡易アプリケーション

データをデータベース(SQLite)に保管するためのサンプルコードを見せつつ外部ライブラリの使用方法について学ばせるためのサンプルです。
グループワークの際に、このリポジトリを各グループのOrganizationにてforkしてもらい、開発を進めます。

## アピールポイント

この部分に、発表に替わる内容を書きます。

前回のプログラムでは作成した三つのタブが個別になっていたのでそれをひとまとめにした。そのひとまとめにしてあるやつを押すと分岐するようにして見やすくすることに成功した。
販売統計とグラフをホームページに実装した。製品ランキング、月次および日次売上データの取得が追加され、視覚的に表現するために Chart.js が統合された。統計とグラフを表示するための HTML 構造が強化された。
注文履歴と製品単価をプログラムが掛け合わせて顧客ごとに合計金額を計算している。Chart.jsのライブラリを用いて描画をさせている。新規注文画面からデータを追加すると、即座にトップページのグラフ（上位5社）も再計算されて更新されるようにした。
作成された注文内容をデータベースから取得し、最新20件分の顧客、製品、個数、注文日時を表示させている。
<img width="2940" height="1614" alt="Image" src="https://github.com/user-attachments/assets/1a450cc0-96fc-4454-ab9e-271e847363f4" />
<img width="1470" height="833" alt="Image" src="https://github.com/user-attachments/assets/4ae398f9-105c-4f65-aac0-e2e600c45031" />
<img width="993" height="768" alt="Image" src="https://github.com/user-attachments/assets/1d9aa998-492f-474f-913f-e026ff323d1f" />
<img width="1168" height="661" alt="Image" src="https://github.com/user-attachments/assets/f02bfd23-d844-43f0-94ad-230ed585bbcb" />
<img width="1440" height="900" alt="Image" src="https://github.com/user-attachments/assets/7491a964-57e2-4080-91ee-a46df3364e03" />



## 動作条件: require

> 動作に必要な条件を書いてください。

```bash
python 3.13 or higher

# python lib
Flask==3.0.3
peewee==3.17.7
```

## 使い方: usage

> このリポジトリのアプリを動作させるために行う手順を詳細に書いてください。

```bash
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ python app.py
```

## プログラミングのルール<br>
- ブランチ名は各人の名簿番号にする<br>

