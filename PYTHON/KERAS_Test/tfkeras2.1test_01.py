#https://www.tensorflow.org/tutorials/keras/classification
#첫 번째 신경망 훈련하기: 기초적인 분류 문제
#FASHION MNIST

import tensorflow as tf
from tensorflow import keras #tf.keras 임포트

#MNIST 데이터셋 로드, 샘플값을 정수에서 부동소수로 변환
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

#층을 차례대로 쌓아 tf.keras.Sequential 모델을 생성. 훈련에 사용할 옵티마이저(optimizer)와 손실 함수를 선택:
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
#모델 훈련 & 평가
model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test,  y_test, verbose=2)

print()

