from flask import Flask, render_template, request, jsonify
import pickle
import requests

app = Flask(__name__)

# Load movie data and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDB API Key (Keep it safe, use env variables in production)
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MGZhODhiZjNhNzE1ZGVjZjQ5ZDgwYmJlNDdiNTQyNiIsIm5iZiI6MTcyMTI0NDE5Ny4zNjgsInN1YiI6IjY2OTgxYTI1YzU3ZDRhYWM1YTIzMTA5ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.W_ZsJoLnsqqzuMjvWBdrXRAtfD_mmoUOf_W4aYZpESQ"


def fetch_poster(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if "poster_path" in data and data["poster_path"]:
        return f"https://media.themoviedb.org/t/p/w600_and_h900_bestv2{data['poster_path']}"
    return None


def recommend(movie):
    try:
        index = movies[movies['Title'] == movie].index[0]
    except IndexError:
        return [], []  # If movie not found

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].TMDB_Id
        recommended_movie_names.append(movies.iloc[i[0]].Title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = None
    selected_movie = None

    if request.method == "POST":
        selected_movie = request.form["movie"]
        movie_names, movie_posters = recommend(selected_movie)
        recommendations = zip(movie_names, movie_posters)

    return render_template("index.html", movies=movies['Title'].values, recommendations=recommendations, selected_movie=selected_movie)


if __name__ == "__main__":
    app.run(debug=True)
