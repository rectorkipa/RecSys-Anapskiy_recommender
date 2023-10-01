import os

import streamlit as st
from dotenv import load_dotenv

from api.omdb import OMDBApi
from recsys import ContentBaseRecSys

from PIL import Image

st.set_page_config(page_title="Anapskiy' RecSys", page_icon=':snake:')

TOP_K = 5
load_dotenv()

API_KEY = os.getenv("API_KEY")
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")

omdbapi = OMDBApi(API_KEY)


recsys = ContentBaseRecSys(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE,
)


img = Image.open("logo.webp")
st.image(img, width=700)

st.markdown(
    "<h1 style='text-align: center; color: brown;'>My Movie Recommender Service</h1>",
    unsafe_allow_html=True
)

selected_data = st.multiselect(
    "Type or select a YEAR(s) you like :",
    recsys.get_data()
)

if selected_data:
    recsys.get_filter_data(selected_data)
    recsys.TfidfVectorizer()


selected_genres = st.multiselect(
    "Type or select a GENRE(s) you like :",
    recsys.get_genres()
)

if selected_genres:
    recsys.get_filter_genres(selected_genres)
    recsys.TfidfVectorizer()


selected_movie = st.selectbox(
    "Type or select a MOVIE you like :",
    recsys.get_title()
)


if st.button('Show My Recommendation!'):
    if selected_movie:
        recommended_movie_names = recsys.recommendation(selected_movie, top_k=TOP_K)
        if len(recommended_movie_names) == 0:
            st.write("Sorry, no recommendations. Please change your query...")
        else:
            st.write("Recommended Movies:")
            recommended_movie_names = recsys.recommendation(selected_movie, top_k=TOP_K)
            recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)
            movies_col = st.columns(len(recommended_movie_names))
            for index, col in enumerate(movies_col):
                with col:
                    st.image(recommended_movie_posters[index])
                    st.subheader(recommended_movie_names[index])

