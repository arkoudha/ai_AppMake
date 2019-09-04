from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys

#APIキーの情報

key = "88d96defa0c538ff574854cd43a540c1"
secret = "b3a7ffb885ec209b"
wait_time = 1    #わざと間隔をあけてあげないとスパムと誤認識されてしまう

#保存フォルダの指定
animalname = sys.argv[1]  #コマンドライン引数でファイル指定(.pyファイルの次に指定する)
savedir = "./" + animalname


flickr = FlickrAPI(key, secret, format='parsed-json')
result = flickr.photos.search(
    text = animalname,  #検索キーワード
    per_page = 400,     #どれぐらいデータを持ってくるか(外れ値が多いから多めに)
    media = 'photos',   #データの種類
    sort = 'relevance', #relevance ← 検索の関連順
    safe_search = 1,    #有害コンテンツ非表示のオプション
    extras = 'url_q, licence'  #取得したいオプション値(url_q←画像のアドレス、licence←ライセンス情報)
)

photos = result['photos']
pprint(photos)