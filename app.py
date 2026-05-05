import streamlit as st
import random

from genre_classifier import predict_genre
from recommendations import (
    get_recommendations_by_genre,
    get_artists_by_genre
)

# -------------------------
# Config
# -------------------------
st.set_page_config(
    page_title="Genre-Erkennung",
    layout="centered"
)

LASTFM_API_KEY = st.secrets["LASTFM_API_KEY"]

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
    max-width: 420px;
    margin: 16px auto;
    padding: 18px;
    border-radius: 18px;
    color: white;
}
.title {
    font-size: 18px;
    font-weight: bold;
}
.meta {
    font-size: 15px;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

def random_bg():
    return random.choice([
        "#1DB954", "#9B59B6", "#E67E22",
        "#3498DB", "#E84393"
    ])

def render_song_card(song):
    st.markdown(
        f"""
        <div class="card" style="background:{random_bg()}">
            <div class="title">{song["title"]}</div>
            <div class="meta">🎤 {song["artist"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_artist_card(artist):
    st.markdown(
        f"""
        <div class="card" style="background:{random_bg()}">
            <div class="title">🎸 {artist["name"]}</div>
            <div class="meta">Beliebter Künstler dieses Genres</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# UI
# -------------------------
st.title("🎧 Genre-Erkennung")
st.write(
    "Lade einen Song hoch. "
    "Die KI erkennt das Genre "
    "und zeigt basierend auf deinem Musikgeschmack passende Songs und Künstler. 🔥 Bisher können nur Songs aus dem Genre Pop und Rock erkannt werden."
)

audio = st.file_uploader(
    "Audio hochladen (MP3 / WAV)",
    type=["mp3", "wav"]
)

if audio and st.button("Genre analysieren"):
    with st.spinner("KI analysiert den Song …"):
        top_genres = predict_genre(audio)

    main_genre, confidence = top_genres[0]

    # Ergebnis
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
        st.info("Für dieses Genre gibt es keine Empfehlungen.")
    else:
        # -------------------------
        # Songs
        # -------------------------
        st.subheader("🎶 Beliebte Songs aus diesem Genre")
        shown = set()

        for tag in tags:
            tracks = get_recommendations_by_genre(tag, LASTFM_API_KEY)
            for song in tracks:
                key = f"{song['artist']} - {song['title']}"
                if key not in shown:
                    shown.add(key)
                    render_song_card(song)

        # -------------------------
        # Artists
        # -------------------------
        st.subheader("🎸 Beliebte Künstler & Bands")
        artists = get_artists_by_genre(tags[0], LASTFM_API_KEY)

        for artist in artists:
            render_artist_card(artist)
