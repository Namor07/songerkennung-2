import numpy as np
import librosa
import tensorflow as tf

# Modell & Labels laden
model = tf.keras.models.load_model("genre_model/keras_model.h5")

with open("genre_model/labels.txt", "r") as f:
    LABELS = [line.strip() for line in f.readlines()]


def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=22050, mono=True)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfcc = np.mean(mfcc.T, axis=0)
    return mfcc


def predict_genre(audio_file):
    features = extract_features(audio_file)
    features = features.reshape(1, -1)

    prediction = model.predict(features)
    index = np.argmax(prediction)

    return LABELS[index]
