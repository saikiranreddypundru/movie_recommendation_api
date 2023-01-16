from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np 
import ast
app = Flask(__name__)
api = Api(app)

@app.route('/top', methods=['GET'])
def home():
    genre = request.args.get('genre', default="")
    df1=pd.read_csv("/tmdb_5000_credits.csv")
    df2=pd.read_csv("/tmdb_5000_movies.csv")
    df1.columns = ['id','title','cast','crew']
    df2= df2.merge(df1,on='id')

    regex = '.*' + genre
    df3 = df2[df2.genres.str.match(regex)]

    C= df3['vote_average'].mean()
    m= df3['vote_count'].quantile(0.9)
    q_movies = df3.copy().loc[df3['vote_count'] >= m]
    def weighted_rating(x, m=m, C=C):
        v = x['vote_count']
        R = x['vote_average']
        # Calculation based on the IMDB formula
        return (v/(v+m) * R) + (m/(m+v) * C)
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
    q_movies = q_movies.sort_values('score', ascending=False)
    pop= df3.sort_values('popularity', ascending=False)
    return jsonify(list(pop['id'][0:10]))
app.run(port=80)