
from bs4 import BeautifulSoup

from src.config import *
from src.utils import *

def get_article_links(content):
    article_links = list()
    soup = BeautifulSoup(content, 'lxml')
    
    posts = soup.find('div', class_='article-grid-layout-3')
    articles = posts.find_all('div', class_='item')
    
    for article in articles:
        link = "https://www.pfmonthenet.net/" + article.a['href']
        article_links.append(link)
            
    return article_links


def scrape_each_article(link):
    try:
        # print("**********************")
        # print(link)
        # print("**********************")
        content = get_html_content(link)
        soup = BeautifulSoup(content, 'lxml')
        
        
        article = soup.find('div', id='article')
        date = format_pfm_date(article.p.text)
        if date == today:
            heading = article.h1.text
            img_src = article.find('div', class_='articleimage').img['src']
            img_src = "https://www.pfmonthenet.net/" + '/'.join(img_src.split('/')[3:])
            heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())

            
            img_path = user_download(img_src, heading_cleaned)
            
            article_start = article.h3.text
            article_contents = article.find_all('p', class_='MsoNoSpacing')[0].text        
            article_content = article_start + '\n' + article_contents 

            article_name = heading 
            # print(article_name)
            content = {
                        "date" : today,
                        "article": article_name,
                        "image": img_path,
                        "image_src" : img_src,
                        "text": article_content,
                        "c2a_link": link,
                        "c2a_button": "Read from Source",
                        "evbex" : 0,
                        "fmj" : 0
                    }
            
            return content
        else:
            return None

    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None

def main():
    contents = list()
        
    content = get_html_content(PFMONTHNET)
    
    articles = get_article_links(content)
    
    for article in articles:
        out = scrape_each_article(article)
        if out:
            contents.append(out)

    print(f"Number of articles from PFM: {len(contents)}")
    return contents

