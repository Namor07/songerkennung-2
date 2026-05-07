import streamlit as st
import random

from genre_classifier import predict_genre
from recommendations import (
    get_recommendations_by_genre,
    get_artists_by_genre
)

# -------------------------------------------------
# Konfiguration
# -------------------------------------------------
st.set_page_config(
    page_title="🎧 Genre-Erkennung",
    layout="centered"
)

LASTFM_API_KEY = st.secrets["LASTFM_API_KEY"]

# -------------------------------------------------
# Session State (SEHR WICHTIG)
# -------------------------------------------------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "main_genre" not in st.session_state:
    st.session_state.main_genre = None

if "confidence" not in st.session_state:
    st.session_state.confidence = None

if "recommendation_seed" not in st.session_state:
    st.session_state.recommendation_seed = random.random()

# -------------------------------------------------
# Genre Mapping (KI → Last.fm Tags)
# -------------------------------------------------
GENRE_MAPPING = {
    "Hintergrundgeräusche": None,
    "Pop": ["pop", "dance pop", "indie pop"],
    "Rock": ["rock", "alternative rock", "classic rock"]
}

# -------------------------------------------------
# Styles
# -------------------------------------------------
st.markdown("""
<style>
.card {
    max-width: 420px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 18px;
    color: white;
}
.title {
    font-size: 22px;
    font-weight: bold;
}
.meta {
    margin-top: 6px;
    font-size: 16px;
}
.artist-card {
    max-width: 420px;
    margin: 12px auto;
    padding: 14px;
    border-radius: 14px;
    background: #222;
    color: white;
    font-size: 17px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Hilfsfunktionen
# -------------------------------------------------
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
        </div>
        """,
        unsafe_allow_html=True
    )

def render_artist_card(artist):
    st.markdown(
        f"""
        <div class="artist-card">
            🎸 <b>{artist}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# UI
# -------------------------------------------------
st.title("🎧 Genre-Erkennung mit KI")
st.write(
    "Lade einen Song hoch, lass das Genre von einer KI erkennen "
    "und erhalte passende Musik-Empfehlungen. 🔥"
)

audio = st.file_uploader(
    "🎵 Audio hochladen (MP3 oder WAV)",
    type=["mp3", "wav"]
)

# -------------------------------------------------
# Genre analysieren (NUR Analyse!)
# -------------------------------------------------
if audio and st.button("🎶 Genre analysieren"):
    with st.spinner("KI analysiert den Song …"):
        top_genres = predict_genre(audio)

    st.session_state.main_genre, st.session_state.confidence = top_genres[0]
    st.session_state.analysis_done = True
    st.session_state.recommendation_seed = random.random()

# -------------------------------------------------
# Analyse-Ergebnis anzeigen
# -------------------------------------------------
if st.session_state.analysis_done:
    st.markdown(
        f"""
        <div class="card" style="background:{random_bg()}">
            <div class="title">Dein Musik-Vibe</div>
            <div class="meta">🎧 Genre: <b>{st.session_state.main_genre}</b></div>
            <div class="meta">📊 Sicherheit: {st.session_state.confidence:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# Neue Empfehlungen Button
# -------------------------------------------------
if st.session_state.analysis_done:
    if st.button("🔁 Neue Empfehlungen laden"):
        st.session_state.recommendation_seed = random.random()

# -------------------------------------------------
# Empfehlungen anzeigen (IMMER NUR EINMAL)
# -------------------------------------------------
if st.session_state.analysis_done:
    random.seed(st.session_state.recommendation_seed)

    tags = GENRE_MAPPING.get(st.session_state.main_genre)

    if not tags:
        st.info("Für dieses Genre gibt es keine Empfehlungen.")
    else:
        # ---------------- Songs ----------------
        st.subheader("🎶 Beliebte Songs aus diesem Genre")

        all_tracks = []
        for tag in tags:
            all_tracks.extend(
                get_recommendations_by_genre(
                    tag,
                    LASTFM_API_KEY,
                    limit=40
                )
            )

        random.shuffle(all_tracks)

        shown = set()
        for song in all_tracks:
            key = f"{song['artist']} - {song['title']}"
            if key not in shown:
                shown.add(key)
                render_song_card(song)
            if len(shown) >= 8:
                break

        # ---------------- Artists ----------------
        st.subheader("🎸 Beliebte Künstler & Bands")

        artists = get_artists_by_genre(
            tags[0],
            LASTFM_API_KEY,
            limit=15
        )

        random.shuffle(artists)
        for artist in artists[:8]:
            render_artist_card(artist)
