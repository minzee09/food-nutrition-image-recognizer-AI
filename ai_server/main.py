import os
import io
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import uvicorn

app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom BatchNormalization Layer
class CustomBatchNormalization(tf.keras.layers.BatchNormalization):
    def __init__(self, **kwargs):
        super(CustomBatchNormalization, self).__init__(**kwargs)

    @classmethod
    def from_config(cls, config):
        # Convert axis from list to int
        if isinstance(config.get('axis'), list):
            config['axis'] = config['axis'][0]
        return cls(**config)

    def get_config(self):
        config = super().get_config()
        return config

def get_custom_objects():
    return {'CustomBatchNormalization': CustomBatchNormalization}

# 모델 로드 함수
def load_model_with_custom_objects(model_path):
    custom_objects = get_custom_objects()
    return tf.keras.models.load_model(model_path, custom_objects=custom_objects)

# 모델 로드
try:
    model = load_model_with_custom_objects('best_model_v4.h5')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# 전처리 함수 정의
def preprocess_image(image: Image.Image):
    image = image.resize((224, 224))
    image = np.array(image)
    image = preprocess_input(image)
    return image

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    processed_image = preprocess_image(image)
    processed_image = np.expand_dims(processed_image, axis=0)

    predictions = model.predict(processed_image)
    predicted_nutrition = predictions[0].tolist()
    
    return JSONResponse(content={"predicted_nutrition": predicted_nutrition})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
