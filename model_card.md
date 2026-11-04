# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Think of it like a judge scoring a talent show, one contestant (song) at a time. Every song walks in with zero points, and it earns points for matching what the listener said they want: a bonus if the genre matches exactly, a smaller bonus if the mood matches, a sliding bonus for how close the song's energy is to what they asked for (not just "more energy is better" — being too energetic is penalized the same as not being energetic enough), and a small bonus for acousticness depending on whether the listener said they like acoustic sound or not. Genre counts for the most points because it felt like the most deliberate thing a listener tells you about their taste, with mood worth a bit less, and the two numeric features acting as smaller nudges on top.

Once every song in the catalog has a score, the model just sorts them from highest to lowest and hands back the top handful — that sorted list is the "recommendation." Along the way it also keeps a short list of plain-English reasons for each song (like "genre match (+2.0)") so a listener can see exactly why something was suggested instead of just trusting a mystery number.

The starter code was just empty placeholders (`# TODO: Implement...`) with no scoring or ranking at all — everything described above, including the point values and the reason messages, was designed and written from scratch rather than tweaked from an existing version.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
