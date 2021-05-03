
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# NASA Mars News
# Save the latest News Title and Paragraph Text

url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'lxml')

news_title = soup.find('div', class_='image_and_description_container').find('div', class_='content_title').a.text.strip()
news_p = soup.find('div', class_='article_teaser_body').text

# JPL Mars Space Images
# Save image url for the current Featured Mars Image 

url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
browser.visit(url)

browser.find_by_id('filter_Mars').click()

browser.find_by_css('.SearchResultCard').click()

html = browser.html
soup = BeautifulSoup(html, 'lxml')

featured_image_url = soup.find('img', class_='BaseImage')['data-srcset'].split(' ')[-2]


# Mars Facts
# Use Pandas to scrape the table containing facts about Mars

url = 'https://space-facts.com/mars/'

tables = pd.read_html(url)

df = tables[0]
df

facts_table = df.to_html(header=False,index=False)

# Mars Hemispheres
# Save high res images for each hemisphere

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

hemisphere_image_urls = []
for i in range(4):
    browser.find_by_css('.description')[i].find_by_css('a').click()
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h2', class_='title').text.split(' Enhanced')[0]
    img_url = 'https://astrogeology.usgs.gov/' + soup.find('img', class_='wide-image')['src']
    hemisphere_image_urls.append({"title": title, "image_url": img_url})
    browser.visit(url)

browser.quit()

