from bs4 import BeautifulSoup

from src.config import *
from src.utils import *

def get_article_links(content):
    soup = BeautifulSoup(content, 'lxml')
    posts = soup.find('div', class_='col-12 col-sm-8 col-lg-9')
    article_links = []

    if posts is None:
        return article_links
    
    articles = posts.find_all('div', class_='sector-block')
    for article in articles:
        date_element = article.find('span', class_='meta')
        if date_element is None:
            continue
        
        date_string = date_element.text
        formatted_date = format_fmnaz_date(str(date_string))
        # You need to define 'today' here before using it in the comparison
        # Assuming today is a properly formatted date string
        
        # if True: # To add previous data
        if formatted_date == today:
            link_parent = article.find('div', class_='sector-block-text')
            if link_parent:
                article_link_element = link_parent.find('div', class_='col-12').a
                if article_link_element and 'href' in article_link_element.attrs:
                    article_link = article_link_element['href']
                    article_links.append(article_link)

    return article_links


def scrape_each_article_getData(link): # To add previous data
    try:
        content = get_html_content(link)
        soup = BeautifulSoup(content, 'lxml')
        article = soup.find('section',class_='personal-details')
        # with open('article_links.html', 'w') as file:
        #     file.write(str(article))
            
        post_date_parent = article.find('div',class_='content-left-block')
        post_date = post_date_parent.find_all('span')[1].text
        formatted_date = format_fmnaz_date(str(post_date))
        print('Adding blogs of date:',formatted_date)
        db = connect_mong()
        coll = db.new_newsletter
        coll.delete_many({"date" : formatted_date, "fmi":1}) # Earlier the key was fmj:1 and I ran it on production
        # coll.delete_many({"date" : formatted_date, "upkeep":1}) # uncomment this when you are deleting all key with fmj:1 => db.new_newsletter.deleteMany({"fmj":'1'})
        
        heading = article.h3.text
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        sub_main_header = soup.find('div', class_='content-right-block')
        if sub_main_header:
            data_src_value = sub_main_header.img['src']
        img_path = user_download(data_src_value, heading_cleaned)
        article_content = sub_main_header.find_all('p')[0].text
        article_name = heading  
        content = {
                    "date" : formatted_date,
                    "article": article_name,
                    "image": img_path,
                    "image_src" : data_src_value,
                    "text": article_content,
                    "c2a_link": link,
                    "c2a_button": "Read from Source",
                    "facilio" : 0,
                    "qad" : 0,
                    "upkeep" : 0,
                    "cleanmiddleeast": 1
                }
        
        return content
    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None
    
def scrape_each_article(link):
    try:
        content = get_html_content(link)
        soup = BeautifulSoup(content, 'lxml')
        article = soup.find('section',class_='personal-details')
        # with open('article_links.html', 'w') as file:
        #     file.write(str(article))

        heading = article.h3.text
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        sub_main_header = soup.find('div', class_='content-right-block')
        if sub_main_header:
            data_src_value = sub_main_header.img['src']
        img_path = user_download(data_src_value, heading_cleaned)
        article_content = sub_main_header.find_all('p')[0].text
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
                    "fmj" : 0,
                    "bmf" : 0,
                    "pfm" : 0,
                    "ifma" : 0,
                    "tomorrow" : 0,
                    "fmlink" : 0,
                    "iwfm" : 0,
                    "facmag" : 0,
                    "fmi" : 1

                }
        
        return content
    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None

def main():
    contents = list()
    content = get_html_content(CLEANMIDDLEEAST_LINK, False)
    # with open('article_links.html', 'w') as file:
    #     file.write(str(content))
    articles = get_article_links(content)
    for article in articles:
    # for article in articles[:15]: # To add previous data
        content = scrape_each_article(article)
        # content = scrape_each_article_getData(article) # To add previous data
        if content:
            contents.append(content)
    print(f"Number of articles from FMJ: {len(contents)}")
    return contents