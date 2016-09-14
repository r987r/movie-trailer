#!/usr/bin/env python

import json    # For debugging json prints.
import fresh_tomatoes
import tmdbsimple as tmdb

tmdb.API_KEY = '65992653354d8113805cb2a26a54c933'

class Movie:
    def __init__(self, title, poster_image_num, trailer_youtube_id):
        self.title = title
        self.poster_image_url = Movie.poster_base_url + poster_image_num
        self.trailer_youtube_id = trailer_youtube_id

    @classmethod
    def make_movie(cls, movieTitle):
        # Return movie object if we find a match in theMovieDb Database, otherwise 
        # return None.

        search = tmdb.Search()
        response = search.movie(query=movieTitle)
        if(not len(search.results)):
            print "movie not found:" + movieTitle
            return None

        s = search.results[0]
        s = tmdb.Movies(s['id'])
        s.info()    # retrieve basic information
        s.videos()  # retrieve video information

        youtube_key = ""
        for videos in s.results:
            if(videos['type'] == "Trailer" and videos['site'] == "YouTube"):
                youtube_key = videos['key']
                break
        
        #print json.dumps(s.__dict__) 
        
        if(response):
            return Movie(s.title, s.poster_path, youtube_key)
        else:
            return None
        
def initOnce():
    # get the base_url used for full poster url.
    s = tmdb.Configuration().info()
    Movie.poster_base_url = s['images']['base_url'] + "original"

initOnce();
movies = { Movie.make_movie("The Force Awakens"),
        Movie.make_movie("Bourne Iden"),
        Movie.make_movie("Slumdog"),
        Movie.make_movie("Warcraft") }
fresh_tomatoes.open_movies_page(movies)
