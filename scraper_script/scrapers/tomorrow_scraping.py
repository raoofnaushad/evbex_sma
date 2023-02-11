
from bs4 import BeautifulSoup

from src.config import *
from src.utils import *

def get_article_links(content):
    article_links = list()
    soup = BeautifulSoup(content, 'lxml')
    
    posts = soup.find_all('div', class_="newsItem")

    for article in posts:
        link = article.a['href']
        article_links.append(link)
    
    return article_links


def scrape_each_article(link):
    try:
        # print("**********************")
        # print(link)
        # print("**********************")
        content = get_html_content(link)
        article = BeautifulSoup(content, 'lxml')
        date_str  = article.find('div', class_='contentDate').text
        date = format_tmrw_date(date_str)

        if date == today:
            heading = article.find('div', class_='contentHeading').h1.text
            heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
            
            img_src = article.find('div', class_='imgCENTRE').img['src']
            img_src = "https://www.tomorrowsfm.com/" + '/' + img_src
            img_path = user_download(img_src, heading_cleaned)

            article_content_main = article.find('div', class_='content')
            article_content_1 = article_content_main.find_all('p')[0].text        
            article_content_2 = article_content_main.find_all('p')[1].text        
            article_content = article_content_1 + '\n' + article_content_2 

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
        
    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None

def main():
    contents = list()
        
    content = get_html_content(TOMORROW_FM_LINK)
    
    articles = get_article_links(content)
    
    for article in articles:
        out = scrape_each_article(article)
        if out:
            contents.append(out)

    print(f"Number of articles from TomorrowScraping: {len(contents)}")

    return contents

