import streamlit as st
from PIL import Image
import numpy as np
import requests
import base64
from io import BytesIO
import json

#POSTするURL設定
post_url = "http://localhost:5000/upload"
#POSTするファイルの読込
files = { "image": "" }
#ヘッダー設定
headers = { "Content-Type": "multipart/form-data" }

def pil_to_base64(img, format="jpeg"):
    buffer = BytesIO()
    img.save(buffer, format)
    img_base64 = base64.b64encode(buffer.getvalue())
    img_str = img_base64.decode('utf-8')
    return img_str

uploaded_file = st.file_uploader('Choose a image file')
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    img_base64 = pil_to_base64(image, format="jpeg") # base64でエンコードされたbytes ※strではない

    files = {
        "image":img_base64
        }

    img_array = np.array(image)
    st.image(
        image, caption='upload images',
        use_column_width=True
    )

if st.button('送信'):
    #POST送信
    response = requests.post(
                post_url,
                data =json.dumps(files))