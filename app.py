# app.py
import streamlit as st
import random

from genre_classifier import predict_genre
from recommendations import get_recommendations_by_genre

# -------------------------
# Config
# -------------------------
st.set_page_config(
    page_title="Genre-Erkennung",
    layout="centered"
)

LASTFM_API_KEY = st.secrets["LASTFM_API_KEY"]

PLACEHOLDER_COVER = (
    "https://via.placeholder.com/400x400/"
    "121212/FFFFFF?text=No+Cover"
)

# -------------------------
# Genre-Mapping (KI → Last.fm)
# -------------------------
GENRE_MAPPING = {
    "Pop": ["pop"],
    "Rock": ["rock"],
    "Klassische Musik": ["classical"]
}

# -------------------------
# Styles
# -------------------------
st.markdown("""
<style>
.card {
    max-width: 360px;
    margin: 20px auto;
    padding: 16px;
    border-radius: 18px;
    color: white;
    text-align: center;
}
.title { font-size: 18px; font-weight: bold; }
.meta { font-size: 14px; opacity: 0.9; margin-top: 4px; }
.cover {
    width: 100%;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

def random_bg():
    return random.choice([
        "#1DB954", "#9B59B6", "#E67E22",
        "#3498DB", "#E84393"
    ])

def render_song_card(song):
    cover = song.get("cover") or PLACEHOLDER_COVER

    st.markdown(
        f"""
        <div class="card" style="background:{random_bg()}">
            <img class="cover" src="{cover}">
            <div class="title">{song["title"]}</div>
            <div class="meta">🎤 {song["artist"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# UI
# -------------------------
st.title("🎧 Genre-Erkennung (KI)")
st.write(
    "Lade einen Song hoch. "
    "Das KI-Modell erkennt das Genre "
    "und zeigt passende Song-Empfehlungen."
)

audio = st.file_uploader(
    "Audio hochladen (MP3 / WAV)",
    type=["mp3", "wav"]
)

if audio and st.button("Genre analysieren"):
    with st.spinner("KI analysiert den Song …"):
        top_genres = predict_genre(audio)

    main_genre, confidence = top_genres[0]

    # Ergebnis-Karte
    st.markdown(
        f"""
        <div class="card" style="background:{random_bg()}">
            <div class="title">Dein Musik-Vibe</div>
            <div class="meta">🎧 Genre: <b>{main_genre}</b></div>
            <div class="meta">📊 Sicherheit: {confidence:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tags = GENRE_MAPPING.get(main_genre)

    if not tags:
        st.info("Für dieses Genre gibt es noch keine Empfehlungen.")
    else:
        st.subheader("🎶 Beliebte Songs aus diesem Genre")

        shown = set()
        for tag in tags:
            tracks = get_recommendations_by_genre(
                tag,
                LASTFM_API_KEY,
                limit=8
            )

            for song in tracks:
                key = f"{song['artist']} - {song['title']}"
                if key not in shown:
                    shown.add(key)
                    render_song_card(song)
