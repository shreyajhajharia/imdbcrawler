# imdbcrawler
Crawl Top 1000 IMDB listings and expose a search API

Pre-requisites:

- Python 2.7
- Flask (pip install flask)
- Requests (pip install requests)
- BeautifulSoup (pip install beautifulsoup4)

Run:

export FLASK_APP=crawler.py  
python -m flask run
```
* Serving Flask app "crawler.py"
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: off

Crawling https://www.imdb.com/search/title?groups=top_1000&view=simple&sort=user_rating,desc&ref_=adv_prv . 
Crawling https://www.imdb.com/search/title?groups=top_1000&view=simple&sort=user_rating,desc&start=51&ref_=adv_nxt . 
Crawling https://www.imdb.com/search/title?groups=top_1000&view=simple&sort=user_rating,desc&start=101&ref_=adv_nxt . 
Crawling https://www.imdb.com/search/title?groups=top_1000&view=simple&sort=user_rating,desc&start=151&ref_=adv_nxt . 
......  
......  
......  
No. of listings: 1000 . 
Getting movie details....  
Crawling https://www.imdb.com/title/tt0085959/?ref_=adv_li_tt  
Crawling https://www.imdb.com/title/tt3521164/?ref_=adv_li_tt  
Crawling https://www.imdb.com/title/tt0289879/?ref_=adv_li_tt  
......  
......  
......  
Crawling https://www.imdb.com/title/tt0068327/?ref_=adv_li_tt  
Crawling https://www.imdb.com/title/tt0081398/?ref_=adv_li_tt  
Crawling https://www.imdb.com/title/tt0373074/?ref_=adv_li_tt  
DONE  
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 ```
 
 Search API call:
 
 curl -X GET http://127.0.0.1:5000/movies?query=spielberg  
 curl -X GET http://127.0.0.1:5000/movies?query=spielberg%20hanks  
 curl -X GET http://127.0.0.1:5000/movies?query=comedy  
 curl -X GET http://127.0.0.1:5000/movies?query=sci-fi%20thriller  
 
 

