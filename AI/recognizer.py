import tensorflow as tf
from PIL import Image
import numpy as np
import io
import base64
import os

emnist_dict = {
    0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
    10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J',
    20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T',
    30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z', 36: 'a', 37: 'b', 38: 'c', 39: 'd',
    40: 'e', 41: 'f', 42: 'g', 43: 'h', 44: 'i', 45: 'j', 46: 'k', 47: 'l', 48: 'm', 49: 'n',
    50: 'o', 51: 'p', 52: 'q', 53: 'r', 54: 's', 55: 't', 56: 'u', 57: 'v', 58: 'w', 59: 'x',
    60: 'y', 61: 'z'
}


def preprocess_image_from_base64(base64_string):
    if base64_string.startswith('data:image'):
        base64_string = base64_string.split(",")[1]

    img_data = base64.b64decode(base64_string)
    
    img = Image.open(io.BytesIO(img_data)).convert('L')  # 'L' = escala de cinza
    img = img.resize((28, 28))  # Redimensiona para 28x28
    
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=-1)
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_image_from_base64(base64_string):
    model = tf.keras.models.load_model(os.path.join('AI', 'emnist.h5'))
    img_array = preprocess_image_from_base64(base64_string)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)
    
    return {
        "emnist_class": int(predicted_class),
        "label": emnist_dict[predicted_class],
        "ascii_code": ord(emnist_dict[predicted_class])
    }