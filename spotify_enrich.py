import json
import os
import requests
from time import sleep

# ==============================
# CONFIGURATIE
# ==============================

INPUT_FILE = "data/songs.json"
OUTPUT_FILE = "data/output_top_tracks.json"

TOP_N = 250           # Aantal tracks dat je wilt behouden
REQUEST_DELAY = 0.1  # Kleine delay tegen rate limits

# ==============================
# SPOTIFY AUTH
# ==============================

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise RuntimeError("Spotify credentials ontbreken")

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    response.raise_for_status()
    return response.json()["access_token"]

# ==============================
# SPOTIFY API
# ==============================

def get_track_popularity(track_id, token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    data = response.json()
    return data.get("popularity")

# ==============================
# MAIN LOGICA
# ==============================

def main():
    print("▶ Laden input JSON...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    print(f"▶ {len(tracks)} tracks gevonden")

    token = get_access_token()
    enriched_tracks = []

    for idx, track in enumerate(tracks, start=1):
        track_id = track.get("spotify_id")
        if not track_id:
            continue

        popularity = get_track_popularity(track_id, token)
        if popularity is None:
            print(f"⚠️ Geen data voor {track.get('title')}")
            continue

        track["popularity"] = popularity
        enriched_tracks.append(track)

        if idx % 25 == 0:
            print(f"  ... {idx}/{len(tracks)} verwerkt")

        sleep(REQUEST_DELAY)

    print("▶ Sorteren op populariteit...")
    enriched_tracks.sort(key=lambda t: t["popularity"], reverse=True)

    top_tracks = enriched_tracks[:TOP_N]

    output = {
        "source": INPUT_FILE,
        "criteria": f"Top {TOP_N} tracks op Spotify popularity",
        "total_tracks_analyzed": len(enriched_tracks),
        "tracks": top_tracks,
    }

    print(f"▶ Schrijven output: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("✅ Klaar!")

# ==============================
# ENTRYPOINT
# ==============================

if __name__ == "__main__":
    main()

