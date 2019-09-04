from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import keras
import numpy as np

classes = ["monkey", "boar", "crow"]
num_classes = len(classes)
image_size = 50

#メインの関数を定義する
def main():
    X_train, X_test, y_train, y_test = np.load("./animal.npy", allow_pickle=True)
    #データの正規化
    X_train = X_train.astype("float") / 256  #浮動小数点数に変換してから256階調で割る
    X_test = X_test.astype("float") / 256
    #one-hot-vector化(正解値は1、その他はゼロ)
    y_train = np_utils.to_categorical(y_train, num_classes)
    y_test = np_utils.to_categorical(y_test, num_classes)

    model = model_train(X_train, y_train)   #モデルの学習
    model_eval(model, X_test, y_test)       #モデルの評価

#学習モデルの定義
def model_train(X, y):
    model = Sequential()
    model.add(Conv2D(32,(3, 3), padding='same',
                input_shape=X.shape[1:])) #X_train.shapeの1番目以降
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))
    model.add(Dense(3))
    model.add(Activation('softmax'))

    #最適化
    opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6) #decayは学習レート
    model.compile(loss='categorical_crossentropy', optimizer=opt,
                    metrics=['accuracy'])

    model.fit(X, y, batch_size=32, nb_epoch=100)

    #モデルの保存
    model.save('./animal_cnn.h5')

    return model

#モデル評価の定義
def model_eval(model, X, y):
    scores = model.evaluate(X, y, verbose=1) #verboseは途中結果出力の有無
    print('Test Loss: ', scores[0])
    print('Test Accuracy: ', scores[1])

#このプログラムが直接呼ばれていた場合は、main()を実行
#そうでない場合は各関数を引用して使用可能
if __name__ == '__main__':
    main()
