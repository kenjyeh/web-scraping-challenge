from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd 
from webdriver_manager.chrome import ChromeDriverManager
import time


# Initialize browser
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # set base url
    browser.visit('https://mars.nasa.gov/news/')

    #set sleep timer
    time.sleep(1)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    #scrape all titles and teasers 
    all_titles = soup.find_all('div', class_='content_title')
    all_teasers = soup.find_all('div', class_='article_teaser_body')
    # selected the latest title and teaser
    news_title = all_titles[1].text
    news_p = all_teasers[0].text


    
    # set image url
    browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')

    time.sleep(1)

    # get to full image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')

    # get full image url

    results = soup.find_all("div", class_="fancybox-overlay")
    relative_img_path = results[0].img['src']
 
    featured_img = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + relative_img_path





    # get mars facts table
    tables = pd.read_html('https://space-facts.com/mars/')


    df = tables[0]

    # rename columns to match table
    df.columns=['description', 'value']

    
    # Convert table to html
    mars_facts_table = df.to_html(classes='data table', index=False, header=False, border=0)



    # set hemisphere url source
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemispheres_main_url="https://astrogeology.usgs.gov/"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    #Finding Titles 

    items_class = soup.find_all('div', class_='item')

    # empty list for hemisphere images url
    hemisphere_image_urls = []  

    # loop through items class to find img url
    for i in items_class: 
    
        title = i.find('h3').text
    
        # point at href url
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # aggregate main url with image url
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # store hemisphere information
        partial_img_html = browser.html
        
        # parse html with beautiful soup
        soup = bs( partial_img_html, 'html.parser')
        
        # point at full image url 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # store the full image url in a dictionary
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        #image_titles=[]
        #titles=soup.find_all('div', class_='description')
        #for title in titles: 
        #        h3=title.find('h3').text
        #        image_titles.append(h3)
                

        #image_titles

        #partial_url=[]
        #items=soup.find_all('div', class_='item')

        #for item in items: 
        #        url=item.find('a')
        #        href=base_url+url['href']
        #        partial_url.append(href)
        #        print(base_url+url['href'])
        #partial_url

        #browser.visit(partial_url[0])
        #time.sleep(1)
        #html=browser.html
        #soup = bs(html, 'html.parser')
        #full_image=soup.find('img', class_='wide-image')
        #full_image=full_image['src']
        #full_image_url=base_url+full_image

        #full_image_url

        #full_image_url_final=[]

        #for url in partial_url: 
        #        browser.visit(url)
        #        html=browser.html
        #        soup = bs(html, 'html.parser')
        #        full_image=soup.find('img', class_='wide-image')
        #        full_image_url_final.append(base_url+full_image['src'])
                
        #full_image_url_final

        #image_dict=[]
        #full_image_url_final


        #for i in range(len(image_titles)):
        #    image_dict.append({'title':image_titles[i],'img_url':full_image_url_final[i]})

        #len(image_titles)



        #image_dict

        

        # Store data in a dictionary
   
    mars_info = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_img,
        "mars_facts": mars_facts_table,
        "hemispheres": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info