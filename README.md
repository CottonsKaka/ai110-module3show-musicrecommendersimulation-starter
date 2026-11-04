# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real recommenders like Spotify or YouTube mostly work in two ways: they look at what *other people with similar taste* listened to (collaborative filtering), or they look at the *attributes of the song itself* and match those to what a listener already likes (content-based filtering). My version only does the second one — it never looks at other users' behavior, only at a song's own features compared to one person's stated preferences. That means it can recommend a brand-new song nobody's ever played (no cold-start problem), but it can't surface the kind of unexpected pick that comes from "people like you also loved this" — it will always stay within the lane defined by the user's profile.

To build that, I picked features that each add something distinct rather than restating the same signal. Genre and mood are the two tags, but they're all-or-nothing matches, so I paired them with energy and acousticness — two numeric dials that cut across genre and mood and capture more of the actual "feel" of a song. I left out tempo and danceability for now, since in this dataset they mostly track energy rather than adding new information, so including them would just double-count the same thing instead of making the recommender smarter.

**Features used:**

- `Song`: genre, mood, energy, acousticness *(the four I scored on)* — plus tempo_bpm, valence, danceability, which exist in the data but aren't weighted in v1.
- `UserProfile`: favorite_genre, favorite_mood, target_energy, likes_acoustic.

**Scoring rule (one song at a time):** every song starts at 0 points and gains:

- `+2.0` if its genre matches the user's favorite genre
- `+1.5` if its mood matches the user's favorite mood
- up to `+1.0` for energy, using a closeness formula instead of "higher is better": `1 - |song.energy - target_energy|`, so a song dead-on the user's target energy scores a full point and one far off scores near zero
- up to `+0.5` for acousticness, scaled toward high acousticness if the user likes acoustic songs, or toward low acousticness if they don't

Genre is weighted heaviest because it's usually the most deliberate signal a listener gives ("I want pop"), with mood next, and the numeric features acting as smaller continuous adjustments on top. That weighting is a judgment call, not a provably correct answer — a different recommender could reasonably weight mood over genre.

**Ranking rule (the whole list):** scoring only tells you how good one song is in isolation. To actually produce a recommendation list, every song in the catalog gets scored this way, the full list is sorted highest-to-lowest, and the top `k` are returned along with a plain-language explanation built from whichever rules fired for that song. You need both steps — scoring without ranking is just a pile of numbers, and ranking without scoring has nothing to sort by.

**Finalized Algorithm Recipe:**

```
score = 0
if song.genre == user.favorite_genre:        score += 2.0
if song.mood  == user.favorite_mood:         score += 1.5
score += max(0, 1 - |song.energy - user.target_energy|) * 1.0
if user.likes_acoustic:  score += song.acousticness * 0.5
else:                    score += (1 - song.acousticness) * 0.5
```

**Potential biases I expect:** This system over-prioritizes genre — a song can lose the exact genre match (`+2.0`) and still lose to another song that does match genre even if the first song is a much closer mood and energy fit, since `2.0` alone outweighs the best possible combined mood+energy score for a non-matching genre in some cases. It also treats genre and mood as strict yes/no labels, so a song one tag away from a match (e.g. "indie pop" vs "pop") gets zero credit instead of partial credit, which could make the system feel unfairly dismissive of closely related genres. Finally, because scoring is catalog-relative, an underrepresented genre in the dataset (e.g. only one "metal" song) will rarely surface for users who don't list it as their favorite, even if it would otherwise be a good energy/mood match — small or lopsided catalogs can quietly bias recommendations toward whatever genres are best represented.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

User profile: `{"genre": "pop", "mood": "happy", "energy": 0.8}` (the default profile in `src/main.py`), run with `python -m src.main` against the 18-song catalog in `data/songs.csv`:

```
Loaded songs: 18

Top recommendations:

1. Sunrise City by Neon Echo - Score: 4.48
   Because: genre match (+2.0); mood match (+1.5); energy close to target (+0.98)

2. Gym Hero by Max Pulse - Score: 2.87
   Because: genre match (+2.0); energy close to target (+0.87)

3. Rooftop Lights by Indigo Parade - Score: 2.46
   Because: mood match (+1.5); energy close to target (+0.96)

4. Neon Skyline by Starlet Kim - Score: 0.95
   Because: energy close to target (+0.95)

5. Night Drive Loop by Neon Echo - Score: 0.95
   Because: energy close to target (+0.95)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



