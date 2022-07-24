from pathlib import Path
from werkzeug.utils import secure_filename

from flask import Flask
from flask import render_template, redirect, send_from_directory, request

import json


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "static" / "media"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_folder="static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=["POST"])
def upload():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    if data["image"] == "":
        # ファイルが選択されていない場合
        print('ファイルが選択されていません')
        return redirect('/')

    img = data['image']
    # 画像として読み込み

    if img.filename == "":
        # ファイル名がついていない場合
        print("ファイル名がありません")
        return redirect('/')

    if img and allowed_file(img.filename):
        filename = secure_filename(img.filename)

        try:
            img.save(UPLOAD_FOLDER / filename)
            # 画像を保存
        except Exception as e:
            print(f"画像の保存に失敗: {e}")

        return redirect('/')


if __name__ == '__main__':
    app.run()