from bs4 import BeautifulSoup

from src.config import *
from src.utils import *


def get_article_links(content):
    soup = BeautifulSoup(content, 'lxml')
    posts = soup.find('div', class_='post-listing')
    articles = posts.find_all('article')
    article_links = list()
    
    for article in articles:
        time_var = article.p.span.text  ## Checking the presence of hours in the articles
        if string_present(time_var, 'hours') or string_present(time_var, 'mins') or string_present(time_var, 'hour') or string_present(time_var, 'min'):
            article_links.append(article.h2.a['href'])
        # elif string_present(time_var, 'days'):
        #     if ('1' in time_var) or ('2' in time_var):
        #         article_links.append(article.h2.a['href'])
            
    return article_links



def scrape_each_article(link):
    try:
        print("**********************")
        print(link)
        print("**********************")
        content = get_html_content(link)
        soup = BeautifulSoup(content, 'lxml')
        article = soup.find('article')
        heading = article.h1.text
        
        img_src = article.find('div', class_='single-post-thumb')
        img_src = img_src.img['data-lazy-src']
        
        img_path = user_download(img_src, heading)
        
        
        article_contents = article.find_all('div', class_='entry')[:1]
        article_content = '\n'.join(para.text for para in article_contents) 
        article_content = article_content.split('\n')[1] + ' ' + article_content.split('\n')[2]


        article_name = heading 
        content = {
                    "date" : today,
                    "article": article_name,
                    "image": img_path,
                    "image_src" : img_src,
                    "text": article_content,
                    "c2a_link": link,
                    "c2a_button": "Read from Source",
                    "evbex" : 0,
                    "fmj" : 1
                }
        
        return content
    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None

def main():
    contents = list()
        
    content = get_html_content(FMJ_LINK)
    articles = get_article_links(content)
    
    for article in articles:
        content = scrape_each_article(article)
        if content:
            contents.append(content)
    print(f"Number of articles from FMJ: {len(contents)}")
    return contents