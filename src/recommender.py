import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


DEFAULT_WEIGHTS = {
    "genre": 2.0,
    "mood": 1.25,
    "energy": 1.5,
    "valence": 1.0,
    "danceability": 1.0,
    "acousticness": 0.75,
    "tempo_bpm": 0.75,
}


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
    likes_acoustic: bool = False
    target_valence: float | None = None
    target_danceability: float | None = None
    target_acousticness: float | None = None
    target_tempo_bpm: float | None = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        if k <= 0:
            return []

        prefs = _user_to_prefs(user)
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(prefs, _song_to_dict(song))[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        prefs = _user_to_prefs(user)
        _, reasons = score_song(prefs, _song_to_dict(song))
        return "; ".join(reasons) if reasons else "General similarity match."


def _user_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile into the dictionary shape used by scoring."""
    acousticness = (
        user.target_acousticness
        if user.target_acousticness is not None
        else (0.85 if user.likes_acoustic else 0.15)
    )
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "valence": user.target_valence,
        "danceability": user.target_danceability,
        "acousticness": acousticness,
        "tempo_bpm": user.target_tempo_bpm,
    }


def _song_to_dict(song: Song) -> Dict:
    """Convert a Song dataclass into the dictionary shape used by scoring."""
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }


def _closeness(song_value: float, target_value: float, scale: float = 1.0) -> float:
    """Return a 0.0 to 1.0 similarity score based on distance from the target."""
    gap = abs(song_value - target_value) / scale
    return max(0.0, 1.0 - gap)


def score_song(user_prefs: Dict, song: Dict, weights: Dict[str, float] | None = None) -> Tuple[float, List[str]]:
    """Score one song against a user profile and explain the main match reasons."""
    active_weights = weights or DEFAULT_WEIGHTS
    score = 0.0
    reasons: List[str] = []

    if user_prefs.get("genre") == song.get("genre"):
        genre_points = active_weights["genre"]
        score += genre_points
        reasons.append(f"genre match (+{genre_points:.2f})")

    if user_prefs.get("mood") == song.get("mood"):
        mood_points = active_weights["mood"]
        score += mood_points
        reasons.append(f"mood match (+{mood_points:.2f})")

    numeric_weights = {
        "energy": active_weights["energy"],
        "valence": active_weights["valence"],
        "danceability": active_weights["danceability"],
        "acousticness": active_weights["acousticness"],
    }

    for feature, weight in numeric_weights.items():
        if feature in user_prefs and user_prefs[feature] is not None:
            similarity = _closeness(float(song[feature]), float(user_prefs[feature]))
            if similarity > 0:
                points = similarity * weight
                score += points
                reasons.append(f"{feature} close (+{points:.2f})")

    if "tempo_bpm" in user_prefs and user_prefs["tempo_bpm"] is not None:
        tempo_similarity = _closeness(
            float(song["tempo_bpm"]),
            float(user_prefs["tempo_bpm"]),
            scale=80.0,
        )
        if tempo_similarity > 0:
            tempo_points = tempo_similarity * active_weights["tempo_bpm"]
            score += tempo_points
            reasons.append(f"tempo close (+{tempo_points:.2f})")

    return score, reasons

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV and convert numeric fields so they can be scored."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append(
                {
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
                }
            )
    print(f"Loaded songs: {len(songs)}")
    return songs

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weights: Dict[str, float] | None = None,
) -> List[Tuple[Dict, float, str]]:
    """Rank songs for one user profile and return scored explanations."""
    if k <= 0:
        return []

    ranked: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights=weights)
        explanation = ", ".join(reasons) if reasons else "general feature similarity"
        ranked.append((song, score, explanation))

    return sorted(ranked, key=lambda item: item[1], reverse=True)[:k]
