
from bs4 import BeautifulSoup

from src.config import *
from src.utils import *

bad_chars = [';', ':', '!', "*", "'", "\n", "‘", "’"]

def get_article_links(content):
    article_links = list()
    soup = BeautifulSoup(content, 'lxml')
    
    posts = soup.find_all('div', class_="teaser__content")
    for post in posts:
        date = post.find('div', class_="teaser__content-main__header__date")
        formatted_date = format_facilitate_date(date.span.text)
        if formatted_date == today:
            article_links.append("https://www.facilitatemagazine.com"+post.a['href'])
    
    return article_links


def scrape_each_article(link):
    try:
        # print("**********************")
        # print(link)
        # print("**********************")
        content = get_html_content(link)
        article = BeautifulSoup(content, 'lxml')
        heading = article.find('h1', class_ = "page-title").text
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        
        for i in bad_chars:
            heading = heading.replace(i, '')
        img_src = "https://www.facilitatemagazine.com/" + article.find('div', class_ = 'media-image-field').img['src']
        
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
            "fmj" : 0
        }
        print(content)
        return content
        
    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None

def main():
    contents = list()
        
    content = get_html_content(FACILITATE_MAG)
    #print(content)
    
    articles = get_article_links(content)
    
    for article in articles:
        out = scrape_each_article(article)
        if out:
            contents.append(out)

    print(f"Number of articles from FacilityMag: {len(contents)}") 
    return contents

