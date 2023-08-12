from bs4 import BeautifulSoup

from src.config import *
from src.utils import *


def get_article_links(content):
    soup = BeautifulSoup(content, 'lxml')
    posts = soup.find('div', class_='inner-post-entry')
    article_links = list()
    articles = posts.find_all('div',class_='elementor-widget-container')
    for article in articles:
        date_string = article.find('span',class_='featc-date')
        if(date_string):            
            formatted_date = format_fmmedia_date(str(date_string.time.text))
            # if True: # To add previous data
            if formatted_date==today:
                article_link=article.find('h3', class_='entry-title').a['href']
                article_links.append(article_link)
    return article_links

# penci-wrapper-posts-content
def get_article_links_getData(content):
    soup = BeautifulSoup(content, 'lxml')
    posts = soup.find('div', class_='inner-post-entry')
    article_links = list()
    articles = posts.find_all('li',class_='list-post')
    for article in articles:
        date_string = article.find('time',class_='entry-date')
        if(date_string):         
            formatted_date = format_fmmedia_date(str(date_string.text))
            if True:
                article_link=article.find('h2', class_='penci-entry-title').a['href']
                article_links.append(article_link)
    return article_links
    
def scrape_each_article(link):
    try:
        content = get_html_content(link, True)
        soup = BeautifulSoup(content, 'lxml')     
        heading = (soup.find('h1',class_='post-title').text).strip()
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        print(heading)
        figure_tag = soup.find('div', class_='post-image')
        img_tag = figure_tag.find('img')
        if img_tag:
            data_src_value = img_tag['src']
        img_path = user_download(data_src_value, heading_cleaned, False)
        article_content_head=soup.find('div', class_="inner-post-entry")
        article_content = (article_content_head.find_all('p'))[1].text 
        article_name = heading
        content = {
                    "date" : today,
                    "article": article_name,
                    "image": img_path,
                    "image_src" : data_src_value,
                    "text": article_content.strip(),
                    "c2a_link": link,
                    "c2a_button": "Read from Source",
                    "evbex" : 0,
                    "fmj" : 0,
                    "bmf" : 1,
                    "pfm" : 0,
                    "ifma" : 0,
                    "tomorrow" : 0,
                    "fmlink" : 0,
                    "iwfm" : 0,
                    "facmag" : 0,
                    "fmi" : 0

                }
        
        return content
    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None
    
def scrape_each_article_getData(link): # To add previous data
    try:  
        content = get_html_content(link, True)
        soup = BeautifulSoup(content, 'lxml')     
        heading = (soup.find('h1',class_='post-title').text).strip()
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        figure_tag = soup.find('div', class_='post-image')
        img_tag = figure_tag.find('img')
        if img_tag:
            data_src_value = img_tag['src']
        img_path = user_download(data_src_value, heading_cleaned, False)
        article_content_head=soup.find('div', class_="inner-post-entry")
        article_content = (article_content_head.find_all('p'))[1].text 
        date_string = soup.find('time',class_='entry-date').text
        if date_string:
        # Extract the date text      
            formatted_date = format_fmmedia_date(str(date_string))
        article_name = heading
        db = connect_mong()
        coll = db.new_newsletter
        coll.delete_many({"date" : formatted_date, "bmf" : 1})        
        coll.delete_many({"date" : formatted_date, "fmmedia" : 1})        
        print('Adding blogs of date:'+ formatted_date)
            
        content = {
                    "date" : formatted_date,
                    "article": article_name,
                    "image": img_path,
                    "image_src" : data_src_value,
                    "text": article_content.strip(),
                    "c2a_link": link,
                    "c2a_button": "Read from Source",
                    "facilio" : 0,
                    "qad" : 0,
                    "fmnaz" : 0,
                    "facilitiesnet" : 0,
                    "upkeep" : 0,
                    "fmmedia" : 1,
                }
        
        return content
    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None

def main():
    contents = list()
    content = get_html_content(FMMEDIA_AUS_LINK, False)
    articles = get_article_links(content)
    # articles = get_article_links_getData(content) # To add previous data
    for article in articles:
        content = scrape_each_article(article)
        # content = scrape_each_article_getData(article) # To add previous data
        if content:
            contents.append(content)
    print(f"Number of articles from FMMEDIA_AUS: {len(contents)}")
    return contents