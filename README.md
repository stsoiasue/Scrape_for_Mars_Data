# Mission to Mars

In this assignment, I built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

___

## Step 1 - Scraper Setup

In a Jupyter Notebook I used BeautifulSoup, Pandas, Requests, and Splinter to do my initial scraper setup. I gathered information from the sources below.

* ### [NASA Mars News:](https://mars.nasa.gov/news/)

* ### [JPL Mars Featured Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)

* ### [Mars Weather from Twitter](https://twitter.com/marswxreport?lang=en)

* ### [Mars Facts](http://space-facts.com/mars/)

* ### [Images of Mars Hemisperes](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

[see my code](mission_to_mars.ipynb)

---

## Step 2 - MongoDB and Flask Application

* I downloded the notebook to a python file and placed all of the scraping methods into one function called `scrape` which returns a python dictionary with all of the scraped data. 

  [see my code](scrape_mars.py)

* In another python file I set up a `Flask` application with a `/scrape` route which calls the scrape function and stores the returned dictionary in a MongoDB database.

  [see my code](scrape_app.py)

* Finally I created a root route `/` which renders an html template using the data gathered from the `/scrape` route

  [see my code](templates/index.html)

---

