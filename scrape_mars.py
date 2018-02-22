# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests as req
import re

def scrape():

    # dictionary to hold scraped data
    scraped_data = {}

    '''
    Get mars news 
    '''
    # assign mars news site html to variable
    mars_news_html = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = req.get(mars_news_html)

    # create Beautiful Soup object
    mars_soup = bs(response.text, "html.parser")

    # find mars news title 
    news_title = mars_soup.find('div', class_='content_title').text

    # remove \n from string
    news_title = news_title.strip('\n')

    # find mars news paragraph 
    news_p = mars_soup.find('div', class_='rollover_description_inner').text

    # remove \n from string
    news_p = news_p.strip('\n')

    # add to dictionary
    scraped_data['news_title'] = news_title 
    scraped_data['news_paragraph'] = news_p

    '''
    Get JPL image URL
    '''
    # assign jpl url to variable
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Retrieve page with the requests module
    response = req.get(jpl_url)

    # create Beautiful Soup object
    jpl_soup = bs(response.text, "html.parser")

    # find div with carosel_items class
    featured_image_url = jpl_soup.find('a', class_='fancybox')

    # reassign to style attribute of div
    featured_image_url = featured_image_url['data-fancybox-href']

    # add jpl website prefix
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url

    # add to dictionary
    scraped_data['jpl_url'] = featured_image_url

    '''
    Get mars weather 
    '''
    # assign mars twitter url to variable
    mars_twitter = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = req.get(mars_twitter)

    # create Beautiful Soup object
    mars_tweet_soup = bs(response.text, "html.parser")

    # find all tweets
    mars_tweets = mars_tweet_soup.find_all('div', class_='tweet')

    # starting timestamp for loop
    latest_timestamp = 0

    for tweet in mars_tweets:
        
        # collect timestamp
        tweet_timestamp = int(tweet.find('span', class_= '_timestamp')['data-time'])
        
        # collect tweet text
        tweet_text = tweet.find('p', class_ = 'tweet-text').text
        
        # assing to weather variable if tweet is mars weather and has the latest timestamp
        if (re.match(r'Sol \d\d\d\d \(', tweet_text) is not None) and (tweet_timestamp > latest_timestamp):
            
            mars_weather = tweet_text
            
            latest_timestamp = tweet_timestamp

    # add to dictionary
    scraped_data['mars_weather'] = mars_weather

    '''
    Get mars facts
    '''
    # assign url to variable
    mars_facts_url = 'https://space-facts.com/mars/'

    # read html tables into dataframes list
    mars_facts_tables = pd.read_html(mars_facts_url)

    # assign mars facts table to variable
    mars_facts_df = mars_facts_tables[0]

    # convert mars_facts_df to html string
    mars_facts_html = mars_facts_df.to_html(index= False, header= None)

    # add to dictionary
    scraped_data['mars_facts'] = mars_facts_html

    '''
    Get mars hemispheres images
    '''
    # assign hemispheres url to variable
    mars_hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Retrieve page with the requests module
    response = req.get(mars_hem_url)

    # create mars_hem soup
    mars_hem_soup = bs(response.text, 'html.parser')

    # define browser
    browser = Browser('chrome', executable_path='chromedriver', headless=False)

    # visit url
    browser.visit(mars_hem_url)

    # find all hem links
    mars_hem_img_list = mars_hem_soup.find_all('a', class_='itemLink')

    # create list to hold title and img_url dicts
    hemisphere_image_urls = []

    # loop through links
    for hem_img in mars_hem_img_list:
        
        hem_dict = {}
        
        # retrieve from header title
        title = hem_img.h3.text
        
        # click on title
        browser.click_link_by_partial_text(title)
        
        # find fullsize image
        full_image_url = browser.find_by_css('.wide-image').first['src']
        
        # add title and image_url to dict
        hem_dict['title'] = title
        hem_dict['img_url'] = full_image_url
        
        # add to hemisphere image list
        hemisphere_image_urls.append(hem_dict) 
        
        # go back to previous page
        browser.back()

    # add to dictionary
    scraped_data['mars_hem_urls'] = hemisphere_image_urls

    return scraped_data