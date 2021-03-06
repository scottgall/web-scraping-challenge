
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
  browser = init_browser()
  mars_data = {}

  # NASA Mars News
  # Save the latest News Title and Paragraph Text
  url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
  browser.visit(url)

  html = browser.html
  soup = BeautifulSoup(html, 'lxml')

  news_title = soup.find('div', class_='image_and_description_container').find('div', class_='content_title').a.text.strip()
  news_p = soup.find('div', class_='article_teaser_body').text
  mars_data['news_title'] = news_title
  mars_data['news_p'] = news_p

  # JPL Mars Space Images
  # Save image url for the current Featured Mars Image 
  url = 'https://spaceimages-mars.com/'
  browser.visit(url)

  html = browser.html
  soup = BeautifulSoup(html, 'lxml')

  image = soup.find('img', class_="headerimage")['src']
  featured_image_url = url + image
  mars_data['featured_image_url'] = featured_image_url

  # Mars Facts
  # Use Pandas to scrape the table containing facts about Mars
  url = 'https://space-facts.com/mars/'

  tables = pd.read_html(url)
  
  df = tables[1]
  df.rename({"Mars - Earth Comparison": "Description"}, axis=1, inplace=True)
  df.set_index(['Description'],inplace=True)

  facts_table = df.to_html()
  facts_table = '\n'.join(facts_table.split('\n')[1:-1])
  
  mars_data['facts_table'] = facts_table

  # Mars Hemispheres
  # Save high res images for each hemisphere
  url = 'https://marshemispheres.com/'
  browser.visit(url)

  hemisphere_image_urls = []
  for i in range(4):
      browser.find_by_css('.description')[i].find_by_css('a').click()
      html = browser.html
      soup = BeautifulSoup(html, 'lxml')
      title = soup.find('h2', class_='title').text.split(' Enhanced')[0]
      img_url = url + soup.find('img', class_='wide-image')['src']
      hemisphere_image_urls.append({"title": title, "image_url": img_url})
      browser.visit(url)
  mars_data['hemisphere_image_urls'] = hemisphere_image_urls

  browser.quit()
  return mars_data