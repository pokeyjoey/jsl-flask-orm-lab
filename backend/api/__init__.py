from .models.movie import Movie
from .models.actor import Actor
from .models.movie_actor import MovieActor
from flask import Flask, jsonify
from api.lib.db import get_db, find_all, find


def create_app(database, user, password):
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE=database,
        DB_USER=user,
        DB_PASSWORD=password
    )

    @app.route('/')
    def home():
        return "Welcome to the movies api"

    @app.route('/actors')
    def actors():
        db = get_db()
        actors = find_all(Actor, db)

        return [actor.__dict__ for actor in actors]

    @app.route('/actors/<id>')
    def actor(id):
        db = get_db()
        actor = find(Actor, id,  db)

        return jsonify(actor.__dict__)

    @app.route('/movies')
    def movies():
        db = get_db()
        movies = find_all(Movie, db)

        return [movie.__dict__ for movie in movies]

    @app.route('/movies/<id>')
    def movie(id):
        db = get_db()
        movie = find(Movie, id,  db)

        return jsonify(movie.__dict__)

    return app
