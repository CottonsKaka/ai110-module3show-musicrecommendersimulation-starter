# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeDial 1.0** — because it works like turning a few dials (genre, mood, energy, acousticness) rather than anything that actually "understands" music.

---

## 2. Intended Use  

**Designed for:** a classroom demo of content-based recommendation on a small, curated, 18-song catalog. It's meant to show how a handful of weighted rules can turn song attributes and a stated taste profile into a ranked, explainable list — nothing more.

It assumes the "user" can state explicit preferences up front (a favorite genre, a favorite mood, a target energy, an acoustic yes/no) rather than being inferred from behavior. It's for exploration and learning, not real listeners — there's no account system, no persistence of taste over time, and no real audio analysis (the numeric features are hand-entered, not computed from actual audio).

**Not intended for:** making real music-streaming product decisions, inferring anything about a real person's demographics or identity from their stated preferences, or running on a catalog much larger than a few dozen songs without a redesign — the exact-match genre/mood scoring and the tiny hand-built dataset don't scale to real-world catalog sizes or diversity.

---

## 3. How the Model Works  

Think of it like a judge scoring a talent show, one contestant (song) at a time. Every song walks in with zero points, and it earns points for matching what the listener said they want: a bonus if the genre matches exactly, a smaller bonus if the mood matches, a sliding bonus for how close the song's energy is to what they asked for (not just "more energy is better" — being too energetic is penalized the same as not being energetic enough), and a small bonus for acousticness depending on whether the listener said they like acoustic sound or not. Genre counts for the most points because it felt like the most deliberate thing a listener tells you about their taste, with mood worth a bit less, and the two numeric features acting as smaller nudges on top.

Once every song in the catalog has a score, the model just sorts them from highest to lowest and hands back the top handful — that sorted list is the "recommendation." Along the way it also keeps a short list of plain-English reasons for each song (like "genre match (+2.0)") so a listener can see exactly why something was suggested instead of just trusting a mystery number.

The starter code was just empty placeholders (`# TODO: Implement...`) with no scoring or ranking at all — everything described above, including the point values and the reason messages, was designed and written from scratch rather than tweaked from an existing version.

---

## 4. Data  

18 songs total in `data/songs.csv` — the original 10 from the starter file, plus 8 I added to cover genres and moods that were completely missing (electronic, blues, metal, r&b, folk, classical, reggae, k-pop; euphoric, melancholic, angry, romantic, nostalgic, dreamy, triumphant). Each song has 7 attributes beyond its id/title/artist: genre, mood, energy, tempo_bpm, valence, danceability, acousticness — all on a 0.0–1.0 scale except tempo_bpm.

Even at 18 songs, 13 different genres appear exactly once each, so most genres have zero internal variety to rank between. Whole dimensions of real musical taste are missing entirely: lyrics and language, instrumentation, era/decade, cultural or regional style, an artist's broader catalog or popularity, and any notion of how a song changes over its own runtime (tempo/energy here are single fixed numbers per song, not a timeline).

---

## 5. Strengths  

It's clearly personalized, not just catalog order: the three main test profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) each produced a completely different, non-overlapping top 5 — see Section 7. It works best for a user whose favorite genre has more than one song in the catalog (pop, lofi), since there's actual competition to rank between.

The explanations match my intuition about *why* a song should rank where it does — Sunrise City winning the High-Energy Pop profile because it hits genre, mood, and energy all at once feels obviously correct, and I could predict most of the top-3 results before running the code just by eyeballing the CSV.

It also doesn't break on messy input. An empty profile, a nonexistent genre, or a self-contradictory profile (high energy + a mood no song has) all still return a ranked list instead of crashing — the system degrades to energy-only ranking rather than failing outright, which is a reasonable fallback even if it isn't flagged as one (see Section 6).

---

## 6. Limitations and Bias 

Counting the catalog directly: of 18 songs, 13 genres appear exactly once each, while `lofi` has 3 and `pop` has 2 (plus a separate `indie pop` tag). That means a user whose favorite genre is one of those 13 singleton genres (rock, metal, classical, folk, blues, jazz, k-pop, r&b, reggae, ambient, synthwave, electronic, indie pop) can only ever earn the `+2.0` genre bonus from one specific song, no matter how well or badly that song otherwise fits them — there's no competition within the genre to surface a *better* match, so the system effectively has one "correct answer" per underrepresented genre and treats everyone who likes that genre identically. Meanwhile lofi and pop fans get real variety and genuine ranking among 2–3 candidates. Testing also showed the system over-relies on genre and energy relative to mood: in both the "High-Energy Pop" and "Deep Intense Rock" profiles, the same song (Gym Hero) ranked in the top 2 despite the two profiles wanting opposite moods ("happy" vs. "intense"), because genre+energy points alone outweigh a mood match. Finally, the system has no concept of an invalid or unrecognized input — a `genre`/`mood` value that doesn't exist anywhere in the catalog (or a mood like "sad" that was never tagged on any song) is silently scored as "no match" rather than flagged, so a confused or contradictory user profile still produces a confident-looking top-5 list instead of an honest "I don't have anything for that" response.

---

## 7. Evaluation  

I tested three "normal" taste profiles and three adversarial/edge-case profiles against the 18-song catalog.

**Normal profiles** (`python -m src.main`):

```
=== High-Energy Pop ({'genre': 'pop', 'mood': 'happy', 'energy': 0.8}) ===
1. Sunrise City by Neon Echo - Score: 4.48 - genre match (+2.0); mood match (+1.5); energy close to target (+0.98)
2. Gym Hero by Max Pulse - Score: 2.87 - genre match (+2.0); energy close to target (+0.87)
3. Rooftop Lights by Indigo Parade - Score: 2.46 - mood match (+1.5); energy close to target (+0.96)
4. Neon Skyline by Starlet Kim - Score: 0.95 - energy close to target (+0.95)
5. Night Drive Loop by Neon Echo - Score: 0.95 - energy close to target (+0.95)

=== Chill Lofi ({'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}) ===
1. Library Rain by Paper Lanterns - Score: 4.93 - genre match (+2.0); mood match (+1.5); energy close to target (+1.00); acoustic match (+0.43)
2. Midnight Coding by LoRoom - Score: 4.79 - genre match (+2.0); mood match (+1.5); energy close to target (+0.93); acoustic match (+0.35)
3. Focus Flow by LoRoom - Score: 3.34 - genre match (+2.0); energy close to target (+0.95); acoustic match (+0.39)
4. Spacewalk Thoughts by Orbit Bloom - Score: 2.89 - mood match (+1.5); energy close to target (+0.93); acoustic match (+0.46)
5. Coffee Shop Stories by Slow Stereo - Score: 1.43 - energy close to target (+0.98); acoustic match (+0.45)

=== Deep Intense Rock ({'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}) ===
1. Storm Runner by Voltline - Score: 4.94 - genre match (+2.0); mood match (+1.5); energy close to target (+0.99)
2. Gym Hero by Max Pulse - Score: 2.94 - mood match (+1.5); energy close to target (+0.97)
3. Neon Pulse by EchoSynth - Score: 1.44 - energy close to target (+0.98)
4. Crimson Riot by Ironclad - Score: 1.42 - energy close to target (+0.93)
5. Neon Skyline by Starlet Kim - Score: 1.40 - energy close to target (+0.95)
```

**Adversarial / edge-case profiles:**

```
=== Conflicting (pop genre, "sad" mood, energy 0.95) ===
1. Gym Hero (pop/intense) - Score: 3.46 - genre match (+2.0); energy close to target (+0.98)
2. Sunrise City (pop/happy) - Score: 3.28 - genre match (+2.0); energy close to target (+0.87)
3. Crimson Riot (metal/angry) - Score: 1.46 - energy close to target (+0.98)

=== Nonexistent genre/mood ("k-dance"/"giddy", energy 0.5) ===
1. Island Time (reggae/relaxed) - Score: 1.00 - energy close to target (+1.00)
2. Golden Hour (r&b/romantic) - Score: 0.95 - energy close to target (+0.95)
3. Midnight Coding (lofi/chill) - Score: 0.92 - energy close to target (+0.92)

=== Empty preferences ({}) ===
1. Sunrise City - Score: 0.00 - general similarity to your taste profile
2. Midnight Coding - Score: 0.00 - general similarity to your taste profile
3. Storm Runner - Score: 0.00 - general similarity to your taste profile
```

**Pairwise comparisons:**

- *High-Energy Pop vs. Chill Lofi:* completely different top 5, no overlap. The pop profile favors loud, upbeat, electronic-leaning tracks; the lofi profile shifts entirely toward quiet, acoustic-leaning tracks — makes sense, since `likes_acoustic=True` plus a low target energy pulls in the exact opposite direction on two separate scoring terms at once.
- *Chill Lofi vs. Deep Intense Rock:* also zero overlap, and the score gaps are much wider for rock (4.94 → 1.40) than for lofi (4.93 → 1.43), because the catalog only has one rock song, so after Storm Runner there's nothing left to give a genre bonus to — the list falls back hard to energy-only scoring.
- *High-Energy Pop vs. Deep Intense Rock:* both profiles put **Gym Hero** in their top 2, despite one wanting "happy" and the other wanting "intense." That's the clearest sign the system leans on genre + energy over mood — a pop/high-energy song is a decent generic answer for almost any "upbeat" request, which is also the bias described in Section 6 below.

**What surprised me:** the "conflicting" profile (pop + sad + very high energy) didn't produce anything resembling "sad" — it just returned the same high-energy pop songs as the happy profile, because no song in the catalog has `mood="sad"`, so that term silently contributed zero instead of signaling "no good match." The "nonexistent genre" profile behaved the same way — an unrecognized `genre`/`mood` is treated exactly like "no preference stated," not flagged as invalid. The empty-preferences profile also didn't error out; it just returned the first 5 catalog rows in their original order, since every score ties at 0.00. None of this crashes, but it means the system can confidently hand back a list that doesn't actually address what the (admittedly contradictory or garbled) input asked for, with no warning to the user.

**Why "Gym Hero" keeps showing up for "Happy Pop" fans (plain language):** Gym Hero is a fast, upbeat pop song, so it earns genre points *and* energy points just from being pop and intense/high-energy — even for someone who said they want a "happy" mood and Gym Hero is actually tagged "intense." Genre + energy alone adds up to more points than a mood match by itself, so a loud pop song that's merely "energy-adjacent" can beat a quieter song that's a perfect mood match. It's the musical equivalent of recommending someone the loudest song in the room because they said they like upbeat music, even if they specifically asked for something cheerful rather than aggressive.

---

## 8. Future Work  

1. **Partial credit for similar genres/moods** instead of strict exact-match — right now "indie pop" gets zero credit from a "pop" fan even though they're obviously related. A small similarity table (or genre embedding) would fix the single-song-per-genre bottleneck described in Section 6.
2. **A real "no good match" signal** — when a user's genre/mood isn't in the catalog at all, the system should say so instead of quietly falling back to energy-only ranking and presenting the result with full confidence.
3. **A simulated collaborative signal** layered on top — even a fake "other listeners who liked X also liked Y" table would let the system recommend outside a user's stated genre/mood, which right now it structurally cannot do (see "How The System Works" in the README).  

---

## 9. Personal Reflection  

My biggest learning moment was realizing scoring and ranking are genuinely two separate problems, not one — I kept wanting to think of "the algorithm" as one thing, but scoring only ever looks at one song in isolation, and ranking is the step that turns a pile of numbers into an actual ordered list. Once I had that split clear, debugging why a particular song ranked where it did got a lot easier, because I could check the score breakdown first and the sort order second instead of guessing at both at once.

AI tools helped most with speed and with making the design decisions explicit instead of leaving them implicit in code I'd forget the reasoning for later — walking through the weighting choices (why genre outweighs mood, how to turn "closer energy is better" into a formula) out loud before writing anything meant I understood the recipe rather than just having working code. Where I had to double-check things: the weighting (2.0 genre / 1.5 mood / etc.) is a judgment call dressed up as a formula, not a provably "correct" answer, so I made sure to actually run adversarial profiles rather than assume the math was fair just because it was consistent. I also had to re-verify sample outputs in the README after expanding the dataset, since a code sample that was accurate against the original 10-song catalog silently became stale once I added 8 more songs — nothing flags that kind of drift automatically.

What surprised me is how much a handful of weighted if-statements can already *feel* like a real recommendation — and how quickly that same simplicity produces a real bias, not a hypothetical one. Gym Hero legitimately shows up near the top for both a "happy" profile and an "intense" profile, which is a small-scale version of the same "the algorithm thinks everyone wants the loudest thing" complaint people make about real platforms. If I extended this project, I'd want to try the partial-credit genre similarity idea from Section 8 first, since the single-song-per-genre problem feels like the most concrete, fixable flaw I found.
