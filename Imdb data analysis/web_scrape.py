import requests
from bs4 import BeautifulSoup
import csv

csv_file = open('imdb_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Movie Name', 'Released Year', 'Rating', 'Gross Earnings in Million $', 'Genre', 'Cast'])

for page_number in range(0,5):
    url = requests.get(f'https://www.imdb.com/list/ls050782187/?sort=user_rating,desc&st_dt=&mode=detail&page={page_number}').text
    soup = BeautifulSoup(url,'lxml')
    movies = soup.findAll('div',class_='lister-item-content')

    for movie in movies:
        movie_name = movie.find('h3',class_='lister-item-header').a.text #name

        released_year = movie.h3.find('span',class_='lister-item-year text-muted unbold').text #released year

        rating = movie.div.div.find('span',class_='ipl-rating-star__rating').text #rating

        genres = []
        try:
            genre_span_tag = movie.p.select('span')[4]
            for genre in genre_span_tag:
                genres.append(genre.text.strip())
        except:
            genres = None

        cast_p_tag = movie.select('p')[2]
        cast = [] #cast
        for actor in cast_p_tag.findAll('a'):
            cast.append(actor.text)

        gross_ptag = movie.select('p')[3]
        try:
            gross = gross_ptag.select('span')[4].text #gross earning
        except:
            gross = None

        csv_writer.writerow([movie_name,released_year,rating,gross,genres,cast])

csv_file.close()

    