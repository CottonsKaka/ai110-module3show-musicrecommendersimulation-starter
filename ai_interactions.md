# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I worked through the whole assignment (Phases 2–4) in one agentic session: designing the scoring/ranking logic, implementing it in `recommender.py` and `main.py`, expanding the song catalog, stress-testing the recommender with normal and adversarial user profiles, and writing up the findings in `README.md` and `model_card.md`.

**Prompts used:**

- "research and summarize how major streaming platforms predict what users will love next... difference between collaborative filtering and content-based filtering" (grounded the design in how real systems work before writing any code)
- "Identify the main data types involved in these systems" (features vs. behavioral data vs. context)
- "write [the How The System Works paragraph] in my own words" (based on the design reasoning we'd already worked through together)
- "Attach songs.csv and suggest which features would be most effective for a simple content-based recommender"
- "design a math-based Scoring Rule... how to calculate a score for a numerical feature (like energy) that rewards songs that are closer to the user's preference"
- "expand this dataset... generate 5–10 additional songs... diverse range of genres and moods not already present"
- "suggest adversarial or edge case user profiles... designed to see if your scoring logic can be tricked"
- "identify potential filter bubbles or biases in your current scoring logic"
- "generate a commit message to summarize your implementation"

**What did the agent generate or change?**

- `src/recommender.py` — implemented `Song`/`UserProfile` dataclasses (already scaffolded), `Recommender.recommend`/`explain_recommendation`, and the functional `load_songs`/`score_song`/`recommend_songs`, all replacing `# TODO` placeholders.
- `src/main.py` — fixed a broken import, added a `Loaded songs: N` confirmation line, and switched from one hardcoded profile to three named profiles for stress-testing.
- `data/songs.csv` — added 8 songs to cover genres/moods missing from the original 10 (electronic, blues, metal, r&b, folk, classical, reggae, k-pop).
- `README.md` — How The System Works, Sample Recommendation Output, Experiments You Tried, Project Summary, and Reflection sections.
- `model_card.md` — every section (Model Name, Intended Use, How the Model Works, Data, Strengths, Limitations and Bias, Evaluation, Future Work, Personal Reflection).
- Ran `pytest` and `python -m src.main` repeatedly to verify behavior at each step, and ran one-off scripts to test adversarial profiles and a weight-shift experiment without committing throwaway code.
- Created two commits and pushed them to `origin/main`.

**What did you verify or fix manually?**

- I had the agent revert a first pass where it implemented everything in one shot without me engaging with the design reasoning first — I wanted to work through feature selection and the scoring formula myself before the code got written.
- I double-checked that the weighting (genre 2.0 / mood 1.5 / energy up to 1.0 / acousticness up to 0.5) was a stated judgment call, not something the agent presented as objectively "correct" — it wasn't, and that distinction is called out explicitly in the README and model card.
- I caught (via the agent's own re-run) that the README's sample output had gone stale after the catalog grew from 10 to 18 songs, and had it regenerate the real terminal output rather than leaving outdated numbers in place.
- I ran the test suite (`pytest`) and the CLI myself at each stage to confirm claims in the writeup actually matched real program output before letting any of it into a commit.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
