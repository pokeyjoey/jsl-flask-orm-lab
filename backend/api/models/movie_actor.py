class MovieActor:
    __table__ = 'movie_actors'
    columns = ['id', 'movie_id', 'actor_id']

    def __init__(self, **kwargs):
        # make sure keyword arguments match column names.
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in {self.columns}')

        # make keyword arguments class attributes
        for k, v in kwargs.items():
            setattr(self, k, v)


