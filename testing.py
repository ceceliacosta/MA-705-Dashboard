import csv

import imdb
ia = imdb.IMDb()

top = ia.get_top250_movies()
with open('testing_file.csv', mode='w', newline= '', encoding= 'utf-8') as testing_file:
    testing_writer = csv.writer(testing_file, delimiter=',')
    testing_writer.writerow(['Title', 'Genres', 'Year', 'Directors', 'Cast', 'Rating'])

    for movie in top:
        id = movie.getID()
        movie_data = ia.get_movie(id)
        # print(movie_data['genres'])
        director_list= []
        for director in movie_data['directors']:
            director_list.append(director['name'])
        cast_list= []
        for cast in movie_data['cast']:
            cast_list.append(cast['name'])

        testing_writer.writerow([movie_data['title'], movie_data['genres'], movie_data['year'], director_list, cast_list, movie_data['rating']])
