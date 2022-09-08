from api.models.movie import Movie
from api.models.actor import Actor
from api.models.movie_actor import MovieActor
from api.lib.db import save, test_conn, drop_all_tables, test_cursor
import pytest

@pytest.fixture()
def movie():
    drop_all_tables(test_conn, test_cursor)
    shawshank = Movie(title = 'shawshank')
    saved_shawshank = save(shawshank, test_conn, test_cursor)

    morgan_freeman = Actor(name = 'Morgan Freeman')
    saved_morgan = save(morgan_freeman, test_conn, test_cursor)

    robbins = Actor(name = 'Tim Robbins')
    saved_robbins = save(robbins, test_conn, test_cursor)
    m_a_1 = MovieActor(actor_id = saved_robbins.id, movie_id = saved_shawshank.id)
    save(m_a_1, test_conn, test_cursor)
    m_a_2 = MovieActor(actor_id = saved_morgan.id, movie_id = saved_shawshank.id)
    save(m_a_2, test_conn, test_cursor)

    yield saved_shawshank

    drop_all_tables(test_conn, test_cursor)

def test_accepts_mass_assignment():
    movie = Movie(title = 'shawshank redemption', runtime = 144)
    assert movie.__dict__  == {'title':'shawshank redemption', 'runtime': 144}

def test_has_setup_to_save_movie():
    movie = Movie(title = 'the minions', studio = 'disney', runtime = 144,
     description = 'cute aliens', release_date = '12/10/2010', year = 2010)
    cursor = test_conn.cursor()
    saved_movie = save(movie, test_conn, cursor)

    assert type(saved_movie.id) == int

def test_actors_method_finds_associated_actors(movie):

    actors = movie.actors(test_conn)

    actor_names = [actor.name for actor in actors]
    assert set(actor_names) == set(['Tim Robbins', 'Morgan Freeman'])

def test_to_json_returns_actors_in_movie(movie):
    movie_json = movie.to_json(test_conn)
    assert movie_json['title'] == 'shawshank'
    assert set([actor['name'] for actor in movie_json['actors']]) == set(['Morgan Freeman', 'Tim Robbins'])
