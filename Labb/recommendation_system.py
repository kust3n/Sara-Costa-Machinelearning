import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Ladda data
movies = pd.read_csv("Labb/ml-latest/movies.csv")

# One-hot encoding, skapa matris av varje genre
genres = movies["genres"].str.get_dummies(sep="|")

# Model training
model = NearestNeighbors(metric="cosine", algorithm="brute")
model.fit(genres)

def recommendation(movie_title, n=5):
    try:
        movie_index = movies[movies["title"] == movie_title].index[0]
    except IndexError:
        return ["Movie not found"]
    
    distances, indices = model.kneighbors(
        genres.iloc[movie_index].values.reshape(1, -1),
        n_neighbors = n + 1
    )

    recs = movies.iloc[indices[0][1:]]['title'].tolist()
    return recs