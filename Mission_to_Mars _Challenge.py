#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site

url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page

browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Notice how we've assigned slide_elem as the variable to look for the <div /> tag and its descendent 
# (the other tags within the <div /> element)? This is our parent element. This means that this element holds 
# all of the other elements within it, and we'll reference it when we want to filter search results even further. 
# The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag with 
# the class of list_text. CSS works from right to left, such as returning the last item on the list instead of the 
# first. Because of this, when using select_one, the first matching element returned will be a <li /> element with a 
# class of slide and all nested elements within it.

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# In this line of code, we chained .find onto our previously assigned variable, slide_elem. 
# When we do this, we're saying, "This variable holds a ton of information, so look inside of that information 
# to find this specific data." The data we're looking for is the content title, which we've specified by saying, 
# "The specific data is in a <div /> with a class of 'content_title'."

slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`

news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL

url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url

img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[12]:


# With this line, we're creating a new DataFrame from the HTML table. 
# The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
# By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in 
# the list. Then, it turns the table into a DataFrame

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[13]:


# Convert the dataframe back to html to propery display it on our website.

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[168]:


# 1. Use browser to visit the URL

url = 'https://marshemispheres.com/'

browser.visit(url)


# In[169]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

html = browser.html

home_soup = soup(html, 'html.parser')

results = home_soup.find_all('div', class_="item")

for result in results:
    
    hemispheres = {}
    
    title = result.h3.text
    page_href = result.a['href']
    page_url = f"https://marshemispheres.com/{page_href}"
    
    browser.visit(page_url)
    
    links_found = browser.links.find_by_text('Sample')
    img_url = links_found[0]["href"]
    
    hemispheres["img_url"] = img_url
    hemispheres["title"] = title
    
    if hemispheres not in hemisphere_image_urls:
        hemisphere_image_urls.append(hemispheres)
    
    browser.back()
    
    
    
    
    




# In[170]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[171]:


# 5. Quit the browser
browser.quit()


# In[ ]:




