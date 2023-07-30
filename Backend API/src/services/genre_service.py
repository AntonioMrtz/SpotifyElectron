import json
from model.Genre import Genre


def get_genres() -> json:
    """ Returns a json with all the available genres"

    Parameters
    ----------

    Raises
    -------

    Returns
    -------
        Json { GenreEnum : 'genre'}
    """

    # Obtener todas las propiedades de la clase Genre
    genre_properties = [(g.name, g.value) for g in Genre]

    genre_dict = dict(genre_properties)
    genre_json = json.dumps(genre_dict)

    return genre_json
