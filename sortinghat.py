import streamlit as st
import pandas as pd
import altair as alt
from collections import Counter
import random

# -------------------
# House definitions
# -------------------
HOUSES = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]

# -------------------
# Questions with dynamic scoring
# Each option maps to a dict: {house: points, ...}
# -------------------
QUESTIONS = [
    {
        "q": "Hi",
        "opts": [
            ("A",
             {"Gryffindor": 2, "Slytherin": 1}),
            ("B",
             {"Ravenclaw": 2, "Gryffindor": 1}),
            ("C",
             {"Hufflepuff": 2, "Ravenclaw": 1}),
            ("D",
             {"Slytherin": 2, "Hufflepuff": -1}),
        ],
    },
    {
        "q": "Hi",
        "opts": [
            ("A",
             {"Gryffindor": 2, "Slytherin": 1}),
            ("B",
             {"Ravenclaw": 2, "Gryffindor": 1}),
            ("C",
             {"Hufflepuff": 2, "Ravenclaw": 1}),
            ("D",
             {"Slytherin": 2, "Hufflepuff": -1}),
        ],
    },
    {
        "q": "Hi",
        "opts": [
            ("A",
             {"Gryffindor": 2, "Slytherin": 1}),
            ("B",
             {"Ravenclaw": 2, "Gryffindor": 1}),
            ("C",
             {"Hufflepuff": 2, "Ravenclaw": 1}),
            ("D",
             {"Slytherin": 2, "Hufflepuff": -1}),
        ],
    },
]

# -------------------
# Helper functions
# -------------------
def score_answers(selected_options):
    """Take selected options (list of scoring dicts) and sum up house points."""
    scores = Counter()
    for option in selected_options:
        for house, pts in option.items():
            scores[house] += pts
    return scores


def determine_house(counts):
    """Return final house and tie list if any."""
    if not counts:
        return None, []
    max_points = max(counts.values())
    top = [h for h, v in counts.items() if v == max_points]
    if len(top) == 1:
        return top[0], top
    return random.choice(top), top


# -------------------
# Streamlit app
# -------------------
st.set_page_config(page_title="Sorting Hat LMAO", page_icon="🧙‍♂️")
st.title("🧙‍♂️ SORTING HAT")
st.write("Answer the following questions")

answers = []

# Render questions
for i, q in enumerate(QUESTIONS, 1):
    st.subheader(f"Q{i}. {q['q']}")
    choice = st.radio(
        "Choose one:",
        [opt[0] for opt in q["opts"]],
        key=f"q{i}"
    )
    # Find the scoring dict for the selected choice
    for text, score_dict in q["opts"]:
        if text == choice:
            answers.append(score_dict)
    st.write("---")

# Submit button
if st.button("Reveal My House"):
    counts = score_answers(answers)
    house, tied = determine_house(counts)

    # Results
    st.header("You belong in...")
    st.subheader(f" {house}!")

        # Show scores
    st.write("### Your House Scores:")
    df_scores = pd.DataFrame({
        "House": HOUSES,
        "Score": [counts.get(h, 0) for h in HOUSES]
    })

    # Define Hogwarts house colors
    house_colors = {
        "Gryffindor": "#7F0909",   # Dark Red
        "Slytherin": "#1A472A",    # Green
        "Ravenclaw": "#0E1A40",    # Blue
        "Hufflepuff": "#EEE117"    # Yellow/Gold
    }

    chart = alt.Chart(df_scores).mark_bar().encode(
        x=alt.X("House", sort=HOUSES),
        y="Score",
        color=alt.Color("House", scale=alt.Scale(domain=list(house_colors.keys()),
                                                 range=list(house_colors.values())))
    ).properties(width=500, height=300)

    st.altair_chart(chart)

