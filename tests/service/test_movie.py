from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_first = Movie(
        id=1,
        title='Йеллоустоун',
        description='Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в неовестерне от автора «Ветреной реки»',
        trailer='https://www.youtube.com/watch?v=UKei_d0cbP4',
        year=2018,
        rating=8.6,
        genre_id=17,
        director_id=1
    )
    movie_second = Movie(
        id=2,
        title='Омерзительная восьмерка',
        description='США после Гражданской войны. Легендарный охотник за головами Джон Рут по кличке Вешатель конвоирует заключенную. По пути к ним прибиваются еще несколько путешественников. Снежная буря вынуждает компанию искать укрытие в лавке на отшибе, где уже расположилось весьма пестрое общество: генерал конфедератов, мексиканец, ковбой… И один из них - не тот, за кого себя выдает.',
        trailer='https://www.youtube.com/watch?v=lmB9VWm0okU',
        year=2015,
        rating=7.8,
        genre_id=4,
        director_id=2
    )

    movie_dao.get_one = MagicMock(return_value=movie_first)
    movie_dao.get_all = MagicMock(return_value=[movie_first, movie_second])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None
        assert movie.title is not None
        assert movie.description is not None
        assert movie.trailer is not None
        assert movie.year is not None
        assert movie.rating is not None
        assert movie.genre_id is not None
        assert movie.director_id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_data = {"title": 'Джанго освобожденный',
        "description": 'Эксцентричный охотник за головами, также известный как Дантист, промышляет отстрелом самых опасных преступников. Работенка пыльная, и без надежного помощника ему не обойтись. Но как найти такого и желательно не очень дорогого? Освобождённый им раб по имени Джанго – прекрасная кандидатура. Правда, у нового помощника свои мотивы – кое с чем надо сперва разобраться.',
        "trailer": 'https://www.youtube.com/watch?v=2Dty-zwcPv4',
        "year": 2012,
        "rating": 8.4,
        "genre_id": 17,
        "director_id": 2
        }
        movie = self.movie_service.create(movie_data)
        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_data = {
            "id": 3,
            "title": 'Вооружен и очень опасен',
            "description": 'События происходят в конце XIX века на Диком Западе, в Америке. В основе сюжета — сложные перипетии жизни работяги — старателя Габриэля Конроя. Найдя нефть на своем участке, он познает и счастье, и разочарование, и опасность, и отчаяние...',
            "trailer": 'https://www.youtube.com/watch?v=hLA5631F-jo',
            "year": 1978,
            "rating": 6.0,
            "genre_id": 17,
            "director_id": 3
        }
        self.movie_service.update(movie_data)
