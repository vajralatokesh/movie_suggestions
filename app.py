import streamlit as st
import requests
import os

# -------------------------------------------------
# BASIC PAGE SETUP
# -------------------------------------------------
st.set_page_config(page_title="OTT Content Explorer", layout="wide")
st.title("🎬 OTT Content Explorer")
st.write("Movies • TV Shows • All Languages • One Place")

# -------------------------------------------------
# TMDB API CONFIG (SECURE)
# -------------------------------------------------
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

if not API_KEY:
    st.error("TMDB API key not found. Please add it in Streamlit Secrets.")
    st.stop()

# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------

# Fetch trending movies + TV shows
def fetch_trending():
    url = f"{BASE_URL}/trending/all/week"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json().get("results", [])

# Search movies + TV shows (all languages)
def search_content(query):
    url = f"{BASE_URL}/search/multi"
    params = {
        "api_key": API_KEY,
        "query": query
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json().get("results", [])

# Display content neatly (text-only, simple)
def display_content(items):
    if not items:
        st.info("No results found.")
        return

    for item in items:
        title = item.get("title") or item.get("name")
        media_type = item.get("media_type", "").upper()
        language = item.get("original_language", "N/A")
        rating = item.get("vote_average", "N/A")
        overview = item.get("overview", "")

        st.markdown(f"### 🎥 {title}")
        st.write(f"**Type:** {media_type} | **Language:** {language} | ⭐ {rating}")
        st.write(overview)
        st.divider()

# -------------------------------------------------
# UI LOGIC
# -------------------------------------------------

search_query = st.text_input(
    "🔍 Search movies or TV shows (any language)",
    placeholder="Type a movie or TV show name..."
)

if search_query:
    st.subheader(f"Search Results for: {search_query}")
    results = search_content(search_query)
    display_content(results)
else:
    st.subheader("🔥 Trending Now")
    trending_items = fetch_trending()
    display_content(trending_items)
