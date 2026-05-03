import streamlit as st
import random

from genre_classifier import predict_genre
from recommendations import get_songs_by_genre

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

if audio and st.button("🎶 Genre analysieren"):
    with st.spinner("KI analysiert den Song …"):
        top_genres = predict_genre(audio)

        main_genre, confidence = top_genres[0]
        
    # -------------------------
    # Genre Story
    # -------------------------
    st.markdown(
    f"""
    <div class="wrapped-section" style="background:{random_bg()}">
        <div class="wrapped-title">Dein Musik-Vibe</div>
        <div class="song-meta">🎧 Genre: <b>{genre}</b></div>
        <div class="song-meta">📊 Sicherheit: {int(max(confidence)*100)}%</div>
    </div>
    """,
    unsafe_allow_html=True
    )

    # -------------------------
    # Genre Recommendations
    # -------------------------
    st.markdown(
        "<div class='section-heading'>🔥 Beliebte Songs aus diesem Genre</div>",
        unsafe_allow_html=True
    )

    songs = get_songs_by_genre(genre)

    if not songs:
        st.info("Keine Song-Empfehlungen gefunden.")
    else:
        for song in songs:
            st.markdown(
            f"""
            <div class="wrapped-section" style="background:{random_bg()}">
                <div class="wrapped-title">{song["title"]}</div>
                <div class="song-meta">{song["artist"]}</div>
                {"<img src='"+song["cover"]+"' class='wrapped-cover'>" if song.get("cover") else ""}
            </div>
            """,
            unsafe_allow_html=True
            )
