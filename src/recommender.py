import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# Weights for the scoring recipe (see README "How The System Works").
GENRE_MATCH_WEIGHT = 2.0
MOOD_MATCH_WEIGHT = 1.5
ENERGY_MATCH_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Scores one song against a user profile, returning (score, reasons)."""
        score = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            score += GENRE_MATCH_WEIGHT
            reasons.append(f"genre match (+{GENRE_MATCH_WEIGHT:.1f})")

        if song.mood == user.favorite_mood:
            score += MOOD_MATCH_WEIGHT
            reasons.append(f"mood match (+{MOOD_MATCH_WEIGHT:.1f})")

        energy_diff = abs(song.energy - user.target_energy)
        energy_points = max(0.0, 1.0 - energy_diff) * ENERGY_MATCH_WEIGHT
        score += energy_points
        if energy_diff < 0.15:
            reasons.append(f"energy close to target (+{energy_points:.2f})")

        if user.likes_acoustic:
            acoustic_points = song.acousticness * ACOUSTIC_WEIGHT
            score += acoustic_points
            if song.acousticness > 0.6:
                reasons.append(f"acoustic match (+{acoustic_points:.2f})")
        else:
            score += (1 - song.acousticness) * ACOUSTIC_WEIGHT

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Scores every song for a user and returns the top k, highest score first."""
        scored = [(song, *self._score(user, song)) for song in self.songs]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _score, _reasons in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was (or wasn't) a good match."""
        score, reasons = self._score(user, song)
        if reasons:
            return f"Recommended because it had a {'; '.join(reasons)} (total score: {score:.2f})."
        return f"Recommended based on overall similarity to your taste profile (score: {score:.2f})."


def load_songs(csv_path: str) -> List[Dict]:
    """Reads a songs CSV into a list of dicts, converting numeric columns to float/int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song dict against a user_prefs dict, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if user_prefs.get("genre") is not None and song["genre"] == user_prefs["genre"]:
        score += GENRE_MATCH_WEIGHT
        reasons.append(f"genre match (+{GENRE_MATCH_WEIGHT:.1f})")

    if user_prefs.get("mood") is not None and song["mood"] == user_prefs["mood"]:
        score += MOOD_MATCH_WEIGHT
        reasons.append(f"mood match (+{MOOD_MATCH_WEIGHT:.1f})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_diff = abs(song["energy"] - target_energy)
        energy_points = max(0.0, 1.0 - energy_diff) * ENERGY_MATCH_WEIGHT
        score += energy_points
        if energy_diff < 0.15:
            reasons.append(f"energy close to target (+{energy_points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is True:
        acoustic_points = song["acousticness"] * ACOUSTIC_WEIGHT
        score += acoustic_points
        if song["acousticness"] > 0.6:
            reasons.append(f"acoustic match (+{acoustic_points:.2f})")
    elif likes_acoustic is False:
        score += (1 - song["acousticness"]) * ACOUSTIC_WEIGHT

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song with score_song, then returns the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        if reasons:
            explanation = "; ".join(reasons)
        else:
            explanation = "general similarity to your taste profile"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
