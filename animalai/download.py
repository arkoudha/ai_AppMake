from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys

#APIキーの情報
key = "88d96defa0c538ff574854cd43a540c1"
secret = "b3a7ffb885ec209b"
wait_time = 1    #わざと間隔をあけてあげないとスパムと誤認識されてしまう

#保存フォルダの指定
animalname = sys.argv[1]    #コマンドライン引数で指定
savedir = "./" + animalname #コマンドライン引数で指定した名前のフォルダを保存用とする


flickr = FlickrAPI(key, secret, format='parsed-json') #jsonファイルをパースする
result = flickr.photos.search(
    text = animalname,  #取得したい画像名
    per_page = 400,     #取得するデータ数(※外れ値も考えて多めに取得)
    media = 'photos',   #取得するデータの種類
    sort = 'relevance', #関連順
    safe_search = 1,    #有害コンテンツの排除
    extras = 'url_q, licence'   #取得したいオプション値(url_q ← 画像のURL, ライセンス)
)

photos = result['photos']
#pprint(photos)

for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']
    filepath = savedir + '/' + photo['id'] + '.jpg'
    if os.path.exists(filepath): continue   #すでにfilepathが存在する場合はスルー
    urlretrieve(url_q, filepath)         #上記1行でfilepathが存在しなかった場合はurl_qのファイルをDLしfilepathに保存)
    time.sleep(wait_time)                   #wait_time秒待機させる
