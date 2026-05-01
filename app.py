import random
import streamlit as st
from genre_classifier import predict_genre
from recommendations import get_songs_by_genre

st.set_page_config(page_title="Genre Wrapped", page_icon="🎧", layout="wide")

# ==================================================
# CSS (identisch zur ersten App)
# ==================================================
st.markdown("""
<style>
.wrapped-section {
    max-width: 760px;
    margin: 0 auto 60px auto;
    padding: 70px 40px;
    border-radius: 28px;
    color: white;
}
.section-heading {
    max-width: 760px;
    margin: 80px auto 20px auto;
    font-size: 32px;
    font-weight: 800;
}
.wrapped-title {
    font-size: 44px;
    font-weight: 800;
}
.song-meta {
    font-size: 22px;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

GRADIENTS = [
    "linear-gradient(135deg, #7f00ff, #e100ff)",
    "linear-gradient(135deg, #1db954, #1ed760)",
    "linear-gradient(135deg, #ff512f, #dd2476)",
    "linear-gradient(135deg, #396afc, #2948ff)",
]

def random_bg():
    return random.choice(GRADIENTS)

# ==================================================
# UI
# ==================================================
st.title("🎧 Dein Genre Wrapped")
st.write("Lade einen Song hoch – das KI-Modell erkennt dein Musikgenre.")

audio = st.file_uploader("Audiodatei hochladen (MP3 oder WAV)", ["mp3", "wav"])

if audio and st.button("Genre analysieren"):
    with st.spinner("KI analysiert das Genre …"):
        genre = predict_genre(audio)

# ----------------------------------------------
# STORY 1 – ERKANNTES GENRE
# ----------------------------------------------
st.markdown(
f"""
<div class="wrapped-section" style="background:{random_bg()}">
    <div class="wrapped-title">Dein Musik-Vibe</div>
    <div class="song-meta">🎧 Genre: <b>{genre}</b></div>
</div>
""",
unsafe_allow_html=True
)

# ----------------------------------------------
# STORY 2 – SONG-EMPFEHLUNGEN AUS DEM GENRE
# ----------------------------------------------
st.markdown(
    "<div class='section-heading'>🔥 Beliebte Songs aus diesem Genre</div>",
    unsafe_allow_html=True
)

genre_songs = get_songs_by_genre(genre)

if not genre_songs:
    st.info("Für dieses Genre wurden keine Songs gefunden.")
else:
    for song in genre_songs:
        st.markdown(f"""
<div class="wrapped-section" style="background:{random_bg()}">
    <div class="wrapped-title">{song["title"]}</div>
    <div class="song-meta">{song["artist"]}</div>
    {"<img src='"+song["cover"]+"' class='wrapped-cover'>" if song.get("cover") else ""}
</div>
""", unsafe_allow_html=True)
