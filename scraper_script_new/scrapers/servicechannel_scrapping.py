from bs4 import BeautifulSoup

from src.config import *
from src.utils import *
import datetime


def get_article_links(content):
    soup = BeautifulSoup(content, 'lxml')
    posts = soup.find('div', class_='list__body')
    article_links = list()
    articles = posts.find_all('article',class_='article-main')
    # with open('article_links.html', 'w') as file:
    #     file.write(str(articles))
    for article in articles:
        article_link=article.find('a')['href']
        article_links.append(article_link)
    return article_links
    
def scrape_each_article(link):
    try:
        content = get_html_content(link, False)
        article = BeautifulSoup(content, 'lxml')

        
        heading = (article.find('div',class_='post__head-title').text).strip()
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        figure_tag = article.find('picture', class_='attachment-app-full')
        img_tag = figure_tag.find('img')
        if img_tag:
            data_src_value = img_tag['src']
        img_path = user_download(data_src_value, heading_cleaned, False)
        content_tag = article.find('div', class_='post__entry')
        article_content = (content_tag.find_all('p'))[0].text
        article_name = heading
        content = {
                    "date" : today,
                    "article": article_name,
                    "image": img_path,
                    "image_src" : data_src_value,
                    "text": article_content.strip(),
                    "c2a_link": link,
                    "c2a_button": "Read from Source",
                    "evbex" : 1,
                    "fmj" : 0,
                    "bmf" : 0,
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
    

def main():
    contents = list()
    content = get_html_content(SERVICECHANNEL_LINK, False)
    # with open('article_links.html', 'w') as file:
    #         file.write(str(content))
    articles = get_article_links(content)
    
    current_date = datetime.date.today() + datetime.timedelta(days=1)
    next_link = get_next_link_by_date(articles, current_date)
    content = scrape_each_article(next_link)
    if content:
        contents.append(content)
    print(f"Number of articles from SERVICECHANNEL: {len(contents)}")
    return contents