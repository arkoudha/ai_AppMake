import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename    #ファイル名をチェックする関数

from keras.models import Sequential, load_model
import keras, sys
import numpy as np
from PIL import Image

classes = ["monkey", "boar", "crow"]
num_classes = len(classes)
image_size = 50


UPLOAD_FOLDER =  './uploads'           #定数。慣例で大文字で書く
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#ファイルのアップロード可否判定関数
def allowed_file(filename):
    #両方OKなら1 いずれかがNGならゼロを返す
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])

#アップロード関数
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)   #危険な文字などを処理（サニタイズ処理)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            #モデルのロード
            model = load_model('./animal_cnn_aug.h5')

            #ファイルパスから画像を入力する
            image = Image.open(filepath)
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax()     #最大値が入っている配列を返す
            percentage = int(result[predicted] * 100)
            return "ラベル: " + classes[predicted] + ", 確率: "+ str(percentage) + " %"
            #return redirect(url_for('uploaded_file', filename=filename))

    return '''
    <!doctype html>
    <html><head>
    <meta charset="UTF-8">
    <title>ファイルをアップロードして判定しよう</title></head>
    <body>
    <h1>ファイルをアップロードして判定しよう</h1>
    <form method = post enctype = multipart/form-data>
    <p><input type = file name=file>
    <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
