import streamlit as st
import pandas as pd
import pickle
import requests

# Load the movies data and similarity matrix
movies_list = pickle.load(open('movies_dict (1).pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open("similarity (3).pkl", "rb"))


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3ea2433457b8518d707a0616f19a3cde&language=en-US"
        response = requests.get(url)
        response.raise_for_status()  # This will raise an exception for bad HTTP codes
        data = response.json()
        
        poster_path = data.get('poster_path')
        if not poster_path:
            # Poster not available
            return "https://via.placeholder.com/500x750?text=No+Poster"
        
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except Exception as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster"

# Movie recommendation logic
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return [], []
    
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# Streamlit UI
st.title(" Film Recommendation System")
st.write("Get movie recommendations based on a film you liked.")

selected_movie = st.selectbox(
    "Which movie have you watched?",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    
    if not names:
        st.error("No recommendations found. Please check your movie data.")
    else:
        st.write("You selected:", selected_movie)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.write(names[i])
                if posters[i]:
                    st.image(posters[i])
                else:
                    st.write("Poster not available.")
else:
    st.write("Please select a movie to get recommendations.")