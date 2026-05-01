import numpy as np
import librosa
import tensorflow as tf

MODEL_PATH = "tflite_model/soundclassifier_with_metadata.tflite"

# Interpreter laden
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Labels laden
with open("tflite_model/labels.txt", "r") as f:
    LABELS = [line.strip() for line in f.readlines()]


def preprocess_audio(audio_file):
    # 1 Sekunde, 16 kHz, Mono
    y, sr = librosa.load(audio_file, sr=16000, mono=True)

    if len(y) < 16000:
        y = np.pad(y, (0, 16000 - len(y)))
    else:
        y = y[:16000]

    y = y.astype(np.float32)
    y = np.expand_dims(y, axis=0)

    return y


def predict_genre(audio_file):
    audio = preprocess_audio(audio_file)

    interpreter.set_tensor(input_details[0]["index"], audio)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]["index"])[0]
    index = int(np.argmax(output))

    return LABELS[index]
