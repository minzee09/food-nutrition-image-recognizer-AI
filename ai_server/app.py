from flask import Flask, request, jsonify
import tensorflow as tf
from keras._tf_keras.keras.models import load_model
#from tensorflow.keras.models import load_model
from keras._tf_keras.keras.applications.resnet50 import preprocess_input
#from tensorflow.keras.applications.resnet50 import preprocess_input
from keras._tf_keras.keras.layers import BatchNormalization
from PIL import Image
import numpy as np
import io
from flask_cors import CORS

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


app = Flask(__name__)
CORS(app)  # CORS 설정

# .h5 모델 로드
custom_objects = {'BatchNormalization': BatchNormalization}
model = load_model('best_model_fixed.h5', custom_objects=custom_objects)

# 이미지 전처리 함수
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image)
    image = preprocess_input(image)
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    image = Image.open(io.BytesIO(file.read()))
    image = preprocess_image(image)
    image = np.expand_dims(image, axis=0)

    # 예측 수행
    nutrition_info = model.predict(image)

    response = {
        'nutrition_info': nutrition_info.tolist()
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
