import requests
from bs4 import BeautifulSoup
from flask import Flask, request
import json

movie_map = {}
movie_list = []
app = Flask(__name__)

class Movie(object):
    def __init__(self, movie_name, year, director, writers, stars, rating, genres):
        self.movie_name = movie_name
        self.release_year = year
        self.director = director
        self.writers = writers
        self.cast = stars
        self.rating = rating
        self.genres = genres

def extract_movie_listings(url):
    count = 0;
    movies = {}
    while url:
        print("Crawling %s" % (url))
        code = requests.get(url)
        plain = code.text
        soup = BeautifulSoup(plain, "html.parser")
        for d in soup.find_all('div',{'class':'lister-col-wrapper'}):
            title = d.find('div',{'class':'col-title'}).find('span', {'class':'lister-item-header'})
            link = title.find('a')
            rating = d.find('div', {'class':'col-imdb-rating'}).find('strong').string.strip()
            movies.update({link.string :
                               {'link':'https://www.imdb.com'+link.get('href'),
                                'rating': rating}})
            count+=1
        url = soup.find('a', {'class': 'next-page'})
        if url:
            url = "https://www.imdb.com" + url.get('href')
        else:
            url = ""
    print("No. of listings: %d" % (count))
    print("Getting movie details....")
    for k in movies:
        print("Crawling %s" % movies[k]['link'])
        extract_movie_details(k, movies[k])

def extract_movie_details(movie, info):
    code = requests.get(info['link'])
    plain = code.text
    soup = BeautifulSoup(plain, "html.parser")
    word_set = set()
    word_set.update(set(movie.lower().split()))
    title_div = soup.find('div',{'class':'title_wrapper'}).find('span',{'id': 'titleYear'}).find('a')
    plot_div = soup.find('div',{'class':'plot_summary'})
    story_div = soup.find('div',{'id':'titleStoryLine'}).find_all('div',{'class':'see-more inline canwrap'})
    release_year = title_div.string.strip()
    word_set.add(release_year)
    credits = plot_div.find_all('div',{'class':'credit_summary_item'})
    for c in credits:
        if "director" in c.find('h4').string.lower():
            for v in c.find_all('a'):
                word_set.update(set(v.string.lower().split()))
        if "writers" in c.find('h4').string.lower():
            for v in c.find_all('a'):
                word_set.update(set(v.string.lower().split()))
        if "star" in c.find('h4').string.lower():
            for v in c.find_all('a'):
                word_set.update(set(v.string.lower().split()))
    for s in story_div:
        if "genre" in s.find('h4').string.lower():
            for v in s.find_all('a'):
                word_set.update(set(v.string.lower().split()))
            break
    for w in word_set:
        if w in movie_map:
            movie_map[w].add(movie)
        else:
            movie_map[w] = set()
            movie_map[w].add(movie)
    # movie_obj = Movie(movie, release_year, director, writers, stars, info['rating'], genres)
    # movie_list.append(movie_obj)

extract_movie_listings('https://www.imdb.com/search/title?groups=top_1000&view=simple&sort=user_rating,desc&ref_=adv_prv')
print("DONE")

@app.route('/movies')
def search_all_movies():
    query = request.args.get('query')
    sets = []
    words = query.lower().split(' ')
    for w in words:
        if w in movie_map:
            sets.append(movie_map[w])
    result = set()
    for s in sets:
        if not result:
            result = s
        else:
            result = result.intersection(s)
    return json.dumps(list(result))

