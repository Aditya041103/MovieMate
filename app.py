import pickle
import streamlit as st
import requests
from tenacity import retry, stop_after_attempt, wait_fixed


def fetch_poster(tmdb_id):
    url = "https://api.themoviedb.org/3/movie/"+str(tmdb_id)+"?language=en-US"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MGZhODhiZjNhNzE1ZGVjZjQ5ZDgwYmJlNDdiNTQyNiIsIm5iZiI6MTcyMTI0NDE5Ny4zNjgsInN1YiI6IjY2OTgxYTI1YzU3ZDRhYWM1YTIzMTA5ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.W_ZsJoLnsqqzuMjvWBdrXRAtfD_mmoUOf_W4aYZpESQ"
}


    response = requests.get(url, headers=headers)
    data = response.json()

    if "poster_path" in data:
        if data["poster_path"]:
            return "https://media.themoviedb.org/t/p/w600_and_h900_bestv2"+data["poster_path"]

movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    index = movies[movies['Title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].TMDB_Id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].Title)

    return recommended_movie_names, recommended_movie_posters


st.header('Your Movie Companion')

movie_list = movies['Title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    if recommended_movie_names and recommended_movie_posters:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])


