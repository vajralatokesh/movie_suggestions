import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
API_KEY = "b8a45c0e4399cb242e0c6a486ca2542c"   # <-- PUT YOUR KEY HERE
BASE_URL = "https://api.themoviedb.org/3"

# -----------------------------
# Fetch genre mapping safely
# -----------------------------
def fetch_genres():
    try:
        response = requests.get(
            f"{BASE_URL}/genre/movie/list",
            params={"api_key": API_KEY},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return {g["id"]: g["name"] for g in data["genres"]}
    except requests.exceptions.RequestException as e:
        print("❌ Error fetching genres:", e)
        return {}

genre_map = fetch_genres()

# -----------------------------
# Fetch popular movies safely
# -----------------------------
def fetch_movies(pages=1):   # keep pages=1 for stability
    movies = []
    for page in range(1, pages + 1):
        try:
            response = requests.get(
                f"{BASE_URL}/movie/popular",
                params={"api_key": API_KEY, "page": page},
                timeout=10
            )
            response.raise_for_status()
            movies.extend(response.json()["results"])
        except requests.exceptions.RequestException as e:
            print("❌ Network error while fetching movies:", e)
            break
    return movies

movies = pd.DataFrame(fetch_movies())

if movies.empty:
    print("❌ No movies fetched. Check internet or API key.")
    exit()

# -----------------------------
# Convert genre IDs to names
# -----------------------------
def get_genre_names(ids):
    return [genre_map.get(i, "") for i in ids]

movies["genres"] = movies["genre_ids"].apply(get_genre_names)

# -----------------------------
# Genre-based recommendation
# -----------------------------
def recommend_by_genre(genre_name, top_n=8):
    genre_name = genre_name.lower()
    filtered = movies[movies["genres"].apply(
        lambda g: genre_name in [x.lower() for x in g]
    )]
    return filtered.sort_values(
        "popularity", ascending=False
    )["title"].head(top_n)

# -----------------------------
# Netflix-style genre rows
# -----------------------------
GENRE_SECTIONS = [
    "Action",
    "Comedy",
    "Drama",
    "Romance",
    "Horror",
    "Science Fiction",
    "Thriller",
    "Animation"
]

print("\n🎬 NETFLIX STYLE MOVIE RECOMMENDATIONS\n")

for genre in GENRE_SECTIONS:
    print(f"\n--- {genre} Movies ---")
    result = recommend_by_genre(genre)
    if result.empty:
        print("No movies found.")
    else:
        print(result.to_string(index=False))
