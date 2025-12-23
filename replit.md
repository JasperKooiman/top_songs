# Top Songs - Spotify Enricher

## Overview
A Python CLI tool that enriches song data with Spotify popularity scores. It reads songs from a JSON file, fetches popularity data from the Spotify API, and outputs the top tracks sorted by popularity.

## Project Structure
- `spotify_enrich.py` - Main script that fetches Spotify popularity data
- `data/songs.json` - Input file containing song data with Spotify IDs
- `data/output_top_tracks.json` - Output file with enriched and sorted tracks
- `requirements.txt` - Python dependencies

## Configuration
The script requires two environment variables:
- `SPOTIFY_CLIENT_ID` - Your Spotify API client ID
- `SPOTIFY_CLIENT_SECRET` - Your Spotify API client secret

You can get these from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

## Running the Script
Run via the "Spotify Enricher" workflow or execute:
```bash
python spotify_enrich.py
```

## Recent Changes
- 2025-12-23: Initial setup for Replit environment
  - Installed Python 3.11
  - Installed requests package
  - Created console workflow
