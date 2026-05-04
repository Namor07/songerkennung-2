import numpy as np
import tensorflow as tf
import librosa
import random

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
WINDOW_SIZE = 44032  # Teachable Machine Standard


def extract_audio_segments(y, sr, num_segments=12):
    """Extrahiert gleichmäßige + zufällige Segmente aus dem Song"""

    total_length = len(y)
    segment_length = WINDOW_SIZE

    segments = []

    # 1. gleichmäßige Fenster
    step = max((total_length - segment_length) // num_segments, 1)

    for i in range(0, total_length - segment_length, step):
        segments.append(y[i:i + segment_length])
        if len(segments) >= num_segments:
            break

    # 2. zufällige zusätzliche Stellen
    for _ in range(3):
        start = random.randint(0, max(0, total_length - segment_length))
        segments.append(y[start:start + segment_length])

    return segments


def predict_genre(audio_file):
    y, sr = librosa.load(audio_file, sr=SAMPLE_RATE, mono=True)

    segments = extract_audio_segments(y, sr)

    predictions = []

    for seg in segments:
        # exakt 44032 Samples
        if len(seg) < WINDOW_SIZE:
            seg = np.pad(seg, (0, WINDOW_SIZE - len(seg)))
        else:
            seg = seg[:WINDOW_SIZE]

        input_data = np.expand_dims(seg, axis=0).astype(np.float32)

        interpreter.set_tensor(input_details[0]["index"], input_data)
        interpreter.invoke()

        output = interpreter.get_tensor(output_details[0]["index"])[0]
        predictions.append(output)

    # 🔥 Mittelwert über alle Segmente
    avg_prediction = np.mean(predictions, axis=0)

    results = [
        (CLASSES[i], round(score * 100, 2))
        for i, score in enumerate(avg_prediction)
    ]

    results.sort(key=lambda x: x[1], reverse=True)

    return results
