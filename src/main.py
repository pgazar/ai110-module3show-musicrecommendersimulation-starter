"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import DEFAULT_WEIGHTS, load_songs, recommend_songs


PROFILE_CASES = [
    (
        "High-Energy Pop",
        {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.80,
            "valence": 0.82,
            "danceability": 0.78,
            "acousticness": 0.20,
            "tempo_bpm": 122,
        },
    ),
    (
        "Chill Lofi",
        {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "valence": 0.58,
            "danceability": 0.56,
            "acousticness": 0.84,
            "tempo_bpm": 76,
        },
    ),
    (
        "Deep Intense Rock",
        {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "valence": 0.45,
            "danceability": 0.60,
            "acousticness": 0.10,
            "tempo_bpm": 150,
        },
    ),
    (
        "Conflicting Edge Case",
        {
            "genre": "lofi",
            "mood": "sad",
            "energy": 0.90,
            "valence": 0.18,
            "danceability": 0.25,
            "acousticness": 0.88,
            "tempo_bpm": 156,
        },
    ),
]

EXPERIMENTAL_WEIGHTS = {
    **DEFAULT_WEIGHTS,
    "genre": DEFAULT_WEIGHTS["genre"] / 2,
    "energy": DEFAULT_WEIGHTS["energy"] * 2,
}


def build_recommendation_report(
    profile_name: str,
    user_prefs: dict,
    songs: list[dict],
    k: int = 5,
    weights: dict | None = None,
) -> str:
    recommendations = recommend_songs(user_prefs, songs, k=k, weights=weights)

    lines = [
        "",
        "=" * 72,
        f"Profile: {profile_name}",
        (
            "Preferences: "
            f"genre={user_prefs.get('genre')}, "
            f"mood={user_prefs.get('mood')}, "
            f"energy={user_prefs.get('energy')}"
        ),
        "=" * 72,
    ]

    for index, (song, score, explanation) in enumerate(recommendations, start=1):
        lines.append(f"{index}. {song['title']} - {song['artist']}")
        lines.append(
            f"   Score: {score:.2f} | Genre: {song['genre']} | Mood: {song['mood']}"
        )
        lines.append(f"   Reasons: {explanation}")
        lines.append("-" * 72)

    return "\n".join(lines)


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILE_CASES:
        print(build_recommendation_report(profile_name, user_prefs, songs, k=5))

    print("\n" + "#" * 72)
    print("Experiment: Double energy weight and halve genre weight")
    print("#" * 72)
    print(
        build_recommendation_report(
            "High-Energy Pop (Experiment)",
            PROFILE_CASES[0][1],
            songs,
            k=5,
            weights=EXPERIMENTAL_WEIGHTS,
        )
    )


if __name__ == "__main__":
    main()
