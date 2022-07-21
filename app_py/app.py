import streamlit as st
import pickle as pkl
import pandas as pd

movies_list = pkl.load(open('movie_data.pkl','rb'))


st.title("Movie Recommendation System")

option = st.selectbox("Select an option", ["Recommendation", "Search"])