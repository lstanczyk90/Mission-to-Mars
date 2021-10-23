
# Import Splinter and BeautifulSoup

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

def scrape_all():

    # Set up Splinter

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres" : mars_hems(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site

    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:

        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')


        # Use the parent element to find the first `a` tag and save it as `news_title`

        news_title = slide_elem.find('div', class_='content_title').get_text()


        # Use the parent element to find the paragraph text

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:

        return None, None

    return news_title, news_p

# ## Featured Images

def featured_image(browser):

    # Visit URL

    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup

    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
    
        # Find the relative image url

        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ## Mars Facts

def mars_facts():

    try:

        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except AttributeError:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace = True)
  

# Convert the dataframe back to html to propery display it on our website.

    return df.to_html(classes="table table-striped")

# This last block of code tells Flask that our script is complete and ready for action. 
# The print statement will print out the results of our scraping to our terminal after executing the code.

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

def mars_hems(browser):

    # 1. Use browser to visit the URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

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

    return hemisphere_image_urls







