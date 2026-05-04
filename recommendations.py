import requests
import streamlit as st

LASTFM_API_KEY = "DEIN_LASTFM_API_KEY"
LASTFM_BASE_URL = "https://ws.audioscrobbler.com/2.0/"

tracks = get_recommendations_by_genre(tag)

def get_recommendations_by_genre(tag, limit=10):
    """
    Holt beliebte Songs zu einem Genre von Last.fm
    """
    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }

    response = requests.get(LASTFM_BASE_URL, params=params)
    data = response.json()

    tracks = []

    if "tracks" not in data:
        return tracks

    for item in data["tracks"]["track"]:
        tracks.append({
            "title": item["name"],
            "artist": item["artist"]["name"],
            "album": None,
            "cover": item["image"][-1]["#text"] if item.get("image") else None
        })

    return tracks
