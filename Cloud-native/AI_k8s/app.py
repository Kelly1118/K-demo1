# import tensorflow as tf
# import numpy as np
# from flask import Flask, request, jsonify
#
# app = Flask(__name__)
# model = tf.keras.models.load_model('mnist_model.h5')
#
#
# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json(force=True)
#     image = np.array(data['image']).reshape((1, 28, 28, 1)).astype('float32') / 255.0
#     prediction = model.predict(image).tolist()
#     return jsonify({'prediction': prediction})
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
import tensorflow as tf
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# 加载模型，并检查模型文件是否存在
try:
    model = tf.keras.models.load_model('mnist_model.h5')
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 接收 JSON 数据并解析
        data = request.get_json(force=True)
        if 'image' not in data:
            return jsonify({'error': 'Missing "image" key in JSON payload'}), 400

        # 验证并处理输入数据
        image = np.array(data['image']).reshape((1, 28, 28, 1)).astype('float32') / 255.0
    except Exception as e:
        return jsonify({'error': f"Invalid input data: {e}"}), 400

    # 预测返回结果
    try:
        prediction = model.predict(image).tolist()
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': f"Error during prediction: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)