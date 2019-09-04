from PIL import Image
import os, glob #globはファイルの一覧取得
import numpy as np
from sklearn import model_selection

classes = ["monkey", "boar", "crow"]
num_classes = len(classes)
image_size = 50

#画像の読み込み
X = []
Y = []

for index, classlabel in enumerate(classes):
    photos_dir = "./" + classlabel
    files = glob.glob(photos_dir + "/*.jpg")     #パターン一致ファイル一覧取得
    for i, file in enumerate(files):
        if i >= 180: break
        image = Image.open(file)    #ファイルを開く
        image = image.convert("RGB")    #RGB値に変換
        image = image.resize((image_size, image_size))  #冒頭で定義したimage_sizeにリサイズ
        data = np.asarray(image)
        X.append(data)
        Y.append(index)

#TensorFlowが扱いやすいデータ型に変換する
X = np.array(X)
Y = np.array(Y)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
np.save("./animal.npy", xy)
