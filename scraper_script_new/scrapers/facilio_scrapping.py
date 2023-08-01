from bs4 import BeautifulSoup

from src.config import *
from src.utils import *


def get_article_links(content):
    soup = BeautifulSoup(content, 'lxml')
    posts = soup.find('div', class_='post-feed')
    article_links = list()
    articles = posts.find_all('article',class_='post-card')
    for article in articles:
        date_string = article.find('time',class_='post-card-meta-date').text
        formatted_date = format_facilio_date(str(date_string))
        # if True: # To add previous data
        if formatted_date==today:
            article_link=article.find('a')['href']
            article_links.append('https://facilio.com'+article_link)
    return article_links
    
def scrape_each_article(link):
    try:
        content = get_html_content(link, False)
        soup = BeautifulSoup(content, 'lxml')
        article = soup.find('article',class_='post')
        with open('article_links.html', 'w') as file:
            file.write(str(article))
        
        heading = article.find('h1',class_='blog-title').text
        print(heading)
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        figure_tag = soup.find('figure', class_='article-image')
        img_tag = figure_tag.find('img')
        if img_tag:
            data_src_value = 'https://facilio.com'+img_tag['src']
        img_path = user_download(data_src_value, heading_cleaned, False)
        article_content = article.find('div', class_='content-section').text
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
                    "bmf" : 0,
                    "pfm" : 0,
                    "ifma" : 0,
                    "tomorrow" : 0,
                    "fmlink" : 0,
                    "iwfm" : 0,
                    "facmag" : 1,
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
        content = get_html_content(link, False)
        soup = BeautifulSoup(content, 'lxml')
        article = soup.find('article',class_='post')
        with open('article_links.html', 'w') as file:
            file.write(str(article))
            
        heading = article.find('h1',class_='blog-title').text
        print(heading)
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        figure_tag = soup.find('figure', class_='article-image')
        img_tag = figure_tag.find('img')
        if img_tag:
            data_src_value = 'https://facilio.com'+img_tag['src']
        date_string = article.find('time',class_='byline-meta-date').text
        formatted_date = format_facilio_date(str(date_string))
        
        db = connect_mong()
        coll = db.new_newsletter
        coll.delete_many({"date" : formatted_date, "facmag" : 1})
        print('Adding blogs of date:'+ formatted_date)
            
        img_path = user_download(data_src_value, heading_cleaned, False)
        article_content = article.find('div', class_='content-section').text
        article_name = heading
        content = {
                    "date" : formatted_date,
                    "article": article_name,
                    "image": img_path,
                    "image_src" : data_src_value,
                    "text": article_content.strip(),
                    "c2a_link": link,
                    "c2a_button": "Read from Source",
                    "facilio" : 1,
                    "qad" : 0,
                    "upkeep" : 0
                }
        
        return content
    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None

def main():
    contents = list()
    content = get_html_content(FACILIO_LINK, False)
    with open('article_links.html', 'w') as file:
            file.write(str(content))
    articles = get_article_links(content)
    for article in articles:
        content = scrape_each_article(article)
        # content = scrape_each_article_getData(article) # To add previous data
        if content:
            contents.append(content)
    # print(content)
    print(f"Number of articles from FACILIO: {len(contents)}")
    return contents