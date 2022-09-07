from api.lib.orm import build_from_records
import api.models as models

class Actor:
    __table__ = 'actors'
    columns = ['id', 'name']

    def __init__(self, **kwargs):
        # verify all keyword arguments are column names
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} is not in {self.columns}')

        # assign keyword arguments to the class attributes
        for k, v in kwargs.items():
            setattr(self, k, v)

    def movies(self, conn):
        cursor = conn.cursor()

        query = f"""SELECT m.* FROM movies m
                    JOIN movie_actors ma
                    ON ma.movie_id = m.id
                    WHERE ma.actor_id = {self.id}"""
        cursor.execute(query)
        movie_records = cursor.fetchall()
        movies = build_from_records(models.Movie, movie_records)

        return movies

    def to_json(self, conn):
        pass
