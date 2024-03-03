from random import randint
from dataclasses import dataclass
import psycopg2
from services.services import parsing_kinopoisk
import memcache

@dataclass
class CacheDatabase:
    ip: str = '127.0.0.1'
    port: str = '11211'
    
    _mc = memcache.Client(servers=[f'{ip}:{port}'], debug=0)

    def set_values(self, key_value, values) -> None:
        self._mc.set(key_value, values)
    
    def get_values(self, key_value) -> list:
        return self._mc.get(key_value)
    
    def delete_values(self, key_value) -> None:
        self._mc.delete(key_value)

@dataclass
class Database:
    dbname: str = 'datas'
    user: str = 'postgres'
    password: str = '1234'
    host: str = 'localhost'
    port: int = '5432'

    _connection = psycopg2.connect(
        dbname= dbname,
        user=user,
        password=password,
        host=host
        )
    
    _cur = _connection.cursor()

    def add_top_250_films(self) -> None:

        self._cur.execute(
            'DELETE FROM public.films'
        )
        self._connection.commit()
        positions = [x for x in range(1, 251)]
        for n in range(1, 6):
            films = parsing_kinopoisk(page=n)

            for place, film in films.items():
                self._cur.execute(
                    '''INSERT INTO public.films(
                    film_name, film_place, film_country, film_rating, film_year, film_url)
                    VALUES ('{film_name}', {film_place}, '{film_country}', '{film_rating}', {film_year}, '{film_url}')'''.format(
                        film_name=film['film_name'], 
                        film_place=positions.pop(0),
                        film_country=film['film_country'],
                        film_rating=film['film_rating'],
                        film_year=int(film['film_year']),
                        film_url=film['film_url']
                        )
                )
                self._connection.commit()

    def registration_row(self, username: str, full_name: str = f'KinoPoisk_user{randint(10_000, 99_000)}') -> None:
        self._cur.execute('''
        INSERT INTO public.users (username, full_name)
        SELECT '{username}', '{full_name}'
        WHERE NOT EXISTS (
            SELECT 1
            FROM public.users
            WHERE username = '{username}');'''.format(
                username=username,
                full_name=full_name
            ))
        self._connection.commit()
        self._cur.execute('''
        INSERT INTO public.favourite_films (username)
        SELECT '{username}'
        WHERE NOT EXISTS (
            SELECT 1
            FROM public.favourite_films
            WHERE username = '{username}');'''.format(
                username=username,
            ))

        self._connection.commit()
    
    def get_film(self, film_position: int = 1) -> tuple:
        self._cur.execute('''
            SELECT film_country, film_rating, film_year, film_url, film_name, film_place
	        FROM public.films WHERE film_place = {film_position};
    '''.format(film_position=film_position))
        result = self._cur.fetchall()

        return result, film_position
    
    def get_user_info(self, username: str = None) -> tuple:
        self._cur.execute('''
            SELECT user_last_page
	        FROM public.users
            WHERE username='{username}';
    '''.format(username=username))
        
        result = self._cur.fetchall()

        return result
    
    def add_to_favourite(self, film: str, username: str = None):
        self._cur.execute('''
            SELECT favourite_films
	        FROM public.favourite_films
	        WHERE username='{username}';
            '''.format(username=username))
        result = self._cur.fetchone()
        result = [x[0] for x in result]
        result = list(x for x in result[0])
        if film not in result:
            result.append(film)
        self._cur.execute('''
        UPDATE public.favourite_films
	    SET favourite_films=ARRAY[{films}]
	    WHERE username='{username}';'''.format(username=username, films=result))
        self._connection.commit()

    def get_favourite(self, username: str = None):
         self._cur.execute('''
            SELECT favourite_films
	        FROM public.favourite_films
	        WHERE username='{username}';
            '''.format(username=username))
         result=self._cur.fetchone()
         result = [x[0] for x in result]
         result = list(x for x in result[0])
         
         return result
    
    def get_link_from_favourite(self, film_name: str = None):
        self._cur.execute('''
            SELECT film_url
	        FROM public.films
	        WHERE film_name='{film_name}';
            '''.format(film_name=film_name))
        result=self._cur.fetchone()
        
        return result[0]