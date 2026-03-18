# Dash UI

import dash
from dash import dcc, html, Input, Output, State
import pandas as pd

from recommendation_system import recommendation

# Load movie titles
movies = pd.read_csv("Labb/ml-latest/movies.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    
    html.H1("Movie Recommendation System", 
            style={"textAlign": "center"}
            ),

    html.P("Search for a movie you like:",
           style={"textAlign": "center"}
           ),

    dcc.Dropdown(
        id="movie-dropdown",
        options=[],
        placeholder="Type to search movie..."
    ),

    html.Button("Recommend me!", id="btn", style={
        "textAlign": "center",
            "width": "100%",
            "padding": "10px",
            "background": "darkgreen",
            "color": "white",
            "fontSize": "16px",
            "cursor": "pointer"
        }, ),

    html.H3("Recommended Movies:",
            style={"marginTop": "30px"}
            ),

    html.Ul(id="output-list")

])


# Dynamic dropdown search
@app.callback(
    Output("movie-dropdown", "options"),
    Input("movie-dropdown", "search_value")
)
def update_dropdown(search_value):

    if not search_value:
        return []

    filtered = movies[movies["title"].str.contains(search_value, case=False)]

    return [
        {"label": row["title"], "value": row["title"]}
        for _, row in filtered.head(20).iterrows()
    ]


# Recommendation callback
@app.callback(
    Output("output-list", "children"),
    Input("btn", "n_clicks"),
    State("movie-dropdown", "value")
)
def show_recommendations(n_clicks, movie_title):

    if n_clicks is None or movie_title is None:
        return []

    recs = recommendation(movie_title)

    return [html.Li(movie) for movie in recs]


if __name__ == "__main__":
    app.run(debug=True)