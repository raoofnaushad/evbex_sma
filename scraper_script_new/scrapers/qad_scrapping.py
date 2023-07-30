from bs4 import BeautifulSoup

from src.config import *
from src.utils import *


def get_article_links(content):
    soup = BeautifulSoup(content, 'lxml')
    posts = soup.find('div', class_='td-ss-main-content')
    article_links = list()
    articles = posts.find_all('div',class_='td_module_10')
    # with open('article_links_1.html', 'w') as file:
    #         file.write(str(articles))
    for article in articles:
        date_string = article.find('time',class_='entry-date').text
        formatted_date = format_qad_date(str(date_string))
        # if True: # To add previous data
        if formatted_date==today:
            article_link=article.find('a')['href']
            article_links.append(article_link)
    return article_links
    
def scrape_each_article(link):
    try:
        content = get_html_content(link, False)
        soup = BeautifulSoup(content, 'lxml')
        with open('article_links.html', 'w') as file:
            file.write(str(soup))
        article = soup.find('article',class_='post')
        # with open('article_links.html', 'w') as file:
        #     file.write(str(article))
        
        heading = article.find('h1',class_='entry-title').text
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        img_tag = soup.find('img', class_='vc_single_image-img')
        # Get the value of the 'data-src' attribute
        if img_tag:
            data_src_value = img_tag['src']
            
        img_path = user_download(data_src_value, heading_cleaned, False)
        article_content = article.find('div', class_='wpb_wrapper').text
        article_name = heading 
        content = {
                    "date" : today,
                    "article": article_name,
                    "image": img_path,
                    "image_src" : data_src_value,
                    "text": article_content,
                    "c2a_link": link,
                    "c2a_button": "Read from Source",
                    "evbex" : 0,
                    "fmj" : 1,
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
    
def scrape_each_article_getData(link): # To add previous data
    try:
        content = get_html_content(link, False)
        soup = BeautifulSoup(content, 'lxml')
        with open('article_links.html', 'w') as file:
            file.write(str(soup))
        article = soup.find('article',class_='post')
        with open('article_links.html', 'w') as file:
            file.write(str(article))
        
        heading = article.find('h1',class_='entry-title').text
        date = article.find('time',class_='entry-date').text
        formatted_date = format_qad_date(str(date))
        db = connect_mong()
        coll = db.new_newsletter
        coll.delete_many({"date" : formatted_date, "iwfm" : 1})
        print('Adding blogs of date'+ formatted_date)
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        img_tag = soup.find('img', class_='vc_single_image-img')
        # Get the value of the 'data-src' attribute
        if img_tag:
            data_src_value = img_tag['src']
            
        img_path = user_download(data_src_value, heading_cleaned, False)
        article_content = article.find('div', class_='wpb_wrapper').text
        article_name = heading 
        content = {
                    "date" : formatted_date,
                    "article": article_name,
                    "image": img_path,
                    "image_src" : data_src_value,
                    "text": article_content,
                    "c2a_link": link,
                    "c2a_button": "Read from Source",
                    "evbex" : 0,
                    "fmj" : 0,
                    "bmf" : 0,
                    "pfm" : 0,
                    "ifma" : 0,
                    "tomorrow" : 0,
                    "fmlink" : 0,
                    "iwfm" : 1,
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
        
    content = get_html_content(QAD_LINK, False)
    articles = get_article_links(content)
    for article in articles:
        content = scrape_each_article(article)
        # content = scrape_each_article_getData(article) # To add previous data
        if content:
            contents.append(content)
    print(f"Number of articles from QAD: {len(contents)}")
    return contents