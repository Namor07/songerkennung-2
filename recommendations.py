import requests

LASTFM_API_KEY = "DEIN_LASTFM_API_KEY"
BASE_URL = "https://ws.audioscrobbler.com/2.0/"

def get_recommendations_by_genre(tag, limit=10):
    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "api_key": LASTFM_API_KEY,
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
        tracks.append({
            "title": t["name"],
            "artist": t["artist"]["name"],
            "album": None,
            "cover": t["image"][-1]["#text"] if t.get("image") else None
        })

    return tracks
