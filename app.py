import streamlit as st
import requests
import pandas as pd
import os

# -------------------------------------------------
# BASIC STREAMLIT CHECK (prevents black screen)
# -------------------------------------------------
st.set_page_config(page_title="Movie Recommendation App", layout="wide")
st.title("🎬 Movie Recommendation System")
st.write("genre-based movie recommendations")

# -------------------------------------------------
# API CONFIG (SECURE)
# -------------------------------------------------
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

if not API_KEY:
    st.error("❌ TMDB API key not found. Please set it in Streamlit Secrets.")
    st.stop()

# -------------------------------------------------
# GENRE NAME → TMDB GENRE ID
# -------------------------------------------------
GENRE_ID_MAP = {
    "Action": 28,
    "Comedy": 35,
    "Drama": 18,
    "Romance": 10749,
    "Horror": 27,
    "Science Fiction": 878,
    "Animation": 16,
    "Thriller": 53
}

# -------------------------------------------------
# FETCH MOVIES BY GENRE (SAFE)
# -------------------------------------------------
def fetch_movies_by_genre(genre_id, pages=2):
    movies = []

    for page in range(1, pages + 1):
        try:
            response = requests.get(
                f"{BASE_URL}/discover/movie",
                params={
                    "api_key": API_KEY,
                    "with_genres": genre_id,
                    "page": page,
                    "sort_by": "popularity.desc"
                },
                timeout=10
            )
            response.raise_for_status()

            for m in response.json().get("results", []):
                movies.append({
                    "title": m.get("title", "N/A"),
                    "overview": m.get("overview", ""),
                    "popularity": m.get("popularity", 0),
                    "release_date": m.get("release_date", "N/A")
                })

        except Exception as e:
            st.warning("⚠️ Network issue while fetching movies. Showing available data.")
            break

    return pd.DataFrame(movies)

# -------------------------------------------------
# UI: GENRE SELECTION
# -------------------------------------------------
selected_genre = st.selectbox(
    "Select a Genre",
    list(GENRE_ID_MAP.keys())
)

st.write(f"Showing movies for: **{selected_genre}**")

# -------------------------------------------------
# FETCH & DISPLAY MOVIES
# -------------------------------------------------
movies_df = fetch_movies_by_genre(GENRE_ID_MAP[selected_genre], pages=2)

if movies_df.empty:
    st.info("No movies found for this genre.")
else:
    movies_df = movies_df.sort_values("popularity", ascending=False)

    for _, row in movies_df.iterrows():
        st.markdown(f"### 🎥 {row['title']}")
        st.write(f"📅 Release Date: {row['release_date']}")
        st.write(row["overview"])
        st.divider()
