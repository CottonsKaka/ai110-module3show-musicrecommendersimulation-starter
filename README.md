# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version, **VibeDial 1.0**, represents each song as a set of attributes (genre, mood, energy, tempo, valence, danceability, acousticness) and each user as a small taste profile (favorite genre, favorite mood, target energy, and whether they like acoustic sound). The `Recommender` scores every song against the profile using a weighted rule, ranks songs highest-score-first, and returns the top `k` along with a plain-language explanation of why each one was picked. See `model_card.md` for the full writeup, including how it behaves under adversarial and edge-case profiles.

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

**Weight shift: genre 2.0 → 1.0, energy 1.0 → 2.0** (tested on the "Deep Intense Rock" profile: `genre=rock, mood=intense, energy=0.9`). Default weights ranked Storm Runner (4.94), Gym Hero (2.94), Neon Pulse (1.44), Crimson Riot (1.42), Neon Skyline (1.40). After the shift: Storm Runner (4.93), Gym Hero (3.92), Neon Pulse (2.42), Neon Skyline (2.35), Crimson Riot (2.35) — the #1 and #2 songs didn't change at all, because Storm Runner already wins on genre *and* mood *and* energy, so no single-weight change could unseat it. The scores at the bottom got closer together and position 4/5 flipped, but the recommendation a user actually sees (the top result) was identical either way. **Takeaway:** the weights matter a lot for close calls, but a song that's a strong match on every axis is robust to re-weighting — this experiment made the *scores* different, not meaningfully more or less accurate.

**How different user types behave:** three named profiles (`High-Energy Pop`, `Chill Lofi`, `Deep Intense Rock`) each produce completely non-overlapping top-5 lists (see Sample Recommendation Output and `model_card.md` Evaluation section for full terminal output) — confirming the ranking is genuinely personalized rather than returning catalog order. Full stress-test output, including adversarial/edge-case profiles, is documented in `model_card.md`.

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

Building this made it concrete that a recommender doesn't "understand" music at all — it turns data into predictions by picking a handful of attributes, assigning each one a point value, adding them up per song, and sorting. That's it. There's no magic in the middle; the "prediction" is just the highest-scoring row after a loop. What surprised me is how convincing that can still feel: when the weights are tuned reasonably, the output looks like genuine taste-matching even though the system has no idea what a song sounds like beyond a handful of numbers someone typed into a CSV.

Bias shows up fastest in whatever the dataset is thin on. In my 18-song catalog, 13 of the genres have exactly one song each, so a listener's "favorite genre" bonus only ever has one possible winner — the system can't actually discriminate between good and bad fits within an underrepresented genre, it just defaults to whatever's there. I also found that genre and energy together can outweigh mood, so the same high-energy pop song showed up as a top pick for both a "happy" and an "intense" profile — a small, very literal example of a recommender flattening two different requests into the same loud answer. Full details and terminal output are in [`model_card.md`](model_card.md).



