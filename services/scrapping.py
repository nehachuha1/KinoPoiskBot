from bs4 import BeautifulSoup
import json


def scrapping_html_to_json(html_page: BeautifulSoup) -> dict:
    page_source = html_page

    result = dict()

    try:
        films_raw = page_source.findAll(name='div', class_='styles_upper__j8BIs')
        num = 1
        for film_raw in films_raw:
            film_position = num
            film_name = film_raw.find(name='span', class_='styles_mainTitle__IFQyZ styles_activeMovieTittle__kJdJj').text
            film_url = f"https://www.kinopoisk.ru{film_raw.find(name='a', class_='base-movie-main-info_link__YwtP1').get('href')}"
            film_country = film_raw.find(name='span', class_='desktop-list-main-info_truncatedText__IMQRP').text.split()[0]
            film_rating = film_raw.find(name='span', class_='styles_kinopoiskValuePositive__vOb2E styles_kinopoiskValue__9qXjg styles_top250Type__mPloU').text
            if film_raw.find(name='span', class_='desktop-list-main-info_secondaryText__M_aus').text[0] == ',':
                film_year = film_raw.find(name='span', class_='desktop-list-main-info_secondaryText__M_aus').text.split(',')[1]
            else:
                film_year = film_raw.find(name='span', class_='desktop-list-main-info_secondaryText__M_aus').text.split(',')[0]
            
            result[film_position] = {
                'film_name': film_name,
                'film_country': film_country,
                'film_rating': film_rating,
                'film_year' : film_year,
                'film_url': film_url
            }

            num += 1
        return result
    except Exception as ex:
        print(ex)