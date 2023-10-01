from typing import List, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from .utils import parse
import streamlit as st

@st.cache_data
def _load_base(path: str, index_col: str = 'id') -> pd.DataFrame:
    """Load CSV file to pandas.DataFrame"""
    return pd.read_csv(path, index_col=index_col)


class ContentBaseRecSys:

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        self.distance = _load_base(distance_filepath, index_col='id')
        self.distance.index = self.distance.index.astype(int)
        self.distance.columns = self.distance.columns.astype(int)
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath) -> None:
        self.movies = _load_base(movies_dataset_filepath, index_col='id')
        self.movies.index = self.movies.index.astype(int)
        self.movies['genres'] = self.movies['genres'].apply(parse)

    def get_title(self) -> List[str]:
        return self.movies['title_x'].values

    def get_genres(self) -> Set[str]:
        genres = [item for sublist in self.movies['genres'].values.tolist() for item in sublist]
        return set(genres)

    def get_data(self) -> Set[int]:
        return self.movies['date'].sort_values(ascending=False).dropna().unique().astype(int)

    def get_filter_data(self, selected_data: int):
        self.movies = self.movies.query('date in @selected_data')

    def get_filter_genres(self, selected_genres: str):
        self.movies = self.movies[self.movies['genres_filtered'].str.contains('|'.join(selected_genres), na=False)]

    def TfidfVectorizer(self):
        vectorizer = TfidfVectorizer(max_features=10000, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(self.movies['overview_keywords'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        self.distance = pd.DataFrame(cosine_sim, index=self.movies.index, columns=self.movies.index)

    def recommendation(self, title: str, top_k: int = 5) -> List[str]:
        """
        Returns the names of the top_k most similar movies with the movie "title"
        """
        movie_index = pd.Series(self.movies.index, index=self.movies['title_x'])
        index = movie_index[title]
        similar_movies = list(enumerate(self.distance[index]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1: top_k+1]
        top_index = [score[0] for score in sorted_similar_movies]
        top_k_movies = self.movies['title_x'].iloc[top_index].values.tolist()
        return top_k_movies
