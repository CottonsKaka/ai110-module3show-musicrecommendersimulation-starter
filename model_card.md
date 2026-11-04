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

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
