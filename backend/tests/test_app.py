import pytest
from flask import json
from api import create_app
from api.lib.db import (get_db, close_db, drop_all_tables,
 save, test_conn, test_cursor)
from api.models import Movie, Actor, MovieActor
from tests.models.test_actor import actor

@pytest.fixture(scope = 'module')
def app():
    flask_app = create_app('imdb_test', 'postgres', 'postgres')


    with flask_app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        drop_all_tables(conn, cursor)
        build_records(conn, cursor)

        conn.commit()
        close_db()
    yield flask_app

    with flask_app.app_context():
        close_db()
        conn = get_db()
        cursor = conn.cursor()
        drop_all_tables(conn, cursor)

        close_db()


def build_records(conn, cursor):
    shawshank = Movie(title = 'Shawshank')
    saved_shawshank = save(shawshank, test_conn, test_cursor)

    bull_durham = Movie(title = 'Bull Durham')
    saved_bull_durham = save(bull_durham, test_conn, test_cursor)


    robbins = Actor(name = 'Tim Robbins')
    saved_robbins = save(robbins, test_conn, test_cursor)

    morgan_freeman = Actor(name = 'Morgan Freeman')
    saved_freeman = save(morgan_freeman, test_conn, test_cursor)

    m_a_1 = MovieActor(actor_id = saved_robbins.id, movie_id = saved_shawshank.id)
    save(m_a_1, test_conn, test_cursor)

    m_a_3 = MovieActor(actor_id = saved_robbins.id, movie_id = saved_bull_durham.id)
    save(m_a_3, test_conn, test_cursor)
    m_a_2 = MovieActor(actor_id = saved_freeman.id, movie_id = saved_shawshank.id)
    save(m_a_2, test_conn, test_cursor)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_root_url(app, client):
    response = client.get('/')
    assert b'Welcome to the movies api' in response.data

def test_actors_index_displays_the_name_and_id_of_each_actor(app, client):
    response = client.get('/actors')
    actors_json = json.loads(response.data)

    assert len(actors_json) == 2
    actor_names = [actor['name'] for actor in actors_json]
    assert actor_names == ['Tim Robbins', 'Morgan Freeman']


def test_movies_index_displays_the_name_and_id_of_each_movie(app, client):
    response = client.get('/movies')
    movies_json = json.loads(response.data)

    assert len(movies_json) == 2
    movie_titles = [movie['title'] for movie in movies_json]
    assert movie_titles == ['Shawshank', 'Bull Durham']

def test_movies_show_displays_the_name_and_id_of_the_movie(app, client):
    test_cursor.execute('SELECT id FROM movies where title = %s;', ('Bull Durham',))
    id = test_cursor.fetchone()[0]
 
    response = client.get(f'/movies/{id}')
    movie_json = json.loads(response.data)
    assert movie_json['id'] == id
    assert movie_json['title'] == 'Bull Durham'


def test_actors_show_displays_the_name_and_id_of_the_actor(app, client):
    test_cursor.execute('SELECT id FROM actors where name = %s;', ('Morgan Freeman',))
    id = test_cursor.fetchone()[0]

    response = client.get(f'/actors/{id}')
    actor_json = json.loads(response.data)
    assert actor_json['id'] == id
    assert actor_json['name'] == 'Morgan Freeman'

def test_actors_show_displays_related_movies(app, client):
    test_cursor.execute('SELECT id FROM actors where name = %s;', ('Tim Robbins',))
    id = test_cursor.fetchone()[0]

    response = client.get(f'/actors/{id}')
    actor_json = json.loads(response.data)
    assert actor_json['id'] == id
    assert [movie['title'] for movie in actor_json['movies']] == ['Shawshank', 'Bull Durham']

def test_movies_show_displays_related_actors(app, client):
    test_cursor.execute('SELECT id FROM movies where title = %s;', ('Shawshank',))
    id = test_cursor.fetchone()[0]

    response = client.get(f'/movies/{id}')
    movie_json = json.loads(response.data)
    assert [actor['name'] for actor in movie_json['actors']] == ['Tim Robbins', 'Morgan Freeman']

def test_movies_index_displays_related_actors(app, client):
    response = client.get(f'/movies')
    movies_json = json.loads(response.data)
    assert set([actor['name'] for actor in movies_json[0]['actors']]) == set(['Morgan Freeman', 'Tim Robbins'])

def test_actors_index_displays_related_movies(app, client):
    response = client.get(f'/actors')
    actors_json = json.loads(response.data)
    assert set([movie['title'] for movie in actors_json[0]['movies']]) == set(['Shawshank', 'Bull Durham'])
