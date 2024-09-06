import tensorflow as tf
from keras._tf_keras.keras.models  import load_model, save_model
from keras._tf_keras.keras.layers import BatchNormalization

# 기존 모델 로드
model = load_model('best_model_fixed.h5')
# 모델 저장
model_json = model.to_json()
with open("best_model_fixed.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("best_model_fixed.h5")

