import numpy as np
import tensorflow as tf
import librosa

MODEL_PATH = "soundclassifier_with_metadata.tflite"

interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

CLASSES = [
    "Hintergrundgeräusche",
    "Klassische Musik",
    "Pop",
    "Rock"
]

SAMPLE_RATE = 44100
WINDOW_SIZE = 44032  # exakt Teachable-Machine-Standard


def load_and_prepare(audio_file):
    y, sr = librosa.load(audio_file, sr=SAMPLE_RATE, mono=True)

    if len(y) < WINDOW_SIZE:
        y = np.pad(y, (0, WINDOW_SIZE - len(y)))
    else:
        y = y[:WINDOW_SIZE]

    # Modell erwartet [1, 44032]
    return np.expand_dims(y, axis=0).astype(np.float32)


def predict_genre(audio_file):
    input_data = load_and_prepare(audio_file)

    interpreter.set_tensor(
        input_details[0]["index"],
        input_data
    )
    interpreter.invoke()

    output = interpreter.get_tensor(
        output_details[0]["index"]
    )[0]

    results = []
    for i, score in enumerate(output):
        results.append((CLASSES[i], round(score * 100, 2)))

    results.sort(key=lambda x: x[1], reverse=True)
    return results
