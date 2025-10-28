import pickle
import streamlit as st
import requests
import streamlit.components.v1 as components

# ----------------- Streamlit Config -----------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide", page_icon="🍿")

# ----------------- TMDB CONFIG -----------------
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
TMDB_IMG_BASE_ORIG = "https://image.tmdb.org/t/p/original"
TMDB_IMG_BASE_W500 = "https://image.tmdb.org/t/p/w500"

# ----------------- Load Pickles -----------------
@st.cache_data(show_spinner=False)
def load_data():
    with open("movie_list.pkl", "rb") as f:
        movies = pickle.load(f)
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
    return movies, similarity


movies, similarity = load_data()

# ----------------- Helper: Fetch Image -----------------
@st.cache_data(ttl=60 * 60)
def get_best_image_for_title(title):
    try:
        q = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={requests.utils.requote_uri(title)}",
            timeout=6,
        ).json()
        results = q.get("results", [])
        if results:
            poster = results[0].get("backdrop_path") or results[0].get("poster_path")
            if poster:
                return TMDB_IMG_BASE_ORIG + poster
    except Exception:
        pass
    return None


# ----------------- Banner Data -----------------
BANNER_TITLES = ["Avatar", "Spider-Man", "Inception", "Iron Man", "Interstellar"]


@st.cache_data(ttl=60 * 30)
def prepare_banner_images():
    imgs = []
    for title in BANNER_TITLES:
        url = get_best_image_for_title(title)
        if not url:
            url = TMDB_IMG_BASE_ORIG + "/qNBAXBIQlnOThrVvA6mA2B5ggV6.jpg"
        imgs.append({"title": title, "poster": url})
    return imgs


banners = prepare_banner_images()

# ----------------- Banner Renderer -----------------
def render_banner(images):
    html = f"""
    <html>
    <head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    body {{
      margin: 0;
      font-family: 'Poppins', sans-serif;
      overflow: hidden;
    }}
    .hero-container {{
      position: relative;
      width: 100%;
      height: 500px;
      overflow: hidden;
      border-radius: 16px;
      box-shadow: 0px 8px 25px rgba(0,0,0,0.6);
    }}
    .hero-slide {{
      position: absolute;
      width: 100%;
      height: 100%;
      opacity: 0;
      transition: opacity 1.5s ease-in-out;
    }}
    .hero-slide img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    .hero-slide.active {{
      opacity: 1;
      z-index: 1;
    }}
    .hero-overlay {{
      position: absolute;
      inset: 0;
      background: linear-gradient(180deg, rgba(0,0,0,0.25) 0%, rgba(0,0,0,0.65) 60%, rgba(0,0,0,0.95) 100%);
      z-index: 2;
    }}
    .hero-heading {{
      position: absolute;
      bottom: 25%;
      left: 50%;
      transform: translateX(-50%);
      color: #ffffff;
      font-size: 2.8rem;
      font-weight: 700;
      text-shadow: 0 0 25px rgba(255,255,255,0.4);
      z-index: 3;
      text-align: center;
      letter-spacing: 1px;
    }}
    .hero-title {{
      position: absolute;
      bottom: 10%;
      left: 50%;
      transform: translateX(-50%);
      color: #f8f8f8;
      font-size: 1.4rem;
      font-weight: 500;
      text-shadow: 0 0 15px rgba(255,255,255,0.3);
      z-index: 3;
      text-align: center;
    }}
    </style>
    </head>
    <body>
    <div class="hero-container">
    """

    for i, b in enumerate(images):
        active = "active" if i == 0 else ""
        html += f'<div class="hero-slide {active}"><img src="{b["poster"]}" alt="{b["title"]}"></div>'

    html += """
      <div class="hero-overlay"></div>
      <div class="hero-heading">🎬 Movie Recommender System</div>
      <div id="movieTitle" class="hero-title"></div>
    </div>
    <script>
    const slides = document.getElementsByClassName('hero-slide');
    const titles = """ + str([b["title"] for b in images]) + """;
    const titleElem = document.getElementById('movieTitle');
    let index = 0;
    const total = slides.length;

    function changeSlide() {
      slides[index].classList.remove('active');
      index = (index + 1) % total;
      slides[index].classList.add('active');
      titleElem.textContent = titles[index];
    }

    titleElem.textContent = titles[0];
    setInterval(changeSlide, 3000);
    </script>
    </body>
    </html>
    """
    components.html(html, height=520)


# Render the banner
render_banner(banners)

# ----------------- Page CSS (with hover effect) -----------------
st.markdown(
    """
<style>
body { background: #0b0f13; color: #e6eef8; }

/* Movie Card */
.movie-card {
  width: 160px;
  text-align: left;
  font-size: 14px;
  margin-bottom: 20px;
  border-radius: 14px;
  overflow: hidden;
  transition: all 0.3s ease;
}

/* Poster image */
.movie-card img {
  width: 100%;
  height: 240px;
  object-fit: cover;
  border-radius: 14px;
  box-shadow: 0 8px 26px rgba(0,0,0,0.6);
  transition: transform 0.4s ease, box-shadow 0.4s ease;
}

/* Title */
.movie-card .title {
  min-height: 44px;
  margin-top: 8px;
  color: #e6eef8;
  font-weight: 600;
  text-align: center;
  transition: color 0.3s ease;
}

/* Hover effects */
.movie-card:hover {
  transform: translateY(-6px) scale(1.05);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.75);
}

.movie-card:hover img {
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
}

.movie-card:hover .title {
  color: #00e0ff;
}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------- Search Bar -----------------
movie_list = movies["title"].values
selected_movie = st.selectbox(
    " ",
    options=[""] + list(movie_list),
    format_func=lambda x: "🔍 Search for movie" if x == "" else x,
)

# ----------------- Recommend Logic -----------------
def fetch_poster_by_id(movie_id):
    if not movie_id:
        return None
    try:
        resp = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}",
            timeout=5,
        ).json()
        path = resp.get("poster_path")
        if path:
            return TMDB_IMG_BASE_W500 + path
    except Exception:
        pass
    return None


def recommend_local(movie, movies_df, similarity_matrix, top_n=15):
    try:
        index = movies_df[movies_df["title"] == movie].index[0]
    except Exception:
        return [], []
    distances = sorted(
        list(enumerate(similarity_matrix[index])),
        reverse=True,
        key=lambda x: x[1],
    )
    names, posters = [], []
    for i in range(1, top_n + 1):
        idx = distances[i][0]
        title = movies_df.iloc[idx].title
        mid = (
            movies_df.iloc[idx].movie_id
            if "movie_id" in movies_df.columns
            else None
        )
        names.append(title)
        posters.append(fetch_poster_by_id(mid))
    return names, posters


# ----------------- Display Recommendations -----------------
if st.button("Show Recommendations 🎥"):
    names, posters = recommend_local(selected_movie, movies, similarity, top_n=15)
    for i in range(0, len(names), 5):
        cols = st.columns(5)
        for j, col in enumerate(cols):
            if i + j < len(names):
                with col:
                    st.markdown(
                        f"<div class='movie-card'><div class='title'>{names[i+j]}</div>",
                        unsafe_allow_html=True,
                    )
                    if posters[i + j]:
                        st.image(posters[i + j], use_container_width=True)
                    else:
                        st.markdown(
                            "<div style='height:225px;background:#111;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#aaa;'>No Image</div>",
                            unsafe_allow_html=True,
                        )
                    st.markdown("</div>", unsafe_allow_html=True)
