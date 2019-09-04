from flickrapi import FlickrAPI
from urlli.request import urlretrieve
from pprint import pprint
import os, time, sys

#APIキーの情報

key = "88d96defa0c538ff574854cd43a540c1"
secret = "b3a7ffb885ec209b"
wait_time = 1    #わざと間隔をあけてあげないとスパムと誤認識されてしまう

#保存フォルダの指定
animalname = sys.argv[1]
savedir = "./" + ai_AppMake


flickrapi = FlickrAPI(key, secret, format='parsed-json')