from api.models.actor import Actor
from api.models.movie import Movie
from api.models.movie_actor import MovieActor
import pytest
from api.lib.db import save, test_conn, test_cursor, drop_all_tables

@pytest.fixture()
def actor():
    drop_all_tables(test_conn, test_cursor)
    shawshank = Movie(title = 'shawshank')
    saved_shawshank = save(shawshank, test_conn, test_cursor)

    bull_durham = Movie(title = 'bull durham')
    saved_bull_durham = save(bull_durham, test_conn, test_cursor)


    robbins = Actor(name = 'Tim Robbins')
    saved_robbins = save(robbins, test_conn, test_cursor)
    m_a_1 = MovieActor(actor_id = saved_robbins.id, movie_id = saved_shawshank.id)
    save(m_a_1, test_conn, test_cursor)

    m_a_2 = MovieActor(actor_id = saved_robbins.id, movie_id = saved_bull_durham.id)
    save(m_a_2, test_conn, test_cursor)

    yield saved_robbins

    drop_all_tables(test_conn, test_cursor)


def test_accepts_mass_assignment():
    actor = Actor(name = 'Morgan Freeman')
    assert actor.__dict__  == {'name':'Morgan Freeman'}

def test_has_setup_to_save_actor():
    actor = Actor(name = 'Morgan Freeman')
    cursor = test_conn.cursor()
    saved_actor = save(actor, test_conn, test_cursor)
    assert type(saved_actor.id) == int

def test_movies_method_finds_associated_movies(actor):
    movies = actor.movies(test_conn)
    movie_titles = [movie.title for movie in movies]
    assert set(movie_titles) == set(['shawshank', 'bull durham'])

#def test_to_json_returns_movies_actors_participated_in(actor):
#    actor_json = actor.to_json(test_conn)
#    assert actor_json['name'] == 'Tim Robbins'
#    assert [movie['title'] for movie in actor_json['movies']] == ['shawshank', 'bull durham']

