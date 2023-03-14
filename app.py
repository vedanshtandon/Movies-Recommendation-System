import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests



def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6f8df2c7bce17353a6c97833cc7f35bc'.format(movie_id))
    data=response.json()
    return "http://image.tmdb.org/t/p/w500/"+data['poster_path']



# movie_list   =>   it is the original data frame conatining  MOVIE_ID | TITLE |  TAGS value
# similarity   =>   it is a  n*n  matrix containing the  similarity  cosines of the all possible movies
 
movie_list=pickle.load(open('movies.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movie_names=movie_list.title


def recommendations(movie):
    movie_index=movie_list[movie_list['title']==movie].index[0]
    L=sorted(list(enumerate(similarity[movie_index])),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_posters=[]
    for i in L:
        id=movie_list.iloc[i[0]].movie_id
        recommended_movies.append(movie_list.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(id))
        print(recommended_movies)
    return recommended_movies,recommended_posters




api_key="6f8df2c7bce17353a6c97833cc7f35bc"

st.title("Movie Recommender System")
st.header('Select a type of movie you have already watched')
option = st.selectbox(
    '',
    (movie_names))


if st.button('Recommend'):
    names,posters=recommendations(option)
    for i in range(5):
        st.header(names[i-1])
        st.image(posters[i-1])
