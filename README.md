# 🎵 Music Recommender Simulation

## Project Summary

This project builds a small CLI-first music recommender that compares a user taste profile to songs in a CSV catalog and ranks the closest matches. My version uses genre, mood, and multiple numeric audio-style features so the recommendations feel more explainable than a simple random playlist.

---


## How The System Works

This recommendation system uses a simple **content-based filtering approach**. Instead of learning from other users, it compares each song's features to a user's preferences and recommends songs that are most similar in style and feel.

### 🎵 Song Features
Each `Song` in the system includes:

- `energy` - intensity of the track  
- `valence` - how positive or negative the song sounds  
- `danceability` - how suitable the song is for dancing  
- `acousticness` - whether the song is more acoustic or electronic  
- `tempo_bpm` - speed of the song  
- `genre` - type of music (for example pop, rock, or lofi)  
- `mood` - overall emotional tone (for example happy, chill, or intense)  

I expanded the dataset from 10 songs to 18 songs by adding `classical`, `reggaeton`, `country`, `metal`, `afrobeat`, `blues`, `house`, and `folk`, plus new moods like `serene`, `fiery`, `nostalgic`, `rebellious`, `celebratory`, `soulful`, `euphoric`, and `tender`.

Future features I would add to deepen the simulation:

- `instrumentalness`
- `speechiness`
- `liveness`
- `loudness`
- `release_year` or `recency_score`

---

### 👤 UserProfile
The main `UserProfile` for the starter simulation uses these target values:

- `favorite_genre = "pop"`  
- `favorite_mood = "happy"`  
- `target_energy = 0.80`  
- `target_valence = 0.82`  
- `target_danceability = 0.78`  
- `target_acousticness = 0.20`  
- `target_tempo_bpm = 122`  

This profile is narrow enough to clearly prefer upbeat pop songs, but still flexible enough to distinguish between something like intense rock and chill lofi by using multiple features instead of genre alone.

---

### 🧠 Scoring Logic
The recommender computes a score for each song using this weighted recipe:

- `+2.0` points for a **genre** match  
- `+1.25` points for a **mood** match  
- up to `+1.5` points for **energy** similarity  
- up to `+1.0` point for **valence** similarity  
- up to `+1.0` point for **danceability** similarity  
- up to `+0.75` points for **acousticness** similarity  
- up to `+0.75` points for **tempo_bpm** similarity  

For numerical features, the system measures how close the song is to the user's target value. Closer values receive more points, which means songs can still score well even without an exact match.

---

### 🎯 Recommendation Selection
- The system loads every song from `data/songs.csv`  
- It calculates a score and explanation for every song  
- Songs are ranked from highest to lowest score  
- The top `k` songs are returned as recommendations  

---

### 🔁 Simple Flow

User Preferences -> Compare with Song Features -> Compute Scores -> Rank Songs -> Recommend Top Results

```mermaid
flowchart LR
    A["User Preferences"] --> B["Load songs from data/songs.csv"]
    B --> C["Loop through each song"]
    C --> D["Check genre and mood"]
    C --> E["Measure numeric similarity"]
    D --> F["Build score and reasons"]
    E --> F
    F --> G["Sort from highest to lowest"]
    G --> H["Return Top K recommendations"]
```

Potential bias note: This system might over-prioritize genre, ignoring songs that match the user's mood and numeric preferences but come from a different genre label.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the tests with:

```bash
pytest
```

Extra edge-case checks I added cover CSV parsing, ranking order, and behavior when `k` is zero or larger than the catalog.

If a global pytest plugin interferes on your machine, this repo-specific fallback command works too:

```bash
PYTHONPATH=. PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -p no:cacheprovider
```

---

## Experiments You Tried

- **High-Energy Pop:** `Sunrise City` ranked first, followed by `Gym Hero` and `Rooftop Lights`. This felt right because the profile strongly favored upbeat, high-energy, positive songs.
- **Chill Lofi:** `Library Rain`, `Midnight Coding`, and `Focus Flow` rose to the top. This made sense because they matched the lofi genre, chill mood, lower energy, and higher acousticness targets.
- **Deep Intense Rock:** `Storm Runner` ranked first by a wide margin. It matched both the rock/intense labels and landed very close on the energy and tempo targets.
- **Conflicting Edge Case:** lofi songs still ranked well even though the requested mood did not exist in the data. This revealed that the genre weight can overpower other missing preferences.
- **Weight Shift Experiment:** After doubling energy and halving genre, `Rooftop Lights` moved above `Gym Hero` for the pop profile. That change made the system more flexible and less genre-dominated.

### CLI Output Snapshots

![High-Energy Pop CLI](assets/high-energy_pop.png)

![Chill Lofi CLI](assets/chill_lofi.png)

![Deep Intense Rock CLI](assets/deep_intense_rock.png)

![Conflicting Edge Case CLI](assets/conflicting_edge_case.png)

![Weight Shift Experiment CLI](assets/high_energy_pop_experiment.png)

---

## Limitations and Risks

- The catalog is still tiny, so some genres and moods only have one representative song
- Genre has a strong fixed weight, which can create a filter bubble
- The system does not use lyrics, artist familiarity, or listening history
- Numeric closeness can sometimes reward a song that matches the math better than the real listening vibe

You will go deeper on this in the model card.

---

## Reflection

I learned that a recommender can feel surprisingly personal even when the logic is just a weighted scoring formula. Once taste is translated into features like genre, mood, and energy, the system can produce results that make intuitive sense, but only if the dataset is varied enough and the weights are balanced carefully.

I also learned how easy it is for bias to appear in a simple system. A small catalog or an oversized genre bonus can make the same kinds of songs keep floating to the top, which is a good reminder that even transparent recommenders still reflect the choices made by the person designing them.

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance.

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
```
