import numpy as np
import librosa
import tensorflow as tf

MODEL_PATH = "soundclassifier_with_metadata.tflite"

CLASS_NAMES = [
    "Hintergrundgeräusche",
    "Klassiche Musik",
    "Pop",
    "Rock",
]

interpreter = tf.lite.Interpreter(
    model_path=MODEL_PATH,
    experimental_delegates=[]
)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

INPUT_LENGTH = input_details[0]["shape"][1]

def extract_segments(audio_file, sr=16000, num_segments=5):
    y, sr = librosa.load(audio_file, sr=sr, mono=True)

    segment_length = INPUT_LENGTH
    max_start = max(0, len(y) - segment_length)

    segments = []

    for _ in range(num_segments):
        start = np.random.randint(0, max_start + 1) if max_start > 0 else 0
        segment = y[start:start + segment_length]

        if len(segment) < segment_length:
            segment = np.pad(segment, (0, segment_length - len(segment)))

        segments.append(segment.astype(np.float32))

    return segments

def predict_genre(audio_file):
    segments = extract_segments(audio_file)
    predictions = []

    for segment in segments:
        input_data = segment.reshape(1, INPUT_LENGTH)
        interpreter.set_tensor(input_details[0]["index"], input_data)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]["index"])[0]
        predictions.append(output)

    avg_prediction = np.mean(predictions, axis=0)
    genre_index = np.argmax(avg_prediction)

    return CLASS_NAMES[genre_index], avg_prediction
