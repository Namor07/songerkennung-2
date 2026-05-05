# recommendations.py
import requests

BASE_URL = "https://ws.audioscrobbler.com/2.0/"

def get_recommendations_by_genre(tag, api_key, limit=10):
    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "api_key": api_key,
        "format": "json",
        "limit": limit
    }

    response = requests.get(
        BASE_URL,
        params=params,
        headers={"User-Agent": "songerkennung-schulprojekt"}
    )

    data = response.json()
    tracks = []

    if "tracks" not in data or "track" not in data["tracks"]:
        return tracks

    for t in data["tracks"]["track"]:
        cover = None

        # Last.fm liefert oft mehrere Bildgrößen
        for img in t.get("image", []):
            if img.get("#text"):
                cover = img["#text"]

        tracks.append({
            "title": t.get("name", "Unbekannt"),
            "artist": t.get("artist", {}).get("name", "Unbekannt"),
            "cover": cover
        })

    return tracks
