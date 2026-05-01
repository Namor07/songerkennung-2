import io
import numpy as np
import soundfile as sf
import tensorflow as tf
from scipy.signal import resample

MODEL_PATH = "tflite_model/soundclassifier_with_metadata.tflite"

# TensorFlow Lite Interpreter
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Erwartete Audio-Länge aus Modell lesen
EXPECTED_SAMPLES = input_details[0]["shape"][1]

# Labels laden
with open("tflite_model/labels.txt", "r") as f:
    LABELS = [line.strip() for line in f.readlines()]


def preprocess_audio(uploaded_file):
    # Datei lesen
    audio_bytes = uploaded_file.read()
    y, sr = sf.read(io.BytesIO(audio_bytes), dtype="float32")

    # Stereo → Mono
    if y.ndim > 1:
        y = np.mean(y, axis=1)

    # Resampling auf 16 kHz (TM-Standard)
    if sr != 16000:
        y = resample(y, int(len(y) * 16000 / sr))

    # Auf Modell-Länge bringen
    if len(y) < EXPECTED_SAMPLES:
        y = np.pad(y, (0, EXPECTED_SAMPLES - len(y)))
    else:
        y = y[:EXPECTED_SAMPLES]

    # Modell-Input-Form
    y = np.expand_dims(y, axis=0).astype(np.float32)

    return y


def predict_genre(uploaded_file):
    audio = preprocess_audio(uploaded_file)

    interpreter.set_tensor(input_details[0]["index"], audio)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]["index"])[0]
    index = int(np.argmax(output))

    return LABELS[index]
