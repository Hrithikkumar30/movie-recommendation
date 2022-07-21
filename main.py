from turtle import distance
import pandas as pd 
import numpy as np

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# print(movies.head(2))
# print(credits.head(2))

movies = movies.merge(credits , on='title') # this helps us to merge the two datasets
# print(movies)

movies = movies[["movie_id" , "title" , 'overview' , 'genres' , 'keywords' , 'cast' , 'crew']]
# print(movies.head(2))


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

# print(movies['genres'].apply(convert))

movies['genres'] = movies['genres'].apply(convert)

movies.head()



movies['keywords'] = movies['keywords'].apply(convert) #


# import ast
# print(ast.literal_eval({"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}))

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
        if i['job'] =='Director':
            L.append(i['name'])
          
            break
    return L
movies['crew'] = movies['crew'].apply(fetch_director) 
# print(movies['crew'].apply(fetch_director) )

# new_df = movies.copy()
# print (new_df.head(2))


movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ","") for i in x])
movies['keywords']= movies['keywords'].apply(lambda x: [i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ","")for i in x])
movies['crew']= movies['crew'].apply(lambda x: [i.replace(" ","")for i in x])

movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(lambda x: " ".join(x))
movies['keywords'] = movies['keywords'].apply(lambda x: " ".join(x))
movies['cast'] = movies['cast'].apply(lambda x: " ".join(x))
movies['crew'] = movies['crew'].apply(lambda x: " ".join(x))


movies['tags'] = movies['overview']+ movies['genres'] + movies[ 'keywords'] + movies['cast'] + movies['crew']

# print(movies.head(2))
new_df = movies[['movie_id' , 'title' , 'tags']]


# new_df = movies.drop(columns=['overview' , 'genres' , 'keywords' , 'cast' , 'crew'])
# new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x)) #this will join all the tags in one column

new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
# print(new_df.head(2))

#text Vectorization
from sklearn.feature_extraction.text import CountVectorizer 
CV = CountVectorizer(max_features=5000 ,  stop_words='english')
vectors = CV.fit_transform(new_df['tags']).toarray()
# print(CV.get_feature_names())

from sklearn.metrics.pairwise import cosine_similarity
simalirity = cosine_similarity(vectors)

# print(simalirity.shape)

def recommendations(movie):
    movie_index = new_df[new_df['title']==movie].index[0]
    distance = simalirity[movie_index]
    movies_list = sorted(enumerate(distance), key=lambda x: x[1], reverse=True)[1:6]
    for i in movies_list:
        # print(i[0])
        print(new_df['title'][i[0]])
        
recommendations('The Dark Knight')