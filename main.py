import pandas as pd 
import numpy as np

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# print(movies.head(2))
# print(credits.head(2))

movies = movies.merge(credits , on='title') # this helps us to merge the two datasets
# print(movies)

movies = movies[["movie_id" , "title" , 'overview' , 'genres' , 'keywords' , 'cast' , 'crew']]
print(movies.head(2))


# print(movies.isnull().sum()) # this will show the number of null values in each column
movies.dropna(inplace = True)

# print(movies.duplicated().sum()) # this will show the number of duplicated values in each column

# print(movies.iloc[0].genres)


# [{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]
# we have to convert it into [Action ,Adventure, Fantasy,  Science Fiction] in this way of list

# for that we have to run loop on it
import ast
def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

# import ast
# print(ast.literal_eval({"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}))

print(movies['genres'].apply(convert))

movies['genres'] = movies['genres'].apply(convert)

movies.head()



movies['keywords'] = movies['keywords'].apply(convert) #

def convert3(obj):
    L=[]
    counter =0
    for i in ast.literal_eval(obj):
        if counter!= 3:
            L.append(i['name'])
            counter= counter+1
        else:
            break
    return L

movies['cast'] = movies['cast'].apply(convert3)


def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job'] ==['Director']:
            L.append(i['name'])
        else:
            break
    return L