# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import selenium

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)



def soup_connect(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


# NASA Mars News



def mars_news():

    url_nasa = 'https://mars.nasa.gov/news/'
    soup1 = soup_connect(url_nasa)
    titles = soup1.find_all('div', class_="content_title")
    latest_title = titles[0].a.text.strip('\n')
    
    news = soup1.find_all('div', class_="rollover_description_inner") 
    latest_news = news[0].text.strip('\n')
    
    #In case more news needed in the future
    #clean_titles = [title.a.text.strip('\n') for title in titles]
    #clean_news = [content.text.strip('\n') for content in news]
    
    mars_news.title = latest_title
    mars_news.news = latest_news
    
    
    return mars_news
        



# JPL Mars Space Images - Featured Image




def JPL_image():

    browser = init_browser()

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser.visit(url_jpl)
    #for button in buttons:
    browser.find_link_by_partial_text('FULL IMAGE').click()
    browser.is_element_not_present_by_id('images', wait_time=2)
    browser.find_link_by_partial_text('more info').click()
    
    link = browser.find_link_by_partial_href('largesize')
    
    image_url = link.html.split("=")
    image_url = link.html.split("=")[-1].lstrip('"')
    image_url = image_url.rstrip('">')
 
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url
    
    return featured_image_url




# Mars Weather




def mars_weather():
    browser = init_browser()
    url_tweet = 'https://twitter.com/MarsWxReport?lang=en'
    MarsWX = 'Mars Weather'
    soup4 = soup_connect(url_tweet)
    
    tweets = soup4.find_all('div', class_='content')
    tweet_weather = []
    i = 0

    while (len(tweet_weather)<1):
        tweet_id = tweets[i].find('strong').text
        tweet_wx = tweets[i].find('p').text
        if tweet_id == MarsWX:
            tweet_weather.append(tweet_wx)    
        i+=1
    mars_weather = tweet_weather[0]
    
    return mars_weather





# Mars Facts




def mars_fact():
    browser = init_browser()
    url_fact = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_fact)
    tables[0]
    tables[0]['index'] =  [tables[0][0][i].strip(":") for i in range(len(tables[0][0]))]
    clean_table = tables[0][['index',1]]
    clean_table = clean_table.set_index('index')
    clean_table = clean_table.rename(columns={1:'value'})
    clean_table
    table_html = clean_table.to_html()
    
    return table_html




# Mars Hemispheres




def mars_hemi():
    url_usgs = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    soup2 = soup_connect(url_usgs)
    results = soup2.find_all('div', class_='item')
    results[0].find('h3').text
    
    img_title_list = []
    img_url_list = []

    for result in results: 
        img_title = result.find('h3').text.strip(' Enhanced')
        img_title_list.append(img_title)
        tt = result.find('a')['href']
        url_usgs_img = 'https://astrogeology.usgs.gov' + tt
        browser.visit(url_usgs_img)
        soup3 = soup_connect(url_usgs_img)
        img_url = soup3.find_all('div',class_='downloads')[0].find('a')['href']
        img_url_list.append(img_url)
        
        hemisphere_image_urls = [
            {"title": img_title_list, "img_url": img_url_list}
        ]
    
    return hemisphere_image_urls



