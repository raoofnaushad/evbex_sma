from bs4 import BeautifulSoup
import re

from src.config import *
from src.utils import *


def get_article_links(content):
    soup = BeautifulSoup(content, 'lxml')
    regex = re.compile('aux-col aux-ajax-item post-*')
    articles = soup.find_all('div', class_=regex)
    article_links = list()
    
    for article in articles:
        article_links.append(article.a['href'])
            
    return article_links[:3]



def scrape_each_article(link):
    try:
        print("**********************")
        print(link)
        print("**********************")
        content = get_html_content(link)
        article = BeautifulSoup(content, 'lxml')
        
        heading = article.h1.text
        img_src = article.find('div', class_='elementor-image').img['src']
        img_path = user_download(img_src, heading)
        
        article_contents = article.find_all('div', class_='aux-modern-heading-description')[:2]
        article_content = '\n'.join(para.text for para in article_contents) 

        article_content = article_content.split('\n')[0] + ' ' + article_content.split('\n')[1]

        article_name = heading 
        content = {
                    "date" : today,
                    "article": article_name,
                    "image": img_path,
                    "image_src" : img_src,
                    "text": article_content,
                    "c2a_link": link,
                    "c2a_button": "Read from Source",
                    "evbex" : 1,
                    "fmj" : 0
                }
        
        return content
    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None



def main():
    contents = list()
        
    content = get_html_content(EVBEX_LINK)
    
    articles = get_article_links(content)
    
    for article in articles:
        if scrape_each_article(article):
            contents.append(scrape_each_article(article))

    print(f"Number of articles from EVBEX: {len(contents)}")
    
    return contents