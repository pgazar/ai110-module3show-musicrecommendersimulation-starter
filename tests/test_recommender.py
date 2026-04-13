from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    load_songs,
    recommend_songs,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_converts_numeric_fields(tmp_path):
    csv_path = tmp_path / "songs.csv"
    csv_path.write_text(
        (
            "id,title,artist,genre,mood,energy,tempo_bpm,valence,"
            "danceability,acousticness\n"
            "1,Test Song,Artist,pop,happy,0.75,120,0.82,0.67,0.15\n"
        ),
        encoding="utf-8",
    )

    songs = load_songs(str(csv_path))

    assert songs[0]["id"] == 1
    assert isinstance(songs[0]["energy"], float)
    assert isinstance(songs[0]["tempo_bpm"], float)
    assert songs[0]["danceability"] == 0.67


def test_recommend_songs_returns_sorted_scores_and_reasons():
    songs = [
        {
            "id": 1,
            "title": "Perfect Match",
            "artist": "A",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "tempo_bpm": 120.0,
            "valence": 0.85,
            "danceability": 0.8,
            "acousticness": 0.2,
        },
        {
            "id": 2,
            "title": "Far Match",
            "artist": "B",
            "genre": "metal",
            "mood": "rebellious",
            "energy": 0.2,
            "tempo_bpm": 180.0,
            "valence": 0.1,
            "danceability": 0.3,
            "acousticness": 0.9,
        },
    ]
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.82,
        "danceability": 0.78,
        "acousticness": 0.2,
        "tempo_bpm": 122.0,
    }

    results = recommend_songs(user_prefs, songs, k=2)

    assert results[0][0]["title"] == "Perfect Match"
    assert results[0][1] > results[1][1]
    assert "genre match" in results[0][2]
    assert "mood match" in results[0][2]


def test_recommend_songs_handles_k_edge_cases():
    songs = [
        {
            "id": 1,
            "title": "Only Song",
            "artist": "Solo",
            "genre": "folk",
            "mood": "tender",
            "energy": 0.3,
            "tempo_bpm": 75.0,
            "valence": 0.7,
            "danceability": 0.4,
            "acousticness": 0.9,
        }
    ]
    user_prefs = {"genre": "folk", "mood": "tender", "energy": 0.3}

    assert recommend_songs(user_prefs, songs, k=0) == []
    assert len(recommend_songs(user_prefs, songs, k=5)) == 1
