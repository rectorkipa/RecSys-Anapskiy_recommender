import requests
from typing import Optional, List
import ast


class OMDBApi:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://www.omdbapi.com"

    def _images_path(self, title: str) -> Optional[str]:
        response = requests.get(f"{self.url}/?apikey={self.api_key}&t={title}")
        if (ast.literal_eval(response.text)['Response'] == 'True'):
            imdbID = ast.literal_eval(response.text)['imdbID']
            url = f"{self.url.replace('www', 'img')}/?apikey={self.api_key}&i={imdbID}"
            if requests.get(url).status_code == 200:
                return url

    def get_posters(self, titles: List[str]) -> List[str]:
        posters = []
        for title in titles:
            path = self._images_path(title)
            if path:  # If image isn`t exist
                posters.append(path)
            else:
                posters.append('assets/none.jpeg')  # Add plug

        return posters 
