# recommendations.py
import requests

BASE_URL = "https://ws.audioscrobbler.com/2.0/"

# -------------------------
# Songs nach Genre
# -------------------------
def get_recommendations_by_genre(tag, api_key, limit=8):
    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "api_key": api_key,
        "format": "json",
        "limit": limit
    }

    r = requests.get(
        BASE_URL,
        params=params,
        headers={"User-Agent": "songerkennung-schulprojekt"}
    )

    data = r.json()
    tracks = []

    for t in data.get("tracks", {}).get("track", []):
        tracks.append({
            "title": t.get("name", "Unbekannt"),
            "artist": t.get("artist", {}).get("name", "Unbekannt")
        })

    return tracks


# -------------------------
# Künstler / Bands nach Genre
# -------------------------
def get_artists_by_genre(tag, api_key, limit=8):
    params = {
        "method": "tag.gettopartists",
        "tag": tag,
        "api_key": api_key,
        "format": "json",
        "limit": limit
    }

    r = requests.get(
        BASE_URL,
        params=params,
        headers={"User-Agent": "songerkennung-schulprojekt"}
    )

    data = r.json()
    artists = []

    for a in data.get("topartists", {}).get("artist", []):
        artists.append({
            "name": a.get("name", "Unbekannt")
        })

    return artists
