from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
import pandas as pd
import time
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 

def init_browser():
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)


def scrape():
        browser = init_browser()
        collection.drop()
        
        news_url = 'https://mars.nasa.gov/news/'
        browser.visit(news_url) 
        news_html = browser.html
        news_soup = bs(news_html,'lxml')
        news_title = news_soup.find("div",class_="content_title").text
        news_p = news_soup.find("div", class_="rollover_description_inner").text
        
        image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url)
        image_html = browser.html
        image_sp = bs(image_html,"html.parser")
        ftimage_url = image_sp.find('div',class_='carousel_container').article.footer.a['data-fancybox-href']
        image_link = "https:"+image_sp .find('div', class_='jpl_logo').a['href'].rstrip('/')
        feature_url = image_link+ftimage_url

        mars_facts_url = 'https://space-facts.com/mars/'
        browser.visit(mars_facts_url) 
        mars_table = pd.read_html(mars_facts_url)
        mars_table[0]
        marsdf = mars_table[0]
        mfacthtml = marsdf.to_html(header=False, index=False)
        mfacthtml

        mars_hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(mars_hem_url)   
        hem_html = browser.html
        hem_sp = bs(hem_html,"html.parser")
        results = hem_sp.find_all("div",class_='item')
        hem_image_url = []
        
        for result in results:
                finaldict = {}
                all_titles = result.find('h3').text
                partial_links = result.find("a")["href"]
                image_links = "https://astrogeology.usgs.gov/" + partial_links   
                browser.visit(image_links)
                html = browser.html
                soup= bs(html, "html.parser")
                downloads = soup.find("div", class_="downloads")
                images_urls = downloads.find("a")["href"]
                print(all_titles)
                print(images_urls)
                finaldict['title']= all_titles
                finaldict['image_url']= images_urls
                hem_image_url.append(product_dict)


        browser.quit()


        all_mars_data ={
	        'news_header' : news_title,
	        'teaser': news_p,
                'featured_pic': feature_url,
	        'mars_fact_table': mfacthtml,
	        'hemisphere_urls': hem_image_url,
                'news_url': news_url,
                'images_url': image_url,
                'mars_facts_url': mars_facts_url,
                'hemisphere_url': mars_hem_url,
                }
        collection.insert(all_mars_data)




