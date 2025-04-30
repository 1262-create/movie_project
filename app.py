import streamlit as st
import pandas as pd
import pickle
import gdown
import requests
import os

# Download similarity.pkl if it doesn't exist
if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/uc?id=1JUYDtsg0lrMnKONOtPEKPKUXFtlaD8UJ", "similarity.pkl", quiet=False)

# Download movie.pkl if it doesn't exist
if not os.path.exists("movie.pkl"):
    gdown.download("https://drive.google.com/uc?id=YOUR_MOVIE_PKL_ID", "movie.pkl", quiet=False)

# Load files
movie_list = pd.read_pickle("movie.pkl")
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

st.title('🎬 Movie Recommendation App')


def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=dcde7a8f0ff576296de9da829900d767&language=en-US'
    data = requests.get(url).json()
    path = data.get('poster_path', "")
    return f"https://image.tmdb.org/t/p/w500/{path}" if path else ""


def recommend(movie_name):
    index = movie_list[movie_list['title'] == movie_name].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    titles, posters = [], []
    for i in distances[1:11]:
        titles.append(movie_list.iloc[i[0]].title)
        posters.append(fetch_poster(movie_list.iloc[i[0]].id))
    return titles, posters


movie_titles = movie_list['title'].values
st.markdown("## **Select a Movie**")
selected_movie = st.selectbox('', movie_titles)

if st.button('Recommend Movies'):
    recommended_titles, recommended_posters = recommend(selected_movie)

    for row in range(2):  # 2 rows
        cols = st.columns(5)
        for i in range(5):
            idx = row * 5 + i
            with cols[i]:
                st.markdown(f"**{recommended_titles[idx]}**")
                st.image(recommended_posters[idx], use_container_width=True)
