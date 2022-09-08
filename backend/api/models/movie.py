from api.lib.orm import build_from_records
import api.models as models

class Movie:
    __table__ = 'movies'
    columns = ['id', 'title', 'studio', 'runtime', 'description', 'release_date', 'year']

    def __init__(self, **kwargs):
        # test that all keyword arguments are table columns
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} is not in {self.columns}')

        # Set the columns for the class
        for k, v in kwargs.items():
            setattr(self, k, v)

    def actors(self, conn):
        cursor = conn.cursor()

        query = f"""SELECT a.* FROM actors a
                    JOIN movie_actors ma
                    ON ma.actor_id = a.id
                    WHERE ma.movie_id = {self.id}"""
        cursor.execute(query)
        actor_records = cursor.fetchall()
        actors = build_from_records(models.Actor, actor_records)

        return actors

    def to_json(self, conn):
        movie_attributes = self.__dict__
        actors = self.actors(conn)
        movie_attributes['actors'] = [actor.__dict__ for actor in actors]

        return movie_attributes
