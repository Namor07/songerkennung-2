import streamlit as st
import random

from genre_classifier import predict_genre
from recommendations import get_recommendations_by_genre
LASTFM_API_KEY = st.secrets["LASTFM_API_KEY"]

st.set_page_config(page_title="Genre-Erkennung", layout="centered")

# -------------------------
# Genre-Mapping (KI → Last.fm)
# -------------------------
GENRE_MAPPING = {
    "Hintergrundgeräusche": None,
    "Klassische Musik": ["classical", "instrumental"],
    "Pop": ["pop", "dance pop"],
    "Rock": ["rock", "alternative rock"]
}


# -------------------------
# Styles
# -------------------------
st.markdown("""
<style>
.card {
    max-width: 420px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 18px;
    color: white;
}
.title { font-size: 22px; font-weight: bold; }
.meta { margin-top: 8px; font-size: 16px; }
img { border-radius: 12px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

def random_bg():
    return random.choice([
        "#1DB954", "#9B59B6", "#E67E22", "#3498DB", "#E84393"
    ])

def render_song_card(song):
    st.markdown(
        f"""
        <div class="card" style="background:{random_bg()}">
            <div class="title">{song["title"]}</div>
            <div class="meta">🎤 {song["artist"]}</div>
            {"<img src='" + song["cover"] + "' width='100%'>" if song["cover"] else ""}
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# UI
# -------------------------
st.title("🎧 Genre-Erkennung")
st.write("Lade einen Song hoch, lasse das Genre erkennen und erhalte Vorschläge, die deinem Musikgeschmack entsprechen. Bisher können nur Songs aus dem Genre Pop, Rock und Klassische Musik erkannt werden.")

audio = st.file_uploader("Audio hochladen (MP3 / WAV)", type=["mp3", "wav"])

if audio and st.button("Genre analysieren"):
    with st.spinner("KI analysiert den Song …"):
        top_genres = predict_genre(audio)

    main_genre, confidence = top_genres[0]

    st.markdown(
        f"""
        <div class="card" style="background:{random_bg()}">
            <div class="title">Dein Musik-Vibe</div>
            <div class="meta">🎧 Genre: <b>{main_genre}</b></div>
            <div class="meta">📊 Sicherheit: {confidence}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tags = GENRE_MAPPING.get(main_genre)

    if tags:
        st.subheader("🎶 Beliebte Songs aus diesem Genre")

        shown = set()
        for tag in tags:
            tracks = get_recommendations_by_genre(tag, LASTFM_API_KEY)
            for song in tracks:
                key = f"{song['artist']} - {song['title']}"
                if key not in shown:
                    shown.add(key)
                    render_song_card(song)
                if len(shown) >= 8:
                    break
    else:
        st.info("Für dieses Genre gibt es keine Musik-Empfehlungen.")
