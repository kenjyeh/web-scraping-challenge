from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 
    exec_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    return Browser('chrome', headless=True, **exec_path)

# create dictionary to store info into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_news():
    try: 
        browser = init_browser()

        # set base URL
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        html = browser.html

        # parse with bs
        soup = bs(html, 'html.parser')

        # retrieve title and paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # store retrieved info
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

# FEATURED IMAGE
def scrape_image():

    try: 

        browser = init_browser()

        # set base URL
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)

        html_image = browser.html


        soup = bs(html_image, 'html.parser')

        # retrieve image URL
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # image base URL
        main_url = 'https://www.jpl.nasa.gov'

        # create full image url
        featured_image_url = main_url + featured_image_url

        #show full link to image
        featured_image_url 

        # add to dictionary
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    finally:

        browser.quit()

        


# Mars Facts
def scrape_facts():

    # set mars facts url
    facts_url = 'http://space-facts.com/mars/'

    mars_facts = pd.read_html(facts_url)

    mars_df = mars_facts[0]

    # set column titles
    mars_df.columns = ['Description','Value']

    mars_df.set_index('Description', inplace=True)

    data = mars_df.to_html()

    # add to dictionary
    mars_info['mars_facts'] = data

    return mars_info


# MARS HEMISPHERES


def scrape_hemispheres():

    try: 

        browser = init_browser()

        # set hemisphere html 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # parse with bs
        soup = bs(html_hemispheres, 'html.parser')

        # retrieve all information in the div and item class
        items = soup.find_all('div', class_='item')

        # create list to store hemisphere urls
        hemi_url = []

        # set base hemisphere url
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # use for loop to look through items list
        for i in items: 
            # store title
            title = i.find('h3').text
            
            # point to the link for image and store them
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # concatenate urls together
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # html object
            partial_img_html = browser.html
            
            soup = bs( partial_img_html, 'html.parser')
            
            # point to image url and stores it
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # append image url to list
            hemi_url.append({"title" : title, "img_url" : img_url})

        mars_info['hemi_info'] = hemi_url

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()