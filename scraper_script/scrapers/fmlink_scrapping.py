
from bs4 import BeautifulSoup

from src.config import *
from src.utils import *

def get_article_links(content):
    article_links = list()
    soup = BeautifulSoup(content, 'lxml')
    
    posts = soup.find_all('article')

    for article in posts:
        link = article.a['href']
        dateofart = article.h1.text.split(" ")
        dateofart = dateofart[len(dateofart)-3:len(dateofart)]
        formatted_date = format_fmlink_date(dateofart[0], dateofart[1], dateofart[2])   #month date and year
        if formatted_date == today:
            article_links.append(link)
    
    return article_links


def scrape_each_article(link):
    try:
        content = get_html_content(link)
        article = BeautifulSoup(content, 'lxml')
        heading = article.find('h1', class_ = "entry-title").text
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        
        img_src = article.find('div', id = "content").img['src']
        img_path = user_download(img_src, heading_cleaned)
        article_content_1 = article.find_all('p')[1].text        
        article_content_2 = article.find_all('p')[2].text        
        article_content_3 = article.find_all('p')[3].text  
        article_content = article_content_1 + '\n' + article_content_2 + '\n' + article_content_3
        content = {
            "date" : today,
            "article": heading,
            "image": img_path,
            "image_src" : img_src,
            "text": article_content,
            "c2a_link": link,
            "c2a_button": "Read from Source",
            "evbex" : 0,
            "fmj" : 0,
            "bmf" : 0,
            "pfm" : 0,
            "ifma" : 0,
            "tomorrow" : 0,
            "fmlink" : 1,
            "iwfm" : 0,
            "facmag" : 0

        }
        return content
        
    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None

def main():
    contents = list()
        
    content = get_html_content(FMLINK_MAG)
    
    articles = get_article_links(content)
    
    for article in articles:
        out = scrape_each_article(article)
        if out:
            contents.append(out)

    print(f"Number of articles from FMLinkScraping: {len(contents)}")
    return contents