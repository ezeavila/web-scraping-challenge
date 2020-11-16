#!/usr/bin/env python
# coding: utf-8

# In[18]:


from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
import pandas as pd
import time


# In[19]:


get_ipython().system('which chromedriver')


# In[20]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[21]:


news_url = 'https://mars.nasa.gov/news/'
browser.visit(news_url)


# In[22]:


# Create a Beautiful Soup object
news_html = browser.html
news_soup = bs(news_html,'lxml')
print(news_soup)


# In[26]:


# Extract title  and paragraph text
news_title = news_soup.find("div",class_="content_title").text
news_p = news_soup.find("div", class_="rollover_description_inner").text
print(news_title)
print(news_p)


# In[23]:


# Get image from JPL Mars Space Images 
image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(image_url)


# In[24]:


image_html = browser.html
print(image_html)

image_sp = bs(image_html,"html.parser")
print(image_sp)


# In[30]:


ftimage_url = image_sp.find('div',class_='carousel_container').article.footer.a['data-fancybox-href']
print(ftimage_url)
image_link = "https:"+image_sp .find('div', class_='jpl_logo').a['href'].rstrip('/')
feature_url = image_link+ftimage_url
featured_image_url = image_sp.find('h1', class_="media_feature_title").text.strip()

print(feature_url)


# In[33]:


mars_facts_url = 'https://space-facts.com/mars/'
browser.visit(mars_facts_url) 


# In[34]:


mars_table = pd.read_html(mars_facts_url)
mars_table[0]


# In[37]:


marsdf = mars_table[0]
mfacthtml = marsdf.to_html(header=False, index=False)
mfacthtml


# In[39]:


mars_hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(mars_hem_url)   


# In[40]:


hem_html = browser.html
hem_sp = bs(hem_html,"html.parser")


# In[45]:


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


# In[46]:


hem_image_url


# In[ ]:




