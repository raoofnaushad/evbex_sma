from bs4 import BeautifulSoup

from src.config import *
from src.utils import *


def get_article_links(content):
    soup = BeautifulSoup(content, 'lxml')
    posts = soup.find('div', class_='posts')
    article_links = list()
    articles = posts.find_all('section',class_='article-item')
    with open('article_links.html', 'w') as file:
        file.write(str(articles))
    for article in articles:
        date_string = article.find('span',class_='tag').text
        formatted_date = format_facilitiesnet_date(str(date_string))
        # if True: # To add previous data
        if formatted_date==today:
            article_link=article.find('a')['href']
            article_links.append('https://www.facilitiesnet.com'+article_link)
    return article_links
    
def scrape_each_article(link):
    try:
        content = get_html_content(link, False)
        soup = BeautifulSoup(content, 'lxml')
        article = soup.find('div',id='article')
        with open('article_links.html', 'w') as file:
            file.write(str(article))
        
        heading = (article.find('h1',class_='headline').text).strip()
        print(heading)
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        figure_tag = soup.find('div', class_='articleDeckDiv')
        img_tag = figure_tag.find('img')
        if img_tag:
            data_src_value = img_tag['src']
        img_path = user_download(data_src_value, heading_cleaned, False)
        article_content = (article.find_all('p'))[2].text
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
                    "tomorrow" : 1,
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
        article = soup.find('div',id='article')
        with open('article_links.html', 'w') as file:
            file.write(str(article))
            
        heading = (article.find('h1',class_='headline').text).strip()
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        figure_tag = soup.find('div', class_='articleDeckDiv')
        img_tag = figure_tag.find('img')
        if img_tag:
            data_src_value = img_tag['src']
        img_path = user_download(data_src_value, heading_cleaned, False)
        article_content = (article.find_all('p'))[2].text
        date_string = article.find('div',{'style': 'float:right; font-size:.8em;'}).text
        if date_string:
        # Extract the date text
            date_parts = date_string.split(': ')[1].strip()        
            formatted_date = format_facilitiesnet_date(str(date_parts))
        
        img_path = user_download(data_src_value, heading_cleaned, False)
        article_name = heading
        
        db = connect_mong()
        coll = db.new_newsletter
        coll.delete_many({"date" : formatted_date, "tomorrow" : 1})
        
        print('Adding blogs of date:'+ formatted_date)
            
        content = {
                    "date" : formatted_date,
                    "article": article_name,
                    "image": img_path,
                    "image_src" : data_src_value,
                    "text": article_content.strip(),
                    "c2a_link": link,
                    "c2a_button": "Read from Source",
                    "facilio" : 0,
                    "qad" : 0,
                    "facilitiesnet" : 1,
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
    content = get_html_content(FACILITIESNET_LINK, False)
    # with open('article_links.html', 'w') as file:
    #         file.write(str(content))
    articles = get_article_links(content)
    for article in articles:
        content = scrape_each_article(article)
        # content = scrape_each_article_getData(article) # To add previous data
        if content:
            contents.append(content)
    print(f"Number of articles from FACILIO: {len(contents)}")
    return contents