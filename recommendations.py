import requests
import streamlit as st

LASTFM_API_KEY = st.secrets["LASTFM_API_KEY"]
BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def get_songs_by_genre(genre, limit=5):
    params = {
        "method": "tag.gettoptracks",
        "tag": genre,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit,
    }

    r = requests.get(BASE_URL, params=params).json()

    songs = []
    for track in r.get("tracks", {}).get("track", []):
        songs.append({
            "title": track["name"],
            "artist": track["artist"]["name"],
            "album": None,
            "cover": track["image"][-1]["#text"] if track["image"] else None
        })

    return songs
