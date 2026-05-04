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

def extract_segments(audio_file, sr=44100, segment_duration=1.0, max_segments=8):
    y, sr = librosa.load(audio_file, sr=sr, mono=True)

    segment_length = int(sr * segment_duration)
    segments = []

    for i in range(0, len(y) - segment_length, segment_length):
        segment = y[i:i + segment_length]
        if len(segment) == segment_length:
            segments.append(segment)
        if len(segments) >= max_segments:
            break

    return segments


def predict_genre(audio_file):
    segments = extract_segments(audio_file)

    if not segments:
        return [("Hintergrundgeräusche", 100.0)]

    predictions = []

    for segment in segments:
        input_data = np.expand_dims(segment, axis=0).astype(np.float32)
        interpreter.set_tensor(input_details[0]["index"], input_data)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]["index"])[0]
        predictions.append(output)

    mean_prediction = np.mean(predictions, axis=0)

    results = []
    for i, score in enumerate(mean_prediction):
        results.append((CLASSES[i], round(score * 100, 2)))

    results.sort(key=lambda x: x[1], reverse=True)
    return results
