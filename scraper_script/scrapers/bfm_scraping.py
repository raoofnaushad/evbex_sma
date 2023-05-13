
from bs4 import BeautifulSoup

from src.config import *
from src.utils import *


def get_article_links(content):
    article_links = list()
    soup = BeautifulSoup(content, 'lxml')
    
    posts = soup.find('div', class_='mag-box-container clearfix')
    articles = posts.find_all('li')
    
    for article in articles:
        link = article.a['href']
        date = article.find('span', class_='date meta-item tie-icon').text
        if string_present(date, 'hours') or string_present(date, 'mins') or string_present(date, 'hour') or string_present(date, 'min') or string_present(date, 'day'):
            article_links.append(article.h2.a['href'])
        # formatted_date = format_bfm_date(date)
        # if formatted_date == today:
        #     article_links.append(link)
            
    return article_links

def scrape_each_article(link):
    try:
        content = get_html_content(link)
        soup = BeautifulSoup(content, 'lxml')
        
        
        article = soup.find('article', id='the-post')
        heading = article.h1.text
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        
        img_src = article.find('div', class_='featured-area-inner').img['src']
        img_path = user_download(img_src, heading_cleaned)
        
        article_contents = article.find_all('p')
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
                    "evbex" : 0,
                    "fmj" : 0,
                    "bmf" : 1,
                    "pfm" : 0,
                    "ifma" : 0,
                    "tomorrow" : 0,
                    "fmlink" : 0,
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
        
    content = get_html_content(BFM_LINK)
    
    articles = get_article_links(content)
    for article in articles:
        out = scrape_each_article(article)
        if out:
            contents.append(out)

    print(f"Number of articles from BFM: {len(contents)}")
    return contents
