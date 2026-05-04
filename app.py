import streamlit as st
import random

from genre_classifier import predict_genre
from recommendations import get_recommendations_by_genre

# -------------------------
# Genre-Mapping (KI → Last.fm)
# -------------------------

GENRE_MAPPING = {
    "Hintergrundgeräusche": None,
    "Klassische Musik": ["classical", "orchestral", "instrumental"],
    "Pop": ["pop", "dance pop", "indie pop"],
    "Rock": ["rock", "alternative rock", "classic rock"]
}

st.set_page_config(page_title="Genre Wrapped", layout="centered")

# -------------------------
# Styles
# -------------------------
def random_bg():
    colors = [
        "#1DB954", "#191414", "#FF4F81", "#6A5ACD",
        "#FF8C00", "#20B2AA", "#8A2BE2"
    ]
    return random.choice(colors)

st.markdown("""
<style>
.wrapped-section {
    max-width: 600px;
    margin: 20px auto;
    padding: 25px;
    border-radius: 20px;
    color: white;
    text-align: center;
}
.wrapped-title {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
}
.song-meta {
    font-size: 18px;
    margin: 5px 0;
}
.wrapped-cover {
    margin-top: 15px;
    width: 150px;
    border-radius: 12px;
}
.section-heading {
    text-align: center;
    font-size: 22px;
    margin-top: 40px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# UI
# -------------------------
st.title("🎧 Genre Wrapped")
st.write("Lade einen Song hoch und entdecke seinen Musik-Vibe.")

audio = st.file_uploader("🎵 Audiodatei hochladen (MP3 oder WAV)", type=["mp3", "wav"])

if audio and st.button("Analysieren"):
    with st.spinner("KI analysiert das Genre …"):
        top_genres = predict_genre(audio)

    # Hauptgenre + Sicherheit
    main_genre, confidence = top_genres[0]

    # -------------------------
    # UI: Erkanntes Genre
    # -------------------------
    st.markdown(
    f"""
    <div class="wrapped-section">
        <div class="wrapped-title">Dein Musik-Vibe</div>
        <div class="song-meta">🎧 Genre: <b>{main_genre}</b></div>
        <div class="song-meta">📊 Sicherheit: {confidence}%</div>
    </div>
    """,
    unsafe_allow_html=True
    )

    # optional: Top Genres anzeigen
    for genre, score in top_genres:
        st.write(f"{genre}: {score}%")

    # -------------------------
    # Genre Recommendations
    # -------------------------
    st.markdown(
        "<div class='section-heading'>🔥 Beliebte Songs aus diesem Genre</div>",
        unsafe_allow_html=True
    )

        # -------------------------
    # Genre → Last.fm Tags
    # -------------------------
    lastfm_tags = GENRE_MAPPING.get(main_genre)

    if not lastfm_tags:
        st.info("Kein Musikgenre erkannt – keine Empfehlungen möglich.")
    else:
        st.write("### 🎶 Beliebte Songs aus deinem Genre")

        shown = set()

        for tag in lastfm_tags:
            tracks = get_recommendations_by_genre(tag)

            for song in tracks:
                key = f"{song['artist']} - {song['title']}"
                if key not in shown:
                    shown.add(key)
                    render_song_card(song)

                if len(shown) >= 10:
                    break
