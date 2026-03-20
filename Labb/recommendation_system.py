"""
Movie Recommendation System
----------------------------
Content-based filtering using genre one-hot encoding and
K-Nearest Neighbours with cosine similarity.
 
Usage

As a module:
    from recommendation_system import recommendation
    recs = recommendation("Fight Club (1999)", n=5)
 
As a script:
    python recommendation_system.py

A dash app is created to accompany this .py file for more interactive use. See "app.py"
"""

import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Data loading
movies = pd.read_csv("ml-latest/movies.csv")

# Exclude movies with no genres, cannot be used in the recommendation system
# as they would only cluster together by default
movies = movies[movies["genres"] != "(no genres listed)"].reset_index(drop=True)

# One-hot encoding, creates a binary column for each genre
genres = movies["genres"].str.get_dummies(sep="|")

# Model training using KNN with cosine similarity and brute-force search
model = NearestNeighbors(metric="cosine", algorithm="brute")
model.fit(genres)

# Code that returns n=5 movie recommendations based on genre similarity, added an "except" to catch IndexError
# if movie is not found
def recommendation(movie_title, n=5):
    try:
        movie_index = movies[movies["title"] == movie_title].index[0]
    except IndexError:
        return ["Movie not found"]
    
    distances, indices = model.kneighbors(
        genres.iloc[movie_index].values.reshape(1, -1),
        n_neighbors = n + 1
    )

    recs = movies.iloc[indices[0][1:]]["title"].tolist()
    return recs

# Main program
if __name__ == "__main__":
    movie = input("Enter a movie you like: ")
    recs = recommendation(movie)

    print("\nRecommended movies:")
    for r in recs:
        print(r)