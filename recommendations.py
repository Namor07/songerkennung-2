import requests
import streamlit as st

LASTFM_API_KEY = "DEIN_LASTFM_API_KEY"
LASTFM_BASE_URL = "https://ws.audioscrobbler.com/2.0/"

def get_songs_by_genre(genre, limit=5):
    params = {
        "method": "tag.gettoptracks",
        "tag": genre,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit,
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    data = response.json()

    songs = []

    for track in data.get("tracks", {}).get("track", []):
        songs.append({
            "title": track["name"],
            "artist": track["artist"]["name"],
            "cover": track["image"][-1]["#text"] if track.get("image") else None,
        })

    return songs
