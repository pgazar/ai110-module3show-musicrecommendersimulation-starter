# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**RhythmPulse 1.0**

---

## 2. Intended Use  

This recommender is designed to suggest songs from a small classroom dataset based on a user's preferred genre, mood, and audio-style features. It is meant for learning and experimentation.

It should not be used for real listener recommendations, business ranking decisions, or any high-stakes product setting.

---

## 3. How the Model Works  

The model compares each song in the CSV catalog to a user taste profile. It gives a strong bonus for matching `genre` and `mood`, then adds partial similarity points for `energy`, `valence`, `danceability`, `acousticness`, and `tempo_bpm`.

Each song gets a final weighted score plus a list of reasons that explain why it ranked well. The recommender sorts the songs from highest score to lowest score and returns the top results.

---

## 4. Data  

The dataset contains 18 songs stored in `data/songs.csv`. I expanded the starter file from 10 songs to 18 songs by adding new genres like classical, reggaeton, country, metal, afrobeat, blues, house, and folk, along with new moods like serene, fiery, nostalgic, rebellious, celebratory, soulful, euphoric, and tender.

The current features are `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. The dataset still reflects a curated and limited view of music taste, with only one or two songs representing some genres and moods.

---

## 5. Strengths  

This system works best for clear profiles like happy pop, chill lofi, and intense rock. In those cases, the top-ranked songs matched both the categorical preferences and the numeric vibe targets, so the results felt intuitive.

Another strength is transparency. Because the recommender returns reasons along with the score, it is easy to see whether a song ranked highly because of genre, mood, energy, or a mix of several features.

---

## 6. Limitations and Bias 

This recommender can over-prioritize genre because genre match earns a large fixed bonus before any finer-grained taste features are considered. In the conflicting edge-case profile, lofi songs still ranked highly even when the requested mood did not exist in the catalog, which shows how the score can favor one strong category over the full listening context.

The system is also limited by a small dataset. Some genres and moods only appear once, so users with uncommon preferences may get narrow or repetitive recommendations. The model does not understand lyrics, language, artist loyalty, or real listening behavior, so its outputs can seem mathematically correct while still feeling musically incomplete.

---

## 7. Evaluation  

I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and a Conflicting Edge Case with mismatched preferences. For each profile, I looked at the top 5 recommendations and checked whether the ranking made sense based on genre, mood, energy, and the other numeric features.

The most accurate-feeling results came from the High-Energy Pop, Chill Lofi, and Deep Intense Rock profiles because the top songs matched both the categorical preferences and the numeric targets. The biggest surprise came from the Conflicting Edge Case profile, where lofi songs still ranked highly because the genre weight stayed strong even when the mood did not match.

I also ran one sensitivity experiment by doubling the energy weight and halving the genre weight. That change made the pop profile more flexible and allowed songs like `Rooftop Lights` to rise above a stricter genre match such as `Gym Hero`.

---

## 8. Future Work  

- Add richer features like `instrumentalness`, `speechiness`, `liveness`, and `release_year`
- Expand the dataset so each genre and mood has more than one or two examples
- Add diversity logic so the top results are not all near-clones of the same vibe
- Support user preferences as ranges instead of a single fixed target value

---

## 9. Personal Reflection  

My biggest learning moment was seeing how a very small scoring system can still feel like a recommender once the data is structured carefully. A few weights and a few well-chosen features were enough to make the output feel personalized, even though the logic stayed simple.

AI tools were helpful for brainstorming datasets, feature ideas, and documentation structure, but I still had to double-check the actual code behavior, imports, and weight choices. What surprised me most is that simple algorithms can look smart quickly, which also means small design mistakes can create bias just as quickly.
